"""
Canonical mutation planning for Data Management.

This module owns the controlled administrative mutation boundary for
daily_prices.

This module owns:

- canonical OHLCV record normalization
- structural hard validation
- non-blocking validation warnings
- row-fatal excluded-observation handling
- plan-fatal duplicate incoming-key detection
- comparison against authoritative daily_prices
- New / Unchanged / Changed classification
- operation-aware proposed actions
- materialized Preview-plan data
- database-baseline fingerprinting
- exact Preview-plan identity
- explicit Preview confirmation binding
- atomic daily_prices mutation plus audit persistence

This module does NOT yet:

- acquire market data from yFinance
- render Streamlit mutation controls
- replace existing legacy dashboard acquisition/persistence paths

The public Commit boundary accepts only an explicitly confirmed materialized
Preview plan. It does not refetch or reinterpret the originating request.

Audit-schema initialization is explicit infrastructure setup and is separate
from the Preview -> Confirm -> Commit mutation transaction.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
import hashlib
import json
import math
from pathlib import Path
import sqlite3
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple

from src.config.settings import DATABASE_FILE, TABLE_NAME
from src.data.market_calendar import (
    get_expected_sessions,
    get_latest_expected_stored_session,
)


AUDIT_TABLE_NAME = "data_management_audit"

AUDIT_REQUIRED_COLUMNS: Tuple[str, ...] = (
    "id",
    "timestamp",
    "action",
    "ticker",
    "start_date",
    "end_date",
    "source",
    "rows_affected",
    "plan_fingerprint",
    "details",
)


CANONICAL_FIELDS: Tuple[str, ...] = (
    "Ticker",
    "Date",
    "Open",
    "High",
    "Low",
    "Close",
    "Adj Close",
    "Volume",
)

PRICE_FIELDS: Tuple[str, ...] = (
    "Open",
    "High",
    "Low",
    "Close",
    "Adj Close",
)

PERSISTED_VALUE_FIELDS: Tuple[str, ...] = (
    "Open",
    "High",
    "Low",
    "Close",
    "Adj Close",
    "Volume",
)

PRESERVE_EXISTING_OPERATIONS = frozenset(
    {
        "Add",
        "Update to Current",
        "Backfill Earlier",
        "Repair Missing",
        "Manual Add",
    }
)

REPLACEMENT_ELIGIBLE_OPERATIONS = frozenset(
    {
        "Replace Range",
        "Refresh Existing Coverage",
        "Manual Replace",
    }
)

CANDIDATE_RECORD_OPERATIONS = (
    PRESERVE_EXISTING_OPERATIONS
    | REPLACEMENT_ELIGIBLE_OPERATIONS
)

DELETION_OPERATIONS = frozenset(
    {
        "Delete Range",
        "Delete Ticker",
    }
)


@dataclass(frozen=True)
class CanonicalOHLCVRecord:
    """One canonical daily_prices observation."""

    ticker: str
    date: date
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: int

    @property
    def key(self) -> Tuple[str, date]:
        """Return the logical daily_prices identity."""
        return (self.ticker, self.date)

    def persisted_values(self) -> Tuple[Any, ...]:
        """Return values participating in stored-record equality."""
        return (
            self.open,
            self.high,
            self.low,
            self.close,
            self.adj_close,
            self.volume,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Return the canonical stored-column representation."""
        return {
            "Ticker": self.ticker,
            "Date": self.date.isoformat(),
            "Open": self.open,
            "High": self.high,
            "Low": self.low,
            "Close": self.close,
            "Adj Close": self.adj_close,
            "Volume": self.volume,
        }


@dataclass(frozen=True)
class ValidationIssue:
    """One hard-validation problem discovered during plan construction."""

    code: str
    message: str
    candidate_index: Optional[int] = None
    ticker: Optional[str] = None
    date: Optional[str] = None


@dataclass(frozen=True)
class ValidationWarning:
    """
    One non-blocking validation finding discovered during plan construction.

    Warnings are part of the exact Preview that the user confirms, but they
    do not make an otherwise valid MutationPlan ineligible for Commit.
    """

    code: str
    message: str
    candidate_index: Optional[int] = None
    ticker: Optional[str] = None
    date: Optional[str] = None


@dataclass(frozen=True)
class ExcludedObservation:
    """
    One returned source candidate excluded from mutation because that
    individual observation failed canonical validation.

    Exclusion is row-fatal, not plan-fatal. The observation remains visible
    in Preview and audit but never becomes a PlannedObservation and is never
    written to daily_prices.
    """

    candidate_index: int
    ticker: Optional[str]
    date: Optional[str]
    issues: Tuple[ValidationIssue, ...]


@dataclass(frozen=True)
class PlannedObservation:
    """
    Comparison result for one unambiguous canonical candidate record.

    classification:
        New
        Unchanged
        Changed

    planned_action:
        insert
        no_change
        preserve_existing
        replacement_candidate
    """

    candidate: CanonicalOHLCVRecord
    classification: str
    planned_action: str
    collision: bool
    existing: Optional[CanonicalOHLCVRecord] = None
    differing_fields: Tuple[str, ...] = ()


@dataclass(frozen=True)
class PlannedDeletion:
    """
    One exact authoritative OHLCV record materialized for explicit deletion.

    The stored record is captured in full so Preview identity is bound to the
    exact database state reviewed by the administrator.
    """

    record: CanonicalOHLCVRecord
    planned_action: str = "delete"


@dataclass(frozen=True)
class SourceMissingObservation:
    """
    One expected NYSE observation absent from the supplied source candidates.

    planned_action:
        preserve_existing
            The authoritative DB already contains this observation. Source
            omission does not authorize replacement or deletion.

        unresolved
            Neither the supplied source candidates nor the authoritative DB
            contain the expected observation.
    """

    ticker: str
    date: date
    planned_action: str
    existing: Optional[CanonicalOHLCVRecord] = None

    @property
    def key(self) -> Tuple[str, date]:
        """Return the logical daily_prices identity."""
        return (self.ticker, self.date)


@dataclass(frozen=True)
class MutationPlan:
    """
    Materialized read-only Preview plan.

    The plan captures exact mutation actions, materialized deletion targets,
    Source Missing observations, excluded invalid observations, warnings,
    plan-fatal validation issues, and the authoritative DB baseline used for
    Preview.
    """

    operation: str
    source: str
    requested_tickers: Tuple[str, ...]
    requested_start_date: Optional[date]
    requested_end_date: Optional[date]
    observations: Tuple[PlannedObservation, ...]
    deletions: Tuple[PlannedDeletion, ...]
    source_missing: Tuple[SourceMissingObservation, ...]
    excluded_observations: Tuple[ExcludedObservation, ...]
    validation_issues: Tuple[ValidationIssue, ...]
    validation_warnings: Tuple[ValidationWarning, ...]
    duplicate_keys: Tuple[Tuple[str, date], ...]
    source_missing_keys: Tuple[Tuple[str, date], ...]
    baseline_fingerprint: str
    plan_fingerprint: str
    latest_expected_stored_session: date
    created_at: datetime

    @property
    def can_commit(self) -> bool:
        """
        Return whether plan-fatal validation permits Commit.

        Row-fatal excluded observations and non-blocking warnings remain
        visible in Preview but do not make the remaining valid plan ineligible.

        An explicit deletion with no stored rows is not commit-eligible.
        """
        if (
            self.operation in DELETION_OPERATIONS
            and not self.deletions
        ):
            return False

        return (
            not self.validation_issues
            and not self.duplicate_keys
        )

    def summary(self) -> Dict[str, int]:
        """Return compact Preview counts by comparison/action state."""
        classifications = {
            "new": 0,
            "unchanged": 0,
            "changed": 0,
        }
        actions = {
            "insert": 0,
            "no_change": 0,
            "preserve_existing": 0,
            "replacement_candidate": 0,
            "delete": len(self.deletions),
        }

        for observation in self.observations:
            classification_key = observation.classification.lower()
            if classification_key in classifications:
                classifications[classification_key] += 1

            if observation.planned_action in actions:
                actions[observation.planned_action] += 1

        source_missing_preserved = sum(
            1
            for item in self.source_missing
            if item.planned_action == "preserve_existing"
        )
        source_missing_unresolved = sum(
            1
            for item in self.source_missing
            if item.planned_action == "unresolved"
        )

        excluded_validation_issues = sum(
            len(item.issues)
            for item in self.excluded_observations
        )

        return {
            **classifications,
            **actions,
            "validation_issues": len(self.validation_issues),
            "validation_warnings": len(self.validation_warnings),
            "excluded_observations": len(self.excluded_observations),
            "excluded_validation_issues": excluded_validation_issues,
            "duplicate_keys": len(self.duplicate_keys),
            "source_missing": len(self.source_missing_keys),
            "source_missing_preserved": source_missing_preserved,
            "source_missing_unresolved": source_missing_unresolved,
        }


@dataclass(frozen=True)
class PlanFreshnessCheck:
    """
    Read-only comparison between a Preview plan's stored DB baseline and
    the current authoritative database state.

    changed_keys contains only logical (Ticker, Date) identities whose
    current stored state no longer matches the state used to create Preview.
    """

    is_current: bool
    expected_fingerprint: str
    current_fingerprint: str
    changed_keys: Tuple[Tuple[str, date], ...]


@dataclass(frozen=True)
class AuditSchemaStatus:
    """
    Read-only status of the Data Management administrative audit table.

    compatible=True means the table exists and exposes every column required
    by the current Data Management audit contract.
    """

    exists: bool
    compatible: bool
    columns: Tuple[str, ...]
    missing_columns: Tuple[str, ...]


@dataclass(frozen=True)
class MutationTransactionResult:
    """
    Result of one successfully committed MutationPlan transaction.

    Returned by the public Commit boundary after atomic data and audit
    persistence succeeds.
    """

    rows_affected: int
    audit_id: int


class DataMutationManager:
    """
    Canonical Data Management administrative mutation owner.

    Owns read-only Preview planning, explicit audit-schema infrastructure,
    exact Preview confirmation, controlled daily_prices mutation, and atomic
    audit persistence.
    """

    def __init__(
        self,
        database_file: str = DATABASE_FILE,
        table_name: str = TABLE_NAME,
        audit_table_name: str = AUDIT_TABLE_NAME,
    ) -> None:
        self.database_path = Path(database_file)
        self.table_name = str(table_name)
        self.audit_table_name = str(audit_table_name)

    def _connect_read_only(self) -> sqlite3.Connection:
        """Open the authoritative database in explicit read-only mode."""
        database_uri = self.database_path.resolve().as_uri() + "?mode=ro"

        connection = sqlite3.connect(
            database_uri,
            uri=True,
        )
        connection.row_factory = sqlite3.Row
        return connection

    def _connect_write(self) -> sqlite3.Connection:
        """
        Open the configured SQLite database for explicit Data Management writes.

        Merely opening this connection does not mutate persistent state.
        Mutation and schema methods must own their transaction boundaries
        explicitly.
        """
        connection = sqlite3.connect(
            self.database_path
        )
        connection.row_factory = sqlite3.Row
        return connection

    def _get_audit_schema_status_from_connection(
        self,
        connection: sqlite3.Connection,
    ) -> AuditSchemaStatus:
        """
        Inspect audit-table readiness using an existing SQLite connection.

        This supports both ordinary read-only inspection and the controlled
        mutation transaction without opening a second database connection.
        """
        table_row = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name = ?
            """,
            (self.audit_table_name,),
        ).fetchone()

        if table_row is None:
            return AuditSchemaStatus(
                exists=False,
                compatible=False,
                columns=(),
                missing_columns=AUDIT_REQUIRED_COLUMNS,
            )

        pragma_rows = connection.execute(
            f'PRAGMA table_info("{self.audit_table_name}")'
        ).fetchall()

        columns = tuple(
            str(row["name"])
            for row in pragma_rows
        )

        column_set = set(columns)

        missing_columns = tuple(
            column_name
            for column_name in AUDIT_REQUIRED_COLUMNS
            if column_name not in column_set
        )

        return AuditSchemaStatus(
            exists=True,
            compatible=not missing_columns,
            columns=columns,
            missing_columns=missing_columns,
        )

    def get_audit_schema_status(self) -> AuditSchemaStatus:
        """
        Return read-only audit-table readiness information.

        This method never creates, alters, or drops database objects.
        """
        connection = self._connect_read_only()

        try:
            return self._get_audit_schema_status_from_connection(
                connection
            )
        finally:
            connection.close()

    def initialize_audit_schema(self) -> AuditSchemaStatus:
        """
        Explicitly create the Data Management audit table when absent.

        This operation initializes administrative infrastructure only.
        It does not mutate daily_prices and does not create an audit event.

        If a table with the configured audit-table name already exists but
        does not satisfy the required column contract, the method raises
        rather than silently altering that table.
        """
        existing_status = self.get_audit_schema_status()

        if existing_status.exists:
            if not existing_status.compatible:
                raise RuntimeError(
                    "Existing Data Management audit table is incompatible. "
                    "Missing required column(s): "
                    + ", ".join(existing_status.missing_columns)
                )

            return existing_status

        create_sql = f"""
            CREATE TABLE "{self.audit_table_name}" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                action TEXT NOT NULL,
                ticker TEXT,
                start_date TEXT,
                end_date TEXT,
                source TEXT NOT NULL,
                rows_affected INTEGER NOT NULL,
                plan_fingerprint TEXT NOT NULL,
                details TEXT
            )
        """

        connection = self._connect_write()

        try:
            connection.execute("BEGIN")
            connection.execute(create_sql)
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

        created_status = self.get_audit_schema_status()

        if not created_status.compatible:
            raise RuntimeError(
                "Data Management audit table was created but did not "
                "satisfy the required schema contract."
            )

        return created_status

    @staticmethod
    def _normalize_date_value(value: Any) -> date:
        """Normalize a supported date-like value to a plain date."""
        if isinstance(value, datetime):
            return value.date()

        if isinstance(value, date):
            return value

        if isinstance(value, str):
            normalized = value.strip()
            if not normalized:
                raise ValueError("Date is required.")
            try:
                return date.fromisoformat(normalized)
            except ValueError as exc:
                raise ValueError(
                    "Date must use YYYY-MM-DD format."
                ) from exc

        raise ValueError(
            "Date must be a date, datetime, or YYYY-MM-DD string."
        )

    @staticmethod
    def _normalize_finite_float(
        field_name: str,
        value: Any,
    ) -> float:
        """Normalize one required finite numeric price value."""
        if value is None or isinstance(value, bool):
            raise ValueError(f"{field_name} must be a finite numeric value.")

        try:
            numeric_value = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"{field_name} must be a finite numeric value."
            ) from exc

        if not math.isfinite(numeric_value):
            raise ValueError(
                f"{field_name} must be a finite numeric value."
            )

        return numeric_value

    @staticmethod
    def _normalize_volume(value: Any) -> int:
        """Normalize Volume to a finite, non-negative integer."""
        if value is None or isinstance(value, bool):
            raise ValueError(
                "Volume must be a finite non-negative integer."
            )

        try:
            numeric_value = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                "Volume must be a finite non-negative integer."
            ) from exc

        if (
            not math.isfinite(numeric_value)
            or numeric_value < 0
            or not numeric_value.is_integer()
        ):
            raise ValueError(
                "Volume must be a finite non-negative integer."
            )

        return int(numeric_value)

    @staticmethod
    def _normalize_requested_tickers(
        tickers: Optional[Iterable[Any]],
    ) -> Tuple[str, ...]:
        """Normalize requested ticker scope while preserving input order."""
        if tickers is None:
            return ()

        normalized_tickers: List[str] = []
        seen = set()

        for value in tickers:
            ticker = str(value or "").strip().upper()

            if not ticker or ticker in seen:
                continue

            seen.add(ticker)
            normalized_tickers.append(ticker)

        return tuple(normalized_tickers)

    @classmethod
    def _normalize_candidate(
        cls,
        candidate: Mapping[str, Any],
        candidate_index: int,
        latest_expected_stored_session: date,
    ) -> Tuple[
        Optional[CanonicalOHLCVRecord],
        List[ValidationIssue],
        List[ValidationWarning],
    ]:
        """
        Normalize one candidate into the canonical record contract.

        Hard validation:
        - canonical structure and types
        - valid persistence date
        - finite, strictly positive prices
        - finite non-negative integer Volume

        Non-blocking validation:
        - raw OHLC envelope inconsistencies

        Warnings remain part of Preview but do not prevent Commit.
        """
        issues: List[ValidationIssue] = []
        warnings: List[ValidationWarning] = []

        if not isinstance(candidate, Mapping):
            return (
                None,
                [
                    ValidationIssue(
                        code="invalid_candidate_type",
                        message=(
                            "Candidate must be a mapping containing the "
                            "canonical OHLCV fields."
                        ),
                        candidate_index=candidate_index,
                    )
                ],
                [],
            )

        missing_fields = [
            field_name
            for field_name in CANONICAL_FIELDS
            if field_name not in candidate
        ]

        if missing_fields:
            return (
                None,
                [
                    ValidationIssue(
                        code="missing_required_fields",
                        message=(
                            "Missing required field(s): "
                            + ", ".join(missing_fields)
                        ),
                        candidate_index=candidate_index,
                    )
                ],
                [],
            )

        raw_ticker = candidate.get("Ticker")
        ticker = str(raw_ticker or "").strip().upper()

        if not ticker:
            issues.append(
                ValidationIssue(
                    code="invalid_ticker",
                    message="Ticker is required.",
                    candidate_index=candidate_index,
                )
            )

        normalized_date: Optional[date] = None

        try:
            normalized_date = cls._normalize_date_value(
                candidate.get("Date")
            )
        except ValueError as exc:
            issues.append(
                ValidationIssue(
                    code="invalid_date",
                    message=str(exc),
                    candidate_index=candidate_index,
                    ticker=ticker or None,
                )
            )

        if (
            normalized_date is not None
            and normalized_date > latest_expected_stored_session
        ):
            issues.append(
                ValidationIssue(
                    code="future_or_incomplete_session",
                    message=(
                        f"{normalized_date.isoformat()} is later than "
                        "the Latest Expected Stored Session "
                        f"({latest_expected_stored_session.isoformat()})."
                    ),
                    candidate_index=candidate_index,
                    ticker=ticker or None,
                    date=normalized_date.isoformat(),
                )
            )

        normalized_prices: Dict[str, float] = {}

        for field_name in PRICE_FIELDS:
            try:
                normalized_prices[field_name] = (
                    cls._normalize_finite_float(
                        field_name,
                        candidate.get(field_name),
                    )
                )
            except ValueError as exc:
                issues.append(
                    ValidationIssue(
                        code="invalid_numeric_value",
                        message=str(exc),
                        candidate_index=candidate_index,
                        ticker=ticker or None,
                        date=(
                            normalized_date.isoformat()
                            if normalized_date is not None
                            else None
                        ),
                    )
                )

        for field_name, numeric_value in normalized_prices.items():
            if numeric_value <= 0:
                issues.append(
                    ValidationIssue(
                        code="non_positive_price",
                        message=(
                            f"{field_name} must be strictly greater than zero; "
                            f"received {numeric_value}."
                        ),
                        candidate_index=candidate_index,
                        ticker=ticker or None,
                        date=(
                            normalized_date.isoformat()
                            if normalized_date is not None
                            else None
                        ),
                    )
                )

        normalized_volume: Optional[int] = None

        try:
            normalized_volume = cls._normalize_volume(
                candidate.get("Volume")
            )
        except ValueError as exc:
            issues.append(
                ValidationIssue(
                    code="invalid_volume",
                    message=str(exc),
                    candidate_index=candidate_index,
                    ticker=ticker or None,
                    date=(
                        normalized_date.isoformat()
                        if normalized_date is not None
                        else None
                    ),
                )
            )

        if not issues:
            open_value = normalized_prices["Open"]
            high_value = normalized_prices["High"]
            low_value = normalized_prices["Low"]
            close_value = normalized_prices["Close"]

            ohlc_warning_specs = (
                (
                    high_value < open_value,
                    "high_below_open",
                    (
                        f"High ({high_value}) is below Open "
                        f"({open_value})."
                    ),
                ),
                (
                    high_value < close_value,
                    "high_below_close",
                    (
                        f"High ({high_value}) is below Close "
                        f"({close_value})."
                    ),
                ),
                (
                    high_value < low_value,
                    "high_below_low",
                    (
                        f"High ({high_value}) is below Low "
                        f"({low_value})."
                    ),
                ),
                (
                    low_value > open_value,
                    "low_above_open",
                    (
                        f"Low ({low_value}) is above Open "
                        f"({open_value})."
                    ),
                ),
                (
                    low_value > close_value,
                    "low_above_close",
                    (
                        f"Low ({low_value}) is above Close "
                        f"({close_value})."
                    ),
                ),
            )

            for (
                condition,
                warning_code,
                warning_message,
            ) in ohlc_warning_specs:
                if condition:
                    warnings.append(
                        ValidationWarning(
                            code=warning_code,
                            message=warning_message,
                            candidate_index=candidate_index,
                            ticker=ticker or None,
                            date=(
                                normalized_date.isoformat()
                                if normalized_date is not None
                                else None
                            ),
                        )
                    )

        if issues:
            return None, issues, warnings

        assert normalized_date is not None
        assert normalized_volume is not None

        return (
            CanonicalOHLCVRecord(
                ticker=ticker,
                date=normalized_date,
                open=normalized_prices["Open"],
                high=normalized_prices["High"],
                low=normalized_prices["Low"],
                close=normalized_prices["Close"],
                adj_close=normalized_prices["Adj Close"],
                volume=normalized_volume,
            ),
            [],
            warnings,
        )

    @classmethod
    def _extract_candidate_identity(
        cls,
        candidate: Any,
    ) -> Optional[Tuple[str, date]]:
        """
        Return a usable (Ticker, Date) identity even when other candidate
        fields later fail validation.

        Source Missing means the source did not return the observation at all.
        A returned-but-invalid observation must remain Invalid rather than also
        being mislabeled Source Missing.
        """
        if not isinstance(candidate, Mapping):
            return None

        ticker = str(
            candidate.get("Ticker") or ""
        ).strip().upper()

        if not ticker:
            return None

        try:
            record_date = cls._normalize_date_value(
                candidate.get("Date")
            )
        except ValueError:
            return None

        return (ticker, record_date)

    @staticmethod
    def _find_duplicate_keys(
        indexed_identities: Iterable[
            Tuple[int, Tuple[str, date]]
        ],
    ) -> Dict[Tuple[str, date], List[int]]:
        """
        Return usable incoming logical identities appearing more than once.

        Duplicate detection is identity-based rather than dependent on full
        canonical normalization. Therefore a malformed returned observation
        cannot hide a duplicate (Ticker, Date) collision.
        """
        indexes_by_key: Dict[Tuple[str, date], List[int]] = {}

        for candidate_index, candidate_key in indexed_identities:
            indexes_by_key.setdefault(
                candidate_key,
                [],
            ).append(candidate_index)

        return {
            key: indexes
            for key, indexes in indexes_by_key.items()
            if len(indexes) > 1
        }

    def _load_existing_records_from_connection(
        self,
        connection: sqlite3.Connection,
        keys: Iterable[Tuple[str, date]],
    ) -> Dict[Tuple[str, date], CanonicalOHLCVRecord]:
        """
        Load authoritative rows for exact logical keys using an existing
        SQLite connection.

        This is required for stale-plan verification inside the same
        transaction that will perform the approved mutation.
        """
        key_set = set(keys)

        if not key_set:
            return {}

        dates_by_ticker: Dict[str, List[date]] = {}

        for ticker, record_date in key_set:
            dates_by_ticker.setdefault(
                ticker,
                [],
            ).append(record_date)

        existing_records: Dict[
            Tuple[str, date],
            CanonicalOHLCVRecord,
        ] = {}

        query = f"""
            SELECT
                Ticker,
                Date,
                Open,
                High,
                Low,
                Close,
                "Adj Close",
                Volume
            FROM "{self.table_name}"
            WHERE Ticker = ?
              AND Date >= ?
              AND Date <= ?
            ORDER BY Date
        """

        for ticker, ticker_dates in dates_by_ticker.items():
            range_start = min(ticker_dates)
            range_end = max(ticker_dates)

            rows = connection.execute(
                query,
                (
                    ticker,
                    range_start.isoformat(),
                    range_end.isoformat(),
                ),
            ).fetchall()

            for row in rows:
                row_date = date.fromisoformat(
                    str(row["Date"])
                )

                row_key = (
                    str(row["Ticker"]).strip().upper(),
                    row_date,
                )

                if row_key not in key_set:
                    continue

                existing_records[row_key] = (
                    CanonicalOHLCVRecord(
                        ticker=row_key[0],
                        date=row_date,
                        open=float(row["Open"]),
                        high=float(row["High"]),
                        low=float(row["Low"]),
                        close=float(row["Close"]),
                        adj_close=float(row["Adj Close"]),
                        volume=int(row["Volume"]),
                    )
                )

        return existing_records

    def _load_existing_records(
        self,
        keys: Iterable[Tuple[str, date]],
    ) -> Dict[Tuple[str, date], CanonicalOHLCVRecord]:
        """
        Load authoritative rows for candidate keys using a dedicated
        read-only connection.
        """
        connection = self._connect_read_only()

        try:
            return self._load_existing_records_from_connection(
                connection,
                keys,
            )
        finally:
            connection.close()

    def _load_deletion_scope_from_connection(
        self,
        connection: sqlite3.Connection,
        *,
        ticker: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> Tuple[CanonicalOHLCVRecord, ...]:
        """
        Load the complete authoritative OHLCV set for one deletion scope.

        Supplying no dates means the complete stored ticker. Supplying both
        dates means one inclusive stored ticker/date range.
        """
        if (start_date is None) != (end_date is None):
            raise ValueError(
                "Deletion scope requires both Start Date and End Date "
                "or neither."
            )

        if start_date is None:
            rows = connection.execute(
                f"""
                SELECT
                    Ticker,
                    Date,
                    Open,
                    High,
                    Low,
                    Close,
                    "Adj Close",
                    Volume
                FROM "{self.table_name}"
                WHERE Ticker = ?
                ORDER BY Date
                """,
                (ticker,),
            ).fetchall()
        else:
            assert end_date is not None

            rows = connection.execute(
                f"""
                SELECT
                    Ticker,
                    Date,
                    Open,
                    High,
                    Low,
                    Close,
                    "Adj Close",
                    Volume
                FROM "{self.table_name}"
                WHERE Ticker = ?
                  AND Date >= ?
                  AND Date <= ?
                ORDER BY Date
                """,
                (
                    ticker,
                    start_date.isoformat(),
                    end_date.isoformat(),
                ),
            ).fetchall()

        return tuple(
            CanonicalOHLCVRecord(
                ticker=str(row["Ticker"]).strip().upper(),
                date=date.fromisoformat(str(row["Date"])),
                open=float(row["Open"]),
                high=float(row["High"]),
                low=float(row["Low"]),
                close=float(row["Close"]),
                adj_close=float(row["Adj Close"]),
                volume=int(row["Volume"]),
            )
            for row in rows
        )

    def _load_deletion_scope(
        self,
        *,
        ticker: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> Tuple[CanonicalOHLCVRecord, ...]:
        """Load one deletion scope through a dedicated read-only connection."""
        connection = self._connect_read_only()

        try:
            return self._load_deletion_scope_from_connection(
                connection,
                ticker=ticker,
                start_date=start_date,
                end_date=end_date,
            )
        finally:
            connection.close()

    @staticmethod
    def _differing_fields(
        candidate: CanonicalOHLCVRecord,
        existing: CanonicalOHLCVRecord,
    ) -> Tuple[str, ...]:
        """Return persisted fields whose canonical values differ."""
        candidate_values = candidate.to_dict()
        existing_values = existing.to_dict()

        return tuple(
            field_name
            for field_name in PERSISTED_VALUE_FIELDS
            if candidate_values[field_name] != existing_values[field_name]
        )

    @staticmethod
    def _planned_action(
        operation: str,
        classification: str,
    ) -> str:
        """Resolve the non-mutating proposed action for Preview."""
        if classification == "New":
            return "insert"

        if classification == "Unchanged":
            return "no_change"

        if operation in PRESERVE_EXISTING_OPERATIONS:
            return "preserve_existing"

        return "replacement_candidate"

    @staticmethod
    def _build_baseline_fingerprint(
        candidate_keys: Iterable[Tuple[str, date]],
        existing_records: Mapping[
            Tuple[str, date],
            CanonicalOHLCVRecord,
        ],
    ) -> str:
        """
        Return a deterministic fingerprint of the DB state used for Preview.

        Missing keys are represented explicitly so a future row appearing
        between Preview and Commit can invalidate the old plan.
        """
        baseline_rows: List[Dict[str, Any]] = []

        for ticker, record_date in sorted(
            set(candidate_keys),
            key=lambda item: (item[0], item[1]),
        ):
            key = (ticker, record_date)
            existing = existing_records.get(key)

            baseline_rows.append(
                {
                    "Ticker": ticker,
                    "Date": record_date.isoformat(),
                    "Existing": (
                        existing.to_dict()
                        if existing is not None
                        else None
                    ),
                }
            )

        serialized = json.dumps(
            baseline_rows,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        )

        return hashlib.sha256(
            serialized.encode("utf-8")
        ).hexdigest()

    @staticmethod
    def _build_plan_fingerprint(
        *,
        operation: str,
        source: str,
        requested_tickers: Tuple[str, ...],
        requested_start_date: Optional[date],
        requested_end_date: Optional[date],
        observations: Tuple[PlannedObservation, ...],
        deletions: Tuple[PlannedDeletion, ...],
        source_missing: Tuple[SourceMissingObservation, ...],
        excluded_observations: Tuple[ExcludedObservation, ...],
        validation_issues: Tuple[ValidationIssue, ...],
        validation_warnings: Tuple[ValidationWarning, ...],
        duplicate_keys: Tuple[Tuple[str, date], ...],
        source_missing_keys: Tuple[Tuple[str, date], ...],
        baseline_fingerprint: str,
        latest_expected_stored_session: date,
    ) -> str:
        """
        Return the deterministic identity of one materialized Preview plan.

        Unlike baseline_fingerprint, this binds confirmation to the complete
        approved Preview semantics: operation, source, scope, candidates,
        classifications, planned actions, validation state, Source Missing
        state, and the DB baseline on which Preview was built.

        created_at is intentionally excluded from identity.
        """
        payload = {
            "operation": operation,
            "source": source,
            "requested_tickers": list(requested_tickers),
            "requested_start_date": (
                requested_start_date.isoformat()
                if requested_start_date is not None
                else None
            ),
            "requested_end_date": (
                requested_end_date.isoformat()
                if requested_end_date is not None
                else None
            ),
            "observations": [
                {
                    "candidate": observation.candidate.to_dict(),
                    "classification": observation.classification,
                    "planned_action": observation.planned_action,
                    "collision": observation.collision,
                    "existing": (
                        observation.existing.to_dict()
                        if observation.existing is not None
                        else None
                    ),
                    "differing_fields": list(
                        observation.differing_fields
                    ),
                }
                for observation in observations
            ],
            "deletions": [
                {
                    "record": deletion.record.to_dict(),
                    "planned_action": deletion.planned_action,
                }
                for deletion in deletions
            ],
            "source_missing": [
                {
                    "Ticker": observation.ticker,
                    "Date": observation.date.isoformat(),
                    "planned_action": observation.planned_action,
                    "existing": (
                        observation.existing.to_dict()
                        if observation.existing is not None
                        else None
                    ),
                }
                for observation in source_missing
            ],
            "excluded_observations": [
                {
                    "candidate_index": observation.candidate_index,
                    "ticker": observation.ticker,
                    "date": observation.date,
                    "issues": [
                        {
                            "code": issue.code,
                            "message": issue.message,
                            "candidate_index": issue.candidate_index,
                            "ticker": issue.ticker,
                            "date": issue.date,
                        }
                        for issue in observation.issues
                    ],
                }
                for observation in excluded_observations
            ],
            "validation_issues": [
                {
                    "code": issue.code,
                    "message": issue.message,
                    "candidate_index": issue.candidate_index,
                    "ticker": issue.ticker,
                    "date": issue.date,
                }
                for issue in validation_issues
            ],
            "validation_warnings": [
                {
                    "code": warning.code,
                    "message": warning.message,
                    "candidate_index": warning.candidate_index,
                    "ticker": warning.ticker,
                    "date": warning.date,
                }
                for warning in validation_warnings
            ],
            "duplicate_keys": [
                [ticker, record_date.isoformat()]
                for ticker, record_date in duplicate_keys
            ],
            "source_missing_keys": [
                [ticker, record_date.isoformat()]
                for ticker, record_date in source_missing_keys
            ],
            "baseline_fingerprint": baseline_fingerprint,
            "latest_expected_stored_session": (
                latest_expected_stored_session.isoformat()
            ),
        }

        serialized = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        )

        return hashlib.sha256(
            serialized.encode("utf-8")
        ).hexdigest()

    def _assert_plan_integrity(
        self,
        plan: MutationPlan,
    ) -> None:
        """
        Reject a MutationPlan whose stored identity no longer matches its
        materialized contents.

        This protects both the public Commit boundary and the private executor
        from accidentally executing a modified/reconstructed Preview object.
        """
        expected_fingerprint = self._build_plan_fingerprint(
            operation=plan.operation,
            source=plan.source,
            requested_tickers=plan.requested_tickers,
            requested_start_date=plan.requested_start_date,
            requested_end_date=plan.requested_end_date,
            observations=plan.observations,
            deletions=plan.deletions,
            source_missing=plan.source_missing,
            excluded_observations=plan.excluded_observations,
            validation_issues=plan.validation_issues,
            validation_warnings=plan.validation_warnings,
            duplicate_keys=plan.duplicate_keys,
            source_missing_keys=plan.source_missing_keys,
            baseline_fingerprint=plan.baseline_fingerprint,
            latest_expected_stored_session=(
                plan.latest_expected_stored_session
            ),
        )

        if expected_fingerprint != plan.plan_fingerprint:
            raise RuntimeError(
                "MutationPlan integrity check failed. "
                "Build a fresh Preview before Commit."
            )

    @staticmethod
    def _find_changed_baseline_keys(
        expected_records: Mapping[
            Tuple[str, date],
            Optional[CanonicalOHLCVRecord],
        ],
        current_records: Mapping[
            Tuple[str, date],
            CanonicalOHLCVRecord,
        ],
    ) -> Tuple[Tuple[str, date], ...]:
        """
        Return logical keys whose authoritative DB state changed after Preview.

        A change includes:
        - previously absent key now exists
        - previously existing key is now absent
        - previously existing key has different persisted OHLCV values
        """
        changed_keys: List[Tuple[str, date]] = []

        for key in sorted(
            expected_records,
            key=lambda item: (item[0], item[1]),
        ):
            expected = expected_records[key]
            current = current_records.get(key)

            if expected is None and current is None:
                continue

            if expected is None or current is None:
                changed_keys.append(key)
                continue

            if expected.persisted_values() != current.persisted_values():
                changed_keys.append(key)

        return tuple(changed_keys)

    def _verify_deletion_plan_current_in_connection(
        self,
        connection: sqlite3.Connection,
        plan: MutationPlan,
    ) -> PlanFreshnessCheck:
        """
        Verify the complete authoritative scope of one deletion Preview.

        Deletion freshness is scope-based rather than limited to the logical
        keys that existed when Preview was built. This ensures that a new
        in-scope row appearing after Preview also invalidates the old plan.
        """
        if plan.operation not in DELETION_OPERATIONS:
            raise ValueError(
                "Deletion freshness verification requires a deletion plan."
            )

        if len(plan.requested_tickers) != 1:
            raise RuntimeError(
                "Deletion plan must contain exactly one requested ticker."
            )

        ticker = plan.requested_tickers[0]

        if plan.operation == "Delete Range":
            if (
                plan.requested_start_date is None
                or plan.requested_end_date is None
            ):
                raise RuntimeError(
                    "Delete Range plan is missing its approved date scope."
                )

            start_date = plan.requested_start_date
            end_date = plan.requested_end_date
        else:
            if (
                plan.requested_start_date is not None
                or plan.requested_end_date is not None
            ):
                raise RuntimeError(
                    "Delete Ticker plan must not contain a date scope."
                )

            start_date = None
            end_date = None

        current_scope = self._load_deletion_scope_from_connection(
            connection,
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
        )

        expected_records: Dict[
            Tuple[str, date],
            CanonicalOHLCVRecord,
        ] = {
            deletion.record.key: deletion.record
            for deletion in plan.deletions
        }

        current_records: Dict[
            Tuple[str, date],
            CanonicalOHLCVRecord,
        ] = {
            record.key: record
            for record in current_scope
        }

        scope_keys = (
            set(expected_records)
            | set(current_records)
        )

        expected_scope_records: Dict[
            Tuple[str, date],
            Optional[CanonicalOHLCVRecord],
        ] = {
            key: expected_records.get(key)
            for key in scope_keys
        }

        current_fingerprint = (
            self._build_baseline_fingerprint(
                scope_keys,
                current_records,
            )
        )

        changed_keys = self._find_changed_baseline_keys(
            expected_scope_records,
            current_records,
        )

        return PlanFreshnessCheck(
            is_current=(
                current_fingerprint
                == plan.baseline_fingerprint
                and not changed_keys
            ),
            expected_fingerprint=plan.baseline_fingerprint,
            current_fingerprint=current_fingerprint,
            changed_keys=changed_keys,
        )

    def _verify_plan_current_in_connection(
        self,
        connection: sqlite3.Connection,
        plan: MutationPlan,
    ) -> PlanFreshnessCheck:
        """
        Verify Preview freshness using an existing SQLite connection.

        The transaction executor uses this after BEGIN IMMEDIATE so no other
        writer can alter the relevant authoritative baseline between this
        verification and the approved mutation.
        """
        if plan.operation in DELETION_OPERATIONS:
            return self._verify_deletion_plan_current_in_connection(
                connection,
                plan,
            )

        baseline_keys = [
            observation.candidate.key
            for observation in plan.observations
        ] + [
            observation.key
            for observation in plan.source_missing
        ]

        expected_records: Dict[
            Tuple[str, date],
            Optional[CanonicalOHLCVRecord],
        ] = {
            observation.candidate.key: observation.existing
            for observation in plan.observations
        }

        expected_records.update(
            {
                observation.key: observation.existing
                for observation in plan.source_missing
            }
        )

        current_records = (
            self._load_existing_records_from_connection(
                connection,
                baseline_keys,
            )
        )

        current_fingerprint = (
            self._build_baseline_fingerprint(
                baseline_keys,
                current_records,
            )
        )

        changed_keys = self._find_changed_baseline_keys(
            expected_records,
            current_records,
        )

        return PlanFreshnessCheck(
            is_current=(
                current_fingerprint
                == plan.baseline_fingerprint
                and not changed_keys
            ),
            expected_fingerprint=plan.baseline_fingerprint,
            current_fingerprint=current_fingerprint,
            changed_keys=changed_keys,
        )

    def verify_plan_current(
        self,
        plan: MutationPlan,
    ) -> PlanFreshnessCheck:
        """
        Verify that authoritative DB state still matches a Preview plan.

        This public planning check is read-only.

        Final mutation execution performs the same check again inside its
        write transaction before changing any authoritative row.
        """
        if not isinstance(plan, MutationPlan):
            raise TypeError(
                "plan must be a MutationPlan produced by build_plan()."
            )

        connection = self._connect_read_only()

        try:
            return self._verify_plan_current_in_connection(
                connection,
                plan,
            )
        finally:
            connection.close()

    def _insert_canonical_record(
        self,
        connection: sqlite3.Connection,
        record: CanonicalOHLCVRecord,
    ) -> None:
        """Insert one record that Preview classified as New."""
        cursor = connection.execute(
            f"""
            INSERT INTO "{self.table_name}" (
                Ticker,
                Date,
                Open,
                High,
                Low,
                Close,
                "Adj Close",
                Volume
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.ticker,
                record.date.isoformat(),
                record.open,
                record.high,
                record.low,
                record.close,
                record.adj_close,
                record.volume,
            ),
        )

        if cursor.rowcount != 1:
            raise RuntimeError(
                "Expected exactly one daily_prices insert."
            )

    def _update_canonical_record(
        self,
        connection: sqlite3.Connection,
        record: CanonicalOHLCVRecord,
    ) -> None:
        """
        Update one exact existing record that Preview classified as an
        explicitly replacement-eligible Changed collision.
        """
        cursor = connection.execute(
            f"""
            UPDATE "{self.table_name}"
            SET
                Open = ?,
                High = ?,
                Low = ?,
                Close = ?,
                "Adj Close" = ?,
                Volume = ?
            WHERE Ticker = ?
              AND Date = ?
            """,
            (
                record.open,
                record.high,
                record.low,
                record.close,
                record.adj_close,
                record.volume,
                record.ticker,
                record.date.isoformat(),
            ),
        )

        if cursor.rowcount != 1:
            raise RuntimeError(
                "Expected exactly one daily_prices replacement update."
            )

    def _apply_planned_observations(
        self,
        connection: sqlite3.Connection,
        plan: MutationPlan,
    ) -> int:
        """
        Apply only already-materialized Preview actions.

        No classification or operation semantics are recalculated here.
        """
        rows_affected = 0

        for observation in plan.observations:
            if observation.planned_action == "insert":
                self._insert_canonical_record(
                    connection,
                    observation.candidate,
                )
                rows_affected += 1
                continue

            if observation.planned_action == "replacement_candidate":
                self._update_canonical_record(
                    connection,
                    observation.candidate,
                )
                rows_affected += 1
                continue

            if observation.planned_action in {
                "no_change",
                "preserve_existing",
            }:
                continue

            raise RuntimeError(
                "Unsupported planned mutation action: "
                f"{observation.planned_action!r}."
            )

        return rows_affected

    def _apply_planned_deletions(
        self,
        connection: sqlite3.Connection,
        plan: MutationPlan,
    ) -> int:
        """
        Apply one already-materialized explicit deletion scope.

        Freshness is verified by the transaction executor immediately before
        this method runs. The DELETE therefore executes only the exact scope
        represented by the approved plan.

        The affected-row count must equal the number of materialized deletion
        records or the transaction fails and rolls back.
        """
        if plan.operation not in DELETION_OPERATIONS:
            raise ValueError(
                "Deletion execution requires a deletion operation."
            )

        if len(plan.requested_tickers) != 1:
            raise RuntimeError(
                "Deletion plan must contain exactly one requested ticker."
            )

        if not plan.deletions:
            raise RuntimeError(
                "Deletion plan contains no materialized rows to delete."
            )

        if any(
            deletion.planned_action != "delete"
            for deletion in plan.deletions
        ):
            raise RuntimeError(
                "Deletion plan contains an unsupported planned action."
            )

        ticker = plan.requested_tickers[0]

        if any(
            deletion.record.ticker != ticker
            for deletion in plan.deletions
        ):
            raise RuntimeError(
                "Deletion plan contains a row outside its approved ticker."
            )

        if plan.operation == "Delete Range":
            if (
                plan.requested_start_date is None
                or plan.requested_end_date is None
            ):
                raise RuntimeError(
                    "Delete Range plan is missing its approved date scope."
                )

            if any(
                not (
                    plan.requested_start_date
                    <= deletion.record.date
                    <= plan.requested_end_date
                )
                for deletion in plan.deletions
            ):
                raise RuntimeError(
                    "Delete Range plan contains a row outside its approved "
                    "date scope."
                )

            cursor = connection.execute(
                f"""
                DELETE FROM "{self.table_name}"
                WHERE Ticker = ?
                  AND Date >= ?
                  AND Date <= ?
                """,
                (
                    ticker,
                    plan.requested_start_date.isoformat(),
                    plan.requested_end_date.isoformat(),
                ),
            )
        else:
            if (
                plan.requested_start_date is not None
                or plan.requested_end_date is not None
            ):
                raise RuntimeError(
                    "Delete Ticker plan must not contain a date scope."
                )

            cursor = connection.execute(
                f"""
                DELETE FROM "{self.table_name}"
                WHERE Ticker = ?
                """,
                (ticker,),
            )

        rows_affected = int(cursor.rowcount)

        if rows_affected != len(plan.deletions):
            raise RuntimeError(
                "Deletion affected an unexpected number of daily_prices "
                "rows. Expected "
                f"{len(plan.deletions)}, affected {rows_affected}."
            )

        return rows_affected

    @staticmethod
    def _build_audit_details(
        plan: MutationPlan,
    ) -> str:
        """Serialize the exact materialized Preview actions for audit."""
        details = {
            "requested_tickers": list(plan.requested_tickers),
            "baseline_fingerprint": plan.baseline_fingerprint,
            "summary": plan.summary(),
            "validation_warnings": [
                {
                    "code": warning.code,
                    "message": warning.message,
                    "candidate_index": warning.candidate_index,
                    "ticker": warning.ticker,
                    "date": warning.date,
                }
                for warning in plan.validation_warnings
            ],
            "excluded_observations": [
                {
                    "candidate_index": observation.candidate_index,
                    "ticker": observation.ticker,
                    "date": observation.date,
                    "issues": [
                        {
                            "code": issue.code,
                            "message": issue.message,
                            "candidate_index": issue.candidate_index,
                            "ticker": issue.ticker,
                            "date": issue.date,
                        }
                        for issue in observation.issues
                    ],
                }
                for observation in plan.excluded_observations
            ],
            "mutations": [
                {
                    "Ticker": observation.candidate.ticker,
                    "Date": observation.candidate.date.isoformat(),
                    "classification": observation.classification,
                    "planned_action": observation.planned_action,
                    "differing_fields": list(
                        observation.differing_fields
                    ),
                }
                for observation in plan.observations
                if observation.planned_action
                in {
                    "insert",
                    "replacement_candidate",
                }
            ],
            "source_missing": [
                {
                    "Ticker": observation.ticker,
                    "Date": observation.date.isoformat(),
                    "planned_action": observation.planned_action,
                }
                for observation in plan.source_missing
            ],
            "deletion": (
                {
                    "planned_action": "delete",
                    "materialized_rows": len(plan.deletions),
                    "first_affected_date": min(
                        deletion.record.date
                        for deletion in plan.deletions
                    ).isoformat(),
                    "last_affected_date": max(
                        deletion.record.date
                        for deletion in plan.deletions
                    ).isoformat(),
                }
                if plan.deletions
                else None
            ),
        }

        return json.dumps(
            details,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        )

    def _insert_audit_event(
        self,
        connection: sqlite3.Connection,
        plan: MutationPlan,
        rows_affected: int,
    ) -> int:
        """
        Insert the one audit event belonging to this MutationPlan transaction.

        The caller owns commit/rollback.
        """
        audit_ticker = (
            plan.requested_tickers[0]
            if len(plan.requested_tickers) == 1
            else None
        )

        timestamp = (
            datetime.now()
            .astimezone()
            .isoformat(timespec="seconds")
        )

        cursor = connection.execute(
            f"""
            INSERT INTO "{self.audit_table_name}" (
                timestamp,
                action,
                ticker,
                start_date,
                end_date,
                source,
                rows_affected,
                plan_fingerprint,
                details
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                timestamp,
                plan.operation,
                audit_ticker,
                (
                    plan.requested_start_date.isoformat()
                    if plan.requested_start_date is not None
                    else None
                ),
                (
                    plan.requested_end_date.isoformat()
                    if plan.requested_end_date is not None
                    else None
                ),
                plan.source,
                rows_affected,
                plan.plan_fingerprint,
                self._build_audit_details(plan),
            ),
        )

        audit_id = cursor.lastrowid

        if audit_id is None:
            raise RuntimeError(
                "Audit event insert did not return an audit id."
            )

        return int(audit_id)

    def _execute_plan_transaction(
        self,
        plan: MutationPlan,
    ) -> MutationTransactionResult:
        """
        Execute one already-materialized MutationPlan atomically.

        PRIVATE TRANSACTION PRIMITIVE.

        Public callers must use commit_plan(), which enforces exact Preview
        confirmation before delegating to this executor.

        Transaction:
            BEGIN IMMEDIATE
            verify audit schema
            verify Preview baseline
            apply exact planned mutations
            insert audit event
            COMMIT

        Any failure rolls back both data and audit changes.
        """
        if not isinstance(plan, MutationPlan):
            raise TypeError(
                "plan must be a MutationPlan produced by build_plan()."
            )

        self._assert_plan_integrity(plan)

        if not plan.can_commit:
            raise ValueError(
                "MutationPlan contains hard validation failures and "
                "cannot be executed."
            )

        connection = self._connect_write()

        try:
            connection.execute("BEGIN IMMEDIATE")

            audit_status = (
                self._get_audit_schema_status_from_connection(
                    connection
                )
            )

            if not audit_status.exists:
                raise RuntimeError(
                    "Data Management audit table is not initialized."
                )

            if not audit_status.compatible:
                raise RuntimeError(
                    "Data Management audit table is incompatible. "
                    "Missing required column(s): "
                    + ", ".join(
                        audit_status.missing_columns
                    )
                )

            freshness = (
                self._verify_plan_current_in_connection(
                    connection,
                    plan,
                )
            )

            if not freshness.is_current:
                changed_text = ", ".join(
                    f"{ticker}/{record_date.isoformat()}"
                    for ticker, record_date
                    in freshness.changed_keys
                )

                raise RuntimeError(
                    "MutationPlan is stale and must be Previewed again."
                    + (
                        f" Changed key(s): {changed_text}."
                        if changed_text
                        else ""
                    )
                )

            if plan.operation in DELETION_OPERATIONS:
                rows_affected = self._apply_planned_deletions(
                    connection,
                    plan,
                )
            else:
                rows_affected = self._apply_planned_observations(
                    connection,
                    plan,
                )

            audit_id = self._insert_audit_event(
                connection,
                plan,
                rows_affected,
            )

            connection.commit()

            return MutationTransactionResult(
                rows_affected=rows_affected,
                audit_id=audit_id,
            )

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    def commit_plan(
        self,
        plan: MutationPlan,
        *,
        confirmed_plan_fingerprint: str,
    ) -> MutationTransactionResult:
        """
        Commit one explicitly confirmed, exact Preview plan.

        The caller must supply the fingerprint of the Preview the user
        confirmed. Commit never refetches source data, rebuilds classification,
        or reinterprets operation semantics.

        The private transaction executor independently verifies:
        - plan integrity
        - hard-validation eligibility
        - audit-schema readiness
        - current authoritative DB baseline

        before applying the exact materialized mutations atomically.
        """
        if not isinstance(plan, MutationPlan):
            raise TypeError(
                "plan must be a MutationPlan produced by build_plan()."
            )

        self._assert_plan_integrity(plan)

        normalized_confirmation = str(
            confirmed_plan_fingerprint or ""
        ).strip()

        if not normalized_confirmation:
            raise ValueError(
                "Explicit Preview confirmation is required."
            )

        if normalized_confirmation != plan.plan_fingerprint:
            raise ValueError(
                "Confirmed Preview does not match this MutationPlan. "
                "Build and confirm the current Preview before Commit."
            )

        if not plan.can_commit:
            raise ValueError(
                "MutationPlan contains hard validation failures and "
                "cannot be committed."
            )

        return self._execute_plan_transaction(plan)

    def build_plan(
        self,
        *,
        operation: str,
        source: str,
        candidates: Iterable[Mapping[str, Any]],
        requested_tickers: Optional[Iterable[Any]] = None,
        requested_start_date: Any = None,
        requested_end_date: Any = None,
    ) -> MutationPlan:
        """
        Build a read-only Preview plan from candidate OHLCV observations.

        No persistent state is changed.

        Source Missing is identified only when the caller supplies a complete
        requested ticker/date scope. Expected observations are based on NYSE
        sessions capped at the Latest Expected Stored Session.

        When requested_tickers is omitted, Source Missing inference remains
        disabled. This preserves manual/planning callers that do not represent
        a complete acquisition request.
        """
        normalized_operation = str(operation or "").strip()

        if normalized_operation not in CANDIDATE_RECORD_OPERATIONS:
            raise ValueError(
                "Unsupported candidate-record operation: "
                f"{normalized_operation!r}."
            )

        normalized_source = str(source or "").strip()

        if not normalized_source:
            raise ValueError("Source is required.")

        normalized_requested_tickers = (
            self._normalize_requested_tickers(
                requested_tickers
            )
        )

        normalized_start_date = (
            self._normalize_date_value(requested_start_date)
            if requested_start_date is not None
            else None
        )
        normalized_end_date = (
            self._normalize_date_value(requested_end_date)
            if requested_end_date is not None
            else None
        )

        if (
            normalized_start_date is not None
            and normalized_end_date is not None
            and normalized_start_date > normalized_end_date
        ):
            raise ValueError(
                "Requested Start Date cannot be later than End Date."
            )

        if normalized_requested_tickers and (
            normalized_start_date is None
            or normalized_end_date is None
        ):
            raise ValueError(
                "Requested Start Date and End Date are required when "
                "requested_tickers is supplied for Source Missing detection."
            )

        latest_expected_stored_session = (
            get_latest_expected_stored_session()
        )

        candidate_list = list(candidates)
        indexed_records: List[
            Tuple[int, CanonicalOHLCVRecord]
        ] = []
        indexed_identities: List[
            Tuple[int, Tuple[str, date]]
        ] = []
        supplied_candidate_keys: set[Tuple[str, date]] = set()
        excluded_observations: List[ExcludedObservation] = []
        validation_issues: List[ValidationIssue] = []
        validation_warnings: List[ValidationWarning] = []

        for candidate_index, candidate in enumerate(candidate_list):
            candidate_identity = self._extract_candidate_identity(
                candidate
            )

            if candidate_identity is not None:
                supplied_candidate_keys.add(
                    candidate_identity
                )
                indexed_identities.append(
                    (candidate_index, candidate_identity)
                )

            record, issues, warnings = self._normalize_candidate(
                candidate,
                candidate_index,
                latest_expected_stored_session,
            )

            validation_warnings.extend(warnings)

            if issues:
                excluded_observations.append(
                    ExcludedObservation(
                        candidate_index=candidate_index,
                        ticker=(
                            candidate_identity[0]
                            if candidate_identity is not None
                            else (
                                issues[0].ticker
                                if issues
                                else None
                            )
                        ),
                        date=(
                            candidate_identity[1].isoformat()
                            if candidate_identity is not None
                            else (
                                issues[0].date
                                if issues
                                else None
                            )
                        ),
                        issues=tuple(issues),
                    )
                )

            if record is not None:
                indexed_records.append(
                    (candidate_index, record)
                )

        duplicate_map = self._find_duplicate_keys(
            indexed_identities
        )

        for duplicate_key, candidate_indexes in sorted(
            duplicate_map.items(),
            key=lambda item: (item[0][0], item[0][1]),
        ):
            ticker, record_date = duplicate_key

            validation_issues.append(
                ValidationIssue(
                    code="duplicate_incoming_key",
                    message=(
                        "Duplicate incoming (Ticker, Date) key "
                        f"{ticker} / {record_date.isoformat()} "
                        "appears at candidate indexes "
                        + ", ".join(
                            str(index)
                            for index in candidate_indexes
                        )
                        + "."
                    ),
                    ticker=ticker,
                    date=record_date.isoformat(),
                )
            )

        duplicate_keys = set(duplicate_map)

        expected_source_keys: set[Tuple[str, date]] = set()

        if normalized_requested_tickers:
            assert normalized_start_date is not None
            assert normalized_end_date is not None

            effective_expected_end = min(
                normalized_end_date,
                latest_expected_stored_session,
            )

            if normalized_start_date <= effective_expected_end:
                expected_sessions = get_expected_sessions(
                    normalized_start_date,
                    effective_expected_end,
                )

                expected_source_keys = {
                    (ticker, session_date)
                    for ticker in normalized_requested_tickers
                    for session_date in expected_sessions
                }

        source_missing_keys = (
            expected_source_keys
            - supplied_candidate_keys
        )

        unambiguous_records = [
            record
            for _, record in indexed_records
            if record.key not in duplicate_keys
        ]

        comparison_keys = {
            record.key
            for record in unambiguous_records
        } | source_missing_keys

        existing_records = self._load_existing_records(
            comparison_keys
        )

        planned_observations: List[PlannedObservation] = []

        for candidate in sorted(
            unambiguous_records,
            key=lambda record: (
                record.ticker,
                record.date,
            ),
        ):
            existing = existing_records.get(candidate.key)

            if existing is None:
                classification = "New"
                differing_fields: Tuple[str, ...] = ()
                collision = False
            else:
                differing_fields = self._differing_fields(
                    candidate,
                    existing,
                )
                collision = True
                classification = (
                    "Changed"
                    if differing_fields
                    else "Unchanged"
                )

            planned_observations.append(
                PlannedObservation(
                    candidate=candidate,
                    classification=classification,
                    planned_action=self._planned_action(
                        normalized_operation,
                        classification,
                    ),
                    collision=collision,
                    existing=existing,
                    differing_fields=differing_fields,
                )
            )

        source_missing_observations: List[
            SourceMissingObservation
        ] = []

        for ticker, record_date in sorted(
            source_missing_keys,
            key=lambda item: (item[0], item[1]),
        ):
            key = (ticker, record_date)
            existing = existing_records.get(key)

            source_missing_observations.append(
                SourceMissingObservation(
                    ticker=ticker,
                    date=record_date,
                    planned_action=(
                        "preserve_existing"
                        if existing is not None
                        else "unresolved"
                    ),
                    existing=existing,
                )
            )

        baseline_keys = {
            record.key
            for record in unambiguous_records
        } | source_missing_keys

        baseline_fingerprint = (
            self._build_baseline_fingerprint(
                baseline_keys,
                existing_records,
            )
        )

        materialized_observations = tuple(
            planned_observations
        )

        materialized_source_missing = tuple(
            source_missing_observations
        )

        materialized_excluded_observations = tuple(
            excluded_observations
        )

        materialized_validation_issues = tuple(
            validation_issues
        )

        materialized_validation_warnings = tuple(
            validation_warnings
        )

        materialized_duplicate_keys = tuple(
            sorted(
                duplicate_keys,
                key=lambda item: (item[0], item[1]),
            )
        )

        materialized_source_missing_keys = tuple(
            sorted(
                source_missing_keys,
                key=lambda item: (item[0], item[1]),
            )
        )

        plan_fingerprint = self._build_plan_fingerprint(
            operation=normalized_operation,
            source=normalized_source,
            requested_tickers=normalized_requested_tickers,
            requested_start_date=normalized_start_date,
            requested_end_date=normalized_end_date,
            observations=materialized_observations,
            deletions=(),
            source_missing=materialized_source_missing,
            excluded_observations=(
                materialized_excluded_observations
            ),
            validation_issues=materialized_validation_issues,
            validation_warnings=materialized_validation_warnings,
            duplicate_keys=materialized_duplicate_keys,
            source_missing_keys=(
                materialized_source_missing_keys
            ),
            baseline_fingerprint=baseline_fingerprint,
            latest_expected_stored_session=(
                latest_expected_stored_session
            ),
        )

        return MutationPlan(
            operation=normalized_operation,
            source=normalized_source,
            requested_tickers=normalized_requested_tickers,
            requested_start_date=normalized_start_date,
            requested_end_date=normalized_end_date,
            observations=materialized_observations,
            deletions=(),
            source_missing=materialized_source_missing,
            excluded_observations=(
                materialized_excluded_observations
            ),
            validation_issues=materialized_validation_issues,
            validation_warnings=materialized_validation_warnings,
            duplicate_keys=materialized_duplicate_keys,
            source_missing_keys=(
                materialized_source_missing_keys
            ),
            baseline_fingerprint=baseline_fingerprint,
            plan_fingerprint=plan_fingerprint,
            latest_expected_stored_session=(
                latest_expected_stored_session
            ),
            created_at=datetime.now(),
        )

    def build_deletion_plan(
        self,
        *,
        operation: str,
        source: str,
        ticker: Any,
        requested_start_date: Any = None,
        requested_end_date: Any = None,
    ) -> MutationPlan:
        """
        Build one read-only explicit deletion Preview.

        Delete Range materializes every stored record for one ticker inside
        the inclusive requested date interval.

        Delete Ticker materializes every stored record for one ticker.

        This method does not modify persistent state.
        """
        normalized_operation = str(operation or "").strip()

        if normalized_operation not in DELETION_OPERATIONS:
            raise ValueError(
                "Unsupported deletion operation: "
                f"{normalized_operation!r}."
            )

        normalized_source = str(source or "").strip()

        if not normalized_source:
            raise ValueError("Source is required.")

        normalized_tickers = self._normalize_requested_tickers(
            [ticker]
        )

        if len(normalized_tickers) != 1:
            raise ValueError(
                "Exactly one ticker is required for deletion."
            )

        normalized_ticker = normalized_tickers[0]

        if normalized_operation == "Delete Range":
            if (
                requested_start_date is None
                or requested_end_date is None
            ):
                raise ValueError(
                    "Delete Range requires Start Date and End Date."
                )

            normalized_start_date = self._normalize_date_value(
                requested_start_date
            )
            normalized_end_date = self._normalize_date_value(
                requested_end_date
            )

            if normalized_start_date > normalized_end_date:
                raise ValueError(
                    "Requested Start Date cannot be later than End Date."
                )
        else:
            if (
                requested_start_date is not None
                or requested_end_date is not None
            ):
                raise ValueError(
                    "Delete Ticker does not accept Start Date or End Date."
                )

            normalized_start_date = None
            normalized_end_date = None

        stored_records = self._load_deletion_scope(
            ticker=normalized_ticker,
            start_date=normalized_start_date,
            end_date=normalized_end_date,
        )

        materialized_deletions = tuple(
            PlannedDeletion(
                record=record,
            )
            for record in stored_records
        )

        existing_records = {
            deletion.record.key: deletion.record
            for deletion in materialized_deletions
        }

        baseline_keys = tuple(existing_records)

        baseline_fingerprint = (
            self._build_baseline_fingerprint(
                baseline_keys,
                existing_records,
            )
        )

        latest_expected_stored_session = (
            get_latest_expected_stored_session()
        )

        plan_fingerprint = self._build_plan_fingerprint(
            operation=normalized_operation,
            source=normalized_source,
            requested_tickers=(normalized_ticker,),
            requested_start_date=normalized_start_date,
            requested_end_date=normalized_end_date,
            observations=(),
            deletions=materialized_deletions,
            source_missing=(),
            excluded_observations=(),
            validation_issues=(),
            validation_warnings=(),
            duplicate_keys=(),
            source_missing_keys=(),
            baseline_fingerprint=baseline_fingerprint,
            latest_expected_stored_session=(
                latest_expected_stored_session
            ),
        )

        return MutationPlan(
            operation=normalized_operation,
            source=normalized_source,
            requested_tickers=(normalized_ticker,),
            requested_start_date=normalized_start_date,
            requested_end_date=normalized_end_date,
            observations=(),
            deletions=materialized_deletions,
            source_missing=(),
            excluded_observations=(),
            validation_issues=(),
            validation_warnings=(),
            duplicate_keys=(),
            source_missing_keys=(),
            baseline_fingerprint=baseline_fingerprint,
            plan_fingerprint=plan_fingerprint,
            latest_expected_stored_session=(
                latest_expected_stored_session
            ),
            created_at=datetime.now(),
        )

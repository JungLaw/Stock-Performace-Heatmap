"""
Persistent ticker-universe storage services.

Phase 2 keeps universe membership independent from authoritative OHLCV storage:

    universe membership != daily_prices membership

This module owns only persistent ticker metadata and universe membership.
It does not acquire market data, mutate daily_prices, or manage dashboard
session selections.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sqlite3
from typing import Dict, Mapping, Tuple

from src.config.assets import (
    COUNTRY_ETFS,
    CUSTOM_DEFAULT,
    SECTOR_ETFS,
)
from src.config.settings import DATABASE_FILE


TICKER_METADATA_TABLE = "ticker_metadata"
TICKER_UNIVERSE_MEMBERSHIP_TABLE = "ticker_universe_membership"

SUPPORTED_UNIVERSE_BUCKETS: Tuple[str, ...] = (
    "Custom",
    "Sector",
    "Country",
)

TICKER_METADATA_REQUIRED_COLUMNS: Tuple[str, ...] = (
    "ticker",
    "display_name",
)

TICKER_UNIVERSE_MEMBERSHIP_REQUIRED_COLUMNS: Tuple[str, ...] = (
    "ticker",
    "bucket",
    "sort_order",
)


@dataclass(frozen=True)
class UniverseSchemaStatus:
    """
    Read-only readiness status for the persistent ticker-universe schema.

    compatible=True means both required tables exist and expose the columns
    required by the current Phase-2 storage contract.
    """

    metadata_exists: bool
    membership_exists: bool
    compatible: bool
    metadata_columns: Tuple[str, ...]
    membership_columns: Tuple[str, ...]
    metadata_missing_columns: Tuple[str, ...]
    membership_missing_columns: Tuple[str, ...]


@dataclass(frozen=True)
class UniverseTickerRecord:
    """
    One canonical ticker-metadata row proposed by bootstrap preview.
    """

    ticker: str
    display_name: str


@dataclass(frozen=True)
class UniverseMembershipRecord:
    """
    One ordered ticker-to-bucket membership proposed by bootstrap preview.
    """

    ticker: str
    bucket: str
    sort_order: int


@dataclass(frozen=True)
class UniverseDisplayNameConflict:
    """
    One source ticker carrying multiple display names across source buckets.
    """

    ticker: str
    source_names: Tuple[str, ...]
    resolved_display_name: str


@dataclass(frozen=True)
class UniverseBootstrapPreview:
    """
    Read-only proposed bootstrap payload derived from current assets.py truth.

    Building this preview performs no database reads or writes.
    """

    ticker_records: Tuple[UniverseTickerRecord, ...]
    membership_records: Tuple[UniverseMembershipRecord, ...]
    display_name_conflicts: Tuple[UniverseDisplayNameConflict, ...]

    @property
    def ticker_count(self) -> int:
        return len(self.ticker_records)

    @property
    def membership_count(self) -> int:
        return len(self.membership_records)

    @property
    def conflict_count(self) -> int:
        return len(self.display_name_conflicts)

    @property
    def multi_bucket_tickers(self) -> Tuple[str, ...]:
        bucket_counts: Dict[str, int] = {}

        for record in self.membership_records:
            bucket_counts[record.ticker] = (
                bucket_counts.get(record.ticker, 0) + 1
            )

        return tuple(
            sorted(
                ticker
                for ticker, count in bucket_counts.items()
                if count > 1
            )
        )


@dataclass(frozen=True)
class UniverseBootstrapCommitResult:
    """
    Result of one successfully committed assets.py universe bootstrap.
    """

    metadata_rows_inserted: int
    membership_rows_inserted: int


@dataclass(frozen=True)
class UniverseBucketRecord:
    """
    One persistent bucket row joined with canonical ticker metadata.
    """

    ticker: str
    display_name: str
    bucket: str
    sort_order: int


@dataclass(frozen=True)
class UniverseMembershipMutationResult:
    """
    Result of one committed Add-to-Bucket or Remove-from-Bucket mutation.
    """

    action: str
    ticker: str
    bucket: str
    metadata_created: bool
    sort_order: int | None


@dataclass(frozen=True)
class UniverseDisplayNameMutationResult:
    """
    Result of one committed canonical ticker display-name update.
    """

    ticker: str
    previous_display_name: str
    display_name: str


@dataclass(frozen=True)
class UniverseReorderMutationResult:
    """
    Result of one committed bucket-local reorder.
    """

    bucket: str
    ordered_tickers: Tuple[str, ...]


class UniverseManager:
    """
    Persistent ticker-universe owner.

    Responsibilities introduced in Phase 2:
    - inspect persistent universe-schema readiness;
    - explicitly initialize persistent universe tables.

    Later Phase-2 updates may add:
    - one-time assets.py bootstrap;
    - read services;
    - controlled membership and metadata mutations.

    This class does not own daily_prices mutation.
    """

    def __init__(
        self,
        database_file: str = DATABASE_FILE,
        metadata_table_name: str = TICKER_METADATA_TABLE,
        membership_table_name: str = TICKER_UNIVERSE_MEMBERSHIP_TABLE,
    ) -> None:
        self.database_path = Path(database_file)
        self.metadata_table_name = str(metadata_table_name)
        self.membership_table_name = str(membership_table_name)

    @staticmethod
    def build_assets_bootstrap_preview(
        display_name_overrides: Mapping[str, str] | None = None,
    ) -> UniverseBootstrapPreview:
        """
        Build the proposed persistent-universe bootstrap payload from assets.py.

        This method is intentionally non-destructive:
        - no database connection is opened;
        - no schema is initialized;
        - no persistent rows are written;
        - assets.py is not modified.

        Current approved migration policy:
        - preserve source bucket membership exactly;
        - preserve source list order as bucket-local sort_order;
        - normalize ticker identity to uppercase;
        - collapse display names to one canonical ticker-level value;
        - surface every source display-name conflict;
        - apply an explicit approved override when one is supplied.

        The currently approved migration resolves:
            IWM -> Russell 2000
        """
        approved_overrides: Dict[str, str] = {
            "IWM": "Russell 2000",
        }

        if display_name_overrides:
            for ticker, display_name in display_name_overrides.items():
                normalized_ticker = str(ticker).strip().upper()
                normalized_name = str(display_name).strip()

                if not normalized_ticker:
                    raise ValueError(
                        "Display-name override ticker cannot be empty."
                    )

                if not normalized_name:
                    raise ValueError(
                        f"Display-name override for {normalized_ticker} "
                        "cannot be empty."
                    )

                approved_overrides[normalized_ticker] = normalized_name

        source_groups = (
            ("Country", COUNTRY_ETFS),
            ("Sector", SECTOR_ETFS),
            ("Custom", CUSTOM_DEFAULT),
        )

        memberships = []
        names_by_ticker: Dict[str, list[str]] = {}
        first_seen_tickers = []

        for bucket, source_rows in source_groups:
            for sort_order, source_row in enumerate(
                source_rows,
                start=1,
            ):
                if (
                    not isinstance(source_row, tuple)
                    or len(source_row) != 2
                ):
                    raise ValueError(
                        f"Malformed {bucket} assets.py row: "
                        f"{source_row!r}"
                    )

                raw_ticker, raw_display_name = source_row

                ticker = str(raw_ticker).strip().upper()
                display_name = str(raw_display_name).strip()

                if not ticker:
                    raise ValueError(
                        f"Empty ticker found in {bucket} source."
                    )

                if not display_name:
                    raise ValueError(
                        f"Empty display name found for {ticker} "
                        f"in {bucket} source."
                    )

                if bucket not in SUPPORTED_UNIVERSE_BUCKETS:
                    raise ValueError(
                        f"Unsupported bootstrap bucket: {bucket!r}"
                    )

                if ticker not in names_by_ticker:
                    names_by_ticker[ticker] = []
                    first_seen_tickers.append(ticker)

                if display_name not in names_by_ticker[ticker]:
                    names_by_ticker[ticker].append(display_name)

                memberships.append(
                    UniverseMembershipRecord(
                        ticker=ticker,
                        bucket=bucket,
                        sort_order=sort_order,
                    )
                )

        ticker_records = []
        conflicts = []

        for ticker in first_seen_tickers:
            source_names = tuple(
                names_by_ticker[ticker]
            )

            if ticker in approved_overrides:
                resolved_display_name = (
                    approved_overrides[ticker]
                )
            else:
                resolved_display_name = source_names[0]

            if len(source_names) > 1:
                conflicts.append(
                    UniverseDisplayNameConflict(
                        ticker=ticker,
                        source_names=source_names,
                        resolved_display_name=(
                            resolved_display_name
                        ),
                    )
                )

            ticker_records.append(
                UniverseTickerRecord(
                    ticker=ticker,
                    display_name=resolved_display_name,
                )
            )

        membership_identity = [
            (record.ticker, record.bucket)
            for record in memberships
        ]

        if len(membership_identity) != len(
            set(membership_identity)
        ):
            raise ValueError(
                "Duplicate (ticker, bucket) membership detected "
                "in assets.py bootstrap source."
            )

        bucket_order_identity = [
            (record.bucket, record.sort_order)
            for record in memberships
        ]

        if len(bucket_order_identity) != len(
            set(bucket_order_identity)
        ):
            raise ValueError(
                "Duplicate bucket sort_order detected in "
                "assets.py bootstrap source."
            )

        return UniverseBootstrapPreview(
            ticker_records=tuple(ticker_records),
            membership_records=tuple(memberships),
            display_name_conflicts=tuple(conflicts),
        )

    def _connect_read_only(self) -> sqlite3.Connection:
        """
        Open the configured SQLite database in explicit read-only mode.
        """
        database_uri = self.database_path.resolve().as_uri() + "?mode=ro"

        connection = sqlite3.connect(
            database_uri,
            uri=True,
        )
        connection.row_factory = sqlite3.Row
        return connection

    def _connect_write(self) -> sqlite3.Connection:
        """
        Open a writable SQLite connection.

        Merely opening this connection does not mutate persistent state.
        Schema and mutation methods must own transaction boundaries explicitly.
        """
        connection = sqlite3.connect(
            self.database_path
        )
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    @staticmethod
    def _get_table_columns(
        connection: sqlite3.Connection,
        table_name: str,
    ) -> Tuple[str, ...]:
        """
        Return the stored column names for one SQLite table.

        An empty tuple means the table does not exist.
        """
        table_row = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name = ?
            """,
            (table_name,),
        ).fetchone()

        if table_row is None:
            return ()

        pragma_rows = connection.execute(
            f'PRAGMA table_info("{table_name}")'
        ).fetchall()

        return tuple(
            str(row["name"])
            for row in pragma_rows
        )

    def _get_schema_status_from_connection(
        self,
        connection: sqlite3.Connection,
    ) -> UniverseSchemaStatus:
        """
        Inspect persistent universe-schema readiness using one connection.
        """
        metadata_columns = self._get_table_columns(
            connection,
            self.metadata_table_name,
        )
        membership_columns = self._get_table_columns(
            connection,
            self.membership_table_name,
        )

        metadata_exists = bool(metadata_columns)
        membership_exists = bool(membership_columns)

        metadata_column_set = set(metadata_columns)
        membership_column_set = set(membership_columns)

        metadata_missing_columns = tuple(
            column_name
            for column_name in TICKER_METADATA_REQUIRED_COLUMNS
            if column_name not in metadata_column_set
        )

        membership_missing_columns = tuple(
            column_name
            for column_name in TICKER_UNIVERSE_MEMBERSHIP_REQUIRED_COLUMNS
            if column_name not in membership_column_set
        )

        compatible = (
            metadata_exists
            and membership_exists
            and not metadata_missing_columns
            and not membership_missing_columns
        )

        return UniverseSchemaStatus(
            metadata_exists=metadata_exists,
            membership_exists=membership_exists,
            compatible=compatible,
            metadata_columns=metadata_columns,
            membership_columns=membership_columns,
            metadata_missing_columns=metadata_missing_columns,
            membership_missing_columns=membership_missing_columns,
        )

    @staticmethod
    def _normalize_bucket_name(
        bucket: str,
    ) -> str:
        """
        Normalize and validate one supported universe bucket name.

        Callers may use either canonical title case or lowercase dashboard-style
        names such as "country", "sector", and "custom".
        """
        normalized_bucket = str(
            bucket or ""
        ).strip().title()

        if normalized_bucket not in SUPPORTED_UNIVERSE_BUCKETS:
            raise ValueError(
                "Unsupported universe bucket. Expected one of: "
                + ", ".join(
                    SUPPORTED_UNIVERSE_BUCKETS
                )
                + "."
            )

        return normalized_bucket

    @staticmethod
    def _normalize_ticker(
        ticker: str,
    ) -> str:
        """
        Normalize one canonical ticker identity for persistent universe use.
        """
        normalized_ticker = str(
            ticker or ""
        ).strip().upper()

        if not normalized_ticker:
            raise ValueError(
                "Ticker cannot be empty."
            )

        return normalized_ticker

    @staticmethod
    def _normalize_display_name(
        display_name: str,
    ) -> str:
        """
        Normalize and validate one canonical ticker display name.
        """
        normalized_display_name = str(
            display_name or ""
        ).strip()

        if not normalized_display_name:
            raise ValueError(
                "Display name cannot be empty."
            )

        return normalized_display_name

    def _require_compatible_schema_from_connection(
        self,
        connection: sqlite3.Connection,
    ) -> None:
        """
        Require the persistent universe schema before serving read results.
        """
        schema_status = self._get_schema_status_from_connection(
            connection
        )

        if not schema_status.compatible:
            raise RuntimeError(
                "Persistent universe schema is not initialized and "
                "compatible."
            )

    def _renumber_bucket_from_connection(
        self,
        connection: sqlite3.Connection,
        bucket: str,
    ) -> Tuple[str, ...]:
        """
        Rewrite one bucket to contiguous sort_order values beginning at 1.

        The caller owns the surrounding transaction.
        """
        normalized_bucket = self._normalize_bucket_name(
            bucket
        )

        rows = connection.execute(
            f"""
            SELECT ticker
            FROM "{self.membership_table_name}"
            WHERE bucket = ?
            ORDER BY
                sort_order ASC,
                ticker ASC
            """,
            (normalized_bucket,),
        ).fetchall()

        ordered_tickers = tuple(
            str(
                row["ticker"]
            )
            for row in rows
        )

        if not ordered_tickers:
            return ()

        max_sort_order = int(
            connection.execute(
                f"""
                SELECT COALESCE(
                    MAX(sort_order),
                    0
                )
                FROM "{self.membership_table_name}"
                WHERE bucket = ?
                """,
                (normalized_bucket,),
            ).fetchone()[0]
        )

        temporary_offset = (
            max_sort_order
            + len(ordered_tickers)
            + 1
        )

        connection.execute(
            f"""
            UPDATE "{self.membership_table_name}"
            SET sort_order = sort_order + ?
            WHERE bucket = ?
            """,
            (
                temporary_offset,
                normalized_bucket,
            ),
        )

        for sort_order, ticker in enumerate(
            ordered_tickers,
            start=1,
        ):
            connection.execute(
                f"""
                UPDATE "{self.membership_table_name}"
                SET sort_order = ?
                WHERE ticker = ?
                  AND bucket = ?
                """,
                (
                    sort_order,
                    ticker,
                    normalized_bucket,
                ),
            )

        return ordered_tickers

    def get_bucket_records(
        self,
        bucket: str,
    ) -> Tuple[UniverseBucketRecord, ...]:
        """
        Return one persistent bucket in canonical bucket-local order.

        Each record includes the canonical ticker-level display name.
        """
        normalized_bucket = self._normalize_bucket_name(
            bucket
        )

        connection = self._connect_read_only()

        try:
            self._require_compatible_schema_from_connection(
                connection
            )

            rows = connection.execute(
                f"""
                SELECT
                    membership.ticker AS ticker,
                    metadata.display_name AS display_name,
                    membership.bucket AS bucket,
                    membership.sort_order AS sort_order
                FROM "{self.membership_table_name}" AS membership
                INNER JOIN "{self.metadata_table_name}" AS metadata
                    ON metadata.ticker = membership.ticker
                WHERE membership.bucket = ?
                ORDER BY
                    membership.sort_order ASC,
                    membership.ticker ASC
                """,
                (normalized_bucket,),
            ).fetchall()

            return tuple(
                UniverseBucketRecord(
                    ticker=str(
                        row["ticker"]
                    ),
                    display_name=(
                        str(
                            row["display_name"]
                        )
                        if row["display_name"] is not None
                        else str(
                            row["ticker"]
                        )
                    ),
                    bucket=str(
                        row["bucket"]
                    ),
                    sort_order=int(
                        row["sort_order"]
                    ),
                )
                for row in rows
            )
        finally:
            connection.close()

    def get_bucket_tickers(
        self,
        bucket: str,
    ) -> Tuple[str, ...]:
        """
        Return ticker symbols for one bucket in persistent bucket order.
        """
        return tuple(
            record.ticker
            for record in self.get_bucket_records(
                bucket
            )
        )

    def get_bucket_memberships(
        self,
        ticker: str,
    ) -> Tuple[UniverseMembershipRecord, ...]:
        """
        Return all persistent bucket memberships for one ticker.

        A ticker may legitimately belong to multiple buckets.
        """
        normalized_ticker = str(
            ticker or ""
        ).strip().upper()

        if not normalized_ticker:
            raise ValueError(
                "Ticker cannot be empty."
            )

        connection = self._connect_read_only()

        try:
            self._require_compatible_schema_from_connection(
                connection
            )

            rows = connection.execute(
                f"""
                SELECT
                    ticker,
                    bucket,
                    sort_order
                FROM "{self.membership_table_name}"
                WHERE ticker = ?
                ORDER BY
                    CASE bucket
                        WHEN 'Custom' THEN 1
                        WHEN 'Sector' THEN 2
                        WHEN 'Country' THEN 3
                        ELSE 4
                    END,
                    sort_order ASC
                """,
                (normalized_ticker,),
            ).fetchall()

            return tuple(
                UniverseMembershipRecord(
                    ticker=str(
                        row["ticker"]
                    ),
                    bucket=str(
                        row["bucket"]
                    ),
                    sort_order=int(
                        row["sort_order"]
                    ),
                )
                for row in rows
            )
        finally:
            connection.close()

    def get_display_name(
        self,
        ticker: str,
    ) -> str:
        """
        Return the canonical persistent display name for one ticker.

        Unknown tickers fall back to their normalized ticker symbol so ad hoc
        session-only ticker selections remain displayable without persistent
        universe membership.
        """
        normalized_ticker = str(
            ticker or ""
        ).strip().upper()

        if not normalized_ticker:
            raise ValueError(
                "Ticker cannot be empty."
            )

        connection = self._connect_read_only()

        try:
            self._require_compatible_schema_from_connection(
                connection
            )

            row = connection.execute(
                f"""
                SELECT display_name
                FROM "{self.metadata_table_name}"
                WHERE ticker = ?
                """,
                (normalized_ticker,),
            ).fetchone()

            if row is None:
                return normalized_ticker

            display_name = row["display_name"]

            if display_name is None:
                return normalized_ticker

            normalized_display_name = str(
                display_name
            ).strip()

            return (
                normalized_display_name
                if normalized_display_name
                else normalized_ticker
            )
        finally:
            connection.close()

    def get_all_universe_tickers(
        self,
    ) -> Tuple[str, ...]:
        """
        Return all unique persistent universe tickers in sorted order.

        This mirrors the legacy get_all_tickers() cross-bucket ordering
        semantics rather than inventing a cross-bucket sort order.
        """
        connection = self._connect_read_only()

        try:
            self._require_compatible_schema_from_connection(
                connection
            )

            rows = connection.execute(
                f"""
                SELECT DISTINCT ticker
                FROM "{self.membership_table_name}"
                ORDER BY ticker ASC
                """
            ).fetchall()

            return tuple(
                str(
                    row["ticker"]
                )
                for row in rows
            )
        finally:
            connection.close()

    def get_schema_status(self) -> UniverseSchemaStatus:
        """
        Return read-only persistent universe-schema readiness information.

        This method never creates, alters, or drops database objects.
        """
        connection = self._connect_read_only()

        try:
            return self._get_schema_status_from_connection(
                connection
            )
        finally:
            connection.close()

    def initialize_universe_schema(self) -> UniverseSchemaStatus:
        """
        Explicitly create the persistent ticker-universe tables when absent.

        This operation initializes Phase-2 administrative infrastructure only.

        It does not:
        - mutate daily_prices;
        - import assets.py memberships;
        - create ticker records;
        - create audit events;
        - alter existing universe tables.

        If either configured universe table already exists without the complete
        required schema, initialization raises rather than silently modifying
        the existing database structure.
        """
        existing_status = self.get_schema_status()

        if existing_status.compatible:
            return existing_status

        if (
            existing_status.metadata_exists
            or existing_status.membership_exists
        ):
            problems = []

            if not existing_status.metadata_exists:
                problems.append(
                    f"missing table {self.metadata_table_name}"
                )
            elif existing_status.metadata_missing_columns:
                problems.append(
                    f"{self.metadata_table_name} missing column(s): "
                    + ", ".join(
                        existing_status.metadata_missing_columns
                    )
                )

            if not existing_status.membership_exists:
                problems.append(
                    f"missing table {self.membership_table_name}"
                )
            elif existing_status.membership_missing_columns:
                problems.append(
                    f"{self.membership_table_name} missing column(s): "
                    + ", ".join(
                        existing_status.membership_missing_columns
                    )
                )

            raise RuntimeError(
                "Existing persistent universe schema is incomplete or "
                "incompatible; refusing automatic alteration. "
                + "; ".join(problems)
            )

        metadata_create_sql = f"""
            CREATE TABLE "{self.metadata_table_name}" (
                ticker TEXT PRIMARY KEY,
                display_name TEXT,
                CHECK (
                    ticker <> ''
                    AND ticker = UPPER(TRIM(ticker))
                )
            )
        """

        membership_create_sql = f"""
            CREATE TABLE "{self.membership_table_name}" (
                ticker TEXT NOT NULL,
                bucket TEXT NOT NULL,
                sort_order INTEGER NOT NULL,
                PRIMARY KEY (ticker, bucket),
                UNIQUE (bucket, sort_order),
                FOREIGN KEY (ticker)
                    REFERENCES "{self.metadata_table_name}" (ticker)
                    ON DELETE CASCADE,
                CHECK (
                    bucket IN ('Custom', 'Sector', 'Country')
                ),
                CHECK (
                    sort_order > 0
                )
            )
        """

        connection = self._connect_write()

        try:
            connection.execute("BEGIN")
            connection.execute(metadata_create_sql)
            connection.execute(membership_create_sql)
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

        created_status = self.get_schema_status()

        if not created_status.compatible:
            raise RuntimeError(
                "Persistent universe tables were created but did not satisfy "
                "the required Phase-2 schema contract."
            )

        return created_status

    def commit_assets_bootstrap(
        self,
        preview: UniverseBootstrapPreview,
    ) -> UniverseBootstrapCommitResult:
        """
        Persist one explicitly approved assets.py bootstrap preview.

        This is a one-time initialization boundary for universe content.

        Safety contract:
        - schema must already exist and be compatible;
        - supplied preview must still match current assets.py bootstrap truth;
        - both persistent universe tables must be empty;
        - metadata and membership rows commit in one transaction;
        - committed row counts must exactly match the approved preview;
        - daily_prices is never read or mutated here;
        - an initialized universe is never silently overwritten.
        """
        if not isinstance(
            preview,
            UniverseBootstrapPreview,
        ):
            raise TypeError(
                "preview must be a UniverseBootstrapPreview."
            )

        schema_status = self.get_schema_status()

        if not schema_status.compatible:
            raise RuntimeError(
                "Persistent universe schema is not initialized and "
                "compatible. Initialize the universe schema explicitly "
                "before committing bootstrap content."
            )

        current_preview = self.build_assets_bootstrap_preview()

        if preview != current_preview:
            raise RuntimeError(
                "Approved bootstrap preview no longer matches current "
                "assets.py bootstrap truth. Build and review a new preview "
                "before committing."
            )

        if not preview.ticker_records:
            raise RuntimeError(
                "Bootstrap preview contains no ticker metadata rows."
            )

        if not preview.membership_records:
            raise RuntimeError(
                "Bootstrap preview contains no membership rows."
            )

        metadata_tickers = [
            record.ticker
            for record in preview.ticker_records
        ]

        if len(metadata_tickers) != len(
            set(metadata_tickers)
        ):
            raise RuntimeError(
                "Bootstrap preview contains duplicate ticker metadata rows."
            )

        metadata_ticker_set = set(
            metadata_tickers
        )

        membership_identity = [
            (
                record.ticker,
                record.bucket,
            )
            for record in preview.membership_records
        ]

        if len(membership_identity) != len(
            set(membership_identity)
        ):
            raise RuntimeError(
                "Bootstrap preview contains duplicate "
                "(ticker, bucket) memberships."
            )

        bucket_order_identity = [
            (
                record.bucket,
                record.sort_order,
            )
            for record in preview.membership_records
        ]

        if len(bucket_order_identity) != len(
            set(bucket_order_identity)
        ):
            raise RuntimeError(
                "Bootstrap preview contains duplicate bucket sort_order "
                "values."
            )

        unsupported_buckets = sorted(
            {
                record.bucket
                for record in preview.membership_records
                if record.bucket not in SUPPORTED_UNIVERSE_BUCKETS
            }
        )

        if unsupported_buckets:
            raise RuntimeError(
                "Bootstrap preview contains unsupported bucket(s): "
                + ", ".join(
                    unsupported_buckets
                )
            )

        missing_metadata_tickers = sorted(
            {
                record.ticker
                for record in preview.membership_records
                if record.ticker not in metadata_ticker_set
            }
        )

        if missing_metadata_tickers:
            raise RuntimeError(
                "Bootstrap preview contains membership ticker(s) "
                "without metadata rows: "
                + ", ".join(
                    missing_metadata_tickers
                )
            )

        connection = self._connect_write()

        try:
            connection.execute("BEGIN IMMEDIATE")

            metadata_existing_count = int(
                connection.execute(
                    f"""
                    SELECT COUNT(*)
                    FROM "{self.metadata_table_name}"
                    """
                ).fetchone()[0]
            )

            membership_existing_count = int(
                connection.execute(
                    f"""
                    SELECT COUNT(*)
                    FROM "{self.membership_table_name}"
                    """
                ).fetchone()[0]
            )

            if (
                metadata_existing_count != 0
                or membership_existing_count != 0
            ):
                raise RuntimeError(
                    "Persistent universe content is already initialized; "
                    "refusing assets.py bootstrap. "
                    f"Existing metadata rows: "
                    f"{metadata_existing_count}; "
                    f"existing membership rows: "
                    f"{membership_existing_count}."
                )

            connection.executemany(
                f"""
                INSERT INTO "{self.metadata_table_name}" (
                    ticker,
                    display_name
                )
                VALUES (?, ?)
                """,
                [
                    (
                        record.ticker,
                        record.display_name,
                    )
                    for record in preview.ticker_records
                ],
            )

            connection.executemany(
                f"""
                INSERT INTO "{self.membership_table_name}" (
                    ticker,
                    bucket,
                    sort_order
                )
                VALUES (?, ?, ?)
                """,
                [
                    (
                        record.ticker,
                        record.bucket,
                        record.sort_order,
                    )
                    for record in preview.membership_records
                ],
            )

            metadata_committed_count = int(
                connection.execute(
                    f"""
                    SELECT COUNT(*)
                    FROM "{self.metadata_table_name}"
                    """
                ).fetchone()[0]
            )

            membership_committed_count = int(
                connection.execute(
                    f"""
                    SELECT COUNT(*)
                    FROM "{self.membership_table_name}"
                    """
                ).fetchone()[0]
            )

            if (
                metadata_committed_count
                != preview.ticker_count
            ):
                raise RuntimeError(
                    "Bootstrap metadata verification failed before commit. "
                    f"Expected {preview.ticker_count} row(s); "
                    f"found {metadata_committed_count}."
                )

            if (
                membership_committed_count
                != preview.membership_count
            ):
                raise RuntimeError(
                    "Bootstrap membership verification failed before commit. "
                    f"Expected {preview.membership_count} row(s); "
                    f"found {membership_committed_count}."
                )

            connection.commit()

        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

        return UniverseBootstrapCommitResult(
            metadata_rows_inserted=preview.ticker_count,
            membership_rows_inserted=preview.membership_count,
        )

    def add_to_bucket(
        self,
        ticker: str,
        bucket: str,
        display_name: str | None = None,
    ) -> UniverseMembershipMutationResult:
        """
        Add one persistent ticker-to-bucket membership.

        If ticker metadata does not yet exist, create it in the same
        transaction. Existing ticker metadata is never renamed implicitly.
        """
        normalized_ticker = self._normalize_ticker(
            ticker
        )
        normalized_bucket = self._normalize_bucket_name(
            bucket
        )

        normalized_display_name = (
            self._normalize_display_name(
                display_name
            )
            if display_name is not None
            else normalized_ticker
        )

        connection = self._connect_write()

        try:
            connection.execute(
                "BEGIN IMMEDIATE"
            )

            self._require_compatible_schema_from_connection(
                connection
            )

            existing_membership = connection.execute(
                f"""
                SELECT sort_order
                FROM "{self.membership_table_name}"
                WHERE ticker = ?
                  AND bucket = ?
                """,
                (
                    normalized_ticker,
                    normalized_bucket,
                ),
            ).fetchone()

            if existing_membership is not None:
                raise ValueError(
                    f"{normalized_ticker} is already a member "
                    f"of {normalized_bucket}."
                )

            metadata_row = connection.execute(
                f"""
                SELECT display_name
                FROM "{self.metadata_table_name}"
                WHERE ticker = ?
                """,
                (normalized_ticker,),
            ).fetchone()

            metadata_created = (
                metadata_row is None
            )

            if metadata_created:
                connection.execute(
                    f"""
                    INSERT INTO "{self.metadata_table_name}" (
                        ticker,
                        display_name
                    )
                    VALUES (?, ?)
                    """,
                    (
                        normalized_ticker,
                        normalized_display_name,
                    ),
                )

            next_sort_order = int(
                connection.execute(
                    f"""
                    SELECT COALESCE(
                        MAX(sort_order),
                        0
                    ) + 1
                    FROM "{self.membership_table_name}"
                    WHERE bucket = ?
                    """,
                    (normalized_bucket,),
                ).fetchone()[0]
            )

            connection.execute(
                f"""
                INSERT INTO "{self.membership_table_name}" (
                    ticker,
                    bucket,
                    sort_order
                )
                VALUES (?, ?, ?)
                """,
                (
                    normalized_ticker,
                    normalized_bucket,
                    next_sort_order,
                ),
            )

            committed_row = connection.execute(
                f"""
                SELECT sort_order
                FROM "{self.membership_table_name}"
                WHERE ticker = ?
                  AND bucket = ?
                """,
                (
                    normalized_ticker,
                    normalized_bucket,
                ),
            ).fetchone()

            if (
                committed_row is None
                or int(
                    committed_row["sort_order"]
                )
                != next_sort_order
            ):
                raise RuntimeError(
                    "Add-to-Bucket verification failed "
                    "before commit."
                )

            connection.commit()

        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

        return UniverseMembershipMutationResult(
            action="add",
            ticker=normalized_ticker,
            bucket=normalized_bucket,
            metadata_created=metadata_created,
            sort_order=next_sort_order,
        )

    def remove_from_bucket(
        self,
        ticker: str,
        bucket: str,
    ) -> UniverseMembershipMutationResult:
        """
        Remove exactly one ticker-to-bucket membership.

        Ticker metadata, other bucket memberships, and daily_prices are not
        removed by this operation.
        """
        normalized_ticker = self._normalize_ticker(
            ticker
        )
        normalized_bucket = self._normalize_bucket_name(
            bucket
        )

        connection = self._connect_write()

        try:
            connection.execute(
                "BEGIN IMMEDIATE"
            )

            self._require_compatible_schema_from_connection(
                connection
            )

            existing_membership = connection.execute(
                f"""
                SELECT sort_order
                FROM "{self.membership_table_name}"
                WHERE ticker = ?
                  AND bucket = ?
                """,
                (
                    normalized_ticker,
                    normalized_bucket,
                ),
            ).fetchone()

            if existing_membership is None:
                raise ValueError(
                    f"{normalized_ticker} is not a member "
                    f"of {normalized_bucket}."
                )

            connection.execute(
                f"""
                DELETE FROM "{self.membership_table_name}"
                WHERE ticker = ?
                  AND bucket = ?
                """,
                (
                    normalized_ticker,
                    normalized_bucket,
                ),
            )

            remaining_row = connection.execute(
                f"""
                SELECT 1
                FROM "{self.membership_table_name}"
                WHERE ticker = ?
                  AND bucket = ?
                """,
                (
                    normalized_ticker,
                    normalized_bucket,
                ),
            ).fetchone()

            if remaining_row is not None:
                raise RuntimeError(
                    "Remove-from-Bucket verification failed "
                    "before commit."
                )

            self._renumber_bucket_from_connection(
                connection,
                normalized_bucket,
            )

            metadata_row = connection.execute(
                f"""
                SELECT 1
                FROM "{self.metadata_table_name}"
                WHERE ticker = ?
                """,
                (normalized_ticker,),
            ).fetchone()

            if metadata_row is None:
                raise RuntimeError(
                    "Ticker metadata disappeared during "
                    "membership removal."
                )

            connection.commit()

        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

        return UniverseMembershipMutationResult(
            action="remove",
            ticker=normalized_ticker,
            bucket=normalized_bucket,
            metadata_created=False,
            sort_order=None,
        )

    def update_display_name(
        self,
        ticker: str,
        display_name: str,
    ) -> UniverseDisplayNameMutationResult:
        """
        Update canonical ticker-level display metadata only.
        """
        normalized_ticker = self._normalize_ticker(
            ticker
        )
        normalized_display_name = self._normalize_display_name(
            display_name
        )

        connection = self._connect_write()

        try:
            connection.execute(
                "BEGIN IMMEDIATE"
            )

            self._require_compatible_schema_from_connection(
                connection
            )

            metadata_row = connection.execute(
                f"""
                SELECT display_name
                FROM "{self.metadata_table_name}"
                WHERE ticker = ?
                """,
                (normalized_ticker,),
            ).fetchone()

            if metadata_row is None:
                raise ValueError(
                    f"No persistent ticker metadata exists for "
                    f"{normalized_ticker}."
                )

            previous_display_name = (
                str(
                    metadata_row["display_name"]
                ).strip()
                if metadata_row["display_name"] is not None
                else normalized_ticker
            )

            connection.execute(
                f"""
                UPDATE "{self.metadata_table_name}"
                SET display_name = ?
                WHERE ticker = ?
                """,
                (
                    normalized_display_name,
                    normalized_ticker,
                ),
            )

            committed_row = connection.execute(
                f"""
                SELECT display_name
                FROM "{self.metadata_table_name}"
                WHERE ticker = ?
                """,
                (normalized_ticker,),
            ).fetchone()

            if (
                committed_row is None
                or str(
                    committed_row["display_name"]
                ).strip()
                != normalized_display_name
            ):
                raise RuntimeError(
                    "Display-name update verification failed "
                    "before commit."
                )

            connection.commit()

        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

        return UniverseDisplayNameMutationResult(
            ticker=normalized_ticker,
            previous_display_name=previous_display_name,
            display_name=normalized_display_name,
        )

    def reorder_bucket(
        self,
        bucket: str,
        ordered_tickers: Tuple[str, ...] | list[str],
    ) -> UniverseReorderMutationResult:
        """
        Replace one bucket's ordering without changing its membership set.
        """
        normalized_bucket = self._normalize_bucket_name(
            bucket
        )

        normalized_tickers = tuple(
            self._normalize_ticker(
                ticker
            )
            for ticker in ordered_tickers
        )

        if len(normalized_tickers) != len(
            set(normalized_tickers)
        ):
            raise ValueError(
                "Reorder request contains duplicate ticker(s)."
            )

        connection = self._connect_write()

        try:
            connection.execute(
                "BEGIN IMMEDIATE"
            )

            self._require_compatible_schema_from_connection(
                connection
            )

            current_rows = connection.execute(
                f"""
                SELECT ticker
                FROM "{self.membership_table_name}"
                WHERE bucket = ?
                ORDER BY
                    sort_order ASC,
                    ticker ASC
                """,
                (normalized_bucket,),
            ).fetchall()

            current_tickers = tuple(
                str(
                    row["ticker"]
                )
                for row in current_rows
            )

            if set(normalized_tickers) != set(
                current_tickers
            ):
                missing_tickers = sorted(
                    set(current_tickers)
                    - set(normalized_tickers)
                )
                extra_tickers = sorted(
                    set(normalized_tickers)
                    - set(current_tickers)
                )

                raise ValueError(
                    "Reorder request must contain exactly the "
                    "current bucket membership. "
                    f"Missing: {missing_tickers}; "
                    f"extra: {extra_tickers}."
                )

            if len(normalized_tickers) != len(
                current_tickers
            ):
                raise ValueError(
                    "Reorder request length does not match "
                    "current bucket membership."
                )

            if normalized_tickers:
                max_sort_order = int(
                    connection.execute(
                        f"""
                        SELECT COALESCE(
                            MAX(sort_order),
                            0
                        )
                        FROM "{self.membership_table_name}"
                        WHERE bucket = ?
                        """,
                        (normalized_bucket,),
                    ).fetchone()[0]
                )

                temporary_offset = (
                    max_sort_order
                    + len(normalized_tickers)
                    + 1
                )

                connection.execute(
                    f"""
                    UPDATE "{self.membership_table_name}"
                    SET sort_order = sort_order + ?
                    WHERE bucket = ?
                    """,
                    (
                        temporary_offset,
                        normalized_bucket,
                    ),
                )

                for sort_order, ticker in enumerate(
                    normalized_tickers,
                    start=1,
                ):
                    connection.execute(
                        f"""
                        UPDATE "{self.membership_table_name}"
                        SET sort_order = ?
                        WHERE ticker = ?
                          AND bucket = ?
                        """,
                        (
                            sort_order,
                            ticker,
                            normalized_bucket,
                        ),
                    )

            committed_rows = connection.execute(
                f"""
                SELECT
                    ticker,
                    sort_order
                FROM "{self.membership_table_name}"
                WHERE bucket = ?
                ORDER BY sort_order ASC
                """,
                (normalized_bucket,),
            ).fetchall()

            committed_tickers = tuple(
                str(
                    row["ticker"]
                )
                for row in committed_rows
            )

            committed_sort_orders = tuple(
                int(
                    row["sort_order"]
                )
                for row in committed_rows
            )

            expected_sort_orders = tuple(
                range(
                    1,
                    len(normalized_tickers) + 1,
                )
            )

            if committed_tickers != normalized_tickers:
                raise RuntimeError(
                    "Bucket reorder verification failed "
                    "before commit."
                )

            if committed_sort_orders != expected_sort_orders:
                raise RuntimeError(
                    "Bucket reorder produced non-contiguous "
                    "sort_order values."
                )

            connection.commit()

        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

        return UniverseReorderMutationResult(
            bucket=normalized_bucket,
            ordered_tickers=normalized_tickers,
        )

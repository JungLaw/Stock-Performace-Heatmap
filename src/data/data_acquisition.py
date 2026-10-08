"""
Canonical yFinance acquisition for Data Management.

This module owns source acquisition only. It translates an explicit inclusive
Data Management request into canonical daily yFinance requests and returns
source observations for DataMutationManager planning.

This module does NOT:

- write to daily_prices or any other database table
- classify database collisions
- own mutation validation or Source Missing semantics
- build, confirm, or commit MutationPlan objects
- replace legacy dashboard acquisition/persistence paths

Permanent Data Management acquisition uses auto_adjust=False and requires the
genuine Adj Close field returned by yFinance. Close is never substituted for
Adj Close here.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Any, Dict, Iterable, List, Optional, Tuple

import pandas as pd
import yfinance as yf

from src.data.market_calendar import (
    get_latest_expected_stored_session,
)


SOURCE_NAME = "yFinance"

CANONICAL_SOURCE_FIELDS: Tuple[str, ...] = (
    "Open",
    "High",
    "Low",
    "Close",
    "Adj Close",
    "Volume",
)


@dataclass(frozen=True)
class DataAcquisitionIssue:
    """One source/acquisition finding produced before mutation planning."""

    level: str
    code: str
    message: str
    ticker: Optional[str] = None


@dataclass(frozen=True)
class DataAcquisitionResult:
    """Materialized result of one read-only Data Management acquisition."""

    source: str
    requested_tickers: Tuple[str, ...]
    requested_start_date: date
    requested_end_date: date
    effective_start_date: Optional[date]
    effective_end_date: Optional[date]
    latest_expected_stored_session: date
    yfinance_end_exclusive: Optional[date]
    candidates: Tuple[Dict[str, Any], ...]
    issues: Tuple[DataAcquisitionIssue, ...]

    @property
    def has_effective_scope(self) -> bool:
        """Return whether any requested dates are eligible for persistence."""
        return (
            self.effective_start_date is not None
            and self.effective_end_date is not None
        )


class DataAcquisitionManager:
    """Read-only canonical yFinance acquisition owner for Data Management."""

    @staticmethod
    def _normalize_date_value(
        value: Any,
        field_name: str,
    ) -> date:
        """Normalize one requested date without introducing time semantics."""
        if isinstance(value, datetime):
            return value.date()

        if isinstance(value, date):
            return value

        try:
            parsed = pd.Timestamp(value)
        except Exception as exc:
            raise ValueError(
                f"{field_name} must be a valid date."
            ) from exc

        if pd.isna(parsed):
            raise ValueError(
                f"{field_name} must be a valid date."
            )

        return parsed.date()

    @staticmethod
    def _normalize_tickers(
        tickers: Iterable[Any],
    ) -> Tuple[str, ...]:
        """Normalize ticker request order while removing duplicates."""
        if isinstance(tickers, str):
            ticker_values: Iterable[Any] = [tickers]
        else:
            ticker_values = tickers

        normalized: List[str] = []
        seen: set[str] = set()

        for raw_ticker in ticker_values:
            ticker = str(raw_ticker or "").strip().upper()

            if not ticker:
                raise ValueError(
                    "Ticker values must be non-empty."
                )

            if ticker in seen:
                continue

            seen.add(ticker)
            normalized.append(ticker)

        if not normalized:
            raise ValueError(
                "At least one ticker is required."
            )

        return tuple(normalized)

    @staticmethod
    def _flatten_single_ticker_columns(
        frame: pd.DataFrame,
    ) -> pd.DataFrame:
        """Flatten yFinance single-ticker MultiIndex columns."""
        normalized = frame.copy()

        if isinstance(normalized.columns, pd.MultiIndex):
            normalized.columns = [
                column[0]
                if isinstance(column, tuple)
                else column
                for column in normalized.columns
            ]

        return normalized

    @staticmethod
    def _to_python_scalar(value: Any) -> Any:
        """Return a plain Python scalar while preserving missing source data."""
        if pd.isna(value):
            return None

        item_method = getattr(
            value,
            "item",
            None,
        )

        if callable(item_method):
            try:
                return item_method()
            except Exception:
                pass

        return value

    @staticmethod
    def _download_one_ticker(
        ticker: str,
        start_date: date,
        end_exclusive: date,
    ) -> pd.DataFrame:
        """Perform one canonical daily yFinance request for one ticker."""
        return yf.download(
            ticker,
            start=start_date.isoformat(),
            end=end_exclusive.isoformat(),
            interval="1d",
            auto_adjust=False,
            progress=False,
        )

    @classmethod
    def _frame_to_candidates(
        cls,
        *,
        ticker: str,
        frame: pd.DataFrame,
        effective_start_date: date,
        effective_end_date: date,
    ) -> List[Dict[str, Any]]:
        """
        Convert returned source rows to mutation-planning candidate mappings.

        This method performs source-shape normalization only. Structural and
        numeric mutation validation remain owned by DataMutationManager.
        """
        normalized = cls._flatten_single_ticker_columns(
            frame
        )

        candidates: List[Dict[str, Any]] = []

        for index_value, row in normalized.iterrows():
            try:
                timestamp = pd.Timestamp(
                    index_value
                )
            except Exception:
                continue

            if pd.isna(timestamp):
                continue

            if timestamp.tzinfo is not None:
                timestamp = timestamp.tz_localize(
                    None
                )

            record_date = timestamp.date()

            if not (
                effective_start_date
                <= record_date
                <= effective_end_date
            ):
                continue

            candidate: Dict[str, Any] = {
                "Ticker": ticker,
                "Date": record_date.isoformat(),
            }

            for field_name in CANONICAL_SOURCE_FIELDS:
                candidate[field_name] = (
                    cls._to_python_scalar(
                        row[field_name]
                    )
                    if field_name
                    in normalized.columns
                    else None
                )

            candidates.append(
                candidate
            )

        return candidates

    def acquire_daily_ohlcv(
        self,
        *,
        tickers: Iterable[Any],
        requested_start_date: Any,
        requested_end_date: Any,
    ) -> DataAcquisitionResult:
        """
        Acquire canonical daily OHLCV for an inclusive Data Management request.

        The effective persistence scope is clipped to the Latest Expected
        Stored Session. yFinance receives end + 1 calendar day because its
        historical end boundary is exclusive. Returned rows are filtered back
        to the exact effective inclusive scope.

        If the entire Adj Close column is missing, one identical canonical
        request is retried. If Adj Close remains unavailable, returned rows are
        still materialized with Adj Close=None so the existing mutation
        validation boundary can exclude them explicitly; Close is never used as
        a substitute.
        """
        normalized_tickers = (
            self._normalize_tickers(
                tickers
            )
        )

        requested_start = (
            self._normalize_date_value(
                requested_start_date,
                "Requested Start Date",
            )
        )

        requested_end = (
            self._normalize_date_value(
                requested_end_date,
                "Requested End Date",
            )
        )

        if requested_start > requested_end:
            raise ValueError(
                "Requested Start Date cannot be later "
                "than End Date."
            )

        latest_expected = (
            get_latest_expected_stored_session()
        )

        effective_end = min(
            requested_end,
            latest_expected,
        )

        issues: List[
            DataAcquisitionIssue
        ] = []

        if requested_end > latest_expected:
            issues.append(
                DataAcquisitionIssue(
                    level="warning",
                    code=(
                        "request_clipped_to_"
                        "persistence_boundary"
                    ),
                    message=(
                        "Requested End Date exceeds the "
                        "Latest Expected Stored Session. "
                        "The effective acquisition scope "
                        f"ends on "
                        f"{latest_expected.isoformat()}."
                    ),
                )
            )

        if requested_start > effective_end:
            issues.append(
                DataAcquisitionIssue(
                    level="warning",
                    code=(
                        "no_persistable_requested_dates"
                    ),
                    message=(
                        "The requested interval contains "
                        "no dates eligible for permanent "
                        "storage under the current "
                        "persistence boundary."
                    ),
                )
            )

            return DataAcquisitionResult(
                source=SOURCE_NAME,
                requested_tickers=(
                    normalized_tickers
                ),
                requested_start_date=(
                    requested_start
                ),
                requested_end_date=(
                    requested_end
                ),
                effective_start_date=None,
                effective_end_date=None,
                latest_expected_stored_session=(
                    latest_expected
                ),
                yfinance_end_exclusive=None,
                candidates=(),
                issues=tuple(issues),
            )

        effective_start = requested_start

        yfinance_end_exclusive = (
            effective_end
            + timedelta(days=1)
        )

        candidates: List[
            Dict[str, Any]
        ] = []

        for ticker in normalized_tickers:
            try:
                frame = (
                    self._download_one_ticker(
                        ticker,
                        effective_start,
                        yfinance_end_exclusive,
                    )
                )
            except Exception as exc:
                issues.append(
                    DataAcquisitionIssue(
                        level="error",
                        code=(
                            "source_request_failed"
                        ),
                        message=(
                            "yFinance request failed: "
                            f"{exc}"
                        ),
                        ticker=ticker,
                    )
                )
                continue

            if (
                frame is None
                or frame.empty
            ):
                issues.append(
                    DataAcquisitionIssue(
                        level="warning",
                        code=(
                            "no_data_returned"
                        ),
                        message=(
                            "yFinance returned no "
                            "observations for the "
                            "effective requested "
                            "interval."
                        ),
                        ticker=ticker,
                    )
                )
                continue

            normalized_frame = (
                self._flatten_single_ticker_columns(
                    frame
                )
            )

            if (
                "Adj Close"
                not in normalized_frame.columns
            ):
                issues.append(
                    DataAcquisitionIssue(
                        level="warning",
                        code="adj_close_retry",
                        message=(
                            "yFinance did not return "
                            "Adj Close. Retrying the "
                            "same canonical request once."
                        ),
                        ticker=ticker,
                    )
                )

                try:
                    retry_frame = (
                        self._download_one_ticker(
                            ticker,
                            effective_start,
                            yfinance_end_exclusive,
                        )
                    )
                except Exception as exc:
                    issues.append(
                        DataAcquisitionIssue(
                            level="error",
                            code=(
                                "adj_close_retry_failed"
                            ),
                            message=(
                                "Adj Close retry request "
                                f"failed: {exc}"
                            ),
                            ticker=ticker,
                        )
                    )
                else:
                    if (
                        retry_frame is not None
                        and not retry_frame.empty
                    ):
                        normalized_retry = (
                            self
                            ._flatten_single_ticker_columns(
                                retry_frame
                            )
                        )

                        if (
                            "Adj Close"
                            in normalized_retry.columns
                        ):
                            normalized_frame = (
                                normalized_retry
                            )

                if (
                    "Adj Close"
                    not in normalized_frame.columns
                ):
                    issues.append(
                        DataAcquisitionIssue(
                            level="error",
                            code=(
                                "adj_close_unavailable"
                            ),
                            message=(
                                "Genuine Adj Close "
                                "remains unavailable "
                                "after the canonical "
                                "retry. Returned "
                                "observations will carry "
                                "Adj Close=None for "
                                "explicit exclusion by "
                                "mutation validation."
                            ),
                            ticker=ticker,
                        )
                    )

            candidates.extend(
                self._frame_to_candidates(
                    ticker=ticker,
                    frame=normalized_frame,
                    effective_start_date=(
                        effective_start
                    ),
                    effective_end_date=(
                        effective_end
                    ),
                )
            )

        return DataAcquisitionResult(
            source=SOURCE_NAME,
            requested_tickers=(
                normalized_tickers
            ),
            requested_start_date=(
                requested_start
            ),
            requested_end_date=(
                requested_end
            ),
            effective_start_date=(
                effective_start
            ),
            effective_end_date=(
                effective_end
            ),
            latest_expected_stored_session=(
                latest_expected
            ),
            yfinance_end_exclusive=(
                yfinance_end_exclusive
            ),
            candidates=tuple(
                candidates
            ),
            issues=tuple(
                issues
            ),
        )
"""
Read-only database inspection services for Data Management.

Workstream 1 intentionally provides inspection only. It does not acquire
market data, validate incoming observations, or mutate persistent data.
"""

from datetime import date
from pathlib import Path
import sqlite3
from typing import Any, Dict, List

from src.config.assets import (
    COUNTRY_ETFS,
    CUSTOM_DEFAULT,
    SECTOR_ETFS,
    get_tickers_only,
)
from src.config.settings import DATABASE_FILE, TABLE_NAME
from src.data.market_calendar import (
    get_expected_sessions,
    get_latest_expected_stored_session,
)


class DatabaseManager:
    """
    Read-only access to the application's authoritative OHLCV database.

    Workstream 1 scope:
    - database-wide overview statistics
    - per-ticker inventory
    - configured universe membership annotation

    Mutation methods are intentionally absent.
    """

    def __init__(self, database_file: str = DATABASE_FILE) -> None:
        self.database_path = Path(database_file)

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

    @staticmethod
    def _configured_memberships() -> Dict[str, set[str]]:
        """
        Return configured ticker memberships by Data Management universe.

        A ticker may legitimately belong to more than one configured universe.
        """
        return {
            "Custom": {
                str(ticker).upper()
                for ticker in get_tickers_only(CUSTOM_DEFAULT)
            },
            "Sector": {
                str(ticker).upper()
                for ticker in get_tickers_only(SECTOR_ETFS)
            },
            "Country": {
                str(ticker).upper()
                for ticker in get_tickers_only(COUNTRY_ETFS)
            },
        }

    @classmethod
    def _bucket_labels_for_ticker(cls, ticker: str) -> List[str]:
        """
        Return every configured universe containing ticker.

        An empty list means the ticker is stored in the database but is
        currently unassigned to Custom, Sector, or Country.
        """
        ticker_upper = str(ticker).upper()
        memberships = cls._configured_memberships()

        return [
            bucket_name
            for bucket_name, bucket_tickers in memberships.items()
            if ticker_upper in bucket_tickers
        ]

    @staticmethod
    def _calculate_ticker_health(
        stored_dates: List[str],
        expected_sessions: set[date],
        latest_expected_stored_session: date,
    ) -> Dict[str, Any]:
        """
        Calculate read-only database-health metrics for one stored ticker.

        Coverage and internal gaps are measured only between the ticker's own
        first and last stored dates. Staleness is measured separately against
        the latest NYSE session expected to be stored under the Data Management
        next-day ingestion policy.
        """
        actual_dates = {
            date.fromisoformat(stored_date)
            for stored_date in stored_dates
        }

        if not actual_dates:
            return {
                "coverage": None,
                "internal_gaps": 0,
                "is_current": False,
                "is_stale": False,
                "status": None,
            }

        first_date = min(actual_dates)
        last_date = max(actual_dates)

        expected_dates = {
            session_date
            for session_date in expected_sessions
            if first_date <= session_date <= last_date
        }

        present_expected_dates = expected_dates.intersection(actual_dates)
        missing_expected_dates = expected_dates.difference(actual_dates)

        coverage = (
            (len(present_expected_dates) / len(expected_dates)) * 100.0
            if expected_dates
            else None
        )

        is_current = last_date == latest_expected_stored_session
        is_stale = last_date < latest_expected_stored_session

        if is_current:
            status = "Current"
        elif is_stale:
            status = "Stale"
        else:
            status = None

        return {
            "coverage": coverage,
            "internal_gaps": len(missing_expected_dates),
            "is_current": is_current,
            "is_stale": is_stale,
            "status": status,
        }

    def get_database_overview(
        self,
        inventory: List[Dict[str, Any]] | None = None,
        ) -> Dict[str, Any]:
        """
        Return database-wide inventory and health statistics for daily_prices.

        These metrics describe the complete authoritative table and are not
        affected by later UI universe filters.
        """
        query = f"""
            SELECT
                COUNT(DISTINCT Ticker) AS unique_tickers,
                COUNT(*) AS total_records,
                MIN(Date) AS earliest_date,
                MAX(Date) AS latest_stored_date
            FROM "{TABLE_NAME}"
        """

        latest_expected_stored_session = (
            get_latest_expected_stored_session()
        )

        if inventory is None:
            inventory = self.get_ticker_inventory(
                latest_expected_stored_session=latest_expected_stored_session
            )

        with self._connect_read_only() as connection:
            row = connection.execute(query).fetchone()

        if row is None:
            return {
                "unique_tickers": 0,
                "total_records": 0,
                "earliest_date": None,
                "latest_stored_date": None,
                "latest_expected_stored_session": (
                    latest_expected_stored_session.isoformat()
                ),
                "current_tickers": 0,
                "stale_tickers": 0,
                "tickers_with_internal_gaps": 0,
            }

        return {
            "unique_tickers": int(row["unique_tickers"] or 0),
            "total_records": int(row["total_records"] or 0),
            "earliest_date": row["earliest_date"],
            "latest_stored_date": row["latest_stored_date"],
            "latest_expected_stored_session": (
                latest_expected_stored_session.isoformat()
            ),
            "current_tickers": sum(
                1 for item in inventory if item["is_current"]
            ),
            "stale_tickers": sum(
                1 for item in inventory if item["is_stale"]
            ),
            "tickers_with_internal_gaps": sum(
                1 for item in inventory if item["internal_gaps"] > 0
            ),
        }

    def get_ticker_inventory(
        self,
        latest_expected_stored_session: date | None = None,
    ) -> List[Dict[str, Any]]:
        """
        Return one inventory row for each ticker stored in daily_prices.

        Universe membership is descriptive only. Database membership and
        configured-universe membership remain independent concepts.

        Coverage and internal gaps are measured between each ticker's own
        first and last stored dates. Current/stale status is measured against the latest
        NYSE session expected to be stored under the Data Management next-day ingestion policy.
        """
        query = f"""
            SELECT
                Ticker AS ticker,
                Date AS date
            FROM "{TABLE_NAME}"
            ORDER BY Ticker, Date
        """

        if latest_expected_stored_session is None:
            latest_expected_stored_session = (
                get_latest_expected_stored_session()
            )

        with self._connect_read_only() as connection:
            rows = connection.execute(query).fetchall()

        dates_by_ticker: Dict[str, List[str]] = {}

        for row in rows:
            ticker = str(row["ticker"]).upper()
            dates_by_ticker.setdefault(ticker, []).append(
                str(row["date"])
            )

        if not dates_by_ticker:
            return []

        earliest_stored_date = min(
            date.fromisoformat(stored_dates[0])
            for stored_dates in dates_by_ticker.values()
        )
        latest_stored_date = max(
            date.fromisoformat(stored_dates[-1])
            for stored_dates in dates_by_ticker.values()
        )

        expected_sessions = set(
            get_expected_sessions(
                earliest_stored_date,
                latest_stored_date,
            )
        )

        inventory: List[Dict[str, Any]] = []

        for ticker in sorted(dates_by_ticker):
            stored_dates = dates_by_ticker[ticker]
            bucket_labels = self._bucket_labels_for_ticker(ticker)
            health = self._calculate_ticker_health(
                stored_dates,
                expected_sessions,
                latest_expected_stored_session,
            )

            inventory.append(
                {
                    "ticker": ticker,
                    "buckets": bucket_labels,
                    "records": len(stored_dates),
                    "first_date": stored_dates[0],
                    "last_date": stored_dates[-1],
                    "coverage": health["coverage"],
                    "internal_gaps": health["internal_gaps"],
                    "is_current": health["is_current"],
                    "is_stale": health["is_stale"],
                    "status": health["status"],
                }
            )

        return inventory
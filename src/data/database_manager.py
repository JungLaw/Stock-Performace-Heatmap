"""
Read-only database inspection services for Data Management.

Workstream 1 intentionally provides inspection only. It does not acquire
market data, validate incoming observations, or mutate persistent data.
"""

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

    def get_database_overview(self) -> Dict[str, Any]:
        """
        Return database-wide inventory statistics for daily_prices.

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

        with self._connect_read_only() as connection:
            row = connection.execute(query).fetchone()

        if row is None:
            return {
                "unique_tickers": 0,
                "total_records": 0,
                "earliest_date": None,
                "latest_stored_date": None,
            }

        return {
            "unique_tickers": int(row["unique_tickers"] or 0),
            "total_records": int(row["total_records"] or 0),
            "earliest_date": row["earliest_date"],
            "latest_stored_date": row["latest_stored_date"],
        }

    def get_ticker_inventory(self) -> List[Dict[str, Any]]:
        """
        Return one inventory row for each ticker stored in daily_prices.

        Universe membership is descriptive only. Database membership and
        configured-universe membership remain independent concepts.
        """
        query = f"""
            SELECT
                Ticker AS ticker,
                COUNT(*) AS records,
                MIN(Date) AS first_date,
                MAX(Date) AS last_date
            FROM "{TABLE_NAME}"
            GROUP BY Ticker
            ORDER BY Ticker
        """

        with self._connect_read_only() as connection:
            rows = connection.execute(query).fetchall()

        inventory: List[Dict[str, Any]] = []

        for row in rows:
            ticker = str(row["ticker"]).upper()
            bucket_labels = self._bucket_labels_for_ticker(ticker)

            inventory.append(
                {
                    "ticker": ticker,
                    "buckets": bucket_labels,
                    "records": int(row["records"]),
                    "first_date": row["first_date"],
                    "last_date": row["last_date"],
                }
            )

        return inventory
"""
NYSE session-calendar services for Data Management.

This module owns the canonical exchange-session semantics used by the new
Data Management path. It is intentionally independent of the existing
Performance calendar helpers, whose behavior remains unchanged.
"""

from datetime import date, datetime
from typing import List, Optional, Union

import pandas as pd
import pandas_market_calendars as mcal


DateLike = Union[str, date, datetime, pd.Timestamp]

_NYSE_CALENDAR = mcal.get_calendar("NYSE")
_NEW_YORK_TIMEZONE = "America/New_York"


def get_expected_sessions(
    start_date: DateLike,
    end_date: DateLike,
) -> List[date]:
    """
    Return expected NYSE session dates within an inclusive date range.

    Weekends, exchange holidays, and other non-session dates are excluded by
    the NYSE calendar. Returned values are plain date objects in ascending
    order.
    """
    schedule = _NYSE_CALENDAR.schedule(
        start_date=start_date,
        end_date=end_date,
    )

    return [
        session_timestamp.date()
        for session_timestamp in schedule.index
    ]


def is_completed_session(
    session_date: DateLike,
    as_of: Optional[DateLike] = None,
) -> bool:
    """
    Return whether a NYSE session has completed as of the supplied timestamp.

    Non-session dates return False.

    When as_of is omitted, the current time in New York is used. A session is
    considered completed when as_of is greater than or equal to that session's
    scheduled market close, including special early closes.
    """
    session_timestamp = pd.Timestamp(session_date)

    schedule = _NYSE_CALENDAR.schedule(
        start_date=session_timestamp.date(),
        end_date=session_timestamp.date(),
    )

    if schedule.empty:
        return False

    market_close = schedule.iloc[0]["market_close"]

    if as_of is None:
        comparison_time = pd.Timestamp.now(
            tz=_NEW_YORK_TIMEZONE
        )
    else:
        comparison_time = pd.Timestamp(as_of)

        if comparison_time.tzinfo is None:
            comparison_time = comparison_time.tz_localize(
                _NEW_YORK_TIMEZONE
            )

    comparison_time_utc = comparison_time.tz_convert("UTC")

    return bool(comparison_time_utc >= market_close)


def get_latest_completed_session(
    as_of: Optional[DateLike] = None,
) -> date:
    """
    Return the latest completed NYSE session as of the supplied timestamp.

    When as_of is omitted, the current time in New York is used. The method
    uses the exchange's scheduled market-close timestamps, so ordinary closes,
    early closes, weekends, and exchange holidays are handled consistently.
    """
    if as_of is None:
        comparison_time = pd.Timestamp.now(
            tz=_NEW_YORK_TIMEZONE
        )
    else:
        comparison_time = pd.Timestamp(as_of)

        if comparison_time.tzinfo is None:
            comparison_time = comparison_time.tz_localize(
                _NEW_YORK_TIMEZONE
            )

    comparison_time_utc = comparison_time.tz_convert("UTC")

    lookback_start = (
        comparison_time
        - pd.Timedelta(days=10)
    ).date()

    schedule = _NYSE_CALENDAR.schedule(
        start_date=lookback_start,
        end_date=comparison_time.date(),
    )

    completed_schedule = schedule[
        schedule["market_close"] <= comparison_time_utc
    ]

    if completed_schedule.empty:
        raise ValueError(
            "Unable to identify a completed NYSE session "
            "within the calendar lookback window."
        )

    return completed_schedule.index[-1].date()


def get_latest_expected_stored_session(
    as_of: Optional[DateLike] = None,
) -> date:
    """
    Return the latest NYSE session expected to be stored in daily_prices.

    Data Management intentionally uses a one-calendar-day ingestion lag for
    daily Yahoo Finance observations so final daily fields, especially Volume,
    can settle before persistence.

    Therefore, the expected stored endpoint is the most recent NYSE session
    strictly before the current New York calendar date.
    """
    if as_of is None:
        comparison_time = pd.Timestamp.now(
            tz=_NEW_YORK_TIMEZONE
        )
    else:
        comparison_time = pd.Timestamp(as_of)

        if comparison_time.tzinfo is None:
            comparison_time = comparison_time.tz_localize(
                _NEW_YORK_TIMEZONE
            )

    new_york_time = comparison_time.tz_convert(
        _NEW_YORK_TIMEZONE
    )

    prior_calendar_date = (
        new_york_time.date()
        - pd.Timedelta(days=1)
    )

    lookback_start = (
        pd.Timestamp(prior_calendar_date)
        - pd.Timedelta(days=10)
    ).date()

    schedule = _NYSE_CALENDAR.schedule(
        start_date=lookback_start,
        end_date=prior_calendar_date,
    )

    if schedule.empty:
        raise ValueError(
            "Unable to identify an expected stored NYSE session "
            "within the calendar lookback window."
        )

    return schedule.index[-1].date()

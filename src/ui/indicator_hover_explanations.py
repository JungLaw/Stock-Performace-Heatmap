"""Display-only, fail-closed explanations for approved indicator hover semantics."""
from __future__ import annotations

import ast
from functools import lru_cache
from numbers import Real
from typing import Mapping, Optional


_HMA_DISTANCES = {9: 0.25, 16: 0.50, 21: 0.50, 50: 0.50, 55: 0.50, 200: 2.00}
_HMA_BUY_SLOPES = {9: 0.20, 16: 0.20, 21: 0.20, 50: 0.20, 55: 0.20, 200: 0.25}
_HMA_TIMING_REFERENCES = {16: "the HMA(16) 14-bar", 21: "the HMA(55)", 55: "the HMA(200)"}
_HMA_DIRECTIONS = ("Up", "Down", "None")
_HMA_TRENDS = ("Rising", "Falling", "Flat")
_HMA_STATES = ("strong_buy", "buy", "neutral", "sell", "strong_sell")


def _fingerprint(expression: str) -> Optional[str]:
    """Canonical Python expression shape, not a second expression evaluator."""
    if not isinstance(expression, str) or not expression.strip():
        return None
    try:
        return ast.dump(ast.parse(expression, mode="eval"), include_attributes=False)
    except (SyntaxError, ValueError, TypeError):
        return None


@lru_cache(maxsize=None)
def _approved_hma_expressions(period: int) -> dict[str, str]:
    """Independent reviewed rule specification; source data remains authoritative."""
    distance = _HMA_DISTANCES[period]
    low_slope = _HMA_BUY_SLOPES[period]
    dist = f"(Close - HMA_{period}) / ATR_14"
    slope = f"(HMA_{period}_slope__linreg_14 / HMA_{period}) * 100"
    return {
        "strong_buy": f"{dist} > {distance:.2f} and {slope} > 0.50",
        "buy": f"{dist} > {distance:.2f} and {slope} > {low_slope:.2f} and {slope} <= 0.50",
        "neutral": "",
        "sell": f"{dist} < -{distance:.2f} and {slope} < -{low_slope:.2f} and {slope} >= -0.50",
        "strong_sell": f"{dist} < -{distance:.2f} and {slope} < -0.50",
    }


def get_hma_rule_explanation(period: int, state: str, active_rules: Mapping[str, str]) -> Optional[str]:
    """Return prose only when all five active HMA rules match audited semantics.

    Neutral is a classifier fallback, not an executable neutral expression; the
    complete five-state fingerprint protects that fallback's explanation.
    """
    if period not in _HMA_DISTANCES or state not in _HMA_STATES:
        return None
    approved = _approved_hma_expressions(period)
    if not isinstance(active_rules, Mapping):
        return None
    for key in _HMA_STATES:
        actual = str(active_rules.get(key, "") or "")
        expected = approved[key]
        if key == "neutral":
            if actual.strip():
                return None
        elif _fingerprint(actual) != _fingerprint(expected):
            return None
    distance = f"{_HMA_DISTANCES[period]:.2f}"
    low = f"{_HMA_BUY_SLOPES[period]:.2f}"
    expressions = {
        "strong_buy": f"Price is more than {distance} ATR above HMA({period}), and its established 14-bar slope exceeds +0.50% per bar. Both strong bullish qualifications are satisfied.",
        "buy": f"Price is more than {distance} ATR above HMA({period}), and its established 14-bar slope is above +{low}% but no greater than +0.50% per bar. A qualified bullish trend is present, below the Strong slope threshold.",
        "neutral": "Price position and the established HMA slope do not jointly satisfy any complete bullish or bearish classification rule. No qualified directional HMA Signal is present.",
        "sell": f"Price is more than {distance} ATR below HMA({period}), and its established 14-bar slope is below -{low}% but no less than -0.50% per bar. A qualified bearish trend is present, below the Strong slope magnitude.",
        "strong_sell": f"Price is more than {distance} ATR below HMA({period}), and its established 14-bar slope is below -0.50% per bar. Both strong bearish qualifications are satisfied.",
    }
    return expressions[state]


def get_hma_context_interpretation(period: int, state: str, turn: str, trend: str, turn_context: str) -> Optional[str]:
    """Translate only an upstream-consistent HMA context combination."""
    if period not in _HMA_TIMING_REFERENCES or state not in _HMA_STATES:
        return None
    if turn not in _HMA_DIRECTIONS or trend not in _HMA_TRENDS:
        return None
    # The upstream context tag must agree with the supplied raw turn/trend pair.
    expected = {
        ("Up", "Rising"): "Bullish Trend-Aligned",
        ("Up", "Falling"): "Bullish Counter-Trend",
        ("Down", "Falling"): "Bearish Trend-Aligned",
        ("Down", "Rising"): "Bearish Counter-Trend",
    }.get((turn, trend))
    if turn == "None":
        if turn_context not in (None, "", "—"):
            return None
        if state == "neutral":
            return "Neither a qualified directional HMA Signal nor a fresh HMA turning event is present today."
        strength = "strong " if state.startswith("strong_") else ""
        side = "bullish" if state in ("buy", "strong_buy") else "bearish"
        return f"A qualified {strength}{side} HMA trend is present, but no fresh turning event occurred today. The Signal describes an established trend, not a new transition."
    if expected is None:
        # A turning event with unavailable/flat trend has no directional alignment label.
        if trend == "Flat" and turn_context in (None, "", "—"):
            direction = "upward" if turn == "Up" else "downward"
            return f"HMA has just turned {direction}, but its broader reference trend is Flat; the turn is not classified as trend-aligned or counter-trend."
        return None
    if turn_context != expected:
        return None
    direction = "upward" if turn == "Up" else "downward"
    reference = _HMA_TIMING_REFERENCES[period]
    alignment = "with" if "Trend-Aligned" in expected else "against"
    base = f"HMA({period}) has just turned {direction} {alignment} {reference} reference trend, which is {trend.lower()}."
    if state == "neutral":
        return base + " This is an early transition, but the primary directional Signal has not qualified."
    qualified = "bullish" if state in ("buy", "strong_buy") else "bearish"
    if (qualified == "bullish" and turn == "Up") or (qualified == "bearish" and turn == "Down"):
        return base + f" The fresh turn supports the qualified {qualified} Signal, while remaining a separate timing observation."
    return base + f" The fresh turn opposes the qualified {qualified} Signal; established trend qualification and immediate turning information are in tension."

# UO's seven-state explanation is display-only. The executable rulebook has
# five score-level flags; Watch and Divergence are distinct upstream states.
_UO_APPROVED_RULES = {
    "strong_buy": "UO_BULLISH_CONFIRMED",
    "buy": "UO_BULLISH_SETUP",
    "neutral": "UO_NO_ACTIVE_SETUP",
    "sell": "UO_BEARISH_SETUP",
    "strong_sell": "UO_BEARISH_CONFIRMED",
}
_UO_EXPECTED_SCORES = {
    "Bullish Confirmed": 2,
    "Bullish Divergence": 1,
    "Bullish Watch": 1,
    "No Active Setup": 0,
    "Bearish Watch": -1,
    "Bearish Divergence": -1,
    "Bearish Confirmed": -2,
}
_UO_WATCH_THRESHOLDS = {
    "UO_5_10_15": 30,
    "UO_7_14_28": 35,
    "UO_10_20_40": 35,
}


def get_uo_rule_explanation(
    indicator_key: str,
    semantic_state: str,
    active_rules: Mapping[str, str],
    score: int,
) -> Optional[str]:
    """Translate approved upstream UO state; never classify or infer from score.

    Return None on missing/inconsistent inputs or rulebook drift so the adapter
    retains its existing generic rulebook-translation fallback.
    """
    if indicator_key not in _UO_WATCH_THRESHOLDS:
        return None
    if semantic_state not in _UO_EXPECTED_SCORES:
        return None
    if isinstance(score, bool) or not isinstance(score, Real) or score != _UO_EXPECTED_SCORES[semantic_state]:
        return None
    if not isinstance(active_rules, Mapping):
        return None
    if any(
        str(active_rules.get(state, "") or "").strip() != expression
        for state, expression in _UO_APPROVED_RULES.items()
    ):
        return None

    # Wording is copied verbatim from the production adapter's seven-state
    # conditional block. Do not revise prose during this ownership migration.
    descriptions = {
        "Bullish Confirmed": (
            "Qualifying bullish divergence + UO broke above its "
            "Classic Confirmation trigger within the 10-session window."
        ),
        "Bullish Divergence": (
            "Lower confirmed price low + higher UO pivot low, "
            "with a qualifying oversold reading; awaiting confirmation."
        ),
        "Bullish Watch": f"UO < {_UO_WATCH_THRESHOLDS[indicator_key]}",
        "Bearish Confirmed": (
            "Qualifying bearish divergence + UO broke below its "
            "Classic Confirmation trigger within the 10-session window."
        ),
        "Bearish Divergence": (
            "Higher confirmed price high + lower UO pivot high, "
            "with a qualifying overbought reading; awaiting confirmation."
        ),
        "Bearish Watch": "UO > 70",
        "No Active Setup": "No active Watch, Divergence, or Confirmed setup.",
    }
    return descriptions[semantic_state]


# VWMA approved heatmap expressions are checked in their entirety, including
# strict versus inclusive boundaries and the relative-spread lag comparison.
_VWMA_PRICE_DISTANCE = {10: 0.25, 20: 0.50, 50: 1.00}


@lru_cache(maxsize=None)
def _approved_vwma_expressions(period: int) -> dict[str, str]:
    distance = _VWMA_PRICE_DISTANCE[period]
    price = f"(Close - VWMA_{period}) / ATR_14"
    slope = f"(VWMA_{period}_slope__linreg_14 / VWMA_{period}) * 100"
    separation = f"(VWMA_{period} - SMA_{period}) / ATR_14"
    spread = f"(VWMA_{period} / SMA_{period} - 1)"
    previous = f"lag(VWMA_{period} / SMA_{period} - 1, 1)"
    bull = f"{price} > {distance:.2f} and {slope} > 0.05"
    bear = f"{price} < -{distance:.2f} and {slope} < -0.05"
    return {
        "strong_buy": f"{bull} and {separation} >= 0.15 and {spread} > {previous}",
        "buy": f"{bull} and ({separation} < 0.15 or {spread} <= {previous})",
        "neutral": "",
        "sell": f"{bear} and ({separation} > -0.15 or {spread} >= {previous})",
        "strong_sell": f"{bear} and {separation} <= -0.15 and {spread} < {previous}",
    }


def get_vwma_rule_explanation(
    period: int,
    state: str,
    active_rules: Mapping[str, str],
    spread_atr: object = None,
    spread_direction: object = None,
) -> Optional[str]:
    """Describe upstream VWMA state; do not classify or manufacture a score."""
    if period not in _VWMA_PRICE_DISTANCE or state not in _HMA_STATES:
        return None
    if not isinstance(active_rules, Mapping):
        return None
    approved = _approved_vwma_expressions(period)
    for key in _HMA_STATES:
        actual = str(active_rules.get(key, "") or "")
        if key == "neutral":
            if actual.strip():
                return None
        elif _fingerprint(actual) != _fingerprint(approved[key]):
            return None

    bullish = f"Price is convincingly above a rising VWMA({period})"
    bearish = f"Price is meaningfully below a falling VWMA({period})"
    if state == "neutral":
        return ("Price position and VWMA direction do not jointly satisfy "
                "a qualified bullish or bearish state.")
    if state == "strong_buy":
        return (bullish + ", and VWMA is both meaningfully above SMA "
                "and strengthening relative to SMA.")
    if state == "strong_sell":
        return (bearish + ", and VWMA is both meaningfully below SMA "
                "and weakening further relative to SMA.")

    # Buy/Sell retain the upstream score. These facts only select which
    # *explanation* applies; they never create a classification.
    if isinstance(spread_atr, bool) or not isinstance(spread_atr, Real):
        return None
    import math
    if not math.isfinite(float(spread_atr)):
        return None
    if spread_direction not in ("Rising", "Falling", "Unchanged"):
        return None
    separation = float(spread_atr)
    if state == "buy":
        separation_fails = separation < 0.15
        direction_fails = spread_direction != "Rising"
        intro = bullish + ", but "
        separation_text = "VWMA is not meaningfully above SMA"
        direction_text = "VWMA is not strengthening relative to SMA"
    else:
        separation_fails = separation > -0.15
        direction_fails = spread_direction != "Falling"
        intro = bearish + ", but "
        separation_text = "VWMA is not meaningfully below SMA"
        direction_text = "VWMA is not weakening further relative to SMA"
    if not (separation_fails or direction_fails):
        return None  # Contradicts the upstream non-Strong score.
    if separation_fails and direction_fails:
        return intro + separation_text + " and " + direction_text + "."
    return intro + (separation_text if separation_fails else direction_text) + "."


def get_vwma_volume_context_interpretation(state: str, event: str) -> Optional[str]:
    """Interpret preclassified session participation, never infer an event."""
    if state not in _HMA_STATES:
        return None
    event_text = {
        "high_up": "an unusually high-volume price increase",
        "high_down": "an unusually high-volume price decline",
        "low_up": "a price increase on exceptionally light volume",
        "low_down": "a price decline on exceptionally light volume",
    }.get(event)
    if event_text is None:
        return None
    trend = ("bullish" if state in ("buy", "strong_buy") else
             "bearish" if state in ("sell", "strong_sell") else None)
    if trend is None:
        return (f"Today's session shows {event_text}, but no qualified directional "
                "VWMA Signal is present.")
    price_up = event.endswith("_up")
    agrees = (trend == "bullish") == price_up
    if event.startswith("low_"):
        return (f"The VWMA Signal is {trend}; today's session shows {event_text}. "
                "Light participation limits the strength of any current-session "
                "confirmation and does not change the Signal.")
    if agrees:
        return (f"The VWMA Signal is {trend}; today's {event_text} provides "
                "directionally aligned, unusually strong participation. "
                "The Signal itself is unchanged.")
    return (f"The VWMA Signal is {trend}, but today's {event_text} creates "
            "short-term tension with that classification. The Signal itself is unchanged.")


# BBP heatmap classification: reviewed independent five-state rule fingerprints.
_BBP_PERIODS = (10, 13, 21)


@lru_cache(maxsize=None)
def _approved_bbp_expressions(period: int) -> dict[str, str]:
    ema = f"EMA_{period}"
    bbp = f"BBP_{period}"
    up = f"{ema} - lag({ema}, 5) > 0.25 * ATR_14"
    down = f"lag({ema}, 5) - {ema} > 0.25 * ATR_14"
    return {
        "strong_buy": f"{up} and lag({bbp}, 2) <= 0 and {bbp} > 0 and rising_2bar({bbp}, 1)",
        "buy": f"{up} and {bbp} > 0 and (lag({bbp}, 2) > 0 or not_rising_2bar({bbp}, 1))",
        "neutral": "",
        "sell": f"{down} and {bbp} < 0 and (lag({bbp}, 2) < 0 or not_falling_2bar({bbp}, 1))",
        "strong_sell": f"{down} and lag({bbp}, 2) >= 0 and {bbp} < 0 and falling_2bar({bbp}, 1)",
    }


def get_bbp_rule_explanation(
    period: int,
    state: str,
    active_rules: Mapping[str, str],
    current_bbp: object = None,
    prior_bbp: object = None,
    two_sessions_ago_bbp: object = None,
) -> Optional[str]:
    """Describe the classified BBP state, never change or infer its score."""
    if period not in _BBP_PERIODS or state not in _HMA_STATES:
        return None
    if not isinstance(active_rules, Mapping):
        return None
    approved = _approved_bbp_expressions(period)
    for key in _HMA_STATES:
        actual = str(active_rules.get(key, "") or "")
        if key == "neutral":
            if actual.strip():
                return None
        elif _fingerprint(actual) != _fingerprint(approved[key]):
            return None

    if state == "strong_buy":
        return ("Buying pressure recently moved from the bearish to the bullish side "
                "of zero while the broader trend was already rising. "
                "Buying pressure is still improving.")
    if state == "strong_sell":
        return ("Selling pressure recently moved from the bullish to the bearish side "
                "of zero while the broader trend was already falling. "
                "Selling pressure is still deteriorating.")
    if state == "neutral":
        return ("Trend and pressure are not sufficiently aligned for a qualified "
                "bullish or bearish BBP state.")

    import math
    observations = (current_bbp, prior_bbp, two_sessions_ago_bbp)
    if any(isinstance(v, bool) or not isinstance(v, Real) or
           not math.isfinite(float(v)) for v in observations):
        return None
    current, previous, two_back = map(float, observations)
    if state == "buy":
        if current <= 0:
            return None
        old_side = two_back > 0
        # The approved rising_2bar(x,1) helper is current > previous.
        stalled = current <= previous
        intro = "Buyers have the pressure advantage, and that agrees with the broader rising trend. However, "
        old_text = "buying pressure was already positive two sessions earlier"
        stalled_text = "buying pressure is not strengthening today"
    else:
        if current >= 0:
            return None
        old_side = two_back < 0
        stalled = current >= previous
        intro = "Sellers have the pressure advantage, and that agrees with the broader falling trend. However, "
        old_text = "selling pressure was already negative two sessions earlier"
        stalled_text = "selling pressure is not worsening today"
    if not (old_side or stalled):
        return None  # Metadata contradicts upstream non-Confirmation classification.
    if old_side and stalled:
        return intro + old_text + " and " + stalled_text + "."
    return intro + (old_text if old_side else stalled_text) + "."


# Exact approved display language; values are presentation-only, not signals.
_BBP_BULLISH_CONTEXT = {
    ('None', 'None'): None,
    ('Bullish', 'None'): 'Reinforcement: Sellers still exert pressure below the EMA, but their influence is fading.',
    ('None', 'Bullish'): 'Supporting evidence: A confirmed lower price low showed improving Bear Power—selling pressure was less severe despite the lower low.',
    ('None', 'Bearish'): 'Counter-trend warning: The trend is bullish, but a confirmed higher price high showed weaker Bull Power. Buying pressure may be losing force.',
    ('Bearish', 'None'): "Tension: Broader bullish classification, but today's buyers are losing strength within a falling one-day EMA.",
    ('Bearish', 'Bearish'): "Multiple warnings: Weaker buying pressure appears in both today's Bearish Setup and the confirmed higher-price-high comparison.",
    ('Bullish', 'Bearish'): 'Mixed evidence: Sellers are weakening within the uptrend, but the confirmed higher price high showed weaker Bull Power. The Setup supports the trend; Divergence introduces caution.',
    ('Bearish', 'Bullish'): "Mixed evidence: Today's buyers are losing strength, but a confirmed lower price low showed improving Bear Power. Short-term pressure and swing-level evidence disagree.",
    ('Bullish', 'Bullish'): 'Reinforcement: Sellers are weakening within the rising trend, and a confirmed lower price low showed improving Bear Power. Both observations indicate fading selling pressure.',
}

_BBP_BEARISH_CONTEXT = {
    ('None', 'None'): None,
    ('Bearish', 'None'): 'Reinforcement: Buyers still exert some upward influence above the EMA, but that influence is fading.',
    ('None', 'Bearish'): 'Supporting evidence: A confirmed higher price high showed weaker Bull Power—buying pressure weakened despite the higher high.',
    ('None', 'Bullish'): "Counter-trend alert: The trend is bearish, but a confirmed lower price low showed improving Bear Power. Selling pressure may be losing force. Stronger than 'Counter-trend development'.",
    ('Bullish', 'None'): "Counter-trend development: The broader trend remains bearish, but today's sellers are losing strength within a rising one-day EMA.",
    ('Bullish', 'Bullish'): "Multiple counter-trend observations: Both today's Bullish Setup and the confirmed lower-price-low comparison suggest selling pressure may be weakening despite the bearish trend.",
    ('Bearish', 'Bullish'): 'Mixed evidence: Buyers are weakening within the downtrend, but a confirmed lower price low showed improving Bear Power. The Setup supports the trend; Divergence introduces caution.',
    ('Bullish', 'Bearish'): "Mixed evidence: Today's sellers are losing strength, but a confirmed higher price high showed weaker Bull Power. Short-term pressure and swing-level evidence disagree.",
    ('Bearish', 'Bearish'): 'Reinforcement: Buyers are weakening within the falling trend, and a confirmed higher price high showed weaker Bull Power. Both observations indicate fading buying pressure.',
}

_BBP_NEUTRAL_CONTEXT = {
    ('None', 'None'): None,
    ('Bullish', 'None'): 'Bullish context: Sellers are weakening within a rising EMA, even though the broader BBP conditions have not qualified.',
    ('Bearish', 'None'): 'Bearish context: Buyers are weakening within a falling EMA, even though the broader BBP conditions have not qualified.',
    ('None', 'Bullish'): 'Bullish pressure evidence: Price made a lower confirmed swing low, but Bear Power improved. Selling pressure may be losing force.',
    ('None', 'Bearish'): 'Bearish pressure evidence: Price made a higher confirmed swing high, but Bull Power weakened. Buying pressure may be losing force.',
    ('Bullish', 'Bullish'): 'Aligned bullish evidence: Sellers are weakening within a rising EMA, and a confirmed lower price low showed improving Bear Power. Both observations indicate fading selling pressure.',
    ('Bearish', 'Bearish'): 'Aligned bearish evidence: Buyers are weakening within a falling EMA, and a confirmed higher price high showed weaker Bull Power. Both observations indicate fading buying pressure.',
    ('Bullish', 'Bearish'): "Mixed evidence: Today's sellers are weakening within a rising EMA, but a confirmed higher price high showed weaker buying pressure. The two observations point in different directions.",
    ('Bearish', 'Bullish'): "Mixed evidence: Today's buyers are weakening within a falling EMA, but a confirmed lower price low showed improving Bear Power. The two observations point in different directions.",
}

def get_bbp_context_interpretation(
    state: str,
    setup: object,
    divergence: object,
) -> Optional[str]:
    """Return approved observation-specific context; no scoring or inference."""
    if state not in _HMA_STATES:
        return None
    if setup not in ("Bullish", "Bearish", "None"):
        return None
    if divergence not in ("Bullish", "Bearish", "None"):
        return None
    table = (
        _BBP_BULLISH_CONTEXT if state in ("buy", "strong_buy") else
        _BBP_BEARISH_CONTEXT if state in ("sell", "strong_sell") else
        _BBP_NEUTRAL_CONTEXT
    )
    return table.get((setup, divergence))


# Downside Exhaustion is separate from primary BBP; the only executable
# classified state is strong_buy, with neutral as a fallback.
@lru_cache(maxsize=None)
def _approved_bbp_exhaustion_expression(period: int) -> str:
    ema = f"EMA_{period}"
    bbp = f"BBP_{period}"
    return (
        f"lag({ema}, 5) - {ema} > 0.25 * ATR_14 "
        f"and {bbp} < 0 and falling_2bar({bbp}, 3) "
        f"and lag({bbp}, 3) - {bbp} > 0.50 * ATR_14"
    )


def get_bbp_exhaustion_hover_explanation(
    period: int,
    state: str,
    active_rules: Mapping[str, str],
    *,
    current_bbp: object,
    bbp_decline: object,
    bbp_atr_ratio: object,
    ema_decline: object,
    ema_atr_ratio: object,
    consecutive_decline: object,
) -> Optional[tuple[str, str]]:
    """Return Rule and formatted Context, never derive a new Signal.

    Fail closed if active executable rules drift, measurements are absent,
    score and measurements contradict, or continuity is unavailable.
    """
    import math
    if period not in (10, 13, 21) or state not in ("strong_buy", "neutral"):
        return None
    if not isinstance(active_rules, Mapping):
        return None
    if _fingerprint(str(active_rules.get("strong_buy", "") or "")) != _fingerprint(
        _approved_bbp_exhaustion_expression(period)
    ):
        return None
    if any(str(active_rules.get(k, "") or "").strip() for k in
           ("buy", "neutral", "sell", "strong_sell")):
        return None
    numeric = (current_bbp, bbp_decline, bbp_atr_ratio, ema_decline, ema_atr_ratio)
    if any(isinstance(v, bool) or not isinstance(v, Real) or
           not math.isfinite(float(v)) for v in numeric):
        return None
    if not isinstance(consecutive_decline, bool):
        return None
    bbp, bd, br, ed, er = map(float, numeric)
    # The transmitted ratios and moves must agree in sign; no reclassification.
    if (bd > 0) != (br > 0) and bd != 0 and br != 0:
        return None
    if (ed > 0) != (er > 0) and ed != 0 and er != 0:
        return None
    qualified = ed > 0 and er > 0.25 and bbp < 0 and consecutive_decline and bd > 0 and br > 0.50
    if state == "strong_buy" and not qualified:
        return None
    if state == "neutral" and qualified:
        return None

    rule = (
        "The stock is already in a meaningful decline, BBP is negative, "
        "selling pressure has worsened for 3 consecutive intervals, and the "
        "total deterioration is unusually large relative to recent volatility."
        if state == "strong_buy" else
        "The complete Downside Exhaustion pattern is not satisfied."
    )

    # Movement is factual. Qualification only refers to thresholds actually
    # defined by the Downside Exhaustion rule; no bullish thresholds invented.
    bbp_severe = bd > 0 and br > 0.50
    ema_bearish = ed > 0 and er > 0.25

    def movement(value: float, component: str) -> tuple[str, str]:
        days = 3 if component == "BBP" else 5
        if abs(value) < 0.005:
            return (f"{component} showed little net change over {days} trading days.", "flat")
        direction = "down" if value > 0 else "up"
        verb = (
            ("deteriorated" if value > 0 else "improved")
            if component == "BBP" else
            ("declined" if value > 0 else "rose")
        )
        observed = f"{component} {verb} by ${abs(value):.2f} over {days} trading days."
        if component == "BBP":
            qualification = (
                "Deterioration meets the severity threshold."
                if bbp_severe else
                "Deterioration does not meet the severity threshold."
                if value > 0 else
                "Improvement observed; reversal remains unconfirmed."
            )
        else:
            qualification = (
                "Bearish EMA trend requirement is met."
                if ema_bearish else
                "EMA decline does not meet the bearish trend requirement."
                if value > 0 else
                "EMA improvement observed; trend reversal remains unconfirmed."
            )
        return f"{observed} {qualification}", direction

    bbp_line, bbp_direction = movement(bd, "BBP")
    ema_line, ema_direction = movement(ed, "EMA")

    # State describes BBP pressure; Bottom-line integrates BBP with EMA.
    # Neither field restates the Signal/Rule when an observation scores None.
    if state == "strong_buy":
        bbp_state = (
            "Selling pressure intensified substantially for 3 consecutive intervals."
        )
        bottom = (
            "Broader bearish EMA trend remains established as selling pressure "
            "intensifies. This may increase rebound potential, but a reversal "
            "is unconfirmed."
        )
    elif bbp_severe and ema_bearish and bbp < 0 and not consecutive_decline:
        bbp_state = (
            "Selling pressure deteriorated substantially over 3 trading days, "
            "but not continuously. This may reflect a shift in selling intensity; "
            "the development is unconfirmed."
        )
        bottom = (
            "Broader bearish EMA trend remains established, but selling pressure "
            "has been uneven. This may warrant monitoring for stabilization or easing."
        )
    else:
        if bbp_direction == "up":
            if bbp < 0:
                bbp_state = (
                    "Although BBP remains negative, selling pressure may be easing. "
                    "This is unconfirmed."
                )
            elif bbp > 0:
                bbp_state = (
                    "BBP remains positive and pressure balance is improving; "
                    "buying-pressure improvement is observed, not reversal confirmation."
                )
            else:
                bbp_state = "BBP improved to zero; a sustained pressure shift remains unconfirmed."
        elif bbp_direction == "down":
            if bbp > 0:
                bbp_state = (
                    "Although BBP remains positive, buying pressure may be weakening. "
                    "This is unconfirmed."
                )
            elif bbp < 0:
                bbp_state = (
                    "Selling pressure deteriorated substantially."
                    if bbp_severe else
                    "Selling pressure deteriorated, but its magnitude is below the severity threshold."
                )
            else:
                bbp_state = "BBP deteriorated to zero; a sustained pressure shift remains unconfirmed."
        else:
            bbp_state = "BBP pressure balance showed little net change over 3 trading days."

        if ema_bearish:
            if bbp_direction == "up":
                bottom = (
                    "Broader bearish trend remains established, but pressure balance "
                    "is improving. This may be an early counter-trend development."
                )
            elif bbp_direction == "down":
                bottom = (
                    "Broader bearish EMA trend remains established alongside "
                    + ("substantial" if bbp_severe else "additional, less pronounced")
                    + " BBP deterioration. Downside pressure may remain elevated."
                )
            else:
                bottom = (
                    "Broader bearish EMA trend remains established while BBP is "
                    "approximately unchanged. Pressure has not yet shown a clear "
                    "counter-trend improvement."
                )
        elif ema_direction == "up":
            if bbp_direction == "down":
                bottom = (
                    "EMA baseline rose while BBP weakened. This may be an early "
                    "counter-trend pressure development."
                )
            elif bbp_direction == "up":
                bottom = (
                    "EMA baseline and BBP both improved. Their alignment may "
                    "indicate developing recovery, but a reversal is unconfirmed."
                )
            else:
                bottom = (
                    "EMA baseline rose while BBP showed little net change. "
                    "Broader improvement is not yet supported by a pressure shift."
                )
        elif ema_direction == "down":
            if bbp_direction == "up":
                bottom = (
                    "EMA decline is below the bearish trend threshold while BBP "
                    "improved. This may be early stabilization, not a confirmed reversal."
                )
            elif bbp_direction == "down":
                bottom = (
                    "EMA declined without meeting the bearish trend threshold, "
                    "while BBP deteriorated. Pressure may be weakening before a "
                    "qualified bearish baseline develops."
                )
            else:
                bottom = (
                    "EMA declined below the bearish trend threshold, while BBP "
                    "was approximately unchanged. Directional evidence is limited."
                )
        else:
            if bbp_direction == "up":
                bottom = (
                    "EMA baseline is approximately unchanged while BBP improved. "
                    "This may be an early pressure improvement worth monitoring."
                )
            elif bbp_direction == "down":
                bottom = (
                    "EMA baseline is approximately unchanged while BBP deteriorated. "
                    "This may be an early pressure warning worth monitoring."
                )
            else:
                bottom = "EMA and BBP showed little net movement; no clear directional shift is evident."

    # Plotly hover labels do not auto-wrap. Retain the approved indentation
    # on every continuation line while wrapping only plain prose (not HTML).
    from textwrap import wrap
    indent = "&nbsp;&nbsp;"

    def indented(text: str, *, width: int = 67) -> str:
        lines = wrap(text, width=width, break_long_words=False, break_on_hyphens=False)
        return "<br>".join(indent + line for line in lines)

    context = (
        "<br><b>Context Interpretation</b><br>"
        "<br><b>BBP — Selling Pressure</b><br>"
        + indented(bbp_line) + "<br>"
        + indented("State: " + bbp_state).replace(
            indent + "State:", indent + "<b>State:</b>", 1
        ) + "<br>"
        + "<br><b>EMA — Broader Trend</b><br>"
        + indented(ema_line) + "<br>"
        + indented("Bottom-line: " + bottom).replace(
            indent + "Bottom-line:", indent + "<b>Bottom-line:</b>", 1
        ) + "<br>"
    )
    return rule, context

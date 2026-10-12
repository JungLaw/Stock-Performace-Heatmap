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

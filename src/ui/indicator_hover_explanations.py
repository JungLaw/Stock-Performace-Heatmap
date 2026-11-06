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

# STOCH explanations are display-only; scoring remains the classifier's responsibility.
_STOCH_VARIANTS = frozenset({"5_3_3", "14_3_3", "21_5_5"})
_STOCH_SCORES = {"strong_buy": 2, "buy": 1, "neutral": 0, "sell": -1, "strong_sell": -2}


def _approved_stoch_rules(variant: str) -> dict[str, str]:
    k, d = f"STOCHK_{variant}", f"STOCHD_{variant}"
    return {
        "strong_buy": f"{k} < 20 and {k} > {d} and rising_2bar({k}, 1)",
        "buy": f"{k} < 20 and ({k} <= {d} or not_rising_2bar({k}, 1))",
        "neutral": f"20 <= {k} <= 80",
        "sell": f"{k} > 80 and ({k} >= {d} or not_falling_2bar({k}, 1))",
        "strong_sell": f"{k} > 80 and {k} < {d} and falling_2bar({k}, 1)",
    }


def get_stoch_rule_explanation(
    variant: str,
    state: str,
    score: int,
    active_rules: Mapping[str, str],
    k_value: object,
    d_value: object,
    previous_k: object = None,
) -> Optional[str]:
    """Explain the authoritative STOCH state; never infer or change classification.

    Missing prior K is not flat/falling. For non-strong states it leaves
    the reason unproven rather than asserting a particular failed condition.
    """
    import math

    if variant not in _STOCH_VARIANTS or state not in _STOCH_SCORES:
        return None
    if isinstance(score, bool) or score != _STOCH_SCORES[state]:
        return None
    if not isinstance(active_rules, Mapping):
        return None
    approved = _approved_stoch_rules(variant)
    if any(
        _fingerprint(str(active_rules.get(key, "") or "")) != _fingerprint(expr)
        for key, expr in approved.items()
    ):
        return None

    def finite(value: object) -> Optional[float]:
        if isinstance(value, bool):
            return None
        try:
            result = float(value)
        except (TypeError, ValueError, OverflowError):
            return None
        return result if math.isfinite(result) else None

    k, d, prior = finite(k_value), finite(d_value), finite(previous_k)
    if k is None or d is None:
        return None
    if state == "neutral":
        return "Trading in the middle portion of its recent range." if 20 <= k <= 80 else None

    if state in ("buy", "strong_buy"):
        if not k < 20:
            return None
        if state == "strong_buy":
            if prior is None or not (k > d and k > prior):
                return None
            return ("Near the bottom of its recent range ('oversold'), with %K above %D and rising. "
                    "This indicates improving bullish momentum and an early potential upward reversal.")
        base = "Trading in 'oversold' territory absent complete bullish momentum support."
        reasons = []
        if k <= d:
            reasons.append("%K is below %D" if k < d else "%K equals %D")
        if prior is not None and k <= prior:
            reasons.append("%K declined from the previous session" if k < prior else "%K was unchanged from the previous session")
        if not reasons:
            # An apparent Strong Buy cannot legitimately be explained as Buy.
            return None if prior is not None else base + " Prior-session %K is unavailable; the missing Strong qualification cannot be reconstructed."
        return base + " " + "; ".join(reasons) + "."

    if not k > 80:
        return None
    if state == "strong_sell":
        if prior is None or not (k < d and k < prior):
            return None
        return ("Near the top of its recent range ('overbought'), with %K below %D and falling. "
                "This indicates deteriorating momentum and an early potential downward reversal.")
    base = "Trading in 'overbought' territory absent complete bearish momentum validation."
    reasons = []
    if k >= d:
        reasons.append("%K is above %D" if k > d else "%K equals %D")
    if prior is not None and k >= prior:
        reasons.append("%K rose from the previous session" if k > prior else "%K was unchanged from the previous session")
    if not reasons:
        return None if prior is not None else base + " Prior-session %K is unavailable; the missing Strong qualification cannot be reconstructed."
    return base + " " + "; ".join(reasons) + "."


def get_stoch_context_interpretation(
    variant: str,
    state: str,
    score: int,
    active_rules: Mapping[str, str],
    k_value: object,
    d_value: object,
    previous_k: object = None,
    previous_d: object = None,
) -> Optional[tuple[str, str, str]]:
    """Read-only STOCH synthesis; never manufacture prior history or reclassify."""
    import math

    if get_stoch_rule_explanation(
        variant, state, score, active_rules, k_value, d_value, previous_k
    ) is None:
        return None

    def finite(value: object) -> Optional[float]:
        if isinstance(value, bool):
            return None
        try:
            result = float(value)
        except (TypeError, ValueError, OverflowError):
            return None
        return result if math.isfinite(result) else None

    k, d, pk, pd = map(finite, (k_value, d_value, previous_k, previous_d))
    if k is None or d is None:
        return None
    if k < 20:
        range_text = "Smoothed %K is in 'oversold' territory below 20, near the lower end of its recent trading range."
    elif k > 80:
        range_text = "Smoothed %K is in 'overbought' territory above 80, near the upper end of its recent trading range."
    else:
        range_text = "Smoothed %K is in the middle zone (20–80), not at either Stochastic extreme."

    spread = k - d
    position = "%K is above %D" if spread > 0 else ("%K is below %D" if spread < 0 else "%K equals %D")
    if pk is None or pd is None:
        development = position + ". Prior-session K/D evidence is unavailable; movement and fresh crossover cannot be established."
        bottom = "The current Stochastic relationship is known, but its latest momentum development is unverified."
        return range_text, development, bottom

    previous_spread = pk - pd
    k_move = "rose" if k > pk else ("fell" if k < pk else "was unchanged")
    d_move = "rose" if d > pd else ("fell" if d < pd else "was unchanged")
    spread_move = "widened upward" if spread > previous_spread else ("shifted downward" if spread < previous_spread else "was unchanged")
    crossover = "A fresh bullish K/D crossover occurred today" if previous_spread <= 0 < spread else (
        "A fresh bearish K/D crossover occurred today" if previous_spread >= 0 > spread else "No fresh K/D crossover occurred today"
    )
    development = f"{position}; %K {k_move}, %D {d_move}, and the K−D spread {spread_move}. {crossover}."

    # Compare direction of the change in the K-D spread with the contrarian signal,
    # without adding or changing any upstream classifier state.
    change = spread - previous_spread
    if change == 0:
        relation = "Relative K/D momentum is unchanged today"
    elif state in ("buy", "strong_buy"):
        relation = "Relative K/D momentum supports the bullish setup" if change > 0 else "Relative K/D momentum is in tension with the bullish setup"
    elif state in ("sell", "strong_sell"):
        relation = "Relative K/D momentum supports the bearish setup" if change < 0 else "Relative K/D momentum is in tension with the bearish setup"
    else:
        relation = "Bullish relative momentum is developing despite a Neutral classification" if change > 0 else "Bearish relative momentum is developing despite a Neutral classification"
    if (k > pk and spread < previous_spread) or (k < pk and spread > previous_spread):
        relation += "; K direction and relative spread development are mixed"
    bottom = relation + "."
    return range_text, development, bottom


# MACD explanations are display-only; the rule engine remains the sole classifier.
_MACD_ACTIVE_VARIANTS = frozenset({"8_17_5", "12_26_9", "20_50_10"})
_MACD_STATES = ("strong_buy", "buy", "neutral", "sell", "strong_sell")
_MACD_SCORES = {"strong_buy": 2, "buy": 1, "neutral": 0, "sell": -1, "strong_sell": -2}


def _approved_macd_rules(variant: str) -> dict[str, str]:
    """Audited rule shapes, compared to live expressions rather than evaluated."""
    line = f"MACD_{variant}_line"
    hist = f"MACD_{variant}_hist"
    return {
        "strong_buy": f"{line} < 0 and {hist} > 0 and rising_2bar({hist}, 2)",
        "buy": f"{line} < 0 and {hist} > 0 and not_rising_2bar({hist}, 2)",
        "neutral": f"({line} >= 0 and {hist} >= 0) or ({line} <= 0 and {hist} <= 0)",
        "sell": f"{line} > 0 and {hist} < 0 and not_falling_2bar({hist}, 2)",
        "strong_sell": f"{line} > 0 and {hist} < 0 and falling_2bar({hist}, 2)",
    }


def get_macd_rule_explanation(
    variant: str,
    state: str,
    score: int,
    active_rules: Mapping[str, str],
    macd_line: float,
    histogram: float,
    prior_histogram: Optional[float] = None,
    two_prior_histogram: Optional[float] = None,
) -> Optional[str]:
    """Explain an externally classified MACD state, or fail closed on drift.

    Historical inputs must represent actual successive observed sessions, not
    adjacent columns in a cropped heatmap. Missing history never means Neutral.
    """
    import math

    if variant not in _MACD_ACTIVE_VARIANTS or state not in _MACD_STATES:
        return None
    if isinstance(score, bool) or score != _MACD_SCORES[state]:
        return None
    if not isinstance(active_rules, Mapping):
        return None
    approved = _approved_macd_rules(variant)
    if any(
        _fingerprint(str(active_rules.get(key, "") or "")) != _fingerprint(approved[key])
        for key in _MACD_STATES
    ):
        return None

    def finite(value: object) -> Optional[float]:
        if isinstance(value, bool):
            return None
        try:
            number = float(value)
        except (TypeError, ValueError, OverflowError):
            return None
        return number if math.isfinite(number) else None

    line, hist = finite(macd_line), finite(histogram)
    if line is None or hist is None:
        return None
    prev = finite(prior_histogram)
    prev2 = finite(two_prior_histogram)
    rising = prev is not None and prev2 is not None and hist > prev > prev2
    falling = prev is not None and prev2 is not None and hist < prev < prev2

    if state == "strong_buy":
        if not (line < 0 and hist > 0 and rising):
            return None
        return ("MACD trend backdrop is negative, but histogram is positive and has "
                "increased for 2 consecutive sessions. This qualifies as a Strong Buy reversal setup.")
    if state == "buy":
        if not (line < 0 and hist > 0 and not rising):
            return None
        if prev is None or prev2 is None:
            return ("MACD trend backdrop is negative and histogram is positive. "
                    "Available history cannot establish 2 consecutive increases; "
                    "the authoritative Signal is Buy, not Strong Buy.")
        return ("MACD trend backdrop is negative and histogram is positive, but "
                "2 consecutive histogram increases are absent. Bullish counter-trend "
                "momentum is present without Strong Buy qualification.")
    if state == "neutral":
        if not ((line >= 0 and hist >= 0) or (line <= 0 and hist <= 0)):
            return None
        if line == 0 or hist == 0:
            return ("MACD line or histogram is exactly zero; neither qualifying "
                    "counter-trend reversal condition applies. Signal remains Neutral.")
        direction = "positive" if line > 0 else "negative"
        return (f"MACD line and histogram are both {direction}. Broader MACD backdrop "
                "and relative momentum agree, so no counter-trend reversal signal qualifies.")
    if state == "sell":
        if not (line > 0 and hist < 0 and not falling):
            return None
        if prev is None or prev2 is None:
            return ("MACD trend backdrop is positive and histogram is negative. "
                    "Available history cannot establish 2 consecutive declines; "
                    "the authoritative Signal is Sell, not Strong Sell.")
        return ("MACD trend backdrop is positive and histogram is negative, but "
                "2 consecutive histogram declines are absent. Bearish counter-trend "
                "momentum is present without Strong Sell qualification.")
    if not (line > 0 and hist < 0 and falling):
        return None
    return ("MACD trend backdrop is positive, but histogram is negative and has "
            "declined for 2 consecutive sessions. This qualifies as a Strong Sell reversal setup.")


def get_macd_context_interpretation(
    variant: str,
    state: str,
    score: int,
    active_rules: Mapping[str, str],
    macd_line: object,
    signal_line: object,
    histogram: object,
    prior_histogram: object = None,
    two_prior_histogram: object = None,
    prior_macd_line: object = None,
    prior_signal_line: object = None,
) -> Optional[tuple[str, str, str]]:
    """Return (backdrop, current development, bottom-line), never a Signal.

    Evidence is from full chronological history. Missing history is not a flat
    or unchanged observation. Adapter owns labels, HTML and numeric formatting.
    """
    import math

    if get_macd_rule_explanation(
        variant, state, score, active_rules, macd_line, histogram,
        prior_histogram, two_prior_histogram,
    ) is None:
        return None

    def finite(value: object) -> Optional[float]:
        if isinstance(value, bool):
            return None
        try:
            number = float(value)
        except (TypeError, ValueError, OverflowError):
            return None
        return number if math.isfinite(number) else None

    line = finite(macd_line)
    signal = finite(signal_line)
    hist = finite(histogram)
    prior_h = finite(prior_histogram)
    prior2_h = finite(two_prior_histogram)
    prior_l = finite(prior_macd_line)
    prior_s = finite(prior_signal_line)

    if line is None or signal is None or hist is None:
        return None

    # Compare full precision, allowing only floating-point subtraction noise.
    if not math.isclose(
        hist, line - signal, rel_tol=1e-9, abs_tol=1e-10
    ):
        return None

    if prior_h is not None and prior_l is not None and prior_s is not None:
        if not math.isclose(
            prior_h, prior_l - prior_s, rel_tol=1e-9, abs_tol=1e-10
        ):
            return None

    if line > 0:
        backdrop = (
            "MACD line is above zero: faster EMA remains above slower EMA. "
            "Broader MACD backdrop is positive, not proof price rose today."
        )
    elif line < 0:
        backdrop = (
            "MACD line is below zero: faster EMA remains below slower EMA. "
            "Broader MACD backdrop is negative, not proof price fell today."
        )
    else:
        backdrop = (
            "MACD line is exactly zero: faster and slower EMA are equal. "
            "Broader MACD direction is not established by this reading."
        )

    if hist > 0:
        position = "MACD line remains above Signal Line"
    elif hist < 0:
        position = "MACD line remains below Signal Line"
    else:
        position = "MACD line and Signal Line are equal"

    if prior_h is None:
        development = (
            position + "; prior-session momentum change is unavailable."
        )
        change = None
    else:
        change = hist - prior_h

        if change > 0:
            movement = "histogram rose"
        elif change < 0:
            movement = "histogram fell"
        else:
            movement = "histogram was unchanged"

        development = (
            position + "; " + movement + " since prior session."
        )

        if prior_l is not None and prior_s is not None:
            delta_line = line - prior_l
            delta_signal = signal - prior_s

            if not math.isclose(
                change, delta_line - delta_signal,
                rel_tol=1e-9, abs_tol=1e-10
            ):
                return None

    if change is None:
        bottom = (
            "Current MACD positioning is visible, but its latest improvement "
            "or deterioration cannot be assessed without prior-session evidence."
        )
    elif hist == 0:
        bottom = (
            "Momentum gap is zero; MACD and Signal Line are level. "
            "No counter-trend reversal state qualifies from this reading."
        )
    elif line == 0:
        bottom = (
            "Broader MACD backdrop is at zero. Histogram positioning shows "
            "relative momentum, but does not establish a broader EMA trend direction."
        )
    elif change == 0:
        bottom = (
            "Relative momentum advantage is unchanged today. "
            "Current position alone does not establish a fresh reversal."
        )
    elif line < 0 and hist > 0:
        bottom = (
            "Bullish counter-trend reversal momentum is strengthening even though "
            "broader MACD trend has not turned positive."
            if change > 0 else
            "Bullish counter-trend advantage is still present, but weakened today. "
            "Positive histogram does not mean momentum improved today."
        )
    elif line > 0 and hist < 0:
        bottom = (
            "Bearish counter-trend momentum is intensifying even while "
            "broader MACD backdrop remains positive."
            if change < 0 else
            "Bearish counter-trend pressure persists, but is easing. "
            "Broader MACD backdrop remains positive."
        )
    elif hist > 0:
        bottom = (
            "Bullish relative momentum is strengthening within a positive MACD "
            "backdrop. Neutral means no counter-trend setup, not weak momentum."
            if change > 0 else
            "Bullish relative momentum remains present, but its advantage is "
            "shrinking. Neutral does not mean momentum has disappeared."
        )
    else:
        bottom = (
            "Bearish relative momentum is worsening within a negative MACD "
            "backdrop. Neutral means no counter-trend setup, not weak momentum."
            if change < 0 else
            "Negative momentum gap is narrowing while MACD backdrop remains "
            "bearish. Selling pressure may be easing without a qualifying "
            "bullish reversal."
        )

    return backdrop, development, bottom


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


# CCI semantic explanations are display-only. Classification, divergence and
# zero-line events remain owned by the rule engine and technical.py.
_CCI_PERIODS = frozenset({10, 14, 20})
_CCI_STATES = ("strong_buy", "buy", "neutral", "sell", "strong_sell")
_CCI_SCORES = {"strong_buy": 2, "buy": 1, "neutral": 0,
               "sell": -1, "strong_sell": -2}
_CCI_RULE_TEXT = {
    "strong_buy": "CCI is severely depressed relative to its recent norm.",
    "buy": "CCI is materially depressed, but not at the most extreme project threshold.",
    "neutral": "CCI is not far enough from its recent norm to trigger the project's contrarian extreme states.",
    "sell": "CCI is materially overextended relative to its recent norm.",
    "strong_sell": "CCI is severely overextended relative to its recent norm.",
}
_CCI_PIVOT_FIELDS = (
    "cci_divergence_prior_pivot_date", "cci_divergence_current_pivot_date",
    "cci_divergence_prior_price", "cci_divergence_current_price",
    "cci_divergence_prior_cci", "cci_divergence_current_cci",
    "cci_divergence_price_basis",
)


def _approved_cci_rules(period: int) -> dict[str, str]:
    col = f"CCI_{period}"
    return {
        "strong_buy": f"{col} <= -200",
        "buy": f"{col} <= -150 and {col} > -200",
        "neutral": "",
        "sell": f"{col} > 150 and {col} < 200",
        "strong_sell": f"{col} >= 200",
    }


def _cci_numeric(value: object) -> Optional[float]:
    import math
    if isinstance(value, bool):
        return None
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError):
        return None
    return result if math.isfinite(result) else None


def _cci_qualifies(state: str, value: float) -> bool:
    if state == "strong_buy":
        return value <= -200
    if state == "buy":
        return -200 < value <= -150
    if state == "neutral":
        return -150 < value <= 150
    if state == "sell":
        return 150 < value < 200
    if state == "strong_sell":
        return value >= 200
    return False


def get_cci_rule_explanation(
    period: int,
    state: str,
    score: int,
    active_rules: Mapping[str, str],
    cci_value: object,
) -> Optional[str]:
    """Describe the supplied CCI classification only when its evidence agrees.

    Fingerprint all five live expressions, including empty Neutral fallback;
    never infer a state, mutate a score, or interpret an unapproved rulebook.
    """
    if period not in _CCI_PERIODS or state not in _CCI_SCORES:
        return None
    if isinstance(score, bool) or score != _CCI_SCORES[state]:
        return None
    if not isinstance(active_rules, Mapping):
        return None
    approved = _approved_cci_rules(period)
    for key in _CCI_STATES:
        actual = str(active_rules.get(key, "") or "")
        if key == "neutral":
            if actual.strip():
                return None
        elif _fingerprint(actual) != _fingerprint(approved[key]):
            return None
    current = _cci_numeric(cci_value)
    if current is None or not _cci_qualifies(state, current):
        return None
    return _CCI_RULE_TEXT[state]


def _cci_event_evidence_valid(direction: str, evidence: Mapping[str, object]) -> bool:
    """Check transported pivot evidence; do not detect/recompute divergence."""
    from datetime import date
    if not isinstance(evidence, Mapping):
        return False
    if any(field not in evidence for field in _CCI_PIVOT_FIELDS):
        return False
    try:
        dates = [date.fromisoformat(str(evidence[field])) for field in
                 _CCI_PIVOT_FIELDS[:2]]
    except (TypeError, ValueError, OverflowError):
        return False
    if dates[0] >= dates[1]:
        return False
    numbers = [_cci_numeric(evidence[field]) for field in _CCI_PIVOT_FIELDS[2:6]]
    if any(value is None for value in numbers):
        return False
    p0, p1, c0, c1 = numbers
    basis = evidence.get("cci_divergence_price_basis")
    if direction == "Bullish":
        return basis == "lows" and p1 < p0 and c1 > c0
    return basis == "highs" and p1 > p0 and c1 < c0


def get_cci_context_interpretation(
    period: int,
    state: str,
    score: int,
    active_rules: Mapping[str, str],
    cci_value: object,
    previous_cci: object,
    divergence: object,
    zero_line: object,
    divergence_evidence: Mapping[str, object] | None = None,
) -> Optional[tuple[str, str, str]]:
    """Return (Relative Position, Current Development, Bottom-line).

    The caller supplies upstream-classified state and events. Missing history
    is not Flat, Neutral or a verified absence of an event. A failed guard
    returns None so the adapter can retain its existing factual hover.
    """
    if get_cci_rule_explanation(period, state, score, active_rules, cci_value) is None:
        return None
    if divergence not in (None, "None", "Bullish", "Bearish"):
        return None
    if zero_line not in (None, "None", "Uptrend Bias", "Downtrend Bias"):
        return None
    current, prior = _cci_numeric(cci_value), _cci_numeric(previous_cci)
    if zero_line in ("Uptrend Bias", "Downtrend Bias"):
        if prior is None:
            return None
        if zero_line == "Uptrend Bias" and not (prior <= 0 < current):
            return None
        if zero_line == "Downtrend Bias" and not (prior >= 0 > current):
            return None
    elif prior is not None and zero_line == "None":
        if prior <= 0 < current or prior >= 0 > current:
            return None
    elif prior is None and zero_line == "None":
        # A reported evaluated absence requires previous-session CCI.
        return None
    if divergence in ("Bullish", "Bearish"):
        if not _cci_event_evidence_valid(divergence, divergence_evidence):
            return None
    elif isinstance(divergence_evidence, Mapping) and any(
        field in divergence_evidence for field in _CCI_PIVOT_FIELDS
    ):
        return None

    if state == "strong_buy":
        level = "CCI is far below zero, in the project's most extreme downside range (CCI <= -200)."
    elif state == "buy":
        level = "CCI is unusually low, but has not reached the Strong Buy range (-200 < CCI <= -150)."
    elif state == "neutral":
        side = "above" if current > 0 else "below" if current < 0 else "at"
        level = f"CCI is {side} zero but remains within the project's Neutral range (-150 < CCI <= +150)."
    elif state == "sell":
        level = "CCI is unusually high, but has not reached the Strong Sell range (+150 < CCI < +200)."
    else:
        level = "CCI is far above zero, in the project's most extreme upside range (CCI >= +200)."

    if prior is None:
        movement = "Previous-session CCI is unavailable; today's CCI movement cannot be verified."
        move_sign = 0
    elif current > prior:
        move_sign = 1
        movement = (
            "CCI rose toward zero today; the negative reading is easing."
            if current < 0 else
            "CCI rose above zero today."
            if prior <= 0 else
            "CCI rose farther above zero today; upward movement is strengthening."
        )
    elif current < prior:
        move_sign = -1
        movement = (
            "CCI fell toward zero today; the positive reading is easing."
            if current > 0 else
            "CCI fell below zero today."
            if prior >= 0 else
            "CCI fell farther below zero today; the negative reading is deepening."
        )
    else:
        move_sign = 0
        movement = "CCI was unchanged from the preceding trading session."

    event_text = {
        ("Bullish", "Uptrend Bias"):
            "A bullish divergence was confirmed using earlier price lows, and CCI crossed above zero today. Both events provide bullish evidence.",
        ("Bullish", "Downtrend Bias"):
            "A bullish divergence was confirmed using earlier price lows, but CCI crossed below zero today. The events point in opposite directions.",
        ("Bearish", "Uptrend Bias"):
            "A bearish divergence was confirmed using earlier price highs, but CCI crossed above zero today. The events point in opposite directions.",
        ("Bearish", "Downtrend Bias"):
            "A bearish divergence was confirmed using earlier price highs, and CCI crossed below zero today. Both events provide bearish evidence.",
        ("Bullish", "None"):
            "A bullish price/CCI divergence was confirmed from earlier price lows; no fresh zero-line crossover occurred.",
        ("Bearish", "None"):
            "A bearish price/CCI divergence was confirmed from earlier price highs; no fresh zero-line crossover occurred.",
        ("None", "Uptrend Bias"):
            "CCI crossed above zero today; no new confirmed divergence occurred.",
        ("None", "Downtrend Bias"):
            "CCI crossed below zero today; no new confirmed divergence occurred.",
        ("None", "None"):
            "No new confirmed divergence or zero-line crossover occurred today.",
    }
    detail = event_text.get((divergence, zero_line))
    if detail is None:
        # Do not turn missing/unevaluable event context into an asserted None.
        detail_parts = []
        if divergence in ("Bullish", "Bearish"):
            detail_parts.append(f"A {divergence.lower()} divergence was confirmed from earlier price pivots.")
        elif divergence == "None":
            detail_parts.append("No new divergence was confirmed today.")
        if zero_line == "Uptrend Bias":
            detail_parts.append("CCI crossed above zero today.")
        elif zero_line == "Downtrend Bias":
            detail_parts.append("CCI crossed below zero today.")
        elif zero_line == "None":
            detail_parts.append("No fresh zero-line crossover occurred.")
        detail = " ".join(detail_parts)
    development = " ".join(part for part in (movement, detail) if part)

    # Preserve divergent readings. A two-event agreement does not override the
    # contrarian classifier, and an event confirmed today refers to past pivots.
    if state in ("strong_buy", "buy"):
        premise = "CCI is unusually low, suggesting possible rebound potential."
        if divergence == "Bearish" and zero_line == "Downtrend Bias":
            conclusion = "However, the newly confirmed divergence and zero-line crossover are bearish. An upward reversal is not established."
        elif divergence == "Bullish" and zero_line == "Downtrend Bias":
            conclusion = "Bullish divergence and today's downward zero-line crossing conflict; a rebound has not been confirmed."
        elif divergence == "Bullish":
            conclusion = "Bullish divergence provides possible rebound evidence, but an upward reversal has not been confirmed."
        elif divergence == "Bearish":
            conclusion = "Bearish divergence conflicts with the rebound setup; a reversal has not been confirmed."
        elif zero_line == "Downtrend Bias":
            conclusion = "The fresh downward zero-line crossing points against a rebound; an upward reversal has not been confirmed."
        elif move_sign > 0:
            conclusion = "CCI is rising toward recovery, but this alone does not confirm a reversal."
        elif move_sign < 0:
            conclusion = "CCI is still falling, so the downside move may not yet be finished."
        else:
            conclusion = "No verified fresh momentum improvement establishes a rebound."
    elif state in ("strong_sell", "sell"):
        premise = "CCI is unusually high, raising possible pullback risk."
        if divergence == "Bullish" and zero_line == "Uptrend Bias":
            conclusion = "Both secondary events are bullish, conflicting with the contrarian Sell warning; a pullback has not been confirmed."
        elif divergence == "Bearish" and zero_line == "Uptrend Bias":
            conclusion = "Bearish divergence and today's upward zero-line crossing conflict; a pullback has not been confirmed."
        elif divergence == "Bearish":
            conclusion = "Bearish divergence provides possible pullback evidence, but a decline has not been confirmed."
        elif divergence == "Bullish":
            conclusion = "Bullish divergence conflicts with the pullback warning; a decline has not been confirmed."
        elif zero_line == "Uptrend Bias":
            conclusion = "The fresh upward zero-line crossing points against a pullback; a decline has not been confirmed."
        elif move_sign < 0:
            conclusion = "CCI is easing from its high reading, but this alone does not confirm a decline."
        elif move_sign > 0:
            conclusion = "CCI is still rising, so the upward move may not yet be finished."
        else:
            conclusion = "No verified fresh momentum change establishes a decline."
    else:
        premise = "The primary CCI Signal remains Neutral."
        if divergence == "Bullish" and zero_line == "Uptrend Bias":
            conclusion = "Bullish divergence and the upward zero-line crossover provide positive secondary evidence worth monitoring."
        elif divergence == "Bearish" and zero_line == "Downtrend Bias":
            conclusion = "Bearish divergence and the downward zero-line crossover provide negative secondary evidence worth monitoring."
        elif (divergence == "Bullish" and zero_line == "Downtrend Bias") or (
            divergence == "Bearish" and zero_line == "Uptrend Bias"
        ):
            conclusion = "The divergence and zero-line crossover conflict; no consistent new direction is established."
        elif divergence == "Bullish":
            conclusion = "Bullish divergence provides positive secondary evidence without changing the Neutral classification."
        elif divergence == "Bearish":
            conclusion = "Bearish divergence provides negative secondary evidence without changing the Neutral classification."
        elif zero_line == "Uptrend Bias":
            conclusion = "The upward zero-line crossing is positive secondary evidence despite the Neutral classification."
        elif zero_line == "Downtrend Bias":
            conclusion = "The downward zero-line crossing is negative secondary evidence despite the Neutral classification."
        elif move_sign > 0:
            conclusion = "CCI is rising, but no fresh divergence or crossover establishes a qualified directional Signal."
        elif move_sign < 0:
            conclusion = "CCI is falling, but no fresh divergence or crossover establishes a qualified directional Signal."
        else:
            conclusion = "No fresh directional event is verified from the available evidence."
    return level, development, premise + " " + conclusion

# CMF Dynamic Rules: display-only, score-checked, guarded by all five live
# rulebook expressions. The classifier remains the sole owner of scores.
_CMF_STRONG_CUTOFFS = {10: 0.25, 21: 0.20, 30: 0.175, 50: 0.15}
_CMF_STATES = ("strong_buy", "buy", "neutral", "sell", "strong_sell")
_CMF_SCORES = {
    "strong_buy": 2, "buy": 1, "neutral": 0, "sell": -1, "strong_sell": -2,
}


@lru_cache(maxsize=None)
def _approved_cmf_rules(period: int) -> dict[str, str]:
    """Audited expressions used only as semantic fingerprints, not for scoring."""
    c = f"CMF_{period}"
    cutoff = str(_CMF_STRONG_CUTOFFS[period])
    return {
        "strong_buy": f"{c} > {cutoff} and rising_2bar({c})",
        "buy": f"{c} > 0.10 and ({c} <= {cutoff} or not_rising_2bar({c}))",
        "neutral": f"-0.10 <= {c} <= 0.10",
        "sell": f"{c} < -0.10 and ({c} >= -{cutoff} or not_falling_2bar({c}))",
        "strong_sell": f"{c} < -{cutoff} and falling_2bar({c})",
    }


def _cmf_finite(value: object) -> Optional[float]:
    """Accept finite raw observations; missing and booleans cannot prove CMF."""
    from math import isfinite
    if isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError):
        return None
    return number if isfinite(number) else None


def _cmf_display(raw_value: float) -> str:
    """CMF is stored fractionally and displayed in signed points (x100)."""
    displayed = raw_value * 100.0
    return (f"{displayed:+.1f}").replace("-", "−")


def get_cmf_rule_explanation(
    period: int,
    state: str,
    score: int,
    active_rules: Mapping[str, str],
    current_cmf: object,
    prior_cmf: object = None,
    prior2_cmf: object = None,
) -> Optional[str]:
    """Explain only a valid, source-qualified CMF classification.

    An absent predecessor is NOT proof that a rise/fall failed. Strong states
    require both finite predecessors; current-only Buy/Sell may still qualify.
    All comparisons use raw numbers, never the rounded hover values.
    """
    if period not in _CMF_STRONG_CUTOFFS or state not in _CMF_SCORES:
        return None
    if isinstance(score, bool) or score != _CMF_SCORES[state]:
        return None
    if not isinstance(active_rules, Mapping):
        return None
    expected = _approved_cmf_rules(period)
    if any(
        _fingerprint(str(active_rules.get(key, "") or "")) != _fingerprint(expected[key])
        for key in _CMF_STATES
    ):
        return None

    c = _cmf_finite(current_cmf)
    if c is None:
        return None  # Missing is never a verified Neutral classification.
    p = _cmf_finite(prior_cmf)
    q = _cmf_finite(prior2_cmf)
    history_ok = p is not None and q is not None
    rising_twice = history_ok and c > p > q
    falling_twice = history_ok and c < p < q
    strong = _CMF_STRONG_CUTOFFS[period]

    # Only use the active classifier's state; reject contradictory supplied
    # score/evidence rather than silently reclassifying or inventing history.
    qualified = (
        "strong_buy" if c > strong and rising_twice else
        "buy" if c > 0.10 else
        "strong_sell" if c < -strong and falling_twice else
        "sell" if c < -0.10 else
        "neutral"
    )
    if qualified != state:
        return None

    cutoff = f"{strong * 100:g}"
    current = _cmf_display(c)
    if state == "strong_buy":
        return (
            f"CMF is above the +{cutoff} Strong Buy cutoff, and rose from "
            f"{_cmf_display(q)} to {_cmf_display(p)} to {current} across 2 consecutive days. "
            "Both Strong Buy conditions are met, indicating substantial and strengthening accumulation pressure."
        )
    if state == "strong_sell":
        return (
            f"CMF is below the −{cutoff} Strong Sell cutoff, and fell from "
            f"{_cmf_display(q)} to {_cmf_display(p)} to {current} across 2 consecutive days, "
            "indicating substantial and strengthening distribution pressure."
        )
    if state == "neutral":
        if c > 0:
            return ("CMF is within the Neutral range. The reading is positive but does not "
                    "establish enough accumulation pressure to qualify for Buy.")
        if c < 0:
            return ("CMF is within the Neutral range. The reading is negative but does not "
                    "establish enough distribution pressure to qualify for Sell.")
        return "CMF is within the Neutral range. Neither accumulation nor distribution pressure qualifies."
    if state == "buy":
        if c > strong and history_ok:
            return (
                f"CMF is above the +10 accumulation cutoff. Although it exceeds +{cutoff}, "
                "it did not rise across both recent moves "
                f"({_cmf_display(q)} → {_cmf_display(p)} → {current})."
            )
        if c > strong:
            return (f"CMF is above +10 and exceeds +{cutoff}, but 2-move history "
                    "is unavailable.")
        return (f"CMF is above the +10 accumulation cutoff but not above the "
                f"+{cutoff} Strong Buy cutoff.")
    # Sell: preserve the user's exact short sentence for the agreed easing
    # fixture; never describe easing when history shows otherwise.
    if c >= -strong:
        if history_ok and c > p > q:
            return "CMF is below the −10.0 distribution cutoff but pressure has eased over the last 2 days."
        return (f"CMF is below the −10.0 distribution cutoff but not below "
                f"the −{cutoff} Strong Sell cutoff.")
    if history_ok:
        return (
            f"CMF is below the −10.0 distribution cutoff. Although it is below −{cutoff}, "
            "it did not fall across both recent moves "
            f"({_cmf_display(q)} → {_cmf_display(p)} → {current})."
        )
    return (f"CMF is below −10 and below −{cutoff}, but 2-move history "
            "is unavailable.")


def get_cmf_easing_marker(
    period: int,
    state: str,
    score: int,
    active_rules: Mapping[str, str],
    current_cmf: object,
    prior_cmf: object,
    prior2_cmf: object,
    prior3_cmf: object = None,
    prior4_cmf: object = None,
) -> str:
    """Display-only CMF suffix; empty on missing or inconsistent evidence.

    Buy/Sell: 2 strict moves against qualified pressure (easing).
    Neutral: 4 strict CMF moves (directional development, not a signal).
    Only the current bar must be Neutral; the prior sequence may cross a
    threshold. All comparisons use unrounded, full-history observations.
    """
    if state not in ("buy", "sell", "neutral"):
        return ""
    if get_cmf_rule_explanation(
        period, state, score, active_rules,
        current_cmf, prior_cmf, prior2_cmf,
    ) is None:
        return ""
    c = _cmf_finite(current_cmf)
    p = _cmf_finite(prior_cmf)
    q = _cmf_finite(prior2_cmf)
    if c is None or p is None or q is None:
        return ""
    if state == "neutral":
        r = _cmf_finite(prior3_cmf)
        t = _cmf_finite(prior4_cmf)
        if r is None or t is None:
            return ""
        if c > p > q > r > t:
            return "↗"
        if c < p < q < r < t:
            return "↘"
        return ""
    if state == "sell" and c > p > q:
        return "↗"
    if state == "buy" and c < p < q:
        return "↘"
    return ""


# CMF Context Interpretation: display-only interpretation of the current
# qualified pressure and verified one-session canonical price direction.
_CMF_DISTRIBUTION_TEXT = (
    "Over the measurement period, trading volume associated with closes near daily lows "
    "had a greater influence on CMF than volume associated with closes near daily highs, "
    "indicating distribution pressure."
)
_CMF_ACCUMULATION_TEXT = (
    "Over the measurement period, trading volume associated with closes near daily highs "
    "had a greater positive influence on CMF than volume associated with closes near daily lows, "
    "indicating accumulation pressure."
)
_CMF_NEUTRAL_TEXT = (
    "CMF remains within the project's Neutral range (−10.0 to +10.0), so neither "
    "accumulation nor distribution pressure qualifies under the current rules."
)


def get_cmf_context_interpretation(
    period: int,
    state: str,
    score: int,
    active_rules: Mapping[str, str],
    current_cmf: object,
    prior_cmf: object = None,
    prior2_cmf: object = None,
    price_current: object = None,
    price_prior: object = None,
    price_basis: object = None,
) -> Optional[tuple[str, str]]:
    """Return (CMF Interpretation, Bottom-line) only for verified CMF.

    This deliberately does NOT claim a common price/CMF time horizon or
    infer same-day buy/sell volume. No price comparison without aligned,
    positive canonical-price evidence transported by the calculator.
    """
    if get_cmf_rule_explanation(
        period, state, score, active_rules,
        current_cmf, prior_cmf, prior2_cmf,
    ) is None:
        return None
    c = _cmf_finite(current_cmf)
    if c is None:
        return None

    if c > 0.10:
        cmf_interpretation = _CMF_ACCUMULATION_TEXT
        pressure = "accumulation"
    elif c < -0.10:
        cmf_interpretation = _CMF_DISTRIBUTION_TEXT
        pressure = "distribution"
    else:
        cmf_interpretation = _CMF_NEUTRAL_TEXT
        pressure = "neutral"

    pc = _cmf_finite(price_current)
    pp = _cmf_finite(price_prior)
    if (
        price_basis not in ("Adj Close", "Close")
        or pc is None or pp is None or pc <= 0 or pp <= 0
    ):
        return (
            cmf_interpretation,
            "No verified same-date price comparison is available; the CMF reading alone "
            "does not establish whether today's price movement agreed or disagreed.",
        )

    # Combine today's price direction with verified CMF development.
    # The CMF Interpretation already explains *why* the sign is negative or
    # positive; don't repeat that explanation or append generic disclaimers.
    p = _cmf_finite(prior_cmf)
    q = _cmf_finite(prior2_cmf)
    rising_twice = p is not None and q is not None and c > p > q
    falling_twice = p is not None and q is not None and c < p < q

    if pc == pp:
        bottom = "Price was unchanged today; CMF reflects the broader measurement period."
    else:
        price_move = "Price rose today" if pc > pp else "Price fell today"
        if pressure == "distribution":
            if rising_twice:
                bottom = (
                    f"{price_move} while CMF became less negative over the last 2 days"
                    "—distribution pressure is easing."
                )
            elif falling_twice:
                bottom = (
                    f"{price_move} while CMF became more negative over the last 2 days"
                    "—distribution pressure is intensifying."
                )
            else:
                bottom = (
                    f"{price_move}, but CMF still indicates distribution pressure."
                    if pc > pp else
                    f"{price_move} alongside distribution pressure."
                )
        elif pressure == "accumulation":
            if rising_twice:
                bottom = (
                    f"{price_move} while CMF increased over the last 2 days"
                    "—accumulation pressure is strengthening."
                )
            elif falling_twice:
                bottom = (
                    f"{price_move} while CMF declined over the last 2 days"
                    "—accumulation pressure is easing."
                )
            else:
                bottom = (
                    f"{price_move} alongside accumulation pressure."
                    if pc > pp else
                    f"{price_move} despite accumulation pressure."
                )
        else:
            bottom = f"{price_move} while CMF remains Neutral."
    return cmf_interpretation, bottom


# Bollinger %B IVE Stage 6 — guarded, display-only explanatory content.
# The classifier owns the five-state Signal. These functions never rescore.
_BB_PCT_B_STATES = ("strong_buy", "buy", "neutral", "sell", "strong_sell")
_BB_PCT_B_SCORES = {
    "strong_buy": 2, "buy": 1, "neutral": 0, "sell": -1, "strong_sell": -2,
}
_BB_PCT_B_BOUNDARIES = {
    "10_1.5": ("-0.20", "1.20"),
    "20_2.0": ("-0.10", "1.10"),
    "50_2.5": ("0.00", "1.00"),
}
_BB_PCT_B_BREACH_STATUSES = frozenset({
    "Fresh Lower Breach", "Continuing Lower Breach",
    "Lower-Band Re-entry", "Fresh Upper Breach",
    "Continuing Upper Breach", "Upper-Band Re-entry",
    "No Active Breach", "Transition Unavailable",
    "Outside Lower Band (Onset Unknown)",
    "Outside Upper Band (Onset Unknown)",
})


def _bb_pct_b_approved_rules(variant: str) -> dict[str, str]:
    """Independent five-state fingerprints, not a second rule evaluator."""
    low, high = _BB_PCT_B_BOUNDARIES[variant]
    return {
        "strong_buy": f"pct_b < {low}",
        "buy": f"pct_b >= {low} and pct_b < 0.10",
        "neutral": "pct_b >= 0.10 and pct_b <= 0.90",
        "sell": f"pct_b > 0.90 and pct_b <= {high}",
        "strong_sell": f"pct_b > {high}",
    }


def _bb_pct_b_finite(value: object) -> Optional[float]:
    """Reject booleans and invalid floating-point values."""
    from math import isfinite
    if isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (ValueError, TypeError, OverflowError):
        return None
    return number if isfinite(number) else None


def _bb_pct_b_verified_value(
    variant: str,
    state: str,
    score: object,
    active_rules: Mapping[str, str],
    raw_pct_b: object,
) -> Optional[float]:
    """Fail closed if score, live rulebook, or raw location disagree."""
    if variant not in _BB_PCT_B_BOUNDARIES or state not in _BB_PCT_B_STATES:
        return None
    if isinstance(score, bool) or score != _BB_PCT_B_SCORES[state]:
        return None
    if not isinstance(active_rules, Mapping):
        return None
    approved = _bb_pct_b_approved_rules(variant)
    if any(
        _fingerprint(str(active_rules.get(key, "") or "")) != _fingerprint(approved[key])
        for key in _BB_PCT_B_STATES
    ):
        return None
    value = _bb_pct_b_finite(raw_pct_b)
    if value is None:
        return None
    low, high = (float(bound) for bound in _BB_PCT_B_BOUNDARIES[variant])
    expected_state = (
        "strong_buy" if value < low else
        "buy" if value < 0.10 else
        "neutral" if value <= 0.90 else
        "sell" if value <= high else
        "strong_sell"
    )
    return value if expected_state == state else None


def _bb_pct_b_display(value: float, variant: str) -> str:
    """Show normal one-decimal precision, expanding near a rule boundary.

    Never print a rounded number equal to a cutoff while prose asserts a
    strict less-than/greater-than inequality that only the raw value proves.
    """
    x = value * 100.0
    low, high = (float(bound) * 100.0 for bound in _BB_PCT_B_BOUNDARIES[variant])
    thresholds = (low, 10.0, 90.0, high)
    for decimals in (1, 3, 6, 10):
        rendered = f"{x:.{decimals}f}"
        rounded = float(rendered)
        if all(not (rounded == boundary and x != boundary) for boundary in thresholds):
            return rendered
    return repr(x)


def get_bollinger_pct_b_rule_explanation(
    variant: str,
    state: str,
    score: int,
    active_rules: Mapping[str, str],
    raw_pct_b: object,
) -> Optional[str]:
    """Observation-specific Rule for the verified five-state %B classifier.

    Returns None on rulebook drift, score mismatch, invalid inputs or a
    conflict with the raw observation. A caller must retain its existing
    rule-translation fallback when None is returned.
    """
    value = _bb_pct_b_verified_value(variant, state, score, active_rules, raw_pct_b)
    if value is None:
        return None
    shown = _bb_pct_b_display(value, variant)
    low, high = (float(bound) * 100 for bound in _BB_PCT_B_BOUNDARIES[variant])
    low_text, high_text = f"{low:g}", f"{high:g}"
    if state == "strong_buy":
        return (f"%B is {shown}, below the {low_text} Strong Buy cutoff; "
                "price is extended below the lower band.")
    if state == "buy":
        position = (
            "below the lower band" if value < 0 else
            "on the lower band" if value == 0 else
            "inside the lower portion of the bands"
        )
        return (f"%B is {shown}, within the Buy interval from {low_text} inclusive "
                f"to below 10; price is {position}.")
    if state == "neutral":
        return f"%B is {shown}, within the Neutral interval of 10 through 90."
    if state == "sell":
        position = (
            "above the upper band" if value > 1 else
            "on the upper band" if value == 1 else
            "inside the upper portion of the bands"
        )
        return (f"%B is {shown}, within the Sell interval above 90 through "
                f"{high_text} inclusive; price is {position}.")
    return (f"%B is {shown}, above the {high_text} Strong Sell cutoff; "
            "price is extended above the upper band.")


def get_bollinger_pct_b_bottom_line(
    variant: str,
    state: str,
    score: int,
    active_rules: Mapping[str, str],
    raw_pct_b: object,
    *,
    breach_status: object = None,
    breach_count: object = None,
    breach_count_exact: object = None,
    bandwidth_state: object = None,
    bandwidth_percentile: object = None,
    bandwidth_direction: object = None,
    bandwidth_relative_5d: object = None,
    bandwidth_direction_streak: object = None,
    bandwidth_compression_exit: object = None,
) -> Optional[str]:
    """Explain the dominant Bollinger price/volatility *condition*.

    Priority: re-entry event -> compression exit -> compressed environment ->
    qualified expansion -> cooling -> remaining material band interaction.
    All evidence is contemporaneous, with no future-bar/outcome inference.
    No five-state score or primary rule is modified.

    Material five-session BW changes (>=20% or <=-20%) are provisional
    *context filters*, never new trading thresholds or a breakout verdict.
    """
    value = _bb_pct_b_verified_value(variant, state, score, active_rules, raw_pct_b)
    if value is None:
        return None

    # Existing independent breach-status integrity contract.
    if breach_status is not None:
        if not isinstance(breach_status, str) or breach_status not in _BB_PCT_B_BREACH_STATUSES:
            return None
        allowed = (
            {"Fresh Lower Breach", "Continuing Lower Breach", "Outside Lower Band (Onset Unknown)"}
            if value < 0 else
            {"Fresh Upper Breach", "Continuing Upper Breach", "Outside Upper Band (Onset Unknown)"}
            if value > 1 else
            {"Lower-Band Re-entry", "Upper-Band Re-entry", "No Active Breach", "Transition Unavailable"}
        )
        if breach_status not in allowed:
            return None
    if breach_count is not None:
        if isinstance(breach_count, bool) or not isinstance(breach_count, int) or breach_count < 0:
            return None
        if breach_status and breach_status.startswith("Continuing ") and breach_count < 2:
            return None
        if breach_status and breach_status.startswith("Fresh ") and breach_count != 1:
            return None
        if breach_status in ("No Active Breach", "Lower-Band Re-entry", "Upper-Band Re-entry") and breach_count != 0:
            return None
    if breach_count_exact is not None and not isinstance(breach_count_exact, bool):
        return None

    # Classify *historical* Bandwidth level from verified production context.
    # The percentile is raw 0..1, with horizon-specific existing cutoffs.
    thresholds = {
        "10_1.5": (0.10, 0.25, 0.75, 0.90),
        "20_2.0": (0.05, 0.15, 0.85, 0.95),
        "50_2.5": (0.05, 0.15, 0.85, 0.95),
    }
    known_states = (
        "Very Compressed", "Compressed", "Normal", "Expanded", "Very Expanded"
    )
    if bandwidth_state is not None and bandwidth_state not in known_states:
        return None
    p = _bb_pct_b_finite(bandwidth_percentile)
    if bandwidth_percentile is not None and (p is None or not 0 <= p <= 1):
        return None
    if p is not None and bandwidth_state is not None:
        p1, p2, p3, p4 = thresholds[variant]
        expected = (
            "Very Compressed" if p < p1 else
            "Compressed" if p < p2 else
            "Normal" if p <= p3 else
            "Expanded" if p <= p4 else
            "Very Expanded"
        )
        if expected != bandwidth_state:
            return None

    if bandwidth_direction not in (None, "Expanding", "Contracting", "Stable"):
        return None
    delta5 = _bb_pct_b_finite(bandwidth_relative_5d)
    if bandwidth_relative_5d is not None and delta5 is None:
        return None
    streak = bandwidth_direction_streak
    if streak is not None and (isinstance(streak, bool) or not isinstance(streak, int) or streak < 0):
        return None
    if streak is not None and bandwidth_direction is not None:
        if (bandwidth_direction == "Stable" and streak != 0) or (
            bandwidth_direction in ("Expanding", "Contracting") and streak < 1
        ):
            return None
    if bandwidth_compression_exit is not None and not isinstance(bandwidth_compression_exit, bool):
        return None
    if bandwidth_compression_exit is True and (
        bandwidth_direction != "Expanding"
        or bandwidth_state in ("Very Compressed", "Compressed")
    ):
        return None

    narrow = bandwidth_state in ("Very Compressed", "Compressed")
    wide = bandwidth_state in ("Expanded", "Very Expanded")
    narrow_text = "exceptionally narrow" if bandwidth_state == "Very Compressed" else "historically narrow"
    wide_text = "exceptionally wide" if bandwidth_state == "Very Expanded" else "historically wide"
    # Percentage threshold is a provisional materiality filter; it does not
    # independently qualify a release or direction of price movement.
    sustained_widening = (
        delta5 is not None and delta5 >= 0.20
        and bandwidth_direction == "Expanding"
        and streak is not None and streak >= 2
    )
    sustained_narrowing = (
        delta5 is not None and delta5 <= -0.20
        and bandwidth_direction == "Contracting"
        and streak is not None and streak >= 2
    )
    side = "lower" if value < 0 else "upper" if value > 1 else None
    pressure = "downside" if side == "lower" else "upside" if side == "upper" else None
    fresh = breach_status in ("Fresh Lower Breach", "Fresh Upper Breach")
    continuing = breach_status in ("Continuing Lower Breach", "Continuing Upper Breach")
    reentry = breach_status in ("Lower-Band Re-entry", "Upper-Band Re-entry")

    # 1. Fresh re-entry: a structural change in price's relation to the band,
    # interpreted in the *actual* contemporaneous volatility environment.
    if reentry:
        prior_side = "lower" if breach_status == "Lower-Band Re-entry" else "upper"
        if bandwidth_compression_exit is True:
            return (f"Price has returned inside from beyond the {prior_side} band as the envelope exits "
                    "historical compression; band position and volatility are changing together.")
        if narrow:
            return (f"Price has returned inside from beyond the {prior_side} band while the envelope "
                    f"remains {narrow_text}; the earlier extension has eased within a compressed market.")
        if sustained_widening:
            return (f"Price has returned inside from beyond the {prior_side} band, interrupting that "
                    "extension while substantial Bandwidth expansion continues.")
        if sustained_narrowing or (wide and bandwidth_direction == "Contracting"):
            return (f"Price has returned inside from beyond the {prior_side} band as Bandwidth contracts; "
                    "both the outside-band extension and envelope width are easing.")
        return (f"Price has returned inside from beyond the {prior_side} band; the outside-band "
                "extension has ended while the current Bandwidth State persists.") if bandwidth_state is not None else None

    # 2. First actual transition out of compressed State, not a rolling
    # 'was compressed recently' flag.
    if bandwidth_compression_exit is True:
        if side:
            return (f"The envelope has just exited historical compression while price "
                    f"remains beyond the {side} band; {pressure} pressure is developing "
                    "alongside materially wider bands.")
        position = "lower" if value < 0.5 else "upper" if value > 0.5 else "middle"
        return ("Bandwidth has just exited historical compression and is expanding "
                f"materially, with price still inside the {position} portion of the envelope.")

    # 3. Historical compression is meaningful on its own. A large increase
    # from a tiny starting base does not override a still-compressed State.
    if narrow:
        if side:
            if sustained_widening:
                return (f"Price is {'newly ' if fresh else ''}beyond the {side} band while "
                        f"the still {narrow_text} envelope widens repeatedly; an emerging "
                        f"{pressure} release is being tested from compressed conditions.")
            if fresh:
                return (f"Price has newly breached the {side} band while Bandwidth is "
                        f"still {narrow_text}; this is an initial {pressure} extension "
                        "within a compressed volatility environment.")
            return (f"Price remains beyond the {side} band, but Bandwidth is still "
                    f"{narrow_text}; {pressure} pressure is occurring without an "
                    "established expansion out of compression.")
        if sustained_narrowing or bandwidth_direction == "Contracting":
            return (f"The {narrow_text} envelope is contracting further; price "
                    "remains inside the bands as volatility compression deepens.")
        if sustained_widening:
            return (f"Bandwidth is widening repeatedly but remains {narrow_text}; "
                    "the compressed environment has not yet transitioned into a broader envelope.")
        if bandwidth_direction == "Expanding":
            return (f"Bandwidth is widening today but remains {narrow_text}; "
                    "the earlier compression has not yet been released.")
        if delta5 is not None and delta5 >= 0.20:
            return ("Bandwidth has widened considerably over five sessions, but the envelope "
                    f"remains {narrow_text}; historical compression is still in place.")
        if delta5 is not None and delta5 <= -0.20:
            return (f"Bandwidth remains {narrow_text} after considerable recent contraction; "
                    "the latest daily movement has paused, but compression persists.")
        location = "lower" if value < 0.5 else "upper" if value > 0.5 else "middle"
        article = "an" if bandwidth_state == "Very Compressed" else "a"
        return (f"Price remains in the {location} portion of {article} {narrow_text} envelope; "
                "the low-volatility environment is still in place.")

    # 4. Established multi-session expansion, with band breach and interior
    # cases distinguished from the price's directional trend.
    if sustained_widening:
        if continuing:
            return (f"Repeated closes beyond the {side} band accompany sustained "
                    f"Bandwidth expansion, indicating persistent {pressure} pressure "
                    "in a widening envelope.")
        if fresh:
            return (f"Price has newly breached the {side} band during established "
                    f"multi-session Bandwidth expansion; {pressure} pressure is intensifying.")
        if side:
            return (f"Price remains beyond the {side} band during sustained widening; "
                    f"the extension and expanding volatility remain aligned to the {pressure} side.")
        return ("Price is inside the bands while the envelope widens materially "
                "across consecutive sessions; volatility expansion remains active "
                "without a current outside-band extension.")

    # 5. Cooling is a *contraction in a still-wide envelope*, not a confirmed
    # change in the future trend or an unsupported historical peak claim.
    if wide and sustained_narrowing:
        if side:
            return (f"Price remains beyond the {side} band while historically wide "
                    "bands contract across recent sessions; the volatility expansion is easing.")
        return ("The historically wide envelope is narrowing across recent sessions; "
                "price is inside the bands as the volatility expansion cools.")

    # 6. Material event/level combinations that do not satisfy an established
    # multi-session expansion or contraction threshold.
    if wide and side:
        article = "an" if bandwidth_state == "Very Expanded" else "a"
        return (f"Price remains beyond the {side} band in {article} {wide_text} volatility "
                f"envelope; {pressure} extension is occurring under elevated dispersion.")
    if wide and bandwidth_direction == "Contracting":
        return ("The historically wide envelope is beginning to contract; "
                "volatility remains elevated even as daily band width eases.")
    if fresh and bandwidth_state is not None:
        return (f"Price has newly breached the {side} band while Bandwidth is "
                f"in its {('typical' if bandwidth_state == 'Normal' else 'elevated')} historical range; "
                f"this marks a fresh {pressure} extension without established multi-session expansion.")
    if bandwidth_direction == "Expanding" and delta5 is not None and delta5 <= -0.20:
        return ("Bandwidth widened today but remains materially narrower than "
                "five sessions earlier; the broader recent movement is still contraction.")

    # 7. An exceptionally wide envelope after material five-session growth
    # remains notable even when the latest daily widening has paused.
    # This is lower priority than every existing event/level condition.
    if (
        bandwidth_state == "Very Expanded"
        and p is not None
        and bandwidth_direction == "Stable"
        and delta5 is not None and delta5 >= 0.20
        and breach_status == "No Active Breach"
    ):
        if value >= 0.90:
            position = "near the upper band, indicating upper-side price strength"
        elif value <= 0.10:
            position = "near the lower band, indicating lower-side price pressure"
        elif value > 0.50:
            position = "in the upper portion of the bands"
        elif value < 0.50:
            position = "in the lower portion of the bands"
        else:
            position = "near the middle of the bands"
        return ("Bandwidth remains exceptionally wide after substantial five-session "
                f"expansion, with price {position}. Material daily widening has paused.")
    return None

# signal_classifier.py
"""
Signal classification and rule-engine evaluation.
This module implements the rulebook-driven signal engine.

Note:
    skip_errors=True is intentionally supported to allow staged indicator
    onboarding. During migration phases, some rulebook expressions may
    reference indicators that are not yet computed; skipping these errors
    allows partial rule evaluation without breaking the pipeline. (12/13/25)
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path

import pandas as pd

try:
    # Package-safe imports (when used as part of a package/module)
    from .expression_engine import ExpressionEngine, SafeExpressionError
    from .signals_loader import RulesRepository
except ImportError:  # pragma: no cover
    # Fallback for running standalone (e.g., ad-hoc scripts)
    from expression_engine import ExpressionEngine, SafeExpressionError
    from signals_loader import RulesRepository


# Order of precedence when multiple rules are true
DEFAULT_SIGNAL_PRIORITY: List[str] = [
    "strong_buy",
    "buy",
    "neutral",
    "sell",
    "strong_sell",
]

# Optional scoring map (if you want numeric scoring later)
DEFAULT_SIGNAL_SCORES: Dict[str, int] = {
    "strong_sell": -2,
    "sell": -1,
    "neutral": 0,
    "buy": 1,
    "strong_buy": 2,
}


class SignalEngine:
    """
    Evaluates technical-analysis rule blocks from master_rules.json against a price/indicator DataFrame.

    Typical usage:

        repo = RulesRepository.from_file("master_rules.json")
        engine = SignalEngine(repo)

        signals = engine.evaluate(
            df=some_dataframe,
            feature_scope="heatmap",
            indicators=None,         # all indicators
        )

    `df` is expected to have columns referenced in rule expressions,
    e.g. RSI_14, MACD_12_26_9, Close, ATRP_14, etc.
    """

    def __init__(
        self,
        rules_repo: RulesRepository,
        expression_engine: Optional[ExpressionEngine] = None,
        signal_priority: Optional[List[str]] = None,
    ):
        self.rules_repo = rules_repo
        self.expr_engine = expression_engine or ExpressionEngine()
        self.signal_priority = signal_priority or DEFAULT_SIGNAL_PRIORITY

    # ------------- Public API -------------

    def evaluate(
        self,
        df: pd.DataFrame,
        feature_scope: str = "heatmap",
        indicators: Optional[List[str]] = None,
        skip_errors: bool = False,
    ) -> Dict[str, Dict[str, pd.Series]]:
        """
        Evaluate rules for the given feature_scope across all or selected indicators.

        Returns:
            {
              "RSI": {
                "10": pd.Series([...signals...]),
                "14": pd.Series([...signals...]),
              },
              "MACD": {
                "12_26_9": pd.Series([...]),
                ...
              },
              ...
            }
        """
        if indicators is None:
            indicator_map = self.rules_repo.list_indicators()
            indicators = list(indicator_map.keys())

        results: Dict[str, Dict[str, pd.Series]] = {}

        for ind_name in indicators:
            feature = self.rules_repo.get_feature_scope(ind_name, feature_scope)
            if not feature:
                continue  # no rules for this scope

            param_keys = list(feature.keys())
            if not param_keys:
                continue

            ind_results: Dict[str, pd.Series] = {}
            for param_key in param_keys:
                rule_block = self.rules_repo.get_rule_block(ind_name, feature_scope, param_key)
                if not rule_block:
                    continue

                # Evaluate a single rule block over df
                try:
                    signals = self._evaluate_rule_block(
                        df=df,
                        rule_block=rule_block,
                        indicator_name=ind_name,
                        param_key=param_key,
                    )
                except SafeExpressionError:
                    if skip_errors:
                        # During staged migrations we may not have all columns implemented;
                        # skipping makes the engine robust while bringing indicators online.
                        continue
                    raise

                ind_results[param_key] = signals

            if ind_results:
                results[ind_name] = ind_results

        return results

    def evaluate_to_scores(
        self,
        df: pd.DataFrame,
        feature_scope: str = "heatmap",
        indicators: Optional[List[str]] = None,
        score_map: Dict[str, int] | None = None,
        skip_errors: bool = True,      # `True`: intended for staged indicator onboarding
    ) -> Dict[str, Dict[str, pd.Series]]:
        """
        Same as evaluate(), but converts signals into numeric scores.
        """
        score_map = score_map or DEFAULT_SIGNAL_SCORES
        signal_results = self.evaluate(
            df=df,
            feature_scope=feature_scope,
            indicators=indicators,
            skip_errors=skip_errors,
        )
        scored: Dict[str, Dict[str, pd.Series]] = {}
        for ind_name, by_param in signal_results.items():
            scored[ind_name] = {}
            for param_key, ser in by_param.items():
                scored[ind_name][param_key] = ser.map(score_map).astype("float")
        return scored

    # ------------- Internal helpers -------------

    def _evaluate_rule_block(
        self,
        df: pd.DataFrame,
        rule_block: Dict[str, Any],
        indicator_name: str,
        param_key: str,
    ) -> pd.Series:
        """
        Evaluate one rule block (strong_buy / buy / neutral / sell / strong_sell)
        and return a Series of signal labels for each row.
        """
        # Initialize all rows as 'neutral' by default
        signal_series = pd.Series("neutral", index=df.index, dtype="object")

        # Build context from df columns
        context = {col: df[col] for col in df.columns}

        # Canonical price aliasing (Option C rule compatibility)
        if "Close" in context and "close" not in context:
            context["close"] = context["Close"]

        for label in self.signal_priority:
            expr = rule_block.get(label, "")
            if not isinstance(expr, str) or expr.strip() == "":
                # No rule defined for this bucket
                continue

            try:
                mask = self.expr_engine.evaluate(expr, context)
            except SafeExpressionError as e:
                # If a single bucket expr is broken, log/raise as you prefer.
                # Here, we opt to raise so you see it during development.
                raise SafeExpressionError(
                    f"Error evaluating expression for {indicator_name}({param_key})[{label}]: {e}"
                ) from e

            # Expect mask to be a Series[bool] aligned with df index
            if not isinstance(mask, pd.Series):
                # If scalar, broadcast
                if isinstance(mask, (bool, int, float)):
                    mask = pd.Series(bool(mask), index=df.index)
                else:
                    raise SafeExpressionError(
                        f"Expression for {indicator_name}({param_key})[{label}] "
                        f"did not return a Series or scalar."
                    )

            # Apply label where mask is True
            signal_series[mask.astype(bool)] = label

        return signal_series

def build_default_signal_engine(
    rules_path: str | Path = "master_rules_normalized.json",
    expression_engine: Optional[ExpressionEngine] = None,
) -> SignalEngine:
    """
    Convenience constructor for a SignalEngine wired to the master rulebook.

    Centralizes the standard way to construct:
      - RulesRepository from the normalized rulebook
      - ExpressionEngine (defaults to safe ExpressionEngine)
    """

    # Robust rulebook path resolution:
    # - If caller passes an absolute path, use it.
    # - If caller passes a relative path that exists from CWD, use it.
    # - Otherwise, fall back to src/config/master_rules_normalized.json
    rp = Path(rules_path)
    if not rp.is_absolute() and not rp.exists():
        # signal_classifier.py lives in src/calculations/
        # so config is one directory up: src/config/
        candidate = Path(__file__).resolve().parents[1] / "config" / "master_rules_normalized.json"
        if candidate.exists():
            rp = candidate

    repo = RulesRepository.from_file(rp)
    #repo = RulesRepository.from_file(rules_path)

    return SignalEngine(rules_repo=repo, expression_engine=expression_engine)

# Helper
def run_optionc_heatmap(
    df: pd.DataFrame,
    rules_path: str | Path = "master_rules_normalized.json",
    feature_scope: str = "heatmap",
    indicators: Optional[List[str]] = None,
    skip_errors: bool = True,
) -> Dict[str, Dict[str, pd.Series]]:
    """
    Rule-engine harness used by technical.py for the initial Option C slice.

    Returns numeric scores in [-2..2] for each indicator/param series:
      {
        "RSI": {"14": Series[int]},
        "MACD": {"12_26_9": Series[int]},
        "Stochastic": {"14_3_3": Series[int]},
        "ADX": {"14": Series[int]},
      }

    If `indicators` is None, defaults to the Option C subset above.
    """
    # Hardening: upstream may return None/empty if OHLCV fetch fails.
    # Return empty payload rather than raising deep inside evaluation.
    if df is None or getattr(df, "empty", True):
        return {}

    if indicators is None:
        indicators = ["RSI", "MACD", "Stochastic", "ADX"]

    engine = build_default_signal_engine(rules_path=rules_path)
    return engine.evaluate_to_scores(
        df=df,
        feature_scope=feature_scope,
        indicators=indicators,
        score_map=DEFAULT_SIGNAL_SCORES,
        skip_errors=skip_errors,
    )
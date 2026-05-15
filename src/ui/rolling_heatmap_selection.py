# Stamp: Thu, May 14, 2026 6:22PM
# src/ui/rolling_heatmap_selection.py
"""
Rolling Heatmap row-selection resolution.

Purpose:
    Own the deterministic row-set resolution path for the Phase III
    Rolling Heatmap Selection & Catalog architecture.

Resolution order:
    1. Selection mode is chosen by the UI layer.
    2. This module resolves that mode into an ordered list of canonical row_key values.
    3. streamlit_app.py feeds the resolved row_key list into the existing manual
       display/remove controls.
    4. Existing manual row-order controls remain the final downstream override.

Scope:
    This module owns derived selection logic only:
      - Custom mode resolution
      - Category / Scope / Window / Family filtering
      - grouped-family filtering
      - explicit Overview preset loading
      - generated thematic preset loading
      - Window = All handling

    It does not own:
      - row classification metadata
      - curated preset membership metadata
      - numeric computation
      - rulebook semantics
      - signal scoring
      - rolling payload generation
      - display names
      - definitions / educational text
      - Plotly transformation
      - UI control rendering

Authority:
    All outputs are canonical rolling heatmap row_key lists.

Important ownership boundary:
    Display / education metadata remains in rolling_heatmap_adapter.py::INDICATOR_DEFS.
    Manual display/remove and row-order controls remain downstream in streamlit_app.py.
"""

from __future__ import annotations

from typing import Iterable, List, Mapping, Sequence

try:
    from .rolling_heatmap_classification import (
        FAMILY_GROUPS,
        ROW_CLASSIFICATION,
        get_categories,
        get_families,
        get_scopes,
        get_windows,
    )
    from .rolling_heatmap_presets import (
        CUSTOM_DEFAULT,
        OVERVIEW_PRESETS,
        PRESET_ORDER,
    )
except ImportError:  # pragma: no cover
    # Allows direct ad-hoc execution from repo root during manual verification.
    from src.ui.rolling_heatmap_classification import (
        FAMILY_GROUPS,
        ROW_CLASSIFICATION,
        get_categories,
        get_families,
        get_scopes,
        get_windows,
    )
    from src.ui.rolling_heatmap_presets import (
        CUSTOM_DEFAULT,
        OVERVIEW_PRESETS,
        PRESET_ORDER,
    )


SELECTION_MODES: tuple[str, ...] = ("Custom", "Category", "Preset")

# Generated thematic presets.
# Overview presets are explicit curated memberships in rolling_heatmap_presets.py.
_THEMATIC_PRESET_RULES: Mapping[str, tuple[str, str]] = {
    "ST Trend": ("Trend", "ST"),
    "MT Trend": ("Trend", "MT"),
    "LT Trend": ("Trend", "LT"),
    "ST Momentum": ("Momentum", "ST"),
    "MT Momentum": ("Momentum", "MT"),
    "LT Momentum": ("Momentum", "LT"),
}


# ---------------------------------------------------------------------
# Generic row-key helpers
# ---------------------------------------------------------------------
def _dedupe_preserve_order(row_keys: Iterable[str]) -> List[str]:
    """Return row keys with duplicates removed while preserving first-seen order."""
    seen: set[str] = set()
    out: List[str] = []

    for row_key in row_keys:
        if row_key in seen:
            continue
        seen.add(row_key)
        out.append(row_key)

    return out


def get_unknown_row_keys(row_keys: Iterable[str]) -> List[str]:
    """Return row keys not present in ROW_CLASSIFICATION."""
    known = set(ROW_CLASSIFICATION.keys())
    return [row_key for row_key in row_keys if row_key not in known]


def validate_row_keys(row_keys: Iterable[str], *, context: str = "row selection") -> None:
    """Raise ValueError when a row-key list references unknown catalog rows."""
    unknown = get_unknown_row_keys(row_keys)
    if unknown:
        raise ValueError(f"Unknown row_key(s) in {context}: {unknown}")


def _normalize_optional_filter(value: str | None) -> str | None:
    """
    Normalize optional UI filter values.

    The UI may use None, empty string, or "All" to mean no filter.
    """
    if value is None:
        return None

    normalized = str(value).strip()
    if not normalized or normalized == "All":
        return None

    return normalized


def _catalog_order(row_keys: Iterable[str]) -> List[str]:
    """
    Return row_keys in ROW_CLASSIFICATION order.

    Selection resolution is deterministic and catalog-order based.
    Unknown keys are ignored here because public resolvers validate separately.
    """
    wanted = set(row_keys)
    return [row_key for row_key in ROW_CLASSIFICATION.keys() if row_key in wanted]


def _family_filter_matches(row_family: str, selected_family: str | None) -> bool:
    """
    Return True if row_family matches the selected Family filter.

    selected_family may be:
      - None / All: no family filtering
      - grouped-family alias such as MVA or Oscillators
      - direct family name such as ADX, MACD, ROC, Bollinger, OBV
    """
    selected = _normalize_optional_filter(selected_family)
    if selected is None:
        return True

    if selected in FAMILY_GROUPS:
        return row_family in FAMILY_GROUPS[selected]

    return row_family == selected


# ---------------------------------------------------------------------
# Available control values
# ---------------------------------------------------------------------
def get_selection_modes() -> List[str]:
    """Return available selection modes in locked v1 order."""
    return list(SELECTION_MODES)


def get_preset_names() -> List[str]:
    """Return preset names in locked v1 dropdown order."""
    return list(PRESET_ORDER)


def get_category_names() -> List[str]:
    """Return available Category values."""
    return get_categories()


def get_scope_names(category: str | None = None) -> List[str]:
    """Return available Scope values, optionally narrowed by Category."""
    return get_scopes(category=_normalize_optional_filter(category))


def get_window_names(category: str | None = None) -> List[str]:
    """Return available Window values, optionally narrowed by Category."""
    return get_windows(category=_normalize_optional_filter(category))


def get_family_names(category: str | None = None) -> List[str]:
    """Return available Family filter values, including grouped-family aliases."""
    return get_families(category=_normalize_optional_filter(category))


# ---------------------------------------------------------------------
# Mode-specific resolvers
# ---------------------------------------------------------------------
def resolve_custom_rows(
    custom_rows: Sequence[str] | None = None,
    *,
    strict: bool = True,
) -> List[str]:
    """
    Resolve Custom mode to an ordered canonical row_key list.

    custom_rows:
        Edited/saved Custom state from UI/session state.
        When omitted, the authoritative CUSTOM_DEFAULT catalog is used.

    strict:
        When True, unknown row keys raise ValueError.
    """
    source_rows = list(CUSTOM_DEFAULT if custom_rows is None else custom_rows)
    resolved = _dedupe_preserve_order(source_rows)

    if strict:
        validate_row_keys(resolved, context="Custom mode")

    return resolved


def resolve_category_rows(
    *,
    category: str,
    scope: str | None = None,
    window: str | None = None,
    family: str | None = None,
    strict: bool = True,
) -> List[str]:
    """
    Resolve Category mode to an ordered canonical row_key list.

    Required:
        category

    Optional AND-filters:
        scope
        window
        family

    Window = All handling:
        Rows classified with window == "All" are included when no Window filter
        is active. When a Window filter is active, Window = All rows are excluded
        from Category-mode results unless they enter later through Custom, Preset,
        or manual UI override.
    """
    normalized_category = _normalize_optional_filter(category)
    normalized_scope = _normalize_optional_filter(scope)
    normalized_window = _normalize_optional_filter(window)
    normalized_family = _normalize_optional_filter(family)

    if normalized_category is None:
        raise ValueError("Category mode requires a concrete category.")

    resolved: List[str] = []

    for row_key, meta in ROW_CLASSIFICATION.items():
        if meta["category"] != normalized_category:
            continue

        if normalized_scope is not None and meta["scope"] != normalized_scope:
            continue

        if normalized_window is not None:
            if meta["window"] == "All":
                continue
            if meta["window"] != normalized_window:
                continue

        if not _family_filter_matches(meta["family"], normalized_family):
            continue

        resolved.append(row_key)

    resolved = _catalog_order(resolved)

    if strict:
        validate_row_keys(resolved, context="Category mode")

    return resolved


def resolve_preset_rows(
    preset_name: str,
    *,
    strict: bool = True,
) -> List[str]:
    """
    Resolve Preset mode to an ordered canonical row_key list.

    Explicit Overview presets:
        Loaded from OVERVIEW_PRESETS.

    Generated thematic presets:
        ST/MT/LT Trend and ST/MT/LT Momentum are generated from
        ROW_CLASSIFICATION via Category + Window rules.
    """
    preset = str(preset_name).strip()

    if preset in OVERVIEW_PRESETS:
        resolved = _dedupe_preserve_order(OVERVIEW_PRESETS[preset])
        if strict:
            validate_row_keys(resolved, context=f"Preset mode ({preset})")
        return resolved

    if preset in _THEMATIC_PRESET_RULES:
        category, window = _THEMATIC_PRESET_RULES[preset]
        resolved = resolve_category_rows(
            category=category,
            window=window,
            strict=strict,
        )
        return resolved

    raise ValueError(f"Unknown preset: {preset_name!r}")


def resolve_row_selection(
    *,
    selection_mode: str,
    custom_rows: Sequence[str] | None = None,
    category: str | None = None,
    scope: str | None = None,
    window: str | None = None,
    family: str | None = None,
    preset_name: str | None = None,
    strict: bool = True,
) -> List[str]:
    """
    Resolve any supported selection mode to an ordered canonical row_key list.

    This is the single public resolver intended for streamlit_app.py wiring.
    """
    mode = str(selection_mode).strip()

    if mode == "Custom":
        return resolve_custom_rows(custom_rows=custom_rows, strict=strict)

    if mode == "Category":
        if category is None:
            raise ValueError("Category selection requires category=...")
        return resolve_category_rows(
            category=category,
            scope=scope,
            window=window,
            family=family,
            strict=strict,
        )

    if mode == "Preset":
        if preset_name is None:
            raise ValueError("Preset selection requires preset_name=...")
        return resolve_preset_rows(preset_name, strict=strict)

    raise ValueError(f"Unknown selection mode: {selection_mode!r}")


# ---------------------------------------------------------------------
# Empty-state helper
# ---------------------------------------------------------------------
def describe_empty_selection(
    *,
    selection_mode: str,
    category: str | None = None,
    scope: str | None = None,
    window: str | None = None,
    family: str | None = None,
    preset_name: str | None = None,
) -> str:
    """
    Return a deterministic, UI-friendly empty-state message.

    This helper does not render the message; streamlit_app.py owns rendering.
    """
    mode = str(selection_mode).strip()

    if mode == "Category":
        parts = [f"Category={category!r}"]
        if _normalize_optional_filter(scope) is not None:
            parts.append(f"Scope={scope!r}")
        if _normalize_optional_filter(window) is not None:
            parts.append(f"Window={window!r}")
        if _normalize_optional_filter(family) is not None:
            parts.append(f"Family={family!r}")
        return "No rolling heatmap rows matched the selected filters: " + ", ".join(parts)

    if mode == "Preset":
        return f"No rolling heatmap rows resolved for preset {preset_name!r}."

    if mode == "Custom":
        return "No rolling heatmap rows are currently selected in Custom mode."

    return "No rolling heatmap rows resolved for the current selection."
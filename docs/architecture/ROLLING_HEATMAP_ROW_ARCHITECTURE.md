# Rolling Heatmap Row Architecture Contract
Version: 1.1
Created: 3/14/26
Last Update: 3/15/26 

**Status:** working architecture spec for Phase III UX / Hover Enrichment
**Purpose:** define where row identity, row metadata, per-cell values, and hover metadata belong before implementation begins.
**Usage:** load this document before any implementation session touching Rolling Heatmap hover behavior.

## 1. Scope and boundary

This contract applies only to the **Rolling Signals Heatmap** UI path.

It must preserve the current layer separation:

* `technical.py` defines rolling row inclusion and produces the rolling payload 
* `rolling_heatmap_adapter.py` converts the rolling payload into Plotly-ready row/cell structures 
* `streamlit_app.py` controls row selection, row ordering, and rendering only 

This contract must **not** introduce changes to:

* indicator computation
* rule thresholds
* signal scoring semantics
* Scenario B data acquisition logic
* OHLCV persistence policy

---

## Phase III UX Workstream Context

**Active UX Task:** Hover Enrichment  
**Primary Implementation Layer:** rolling_heatmap_adapter.py  
**Supporting UI Layer:** streamlit_app.py  

The Row Architecture Contract exists to ensure that hover enrichment
and other UX improvements are implemented without modifying:

- rule semantics
- indicator computation
- rolling payload contracts
- Scenario B data assembly behavior

All hover metadata must therefore be derived within the adapter layer
(`build_plotly_heatmap_inputs`) using the existing rolling payload.


---

## 2. Canonical row identity source

### File

* `technical.py`

### Function

* `_get_optionc_meta()`

### Authoritative fields

Each heatmap-capable indicator row is defined by metadata entries containing:

* `engine_indicator`
* `param_key`
* `display_key`
* `value_col`
* `extra_value_cols` (only where applicable, e.g. BullBearPower) 

### Rule

`display_key` is the canonical row identity for indicator rows.

Examples already present in `_get_optionc_meta()` include:

* `RSI_14`
* `MACD_12_26_9`
* `STOCH_14_3_3`
* `ROC_12`
* `WILLR_14`
* `ADX_14`
* `MFI_14`
* `CMF_21`
* `OBV`
* `EMA_20`
* `HMA_21`
* `CCI_14`
* `UO_7_14_28` 

### Constraint

No UI layer may invent or rename row identities independently of `_get_optionc_meta()`.

---

## 3. Rolling payload contract (backend)

### File

* `technical.py`

### Function

* `_build_optionc_rolling_signals(...)`

### Current top-level payload fields

The rolling payload returned from `_build_optionc_rolling_signals(...)` currently contains:

* `engine`
* `status`
* `ticker`
* `dates`
* `short_term`
* `intermediate_term`
* `long_term`
* `composite_scores`
* `extras` 

### Active timeframe block

The currently active row/cell data lives under:

* `short_term["indicators"]`
* `short_term["data"]` 

### Date-major data rule

`short_term["data"]` is organized by date first, then by indicator row key:

```python
short_term["data"] = {
    <date_key>: {
        <display_key>: cell,
        ...
    },
    ...
}
```

This is the current backend storage shape. 

### Price row source

The display-only price row is sourced from:

* `extras["price"]["label"]`
* `extras["price"]["values"]`
* `extras["price"]["dates"]` 

### Constraint

Any Phase III UX enhancement must consume this payload contract rather than bypass it.

---

## 4. Adapter contract (UI-ready transformation)

### File

* `rolling_heatmap_adapter.py`

### Primary components

* `PlotlyHeatmapInputs`
* `INDICATOR_DEFS`
* `build_plotly_heatmap_inputs(...)`
* `make_rolling_heatmap_figure(...)` 

### Final UI-ready output

The adapter emits `PlotlyHeatmapInputs` with these exact fields:

* `z`
* `text`
* `customdata`
* `x`
* `y`
* `row_keys` 

### Meaning

* `z` = score/color matrix
* `text` = displayed cell text
* `customdata` = per-cell hover/click metadata
* `x` = date column labels
* `y` = row display labels
* `row_keys` = stable internal row IDs

---

## 5. Row display metadata source

### File

* `rolling_heatmap_adapter.py`

### Variable

* `INDICATOR_DEFS`

### Current row metadata fields

For indicator rows, `INDICATOR_DEFS` currently stores:

* `display_name`
* `definition`
* `how_to_read` 

### Rule

These are **row-stable** descriptive fields and belong in the adapter metadata layer.

### Constraint

The UI must not construct or hardcode indicator explanation text independently if it can be sourced from `INDICATOR_DEFS`.

---

## 6. Current per-cell `customdata` contract

### File

* `rolling_heatmap_adapter.py`

### Function

* `build_plotly_heatmap_inputs(...)`

### Indicator cell `customdata`

Each indicator heatmap cell currently carries:

* `indicator_key`
* `display_name`
* `date`
* `raw_value`
* `score`
* `meta` 

### Price row `customdata`

Each price-row cell currently carries the same general shape, with:

* `indicator_key = "__PRICE__"`
* `display_name = "Price"`
* `score = None` 

### Rule

Cell-level hover enrichment must extend this `customdata` object rather than creating a parallel hover data path.

---

## 7. Synthetic price row rule

### File

* `rolling_heatmap_adapter.py`

### Current behavior

The adapter creates a synthetic display-only row using the stable row key:

* `__PRICE__` 

### Rule

The Price row is classified as a **display-only row**.

It must never:

* participate in rule evaluation
* affect scoring
* alter indicator semantics

This is consistent with your existing architecture and planning rules.

---

## 8. UI-owned state vs adapter-owned state

### UI-owned state

**File:** `streamlit_app.py`

The UI currently owns:

* `selected_keys`
* `st.session_state.rh_row_order`
* `ordered_selected_keys`
* the call to `build_plotly_heatmap_inputs(...)`
* the call to `make_rolling_heatmap_figure(...)` 

### Adapter-owned state

**File:** `rolling_heatmap_adapter.py`

The adapter owns:

* row label resolution
* row definition metadata
* per-cell hover metadata construction
* conversion from rolling payload → Plotly-ready matrices 

### Rule

The UI may control:

* selection
* visibility
* ordering
* rendering

The UI must not own:

* rule explanation construction
* row semantic metadata
* per-cell calculation logic beyond formatting

---

## 9. Hover enrichment placement rules

This is the most important implementation guidance for the next session.

### A. Row-stable hover/explanation fields

These belong in:

* `INDICATOR_DEFS`

Examples:

* `display_name`
* `definition`
* `how_to_read`

These do not vary by date.

### B. Date-specific hover fields

These belong in:

* `customdata` built inside `build_plotly_heatmap_inputs(...)`

#### Price-row examples

The future hover fields you defined should be added there:

* delta vs prior day
* percent change vs prior day
* volume
* volume vs 5D average

#### Indicator-row examples

These should also be added to `customdata`:

* value delta vs prior day
* relative delta
* trend
* signal text
* rule text

### Constraint

No date-specific hover field should be stored in `INDICATOR_DEFS`.

---

## 10. Implementation guardrails for the next session

Hover enrichment must be implemented without changing:

* `_get_optionc_meta()` row identities unless explicitly justified
* backend rule scores
* `master_rules_normalized.json`
* indicator computation in `indicator_preprocessor.py`
* Scenario B helper behavior in `technical.py`

All hover work should remain localized to:

* `rolling_heatmap_adapter.py`
* `streamlit_app.py`

with `technical.py` referenced only when necessary to understand existing payload structure.

---

## 11. Minimum verification checklist for implementation

Before accepting hover enrichment as complete, verify:

* row keys in `row_keys` still match backend row identities
* `__PRICE__` remains display-only
* `selected_keys` and `rh_row_order` still work unchanged
* `customdata` contains the new hover fields for both indicator rows and price row
* no rule scores or displayed values changed unintentionally
* no new persistence behavior was introduced

---

## 12. One-sentence working summary

The Rolling Heatmap row architecture is:

* **row identity from `_get_optionc_meta()`**
* **rolling payload from `_build_optionc_rolling_signals(...)`**
* **row/cell transformation in `build_plotly_heatmap_inputs(...)`**
* **selection/order/rendering in `streamlit_app.py`**

---
# Rolling Heatmap Selection & Catalog Contract — Phase III UI Selection Architecture (v1)
Date: 5/6/26

**Status:** working architecture spec for the rolling heatmap grouping / selection workstream
**Purpose:** define where row classification, curated row-set membership, and selection-resolution logic belong before implementation begins.
**Usage:** load this document before any implementation session touching rolling heatmap grouping, presets, custom row sets, or selection controls.

---

## 1. Scope and boundary

This contract applies only to the **rolling heatmap selection / grouping architecture**.

It must preserve the current layer separation:

* `technical.py` computes / assembles rolling payloads and remains the runtime authority for row-producing indicator data
* `rolling_heatmap_adapter.py` owns display-facing row presentation metadata and Plotly transformation
* `streamlit_app.py` owns UI controls and user interaction flow
* new selection/catalog modules in `src/ui` own grouping metadata, curated memberships, and selection-resolution logic
* upstream numeric and semantic layers remain authoritative for indicator values and scores

This contract must **not** introduce changes to:

* base indicator formulas in `indicator_preprocessor.py`
* rule semantics in `master_rules_normalized.json`
* rule-engine evaluation behavior in `signal_classifier.py`
* Scenario B OHLCV acquisition / persistence behavior in `technical.py`
* `INDICATOR_DEFS` educational/display ownership in `rolling_heatmap_adapter.py`
* existing rolling heatmap rendering contract beyond the row-selection input path

### Workstream context

**Workstream type:** Phase III UI selection architecture
**Primary implementation layer:** `src/ui` selection/catalog metadata + `streamlit_app.py` control wiring
**Goal:** allow rolling heatmap row sets to be resolved through:

* Custom
* Category
* Preset

without redefining numeric computation, rule semantics, or row presentation ownership.

### Included in scope

* authoritative row classification mapping
* Window / Category / Scope / Family selection architecture
* Custom default row-set ownership
* curated Overview preset ownership
* generated thematic preset ownership
* selection-resolution logic
* integration of those resolved row sets into the existing manual display/remove and row-order controls

### Explicitly out of scope

* changing indicator formulas
* changing score semantics
* changing rulebook thresholds
* introducing new row identity schemes
* moving educational hover/definition content into the new catalog layer
* replacing existing manual row controls rather than feeding them

---

## 2. Canonical row identity source

### Files

* `technical.py`
* `rolling_heatmap_adapter.py`
* new classification catalog module(s) in `src/ui`

### Primary row identity

Canonical row identity is defined by:

* `row_key`

Examples:

* `EMA_50`
* `RSI_14`
* `VWMA_20`
* `BB_PCT_B`
* `MACD_12_26_9`

### Rule

Row identity is **not** defined by:

* `display_name`
* hover text
* dropdown labels
* family names alone
* category/scope/window classification fields

### Constraint

All grouping, preset, and custom membership metadata must resolve by canonical `row_key`, because the current adapter/runtime contract already uses stable row keys as row IDs.  

---

## 3. Canonical grouping metadata source

### Files

* new classification catalog module(s) in `src/ui`

### Required metadata domains

The grouping/catalog layer must maintain three distinct metadata domains.

#### A. Classification metadata

Per `row_key`:

* `family`
* `category`
* `scope`
* `window`
* optional `tags`
* optional `family_group`

#### B. Curated membership metadata

Per `row_key` or preset:

* Custom default membership
* explicit Overview preset membership
* preset ordering / labels

#### C. Display / education metadata

Remains in:

* `rolling_heatmap_adapter.py::INDICATOR_DEFS`

### Rule

The new selection/catalog layer must own classification and curated membership metadata only.

### Constraint

`INDICATOR_DEFS` remains the authoritative home for:

* `display_name`
* `definition`
* `how_to_read`
* future display-only warning/help text

That display metadata must not be silently migrated into the new grouping catalog. 

---

## 4. Selection transformation path

### Files

* `streamlit_app.py`
* new selection-resolution module(s) in `src/ui`
* existing downstream consumer path in `technical.py` / `rolling_heatmap_adapter.py`

### Primary transformation path

The row-selection path must be:

1. **Selection Mode**
2. **mode-specific controls**
3. **resolved base row-key set**
4. **manual display/remove override**
5. **manual row-order override**
6. **existing heatmap render path**

### Selection modes

#### A. Custom

Base set = saved Custom row-key set

#### B. Category

Base set = all rows whose canonical classification matches selected Category
Optional narrowing filters:

* Scope
* Window
* Family

#### C. Preset

Base set = rows belonging to the selected preset

### Rule

Selection-resolution logic must resolve to an ordered list of canonical `row_key` values before the existing heatmap render path consumes the row set.

### Constraint

No downstream layer may infer grouping membership ad hoc from UI labels or `INDICATOR_DEFS`.

---

## 5. Category / Scope / Window / Family contract

### Primary navigation model

The canonical structured browsing model is:

* `Category → Scope → Window`

with these rules:

* `Category` is the entry point
* `Scope` is optional
* `Window` is a filter that may be applied whether or not Scope is selected
* `Family` is also a filter, not a separate drill-down hierarchy

### Valid Category mode combinations

All of the following must be legal:

* Category only
* Category + Scope
* Category + Window
* Category + Family
* Category + Scope + Window
* Category + Scope + Family
* Category + Window + Family
* Category + Scope + Window + Family

### Filter logic

Within Category mode, filters combine with **AND** logic.

### Grouped family filters

At minimum:

* `MVA`
* `Oscillators`

`MVA` includes:

* SMA
* EMA
* VWMA
* HMA

`Oscillators` includes:

* RSI
* Stoch
* WILL
* CCI
* UO
* MFI
* CMF

### Constraint

Grouped family filters are first-class filter logic, not free-form tags.

---

## 6. Preset contract

### Files

* new preset membership module(s) in `src/ui`

### Preset classes

#### A. Overview presets

These are **explicit curated memberships**:

* ST Overview
* MT Overview
* LT Overview

#### B. Thematic presets

These are **generated from classification rules**:

* ST Trend
* MT Trend
* LT Trend
* ST Momentum
* MT Momentum
* LT Momentum

### Rule

Overview presets must be explicitly defined by row membership.

Thematic presets may be generated from:

* Category
* optional Scope
* Window

### Preset ordering

The v1 preset dropdown order is:

1. ST Overview
2. MT Overview
3. LT Overview
4. ST Trend
5. MT Trend
6. LT Trend
7. ST Momentum
8. MT Momentum
9. LT Momentum

### Constraint

Preset mode must remain a curated selection path. It must not be overloaded with Category-mode filters in v1 unless explicitly expanded later.

---

## 7. Custom set contract

### Files

* new curated-membership module(s) in `src/ui`
* `streamlit_app.py`

### Rule

Custom is a **saved selection set**, not a static conceptual bucket.

It must support:

* add row
* remove row
* reorder row
* restore default custom set

### Source of truth

* default Custom membership lives in the catalog layer
* edited Custom state may live in UI/session state or later persistence, but restore-default must resolve from the catalog definition

### Constraint

Custom must not be derived from Category / Window filters implicitly.

---

## 8. Special-case contracts

### A. VWMA

Canonical home:

* `Trend → Directional Bias`

Secondary tag:

* `Institutional Anchor`

Rule:

* VWMA must not be duplicated structurally into Volume classification
* tag presence does not alter v1 base selection logic unless explicitly used later

### B. OBV

Window:

* `All`

Rule:

* OBV must not be forced into fake ST / MT / LT classification
* when a Window filter is active, `Window = All` rows do not appear unless:

  * explicitly selected
  * or included in a preset / manual override

### Constraint

These special cases must be handled in the selection layer, not by distorting the canonical classification model.

---

## 9. Downstream consumer contract

### Consumers

* `streamlit_app.py`
* `technical.py`
* `rolling_heatmap_adapter.py`

### Rule

Downstream consumers may:

* receive resolved row-key lists
* display those rows
* format those rows
* allow manual refinement of the visible set

Downstream consumers must not:

* redefine category membership
* redefine preset membership
* infer canonical row classification from presentation labels
* create parallel selection logic in multiple places

### Constraint

There must be one authoritative selection-resolution path for row-set construction.

---

## 10. Existing control preservation contract

### Files

* `streamlit_app.py`

### Existing controls that must remain

* Rolling Window control
* Anchor Date control
* Indicators to Display/Remove
* Change Indicator Order
* heatmap rendering path
* Indicator Definitions / Learn More behavior

### Rule

The new selection framework must be inserted **above** the current manual indicator controls.

### Constraint

The new grouping architecture feeds the existing controls; it does not replace their final override role. The current app already contains indicator display/remove and ordering control patterns that must remain the downstream refinement layer. 

---

## 11. File ownership contract

### New files in `src/ui`

Recommended split:

#### `rolling_heatmap_classification.py`

Owns:

* authoritative row classification mapping
* family groups
* tags
* canonical Category / Scope / Window assignments

#### `rolling_heatmap_presets.py`

Owns:

* Custom default membership
* explicit Overview preset memberships
* preset ordering / labels

#### `rolling_heatmap_selection.py`

Owns:

* selection-resolution logic
* Category/Scope/Window/Family filtering
* generated thematic preset resolution
* special-case handling (`Window = All`, grouped family filters)

### Existing files

#### `rolling_heatmap_adapter.py`

Retains ownership of:

* `INDICATOR_DEFS`
* display names
* educational metadata
* hover/display transformation

#### `streamlit_app.py`

Retains ownership of:

* control rendering
* session-state wiring
* passing selected row-key sets into the existing heatmap flow

#### `technical.py`

Retains ownership of:

* runtime payload generation
* row-producing indicator/value/score paths
* no local grouping authority beyond consuming resolved row keys

---

## 12. Guardrails

### Architectural guardrails

* do not compute grouping membership in multiple files
* do not duplicate preset definitions in `streamlit_app.py`
* do not use `INDICATOR_DEFS` as the authoritative grouping source
* do not encode category/scope/window membership in UI labels
* do not reopen rulebook semantics for a UI grouping feature
* do not reopen numeric preprocessor formulas for a UI grouping feature
* do not reopen Scenario B data rules for a UI grouping feature

### Layer guardrails

* numeric truth remains upstream
* semantic truth remains upstream
* selection truth belongs to the new catalog/selection layer
* presentation truth remains in adapter/UI display layers

### Documentation / maintainability guardrails

All new files must include clear module-level docstrings and function/dict comments stating:

* purpose
* scope
* whether the object is authoritative metadata, curated membership, or derived logic

This is required so the source of truth remains understandable later.

---

## 13. Verification checklist

This phase is complete only when the following are true:

### Classification verification

* [ ] every visible rolling-heatmap row has one canonical `row_key`
* [ ] every grouped row has one canonical Category / Scope / Window assignment
* [ ] VWMA has one canonical home plus secondary tag
* [ ] OBV uses `Window = All`

### Custom verification

* [ ] Custom loads a saved/default row set
* [ ] Custom supports add/remove/reorder
* [ ] restore-default resets from the authoritative Custom definition

### Category verification

* [ ] Category-only resolution works
* [ ] Scope filtering works
* [ ] Window filtering works
* [ ] Family filtering works
* [ ] grouped families (`MVA`, `Oscillators`) resolve correctly
* [ ] filters combine with AND logic
* [ ] empty-state behavior is deterministic and friendly

### Preset verification

* [ ] ST/MT/LT Overview presets load explicit curated memberships
* [ ] ST/MT/LT Trend presets resolve correctly
* [ ] ST/MT/LT Momentum presets resolve correctly
* [ ] preset ordering matches the locked v1 order

### Downstream integration verification

* [ ] existing manual display/remove still works after mode resolution
* [ ] existing row ordering still works after mode resolution
* [ ] resolved row-key sets feed the current heatmap path without identity drift
* [ ] `INDICATOR_DEFS` educational/hover behavior remains intact

### Non-regression verification

* [ ] no numeric formulas changed
* [ ] no semantic thresholds changed
* [ ] no Scenario B behavior changed
* [ ] no row identity was changed from `row_key` to display-name-based logic

---

## 14. This phase must not modify

This phase must not modify:

* `indicator_preprocessor.py` numeric formulas
* `master_rules_normalized.json` rule semantics / thresholds
* `signal_classifier.py` semantic evaluation rules
* Scenario B OHLCV acquisition / persistence policy in `technical.py`
* `INDICATOR_DEFS` display/education ownership in `rolling_heatmap_adapter.py`
* the existing role of manual display/remove and ordering controls in `streamlit_app.py`

Any proposed change that crosses those boundaries must be treated as a separate workstream, not silently folded into this one.

---

## 15. Summary rule

This workstream adds a **row-selection architecture**, not a new semantic layer and not a new numeric layer.

Its authoritative flow is:

* catalog metadata + curated memberships
* selection-resolution logic
* resolved row-key set
* existing manual overrides
* existing rolling heatmap render path

That architecture must remain explicit and single-sourced.

# Semantic Layer Contract — Option F — Semantic & Relational Logic (Wave 1)

**Status:** working architecture spec for **Phase II — Option F — Semantic & Relational Logic (Wave 1)**, the **next active workstream**
**Purpose:** define where semantic meaning, thresholds, signal classification, relational logic, and rule-evaluable interpretation belong before implementation begins.  
**Usage:** load this document before any implementation session touching rule semantics, signal meaning, or semantic activation of existing numeric primitives.

---

## 1. Scope and boundary

This contract applies only to the **semantic interpretation layer (Option F)**.

It must preserve the current layer separation:

* `indicator_preprocessor.py` computes base indicator series and derived numeric outputs  
* `signals_loader.py` builds rulebook-driven compute configuration for numeric computation  
* `technical.py` orchestrates runtime execution and packages score/value payloads  
* `signal_classifier.py` and the rulebook apply meaning to existing numeric outputs  
* UI / heatmap layers consume semantic outputs but must not invent semantics locally

This contract must **not** introduce changes to:

* base indicator formulas  
* derived numeric formulas already completed in Option E  
* Scenario B data acquisition logic  
* OHLCV persistence policy  
* UI-only formatting as a substitute for engine semantics  
* Phase IV explanation / rationale behavior  

---

## Phase II Option F Workstream Context

**Active Task:** Option F — Semantic & Relational Logic (Wave 1)  
- **Workstream type**: first-family semantic activation
**Primary Implementation Layer:** rulebook + semantic consumer path  
**Initial target families:**
- Bollinger semantics
- VWMA rule semantics

This contract exists to ensure that semantic interpretation is implemented without modifying:

- Phase I numeric foundations
- Option E numeric primitives
- Scenario B data assembly behavior
- presentation-only layers as the source of truth

All Option F outputs must be:

- derived from existing numeric columns
- evaluated through the rule engine path
- packaged through the existing rolling-score / rolling-payload path
- rendered by the UI without local reinterpretation

---

## 2. Canonical semantic identity source

### Files

* `master_rules_normalized.json`
* `signal_classifier.py`

### Primary semantic identity

Semantic identity is defined by the combination of:

* `engine_indicator`
* `param_key`
* rule block for a feature scope (e.g. `heatmap`)
* resulting signal / score state

### Rule

Semantic meaning is **not** defined by UI labels, hover text, or row names.

Semantic identity comes from the rulebook and its runtime consumer path.

### Examples

* `Bollinger` + `20_2.0` + `heatmap`
* `VWMA` + `20` + `heatmap`
* resulting states:
  * `strong_buy`
  * `buy`
  * `neutral`
  * `sell`
  * `strong_sell`

### Constraint

No downstream layer may independently define, rename, or reinterpret semantic states outside the rulebook / signal-classifier path.

---

## 3. Numeric input contract (upstream dependency)

### Files

* `indicator_preprocessor.py`
* `technical.py`

### Primary function

* `compute_all_indicators(...)`
* `calculate_optionc_indicators(...)`

### Structure

Option F consumes the already-computed indicator dataframe, which contains:

* base indicator columns
* derived numeric columns from Option E
* OHLCV columns where applicable

### Rule

The indicator dataframe remains the **single source of truth** for numeric inputs used by Option F.

### Constraint

Option F must consume numeric columns from the dataframe.  
It must not compute numeric primitives locally in the semantic layer.

---

## 4. Semantic transformation path

### Files

* `master_rules_normalized.json`
* `signal_classifier.py`
* `technical.py`

### Primary components

* `SignalEngine.evaluate(...)`
* `SignalEngine.evaluate_to_scores(...)`
* `SignalEngine._evaluate_rule_block(...)`
* `technical.calculate_rule_engine_signals_optionc(...)`

### Responsibilities

The semantic path is responsible for:

* interpreting existing numeric columns
* applying thresholds / rule logic
* producing signal labels and scores
* ensuring score series exist for the intended indicator families
* passing those scores into rolling payload generation

### Rule

All semantic outputs must be created through the **rulebook → signal-classifier → score-series** path.

### Constraint

No semantic interpretation should be hardcoded outside this pathway.

---

## 5. Rolling payload contract

### File

* `technical.py`

### Functions

* `_get_optionc_meta(...)`
* `_build_optionc_rolling_signals(...)`

### Responsibilities

* align scored families with emitted heatmap rows
* package score / signal / value data into rolling payload cells
* preserve row-coverage parity between engine output and heatmap output

### Rule

If a row is meant to be semantically active in Option F, it must be backed by actual score-series coverage from the rule-engine path.

### Constraint

Preview-only fallback behavior may be used temporarily during onboarding, but must not replace true semantic activation for a target Option F family.

---

## 6. Downstream consumer contract

### Consumers

* rolling payload builder in `technical.py`
* `streamlit_app.py`
* `rolling_heatmap_adapter.py`

### Rule

Downstream consumers:

* may display signals / scores / values
* may format or explain outputs for presentation
* must not alter score meaning
* must not compute derived semantic states
* must not substitute UI-local logic for missing engine semantics

### Constraint

All semantic interpretation must be completed upstream before rendering.

---

## 7. Rulebook variable / binding contract

### Files

* `master_rules_normalized.json`
* `signal_classifier.py`

### Responsibilities

* rulebook variables must resolve to actual dataframe columns or approved bound aliases
* instance-specific families must bind deterministically by `param_key`
* variable naming must remain aligned with numeric layer outputs

### Rule

Semantic activation is only valid if:

- target rule variables resolve correctly
- required numeric inputs exist in the dataframe
- rule blocks can evaluate without hidden UI or adapter dependencies

### Constraint

If a semantic family cannot be bound cleanly to the current dataframe contract, that is a **binding / engine issue**, not a UI problem.

---

## 8. Layer ownership vs responsibility

### Numeric layer (Option E)
Owns:
- numeric primitives
- normalization
- dataframe column creation

### Semantic layer (Option F)
Owns:
- interpretation
- thresholds
- signal classification
- family-level rule meaning
- cross-indicator and relational logic when explicitly activated

### Presentation layer (Phase III UI)
Owns:
- display text
- hover content
- educational context
- formatting
- row ordering / visibility

### Rule

No leakage between layers is allowed.

### Constraint

If meaning is introduced in the UI, or numeric derivation is introduced in the semantic layer, the architecture has drifted.

---

## 9. Option F — Semantic & Relational Logic (Wave 1) scope contract

### Included in Option F Wave 1

* Bollinger semantic activation
* VWMA semantic activation

### Accounted for, but later

* composites
* cross-confirmation
* regime logic

### Deferred outside this wave

* SMA slope / SMA semantic reopen — later numeric backlog / review item
* Phase IV rationale / explanation layer

### Rule

Option F Wave 1 must stay focused on **single-family semantic activation** only.

### Constraint

Do not silently expand into multi-indicator semantics during first-wave family onboarding.

---

## 10. Implementation guardrails

Option F must be implemented without changing:

* base indicator values
* derived numeric formulas already completed in Option E
* Scenario B data acquisition behavior
* persistence policy
* UI adapter ownership
* Phase IV explanation ownership

All Option F work must remain localized to:

* `master_rules_normalized.json`
* `signal_classifier.py`
* `technical.py` (semantic execution + rolling payload alignment)

UI files may only be touched if a **payload transport issue** is proven.

---

## 11. Drift-risk guardrails

### A. Numeric drift
Do not reopen:

* ROC normalization
* ATRP prerequisites
* slope formulas
* Bollinger numeric formulas

unless a missing prerequisite is explicitly proven.

### B. UI-local semantics
Do not solve missing semantic behavior by patching:

* `rolling_heatmap_adapter.py`
* `streamlit_app.py`

### C. Silent scope expansion
Do not introduce:

* composites
* regime logic
* cross-confirmation
* SMA reopen

during Wave 1.

### D. Coverage mismatch
Do not let a family appear semantically “active” in the heatmap unless:

* the rule engine actually emitted score series
* rolling payload row coverage matches the scored family coverage

---

## 12. Verification checklist

Before accepting Option F implementation:

### A. Rulebook / binding verification

* target semantic family exists in `master_rules_normalized.json`
* rule variables resolve to current dataframe columns or approved aliases
* no threshold/unit mismatch remains

### B. Runtime score generation verification

* target family emits score series in `calculate_rule_engine_signals_optionc(...)`
* score series are populated on expected dates
* no hidden `skip_errors` path is masking a failed semantic activation

### C. Rolling payload verification

* `_get_optionc_meta(...)` row coverage matches semantic score coverage
* `_build_optionc_rolling_signals(...)` packages score-backed cells for active families
* preview-only fallback is not carrying long-term semantic rows

### D. UI verification

* row appears in heatmap
* displayed value matches dataframe truth
* shading matches engine score output
* hover remains presentation-only and does not invent meaning

### E. Regression verification

* Option E numeric columns remain unchanged
* non-target semantic families do not drift
* Scenario B remains unchanged
* no persistence behavior is introduced

---

## 13. Minimum acceptance checklist

Before accepting Option F Wave 1:

* first-wave target families emit real engine-native score series
* target rows are no longer dependent on preview-only fallback behavior
* numeric inputs remain unchanged from the current stabilized post-Option E state
* no UI-local semantics were introduced
* no later-wave semantic families were activated implicitly

---

## 14. One-sentence working summary

The Semantic Layer architecture is:

* **numeric truth defined upstream in `compute_all_indicators(...)`**
* **semantic meaning defined in `master_rules_normalized.json`**
* **evaluated by `signal_classifier.py`**
* **packaged by `technical.py`**
* **rendered by the UI without reinterpretation**
```

This follows the same template structure as the Option E contract and keeps the same architectural separation, just shifted from numeric ownership to semantic ownership.

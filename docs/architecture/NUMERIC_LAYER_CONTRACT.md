# Numeric Layer Contract — Option E (Derived Numeric Primitives)
Version: 1.1
Created: 4/11/26
Last Update: 4/11/26 

**Authoritative Reference:** must be loaded and enforced during all Option E implementation sessions.

**Status:** working architecture spec for Phase II Option E (numeric derivation layer)  
**Purpose:** define where numeric series, derived numeric primitives, normalization logic, and rule-consumable fields belong before implementation begins.  
**Usage:** load this document before any implementation session touching indicator computation or derived numeric outputs.

---

## 1. Scope and boundary

This contract applies only to the **numeric computation layer (Option E)**.

It must preserve the current layer separation:

* `indicator_preprocessor.py` computes base indicator series and derived numeric outputs  
* `signals_loader.py` builds rulebook-driven compute configuration  
* `technical.py` orchestrates runtime execution and returns the final indicator dataframe  
* rule engine consumes numeric outputs without modifying them  

This contract must **not** introduce changes to:

* rule thresholds  
* signal scoring semantics  
* UI / heatmap / hover behavior  
* Scenario B data acquisition logic  
* OHLCV persistence policy  

---

## Phase II Option E Workstream Context

**Active Task:** Derived Numeric Primitives (Wave 1 — slope stabilization + numeric correctness)  
**Primary Implementation Layer:** `indicator_preprocessor.py`  
**Supporting Configuration Layer:** `signals_loader.py`  

This contract exists to ensure that numeric derivations are implemented without modifying:

- base indicator computation (Phase I outputs)
- rule semantics or scoring behavior (Phase II)
- rolling payload or UI adapter behavior (Phase III)
- Scenario B data assembly behavior

All derived numeric outputs must be:

- computed in the preprocessor layer
- passed forward through the existing dataframe
- consumed by the rule engine without reinterpretation

---

## 2. Canonical column identity source

### File

* `indicator_preprocessor.py`

### Function

* `compute_all_indicators(...)`

### Authoritative fields

Each numeric series (base or derived) is represented as a dataframe column.

### Rule

Column names are the canonical identity for numeric series.

Examples:

* `EMA_20`
* `HMA_21`
* `RSI_14`
* `ROC_12`
* `ATR_14`
* `ATRP_14`
* `EMA_20_slope`
* `VWMA_slope`
* `BB_PCT_B`
* `BB_BW`

### Constraint

No downstream layer may rename or reinterpret columns independently of the preprocessor.

---

## 3. Indicator dataframe contract (backend)

### File

* `technical.py`

### Function

* `calculate_optionc_indicators(...)`

### Structure

The indicator dataframe returned from the computation pipeline contains:

* base indicator columns
* derived numeric columns (Option E)
* OHLCV columns (where applicable)

### Rule

The dataframe is the **single source of truth** for all numeric values used by:

- rule engine
- rolling payload builder
- downstream UI layers

### Constraint

All Option E enhancements must extend this dataframe, not bypass it.

---

## 4. Preprocessor contract (numeric transformation)

### File

* `indicator_preprocessor.py`

### Primary components

* `compute_all_indicators(...)`
* `_rolling_linreg_slope(...)`

### Responsibilities

The preprocessor is responsible for:

* base indicator computation
* derived numeric primitive generation
* normalization logic
* column naming consistency

### Rule

All derived numeric outputs must be created inside the preprocessor.

---

## 5. Compute configuration contract

### File

* `signals_loader.py`

### Function

* `build_compute_config(...)`

### Responsibilities

* translate rulebook requirements into compute config
* define slope parameters
* define normalization requirements
* ensure required prerequisites (e.g., ATRP) are included

### Rule

The compute config is the only mechanism by which:

- rulebook requirements influence numeric computation

### Constraint

No derived numeric logic should be hardcoded outside this pathway.

---

## 6. Derived numeric column contract

### Definition

Derived numeric columns are:

- computed from base indicators
- additive to the dataframe
- consumed by rule logic

### Examples

* `EMA_20_slope`
* `HMA_21_slope`
* `VWMA_slope`
* `BB_PCT_B`
* `BB_BW`

### Rule

Derived columns must:

- be additive only
- not overwrite base columns
- not introduce semantic meaning

---

## 7. Numeric correctness and normalization rules

### A. Unit consistency

All numeric outputs must have consistent units.

Example:
- ROC must be globally consistent (fraction vs percent)

### B. Volatility normalization

Derived outputs using ATR/ATRP must:

- use consistent lookback
- align with rulebook expectations

### Rule

All normalization must be:

- explicit
- consistent across indicators
- validated before downstream use

---

## 8. Rule engine consumption contract

### Consumer

* rule evaluation system (`signal_classifier.py`, DSL execution)

### Rule

The rule engine:

- consumes numeric columns
- must not modify numeric values
- must not compute derived columns itself

### Constraint

All numeric derivations must be completed upstream.

---

## 9. Layer ownership vs responsibility

### Numeric layer (Option E)
Owns:
- derived numeric primitives
- normalization
- column creation

### Semantic layer (Option F)
Owns:
- interpretation
- thresholds
- signal classification

### Rule

No leakage between layers is allowed.

---

## 10. Implementation guardrails

Option E must be implemented without changing:

* base indicator values
* rule semantics
* signal classification outputs
* Scenario B data acquisition behavior

All work must remain localized to:

* `indicator_preprocessor.py`
* `signals_loader.py`

---

## 11. Minimum verification checklist

Before accepting Option E implementation:

* base indicator columns match baseline exactly
* derived columns are present and correctly named
* no existing columns changed
* rule engine behavior unchanged (unless explicitly intended)
* no new persistence introduced

---

## 12. One-sentence working summary

The Numeric Layer architecture is:

* **columns defined in `compute_all_indicators(...)`**
* **configuration driven by `build_compute_config(...)`**
* **execution orchestrated by `technical.py`**
* **consumed by rule engine without modificati
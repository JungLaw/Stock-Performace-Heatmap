# Master Checklist (Authoritative) — Phase 3  
**TA Rule Engine (GPT)**  
**Created**: 12/23/25
**last update**: 4/22/26   
**Version**: 1.8  

---
## Change Log

### v1.8 — 4/22/26
- Option F Wave 1 marked COMPLETE
- Completed Option F Wave 1 scope recorded as:
  - Bollinger semantic activation
  - VWMA rule semantics
- Deferred semantic tiers explicitly carried forward unchanged:
  - composites
  - cross-confirmation
  - regime logic
- SMA retained as later numeric backlog / review item
- No next active workstream assigned in this retrospective pass

### v1.7 — 4/16/26
- Next active workstream updated to Option F Wave 1
- Option F Wave 1 scope locked to:
  - Bollinger semantic activation
  - VWMA rule semantics
- Later semantic tiers explicitly carried forward:
  - composites
  - cross-confirmation
  - regime logic
- SMA retained as later numeric backlog / review item
- Option D routing role clarified as completed governance / inventory work

### v1.6 — 4/15/26
- Option E Wave 1 marked COMPLETE
- EMA / HMA / VWMA slope primitives stabilized
- ROC normalization resolved to fractional-unit numeric truth
- ATRP / volatility-normalization validation completed
- Bollinger numeric outputs implemented:
  - `BB_PCT_B`
  - `BB_BW`
- Frozen-baseline validation completed for Option E Wave 1 core work

### v1.4 — 3/13/26
- Scenario B marked COMPLETE after validation
- Historical buffer updated from 386 → 435 calendar days
- Added Phase III UX refinement workstream
- Added Rolling Heatmap hover enrichment milestone

### v1.3 — 2/16/26
- Scenario B data plumbing implementation documented
- DB-first missing-range acquisition rules finalized

**Current Active Workstream:** Option F — Semantic & Relational Logic (Wave 1)


---

## Phase 3 Checkpoint Summary

| Option B     | Complete                        |
| Option C     | Complete                        |
| Scenario B   | **Complete**                    |
| Option D     | Complete (routing-only)         |
| Phase III UX | **Complete**                    |
| Option E     | **Wave 1 Complete**             |
| Option F     | **Wave 1 Complete**             |

**Status**: Scenario B complete and validated; Phase III UX complete and closed; Option E Wave 1 complete; Option F Wave 1 complete

**Recently completed**:
- Option B — Core indicator families
- Option C — Rolling rule-engine integration
- Scenario B — DB-first OHLCV stabilization (stabilization validated)
- Phase III UX — hover enrichment, educational expander, and Learn More system
- Option E Wave 1 — derived numeric primitives:
  - EMA / HMA / VWMA slope primitives
  - ROC normalization
  - ATRP validation
  - `BB_PCT_B`
  - `BB_BW`
  - baseline validation pass
- Option F Wave 1 — first-family semantic activation:
  - Bollinger semantic activation
  - VWMA rule semantics

**Deferred beyond completed Option F Wave 1:**
- composites
- cross-confirmation
- regime logic

**Deferred outside current semantic wave:**
- SMA slope (later numeric backlog / review item)

---
## Continuity & Scope Enforcement

All phases and options are governed by:
- `constraints_chatgpt.md`
- Explicit deferrals and exclusions carry forward automatically
- New phases do not reset scope unless explicitly stated

---

## Phase 3 — Purpose

Phase 3 is responsible for integrating the **rulebook (JSON)** with the **runtime rule engine**, producing:

- normalized indicator values,
- discrete signals + scores,
- rolling heatmap–compatible outputs,
- stable DB-first OHLCV assembly (Scenario B),
- with extensibility for future indicator families.

Phase 3 remains **backend-first** with UI work strictly consuming engine outputs.

---

## Phase 3 Structure

Phase 3 is divided into **indicator option groups and data-layer stabilization tracks**, executed according to dependency order:

| Track        | Purpose                             | Status       |
| ------------ | ----------------------------------- | ------------ |
| Option B     | Core oscillator & volume / ERI-style indicators | Complete     |
| Option C     | Rolling heatmap engine integration & runtime orchestration  | Complete     |
| Scenario B   | Data acquisition: DB-first OHLCV stabilization (Data authority & missing-range stabilization)     | **Complete** |
| Option D     | Derived / slope / band indicators (inventory / routing) | Complete     |
| Phase III UX | Rolling heatmap interaction layer   | Complete     |
| Option E     | Derived numeric primitives          | Wave 1 Complete |
| Option F     | Rule semantics / relational logic   | Wave 1 Defined / Pending |

---
## Option F — Completed Workstream (Wave 1)

Option F owns **semantic interpretation / relational logic**. Wave 1 is now complete as the first-family semantic activation workstream following Option E Wave 1 completion.

### Option F Wave 1 completed scope
- [x] Bollinger semantic activation
- [x] VWMA rule semantics

### Deferred beyond completed Option F Wave 1
- [ ] composites
- [ ] cross-confirmation
- [ ] regime logic

### Deferred outside current semantic wave
- [ ] SMA slope
  - remains a later numeric backlog / review item
  - not a first-wave Option F target

### Guardrails carried forward
- [x] consumed existing numeric dataframe outputs
- [x] did not reopen Option E numeric formulas unless a missing prerequisite was proven
- [x] did not implement semantics in UI / adapter layers as the semantic source of truth
- [x] kept first-wave work at the single-family semantic level

---

## Scenario B — Data Acquisition Stabilization

Scenario B governs how OHLCV data is assembled for runtime computation.

**Purpose:**  
Stabilize Rolling Heatmap data retrieval using a DB-first, missing-range strategy without altering numeric semantics, rule logic, or persistence authority.

Scenario B corrected **data-layer plumbing**, not indicator semantics.


### Authority Rules (Locked)

1. `daily_prices` database is authoritative on overlaps.
2. yfinance is used only to fill missing head, tail, or interior gaps.
3. Overlapping rows must never overwrite existing DB rows.
4. Technical Analysis must not persist OHLCV.
5. Pivot Points must not persist OHLCV.
6. Only Performance layer may write to `daily_prices`.


### Assembly Requirements

- DB coverage must be checked first.
- Missing date ranges must be identified deterministically.
- Historical buffer = 435 calendar days (to safely support 200-day MA lookbacks and indicator warmup periods (and possible 300-day MVA inclusion).
- Final OHLCV frame must be:
  - continuous
  - sorted
  - duplicate-free
  - timezone-normalized
  - forward-compatible with indicator pipeline

### Deep Anchor Requirement

Rolling heatmap must support anchors prior to 10/16/23.

Indicators must compute correctly if sufficient historical DB data exists.

### Verification Criteria

- DB-only case: no yfinance call.
- Head-gap case: only head fetched.
- Tail-gap case: only tail fetched.
- Interior-gap case: only gap fetched.
- Overlap case: DB rows preserved.
- No implicit persistence during TA execution.

---

### Scenario B Completion Gate

Scenario B is complete only when:

1. Deep historical anchors render correctly
2. Indicators are stable across long history
3. No persistence leakage exists
4. No semantic changes were introduced

Only after this gate may Option E / Option F work resume.

#### Scenario B Status
**COMPLETE — validated**

Scenario B was validated through the following tests:

- as-of run on well-covered ticker
- deep-anchor run on partial-history ticker
- no-DB-history run (yfinance-only path)
- missing-range detection logging confirmed
- DB precedence confirmed on overlap
- no implicit persistence from TA layer


Validation confirmed:

- DB-first coverage detection is stable
- deep historical anchors render correctly
- indicator pipelines operate on long-history datasets
- TA execution does not persist OHLCV to `daily_prices`
- missing-range fetch logic functions correctly

Completion confirmed **2/16/26**.

---

## ✅ OPTION B — Core Indicator Families (COMPLETE)

### Scope (What Option B Covers)
Indicators that emit primary numeric values mapped directly to signals.

Option B covers **raw indicator families** that:
- emit a primary numeric value,
- map cleanly to buy/sell/neutral scoring,
- do not require multi-stage derivations.

Included families:
- RSI
- MACD
- Stochastic
- ROC
- Williams %R
- ADX
- MFI
- CMF
- OBV
- Bull / Bear Power (ERI-style)

---

### B1 — Rulebook Coverage

- [x] All Option B indicators enumerated in `master_rules_normalized.json`
- [x] Each indicator has:
  - `engine_indicator`
  - `display_key`
  - scoring thresholds
- [x] BullBearPower represented as **score-first**, with extras carried separately
- [x] No slope, ATRP, or band logic included

---

### B2 — Indicator Preprocessing

- [x] `indicator_preprocessor.py` emits numeric series for:
  - RSI (multiple periods)
  - MACD (multiple parameterizations)
  - Stochastic (multiple windows)
  - ROC
  - Williams %R
  - ADX
  - MFI
  - CMF
  - OBV
  - BullPower / BearPower / BBP composite
- [x] Canonical price selection enforced (`Adj Close` preferred)
- [x] Volume-based indicators normalized for intraday safety
- [x] All outputs numeric and NaN-safe

---

### B3 — Signal Classification & Engine

- [x] `signal_classifier.py` correctly maps values → discrete signals
- [x] Scoring consistent with rulebook thresholds
- [x] No implicit alias injection required for Option B
- [x] No composite scoring beyond defined thresholds

---

### B4 — Rolling Engine Integration

- [x] Option B indicators appear in rolling payload
- [x] `value_col` made optional and non-breaking
- [x] Missing values handled gracefully
- [x] `extras` field supported per-cell (BullBearPower)

---

### B5 — Database & Data Integrity (Completed During Option B)

- [x] Idempotent OHLCV inserts implemented (`INSERT OR IGNORE`)
- [x] Column order stabilized for DB writes
- [x] Timezone / date normalization corrected
- [x] Session-only vs DB-backed paths validated
- [x] New ticker ingestion smoke-tested

---

### B6 — Debugging & Validation

- [x] Rolling payload verified via debug headers
- [x] DB-backed vs non-DB-backed parity confirmed
- [x] Indicator family coverage aligned between:
  - rulebook (`optionc_meta`)
  - runtime scores (`scores`)
- [ ] Debug statements to be removed (explicitly deferred)

---

### B7 — Explicit Non-Goals (Confirmed)

The following are **not** part of Option B and are intentionally deferred:

- Slopes / derivatives
- ATRP normalization
- Band logic (Bollinger, Keltner, etc.)
- Multi-indicator composites
- UI / Plotly rendering decisions

---

## OPTION C — Rolling Heatmap Engine (COMPLETE)

Option C integrated rule-engine outputs with rolling time-window evaluation
to power the Rolling Signals Heatmap.

Responsibilities included:

- rolling indicator evaluation across time windows
- score normalization (-2 … +2)
- heatmap-ready payload generation
- adapter compatibility for UI consumption

Core components involved:

- `technical.py`
- `indicator_preprocessor.py`
- `signal_classifier.py`
- `rolling_heatmap_adapter.py`

Option C introduced no new indicator semantics and relied entirely
on Option B indicator outputs and the rulebook definitions.


---
## OPTION D — Derived & Composite Indicators 
Note: Option D remains deferred until Scenario B completion and explicit reopening (Deferred to Option E/F). 

Option D was intended to build **on top of Option B outputs** and introduce:
- slope / rate-of-change on indicators,
- normalized derivatives (e.g., ATRP),
- band-based logic,
- multi-stage rule evaluation.

Option D is split into phases, starting with **inventory and classification**.


- Phase 1 (Rulebook Inventory): ✅ COMPLETE — closed with no in-scope indicators
- All Option D-adjacent rule families deferred to Option E / Option F

**Deferred (NOT Option D Phase 1 work):**
* [ ] Slopes → Option E
* [ ] Band positioning → Option F
* [ ] Composite context features → Option F

➡️ **Reference:** option_d_phase1_inventory.md

---
## Option E / Option F Reopening Rule

Work on Option E or Option F may resume only after Phase III UX work
is explicitly closed.

**Reopening Status:** ✅ SATISFIED

Evidence:
- Phase III UX declared complete
- `baseline/indicator_baseline_AAPL_phase3_baseline.csv` created
- `master_rules_normalized__phase3_baseline.json` created
- Option E Wave 1 completed and baseline-validated

### Current interpretation

- Option E Wave 1 is complete
- Option F Wave 1 is now authorized as the next active workstream
- Later semantic tiers remain deferred until first-wave semantic families are stable

---

## Option E — Wave 1 Complete

Objective:
Introduce derived numeric indicators without altering baseline computations.

Rules:
- No modification to existing indicator values except for explicitly approved
  numeric normalization corrections
- No rule semantics introduced
- Derived fields must be additive only

Wave 1 completed:
- [x] Derived indicator family defined
- [x] Computation implemented
- [x] Naming aligned
- [x] Integrated into compute path
- [x] Verified against baseline (no drift beyond approved ROC normalization)
- [x] Added to UI where explicitly approved for display-only preview

Wave 1 completed scope:
- EMA / HMA / VWMA slope primitives
- ROC normalization
- ATRP validation
- `BB_PCT_B`
- `BB_BW`

### Option E — Indicator Numeric Semantics
Applies to:
- indicator computation formulas
- numeric normalization (e.g., ROC unit alignment)
- lookback / warmup adjustments
- parameter harmonization

Option E may modify **numeric indicator outputs** but must not alter
rule interpretation.

### Option F — Rule Semantics
Applies to:
- rule thresholds
- scoring interpretation
- composite signals
- multi-indicator logic

Option F modifies **signal meaning and scoring behavior**.

**Reopening Status:** ✅ SATISFIED

Evidence:
- Phase III UX declared complete
- `baseline/indicator_baseline_AAPL_phase3_baseline.csv` created
- `master_rules_normalized__phase3_baseline.json` created


---
## Phase III — Rolling Heatmap UX Refinement
Purpose:
- Improve interpretability and usability of the rolling heatmap
- without modifying indicator semantics or rule-engine scoring.

Phase III UX work operates strictly within the UI adapter layer.



**Status:** ✅ COMPLETE (Closed)

Completion summary:
- Hover enrichment implemented and validated
- Indicator definition panel implemented
- Learn More markdown system implemented
- UI behavior verified without semantic drift

---

### Current UX Objectives

1) Hover enrichment
   - display value, signal score, and rule explanation
   - include contextual interpretation for indicators

2) Indicator definition panel
   - allow users to view indicator explanation and parameters

3) Row grouping
   - group indicators by category (momentum, trend, volume)

4) Indicator category toggles
   - allow users to filter indicator families

### Architecture Constraint

UI improvements must not modify:

- indicator computation
- rule engine thresholds
- scoring semantics
- rolling payload contract

All interpretation text must originate from metadata
exposed through the rolling_heatmap_adapter layer
rather than being constructed inside the UI.




---


## Canonical Design Rules (Phase 3)

- Rulebook is authoritative
- Preprocessor emits facts, not opinions
- Classifier maps facts → signals
- Engine orchestrates, never infers
- Data-layer plumbing changes (e.g., Scenario B) must not alter numeric semantics or rule thresholds
- Heatmap payload must remain forward-compatible
- Data assembly must be deterministic and persistence-safe (Scenario B)


---

## 8) Documentation / consolidation (Defer until after B + Derived)
- [ ] Consolidate configs/docs after Options B and Derived are complete (avoid churn)
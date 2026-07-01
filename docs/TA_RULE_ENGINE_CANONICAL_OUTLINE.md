# TA Rule Engine Project — Canonical End-to-End Outline
- Version: 3.3.1
- Created: 1/12/26
- Last update: 6/30/2026

**(Authoritative, Corrected, Chronological, Single Source)**

---

## MAJOR PHASE I — Core Data & Indicator Foundation (Numbers)

**Goal:** Produce stable, correct, and reproducible indicator time series with canonical naming, predictable dtypes, and known numerical semantics.

### 1. Data acquisition & normalization

* OHLCV retrieval (daily semantics)
* Trading-calendar correctness (“last completed trading day” logic)
* DB caching with deterministic fallback (yfinance) **under explicit policies**:
  - **TA dashboards:** session-only by default unless user opts in
  - **Rolling Heatmap Scenario B:** DB-first + missing-range fetch; DB wins overlaps; no default persistence
* Canonical index alignment and dtype normalization

### 2. Option A — Baseline indicators (price-driven)

* RSI, ROC, Williams %R, Stochastic
* Canonical column naming
* No rule semantics yet; numeric correctness only

### 3. Option B — Volume-aware indicators

* MFI, CMF, OBV
* Explicit daily-volume assumptions
* Guardrails for intraday usage
* Local implementations where third-party libraries prove unstable

### 4. Option C — Expanded indicator inventory

* EMA, HMA, ADX, CCI, Ultimate Oscillator (multi-parameter families)
* Parameter-instance normalization (e.g., `UO_7_14_28`)
* `indicator_preprocessor.py` as the canonical computation wrapper


**Canonically named Bollinger-derived outputs**

The following Bollinger-derived numeric outputs are canonically named and now
computed in the numeric layer:

- Bollinger %B → `BB_PCT_B`
- Bollinger Bandwidth → `BB_BW`

**Status:**
- Naming is locked to prevent future churn.
- Numeric computation is complete in **Option E Wave 1**.
- Semantic interpretation remains deferred to:
  - Option F (band-position semantics)


### 5. Required detour — pandas dtype & stability fixes

**Why it mattered:** pandas-ta and legacy dtype assumptions caused silent corruption and FutureWarnings that became runtime failures.

* Stable float64 enforcement for volume series
* Removal / replacement of fragile third-party paths
* Elimination of dtype mutation warnings that break Streamlit runs

**Status:**
✅ Phase I is **complete**.
Known non-blocking issues: pandas fragmentation/performance warnings.

---

## MAJOR PHASE II — Signal & Rule Infrastructure (Meaning / Scoring)

**Goal:** Convert numeric indicator outputs into consistent, rule-evaluable signals and rolling scores.

### 6. Rulebook ingestion & normalization

* `master_rules_normalized.json`
* Deterministic rule loading & validation
* Scope-aware rule segmentation (heatmap / overlay / alerts)

### 7. Option D — Rule inventory & scope locking

* Indicator families enumerated
* Explicit scope definitions
* Deferred semantics documented (no silent expansion)

**Status:** ✅ Completed earlier

### 8. Rule execution engine

* Expression engine (DSL)
* Signal classifier (`-2 .. +2`)
* Rolling-window score packaging
* Instance binding for multi-parameter indicators (e.g., UO)


**Rule-evaluation correctness checkpoint — ROC unit normalization**
- ROC_* numeric series must match the thresholds defined in
  `master_rules_normalized.json`.

**Resolved decision (authoritative):**
- ROC series are normalized to **fractional units** in the numeric layer:
  - `ROC = ROC / 100`
- Rule thresholds remain expressed in fractional units.
- Mixed-unit handling is prohibited.

**Status:**
- ROC normalization completed in **Option E Wave 1**.
- Heatmap display may format ROC in percent-point style for readability,
  but numeric truth remains fractional upstream.

**Acceptance criteria:**
- ROC_12 / ROC_20 signals transition correctly across
  neutral / buy / sell boundaries when replayed against historical data.

### 9. Option E — Derived numeric primitives (**NOT semantics**)

**Purpose:** Provide reusable numeric transforms that other layers depend on.

Examples:
* Slopes (EMA/HMA/ADX)
* Deltas / ROC-of-indicators
* Volatility normalization
* Distance-to-band (numeric only)

> ⚠️ Important boundary:
> Option E produces **numbers**, not interpretations.

---
**Status:** ✅ WAVE 1 COMPLETE

**Constraints (authoritative):**
- MUST NOT modify existing indicator values except for explicitly approved
  numeric normalization corrections
- MUST NOT introduce rule semantics
- MUST remain computation-layer only

**Validation requirement:**
- All derived outputs must be validated against:
  - `baseline/indicator_baseline_AAPL_phase3_baseline.csv`

**Wave 1 completed scope:**
- EMA / HMA / VWMA slope primitives
- ROC normalization to fractional units
- ATRP / volatility-normalization validation
- Bollinger-derived numeric outputs:
  - `BB_PCT_B`
  - `BB_BW`

**Still deferred beyond Wave 1:**
- SMA slope
- Option F semantic activation, beginning with:
  - Bollinger semantics
  - VWMA rule semantics
- later semantic tiers:
  - composites
  - cross-confirmation
  - regime logic

---
#### Option E Task Class — Numeric Deviation & Normalization (Explicit)

**Definition (Option E):** Numeric deviation work defines or corrects **pure numeric transforms** such as units, scaling, normalization, and derived series. It must not introduce buy/sell meaning or thresholds beyond unit alignment.

Numeric deviation tasks may be initiated by UI discrepancies or rule-evaluation mismatches but must be resolved entirely within Option E before any semantic interpretation occurs.

**In-scope examples (Option E):**
- Unit normalization (percent vs fractional, basis points vs percent points)
- Derived numeric series (slopes, deltas, ratios, z-scores)
- Band-derived numeric series (e.g., Bollinger %B and bandwidth)
- Numeric distance-to-band series (raw and normalized)
- Volatility normalization primitives (numeric only)

**Out of scope (Option E):**
- Any semantic interpretation of numeric values (belongs to Option F)
- Any UI formatting or display-only transforms (belongs to Phase III)

Implementation of Option E must conform to the
"Numeric Layer Contract"
(NUMERIC_LAYER_CONTRACT.md),
which defines column identity, derived numeric outputs,
normalization rules, and separation from semantic interpretation.

### 10. Option F — Semantic & relational logic

**Purpose:** Interpret numbers.

Examples:

* Band position meaning
* Cross-confirmation logic
* Regime classification
* Composite signals

**Status:** ✅ WAVE 1 COMPLETE

**Wave 1 completed scope (authoritative):**
* Bollinger semantic activation
* VWMA rule semantics

**Wave 1 boundary (preserved):**
* Option F consumed existing numeric primitives from the indicator dataframe
* semantic meaning was created through the rulebook / signal-classifier path
* UI layers may display semantic outputs but must not invent semantics locally

**Deferred beyond completed Wave 1:**
* composites
* cross-confirmation
* regime logic

**Deferred outside Option F Wave 1:**
* SMA slope / SMA semantic reopen
  - remains a later numeric backlog / review item, not a first-wave semantic target

---
#### Option F Sequencing (authoritative)

Option F proceeds in semantic tiers:

**Wave 1 — single-family semantic activation**
- Bollinger semantics
- VWMA semantics
- **Status: complete**

**Wave 2 — multi-indicator semantics**
- composites
- cross-confirmation

**Wave 3 — higher-order context**
- regime logic

This sequencing exists to prevent higher-order semantic work from being introduced before family-level semantic outputs are stable.

---

## MAJOR PHASE III — Visualization & Interaction Layer (UI)
Implementation of the Rolling Heatmap UX layer must conform to the
"Rolling Heatmap Row Architecture Contract" (ROLLING_HEATMAP_ROW_ARCHITECTURE.md),
which defines row identity, payload mapping, adapter transformation, and UI responsibilities.

**Goal:** Make engine outputs visible, explorable, and trustworthy **without redefining the math**.

### 11. Rolling signal heatmap (primary UI driver)

* Rule-engine rolling scores
* Indicator-instance rows
* Time-indexed columns
* Stable adapter contract
* Group selection (custom tickers, ETFs, etc.)

---
#### Rolling Heatmap Data Acquisition Milestone — Scenario B (DB-first missing-range fetch)
(Added: 2/14/26)
**Goal:** Allow anchors prior to current DB coverage (e.g., pre 10/16/23) by fetching **only missing ranges**, while treating DB as authoritative on overlaps.

**Rules (authoritative):**
- **DB-first:** use `daily_prices` when coverage exists.
- **Missing-range fetch:** fetch only gaps (head/tail/interior) from yfinance.
- **Overlap resolution:** DB wins whenever dates collide (“DB keeps its seat”).
- **Persistence policy:** Rolling Heatmap must **not** write to `daily_prices` by default; fetched data is session-only unless an explicit save workflow is triggered.

**Buffer policy (revised):**
- Anchor-relative buffer = **435 calendar days**.

**Rationale:**
- Maintains coverage for ≥200-trading-day indicators.
- Provides sufficient headroom for potential future indicators
  such as a **300-day moving average** without requiring a
  new acquisition policy change.

The buffer remains **anchor-relative** and applies only to the Rolling Heatmap Scenario B acquisition path.

**Policy lock (important):**
The 435-day buffer replaces the earlier 386-day policy used during initial Scenario B design. Future revisions must **not revert to 386** unless the indicator inventory is formally reduced below the current requirements.

**Acceptance criteria:**
- Deep anchor dates (e.g., 2018/2019) render full rolling heatmap with populated indicators.
- For tickers with historical DB coverage (e.g., META 2018–2020), indicator series must reflect full merged history and must not silently truncate to recent DB segments (e.g., 2023-10-18).
- Dataset merge logic must ensure:
  - final `df_ind.index.min()` ≤ (anchor_date − 435 days)
  - no interior gaps remain after DB + yfinance merge
- No new tickers are persisted to `daily_prices` from Rolling Heatmap by default.
- For DB-backed tickers, yfinance is only called when DB coverage is missing.

---
#### **Rolling Heatmap UX Milestone — Layout & Semantics (UI-only)**

**Must-haves (Phase III, blocking for usability):**
- Dates rendered at the **top** of the heatmap.
- Date format normalized to `M/D` (e.g., `12/24 … 1/7`).
- Add a **Price row** directly under dates:
  - Row label = ticker symbol (fallback: `Price`)
  - Cell format = `$X,XXX.XX`
  - Price source must be the same canonical close series used by indicators.
- Enforce consistent column widths across all dates.
- Persist indicator row order across reruns
  (no forced re-selection to preserve ordering).

**Nice-to-haves (Phase III, explicitly optional):**
- Hover enrichment for Price row:
  - absolute change vs prior day
  - % change vs prior day
  - raw volume
  - volume vs trailing average
- Optional date-range selector:
  - user chooses start date
  - heatmap renders next *N* completed trading days
  - must not introduce new rule semantics.

**Heatmap UI Guardrail (Authoritative)**
The Rolling Heatmap UI layer may control:
- ordering, grouping, labels, tooltips, legends, and display-only rows

The Rolling Heatmap UI layer must **not**:
- alter rule thresholds or score meanings
- reinterpret indicator semantics locally
- introduce UI-specific logic into the rule engine or indicator engine

Any issue discovered through UI usage must be routed to:
- Phase II / Option E (numeric derivation), or
- Phase II / Option F (semantic interpretation),
not patched inside the UI layer.

#### Hover Enrichment — Tooltip Context (UI-only)

**Purpose:** Improve interpretability of heatmap cells by surfacing contextual data in hover tooltips.

Hover enrichment is **presentation-only** and must not alter rule semantics,
indicator computation, or signal classification.

**Price row hover content**
Display the following contextual metrics derived from the canonical price series:

- Δ vs prior day
- % change vs prior day
- Volume
- Volume vs 5-day average (show both relative delta and the 5-day average value)

Example:

Δ vs prior day: +4.81  
% change: +0.99%  
Volume: 18.2M  
Volume vs 5D Avg: +11.7% (16.3M)

**Indicator row hover content**

Tooltips must include contextual information derived from the indicator series
and rule engine outputs.

Display:

- Value (2 decimal places)
- Δ vs prior day (absolute and relative)
- Trend (Rising / Falling / Flat based on prior-day comparison)
- Signal (existing rule-engine signal classification)
- Rule (rulebook-authored explanation text when available)

Example:

Value: 62.34  
Δ vs prior day: +1.85 (+3.06%)  
Trend: Rising  
Signal: Buy (+1)  
Rule: RSI above 60 momentum threshold

**Guardrails**

Hover enrichment must:

- use existing indicator values and rule-engine outputs
- remain strictly UI/presentation logic
- never modify rule thresholds, indicator computation, or signal meaning

If interpretability gaps are discovered, they must be routed to:

- Option E — numeric derivations
- Option F — semantic rule interpretation

### 12. Technical Analysis dashboard (tiles)

* Secondary view
* Feature-flag controlled
* Must not mutate rule semantics

### **Formal Feedback Loop (Governed)**

UI is allowed to:

* Reveal missing numeric primitives
* Expose naming or binding gaps
* Surface usability constraints

UI is **not** allowed to:

* Invent semantics
* Patch numeric logic locally
* Diverge from engine outputs

Any gap discovered becomes:

* Option E task (numeric)
* or Option F task (semantic)

**Status:**
✅ Phase III is **complete (closed)**.
Rolling heatmap core is functional and validated.

✅ Step 1 complete — TA persistence policy fixed (no TA writes to `daily_prices` when save_to_db=False).
✅ Pivot Points date-normalization bug fixed (restored pivot table display).
✅ Fingerprinting instrumentation used for runtime path proof; later removed after verification.
✅ Hover enrichment implemented and validated (value, deltas, rule text, notes).
✅ Educational expander implemented (row-stable `INDICATOR_DEFS` content).
✅ Learn More system implemented (family-level markdown via `docs/indicators/`).
✅ UI contract integrity verified (selection sync, ordering, no regressions).

**Closure constraints (verified):**
- No changes to rule semantics
- No changes to indicator computation
- No changes to Scenario B acquisition or persistence behavior
- All UX enhancements are additive and contract-safe

---
#### Phase III Extension — Rolling Heatmap Selection & Catalog Architecture (v1)

**Status:** ✅ COMPLETE

**Purpose:**  
Introduce a row-selection / grouping architecture for the Rolling Signals Heatmap without redefining numeric truth, semantic meaning, or adapter-owned presentation metadata.

**Completed scope:**
- authoritative row classification catalog
- curated Custom default membership
- explicit ST / MT / LT Overview preset membership
- generated thematic preset resolution
- `Custom` / `Category` / `Preset` selection modes
- `Category → Scope → Window` browsing model
- optional `Family` filter, including grouped-family filters such as `MVA` and `Oscillators`
- manual `Indicators to display/remove` override preserved
- manual row-order override preserved
- Rolling Signal Heatmap UI wiring through resolved canonical `row_key` sets
- Technical Analysis Dashboard section reorder completed
- ATR rolling heatmap support expanded and validated
- DPO rolling heatmap support added and validated

**Canonical interaction model**
- `Category → Scope → Window`
- `Scope` optional
- `Window` filter
- `Family` first-class filter
- selection modes:
  - `Custom`
  - `Category`
  - `Preset`

**Closure constraints verified**
- no Scenario B acquisition / persistence behavior changed
- no DB schema changes introduced
- no UI-local semantic scoring introduced
- `rolling_heatmap_adapter.py::INDICATOR_DEFS` remains the display / education metadata owner
- manual display/remove and row-order controls remain downstream override layers
- deferred semantic tiers remain deferred

**Interpretation**
This completed workstream added a row-selection / grouping architecture and related Rolling Heatmap row support. It does not constitute Option F Wave 2, regime logic, composite logic, cross-confirmation logic, or Phase IV explanation / rationale work.

---
#### Phase III Extension — Stock Comparison Dashboard v1

**Status:** Feature-branch implementation and focused regression validation complete; D3-D9 cleanup / promotion decision active.

**Current objective:**  
Finalize D3-D9 cleanup, update planning assets, and decide whether to merge `feature/scd-v1-exploration` into `main` for SCD v1 stabilization.

**Current checkpoint:** `0727ee6` — `(feat) Split Single Indicator today refresh controls`

**Primary architecture label:**  
SCD Signal Matrix Architecture

**Primary interaction / navigation model**
- `Ticker Source → Ticker Set → Analysis Mode → Indicator Selection → SCD Matrix View`

**Implemented analysis modes**
- `Multiple Indicators`
  - cross-sectional ticker × indicator matrix
- `Single Indicator`
  - date × ticker time-series matrix for one selected row

**Active v1 display modes**
- **SCD Multiple Indicators Cross-Sectional Matrix View**
  - rows = selected indicators
  - columns = selected tickers
  - cells = existing Rolling Heatmap value / signal / score
  - color = existing semantic score color
  - primary display = SCD Plotly Heatmap View
  - secondary display = SCD Detail Table View
    - copy/export/audit companion to the heatmap
    - uses the same underlying matrix cells
    - must not introduce ranking, aggregation, new scoring, or semantic reinterpretation
  - supports completed historical cache reuse
  - supports today/live refresh

- **SCD Single Indicator Time-Series Matrix View**
  - rows = dates
  - columns = selected tickers
  - indicator = one selected technical indicator row
  - cells = existing Rolling Heatmap value / signal / score
  - supports completed historical cache reuse
  - supports selected-row refresh through `Refresh this indicator only`
  - supports broad today payload refresh through `Refresh all indicators for today`
  - displays data freshness timestamp separately from matrix render/build time

**Formerly deferred display mode now promoted**
- SCD Single-Indicator Time-Series Matrix View was recognized as deferred in v3.3.0 and has now been explicitly promoted and implemented in SCD v1 D3.

**Scope boundary**
This workstream is a Phase III UI / display workstream. It must reuse existing Rolling Heatmap row-selection, rule-engine payload, Scenario B acquisition behavior, and value / signal / score cells. It must not redefine numeric truth, semantic meaning, score meaning, data acquisition policy, or persistence behavior.

**Active v1 includes**
- SCD-specific ticker controls
- SCD curated default ticker sets
- reuse of existing asset universes:
  - `assets::COUNTRY_ETFS`
  - `assets::SECTOR_ETFS`
  - `assets::CUSTOM_DEFAULT`
- reuse of the existing Rolling Heatmap row-selection resolver
- multi-ticker execution through the existing Rolling Heatmap / Option-C rule-engine path
- latest-cell extraction per selected ticker and row_key
- Single Indicator date × ticker matrix assembly
- SCD Plotly Heatmap View
- SCD Detail Table View
- Single Indicator chart layer
- Single Indicator freshness timestamp display
- Multiple Indicators live/today refresh
- Single Indicator refresh controls:
  - `Refresh this indicator only`
  - `Refresh all indicators for today`
- session-only SCD cache controls
- coverage-aware bundle cache
- completed historical result-cell cache

**Refresh / cache guardrails**
- selected-row / current-indicator refresh is not equivalent to broad today refresh
- broad today refresh must be labeled separately from selected-indicator refresh
- SCD cache layers remain session-only unless a future persistence change is explicitly approved
- completed historical result-cell cache remains separate from live/today refresh behavior

**Active v1 excludes**
- new semantic scoring
- ticker ranking
- aggregate technical strength score
- relative within selected tickers color mode
- composites
- cross-confirmation
- regime logic
- new numeric formulas
- new rulebook thresholds
- new DB table
- new persistence behavior
- persistent SCD ticker-set management
- AgGrid / pivot-table implementation

**Rejected / removed D3 experimental path**
- D3-F row-specific live result-cell cache:
  - status = tested, rejected, and removed
  - reason:
    - older row-specific live cells could override newer broad payload freshness
    - created confusing cross-indicator timestamp behavior
  - retained outcome:
    - Single Indicator freshness timestamp display remains
    - row-specific live-cell cache and diagnostics were removed

**Deferred / later cleanup items**
- Hidden D3-C / D3-D diagnostic scaffolding remains available but hidden:
  - `SCD_SHOW_TAIL_BUFFER_DIAGNOSTIC = False`
- Cleanup decision:
  - keep hidden diagnostics for now
  - document future cleanup / maintenance pass
- Deferred UX idea:
  - in-window Single Indicator display-date selector
  - useful but not required for D3 promotion
- Deferred optimization:
  - further broad-refresh runtime optimization
  - current broad refresh is coherent and validated, but runtime can remain broad-path-like

**Deferred numeric backlog remains unchanged**
- SMA slope / SMA semantic reopen

**Deferred later-wave semantic tiers remain unchanged**
- composites
- cross-confirmation
- regime logic

**D3-D9 validation checkpoint**
- Validated checkpoint:
  - `0727ee6` — `(feat) Split Single Indicator today refresh controls`
- Focused validation completed:
  - Single Indicator initial build
  - `Refresh this indicator only`
  - `Refresh all indicators for today`
  - cross-indicator timestamp reuse after broad refresh
  - unsupported-row fallback behavior
  - Multiple Indicators historical build
  - Multiple Indicators today refresh
  - no live-cell cache diagnostics after D3-F removal
  - compile/static checks passed for:
    - `streamlit_app.py`
    - `src/calculations/indicator_preprocessor.py`
    - `src/calculations/signal_classifier.py`
    - `src/calculations/signals_loader.py`
    - `src/calculations/technical.py`
- Promotion status:
  - ready for merge-to-main consideration after planning assets are updated

---
## Phase Transition — Option E Wave 1 Complete → Option F Activation

**Prerequisites satisfied:**

1. Phase III UX declared complete
2. Indicator numeric baseline captured  
   - `baseline/indicator_baseline_AAPL_phase3_baseline.csv`
3. Rulebook version frozen  
   - `master_rules_normalized__phase3_baseline.json`
4. Option E Wave 1 numeric primitives completed and validated

**Interpretation:**
- System is now safe to proceed with first-wave semantic activation (Option F)
- Numeric baselines remain available to detect unintended drift while semantic work is introduced

**Historical next active workstream at this transition:**
→ Option F — Semantic & Relational Logic (Wave 1)

**Wave 1 initial targets:**
- Bollinger semantics
- VWMA rule semantics

**Current status note:**
Option F Wave 1 is now complete. This section is retained as historical phase-transition context and no longer defines the current active workstream.

## MAJOR PHASE IV — Semantic Presentation & Decision Support

**Goal:** Explain *why* signals exist, not just show them.

* Natural-language explanations
* Rule rationale panels
* Composite signal narratives
* User-facing decision support

**Depends on:**
Stable completion of Option E + Option F.

---

## Design-Level Decisions (Explicit, Non-Negotiable)

### SMA Exclusion — Rationale (Authoritative)

SMA is **intentionally excluded** at this stage because:

1. **Numerically redundant** with EMA/HMA for current goals
2. **Lag-heavy**, adds little signal value in rolling heatmap context
3. Increases cognitive and UI clutter
4. Slopes/deltas (Option E) are better applied to EMA/HMA
5. SMA inclusion is a **Phase IV or later** decision, justified only if:

   * a semantic use case emerges
   * or SMA is required for external compatibility

This is a **design choice**, not a missing feature.

---

## Canonical Path Selection (Resolved)

### ❌ Path B — Phase II-first (Option E first)

* Deferred
* To be revisited only when UI requirements stabilize

### ✅ Path A — Phase III-first (**Canonical**)

* Rolling heatmap UX refinement
* Tight feedback loop into Option E
* No speculative numeric expansion

This is now the **official project path**.

---
## Open Architectural Decisions (Pending Resolution)
(Added: 2/14/26)

The following items remain unresolved and require explicit policy decisions before Phase III/IV stabilization:

### 1. `price_extremes_periods` Table
- Question: Should close-based extremes be cached persistently?
- Risk: Stale extremes vs unnecessary recomputation.
- Decision required:
  - Keep with auto-invalidation logic, OR
  - Compute on demand (session-only) and remove table.

### 2. `pivot_points_daily` Table
- Question: Should pivot calculations ever persist to DB?
- Current leaning: Pivot Points follow TA persistence policy (session-only unless explicitly saved).
- Decision required: Remove persistence entirely or formalize opt-in workflow.

### 3. `technical_indicators_daily` / `technical_indicators_variants_daily`
- Question: Are these historical indicator tables required for future features?
- Risk: Redundant storage vs performance gain.
- Decision required:
  - Keep as performance optimization layer, OR
  - Remove to simplify system and reduce data integrity complexity.

No structural DB changes should occur until these decisions are finalized.

---
## Current Project State (Snapshot)

* Phase I: ✅ Complete
* Phase II:

  * Core engine: ✅
  * Option D: ✅
  * Option E: ✅ Wave 1 complete
  * Option F: ✅ Wave 1 complete
  * Later semantic tiers remain deferred:
    - composites
    - cross-confirmation
    - regime logic
  * SMA slope / SMA semantic reopen remains later numeric backlog / review item

* Phase III:

  * Rolling heatmap acquisition (Scenario B): ✅ complete
  * Layout & semantics: ✅ complete
  * Rolling Heatmap Selection & Catalog Architecture (v1): ✅ complete
  * Stock Comparison Dashboard v1: ✅ feature-branch implementation / focused regression validation complete; D3-D9 promotion decision active

* Phase IV: 🔒 future

---

## What Comes Next (Immediately)

**Next active workstream:**
1) **Phase III Extension — Stock Comparison Dashboard v1 — D3-D9 cleanup / promotion decision**
   - update planning assets to reflect completed SCD v1 D3 implementation
   - decide whether to merge `feature/scd-v1-exploration` into `main`
   - after merge, run post-merge validation on `main`
   - if validation passes, tag a stable checkpoint:
     - candidate tag: `v0.3.3-scd-single-indicator-refresh-controls`

**Recently completed workstreams:**
2) **Phase III Extension — Stock Comparison Dashboard v1 / D3** — feature-branch implementation and focused regression validation complete
   - Multiple Indicators cross-sectional matrix implemented
   - Single Indicator time-series matrix promoted and implemented
   - Single Indicator chart layer implemented
   - SCD session cache controls implemented
   - coverage-aware bundle cache implemented
   - completed historical result-cell cache implemented
   - Multiple Indicators live/today refresh implemented
   - Single Indicator selected-row refresh implemented
   - Single Indicator freshness timestamp display implemented
   - split Single Indicator refresh controls:
     - `Refresh this indicator only`
     - `Refresh all indicators for today`
   - D3-F row-specific live result-cell cache tested, rejected, and removed
   - focused SCD regression checks passed at checkpoint `0727ee6`

3) **Recent indicator reference / rule-preprocessor updates**
   - `dfd0c29` — MACD & ATR reference / definition updates
   - `06d48a5` — DPO, MACD, STOCH markdown reference updates
   - `06d48a5` — `master_rules_normalized.json` fine-tuning:
     - window-aligned slope for HMA
     - standardized ATRP handling for BBP
   - `06d48a5` — `indicator_preprocessor.py` parameterized VWMA compatibility aliases

4) **Phase III UI Selection Architecture — Rolling Heatmap Selection & Catalog (v1)** — ✅ COMPLETE
   - authoritative row classification mapping
   - curated preset / Custom membership
   - selection-resolution logic
   - UI wiring for:
     - `Custom`
     - `Category`
     - `Preset`
   - preservation of the current manual display/remove and row-order controls as the downstream override layer
   - expanded Rolling Heatmap row support, including validated ATR and DPO additions

**Deferred later-wave semantic tiers remain unchanged**
- Option F Wave 2:
  - composites
  - cross-confirmation
- Option F Wave 3:
  - regime logic

**Deferred numeric backlog remains unchanged**
- SMA slope / SMA semantic reopen

**Important boundary**
- SCD D3 did not introduce new formulas, new scoring, ranking, aggregate technical strength, DB tables, persistence behavior, composites, cross-confirmation, or regime logic.
- Single Indicator selected-row refresh and broad today refresh must remain explicitly labeled as separate actions.
- Hidden diagnostics remain hidden and deferred for later cleanup.

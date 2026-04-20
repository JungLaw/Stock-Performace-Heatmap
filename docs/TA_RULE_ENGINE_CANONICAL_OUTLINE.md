# TA Rule Engine Project — Canonical End-to-End Outline
- Version: 3.2.6 
- Created: 1/12/26
- Last update: 4/16/2026

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

**Status:** 🟡 NEXT ACTIVE WORKSTREAM (Wave 1 defined; implementation pending)

**Wave 1 scope (authoritative):**
* Bollinger semantic activation
* VWMA rule semantics

**Wave 1 boundary:**
* Option F must consume existing numeric primitives from the indicator dataframe
* semantic meaning must be created through the rulebook / signal-classifier path
* UI layers may display semantic outputs but must not invent semantics locally

**Deferred beyond Wave 1:**
* composites
* cross-confirmation
* regime logic

**Deferred outside Option F Wave 1:**
* SMA slope / SMA semantic reopen
  - remains a later numeric backlog / review item, not a first-wave semantic target

---
#### Option F Sequencing (authoritative)

Option F should proceed in semantic tiers:

**Wave 1 — single-family semantic activation**
- Bollinger semantics
- VWMA semantics

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

**Next Active Workstream:**
→ Option F — Semantic & Relational Logic (Wave 1)

**Wave 1 initial targets:**
- Bollinger semantics
- VWMA rule semantics

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
  * Option F: ⏸️ deferred pending explicit reopening

* Phase III:

  * Rolling heatmap acquisition (Scenario B): ✅ complete
  * Layout & semantics: ✅ complete
* Phase IV: 🔒 future

---

## What Comes Next (Immediately)

**Next active workstream (in order):**
1) **Option E — Derived numeric primitives**
   - EMA slope
   - validation against numeric baseline
   - additive-only numeric derivation work

2) **Option E backlog continuation**
   - additional slopes / derived metrics
   - normalization primitives
   - band-derived numeric outputs

Only after Option E stabilization:
- Phase II continuation via **Option F**
- Later semantic expansion via **Phase IV**

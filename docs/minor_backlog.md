# Minor Backlog Ledger — TA Rule Engine
Version: 1.2
Last update: 7/13/26

## Authority level

This file is an intake and triage ledger for minor tasks, audits, cleanup items, UX polish, and one-off fixes.

It is subordinate to:
1. `TA_RULE_ENGINE_CANONICAL_OUTLINE.md`
2. `Master Checklist (Authoritative)- Phase 3.md`
3. `Constraints_ChatGPT.md`

This ledger does not create new scope by itself.

Items in this ledger become authoritative only when:
- promoted into the Master Checklist,
- reflected in the Canonical Outline,
- implemented and committed,
- or explicitly approved as an active task by the user.

## Routing rule

- Use this ledger for candidate/minor items.
- Update the Master Checklist only when an item is completed, rejected, deferred, or promoted.
- Update the Canonical Outline only when an item changes architecture, phase status, major scope, or authoritative project model.

---
## Active minor candidates

### MINOR-001 — SMA Rulebook / Runtime Reconciliation

Status: Candidate
Type: audit / governance
Related Master Checklist item: SMA slope / SMA semantic reopen
Related Canonical Outline section: Option E / Option F deferred backlog

Objective:
Determine whether current SMA rulebook/runtime behavior is fully active, partially active, or documentation-mismatched.

Potential outcomes:
- mark SMA semantics as active/validated
- keep SMA as deferred pending validation
- identify gaps in SMA slope/ATRP computation or scoring
- update Master Checklist / Canonical Outline if official status changes


### MINOR-002 — Crossover Event Signals Feasibility Audit

Status: Audit complete — promote to major-scoped planning
Type: audit / major-candidate triage
Source: user-proposed enhancement; `Initial Q&A-Crossover.txt`
Priority: High
Requires major workstream? Yes — compact major workstream
Related Master Checklist item: To be added as upcoming workstream if approved
Related Canonical Outline section: Option E numeric primitives / Option F semantic & relational logic

Objective:
Determine whether crossover event rows for moving averages and RSI threshold crossings can be implemented as a minor task or require a dedicated major workstream.

Audit conclusion:
Crossover event rows should be promoted to a compact major workstream because implementation touches derived event computation, rulebook/semantic representation, row catalog metadata, display metadata, Rolling Heatmap selection, SCD Multiple Indicators, SCD Single Indicator, hover/detail behavior, and validation.

Recommended workstream name:
`Crossover Event Signal Rows v1`

Recommended first-wave rows:
- `EMA_9_X_EMA_21`
- `SMA_20_X_SMA_50`
- `SMA_50_X_SMA_200`

Deferred from first wave:
- `EMA_5_X_EMA_13`
- RSI threshold crossover rows until direction/label/scoring semantics are locked
- selected-row refresh optimization
- event + state scoring
- days-since-last-cross unless low-cost after core event rows are stable

Required design locks before implementation:
- event-only vs event + state
- canonical row-key naming
- internal `XA` / `XB` helper naming
- rulebook representation
- hover/detail metadata
- default/preset membership
- RSI threshold terminology and direction

Promotion rule:
- Add to Master Checklist as next active/upcoming major workstream once user approves prioritizing it over Option F Wave 2 / Wave 3.
- Update Canonical Outline only after approval to recognize it as the next active workstream / Option E-F bridge item.

---
### MINOR-003 — Moving Average Analysis Display Cleanup

Status: Completed
Type: UX / code / cleanup
Source: user observation; screenshot and CSV export from Technical Analysis dashboard
Priority: High
Requires major workstream? No
Docs update needed? Minor backlog ledger only; Master Checklist and Canonical Outline not required

Completion date: 7/13/26
Commit: `046b80e` — `(feat) Complete MINOR-003 moving average display cleanup`
Branch: `main`
Push status: Pushed to `origin/main`

Objective:
Improve the Technical Analysis dashboard subsection `Moving Average Analysis` so the displayed SMA / EMA analysis is readable, compact, and presentation-quality.

Completed implementation:
- Split SMA and EMA into separate tabs.
- Replaced the wide side-by-side table with compact tables using:
  - `Period`
  - `MA Value`
  - `Price vs MA`
  - `Signal`
  - `Strength`
  - `Comment`
- Changed period labels to forms such as `SMA(20)` and `EMA(20)`.
- Removed raw signal payloads from visible table cells.
- Removed inverse distance columns such as `SMA/P0` and `EMA/P0`.
- Preserved existing moving-average signal and strength semantics.
- Added concise comments such as:
  - `NVDA is 0.5% above its 20D SMA. It has to fall 0.5% to reach it.`
  - `NVDA is 2.3% below its 50D EMA. It has to rise 2.3% to reach it.`
- Corrected exact / display-rounded equality wording to:
  - `<ticker> is at its <period>D <MA type>.`
- Added `SMA(250)` to the SMA tab only.
- Left EMA periods unchanged.
- Preserved the existing public current-price float API.
- Added price-source provenance metadata without adding a new acquisition call.
- Added effective date / timestamp transport into the Moving Average Analysis payload.
- Added date/time display behavior:
  - Historical or latest completed data:
    - `Latest Price: $202.78 (7/10/26)`
  - Same-day data with a reliable market timestamp:
    - `Latest Price: $202.78 (7/13/26 @ 1:23P)`
  - Same-day data without a reliable market timestamp:
    - date-only fallback
- Restored the compact native `st.dataframe()` renderer.

Accepted limitation:
- The proposed `Price vs MA` boldface rule was not enabled.
- Installed runtime:
  - Streamlit `1.46.1`
  - pandas `2.3.2`
- The installed Streamlit version did not render pandas Styler font-weight behavior reliably for this table.
- Two attempted renderer/styling approaches did not satisfy the requirement.
- The changes were rolled back to the appropriate compact `st.dataframe()` implementation.
- The explanatory bolding note was removed so the UI does not claim unsupported behavior.
- This limitation is accepted for MINOR-003 and does not block completion.
- Bolding may be reconsidered later after a controlled Streamlit upgrade and isolated capability test.

Scope preserved:
- No moving-average formula changes.
- No signal-threshold changes.
- No rulebook changes.
- No scoring changes.
- No DB schema changes.
- No persistence changes.
- No new acquisition path.
- No Rolling Heatmap changes.
- No Stock Comparison Dashboard changes.
- No unrelated Technical Analysis dashboard behavior changes.

Verification completed:
- Python compile checks passed.
- `$LASTEXITCODE` returned `0`.
- Static Status Verification checks passed.
- Sunday / closed-market manual checks passed.
- Monday / same-day timestamp manual checks passed.
- SMA(250) is visible only in the SMA tab.
- EMA periods remain unchanged.
- Signal and Strength outputs remain unchanged.
- Raw signal dictionaries are not visible.
- Inverse distance columns are not visible.
- Compact table rendering is restored.
- Git diff check passed.
- Code commit was created and pushed successfully.

Completion criteria outcome:
- SMA and EMA Moving Average Analysis displays are readable without horizontal overload: PASS
- Raw signal payloads are no longer visible: PASS
- Signal and Strength are clean user-facing fields: PASS
- `Price vs MA` is formatted clearly: PASS
- Boldface proximity treatment: ACCEPTED LIMITATION / DEFERRED
- Comment text uses the agreed format: PASS
- Effective price date/time behavior is accurate to the available source metadata: PASS
- No unrelated dashboard behavior changed: PASS
- Compile and focused manual checks passed: PASS
- Commit and push completed: PASS

Future optional cleanup:
- SMA(9) and SMA(21) may later be removed from this table as display-only changes by deleting `9` and `21` from `periods_by_type['SMA']` in `streamlit_app.py`.
- Upstream calculation changes are not required for a display-only removal.

Promotion result:
- Remained a minor scoped task.
- No promotion to a major workstream was required.
- No Master Checklist or Canonical Outline update is required.

---
### MINOR-004 — Price Performance Hover Context Expansion

Status: Planned
Type: UX / code / hover-display cleanup
Source: user-requested hover enhancement for Performance Heatmap → Price Performance
Priority: High
Requires major workstream? No
Docs update needed? Minor backlog ledger; Master Checklist only after completion if completed-status rollup is desired; Canonical Outline not expected

Objective:
Improve the Performance Heatmap hover content for `Analysis Mode: Price Performance` by adding richer context: current price, selected price-period comparison, current volume, volume comparisons versus multiple benchmark windows, and an as-of date for the displayed current data.

Current observed behavior:
The current Price Performance hover is compact but limited. Example:

```text
Ticker: GOOGL
Current: $358.29
1D (7/1/26): $361.21
Change: $-2.92 (-0.81%)
```

Desired hover direction:
Replace or expand the Price Performance hover so it follows this general structure:

```text
Current: $358.29
- vs. 1D (7/9): ($-2.92, -0.8%)

Current Volume: 10.0M
- vs. 1D:       -9.1% (11.0M)
- vs. 1W Avg:   -9.1% (11.0M)
- vs. 2W Avg:   -9.1% (11.0M)
- vs. 1M Avg:  +11.1% (9.0M)
- vs. 3M Avg:  -50.0% (20.0M)

As of: 7/9
```

Notes:

* Example values are illustrative; implementation must use actual available data.
* User comments marked with `#` in the original request are not part of hover text.
* Preserve visual alignment of volume-comparison percentages as much as Plotly hover rendering allows.
* Use fixed-width formatting, non-breaking spaces, or another safe hover-formatting approach if ordinary spaces collapse.
* This is a display/hover-content enhancement only.

Scope boundaries:

* Preserve existing price-performance calculations.
* Preserve existing color logic and tile sizing.
* Preserve existing ticker universe behavior.
* Preserve existing DB/cache/acquisition policy unless current code already exposes the needed values.
* Reuse existing volume benchmark logic if available.
* Stop and reassess if this requires new persistence behavior, new DB schema, or a broad acquisition redesign.

Completion criteria:

* Price Performance hover displays current price, selected price-period comparison, current volume, volume benchmark comparisons, and as-of date.
* No unrelated Performance Heatmap behavior changes.
* Existing price-performance tiles continue to render correctly.
* Hover spacing/alignment is improved as much as Plotly supports.
* Code compiles.
* Status Verification Block passes.
* Focused manual checks pass.
* Git diff is focused.


---
### MINOR-005 — Volume Performance Hover Context / As-of Context Review

Status: Planned
Type: UX / code / hover-display cleanup / bounded feasibility review
Source: user-requested hover enhancement for Performance Heatmap → Volume Performance
Priority: High
Requires major workstream? No, unless current-day / intraday as-of support requires new acquisition, cache, or persistence behavior
Docs update needed? Minor backlog ledger; Master Checklist only after completion if completed-status rollup is desired; Canonical Outline not expected unless as-of support changes acquisition/cache/persistence architecture

Objective:
Improve the Performance Heatmap hover content for `Analysis Mode: Volume Performance` by adding price context, richer multi-window volume comparisons, and an as-of line. Also assess whether current-day / incomplete-volume as-of support can be implemented using existing Performance / Volume dashboard data paths without changing acquisition, cache, persistence, or DB behavior.

Current observed behavior:
The current Volume Performance hover is limited. Example:

```text
Ticker: GOOGL
Current Volume: 26,687,500
10 days Avg: 45,461,460
Volume Change: -41.17%
```

Desired hover direction:
Replace or expand the Volume Performance hover so it follows this general structure:

```text
Ticker: GOOGL
Price: $100 (-$5.00, -4.7%)

Current Volume: 12,500,000
- vs. 1D:       -9.1% (11.0M)
- vs. 1W Avg:   -9.1% (11.0M)
- vs. 2W Avg:   -9.1% (11.0M)
- vs. 1M Avg:  +11.1% (9.0M)
- vs. 3M Avg:  -50.0% (20.0M)

As of: 7/9
```

Conditional as-of enhancement:
Assess whether an as-of-date option can be added for Volume Performance, similar in spirit to the Rolling Heatmap anchor/as-of behavior, so the dashboard can display current-day incomplete volume when available.

If current-day / intraday values are available through existing data paths, the hover should support:

```text
As of: 7/10 @ 6:26 PM
```

and `Price:` should reflect the intraday/current price with comparison versus the previous completed trading day.

Scope boundaries:

* Base task is hover-display enhancement for Volume Performance only.
* Current-day / intraday as-of support is conditional.
* Reuse existing Performance / Volume calculator paths if available.
* Do not add new DB schema, persistence behavior, or broad acquisition/cache behavior inside this minor task.
* Stop and reassess if current-day support requires new acquisition architecture, new cache policy, or material performance changes.

Completion criteria:
* Volume Performance hover displays ticker, price context, current volume, volume comparisons across 1D / 1W / 2W / 1M / 3M, and an as-of line.
* If current-day / intraday support is feasible using existing paths, it is implemented in a bounded way.
* If current-day / intraday support is not feasible without scope expansion, limitation is documented and the base hover cleanup still proceeds if safe.
* Existing Volume Performance calculations and tile coloring are preserved.
* No unrelated Performance Heatmap behavior changes.
* Code compiles.
* Status Verification Block passes.
* Focused manual checks pass.
* Git diff is focused.

Promotion rule:
* Keep as minor if implementation is confined to existing Volume Performance hover/data-shaping paths.
* Split or promote if current-day / intraday as-of support requires new acquisition, cache, persistence, DB schema, or broader dashboard architecture.

---
## Template

```
### <Item Name>
Status: Candidate / Planned / In progress / Complete / Rejected / Deferred
Type: audit / doc / UX / code / verification / cleanup
Source: chat note / user observation / regression result
Priority: Low / Medium / High
Requires major workstream? Yes/No/Unknown
Docs update needed? None / Master Checklist / Canonical Outline / Completion ledger only

Objective:
...

Notes:
...

Completion criteria:
...

Promotion rule:
- If audit shows this is bounded to a few existing paths, create a Minor Task Brief for implementation.
- If audit shows new semantic/event architecture is needed, promote to major workstream planning.
- Update Master Checklist only if promoted, completed, rejected, or formally deferred as project-significant.
- Update Canonical Outline only if it changes semantic architecture, phase status, or the authoritative project model.

## Completed minor items
...
```


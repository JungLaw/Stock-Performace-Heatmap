# Minor Backlog Ledger — TA Rule Engine

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

## Completed minor items
...
```


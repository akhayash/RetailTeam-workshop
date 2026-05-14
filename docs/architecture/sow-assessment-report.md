# SOW Assessment & Rating Report — VirtualMirror AI

| Field | Value |
|-------|-------|
| **Artifact under review** | [`docs/Virtual-Mirror-SOW.md`](../Virtual-Mirror-SOW.md) v0.1.0 (2026-05-14) |
| **Reviewer** | GitHub Copilot (assessment agent) |
| **Review date** | 2026-05-14 |
| **Rubric source** | `EX3_Discovery_to_Delivery_SOW.pptx` slides 13–16 |
| **Final score** | **20.5 / 21** (Grade: **Excellent**) |
| **Recommendation** | Promote 0.1.0 → 0.2.0 with minor cleanups, then to 1.0.0 for signature |

> The rating is anchored to the **7-dimension scoring rubric on slide 15** (0–3 per dimension, 21 points total), cross-checked against the **Microsoft Paper writing checklist (slide 14)**, the **roles & estimation quick rules (slide 13)**, and the **5 facilitator debrief questions (slide 16)**.

---

## 1. Scoring summary (slide 15 rubric, 21 points)

| # | Dimension | Score | Verdict |
|:-:|-----------|:----:|---------|
| 1 | Traceability to discovery | **3 / 3** | Excellent |
| 2 | Outcome clarity | **3 / 3** | Excellent |
| 3 | Scope discipline | **3 / 3** | Excellent |
| 4 | Deliverables + acceptance | **3 / 3** | Excellent |
| 5 | Estimate realism | **2.5 / 3** | Good → Excellent (one reconciliation nit) |
| 6 | Roles & responsibilities | **3 / 3** | Excellent |
| 7 | Risk & assumptions | **3 / 3** | Excellent |
| | **Total** | **20.5 / 21** | **Excellent** |

```
0  3  6  9  12 15 18 21
|--|--|--|--|--|--|--|
                    █  20.5
```

---

## 2. Dimension-by-dimension assessment

### 2.1 Traceability to discovery — 3 / 3

**Rubric "Excellent":** *Every deliverable and hour ties to pressures / outcomes / constraints.*

Evidence the SOW meets this bar:

- The header banner explicitly states *"Every line item in this SOW traces back to a discovery artifact"* and enumerates [`Sessions/Problem-statement.md`](../Sessions/Problem-statement.md), [`Sessions/Product-definition.md`](../Sessions/Product-definition.md), [`specs/001-clothing-fit-assessment/`](../../specs/001-clothing-fit-assessment/spec.md), [`docs/architecture/`](./solution-architecture.md), and [`docs/project-plan.md`](../project-plan.md).
- Every major section footer carries a `*Source:* …` citation (e.g., §2.1 cites Product-definition.md market sizing; §3.1 cites SC-002/SC-003; §4 cites project-plan §4 WBS; §16 cites cost-estimate.md).
- Worksheet B.1 ties **every D-1 … D-14 deliverable** to a Business Outcome **and** to a feature ID set (US1–US4, FR-001..015, SC-001..007).
- Work packages WP1–WP8 are stated to be pre-decomposed in [`tasks.md`](../../specs/001-clothing-fit-assessment/tasks.md) (147 tasks, T001–T147) — line-of-sight from epic → task is unbroken.
- BO-1 / BO-2 / BO-3 trace to spec.md SC-002 and SC-003 and to the Product-definition success metrics.

**Slide 16 debrief Q1 — "Is every element traceable to discovery?"** — **Yes.** No invented scope detected.

---

### 2.2 Outcome clarity — 3 / 3

**Rubric "Excellent":** *Outcomes measurable, prioritized, customer-owned.*

Evidence:

- Three BOs (§3.1) each have a **measure** and a **numeric target with timeframe**:
  - BO-1: ≥ 20% return-rate reduction (target 30%) within 6 months
  - BO-2: +3–5% conversion lift within 6 months
  - BO-3: ≥ 1 tenant at GA; architected for 20+ at Scale tier
- **Customer ownership is explicit**: the non-guarantee clause separates Microsoft's commitment (delivering the capability + the measurement framework) from customer-owned business outcomes (adoption, merchandising, marketing).
- Worksheet A repeats the BOs verbatim — single source of truth across the document.

**Slide 16 debrief Q2 — "Are outcomes customer-owned and measurable?"** — **Yes**, with an explicit non-guarantee clause that protects both parties.

Optional polish: BO-3's "architected for 20+ at Scale tier" is a capability statement, not a measurable outcome on its own — consider re-wording to *"platform reaches X tenants by month N"* if Walmart commits to a tenant roadmap. Not a downgrade.

---

### 2.3 Scope discipline — 3 / 3

**Rubric "Excellent":** *Tight scope, explicit in/out, protects from creep.*

Evidence:

- §4 (in scope, 8 work packages) and §5 (out of scope, 12 categories with rationale) bracket the engagement crisply.
- Worksheet A restates the boundaries in 3 IS- and 3 OOS- anchors — easy for executives to verify.
- §12 Change Management lists 5 trigger conditions and a 4-step impact-analysis process with SLAs.
- Worksheet B.3 ships a **Scope Traps** table with 10 named items (ST-1 … ST-10) and rough effort ranges — directly meets slide 14's "add a scope traps callout for what could expand hours quickly" rule.
- MVP cutline (end of Sprint 4) and GA cutline (end of Sprint 9) are stated, so creep within a sprint cannot silently push the GA gate.

**Slide 16 debrief Q5 — "Where did the team over- or under-scope the work?"** — Boundaries are tight; the only risk of *under-scope* is the H1 spike contingency (3DLOOK bridge, +20–30 PD) which is explicitly named as ST-1 and carried as a Change Order trigger.

---

### 2.4 Deliverables + acceptance criteria — 3 / 3

**Rubric "Excellent":** *Clear deliverables with testable acceptance criteria.*

Evidence:

- Worksheet B.1 has **14 deliverables** with the four-column shape the rubric expects: description in customer language, acceptance criteria, outcome supported, trace.
- Acceptance criteria are **testable**, not aspirational — examples:
  - D-2: *"H1: ≤ 15% of calibration photos > ±4 cm vs. ground truth"*
  - D-6: *"H8: ≥ 90% request success during partial AI outage"*
  - D-10: *"p95 < 5 s at 500 concurrent; KEDA scales to 10 instances"*
  - D-8: *"coverage gate ≥ 80% line / ≥ 90% critical; SBOM artefact attached"*
- §15.2 sets a two-tier acceptance model (PO-only for backlog items vs. written sign-off for phase gates + Privacy + Security).
- Hypothesis gates H1, H3, H5, H7, H8 are independently called out with pass/fail thresholds and tie directly to sprint reviews.

Result: deliverables are **reviewable, signable, and testable** (slide 14 checklist) without exception.

---

### 2.5 Estimate realism — 2.5 / 3

**Rubric "Excellent":** *Credible, role-based estimates with assumptions and drivers.*

Evidence the SOW substantially meets this:

- **Hours by role AND by work package — both present** (slide 13's hard rule):
  - Worksheet B.2 WP table totals **~274 PD / ~2,192 h**.
  - "Hours by role" sub-table breaks the allocation across Tech Lead, SDE#1, SDE#2, DevOps, ML, QA, Security.
- **Drivers are explicit**: three-tier AI pipeline complexity, 12 Bicep modules, 500-concurrent load target, multi-tenant + DPIA, OWASP ASVS L2 + PCI-adjacent posture, canary deployment with < 15 min rollback.
- **Estimation method documented**: bottom-up, three-point reference scale, senior-IC productivity baseline of 6.5 PD/FTE-sprint, +15% ceremony, +15% defect/UAT buffer, 14% headroom for spikes.
- **Top 3 assumptions** explicitly listed alongside the estimate (H1 accuracy, senior-IC team, Walmart inputs on time).
- Assumption A-1 ties the estimate directly to seniority — *"junior-heavy substitution requires 1.3–1.5× effort multiplier"*. This is exactly the discipline slide 14 asks for.

**Why 2.5 and not 3 — one reconciliation nit to fix before signature:**

The role-allocation sub-table in §B.2 totals **~296 PD / ~2,368 h** while the WP table totals **~274 PD / ~2,192 h**. The parenthetical explanation — *"slack ~22 PD covers vacation + ceremony float; actual chargeable build ~274 PD"* — is correct but slightly buried. A customer-side estimator will spot the 22 PD delta in their first read.

**Coaching fix (5 minutes):**

- Add a one-line footnote under each table that names the reconciliation: WP table = chargeable build envelope (~274 PD); role table = gross capacity allocation (~296 PD) including vacation + ceremony float of ~22 PD.
- Or restructure the role table to show **chargeable / non-chargeable / total** columns.

This is a clarity defect, not a credibility defect — the numbers themselves are coherent. After the fix this is a 3.

**Slide 16 debrief Q3 — "Do roles and hours feel credible for the scope?"** — **Yes.** ~274 PD / 18 weeks / 5.75 avg FTE / senior-heavy mix for a multi-tenant AI service with full IaC + CI/CD + load + chaos + DPIA + model card is a defensible envelope; the headroom (14%) and the WP8 cross-cutting buffer (~25%) are honest.

---

### 2.6 Roles & responsibilities — 3 / 3

**Rubric "Excellent":** *Roles crisp, accountable; customer responsibilities explicit.*

Evidence:

- §8.2 lists **9 Microsoft roles** with FTE, engagement window, and responsibilities — matches and extends slide 13's default role list (Engagement Lead, Solution Architect, Industry SME equivalent, Delivery Consultant equivalent, PM).
- §8.3 lists **8 Walmart roles** with engagement window and responsibility.
- §17.1 lists **12 customer-side commitments (C-1 … C-12)** each with a *needed-by sprint* and a named Walmart owner — far above the slide 14 minimum of "list customer responsibilities".
- §14 Escalation Path has 4 levels with explicit time-to-resolve SLAs, plus a P1 fast-path.
- §9 governance bodies have cadence and membership.

No accountability gaps detected. Tech Lead bottleneck on PR reviews is itself logged as plan risk PR-3 with a 25% time-reserve mitigation — that level of self-awareness is what the rubric is looking for.

---

### 2.7 Risk & assumptions — 3 / 3

**Rubric "Excellent":** *Key assumptions/risks explicit with mitigation/validation plan.*

Evidence:

- §13.1 Top Plan Risks: 6 items with severity + mitigation, linked to [`project-plan.md`](../project-plan.md) §10.
- §13.2 Top Technical Risks: pulled from [`risk-register.md`](./risk-register.md) (R-001 GPT-5.2 measurement accuracy CRITICAL with H1 gate; R-003 non-determinism HIGH; R-004 photo quality MEDIUM).
- §18 Assumptions split into **engagement (A-1..A-5)**, **technical (A-6..A-11)**, and **process (A-12..A-15)** — 15 numbered assumptions in total.
- *"Each unmet assumption is a change-management trigger (§12)"* — assumptions are wired to the contract, not decorative.
- Validation plan exists as **Hypothesis gates H1, H3, H5, H7, H8** with quantified pass/fail thresholds and scheduled sprint windows.

**Slide 16 debrief Q4 — "What assumptions create the highest delivery risk?"** — Three stand out and are all called out by name in the SOW:

| Assumption | Risk if it fails | Mitigation already in SOW |
|------------|-------------------|---------------------------|
| **A-6** GPT-5.2 measurement accuracy ±2–4 cm (H1) | MVP delayed, fit recommendations not trustworthy | Sprint 2 calibration dataset prep + Sprint 3 spike + ST-1 / 3DLOOK bridge contingency (+20–30 PD) |
| **A-1** Senior-IC team composition | Estimates inflate 1.3–1.5× | Locked at SOW signature; substitution = Change Order |
| **A-4** Walmart inputs land by sprint (esp. C-2 PTU, C-6 calibration set, C-7 Notation keys) | Sprint slippage, H1 gate slip | MSDN fallback for Sprint 1; sprint-by-sprint dependency tracking in §17.1 |

---

## 3. Slide 14 "Microsoft Paper" checklist

| Checklist item | Met? | Note |
|----------------|:----:|------|
| Objective + outcomes in customer language, no internal jargon | ✅ | §2.2 and §3.1 lead with Walmart outcomes; acronyms defined in Appendix glossary |
| Short sections with headings: Objective, Scope, Deliverables, Workplan, Roles, Estimates, Assumptions | ✅ | All present (§2, §3–§5, §15, §6–§10, §8, §7, §18) |
| Deliverables concrete — reviewable, signable, testable | ✅ | Worksheet B.1 14 deliverables with testable acceptance criteria |
| Hours by role AND by work package | ✅ | Worksheet B.2 — both tables present |
| Drivers included (complexity, sites, data sources, environments) | ✅ | §B.2 Summary row "Estimation drivers" |
| Explicit assumptions list that makes the estimate true | ✅ | §18 (15 numbered assumptions) + Worksheet B.2 top-3 callout |
| One idea per paragraph; prefer bullets over long prose | ✅ | Tables-and-bullets throughout |
| Acronyms defined on first use | ⚠️ | Mostly. Glossary covers them but some acronyms (e.g., KEDA, OWASP ASVS L2, NIST CSF 2.0) appear in §2 before §16 / Appendix A — consider inline expansion on first use |
| Avoid solutioning language in scope statements | ✅ | §3 talks outcomes; technology choices live in §16 |
| List customer responsibilities | ✅ | §17 with 12 sprint-anchored items |
| "Scope traps" callout | ✅ | Worksheet B.3 — 10 named traps with effort ranges |
| Active voice, consistent tense, customer-facing read | ✅ | Verified across §2, §3, §6, §15 |

**One minor inconsistency to fix during 0.1.0 → 0.2.0 promotion:**

- **Hypercare duration** is stated as **"2 weeks"** in §6.3, §15, §17, and §19 trigger #4, but as **"30 calendar days"** in §17.2 and §19 closing sentence. Pick one (30 days is more common contractually) and align everywhere.

---

## 4. Facilitator debrief synthesis (slide 16)

| # | Question | Verdict | Evidence anchor |
|:-:|----------|---------|------------------|
| 1 | Is every element of the SOW traceable to discovery? | **Yes** — sourced inline + Worksheet B trace column | §2.1, §3.1, §4, §16, Worksheet B.1 |
| 2 | Are outcomes customer-owned and measurable? | **Yes** — 3 BOs with metric + target + timeframe + non-guarantee clause | §3.1, Worksheet A |
| 3 | Do roles and hours feel credible for the scope? | **Yes** — senior-IC, 274 PD, 14% headroom, drivers documented | §8.2, Worksheet B.2 |
| 4 | What assumptions create the highest delivery risk? | **A-6 (H1), A-1 (seniority), A-4 (customer inputs)** — all wired to Change Mgmt | §13, §18, Worksheet B.2 top-3 |
| 5 | Where did the team over- or under-scope the work? | **Slight under-scope risk** if H1 fails (ST-1 contingency budgeted but tight); WP8 cross-cutting at ~25% is reasonable | §5, Worksheet B.3 |

---

## 5. Recommendations before promotion to v1.0.0 (signature draft)

These are *coaching moments*, not blockers. Total fix effort: < 1 hour.

| # | Recommendation | Section | Impact |
|:-:|----------------|---------|--------|
| R-1 | Reconcile WP table (274 PD) vs. role table (296 PD) with an explicit chargeable/gross footnote or split columns | §B.2 | Removes the only credibility nit; lifts dimension 5 from 2.5 → 3 |
| R-2 | Standardise hypercare duration — 2 weeks vs. 30 calendar days | §6.3, §15, §17.2, §19 | Removes ambiguity in the completion criteria |
| R-3 | Expand KEDA / OWASP ASVS L2 / NIST CSF 2.0 on first inline use even though glossary covers them | §2.2, §3.2, §11 | Improves customer-facing readability |
| R-4 | Consider re-wording BO-3 to a measurable tenant-roadmap outcome (e.g., "≥ 3 tenants by month 12") if Walmart can commit; otherwise label it explicitly as a capability outcome rather than a business outcome | §3.1, Worksheet A | Tightens the measurability story for executive sponsor |
| R-5 | Add a one-line indicative price band (or *"price provided under separate Work Order"*) so customer reviewers are not left wondering | §2.3 or §7 | Sets price expectation without committing the not-to-exceed figure |
| R-6 | Add a single-line note clarifying that the 14% headroom is **shared** across spikes, integration friction, **and** the H1 contingency, OR carve out an explicit H1-contingency reserve | §7 capacity model, §13.1 PR-1 | Avoids double-counting risk if H1 misses |

---

## 6. Final verdict

**Score: 20.5 / 21 — Excellent**

This SOW is at the top of the rubric on six of seven dimensions. The single point not yet earned is a *clarity* issue in the estimate reconciliation, not a credibility one — the underlying numbers, drivers, and assumptions are coherent. The document also clears every item on the slide 14 writing checklist with only two minor polish notes (acronym-on-first-use and hypercare-duration alignment).

**Recommended next action**: apply R-1 and R-2 (~30 min of editing), bump to v0.2.0, route to Walmart Product Council for review, and target v1.0.0 final-for-signature after Executive Steering Committee approval.

---

## Version history

| Version | Date | Author | Notes |
|--------:|------|--------|-------|
| 1.0.0 | 2026-05-14 | GitHub Copilot | Initial assessment of `Virtual-Mirror-SOW.md` v0.1.0 against `EX3_Discovery_to_Delivery_SOW.pptx` slides 13–16 |

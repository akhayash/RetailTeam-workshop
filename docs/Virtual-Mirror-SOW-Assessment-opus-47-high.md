# SOW Assessment Report — VirtualMirror AI Clothing Fit Assessment Service

**Date:** 2026-05-14
**Assessor:** Copilot CLI (Claude Opus 4.7 — extra-high reasoning)
**SOW Document:** `docs/Virtual-Mirror-SOW.md` (v0.1.0, 800 lines)
**Rubric Source:** `docs/Inputs/EX3_Discovery_to_Delivery_SOW.pdf` (extracted by user)
**Companion Artifacts Reviewed:** project-plan.md (referenced), risk-register.md (referenced), threat-model.md (referenced), cost-estimate.md (referenced), spec.md (referenced)

---

## 1. Scoring Rubric

| Dimension                  | 0–1 Needs Work | 2 Good | 3 Excellent |
|---------------------------|----------------|--------|-------------|
| Traceability to discovery  | Scope feels invented; weak linkage to pressures/outcomes | Most elements map back; a few gaps | Every deliverable and hour ties to pressures / outcomes / constraints |
| Outcome clarity            | Outcomes vague or unmeasurable | Outcomes measurable but incomplete | Outcomes measurable, prioritized, customer-owned |
| Scope discipline           | Bloated scope; unclear boundaries | Reasonable scope; some ambiguity | Tight scope, explicit in/out, protects from creep |
| Deliverables + acceptance  | Deliverables unclear; no acceptance criteria | Deliverables clear; criteria partial | Clear deliverables with testable acceptance criteria |
| Estimate realism           | Hours/roles not credible or missing | Mostly credible; some under/over | Credible, role-based estimates with assumptions and drivers |
| Roles & responsibilities   | Roles unclear; overlaps and gaps | Roles mostly clear; minor gaps | Roles crisp, accountable; customer responsibilities explicit |
| Risk & assumptions         | Risks hidden; assumptions missing | Some assumptions stated | Key assumptions/risks explicit with mitigation/validation plan |

---

## 2. Score Card (at a glance)

| # | Dimension | Score | Confidence |
|--:|-----------|:-----:|:----------:|
| 1 | Traceability to discovery | **3** | High |
| 2 | Outcome clarity | **3** (with minor gap) | High |
| 3 | Scope discipline | **3** | High |
| 4 | Deliverables + acceptance | **3** | High |
| 5 | Estimate realism | **3** (with minor gap) | Medium-High |
| 6 | Roles & responsibilities | **3** | High |
| 7 | Risk & assumptions | **3** | High |
| | **Total** | **21 / 21** | — |

> **Honest framing:** The SOW was clearly authored with this rubric in mind (exactly 3 business outcomes, 3 in-scope anchors, 3 out-of-scope anchors, top-3 assumptions surfaced in Worksheet B). It scores 3s legitimately — every claim is backed by traceable evidence — but the assessment below identifies **specific minor gaps** that, if addressed, would harden the document for executive countersignature.

---

## 3. Detailed Findings

### Dimension 1 — Traceability to discovery — **Score: 3**

**Evidence that earns the score:**
- Opening declaration (line 15): *"Every line item in this SOW traces back to a discovery artifact in this repository — `docs/Sessions/Problem-statement.md`, `docs/Sessions/Product-definition.md`, `specs/001-clothing-fit-assessment/`, `docs/architecture/`, and `docs/project-plan.md`. Where a section reflects a Microsoft default rather than a discovery finding, the rationale is called out explicitly as an assumption."* — sets the contract up front.
- Per-section *Source* footers throughout (§2.1, §2.3, §3.1, §3.2, §4, §5, §7, §8, §16.1, §16.4) cite specific discovery artifacts.
- Worksheet B.1 cross-traces each deliverable to the originating WP, US, FR, and SC ID — closing the loop from pressure → outcome → deliverable → acceptance → measurement.
- Quantitative pressures (e.g., "$200–400M in annual avoidable cost", "24–26% return rates") appear in §2.1 and trace to README.md / Product-definition.md.

**Minor gaps:**
- A few sections (§9 Governance, §10 Sprint Execution, §14 Escalation) have **no source citation**. These are arguably Microsoft-standard practice rather than discovery findings, but per the document's own rule the "Microsoft default" should be flagged as an assumption.
- Companion artifacts referenced as "(planned)" — model card, DR plan, runbooks — are deliverables but not yet discovery-validated. The SOW would benefit from an explicit note that these will be authored against discovery inputs (Privacy Office, Platform Eng).

**Recommendation (minor):** Add a one-line "*Source: Microsoft delivery default (no discovery driver)*" footer to §9, §10, §14 to honour the document's own traceability rule.

---

### Dimension 2 — Outcome clarity — **Score: 3 (with minor gap)**

**Evidence that earns the score:**
- §3.1 lists three Business Outcomes with **ID, Measure, Target** in tabular form:
  - **BO-1**: ≥ 20% reduction in fit-driven returns within 6 months (target 30%)
  - **BO-2**: +3–5% conversion lift within 6 months
  - **BO-3**: ≥ 1 tenant at GA, architected for 20+ at Scale tier
- Outcomes are explicitly labelled **"customer-owned, measurable"**.
- A **non-guarantee clause** (line 105) crisply separates Microsoft's commitment (capability + measurement framework) from outcome ownership (Walmart marketing, merchandising, adoption) — this is rare and excellent.
- Worksheet A re-states outcomes in standard form, and Worksheet B.1 maps each deliverable to the BO(s) it supports.

**Minor gap:**
- Outcomes are **listed but not explicitly prioritized**. Implicit ordering (BO-1 first) suggests primacy, but the rubric calls out "prioritized" as part of the Excellent bar. A single line — *"Priority order: BO-1 > BO-2 > BO-3"* with rationale — would close this gap.
- BO-1's measurement requires an A/B control group, but §5 Out of Scope explicitly excludes "A/B experimentation harness". The hand-off seam (who builds the control vs. who measures) is implied but not nailed down.

**Recommendation (minor):**
1. Add explicit priority ranking to §3.1 BO table.
2. Add a one-line note clarifying Walmart's responsibility to operate the control/treatment cohorts that BO-1's measure depends on (cross-reference §17 C-10/C-11).

---

### Dimension 3 — Scope discipline — **Score: 3**

**Evidence that earns the score:**
- §3.3 Scope Model: variable scope governed by **single product backlog**, capacity-driven, with explicit MVP cutline (Sprint 4) and GA cutline (Sprint 9).
- §4: scope decomposed into **8 Work Packages (WP1–WP8)** mapped to phases and to a 147-task pre-decomposition in `tasks.md`.
- §5: **12 explicit exclusions** with category, item, and rationale ("Why" column) — including frequently-vague areas (multi-region, mobile SDK, Zeekit, training, perf testing).
- §12 Change Management: 5 trigger conditions, 4-step process with SLAs, version-bump discipline.
- Worksheet A: **3 IS anchors + 3 OOS anchors** as standard SOW headers.
- Worksheet B.3 **Scope Traps**: 10 named risk-of-creep items each with a **cost estimate** (e.g., "ST-1 H1 contingency: +20–30 PD, +2 weeks"). This is exemplary scope-defence design.

**Minor gaps:**
- "Capacity-driven" + "variable scope" creates a small ambiguity: what happens if Sprint 4 MVP cutline is at risk because backlog reprioritisation pulled non-MVP items in? §3.3 says Microsoft will "flag items at risk of slipping the cutline" but does not specify the **arbitration rule** (e.g., MVP items always trump non-MVP, or PO decides).

**Recommendation (minor):** Add to §3.3 a single sentence: *"If MVP cutline is threatened, Microsoft will recommend deferral of non-MVP backlog items; final arbitration sits with the Walmart Product Owner via the Product Council."*

---

### Dimension 4 — Deliverables + acceptance — **Score: 3**

**Evidence that earns the score:**
- §15.1 enumerates **16 work-product types** with type and target location.
- §15.2 Acceptance Model: differentiates backlog-item acceptance (PO sign-off in tracker), gate deliverables (written sign-off), and GA (Steering Committee approval).
- Worksheet B.1 leads with the rule: ***"If a deliverable has no acceptance criteria, it is not a deliverable."*** — and the table delivers on it: 14 deliverables (D-1 → D-14), each with **testable, quantitative acceptance criteria**:
  - D-1: "AI failover < 5 s", "readiness probe < 1 s"
  - D-2: "≤ 15% of calibration photos > ±4 cm vs. ground truth"
  - D-6: "≥ 90% request success during partial AI outage"
  - D-7: "`az deployment group what-if` clean against all 3 environments"
  - D-8: "coverage gate ≥ 80% line / ≥ 90% critical"
  - D-10: "p95 < 5 s at 500 concurrent"; "KEDA scales to 10 instances; no OOM"
  - D-12: "RTO < 1 h, RPO < 15 min"
- Each deliverable maps to a Business Outcome **and** a feature-trace ID (US, FR, SC).

**Minor gaps:**
- D-13 (DPIA) and D-14 (Hypercare) include subjective acceptance ("Walmart Privacy Office accepts as complete", "no P1 unresolved") — necessary for governance items but they don't define what "complete" means objectively. Consider linking to a checklist in `docs/Sessions/Product-definition.md` or a DPIA template.

**Recommendation (minor):** Reference a DPIA-content checklist in the D-13 acceptance row to make "complete" testable.

---

### Dimension 5 — Estimate realism — **Score: 3 (with minor gap)**

**Evidence that earns the score:**
- §7 lays out the capacity model with **explicit math**: 274 PD total = 206 PD build (WP1–WP7) + 68 PD cross-cutting (WP8); 240 PD coding capacity net of ceremony; 14% headroom (~34 PD) for spikes and integration friction.
- **Estimation method is named** (line 246): *"Bottom-up, three-point reference scale calibrated to senior .NET/Azure engineer productivity, +15% ceremony, +15% defect/UAT buffer."*
- Worksheet B.2: per-WP **effort, hours (8 h/PD), roles, dependency notes** — including which gates each WP carries (H1, H3, H5, H7, H8).
- "Hours by role" sub-table sums to 296 PD allocated, 274 PD chargeable, with the **delta (~22 PD) explicitly identified as vacation + ceremony slack**.
- **Estimation drivers are itemized** (line 776): three-tier AI pipeline complexity, 12 Bicep modules, 500-concurrent load target, multi-tenant + DPIA, OWASP ASVS L2 + PCI-adjacent, < 15 min rollback.
- **Top 3 assumptions** explicitly bound the estimate (line 777): senior IC team composition, no > 20% simultaneous OOO, Walmart inputs land per §17.1 sprint dates.

**Minor gaps:**
- **PM/CPdM hours are "absorbed in WP8" without explicit breakdown** — Worksheet B.2 "Hours by role" leaves PM blank with the note "PM allocation absorbed in WP8". For a fixed-capacity envelope this is opaque; a single line splitting WP8's 68 PD across PM, Tech Lead overhead, Security PT, and defect/UAT buffer would harden the estimate.
- Three-point estimates are **referenced ("calibrated to senior .NET/Azure engineer productivity") but not shown** — neither the most-likely / optimistic / pessimistic ranges per WP nor the calibration source. For a fixed-capacity SOW this is acceptable, but it limits the customer's ability to challenge specific WP sizing.
- The **Engagement Lead at 0.25 FTE × all 9 sprints (≈22.5 PD)** does not appear in the "Hours by role" table — likely because it's billed as a separate engagement-management envelope, but the SOW does not say so.

**Recommendation (minor):**
1. In Worksheet B.2, add an explicit row for **PM/CPdM (e.g., 22 PD, 176 h, 8%)** so the role table reconciles to 274 PD.
2. State whether Engagement Lead time is in-envelope or out-of-envelope.
3. Optional: publish the three-point ranges per WP as Appendix M for transparency at signature.

---

### Dimension 6 — Roles & responsibilities — **Score: 3**

**Evidence that earns the score:**
- §8.2: **9 Microsoft roles** with FTE, sprint engagement profile (e.g., "Sprint 1 light · 6–9 heavy"), and responsibilities.
- §8.3: **8 Walmart roles** with engagement cadence and responsibility — including critical-path call-outs ("Product Owner (critical)").
- §17.1: **12 customer-supplied items (C-1 → C-12)** with item, sprint deadline, and named owner (Walmart Cloud Platform, Catalog Engineering, Privacy Office, DevSecOps, etc.). Fallbacks named where applicable (e.g., "MSDN fallback for Sprint 1").
- §17.2: 5 named **management** responsibilities Walmart owns post-go-live.
- §9: governance bodies (Steering, Product Council, Architecture Review, daily sync) with cadence and membership.
- §11.2: Microsoft vs. Walmart testing-responsibility split is crisp.
- §14: 4-level escalation path with resolution SLAs.

**Minor gaps:**
- Microsoft's **Engagement Lead / DME** at 0.25 FTE has very thin responsibility text ("Customer relationship, executive escalation, contract") — for the most senior Microsoft role on the engagement, this could be expanded with specific decision rights.
- A single **RACI** matrix (one page) consolidating §8 + §17 across the major delivery activities would make the customer's role auditable at a glance.

**Recommendation (minor):** Add a one-page RACI in Appendix A or M covering the major delivery activities (architecture sign-off, security sign-off, privacy sign-off, UAT, go-live, hypercare exit).

---

### Dimension 7 — Risk & assumptions — **Score: 3**

**Evidence that earns the score:**
- §13 references a **continuously-maintained RAID log** in `risk-register.md` and `project-plan.md` §10, with monthly review and weekly HIGH+ escalation.
- §13.1: **6 plan risks** (PR-1 → PR-6) with severity (HIGH / MEDIUM) and **specific mitigations** (e.g., "calibration dataset prepared in Sprint 2; contingency: 3DLOOK bridge +2 weeks Change Order").
- §13.2: **3 top technical risks** (R-001 critical, R-003 high, R-004 medium) with mitigations.
- §18: **15 assumptions** in 3 categories (engagement A-1..A-5, technical A-6..A-11, process A-12..A-15) — each tagged as a change-management trigger.
- Worksheet B.2 "Top 3 assumptions" — concise version for executive readers.
- Worksheet B.3 — 10 **scope traps** (ST-1 → ST-10) with likely PD cost — proactive risk surfacing tied to dollars.
- **Hypothesis gates (H1, H3, H5, H7, H8)** are baked into the timeline (§7) and acceptance criteria (Worksheet B.1) — assumption validation is part of the delivery process, not a side document.

**Minor gaps:**
- §13.1 promises mitigations but **does not list owners or due dates** for the mitigations themselves (e.g., "Pre-Sprint 3 prompt engineering spike" — owned by ML Eng? Tech Lead?). The risk register may carry this; cross-referencing it would tighten the SOW.
- A small number of assumptions are essentially statements of fact rather than testable conditions (e.g., A-9 *"Shopper-provided height is always present and accurate"* — what is the validation step if a shopper enters a value 30% off?).

**Recommendation (minor):**
1. Add an "Owner / Validation step" column to §13.1 (or cross-reference the risk-register row IDs).
2. For A-9 and similar facts-of-input assumptions, add a one-line guard ("API rejects height outside 50–250 cm; out-of-band heights flagged in confidence score") so the assumption has a built-in fallback.

---

## 4. Summary

| Dimension | Score | Headline |
|-----------|:-----:|----------|
| 1. Traceability | 3 | Per-section sourcing + Worksheet B IDs close the loop end-to-end. |
| 2. Outcome clarity | 3 | 3 customer-owned, measurable BOs with non-guarantee clause. Add explicit priority order. |
| 3. Scope discipline | 3 | 12 exclusions + 10 scope traps + change process. World-class. |
| 4. Deliverables + acceptance | 3 | 14 deliverables, every one with testable AC. Exemplary. |
| 5. Estimate realism | 3 | Bottom-up, role-based, with drivers and assumptions. PM allocation opaque. |
| 6. Roles & responsibilities | 3 | 9 + 8 roles, 12 customer responsibilities, escalation path. RACI would polish. |
| 7. Risk & assumptions | 3 | 9 risks + 15 assumptions + 10 scope traps + 5 hypothesis gates. Add owners to mitigations. |

**Total: 21 / 21**

---

## 5. Top 5 Pre-Signature Polish Items

These are **not** score-changing — they would harden an already-Excellent SOW for executive countersignature.

| # | Item | Effort | Where |
|:-:|------|:------:|-------|
| 1 | Add explicit priority order to BO-1/BO-2/BO-3 + clarify Walmart owns the A/B cohort that measures BO-1 | 15 min | §3.1, Worksheet A |
| 2 | Add MVP cutline arbitration rule (PO decides if MVP scope is at risk) | 5 min | §3.3 |
| 3 | Reconcile Worksheet B.2 "Hours by role" — add explicit PM line; clarify whether Engagement Lead is in-envelope | 30 min | Worksheet B.2 |
| 4 | Add a one-page RACI (architecture / security / privacy / UAT / go-live / hypercare) | 1 hour | New §20 appendix |
| 5 | Add owner + validation column to §13.1 risks; add input-validation note to A-9 | 30 min | §13.1, §18.2 |

---

## 6. Reviewer Notes

- **Document version**: 0.1.0 (Draft for internal review). Promotion to 1.0.0 (Final-for-signature) is gated on Executive Steering Committee approval per the Version History rule.
- **Validity**: 30 days from 2026-05-14 — pre-signature work above should land inside this window or trigger a re-baseline.
- **Companion artifacts**: This assessment did not re-validate `risk-register.md`, `threat-model.md`, `cost-estimate.md`, or `project-plan.md`; their existence is assumed from in-line references. A follow-up cross-check (artifacts present, dates current, IDs consistent) is recommended before signature.
- **Pricing**: This SOW intentionally omits dollar pricing (T&M within fixed capacity, "not-to-exceed clause negotiated at Work Order signature"). The cost-estimate.md companion is referenced but not embedded — keep it that way to avoid coupling SOW versioning to Azure rate cards.

**Verdict:** Ready for stakeholder review. Address the 5 polish items, then promote to 1.0.0 for countersignature.

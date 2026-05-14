# SOW Assessment Report — OLR Control Room (ExxonMobil)

**Date:** 2026-05-14
**Assessor:** Copilot CLI (Claude Opus 4.6)
**SOW Document:** `docs/OLR-ControlRoom-SOW_Fictitious.pdf` (v1.1 Amended, 20 pages)
**Rubric Source:** EX3 Discovery-to-Delivery SOW scoresheet (7 dimensions, 0–3 scale)

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

## 2. Score Card

| # | Dimension | Score | Confidence |
|--:|-----------|:-----:|:----------:|
| 1 | Traceability to discovery | **2** | High |
| 2 | Outcome clarity | **2** | High |
| 3 | Scope discipline | **3** (with caveats) | Medium-High |
| 4 | Deliverables + acceptance | **2** | High |
| 5 | Estimate realism | **2** | Medium |
| 6 | Roles & responsibilities | **3** | High |
| 7 | Risk & assumptions | **3** | High |
| | **Total** | **17 / 21** | — |

---

## 3. Detailed Findings

### Dimension 1 — Traceability to discovery — **Score: 2**

**What earns credit:**
- §2.1 explicitly ties the engagement to five pressures identified during discovery ("Capital Triple-Lock", "Pioneer synergy run-rate", "declining Low-Carbon Wallet", "methane attribution", "process-safety trend").
- §3.1 maps to eight customer-owned outcomes (O1–O8) with specific attribution to pressures (P1–P5).
- The document references an external "OLR Control Room reference site" with Traceability, Deliver, Decide, Defend, and Concepts tabs.
- §22 includes an EX3 Compliance Map showing where each required section is addressed.

**Why it misses Excellent (3):**
- **Heavy reliance on external references that are not self-contained in the SOW.** The document constantly points to "the OLR site Deliver tab", "Schedule H snapshot", "Traceability tab" — a reviewer cannot assess traceability without access to those external systems. Reviewer comment [BL1] explicitly flags: *"I don't [like] so many references to external document/tabs that I have to hunt down. The SOW needs to be complete and/or the other documents attached in an appendix?"*
- The discovery pressures and outcomes are named but **not quantified in the SOW body** (e.g., what is the measurable target for O1 "Earnings growth to 2030"? The $15.6B figure is historical context, not a forward target).
- WBS leaves (60 items) are referenced but not reproduced; the SOW directs readers to Schedule C which "mirrors Deliver tab" — circular reference.

**Recommendation:** Inline the critical traceability data (outcome measures + targets, at minimum a summary WBS) rather than relying solely on an external reference site. Attach Schedule H as a binding appendix at signing.

---

### Dimension 2 — Outcome clarity — **Score: 2**

**What earns credit:**
- Eight outcomes (O1–O8) are defined, with four (O1, O3, O4, O5) contracted under this amendment.
- Outcomes are explicitly labelled "customer-owned".
- Non-guarantee clause is present (§3.1): outcomes depend on backlog priority, data availability, third-party readiness, and adoption.
- Each outcome maps to a pressure (P1–P5), providing strategic linkage.

**Why it misses Excellent (3):**
- **Outcomes are not measurable as stated in the SOW.** O1 is "Sustain earnings growth to 2030" — but what is the specific target? O3 is "per-well cycle-time and cost gap closure" — but what is the measure, baseline, and target?
- Reviewer comment [BL2]: *"Where are O1, O3, etc… defined?"* — the outcomes are asserted by label only; definitions and metrics live externally.
- **No explicit prioritization** between the four in-scope outcomes (O1, O3, O4, O5). Are they equal? If capacity runs out at 80%, which survives?
- The "headline three" in §3.1 are well-articulated as narrative but lack the tabular **ID / Measure / Target** structure that makes outcomes testable.

**Recommendation:**
1. Add a table: ID | Outcome | Measure | Baseline | Target | Owner.
2. Explicitly prioritize (e.g., O1 > O3 > O4 > O5) with a tiebreaker rule if capacity is at risk.
3. Define what "customer-owned" means operationally (who reports? what cadence?).

---

### Dimension 3 — Scope discipline — **Score: 3 (with caveats)**

**What earns credit:**
- §5 Out of Scope is extensive: 13 explicit exclusions, including the critical OT closed-loop control prohibition (ADR-09).
- §12 Change Management is robust: trigger conditions, 3-business-day decision SLA, escalation path, and a **Change Order Log** (CR-01 through CR-14) showing how scope has been actively managed.
- §3.3 "Scope is variable, governed by backlog prioritisation" + "Delivery is capacity-driven: 14,500 hours" — clear model.
- §12.4 documents the scope *narrowing* (P2, P4, P5 moved out) — disciplined descoping.
- Scope traps are named (§13): 5 specific items that can expand hours.
- "Probe-set additions do not require a Change Order" — micro-boundary clarity.

**Caveats:**
- Out-of-scope numbering starts at 4, not 1 (reviewer comment [BL3]) — formatting error that could cause contractual ambiguity.
- The scope boundary between "assurance constraint" (safety, audit) and "value-delivery commitment" is novel and well-explained but could trip up less technical readers.

**Recommendation:** Fix the §5 numbering (start at 1). Add a one-line rule: *"If an item is not in §4 or a signed Change Order, it is out of scope."*

---

### Dimension 4 — Deliverables + acceptance — **Score: 2**

**What earns credit:**
- §15.2 lists 16 named deliverables (D-01 → D-16) with Outcome Supported, Acceptance Criteria, and Phase columns.
- Several deliverables have strong testable criteria: D-02 requires "no write paths detected in a 7-day audit"; D-07 requires "SLO-07 100% pass in drill"; D-13 requires "freshness ≤ 14 days".
- Two deliverables (D-08, D-09) are explicitly marked DEFERRED with scope reference — honest and clean.
- §15.3 Validation Model distinguishes sprint-validated vs. formal-acceptance items.

**Why it misses Excellent (3):**
- **Several acceptance criteria are vague or dependent on undefined external references:**
  - D-01: "Policy assignments green; baseline scorecard ≥ 95%" — what scorecard? What constitutes "green"?
  - D-04: "10 named queries return cited responses" — but the queries aren't listed here or in a referenced appendix.
  - D-05: "KPI parity demonstrated" — parity with what baseline?
  - D-06: "Weighted criteria, alternatives, consequences attested" — this describes format, not a testable pass/fail.
- **No deliverable-level effort allocation.** §15.4 gives WP-level hours but doesn't map to D-01..D-16 — can't tell if a specific deliverable is adequately resourced.
- Reviewer comment [MR5] on §7: *"What is v1 being referred to?"* — unclear baseline for the capacity delta.

**Recommendation:**
1. For each deliverable, define a binary pass/fail gate (or reference a numbered NFR/SLO that provides one).
2. Provide a deliverable → WP cross-reference so effort allocation is traceable.
3. Inline or attach the "10 named queries" for D-04 as an appendix.

---

### Dimension 5 — Estimate realism — **Score: 2**

**What earns credit:**
- §7 provides phase-based capacity: Mobilize 700h, MVP 5,400h, GA 7,200h, Hypercare 1,900h = 14,500h total.
- §15.4 breaks hours into 9 work packages with roles and notes.
- §8.2 provides role-level indicative hours that sum correctly (spot-checked: ~7,800h for named roles + "remaining balance" to 14,500h).
- Capacity increase (CR-11: +3,220h, +28.5%) is documented with rationale (4-site footprint expansion).
- Assumptions §18 enumerate 12 conditions that make the estimate true.
- Commercial terms (§20.1) provide fee ranges by phase ($4.13M–$5.08M total).

**Why it misses Excellent (3):**
- **"Remaining specialist roles" in §8.2 are vaguely capped at "remaining balance within 14,500-hour total"** — ~6,700h with no role breakdown. This is nearly half the engagement unattributed at role level.
- **Estimation method is not stated.** Was this top-down, bottom-up, analogous? Three-point? What productivity assumptions?
- **No explicit estimation drivers** (e.g., "28 components × average build hours" or "4 sites × per-site rollout template"). The *what* is clear (14,500h) but the *how-we-got-there* is opaque.
- Reviewer comment [BL4]: *"Where is this calculated from / shown?"* — the +3,220h delta is asserted without a visible breakdown.
- **No headroom / contingency buffer** explicitly called out (unlike the VirtualMirror SOW's 14% headroom).

**Recommendation:**
1. Add an "Estimation drivers and method" paragraph explaining how 14,500h was derived.
2. Break "remaining specialist roles" into named categories with indicative ranges.
3. Explicitly call out contingency (e.g., "WP-8 Sprint Mechanics includes 10% buffer for integration friction").

---

### Dimension 6 — Roles & responsibilities — **Score: 3**

**What earns credit:**
- §8.2 defines **6 Customer roles** with clear responsibilities and **12+ Microsoft roles** with indicative hours each.
- §17 Customer Responsibilities is comprehensive: 9 "Provide" items and 5 "Manage" items, including OT-specific requirements (OIMS attestation, ExpressRoute commissioning, two-deep staffing).
- DEL-17 (Operational Handoff) has **7 explicit completion criteria** that operationalize what "done" means for the customer.
- Structural model (§8.1) clearly separates Executive Steering, Product Council, and Delivery pods.
- Two-deep pairing model makes knowledge-transfer expectations concrete from Sprint 1.
- Governance bodies (§9) have defined cadence and function.

**Minor gaps:**
- Customer "two-deep technical staff" responsibility is named but no sprint deadline is given (beyond "by MVP start T+3") — could be tighter.
- No RACI matrix — roles are clear narratively but a single-page RACI would aid at-a-glance review.

**Recommendation:** Add a one-page RACI covering the major gates (ADR ratification, OIMS attestation, DR drill, DEL-17 sign-off).

---

### Dimension 7 — Risk & assumptions — **Score: 3**

**What earns credit:**
- §13 lists **10 named risks** (RSK-WORK-01..04, RSK-SEC-01, RSK-CAPC-01, RSK-PEOPLE-01, RSK-ADR-01, RSK-COST-01..02, RSK-REG-01) with Severity, Mitigation, and Owner columns.
- The full risk register (28 risks) is maintained live and referenced.
- **5 scope traps** are explicitly named with expansion-risk narrative.
- §18 lists **12 assumptions** that are explicitly tagged as change-management triggers.
- Change Order Log (§12.4) demonstrates active risk/scope management — risks have already materialized and been formally handled (CR-02, CR-11, CR-14).
- ADR-09 (OT boundary) has its own **5 detection controls (DET-01..05)** with mechanism and evidence — this is exemplary risk-driven design.
- Cost risk has a named guardrail (NFR-14) with a FinOps Hub monitoring mechanism.

**Minor gaps:**
- Risk severity uses a compact notation (e.g., "H/LH", "H/LM", "M/M") that is **never defined** in the SOW or glossary. Presumably Likelihood/Impact but the encoding is opaque.
- No explicit risk-review cadence stated (though Product Council bi-weekly implicitly covers this).

**Recommendation:**
1. Add a legend for the severity notation (e.g., "H/LH = High severity / Low-High likelihood").
2. Add one line: "RAID log reviewed at every Product Council (bi-weekly)."

---

## 4. Summary

| Dimension | Score | Headline |
|-----------|:-----:|----------|
| 1. Traceability | 2 | Strong pressure/outcome mapping but too dependent on external reference site; not self-contained |
| 2. Outcome clarity | 2 | Outcomes named and customer-owned but lack measurable targets and explicit prioritization |
| 3. Scope discipline | 3 | Excellent: 13 exclusions, active Change Order log, scope traps named, ADR-09 boundary crisp |
| 4. Deliverables + acceptance | 2 | 16 named deliverables but several acceptance criteria are vague or reference undefined externals |
| 5. Estimate realism | 2 | Capacity and phases are clear; role/WP hours provided; but method unstated, ~47% of hours unattributed by role |
| 6. Roles & responsibilities | 3 | Comprehensive Microsoft + Customer roles with DEL-17 exit criteria; two-deep model is strong |
| 7. Risk & assumptions | 3 | 10 risks with owners + mitigations; 12 assumptions as triggers; 5 scope traps; active CR log |

**Total: 17 / 21**

---

## 5. Top Remediation Items (to reach 21/21)

| # | Gap | Fix | Effort | Target Score |
|:-:|-----|-----|:------:|:------------:|
| 1 | Outcomes not measurable in the SOW | Add table: ID / Measure / Baseline / Target / Owner for O1, O3, O4, O5 + explicit priority ranking | 1–2 hours | Outcome clarity → 3 |
| 2 | SOW not self-contained (external site dependency) | Inline critical traceability (outcome targets, WBS summary, "10 named queries") or mandate Schedule H attached at signature | 2–3 hours | Traceability → 3 |
| 3 | Acceptance criteria vague on D-01, D-04, D-05, D-06 | Define binary pass/fail for each (reference specific NFR/SLO numbers with quantitative thresholds) | 1–2 hours | Deliverables → 3 |
| 4 | Estimation method not stated; ~47% of hours unattributed | Add estimation-method paragraph; break "remaining specialist roles" into categories; call out contingency | 1–2 hours | Estimate realism → 3 |
| 5 | Formatting / clarity defects | Fix §5 numbering (start at 1); define risk severity notation; clarify "v1" reference in §7 | 30 min | Polish |

---

## 6. Comparison with VirtualMirror SOW

| Dimension | VirtualMirror (v0.3.0) | OLR Control Room (v1.1) | Delta |
|-----------|:----------------------:|:-----------------------:|:-----:|
| Traceability | 3 | 2 | -1 |
| Outcome clarity | 3 | 2 | -1 |
| Scope discipline | 3 | 3 | 0 |
| Deliverables + acceptance | 3 | 2 | -1 |
| Estimate realism | 3 | 2 | -1 |
| Roles & responsibilities | 3 | 3 | 0 |
| Risk & assumptions | 3 | 3 | 0 |
| **Total** | **21** | **17** | **-4** |

The OLR SOW is a strong enterprise document with excellent scope discipline and risk management, but its reliance on external references and lack of measurable outcome targets prevent it from reaching the "Excellent" bar across all dimensions. The VirtualMirror SOW is more self-contained and uses explicit quantitative acceptance criteria throughout.

---

## 7. Reviewer Comments Noted in the Document

The PDF contains several reviewer comments (likely from a prior review pass) that align with the gaps identified above:

| Comment | Reviewer | Issue |
|---------|----------|-------|
| [BL1] | BL | Too many references to external tabs/documents; SOW should be self-contained |
| [BL2] | BL | Where are O1, O3, etc. defined? Why talking about amendment when this is initial SOW? |
| [BL3] | BL | §5 numbering starts at 4, not 1 |
| [BL4] | BL | Where is the +3,220h calculated from / shown? |
| [MR5] | MR | What is "v1" being referred to? |
| [BL6] | BL | Difference between ADR and ADR-09 unclear |

These comments corroborate the assessment findings and suggest the document has not yet completed its internal review cycle.

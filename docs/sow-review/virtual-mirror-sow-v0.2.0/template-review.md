# Template Review — Virtual-Mirror-SOW.md Against SOW-Agile v1.3.2

| Field                     | Value                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Document under review** | [docs/Virtual-Mirror-SOW.md](../../Virtual-Mirror-SOW.md) v0.2.0 (2026-05-14, Draft for internal review)                                                                                                                                                                                                                                                                                                                               |
| **Template reference**    | [docs/Inputs/SOW-Agile_v1.3.2.md](../../Inputs/SOW-Agile_v1.3.2.md), converted from `SOW-Agile_v1.3.2(WW)(English)(May2026).docx`                                                                                                                                                                                                                                                                                                      |
| **Review scope**          | Structural fit to the Microsoft Agile Sprint Delivery SOW template, fixed-capacity / variable-scope language, delivery approach, testing and defect remediation, sprint and project completion, project organization, governance, exhibits, technology / environment requirements, customer responsibilities, project assumptions, and template hygiene.                                                                               |
| **Reviewer**              | Microsoft ISD — SOW Template Review                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Review date**           | 2026-05-14                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **Verdict**               | **Conditional Pass.** The SOW is materially stronger than the base template in traceability, delivery planning, technical specificity, and risk articulation. However, several template-alignment issues should be corrected before signature, especially the work-products acceptance model, completion language, section mapping to the Agile template, technology / environment tables, and template-required AI usage assumptions. |
| **Cross-references**      | [technical-review.md](technical-review.md) · [compliance-and-security-review.md](compliance-and-security-review.md)                                                                                                                                                                                                                                                                                                                    |

---

## 1. Severity Legend

**v0.2.0 delta**: The update improves several template-facing concerns: business objectives are prioritized, MVP cutline arbitration is explicit, plan risks have owners and validation steps, PM / CPdM capacity is reconciled, and a decision-rights RACI was added. The remaining blockers are now narrower but still signature-relevant: fixed-capacity / variable-scope wording, defect remediation over-commitment, formal acceptance language for Agile work products, template technology / environment tables, and May 2026 AI Usage assumptions.

|     Severity      | Definition                                                                                                                                                       | Action                                                          |
| :---------------: | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
|   **Critical**    | Direct conflict with the Agile SOW template's commercial model or creates acceptance / delivery obligations inconsistent with fixed capacity and variable scope. | Must fix before signature.                                      |
|     **High**      | Important template requirement or deal-shaping guardrail is missing, ambiguous, or materially altered.                                                           | Fix before final-for-signature or obtain RMQA / legal approval. |
|    **Medium**     | Template section exists but should be reworked for clearer alignment, cleaner customer expectations, or better reviewability.                                    | Resolve in the next SOW draft.                                  |
|      **Low**      | Style, terminology, cross-reference, or template-hygiene issue.                                                                                                  | Track for polishing before v1.0.0.                              |
| **Informational** | Stronger-than-template practice or optional improvement.                                                                                                         | No blocking action.                                             |

---

## 2. Findings Summary

|  #   | Template section                          | Finding                                                                                                                                                                                 |   Severity   | SOW section(s)       |
| :--: | ----------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------: | -------------------- |
| T-1  | Opening SOW / WO paragraph                | The SOW does not include the template's standard Work Order anchoring paragraph and party shorthand definitions.                                                                        |   **High**   | Header, §1           |
| T-2  | §1 Project objectives and scope           | The SOW uses a custom 23-section structure instead of preserving the template's master section order.                                                                                   |  **Medium**  | All sections         |
| T-3  | §1.2 Customer desired business objectives | The SOW is strong on business outcomes, but should more explicitly preserve the template's “desired objectives are not fixed scope” language.                                           |   **High**   | §3.1, Worksheet A    |
| T-4  | §1.3 Targeted scope (Epics)               | Work packages are detailed and useful, but they read closer to committed deliverables than variable epics.                                                                              |   **High**   | §4, Worksheet B      |
| T-5  | §1.4 Areas out of scope                   | Out-of-scope coverage is strong, but some default exclusions should be mirrored or intentionally removed with rationale.                                                                |  **Medium**  | §5                   |
| T-6  | §2.1 Delivery overview                    | Delivery overview mostly aligns, but template key tenets such as automation strategy, zero-downtime deployment, DOR / DOD / ORC / BWBM should be explicitly tied to the SOW.            |  **Medium**  | §6, §10, §11         |
| T-7  | §2.2 Delivery approach                    | The SOW's sprint plan is stronger than the template, but customer activities / dependencies are split across sections rather than presented phase-by-phase.                             |  **Medium**  | §6, §7, §17          |
| T-8  | §2.3 Testing and defect remediation       | Defect remediation language conflicts with the template's default stance for Agile delivery: P3/P4 are logged, not automatically remediated.                                            | **Critical** | §11.3                |
| T-9  | §2.4 Sprint completion                    | The SOW introduces written sign-off for phase and gate deliverables; this conflicts with the template guidance that Agile work products should generally not require formal acceptance. | **Critical** | §15.2, Worksheet B   |
| T-10 | §2.5 Project completion                   | Completion criteria are close, but planned completion path may imply outcome / go-live acceptance beyond consumed capacity or term expiry.                                              |   **High**   | §19                  |
| T-11 | §2.6 Timeline                             | Timeline is well specified, but should repeat the template's “estimate only; capacity drives timeline” language next to the sprint table.                                               |  **Medium**  | §7                   |
| T-12 | §3.1 Project capacity                     | Capacity is detailed, but the SOW should state that capacity is defined in the Work Order and changes require change management.                                                        |   **High**   | §7, Worksheet B.2    |
| T-13 | §3.2 Project staffing                     | Staffing is more specific than template, but several template roles are renamed or omitted without an explicit mapping.                                                                 |  **Medium**  | §8                   |
| T-14 | §3.3 Executive steering committee         | ESC exists but membership and authority should be mapped to the template role table.                                                                                                    |   **Low**    | §8, §9, §20.1        |
| T-15 | §3.4 Product council                      | Product Council is appropriate, but the base template says to remove it for smaller projects; retain with justification.                                                                |   **Low**    | §9                   |
| T-16 | §3.5 Feature team                         | Feature-team model is present, but the SOW should explicitly state the autonomous / empowered feature-team principle from the template.                                                 |   **Low**    | §8, §10              |
| T-17 | §4 Project governance                     | Governance is strong, but weekly risk reassessment from the template should be reflected consistently.                                                                                  |   **Low**    | §9, §13              |
| T-18 | §4.3 Change management process            | Change process is concise but omits key template language: no obligation to start changed work until fee / schedule impact is signed.                                                   |   **High**   | §12                  |
| T-19 | §4.4 Escalation path                      | Escalation path is clear, but differs from the template escalation sequence; acceptable if intentional.                                                                                 |   **Low**    | §14                  |
| T-20 | §5.1 Initial targeted product backlog     | The SOW references the full 147-task backlog; template guidance says stay at epic / feature level.                                                                                      |   **High**   | §4, §20, Worksheet B |
| T-21 | §5.2 Customer-specific documentation      | Supporting artifacts are listed well, but the SOW should identify which documents are attachments vs. repository references.                                                            |  **Medium**  | §20                  |
| T-22 | §6.1 Definitions and acronyms             | Glossary is strong but should be scrubbed for only terms actually used.                                                                                                                 |   **Low**    | §20 Glossary         |
| T-23 | §6.2 Technology requirements              | The SOW has a stack table but not the template's product / version / ready-by technology requirements table, including GitHub Copilot assumptions.                                      |   **High**   | §16.1, §18           |
| T-24 | §6.3 Environment requirements             | Environment section lacks the template's columns for location, responsible party for configuration / maintenance, subscription ownership, and ready-by date.                            |   **High**   | §16.2                |
| T-25 | §6.4 Customer responsibilities            | Customer responsibilities are strong, but should include general template responsibilities and avoid duplicating project-specific items.                                                |  **Medium**  | §17                  |
| T-26 | §6.5 Project assumptions                  | AI Usage assumptions from the May 2026 template are not included; for an AI engagement this is a signature-grade gap.                                                                   | **Critical** | §18                  |
| T-27 | Template hygiene                          | The converted template includes instructional text; the final SOW is clean, but review should confirm no template placeholders remain.                                                  |   **Low**    | All sections         |

---

## 3. Detailed Findings

### T-1 — Missing Work Order anchoring paragraph · Severity: **High**

**Template master**: The Agile SOW template begins the customer-facing body with: “This Statement of Work (SOW) and any exhibits, appendices, schedules, and attachments to it are made pursuant to Work Order (WO) [insert WO number]...” and defines party shorthand such as Microsoft, Customer, and Project.

**Observation**: The VirtualMirror SOW has a strong Document Control section and states “Work Order reference TBD,” but it does not include the template's legal anchoring paragraph. That paragraph matters because it links the SOW to the WO and establishes that exhibits / appendices are part of the SOW package.

**Recommended fix**: Add a preamble immediately before or inside §1 Document Control:

> This Statement of Work (SOW) and any exhibits, appendices, schedules, and attachments to it are made pursuant to Work Order (WO) [TBD] and describe the services to be performed by Microsoft for Walmart Digital — Apparel & Marketplace relating to VirtualMirror AI — Clothing Fit Assessment Service (v1).

---

### T-2 — Custom section order vs. template master order · Severity: **Medium**

**Template master**: The template's canonical section order is:

1. Project objectives and scope
2. Delivery approach, completion and timeline
3. Project organization
4. Project governance
5. Exhibits
6. Appendix

**Observation**: The SOW expands these into 23 sections. That is readable for engineering stakeholders, but it makes template compliance review harder and may force reviewers to mentally map sections back to the official structure.

**Recommended fix**: Either restructure the SOW into the template's 6 master sections with nested subsections, or add a short mapping table in §1 showing how the custom sections map to the template sections. The mapping approach is lower-risk because it preserves the current content.

---

### T-3 — Desired objectives should be non-fixed scope · Severity: **High**

**Template master**: §1.2 states that desired objectives and initial backlog do not constitute fixed scope, and that not all objectives / backlog items may be completed within contracted capacity.

**Observation**: The SOW includes a good non-guarantee clause for BO-1 and BO-2, and a fixed-capacity / variable-scope statement. It should still include the exact template concept: desired objectives and initial backlog are planning inputs, not a fixed delivery commitment.

**Recommended fix**: Add explicit template-aligned wording to §3.1:

> The desired business objectives and any initial backlog items described in this SOW do not constitute fixed scope. There is no guarantee that all desired business objectives or all initial backlog items will be completed within contracted capacity. Walmart's Product Owner will prioritize the backlog against available capacity through the governance process.

---

### T-4 — Work packages read as committed deliverables rather than variable epics · Severity: **High**

**Template master**: §1.3 says targeted scope “might be revised at any time based on direction from Customer” and may include areas that are not built because they fall below the capacity cutline.

**Observation**: WP1–WP8 are useful, traceable, and detailed. However, “The build is organised into eight work packages” plus Worksheet B acceptance criteria may read as fixed scope. That creates tension with the Agile template.

**Recommended fix**: In §4 and Worksheet B, call WP1–WP8 “initial targeted epics / work packages used for baseline planning” and add that specific backlog items may be reprioritized, split, deferred, or removed by Walmart PO within capacity.

---

### T-8 — Defect remediation over-commits P3/P4 · Severity: **Critical**

**Template master**: §2.3 states P1 and P2 remediation are in scope; P3 and P4 are logged and remediated only through agreed change request unless otherwise negotiated.

**Observation**: §11.3 says P3 fixes are “Next sprint” and P4 fixes are “Backlog.” That may be interpreted as a commitment to remediate all P3/P4 defects within the SOW, which is broader than the template default.

**Recommended fix**: Revise §11.3 to align with the template:

| Priority | Remediation in scope?                                                               |
| -------- | ----------------------------------------------------------------------------------- |
| P1       | Yes, within available capacity and release gate constraints.                        |
| P2       | Yes, prior to production release where possible.                                    |
| P3       | Logged and prioritized; remediation only if capacity remains or via change request. |
| P4       | Logged; remediation via backlog prioritization or change request.                   |

Also clarify whether post-go-live defects are handled only during hypercare and only within business hours unless a managed-services SOW is signed.

---

### T-9 — Formal acceptance conflicts with Agile sprint-completion guidance · Severity: **Critical**

**Template master**: §2.4 says backlog items do not require formal sign-off or customer acceptance when completed by the feature team. Template guidance further warns: “Given that this is an Agile model there should be no work products requiring acceptance.” If work products require acceptance, standard deliverable acceptance language and RMQA review are required.

**Observation**: §15.2 requires written sign-off for phase and gate deliverables, security / privacy gates, and Executive Steering Committee approval for GA cutover. Worksheet B also defines deliverable-level acceptance criteria. This may be necessary for the engagement, but it is not neutral under the Agile SOW template.

**Recommended fix**: Choose one of two paths:

- **Preferred Agile template path**: Reframe H1/H3/H5/H7/H8/MVP/GA as sprint review work products and governance gates, not formal deliverables requiring acceptance.
- **Formal deliverable path**: Keep written sign-off, but add the standard deliverable acceptance language after Sprint Completion and route through RMQA / legal review.

The SOW should not remain halfway between both models.

---

### T-10 — Project completion language needs stronger capacity primacy · Severity: **High**

**Template master**: §2.5 says the project is complete when at least one condition is met: all capacity used, term expired, all activities / backlog completed, or WO terminated. It also states not all backlog items or objectives may be completed.

**Observation**: §19 includes capacity consumed and term expiry, but trigger 1 frames the planned completion path around Sprint 9 acceptance criteria, 100% canary, green SLO dashboard, and runbook sign-off. That is useful operationally but could be read as the primary contractual completion condition.

**Recommended fix**: Reorder §19 so capacity consumed / term expired / WO terminated are equal completion triggers, and explicitly state that failure to complete all Sprint 9 items does not prevent project completion if capacity or term is exhausted.

---

### T-12 — Capacity should point to the Work Order · Severity: **High**

**Template master**: §3.1 states that available capacity for each resource is specified in the WO and additional capacity is added through change management.

**Observation**: The SOW estimates 274 PD and provides role allocation, which is helpful. It does not explicitly state that the binding capacity is the capacity specified in the WO.

**Recommended fix**: Add to §7 or Worksheet B.2:

> The capacity available for each Microsoft resource is specified in the Work Order. If more capacity of any role is needed, it will be added through the change management process.

---

### T-18 — Change management lacks “no obligation to start changed work” language · Severity: **High**

**Template master**: §4.3 says Microsoft has no obligation to commence changed work until estimated fee and schedule impact are agreed in a written amendment signed by authorized signatories.

**Observation**: §12 has a good 4-step process, but it does not include the explicit no-obligation-to-start clause. That clause is important for scope containment.

**Recommended fix**: Add to §12.1 or §12.3:

> Microsoft has no obligation to commence work related to any requested change until the estimated fee and schedule impact are agreed in a written amendment signed by authorized signatories from both parties.

---

### T-20 — Initial backlog should stay at epic / feature level · Severity: **High**

**Template master**: §5.1 says the initial product backlog is optional and should stay at epic / feature level, not user-story level.

**Observation**: The SOW references `tasks.md` with 147 implementation tasks. This is excellent for engineering traceability, but if treated as SOW backlog it violates the template's guidance and may make individual tasks appear contractually committed.

**Recommended fix**: Keep WP1–WP8 in the SOW as the initial targeted backlog. Move the 147-task reference to “supporting implementation planning artifact only; not a contractual backlog commitment.”

---

### T-23 — Missing template technology requirements table and GitHub Copilot assumptions · Severity: **High**

**Template master**: §6.2 includes a “Product and technology item / Version / Ready by” table and May 2026 assumptions for GitHub Copilot usage, including customer consent and license availability.

**Observation**: §16.1 has a stack table but no ready-by table. The SOW also does not include the template's GitHub Copilot assumptions. Because this is a Microsoft ISD Agile template updated in 2026, this omission is visible.

**Recommended fix**: Add a §16.5 “Technology Requirements” table with at least Azure subscription, GitHub / Azure DevOps automation environment, GitHub Copilot Enterprise, .NET 8 SDK, Azure Cosmos DB Emulator, Azurite, and Foundry / Azure OpenAI access. Add AI / Copilot assumptions to §18.3 or a new §18.4.

---

### T-24 — Environment requirements table is missing template columns · Severity: **High**

**Template master**: §6.3 requires Environment, Location, Responsible for configuration and maintenance, Subscription ownership, Ready by.

**Observation**: §16.2 lists local/dev/staging/prod with purpose and owner. It should add the missing columns because they drive readiness and customer obligations.

**Recommended fix**: Replace or supplement §16.2 with:

| Environment | Location                           | Responsible for configuration and maintenance                | Subscription ownership | Ready by     |
| ----------- | ---------------------------------- | ------------------------------------------------------------ | ---------------------- | ------------ |
| Local dev   | Developer workstation / containers | Microsoft                                                    | Microsoft              | Sprint 1     |
| dev         | Microsoft Azure, East US 2         | Microsoft, with Walmart RBAC                                 | Walmart                | Sprint 1 / 2 |
| staging     | Microsoft Azure, East US 2         | Microsoft, with Walmart RBAC                                 | Walmart                | Sprint 7     |
| prod        | Microsoft Azure, East US 2         | Walmart owns operations; Microsoft deploys during engagement | Walmart                | Sprint 9     |

---

### T-26 — May 2026 AI Usage assumptions are missing · Severity: **Critical**

**Template master**: §6.5 includes May 2026 AI Usage language covering Microsoft use of AI Tools, ownership / confidentiality unchanged by AI use, telemetry, and removal of AI Tools installed or deployed in the customer environment at engagement conclusion. It also notes that AI projects are not eligible for PDOC.

**Observation**: The VirtualMirror SOW is itself an AI engagement, but §18 does not include the template's AI Usage assumptions. This is a signature-grade template gap.

**Recommended fix**: Add a dedicated §18.4 “AI Usage Assumptions” adapted from the template. At minimum:

- Microsoft may use Microsoft-developed or Microsoft-licensed AI Tools to perform the services.
- AI Tool use does not alter ownership, licensing, or confidential treatment of pre-existing work, data, confidential information, or service deliverables.
- Microsoft will comply with internal standards, privacy / security requirements, and Responsible AI principles.
- AI Tool execution telemetry may be generated and processed under the Microsoft Products and Services Data Protection Addendum.
- AI Tools installed or deployed in Walmart's environment will be removed at engagement conclusion unless otherwise agreed in writing.
- State whether this engagement is not PDOC-eligible due to AI scope.

---

## 4. Template Section-by-Section Assessment

| Template section                         | Fit assessment                                                             |   Severity    | Recommended action                                                                  |
| ---------------------------------------- | -------------------------------------------------------------------------- | :-----------: | ----------------------------------------------------------------------------------- |
| Opening SOW / WO paragraph               | Partially covered by Document Control; standard legal paragraph missing.   |   **High**    | Add WO anchoring paragraph and party definitions.                                   |
| 1.1 Introduction                         | Strong and customer-specific.                                              | Informational | Keep.                                                                               |
| 1.2 Customer desired business objectives | Strong, measurable, and prioritized; needs exact non-fixed-scope language. |   **High**    | Add template non-guarantee language for objectives and backlog.                     |
| 1.3 Targeted scope (Epics)               | Strong but too implementation-task oriented.                               |   **High**    | Keep WP1–WP8 as epics; demote 147 tasks to non-contractual planning artifact.       |
| 1.4 Areas out of scope                   | Strong project-specific exclusions.                                        |  **Medium**   | Mirror key default exclusions or document why omitted.                              |
| 2.1 Delivery overview                    | Mostly aligned.                                                            |  **Medium**   | Tie DOR, DOD, ORC, BWBM, automation, and zero-downtime strategy to SOW sections.    |
| 2.2 Delivery approach                    | Stronger than template; dependencies split across sections.                |  **Medium**   | Add phase-by-phase Customer activities or cross-reference §17.                      |
| 2.3 Testing and defect remediation       | Testing is robust; defect commitments exceed template default.             | **Critical**  | Rework P3/P4 remediation and clarify post-go-live hypercare boundary.               |
| 2.4 Sprint completion                    | Formal sign-offs conflict with Agile template guidance.                    | **Critical**  | Choose Agile work-product model or add formal acceptance language with RMQA review. |
| 2.5 Project completion                   | Close but planned completion path may dominate capacity / term triggers.   |   **High**    | Reorder and reinforce capacity / term completion triggers.                          |
| 2.6 Timeline                             | Detailed and useful.                                                       |  **Medium**   | Repeat “estimate only; capacity drives timeline” immediately above timeline.        |
| 3.1 Project capacity                     | Detailed estimates; WO capacity link missing.                              |   **High**    | State capacity is specified in the WO.                                              |
| 3.2 Project staffing                     | Strong role table.                                                         |  **Medium**   | Add mapping for template roles / omitted roles.                                     |
| 3.3 Executive steering committee         | Covered.                                                                   |      Low      | Add template role table or cross-reference RACI.                                    |
| 3.4 Product council                      | Covered and justified by scope.                                            |      Low      | State why Product Council is retained despite single feature team.                  |
| 3.5 Feature team                         | Covered.                                                                   |      Low      | Add autonomous / empowered feature-team wording.                                    |
| 4.1 Project communication                | Covered.                                                                   |      Low      | Keep.                                                                               |
| 4.2 Risk and issue management            | Covered; monthly vs weekly cadence differs.                                |      Low      | Align cadence wording.                                                              |
| 4.3 Change management process            | Good but missing no-obligation-to-start changed work.                      |   **High**    | Add template clause.                                                                |
| 4.4 Escalation path                      | Covered.                                                                   |      Low      | Keep, or map to template sequence.                                                  |
| 5.1 Initial targeted product backlog     | Overly detailed if 147 tasks are treated as SOW backlog.                   |   **High**    | Keep only epic / feature level in SOW.                                              |
| 5.2 Customer-specific documentation      | Covered through appendices.                                                |  **Medium**   | Distinguish attachments from repository references.                                 |
| 6.1 Definitions and acronyms             | Covered.                                                                   |      Low      | Scrub unused terms.                                                                 |
| 6.2 Technology requirements              | Stack present, template table missing.                                     |   **High**    | Add Product / Version / Ready-by table and GitHub Copilot assumptions.              |
| 6.3 Environment requirements             | Environment list present, template columns missing.                        |   **High**    | Add Location / Responsible / Subscription / Ready-by columns.                       |
| 6.4 Customer responsibilities            | Strong.                                                                    |  **Medium**   | Add general template responsibilities and avoid duplication.                        |
| 6.5 Project assumptions                  | Strong technical assumptions; template AI Usage missing.                   | **Critical**  | Add AI Usage assumptions.                                                           |

---

## 5. Recommended Changes Before Signature

### MUST-FIX

|  #  | Change                                                                                                                                                                     | Where                |
| :-: | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------- |
|  1  | Add the standard Work Order anchoring paragraph and party shorthand definitions.                                                                                           | Header / §1          |
|  2  | Add explicit template language that desired objectives and initial backlog are planning inputs, not fixed scope.                                                           | §3.1, Worksheet A    |
|  3  | Reframe WP1–WP8 as initial targeted epics / work packages and clarify they remain variable within contracted capacity.                                                     | §4, Worksheet B      |
|  4  | Rework defect remediation so P3/P4 are logged and prioritized, not automatically committed for remediation.                                                                | §11.3                |
|  5  | Resolve the formal acceptance conflict: either remove formal deliverable sign-off language or add standard deliverable acceptance language and obtain RMQA / legal review. | §15.2, Worksheet B   |
|  6  | Reorder / clarify project completion criteria so capacity consumed, term expiry, backlog completion, and WO termination are equal completion triggers.                     | §19                  |
|  7  | State that binding resource capacity is specified in the Work Order and additional capacity requires change management.                                                    | §7, Worksheet B.2    |
|  8  | Add the template no-obligation-to-start-changed-work clause.                                                                                                               | §12                  |
|  9  | Treat `tasks.md` 147 tasks as non-contractual implementation planning detail, not SOW-level backlog commitment.                                                            | §4, §20, Worksheet B |
| 10  | Add the template-format technology requirements table with Product / Version / Ready-by columns.                                                                           | §16                  |
| 11  | Add the template-format environment requirements table with Location / Responsible / Subscription ownership / Ready-by columns.                                            | §16.2                |
| 12  | Add May 2026 AI Usage assumptions, including AI Tools, telemetry, confidentiality / ownership preservation, and tool removal at engagement conclusion.                     | §18                  |

### SHOULD-FIX

|  #  | Change                                                                                                                                                   | Where        |
| :-: | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ |
|  1  | Add a template mapping table from the SOW's 23 custom sections to the 6 Agile template master sections.                                                  | §1           |
|  2  | Mirror default out-of-scope categories where applicable or document why each is intentionally omitted.                                                   | §5           |
|  3  | Add DOR, DOD, ORC, BWBM, automation, and zero-downtime deployment references in the delivery overview.                                                   | §6, §10, §11 |
|  4  | Add a phase-by-phase table showing Microsoft activities and key Walmart activities, matching template Table 4.                                           | §6 / §17     |
|  5  | Add role mapping from template roles to the SOW's named roles, including CPdM / PM, DME, Service Delivery Manager if applicable, and feature-team roles. | §8           |
|  6  | Align risk review cadence language: template says active issues and risks are monitored and reassessed every week.                                       | §13          |
|  7  | Identify appendix references that are actual SOW attachments vs. repository-only supporting material.                                                    | §20          |
|  8  | Add general Customer responsibilities from the template without duplicating project-specific C-1 through C-12.                                           | §17          |

### NICE-TO-HAVE

|  #  | Change                                                                                                                                           | Where                       |
| :-: | ------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------- |
|  1  | Preserve current 23-section format but add parenthetical template section labels to headings.                                                    | All headings                |
|  2  | Add a short “Template deviations approved” table for reviewer traceability.                                                                      | §1 or §20                   |
|  3  | Scrub glossary so it includes only acronyms used in the SOW.                                                                                     | §20 Glossary                |
|  4  | Convert Worksheet A and B into explicit exhibits under the template §5 heading.                                                                  | Worksheet A / B             |
|  5  | Add final pre-send checklist: no placeholders, no instructional text, refreshed table of contents, spelling review, document properties updated. | Version History or appendix |

---

## 6. Version History

| Version | Date       | Author                              | Status | Summary of changes                                                                                                                                                                                                                                                          |
| ------: | ---------- | ----------------------------------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|   0.1.0 | 2026-05-14 | Microsoft ISD — SOW Template Review | Draft  | Initial template-alignment review using SOW-Agile v1.3.2 section order as the master structure.                                                                                                                                                                             |
|   0.2.0 | 2026-05-14 | Microsoft ISD — SOW Template Review | Draft  | Re-ran template-alignment findings against Virtual-Mirror-SOW.md v0.2.0; acknowledged improvements to business objective priority, MVP cutline arbitration, risk ownership, capacity reconciliation, D-13 acceptance, and RACI while retaining remaining template blockers. |

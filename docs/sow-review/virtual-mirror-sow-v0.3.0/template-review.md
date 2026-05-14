# Template Review - Virtual-Mirror-SOW.md v0.3.0 Against SOW-Agile v1.3.2

| Field | Value |
| ----- | ----- |
| **Document under review** | [docs/Virtual-Mirror-SOW.md](../../Virtual-Mirror-SOW.md) v0.3.0 (2026-05-14, Draft for internal review) |
| **Template reference** | [docs/Inputs/SOW-Agile_v1.3.2.md](../../Inputs/SOW-Agile_v1.3.2.md), converted from `SOW-Agile_v1.3.2(WW)(English)(May2026).docx` |
| **Review scope** | Microsoft Agile SOW template alignment, fixed-capacity / variable-scope language, delivery approach, sprint completion, defect remediation, formal acceptance, capacity, governance, technology / environment tables, assumptions, AI Usage language, and document hygiene. |
| **Reviewer** | Microsoft ISD - SOW Template Review |
| **Review date** | 2026-05-14 |
| **Verdict** | **Conditional Pass.** v0.3.0 resolves the header / Section 1 version mismatch and improves backlog-driven delivery language, but several Agile SOW template blockers remain before final-for-signature. Critical blockers remain around P3/P4 remediation language, formal acceptance gates, and missing May 2026 AI Usage assumptions. |
| **Master structure used** | The source SOW-Agile v1.3.2 template is the master for this review. Findings are organized against the template's original section order, not the SOW's custom 23-section order. |
| **Cross-references** | [technical-review.md](technical-review.md) - [compliance-and-security-review.md](compliance-and-security-review.md) |

---

## 1. Severity Legend

| Severity | Definition | Action |
| :------: | ---------- | ------ |
| **Critical** | Direct conflict with the Agile SOW template's commercial model or creates acceptance / delivery obligations inconsistent with fixed capacity and variable scope. | Must fix before signature. |
| **High** | Important template requirement or deal-shaping guardrail is missing, ambiguous, or materially altered. | Fix before final-for-signature or obtain RMQA / legal approval. |
| **Medium** | Template section exists but should be reworked for clearer alignment, cleaner customer expectations, or better reviewability. | Resolve in the next SOW draft. |
| **Low** | Style, terminology, cross-reference, or template-hygiene issue. | Track for polishing before v1.0.0. |
| **Informational** | Stronger-than-template practice or optional improvement. | No blocking action. |

---

## 2. v0.3.0 Delta

The previously observed header / Section 1 version mismatch is now resolved: both fields show `0.3.0`. However, the Version History still does not include a `0.3.0` row, so the document does not explain what changed in v0.3.0. That remains a signature-readiness gap because the SOW uses semantic versioning and says post-signature changes are reflected in the version table.

The SOW also improves defect-management context by adding that remediation is backlog-driven within sprint capacity. However, the P3/P4 table still says `Next sprint` and `Backlog`, which can still be read as a remediation commitment unless tied clearly to capacity and change management.

---

## 3. Findings Summary

| # | Template master section | Finding | Severity | SOW section(s) |
| :-: | ----------------------- | ------- | :------: | -------------- |
| T-1 | Opening SOW / WO paragraph | Standard Work Order anchoring paragraph and party shorthand definitions are still incomplete. | **High** | Header, Section 1 |
| T-2 | Section 1 - Project objectives and scope | The SOW uses a custom 23-section structure without a mapping table to the Agile template master sections. | **Medium** | All sections |
| T-3 | Section 1.2 - Customer desired business objectives | Desired business objectives are strong but should preserve template language that objectives / backlog are not fixed scope. | **High** | Section 3.1, Worksheet A |
| T-4 | Section 1.3 - Targeted scope (Epics) | WP1-WP8 still read like committed deliverables rather than variable targeted epics. | **High** | Section 4, Worksheet B |
| T-5 | Section 2.3 - Testing and defect remediation | P3/P4 still risk over-commitment despite new backlog-driven caveat. | **Critical** | Section 11.3 |
| T-6 | Section 2.4 - Sprint completion | Tier-2 formal acceptance gates remain in tension with the Agile template guidance that work products generally should not require formal acceptance. | **Critical** | Section 15.2, Worksheet B |
| T-7 | Section 2.5 - Project completion | Completion criteria are improved but still need stronger capacity / term primacy. | **High** | Section 19 |
| T-8 | Section 3.1 - Project capacity | Binding capacity should be explicitly tied to the Work Order, with changes through change management. | **High** | Section 7, Worksheet B.2 |
| T-9 | Section 4.3 - Change management process | Missing explicit no-obligation-to-start-changed-work-until-signed clause. | **High** | Section 12 |
| T-10 | Section 5.1 - Initial targeted product backlog | The 147-task implementation plan reference can still be read as SOW-level committed backlog. | **High** | Section 4, Section 20, Worksheet B |
| T-11 | Section 6.2 - Technology requirements | Technology table exists but still lacks enough template-grade product/version/SKU clarity and includes unresolved Azure service names. | **High** | Section 16.1 |
| T-12 | Section 6.3 - Environment requirements | Environment table lacks template columns for location and ready-by date. | **High** | Section 16.2 |
| T-13 | Section 6.5 - Project assumptions | May 2026 AI Usage assumptions are not present as a dedicated template clause. | **Critical** | Section 18 |
| T-14 | Version History | Version History has no `0.3.0` row even though the SOW header and Section 1 are v0.3.0. | **High** | Version History |

---

## 4. Detailed Findings By Template Master Section

### Opening SOW / Work Order Paragraph

#### T-1 - Work Order anchoring paragraph and party definitions still incomplete - Severity: **High**

**Template master**: The Agile SOW template begins the customer-facing body with a standard paragraph: the SOW and all exhibits, appendices, schedules, and attachments are made pursuant to a Work Order, and the paragraph defines party shorthand such as Microsoft, Customer, and Project.

**v0.3.0 observation**: Section 1 now includes a `Work Order reference` field and a master-agreement precedence sentence. That is an improvement. However, it still does not fully mirror the template's standard SOW / WO anchoring paragraph or state that exhibits, appendices, schedules, and attachments are part of the SOW package.

**Required fix**: Add the standard opening paragraph before or inside Section 1. Suggested language:

> This Statement of Work (SOW) and any exhibits, appendices, schedules, and attachments to it are made pursuant to Work Order (WO) [TBD] and describe the services to be performed by Microsoft Industry Solutions Delivery ("Microsoft") for Walmart Digital - Apparel & Marketplace ("Customer") relating to VirtualMirror AI - Clothing Fit Assessment Service ("Project").

### 1. Project Objectives And Scope

#### T-2 - Custom section order lacks template mapping - Severity: **Medium**

**Template master**: The Agile template uses six master sections: Project objectives and scope; Delivery approach, completion and timeline; Project organization; Project governance; Exhibits; Appendix.

**v0.3.0 observation**: The SOW uses a custom 23-section structure. This may be useful for engineering review, but it makes template compliance harder unless a mapping table is present.

**Required fix**: Add a mapping table in Section 1 that maps the SOW's 23 sections to the six Agile template master sections. Do not restructure the SOW unless RMQA / legal asks for it.

#### T-3 - Desired objectives need exact non-fixed-scope template language - Severity: **High**

**Template master**: Section 1.2 says desired business objectives and initial backlog are planning inputs, not fixed scope; not all objectives / backlog items may be completed within contracted capacity.

**v0.3.0 observation**: Section 3.1 clearly states Customer goals are not contractually guaranteed. That is good, but it does not fully preserve the template's broader point that desired objectives and the initial backlog do not constitute fixed scope.

**Required fix**: Add language to Section 3.1 / Worksheet A:

> The desired business objectives and any initial backlog items described in this SOW do not constitute fixed scope. There is no guarantee that all desired business objectives or all initial backlog items will be completed within contracted capacity. Customer's Product Owner prioritizes the backlog against available capacity through the governance process.

#### T-4 - WP1-WP8 read like committed deliverables, not variable targeted epics - Severity: **High**

**Template master**: Section 1.3 says targeted scope / epics may be revised based on Customer direction and may not all be built if capacity is consumed.

**v0.3.0 observation**: Section 4 states the build is organized into eight work packages and maps them to implementation tasks and Worksheet B acceptance criteria. This is useful, but it can read as fixed scope.

**Required fix**: Rename or qualify WP1-WP8 as "initial targeted epics / work packages used for baseline planning" and state that backlog items may be reprioritized, split, deferred, or removed by the Customer Product Owner within capacity.

### 2. Delivery Approach, Completion And Timeline

#### T-5 - P3/P4 defect remediation still over-commits - Severity: **Critical**

**Template master**: Section 2.3 says P1 and P2 remediation are in scope; P3 and P4 are logged and remediated only through agreed change request unless otherwise negotiated.

**v0.3.0 observation**: Section 11.3 now adds backlog-driven context, but the table still says P3 fixes are `Next sprint` and P4 fixes are `Backlog`. Those labels can still be read as a commitment to remediate all lower-priority defects.

**Required fix**: Rewrite P3/P4 rows to say:

| Priority | Recommended remediation wording |
| -------- | ------------------------------- |
| P3 | Logged and prioritized; remediated only if capacity remains or through agreed change request. |
| P4 | Logged; remediation only through backlog prioritization within remaining capacity or through agreed change request. |

#### T-6 - Formal acceptance model conflicts with Agile sprint completion guidance - Severity: **Critical**

**Template master**: Section 2.4 says backlog items do not require formal sign-off or Customer acceptance when completed by the feature team. Template guidance further warns that Agile work products generally should not require formal acceptance unless standard deliverable acceptance language is added and reviewed.

**v0.3.0 observation**: Section 15 improves the model by distinguishing Tier-1 sprint-validated backlog items from Tier-2 formal acceptance gates. That distinction helps, but Tier-2 still introduces formal acceptance obligations that require explicit template/legal handling.

**Required fix**: Choose one of two paths:

| Path | Required action |
| ---- | --------------- |
| Agile template path | Treat H1/H3/H5/H7/H8/MVP/GA as sprint review work products and governance gates, not formal deliverables requiring acceptance. |
| Formal deliverable path | Keep Tier-2 formal gates, but add standard deliverable acceptance language and route through RMQA / legal review. |

#### T-7 - Completion criteria still need stronger capacity / term primacy - Severity: **High**

**Template master**: Section 2.5 says the project is complete when at least one condition is met: all capacity used, term expired, all activities / backlog completed, or WO terminated.

**v0.3.0 observation**: Section 19 now lists these triggers and starts with capacity consumed, which is a good improvement. However, trigger 1 says capacity consumed plus Customer Product Owner acceptance of the delivered backlog state. That additional acceptance phrase could weaken the template's capacity-consumed completion trigger.

**Required fix**: Clarify that capacity exhaustion or term expiry is itself sufficient to complete the engagement, while Customer review records the delivered backlog state and any remaining items for change order / backlog continuation.

### 3. Project Organization

#### T-8 - Capacity should explicitly point to the Work Order - Severity: **High**

**Template master**: Section 3.1 says available capacity for each resource is specified in the WO and additional capacity is added through change management.

**v0.3.0 observation**: Section 7 provides an estimated 274 PD capacity model and role allocation, but the binding capacity should explicitly be the capacity stated in the Work Order.

**Required fix**: Add to Section 7 or Worksheet B.2:

> The capacity available for each Microsoft role is specified in the Work Order. If more resource capacity of any role is needed, it will be added only through the change management process.

### 4. Project Governance

#### T-9 - Missing no-obligation-to-start changed work clause - Severity: **High**

**Template master**: Section 4.3 says Microsoft has no obligation to commence changed work until estimated fee and schedule impact are agreed in a written amendment signed by authorized signatories.

**v0.3.0 observation**: Section 12 has a reasonable change process and a default-if-no-decision rule, but it still lacks the explicit no-obligation-to-start clause.

**Required fix**: Add to Section 12:

> Microsoft has no obligation to commence work related to any requested change until the estimated fee and schedule impact are agreed in a written amendment signed by authorized signatories from both parties.

### 5. Exhibits

#### T-10 - 147-task plan can still be read as committed backlog - Severity: **High**

**Template master**: Section 5.1 says the initial product backlog is optional and should stay at epic / feature level, not user-story or implementation-task level.

**v0.3.0 observation**: Exhibit L is now at epic / feature level, which is an improvement. However, it still links to `specs/001-clothing-fit-assessment/tasks.md` as task-level decomposition. Without stronger wording, the 147 tasks can be treated as contractual backlog.

**Required fix**: State that `tasks.md` is an implementation planning artifact only and is not itself a contractual backlog commitment. The contractual backlog should remain Exhibit L at epic / feature level.

### 6. Appendix

#### T-11 - Technology requirements table needs template-grade product / version / SKU clarity - Severity: **High**

**Template master**: Section 6.2 uses a table with Product and technology item, Version, and Ready by.

**v0.3.0 observation**: Section 16.1 exists, but the template review still needs to flag unresolved service names and missing product/version/SKU precision. This overlaps with the technical review, but it is also a template issue because the required technology table must be reviewable before signature.

**Required fix**: Add or revise Section 16.1 as a template-format technology requirements table with at least Product / Version or SKU / Ready by. Resolve or explicitly mark as assumptions the Foundry / Azure OpenAI model, Florence-2 deployment path, Front Door / APIM choice, Cosmos DB API, and GitHub Copilot / GitHub Enterprise requirements.

#### T-12 - Environment requirements table lacks required template columns - Severity: **High**

**Template master**: Section 6.3 requires Environment, Location, Responsible for configuration and maintenance, Subscription ownership, and Ready by.

**v0.3.0 observation**: Section 16.2 describes environments but does not include all template columns, especially Location and Ready by.

**Required fix**: Add the missing columns to Section 16.2:

| Environment | Location | Responsible for configuration and maintenance | Subscription ownership | Ready by |
| ----------- | -------- | --------------------------------------------- | ---------------------- | -------- |

#### T-13 - May 2026 AI Usage assumptions missing - Severity: **Critical**

**Template master**: Section 6.5 includes May 2026 AI Usage assumptions covering Microsoft use of AI Tools, ownership / confidentiality unchanged by AI Tool use, telemetry, and removal of AI Tools installed or deployed in the Customer environment at engagement conclusion.

**v0.3.0 observation**: Section 18 contains several assumptions and a GitHub Consulting Services notice, but it does not include the template's AI Usage assumptions as a dedicated clause. Because this is an AI engagement, this remains signature-grade.

**Required fix**: Add a dedicated Section 18.x "AI Usage Assumptions" adapted from the template. At minimum include:

- Microsoft may use Microsoft-developed or Microsoft-licensed AI Tools to perform the Services.
- AI Tool use does not alter ownership, licensing, or confidential treatment of pre-existing work, data, confidential information, or service deliverables.
- Microsoft will comply with internal standards, privacy / security requirements, and Responsible AI principles.
- AI Tool execution telemetry may be generated and processed under the Microsoft Products and Services Data Protection Addendum.
- AI Tools installed or deployed in the Customer environment will be removed at engagement conclusion unless otherwise agreed in writing.
- State whether this AI engagement is not PDOC-eligible.

### Version History

#### T-14 - Version History lacks v0.3.0 row - Severity: **High**

**Template master**: The template expects document versioning to explain material changes and review readiness.

**v0.3.0 observation**: The SOW header and Section 1 both say `0.3.0`, but the Version History section has no `0.3.0` row. The visible section currently contains only the versioning policy, not the actual v0.3.0 history row.

**Required fix**: Add a `0.3.0` Version History row summarizing changes from v0.2.0 and confirming review status.

---

## 5. Template Section-By-Section Assessment

| Template master section | v0.3.0 fit assessment | Severity | Required action |
| ----------------------- | --------------------- | :------: | --------------- |
| Opening SOW / WO paragraph | Partially improved; Work Order field and master-agreement precedence exist, but standard SOW / WO anchoring paragraph and attachment coverage remain incomplete. | **High** | Add standard paragraph and party shorthand definitions. |
| 1.1 Introduction | Strong, customer-specific, and grounded in discovery artifacts. | Informational | Keep. |
| 1.2 Customer desired business objectives | Strong customer-goal separation; still needs exact non-fixed-scope language for objectives and backlog. | **High** | Add template non-guarantee / variable backlog language. |
| 1.3 Targeted scope (Epics) | WP1-WP8 are useful but still risk reading as fixed deliverables. | **High** | Reframe as initial targeted epics / planning inputs. |
| 1.4 Areas out of scope | Project-specific out-of-scope table is strong. | Medium | Keep; optionally mirror key default exclusions if required by RMQA. |
| 2.1 Delivery overview | Agile fixed-capacity model is present. | Low | Keep. |
| 2.2 Delivery approach | Delivery phases and gates are detailed. | Low | Keep. |
| 2.3 Testing and defect remediation | P3/P4 wording still over-commits relative to template. | **Critical** | Rewrite P3/P4 rows. |
| 2.4 Sprint completion | Tier-1 / Tier-2 split improves clarity but formal acceptance still needs legal/template handling. | **Critical** | Pick Agile sprint-review model or add formal deliverable acceptance language. |
| 2.5 Project completion | Four triggers are present but capacity / term primacy should be absolute. | **High** | Remove or soften acceptance dependency from capacity-exhaustion trigger. |
| 2.6 Timeline | Timeline is detailed and capacity driven. | Low | Keep; maintain "estimate only" language. |
| 3.1 Project capacity | Capacity estimate is clear; binding WO capacity language missing. | **High** | Add WO capacity primacy language. |
| 3.2 Project staffing | Roles and RACI are strong. | Low | Keep. |
| 3.3 Executive steering committee | Covered. | Low | Keep. |
| 3.4 Product council | Covered and justified by governance needs. | Low | Keep. |
| 3.5 Feature team | Covered. | Low | Keep. |
| 4.1 Project communication | Covered. | Low | Keep. |
| 4.2 Risk and issue management | Covered; monthly review plus weekly escalation for High+ items is acceptable. | Low | Keep. |
| 4.3 Change management process | Process exists; no-obligation-to-start clause missing. | **High** | Add template clause. |
| 4.4 Escalation path | Covered. | Low | Keep. |
| 5.1 Initial targeted product backlog | Exhibit L improves epic-level backlog, but `tasks.md` link needs non-contractual qualifier. | **High** | Mark task list as planning artifact only. |
| 5.2 Customer-specific documentation | Exhibits list is strong. | Low | Keep. |
| 6.1 Definitions and acronyms | Glossary exists and is useful. | Low | Keep; scrub unused terms before signature. |
| 6.2 Technology requirements | Table exists but lacks enough product / version / SKU / ready-by clarity. | **High** | Add template-format technology requirements table. |
| 6.3 Environment requirements | Environment section lacks Location and Ready-by columns. | **High** | Add template columns. |
| 6.4 Customer responsibilities | Customer responsibilities are generally strong. | Medium | Confirm general template responsibilities are not omitted. |
| 6.5 Project assumptions | Missing May 2026 AI Usage assumptions. | **Critical** | Add dedicated AI Usage assumptions. |
| Version History | v0.3.0 header exists, but Version History has no v0.3.0 row. | **High** | Add row before signature. |

---

## 6. Recommended Changes Before Signature

### MUST-FIX

| # | Change | Where |
| :-: | ------ | ----- |
| 1 | Rework P3/P4 defect remediation to avoid automatic remediation commitment. | Section 11.3 |
| 2 | Resolve the formal acceptance model: pure sprint-review model or standard formal deliverable acceptance language with RMQA / legal review. | Section 15.2, Worksheet B |
| 3 | Add May 2026 AI Usage assumptions, including AI Tools, telemetry, confidentiality / ownership preservation, tool removal, and PDOC eligibility stance. | Section 18 |

### SHOULD-FIX BEFORE FINAL-FOR-SIGNATURE

| # | Change | Where |
| :-: | ------ | ----- |
| 4 | Add `0.3.0` Version History row. | Version History |
| 5 | Add standard Work Order anchoring paragraph and party shorthand definitions. | Header / Section 1 |
| 6 | Add explicit template language that desired objectives and initial backlog are planning inputs, not fixed scope. | Section 3.1, Worksheet A |
| 7 | Reframe WP1-WP8 as initial targeted epics / work packages and clarify they remain variable within contracted capacity. | Section 4, Worksheet B |
| 8 | Clarify capacity exhaustion and term expiry as sufficient completion triggers. | Section 19 |
| 9 | State that binding resource capacity is specified in the Work Order and additional capacity requires change management. | Section 7, Worksheet B.2 |
| 10 | Add the template no-obligation-to-start-changed-work clause. | Section 12 |
| 11 | Treat `tasks.md` 147 tasks as non-contractual implementation planning detail, not SOW-level backlog commitment. | Section 4, Section 20, Worksheet B |
| 12 | Add template-format technology requirements table with Product / Version or SKU / Ready-by columns. | Section 16.1 |
| 13 | Add template-format environment requirements table with Location / Responsible / Subscription ownership / Ready-by columns. | Section 16.2 |

---

## 7. Go / No-Go Recommendation

| Decision point | Recommendation | Rationale |
| -------------- | -------------- | --------- |
| Continue drafting v0.3.0 | **Go** | v0.3.0 improves version alignment and backlog framing. |
| Send for final signature | **No-Go** | Critical template blockers remain: P3/P4 remediation language, formal acceptance model, and missing AI Usage assumptions. |
| Send to RMQA / legal for review | **Conditional Go** | Reasonable after the Critical items are corrected or explicitly accepted as approved deviations. |

---

## 8. Version History

| Version | Date | Author | Status | Summary of changes |
| ------: | ---- | ------ | ------ | ------------------ |
| 0.3.0 | 2026-05-14 | Microsoft ISD - SOW Template Review | Draft | Re-ran template review for SOW v0.3.0 using SOW-Agile v1.3.2 source section order as the master structure; preserved T-1 through T-14 findings and expanded section-by-section assessment. |
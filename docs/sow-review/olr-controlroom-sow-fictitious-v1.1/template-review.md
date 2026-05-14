# Template Review - OLR-ControlRoom-SOW_Fictitious.docx v1.1 Against SOW-Agile v1.3.2

| Field | Value |
| ----- | ----- |
| **Document under review** | [docs/Inputs/OLR-ControlRoom-SOW_Fictitious.docx](../../Inputs/OLR-ControlRoom-SOW_Fictitious.docx) v1.1 - Amended; Draft pending Customer and Microsoft signature |
| **Template reference** | [docs/Inputs/SOW-Agile_v1.3.2.md](../../Inputs/SOW-Agile_v1.3.2.md) |
| **Review scope** | Agile SOW template alignment, fixed-capacity / variable-scope model, Work Order anchoring, project objectives, target scope, capacity, sprint completion, defect remediation, change management, technology/environment tables, customer responsibilities, assumptions, and signature hygiene. |
| **Reviewer** | Microsoft ISD - SOW Template Review |
| **Review date** | 2026-05-14 |
| **Verdict** | **Conditional Pass.** The SOW is substantially aligned to the fixed-capacity / variable-scope Agile model, but several signature-readiness gaps remain around Work Order references, external technical baselines, defect-remediation detail, technology/environment table completeness, and AI Usage assumptions. |
| **Master structure used** | The source SOW-Agile v1.3.2 template is the master for this review. Findings are organized against the template's original section order, not the SOW's custom 22-section / EX3 order. |
| **Cross-references** | [compliance-and-security-review.md](compliance-and-security-review.md) - [technical-review.md](technical-review.md) |

---

## 1. Severity Legend

| Severity | Definition | Action |
| :------: | ---------- | ------ |
| **Critical** | Direct conflict with Agile SOW model or incomplete contract package. | Must fix before signature. |
| **High** | Important template requirement missing or ambiguous. | Fix before final-for-signature or approve deviation. |
| **Medium** | Template section exists but needs clearer alignment. | Resolve in next draft. |
| **Low** | Style, terminology, or hygiene issue. | Track before v1.0/final signature. |
| **Informational** | Strong practice or optional improvement. | No blocking action. |

---

## 2. Findings Summary

| # | Template master section | Finding | Severity | SOW section(s) |
| :-: | ----------------------- | ------- | :------: | -------------- |
| TP-1 | Opening SOW / WO paragraph | Work Order, MCSA, Date, and key schedules remain TBD. | **Critical** | §1, §22 |
| TP-2 | Section 1 - Project objectives and scope | Objectives are well separated from guaranteed outcomes. | Informational | §3 |
| TP-3 | Section 1.3 - Targeted scope | Epics are mostly appropriate, but Schedule H / live-site baseline can expand scope if not frozen. | **High** | §2.3, §4, §22 |
| TP-4 | Section 2.3 - Testing and defect remediation | Defect remediation is too terse; P1/P2/P3/P4 handling lacks template-grade remediation rules. | **High** | §11.3 |
| TP-5 | Section 2.4 - Sprint completion | Validation model is mostly aligned; absence-of-objection language should be checked by legal/RMQA. | **Medium** | §15.3 |
| TP-6 | Section 2.5 - Project completion | Completion triggers are present and generally template-aligned. | Low | §19 |
| TP-7 | Section 3.1 - Project capacity | Capacity is clear, but binding Work Order capacity and rate-card/schedule attachment are incomplete. | **High** | §7, §8.2, §15.4, §20 |
| TP-8 | Section 4.3 - Change management | Change order process exists, but the explicit no-obligation-to-start-changed-work clause is missing. | **High** | §12 |
| TP-9 | Section 5.1 - Initial targeted backlog | 60 WBS leaves and live-site Deliver tab are referenced; risk of becoming fixed scope unless clearly non-contractual. | **High** | §2.3, §10, §22 |
| TP-10 | Section 6.2 - Technology requirements | Technology stack exists but lacks template-format Product / Version / Ready-by table. | **High** | §16.1 |
| TP-11 | Section 6.3 - Environment requirements | Environment table lacks Location and Ready-by columns. | **High** | §16.2 |
| TP-12 | Section 6.5 - Project assumptions | May 2026 AI Usage assumptions are missing. | **Critical** | §18 |
| TP-13 | Template hygiene | The document advertises 19 required sections but includes §22 appendices; numbering and EX3 map need cleanup. | **Medium** | Header, §22 |

---

## 3. Detailed Findings By Template Master Section

### Opening SOW / Work Order Paragraph

#### TP-1 - Binding references remain TBD - Severity: **Critical**

**Template master:** The SOW should be tied to an executed Work Order and controlling agreement, with exhibits/schedules attached or clearly incorporated.

**Observation:** The SOW has a good Document Control table, but Date, Work Order Reference, MCSA reference, Schedule A, and Schedule H are unresolved. Because Schedule H is stated as the authoritative technical baseline, this is a signature blocker.

**Required fix:** Replace TBD references and attach signed schedules before signature. Add document IDs, version/date, and precedence rules.

### 1. Project Objectives And Scope

#### TP-2 - Objectives and non-guarantee language are strong - Severity: Informational

The SOW clearly distinguishes customer-owned outcomes from Microsoft delivery and states that objectives are not contractually guaranteed within the capacity envelope. This aligns well with the Agile fixed-capacity / variable-scope template.

#### TP-3 - External technical baseline could expand scope - Severity: **High**

The SOW says the OLR live site is reference-only but also makes the executed Schedule H snapshot authoritative for technical content. That can work, but only if Schedule H is fixed and signed. Otherwise, the reference architecture, WBS, BOM, NFRs, SLOs, and probes could create ambiguity.

**Required fix:** Attach Schedule H with immutable version/hash/date. State that WBS leaves and live-site artifacts are planning/evidence references, not additional fixed-scope commitments except as explicitly incorporated.

### 2. Delivery Approach, Completion And Timeline

#### TP-4 - Defect remediation needs template-grade P1/P2/P3/P4 rules - Severity: **High**

Section 11.3 says defects enter the backlog and remediation is priority-driven. That avoids over-commitment, but it is too thin for signature. The Agile template normally distinguishes P1/P2 remediation from P3/P4 backlog treatment.

**Required fix:** Add a defect table covering priority, response target, remediation treatment, owner, and capacity/change-order rule. P3/P4 should be logged and prioritized; remediation should occur only within remaining capacity or through change request.

#### TP-5 - Absence-of-objection validation should be reviewed - Severity: **Medium**

Section 15.3 says absence of Customer objection in sprint review confirms validation for tracking and does not convert the engagement into fixed-price scope. That is commercially useful, but it should be reviewed because it may be treated as implied acceptance.

**Required fix:** Confirm with legal/RMQA or replace with explicit sprint-review validation language.

#### TP-6 - Completion triggers are mostly aligned - Severity: Low

Section 19 includes backlog complete, capacity consumed, timeline expired, and contract terminated. This matches the Agile template pattern. The capacity-consumed trigger is appropriately clear that additional work requires a signed Change Order.

### 3. Project Organization

#### TP-7 - Capacity is clear but schedule/rate-card binding is incomplete - Severity: **High**

The SOW gives total hours, role hours, work-package hours, and pricing ranges. However, Schedule A and rate-card confirmation remain future attachments, and the Work Order reference is TBD.

**Required fix:** Attach the rate card / fee schedule and clarify whether 14,500 hours is the binding cap in the Work Order or an estimate subject to Schedule A.

### 4. Project Governance

#### TP-8 - No-obligation-to-start changed work clause is missing - Severity: **High**

The change process is good, but the template expects explicit language that Microsoft has no obligation to start changed work until fee and schedule impact are agreed in a signed amendment.

**Required fix:** Add the no-start clause to §12.3.

### 5. Exhibits

#### TP-9 - WBS / live-site references may become fixed scope - Severity: **High**

The SOW references 60 WBS leaves, live OLR site tabs, BOM rows, hostile probes, and proof graph evidence. These can be valuable, but should not accidentally become fixed-scope commitments beyond capacity.

**Required fix:** State that WBS leaves and evidence artifacts are planning and validation references unless expressly listed as named work products in §15.2 or signed schedules.

### 6. Appendix

#### TP-10 - Technology requirements table is not template-format - Severity: **High**

Section 16.1 lists stack patterns, but the template expects Product / Version / Ready-by information. The current table does not show SKU, version, region, owner, or readiness date.

**Required fix:** Add a Product / Version or SKU / Region / Owner / Ready-by table for Azure IoT Operations, AKS, APIM, Front Door, Azure OpenAI/Foundry, Azure ML, AI Search, Cosmos DB Gremlin, Fabric, ADX, Event Hubs, Sentinel, Defender, and Power BI.

#### TP-11 - Environment requirements table lacks required columns - Severity: **High**

Section 16.2 lists Dev, Test/Pre-prod, Production SCUS, Production NCUS, and Site/OT zone. It does not include Location and Ready-by.

**Required fix:** Add columns: Environment, Location, Responsible for configuration and maintenance, Subscription ownership, Ready by.

#### TP-12 - AI Usage assumptions are missing - Severity: **Critical**

The SOW is an AI engagement and mentions Foundry RAG, Azure ML, Content Safety, AI Search, and AOAI PTU reservations. It does not include the May 2026 AI Usage assumptions covering Microsoft use of AI tools, ownership/confidentiality preservation, telemetry, and removal of AI tools installed in the Customer environment.

**Required fix:** Add a dedicated AI Usage assumptions clause in §18 or Schedule.

#### TP-13 - EX3 / section-count hygiene issue - Severity: **Medium**

The header says EX3-compliant structure with 19 required sections, but the SOW includes §20 pricing, §21 signatures, and §22 appendices. That may be deliberate, but the phrasing can confuse reviewers.

**Required fix:** Change the header to say 19 EX3 core sections plus commercial/signature/appendix schedules, or update the EX3 compliance map.

---

## 4. Template Section-By-Section Assessment

| Template master section | Fit assessment | Severity | Required action |
| ----------------------- | -------------- | :------: | --------------- |
| Opening SOW / WO paragraph | Strong document control table but TBD Work Order/MCSA/schedules. | **Critical** | Complete binding references. |
| 1.1 Introduction | Strong context and purpose. | Low | Keep. |
| 1.2 Customer desired business objectives | Strong non-guarantee and customer-owned outcomes. | Informational | Keep. |
| 1.3 Targeted scope (Epics) | Epics are appropriate; Schedule H and live-site references need boundaries. | **High** | Freeze Schedule H and limit live-site scope effect. |
| 1.4 Areas out of scope | Strong exclusions, especially closed-loop OT control. | Low | Keep; add PCI/HIPAA/FedRAMP/EU AI Act out-of-scope statements if needed. |
| 2.1 Delivery overview | Fixed-capacity / variable-scope model is clear. | Low | Keep. |
| 2.2 Delivery approach | Delivery phases are adequate. | Low | Keep. |
| 2.3 Testing and defect remediation | Too thin for P1-P4. | **High** | Add priority/remediation table. |
| 2.4 Sprint completion | Validation model is mostly aligned but legal-sensitive. | Medium | Confirm absence-of-objection language. |
| 2.5 Project completion | Aligned. | Low | Keep. |
| 2.6 Timeline | Relative timeline is clear. | Low | Keep. |
| 3.1 Project capacity | Strong hours model; Schedule A / WO cap incomplete. | **High** | Attach rate card and binding capacity reference. |
| 3.2 Project staffing | Detailed role model. | Low | Keep. |
| 3.3 Executive steering committee | Covered. | Low | Keep. |
| 3.4 Product council | Covered. | Low | Keep. |
| 3.5 Feature team | Covered through pods. | Low | Keep. |
| 4.1 Project communication | Covered. | Low | Keep. |
| 4.2 Risk and issue management | Covered with RAID and risks. | Low | Keep. |
| 4.3 Change management process | Process exists; no-start clause missing. | **High** | Add clause. |
| 4.4 Escalation path | Covered. | Low | Keep. |
| 5.1 Initial targeted product backlog | WBS/live-site references need non-contractual qualifier. | **High** | Bound WBS / live site to signed schedules. |
| 5.2 Customer-specific documentation | Schedules are listed but not attached. | **High** | Attach schedules or mark not incorporated. |
| 6.1 Definitions and acronyms | Glossary exists. | Low | Keep. |
| 6.2 Technology requirements | Stack list exists but no Product/Version/Ready-by table. | **High** | Add template-format table. |
| 6.3 Environment requirements | Environment list exists but missing Location/Ready-by. | **High** | Add missing columns. |
| 6.4 Customer responsibilities | Strong and specific. | Medium | Confirm general template obligations are not omitted. |
| 6.5 Project assumptions | Useful assumptions; AI Usage assumptions missing. | **Critical** | Add AI Usage language. |

---

## 5. Recommended Changes Before Signature

### MUST-FIX

| # | Change | Where |
| :-: | ------ | ----- |
| 1 | Complete Work Order, MCSA, Date, Schedule A, and Schedule H references. | §1, §22 |
| 2 | Attach and freeze Schedule H or remove its precedence until signed. | §2.3, §22 |
| 3 | Add May 2026 AI Usage assumptions. | §18 |

### SHOULD-FIX BEFORE FINAL-FOR-SIGNATURE

| # | Change | Where |
| :-: | ------ | ----- |
| 4 | Add no-obligation-to-start-changed-work clause. | §12 |
| 5 | Add P1/P2/P3/P4 defect remediation table. | §11.3 |
| 6 | Add template-format technology requirements table. | §16.1 |
| 7 | Add template-format environment requirements table. | §16.2 |
| 8 | Add non-contractual qualifier for live-site WBS/proof graph unless included in signed schedules. | §2.3, §10, §22 |
| 9 | Confirm sprint-review absence-of-objection language with legal/RMQA. | §15.3 |
| 10 | Clarify 19 EX3 core sections plus commercial/signature/appendix schedules. | Header / EX3 map |

### NICE-TO-HAVE

| # | Change | Where |
| :-: | ------ | ----- |
| 11 | Add a compact SOW-to-template mapping table for reviewers. | §22 or new appendix |
| 12 | Add explicit PCI/HIPAA/FedRAMP/EU AI Act applicability statements. | §5 / §18 |

---

## 6. Go / No-Go Recommendation

| Decision point | Recommendation | Rationale |
| -------------- | -------------- | --------- |
| Continue drafting | **Go** | Strong Agile model, scope exclusions, and capacity framing. |
| Send for signature now | **No-Go** | Binding references, Schedule H, and AI Usage assumptions are not ready. |
| Send to legal/RMQA | **Conditional Go** | Appropriate once MUST-FIX items are inserted or explicitly accepted as deviations. |

---

## 7. Version History

| Version | Date | Author | Status | Summary of changes |
| ------: | ---- | ------ | ------ | ------------------ |
| 1.0 | 2026-05-14 | Microsoft ISD - SOW Template Review | Draft | Initial template review for OLR Control Room SOW v1.1 using SOW-Agile v1.3.2 source section order as master. |
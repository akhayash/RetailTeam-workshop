# Compliance And Security Review - OLR-ControlRoom-SOW_Fictitious.docx v1.1

| Field | Value |
| ----- | ----- |
| **Document under review** | [docs/Inputs/OLR-ControlRoom-SOW_Fictitious.docx](../../Inputs/OLR-ControlRoom-SOW_Fictitious.docx) v1.1 - Amended; Draft pending Customer and Microsoft signature |
| **Review scope** | Security, privacy, AI governance, OT boundary controls, incident response, data protection, regulatory posture, assurance evidence, and contractual completeness. |
| **Reviewer** | Microsoft ISD - Compliance & Security Review |
| **Review date** | 2026-05-14 |
| **Verdict** | **Conditional Pass / No-Go for signature.** The SOW has strong OT-boundary intent and explicit no-write-to-control-system language, but it is not signature-ready until data protection, incident response, AI governance, assurance evidence, and binding document references are completed. |
| **Cross-references** | [technical-review.md](technical-review.md) - [template-review.md](template-review.md) |

---

## 1. Executive Summary

The SOW is unusually strong on several high-risk points: it excludes closed-loop OT control, defines five OT-boundary detection controls, separates customer-owned outcomes from Microsoft delivery, and uses fixed-capacity / variable-scope language. Those are important strengths for an oil and gas operational analytics engagement.

However, this is still a high-risk AI + industrial OT + critical infrastructure SOW. The current draft leaves several signature-grade controls as references to external schedules, live sites, or future signature attachments. Before signature, the SOW should convert the most important security, privacy, and assurance requirements into explicit contractual language inside the SOW or signed schedules.

Top material gaps:

| # | Gap | Severity | Why it matters |
| :-: | --- | :------: | -------------- |
| C-1 | MCSA, Work Order, Schedule A, and Schedule H references remain TBD / externally authoritative. | **Critical** | Contract package is not complete enough for signature. |
| C-2 | Data classification, retention, deletion, DSAR/export, and destruction-on-exit are not specified by data class. | **Critical** | Operational, subsurface, telemetry, identity, logs, and AI prompt/response data need explicit handling rules. |
| C-3 | Controller / processor allocation, DPA inheritance, sub-processor list, and cross-border transfer posture are missing. | **Critical** | The SOW names many Azure/AI/third-party services but does not enumerate data protection roles or processors. |
| C-4 | AI governance is under-specified for an engineer-facing advisor. | **High** | RAG and forecasting outputs can influence operational decisions; the SOW needs human-in-the-loop and non-authoritative-advice language. |
| C-5 | Security assurance is too abstract for OT-adjacent work. | **High** | STRIDE-lite and Cyber/OIMS sign-off are useful but insufficient without pen-test scope, threat-model refresh, evidence pack, and remediation rules. |
| C-6 | Incident response and breach notification terms are not explicit. | **High** | OT-boundary incidents, data incidents, and AI abuse events need notification, forensic preservation, and ownership rules. |

---

## 2. Compliance Framework Mapping

| Framework / regime | Coverage in SOW | Assessment | Required action |
| ------------------ | --------------- | ---------- | --------------- |
| OWASP ASVS L2 | Security model, STRIDE-lite, Defender, Sentinel, Key Vault, APIM, Front Door are mentioned. | **Claimed but inadequate** | Add ASVS L2 self-assessment or equivalent application security verification deliverable. |
| SOC 2 TSC | Audit completeness, monitoring, access controls, DR, and runbooks are mentioned. | **Implicit only** | Map controls to Security, Availability, Confidentiality, and Processing Integrity. |
| NIST CSF 2.0 | Governance, identify/protect/detect/respond/recover concepts appear across sections 9, 11, 13, 16, 17. | **Implicit only** | Add a NIST CSF alignment appendix or evidence package deliverable. |
| GDPR / UK GDPR / CCPA / CPRA | Data residency and privacy/DLP appear as NFRs, but roles and rights are not stated. | **Inadequate** | Add controller/processor roles, DSAR support, retention/deletion, DPA, and transfer terms. |
| PCI DSS | Not addressed. | **Not addressed** | State whether no CHD/SAD is processed and exclude PCI scope unless later added by Change Order. |
| HIPAA | Not addressed. | **Not addressed** | State whether PHI is out of scope. |
| FedRAMP / US public sector | Not addressed. | **Not addressed** | Confirm commercial-cloud terms or add government-cloud amendment if required. |
| EU AI Act | Not addressed. | **Not addressed** | Add AI risk-tier memo; confirm system is advisory and not autonomous control. |
| NIST AI RMF | Responsible AI is not explicitly mapped. | **Inadequate** | Add AI risk management deliverables: evaluation, monitoring, fallback, human review, model card. |
| OT / industrial cybersecurity | OT boundary controls are a strong start. | **Partial** | Add IEC 62443 / NIST SP 800-82-aligned control mapping or Customer OIMS equivalent. |
| Accessibility / WCAG | NFR-16 says accessibility for engineer surface. | **Partial** | Define WCAG target, test owner, and evidence deliverable. |

---

## 3. Data Protection And Privacy Findings

### C-1 - Binding document references are incomplete - Severity: **Critical**

The Document Control table leaves the Work Order reference, MCSA reference, signature date, Schedule A, and the executed Schedule H PDF as TBD or future attachments. Section 2.3 also says the Schedule H snapshot prevails on technical content. That is acceptable only if Schedule H is actually attached, versioned, and signed with the SOW.

**Required fix:** Before signature, replace TBD references and attach the exact Schedule H snapshot, Schedule A rate card, and any incorporated schedules. Add a rule that unsigned live-site changes do not modify scope, acceptance, or security obligations.

### C-2 - Data handling is not specified by data class - Severity: **Critical**

The SOW processes or observes operational telemetry, historian data, drilling/completions/reliability signals, methane-related data references, identity data, logs, prompts, RAG grounding data, AI outputs, security alerts, and audit evidence. Retention, deletion, export, purge, and destruction-on-exit rules are not stated by data class.

**Required fix:** Add a data classification and lifecycle table with: data class, owner/controller, processor, storage service, region, retention, delete/purge SLA, export/DSAR path, encryption/key stance, and exit destruction/certification.

### C-3 - Data protection roles and sub-processors are missing - Severity: **Critical**

The SOW names Azure AI Foundry/AOAI, Azure ML, Azure AI Search, Fabric, ADX, Event Hubs, Event Grid, Service Bus, Sentinel, Defender for Cloud, Front Door, APIM, Power BI Premium, OSDU vendor, PI/AVEVA, and potentially GitHub/Azure DevOps. It does not enumerate sub-processors or separate Customer-procured third parties from Microsoft-provided services.

**Required fix:** Add a sub-processor / service-provider schedule and confirm DPA inheritance. State controller/processor roles for Customer operational data, security logs, AI inputs/outputs, and support telemetry.

### C-4 - Cross-border and region controls are incomplete - Severity: **High**

NFR-09 says US regions only and the architecture uses SCUS + NCUS. The SOW does not state whether any support, telemetry, abuse monitoring, AI processing, or third-party tooling can process data outside the US.

**Required fix:** Add a US-only processing assumption or list approved exceptions. For any non-US processing, include transfer mechanism and Customer approval path.

---

## 4. Security Architecture And Controls

### C-5 - OT-boundary controls are strong but need assurance depth - Severity: **High**

DET-01..05 are a strong foundation: architecture prohibition, Azure Firewall deny rules, AKS NetworkPolicy, Sentinel anomalous-egress detection, and quarterly OT red-team drill. The gap is evidence specificity: who signs, what logs are retained, how failures are classified, and what retest/remediation windows apply.

**Required fix:** Add an OT assurance pack deliverable with evidence sources, retention, owner, acceptance criteria, failure severity, retest procedure, and OIMS sign-off.

### C-6 - Incident response and breach notification are incomplete - Severity: **High**

Escalation exists, but the SOW lacks explicit security incident definitions, breach notification SLA, forensic preservation, joint investigation, regulator/customer notification ownership, and AI abuse-event handling.

**Required fix:** Add a security incident response section covering Sec-Sev levels, 72-hour GDPR-style breach notification where applicable, immediate OT-boundary escalation, forensic log preservation, contact matrix, and post-incident report obligations.

### C-7 - Supply-chain security needs a concrete evidence package - Severity: **High**

The SOW mentions Defender, Sentinel, Key Vault, Azure DevOps / GitHub Enterprise, and customer-selected DevOps. It does not require SAST/SCA/SBOM/container signing/secret scanning/branch protection evidence as a delivered artifact.

**Required fix:** Add a DevSecOps evidence package with SAST, SCA, SBOM, secret scanning, IaC scanning, container image signing, deployment approvals, workload identity, and privileged access review.

---

## 5. AI / ML Risk

### C-8 - AI advisor governance is under-specified - Severity: **High**

The Foundry RAG advisor and Azure ML forecasts produce engineer-facing and executive-facing recommendations. The SOW says no OT write-back, which is good, but does not clearly state that AI outputs are advisory, non-authoritative, and require qualified human review before operational action.

**Required fix:** Add AI advisory disclaimer, human-in-the-loop rules, unacceptable-use boundaries, prompt-injection testing, red-team testing, grounding/citation requirements, model evaluation thresholds, drift monitoring, and rollback criteria.

### C-9 - Responsible AI artifacts are missing - Severity: **High**

The SOW does not list model cards, RAI impact assessment, evaluation report, prompt/grounding test set, or safety-monitoring dashboard as work products.

**Required fix:** Add RAI deliverables mapped to Discover / Protect / Govern: risk assessment, safety evaluation, guarded deployment, telemetry, continuous monitoring, and post-deployment governance.

---

## 6. Resilience, Availability, And Assurance

### C-10 - SLOs are referenced but not enough for contractual clarity - Severity: **High**

Section 16.3 says NFRs/SLOs are maintained in Schedule H and do not create a standalone SLA or warranty. That is good commercially, but the SOW still needs measurement definitions and evidence requirements for exit gates.

**Required fix:** Add SLO measurement windows, data sources, exclusions, synthetic/user traffic distinction, owner, and pass/fail evidence for DEL-09, DEL-14, DEL-17, and HG gates.

### C-11 - Hypercare and P1 simulation terms need warranty boundaries - Severity: **Medium**

Section 17 requires three P1 simulations or real P1 incidents, all runbooks executed, DR drill pass, and error-budget attestation. This is useful, but should not imply ongoing managed operations or warranty after hypercare.

**Required fix:** Add explicit hypercare hours, response targets, exclusions, and transition-to-support boundary.

---

## 7. Recommended Changes Before Signature

### MUST-FIX

| # | Change | SOW section |
| :-: | ------ | ----------- |
| 1 | Replace all TBD binding references and attach signed Schedule A / Schedule H package. | §1, §2.3, §22 |
| 2 | Add data classification, retention, deletion, export, and destruction-on-exit table. | New §16.x or §18 |
| 3 | Add controller/processor, DPA, sub-processor, and cross-border processing schedule. | New §18.x / Schedule |
| 4 | Add AI advisory / human-in-the-loop / Responsible AI governance language. | §15, §16, §18 |
| 5 | Add security incident response, breach notification, forensic preservation, and OT-boundary escalation terms. | §14 / new security section |
| 6 | Add OT assurance evidence pack and retest/remediation rules for DET-01..05. | §16.4, §17 |
| 7 | Add DevSecOps evidence package and deployment control requirements. | §10, §16, Schedule |

### SHOULD-FIX

| # | Change | SOW section |
| :-: | ------ | ----------- |
| 8 | Add OWASP ASVS L2, SOC 2, NIST CSF, and NIST AI RMF mapping deliverables. | Schedule |
| 9 | Add PCI, HIPAA, FedRAMP, and EU AI Act explicit out-of-scope / applicability statements. | §5, §18 |
| 10 | Clarify hypercare support hours, response targets, and transition boundary. | §17, §19 |
| 11 | Define SLO measurement windows, exclusions, and evidence sources. | §16.3 |
| 12 | Define accessibility target and test evidence for NFR-16. | §16.3 |

---

## 8. Go / No-Go Recommendation

| Decision point | Recommendation | Rationale |
| -------------- | -------------- | --------- |
| Continue drafting | **Go** | The SOW has a coherent delivery model and strong OT write-back exclusion. |
| Sign now | **No-Go** | Critical data protection, DPA/sub-processor, AI governance, and incident response gaps remain. |
| Send for legal / security review | **Conditional Go** | Send after TBD schedules and the Critical items above are inserted or explicitly accepted as deviations. |

---

## 9. Version History

| Version | Date | Author | Status | Summary of changes |
| ------: | ---- | ------ | ------ | ------------------ |
| 1.0 | 2026-05-14 | Microsoft ISD - Compliance & Security Review | Draft | Initial compliance and security review for OLR Control Room SOW v1.1. |
# Compliance and Security Review - Virtual-Mirror-SOW.md v0.3.0

| Field                     | Value                                                                                                                                                                                                                                                                                                                        |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Document under review** | [docs/Virtual-Mirror-SOW.md](../../Virtual-Mirror-SOW.md) v0.3.0 (2026-05-14, Draft for internal review)                                                                                                                                                                                                                     |
| **Review scope**          | Compliance posture, privacy, biometric / sensitive personal data, security obligations, AI risk, sub-processors, incident response, assurance, data exit, and contractual completeness.                                                                                                                                      |
| **Reviewer**              | Microsoft Industry Solutions Delivery - Security and Compliance Review                                                                                                                                                                                                                                                       |
| **Review date**           | 2026-05-14                                                                                                                                                                                                                                                                                                                   |
| **Verdict**               | **Conditional Pass.** v0.3.0 remains a strong pre-signature draft but is not signature-ready. It keeps useful privacy-by-design commitments, DPIA checkpoints, Responsible AI language, and security hardening deliverables, but several binding compliance obligations still need explicit SOW text before final signature. |
| **Cross-references**      | [technical-review.md](technical-review.md) - [template-review.md](template-review.md)                                                                                                                                                                                                                                        |

---

## 1. Executive Summary

v0.3.0 aligns the SOW header and section 1 version fields, and it slightly improves defect management by saying remediation is backlog-driven within sprint capacity. It does not close the main compliance and security blockers from v0.2.0.

The biggest unresolved issue is still the treatment of shopper photos and derived body measurements. The SOW says `biometric-adjacent`, but state biometric privacy laws, CCPA sensitive personal information, and GDPR special-category analysis might classify the data more strictly. The SOW should not rely on softened terminology without a legal assumption record and explicit consent / notice responsibilities.

---

## 2. Material MUST-FIX Items

| #    | Finding                                                                                    |    Severity    | SOW section(s)              | Required action                                                                                                                                            |
| ---- | ------------------------------------------------------------------------------------------ | :------------: | --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| C-1  | Biometric data classification remains hedged as `biometric-adjacent`.                      |  **MUST-FIX**  | Sections 3, 15, 18          | Add legal assumption record for BIPA / CUBI / WA MHMD / CCPA / GDPR Art. 9 and state whether photos and derived measurements are biometric identifiers.    |
| C-2  | Shopper consent and biometric notice ownership is not binding enough.                      |  **MUST-FIX**  | Sections 17, 18, D-3, D-13  | State that Customer storefront captures required biometric/privacy notices and passes a consent reference to the API before photo upload.                  |
| C-3  | Breach notification and security incident response SLAs are missing from contractual text. |  **MUST-FIX**  | Sections 13, 14, D-13       | Add security incident severity matrix, customer notification SLA, forensic preservation, joint IR contacts, and preliminary report timeline.               |
| C-4  | Controller / processor roles and DSAR responsibility remain implicit.                      |  **MUST-FIX**  | Sections 17, 18, D-3, D-13  | State Customer is controller and Microsoft is processor / sub-processor as applicable; define DSAR support and deletion/export boundaries.                 |
| C-5  | Sub-processor disclosure is incomplete.                                                    |  **MUST-FIX**  | D-13, Section 17            | Name Azure OpenAI / Foundry, Azure AI Content Safety, GitHub build services, and any abuse-monitoring reviewer path; include DPA/change mechanics.         |
| C-6  | AI recommendation liability and advisory-disclaimer obligations are missing.               |  **MUST-FIX**  | Sections 17, 18, D-2, D-11  | State fit recommendations are advisory; Customer must display confidence/disclaimer text in the storefront.                                                |
| C-7  | AI fairness and demographic accuracy criteria are not specific enough.                     |  **MUST-FIX**  | D-11, D-13                  | Add model-card acceptance criteria for stratified accuracy across relevant body type, skin tone, and gender-presentation cohorts where lawfully collected. |
| C-8  | Data retention and contract-exit obligations are incomplete.                               |  **MUST-FIX**  | D-12, Section 19            | Add retention table for photos, height, measurements, assessments, audit logs, model artifacts, and deletion/return on termination.                        |
| C-9  | Hypercare / P1 obligations remain in tension.                                              |  **MUST-FIX**  | Sections 11.3, 14, 19, D-14 | Reconcile 4-hour P1 fix, business-hours best effort, two-week hypercare, and any production support exclusion.                                             |
| C-10 | OWASP ASVS L2 is claimed but no ASVS L2 mapping deliverable is committed.                  |  **MUST-FIX**  | Sections 3, 11, 15          | Add ASVS L2 self-assessment / gap report deliverable and acceptance criteria.                                                                              |
| C-11 | Private networking and PII telemetry scrubbing are not explicit commitments.               |  **MUST-FIX**  | D-7, D-9, Section 16        | Add private endpoints / public network disablement where supported; require telemetry redaction and audit-log integrity controls.                          |
| C-12 | Version History lacks a v0.3.0 entry, weakening change auditability.                       | **SHOULD-FIX** | Version History             | Add a v0.3.0 row before signature so reviewers can trace what changed from v0.2.0 to v0.3.0.                                                               |

---

## 3. Framework Coverage

| Framework / regime   | Current posture                                        | Gap                                                                                                                         |
| -------------------- | ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| GDPR / CCPA          | DPIA package exists and deletion appears in US2 / D-3. | Roles, DSAR support, breach notification, and special-category / sensitive personal information analysis need binding text. |
| State biometric laws | Not explicitly addressed.                              | BIPA / CUBI / WA MHMD style notice and consent assumptions need to be stated.                                               |
| OWASP ASVS L2        | Claimed in value theme / assumptions.                  | No committed ASVS mapping or control evidence deliverable.                                                                  |
| SOC 2 / NIST CSF     | Mentioned as alignment.                                | Control mapping remains light; audit log integrity and incident response should be stronger.                                |
| PCI DSS adjacent     | Correctly scoped as no CHD.                            | Add a short PCI scoping memo or explicit no-CHD statement if Walmart reviewers require it.                                  |
| EU AI Act            | Treated as Change Order.                               | Add risk-tier rationale now so future EU expansion has a baseline.                                                          |
| NIST AI RMF          | Not named.                                             | D-11 model card is the natural anchor for Govern / Map / Measure / Manage alignment.                                        |

---

## 4. Positive Controls to Preserve

- Photos are intended to be transient and not persisted beyond a 60-second blob TTL.
- Measurement profiles are opt-in and have a 24-hour hard-delete SLA.
- DPIA review slots are named for kickoff, Sprint 4, and Sprint 8 / 9.
- D-8 includes CI security controls: SAST, SCA, SBOM, Trivy, and Notation signing.
- D-10 includes load and chaos validation.
- A-24 acknowledges Responsible AI sensitive-use review and customer cooperation.

---

## 5. Pre-Signature Remediation Sequence

1. Resolve data classification, controller/processor roles, and consent ownership first.
2. Normalize model names and sub-processors after the technical model stack is corrected.
3. Add breach notification and security incident response obligations.
4. Reconcile hypercare, P1 fix obligations, and production support exclusions.
5. Add ASVS L2, data retention, audit integrity, and AI fairness acceptance criteria.
6. Add the v0.3.0 Version History row before final review circulation.

---

## 6. Version History

| Version | Date       | Author                                         | Status | Summary of changes                                                                                                                                                |
| ------: | ---------- | ---------------------------------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|   0.3.0 | 2026-05-14 | Microsoft ISD - Security and Compliance Review | Draft  | Initial compliance and security review for SOW v0.3.0; confirms v0.3.0 version alignment in header / section 1 and carries forward unresolved signature blockers. |

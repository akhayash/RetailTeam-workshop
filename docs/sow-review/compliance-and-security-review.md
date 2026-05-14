# Compliance & Security Review — Virtual-Mirror-SOW.md

| Field                     | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Document under review** | [docs/Virtual-Mirror-SOW.md](../Virtual-Mirror-SOW.md) v0.1.0 (2026-05-14, Draft for internal review)                                                                                                                                                                                                                                                                                                                                                                       |
| **Review scope**          | Compliance posture (GDPR/CCPA, PCI DSS-adjacent, SOC 2, NIST CSF 2.0, OWASP ASVS L2, EU AI Act), security obligations, biometric/PII handling, AI risk management, supply chain, incident response, and contractual completeness                                                                                                                                                                                                                                            |
| **Reviewer**              | Microsoft Industry Solutions Delivery — Security & Compliance Review                                                                                                                                                                                                                                                                                                                                                                                                        |
| **Review date**           | 2026-05-14                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **Verdict**               | **Conditional Pass.** The SOW is materially aligned with the discovery artifacts (threat model, risk register, product definition) and bakes in OWASP ASVS L2, SOC 2, NIST CSF 2.0, GDPR/CCPA, and PCI-adjacent posture. However, several **MUST-FIX** gaps exist before signature, primarily around biometric data classification, incident response/breach notification SLAs, AI-specific contractual language, sub-processor governance, and pen-test ownership clarity. |
| **Cross-references**      | [threat-model.md](../architecture/threat-model.md) · [risk-register.md](../architecture/risk-register.md) · [Product-definition.md](../Sessions/Product-definition.md) · [spec.md](../../specs/001-clothing-fit-assessment/spec.md)                                                                                                                                                                                                                                         |

---

## 1. Executive Summary

The Virtual-Mirror SOW is an above-average draft for an AI/biometric-adjacent engagement. It correctly inherits compliance themes from the discovery artifacts (PCI-DSS-adjacent, SOC 2 TSC, NIST CSF 2.0, OWASP ASVS L2, GDPR/CCPA), explicitly carves out HIPAA/FedRAMP/EU AI Act as Change Orders, and ties hypothesis gates (H1, H3, H5, H7, H8) to acceptance criteria.

**Strengths**

- Privacy-by-design assumption (A-11) — photos processed in-memory with 60-second blob TTL — is explicit and consistent with the threat model (I-1, R-3).
- DPIA inputs are a named deliverable (D-13) with three review checkpoints (kickoff, Sprint 4, Sprint 8).
- Hardening pipeline (SAST/SCA/SBOM/Trivy/Notation) is contractually a deliverable (D-8), not an aspiration.
- Degradation ladder (L1–L5) and chaos validation are acceptance-tested (D-6, D-10) — operational resilience is in scope.
- Compliance scope is bounded (A-15) so scope creep into HIPAA/FedRAMP/EU AI Act is a change-order trigger.

**Material gaps (MUST-FIX before signature)**

1. **Biometric data classification is hedged** — the SOW says "biometric-adjacent" but Illinois BIPA, Texas CUBI, Washington MHMD/HB1155, EU GDPR Art. 9, and CCPA's "sensitive personal information" definition may classify body photos and derived measurements as biometric identifiers outright. Requires a documented legal opinion or assumption record.
2. **No breach notification SLA** in §13 / §14 — GDPR Art. 33 requires 72 h, CCPA / state breach laws have parallel timelines. Microsoft's obligations to assist with breach detection and notification are unspecified.
3. **Pen-test ownership is split unsafely** — §11.1 says "External vendor (Walmart-procured)" but §17.2 says Walmart "manages" external dependencies including pen-test procurement. No Microsoft commitment to remediation SLA or re-test inclusion in capacity envelope.
4. **AI-specific contractual posture is missing** — no clause covering hallucination liability, model drift remediation, training-data warranties from sub-processors (Azure OpenAI, Florence-2), or EU AI Act readiness if scope changes.
5. **Sub-processor list is implicit** — Azure OpenAI, Azure AI Foundry (Florence-2), Azure AI Content Safety, and any abuse-monitoring reviewer are de-facto sub-processors handling biometric-adjacent data. GDPR Art. 28 requires named sub-processors and prior consent for changes.
6. **Data residency is single-region but cross-border processing isn't addressed** — East US 2 implies US data storage; if any Walmart customers are non-US (Canada, Mexico operations) this needs an SCC / adequacy decision call-out.
7. **Hypercare scope vs. P1 SLAs in §11.3 are inconsistent** — §11.3 promises a 4-hour P1 fix SLA but §17.2 says Microsoft's hypercare is best-effort within business hours. These contradict during the 30-day hypercare window.
8. **No data deletion / contract-exit clause** — what happens to audit logs, model artefacts, and profile data on termination (§19 triggers 4 and 5)? GDPR Art. 17 and CCPA §1798.105 require deletion paths.
9. **Coverage gate (80%/90%) is contractual but not tied to security-relevant code paths** — auth middleware, tenant isolation, deletion cascade, and audit-log integrity should be called out as "critical paths" requiring ≥ 90%.
10. **OWASP ASVS L2 is claimed but no mapping artefact is committed** — §3.2 / §15.1 list ASVS L2 as a posture but no ASVS L2 self-assessment / gap report is in Worksheet B.

**Recommended outcome**: Address the 10 MUST-FIX items in §10 of this review before promoting to v1.0.0 final-for-signature.

---

## 2. Compliance Framework Mapping

### 2.1 Coverage assessment

| Framework                                                |  Claimed in SOW   | Where                                 | Adequacy of coverage                                                                                                                      | Gap                                                                                                                                             |
| -------------------------------------------------------- | :---------------: | ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **OWASP ASVS L2**                                        |        ✅         | §3.2, §7 capacity drivers, §18.2 A-15 | Posture stated; no deliverable artefact                                                                                                   | **MUST-FIX**: add ASVS L2 self-assessment / gap report as D-15                                                                                  |
| **PCI DSS** (adjacent)                                   |    ✅ adjacent    | §3.2, A-15                            | Correctly scoped — no CHD in the data plane                                                                                               | OK; recommend recording PCI scoping memo                                                                                                        |
| **SOC 2 TSC**                                            |        ✅         | §3.2                                  | Listed as a "value theme" but not mapped to controls                                                                                      | **SHOULD-FIX**: add control-to-TSC mapping (Security, Availability, Confidentiality minimum)                                                    |
| **NIST CSF 2.0**                                         |        ✅         | §3.2, A-15                            | Listed; Govern/Identify/Protect/Detect/Respond/Recover not individually mapped                                                            | **SHOULD-FIX**: map deliverables to CSF functions (Detect = D-9; Respond/Recover = D-12; Govern = D-13)                                         |
| **GDPR / CCPA**                                          |        ✅         | A-15, D-13                            | DPIA committed; rights-management is implicit                                                                                             | **MUST-FIX**: explicit DSAR support paths, breach notification SLA (Art. 33), Art. 28 sub-processor list                                        |
| **EU AI Act**                                            |    ⚠️ Excluded    | A-15                                  | Treated as a Change Order trigger                                                                                                         | Reasonable, but classify VirtualMirror's risk tier explicitly — Annex III / high-risk argument should be documented now to avoid late discovery |
| **State biometric privacy** (BIPA / TX CUBI / WA HB1155) | ❌ Not addressed  | —                                     | **MUST-FIX**: add explicit assumption on whether shopper photos / derived measurements are "biometric identifiers" under these state laws |
| **ISO/IEC 27001 / 27701**                                | ❌ Not referenced | —                                     | Optional; recommend a one-line statement aligning evidence with ISO controls to ease future certification                                 |
| **NIST AI RMF 1.0**                                      | ❌ Not referenced | —                                     | **SHOULD-FIX**: model card (D-11) is the natural anchor — reference AI RMF Govern/Map/Measure/Manage                                      |
| **WCAG 2.2 AA**                                          | ❌ Not addressed  | —                                     | UX is out of scope per OOS-1, but the OpenAPI contract (D-4) should not preclude accessible client implementations — clarify              |

### 2.2 Compliance scope statement quality

A-15 is a strong statement and properly excludes HIPAA / FedRAMP / EU AI Act. However:

- "PCI-DSS-adjacent" should be defined contractually — "the service does not store, process, or transmit cardholder data, and is in PCI-DSS scope only as a connected system."
- "GDPR/CCPA" without naming the **roles** (controller vs. processor) is ambiguous. The SOW implies Microsoft is a sub-processor to Walmart-the-controller, but does not state it. **MUST-FIX**.

---

## 3. Data Protection & Privacy

### 3.1 Data classification — gap

The threat model (`threat-model.md` §System Decomposition) classifies the body photo as **"Biometric-adjacent / Sensitive"**. The SOW does not propagate this classification consistently:

- §15.1 D-12 commits to "data classification labels (transient, ephemeral, opt-in, audit)" — good.
- §3.2 calls the engagement "PCI-DSS-adjacent, SOC 2-aligned, NIST CSF 2.0 mapped, OWASP ASVS L2, GDPR/CCPA" — no mention of biometric law exposure.
- **Risk**: BIPA awards $1,000–$5,000 per violation. A single Illinois shopper photo retained beyond 60 s with no written notice or release could expose Walmart to class-action exposure. The SOW should commit Microsoft to:
  - Engineering controls that enforce the 60-s TTL.
  - An auditable purge log (already in D-9 indirectly).
  - A documented assumption that Walmart's storefront UI captures BIPA-style "informed written release" before the photo is sent to the API.

**MUST-FIX**: Add A-16 — "Walmart's storefront captures biometric privacy notice and informed consent (BIPA / state-equivalent) before invoking `POST /v1/assessments`; the consent reference is passed via the API and recorded in the audit log."

### 3.2 Retention, deletion, and the right to be forgotten

| Data                           | Retention claimed                                   | Verified by                     | Gap                                                                                                                                                            |
| ------------------------------ | --------------------------------------------------- | ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Body photo                     | < 60 s                                              | D-6 chaos test? D-9 dashboards? | **No explicit deliverable verifies 60-s SLA in production**. Add to D-10 or D-12.                                                                              |
| Height input                   | Not stored separately                               | Threat model only               | Restate in SOW                                                                                                                                                 |
| Derived measurements (profile) | Until deletion (24 h hard-delete SLA per US2)       | D-3 acceptance criteria         | OK                                                                                                                                                             |
| Assessment results             | 365 d TTL                                           | data-model.md, not SOW          | **MUST-FIX**: SOW does not state the 365 d assessment retention. Add to D-12.                                                                                  |
| Audit logs                     | "Immutable; retention per policy" (threat-model.md) | D-12                            | **MUST-FIX**: SOW does not state audit retention. Recommend ≥ 12 months for SOC 2, ≥ 7 years if Walmart-internal retention applies. Make this a Walmart input. |
| Tenant config                  | Persistent                                          | —                               | OK                                                                                                                                                             |

### 3.3 DSAR (Data Subject Access Request) support

CCPA §1798.100 and GDPR Art. 15–22 grant shoppers rights to access, port, correct, restrict, object, and delete. The SOW (D-3) provides `DELETE /v1/profiles/{shopperRef}` with a 24-hour hard-delete SLA — good. But:

- **No read/export path** is contractually committed. Either Walmart owns DSAR-read (likely correct — storefront is the controller) or the SOW must add it. **MUST-FIX**: state the controller/processor split and that DSAR fulfilment is Walmart's responsibility, supported by the API surface delivered.
- **Deletion cascade** to audit logs is intentionally not happening (audit logs are immutable). This is correct from a SOC 2 standpoint but may conflict with GDPR Art. 17. Document the legal basis (legitimate interest / legal obligation under SOX-adjacent retention) explicitly. **SHOULD-FIX**.

### 3.4 Cross-border data transfers

§16.3 commits to East US 2 single-region. The SOW does not address:

- Walmart's potential non-US operations (Canada, Mexico, Central America). If any tenant onboarded under BO-3 is non-US, EU SCCs / UK IDTA / Canadian PIPEDA adequacy come into play.
- Azure OpenAI's geographic processing (some Azure OpenAI features fail over across regions for capacity reasons).

**SHOULD-FIX**: Add A-17 — "V1 processes data only in East US 2. Any tenant requiring EU / UK / Canada data residency triggers a Change Order. Microsoft will configure Azure OpenAI / Florence-2 with `DataZone=US` where the feature flag exists."

### 3.5 Sub-processor disclosure

The SOW does not enumerate sub-processors. For Walmart-the-controller to comply with GDPR Art. 28, the following must be disclosed:

| Sub-processor                       | Role                              | Data accessed            | Where to disclose                                                                |
| ----------------------------------- | --------------------------------- | ------------------------ | -------------------------------------------------------------------------------- |
| Microsoft Azure (platform)          | Infrastructure                    | All                      | Implicit                                                                         |
| Azure OpenAI Service                | Inference (GPT-5.2 Vision)        | Photo, height            | **MUST add**                                                                     |
| Azure AI Foundry (Florence-2)       | Inference                         | Photo                    | **MUST add**                                                                     |
| Azure AI Content Safety             | Moderation                        | Photo                    | **MUST add**                                                                     |
| GitHub (CI/CD)                      | Build artefacts (no shopper data) | Code, SBOM               | Should add                                                                       |
| Any abuse-monitoring human reviewer | Limited cases                     | Photo (if not opted out) | **MUST add** — and A-11 already implies opt-out; restate as a binding obligation |

**MUST-FIX**: Add §17.3 or Appendix M — "Sub-processors and data processing addenda." Confirm that Microsoft opts out of Azure OpenAI abuse monitoring for this workload (where eligible) and reflect this as an acceptance criterion under D-13.

---

## 4. Security Architecture & Controls

### 4.1 Identity, authentication, and authorization

The SOW correctly commits Entra ID OAuth 2.0, per-operation scopes (C-1), managed identities (implicit), and JWT validation. Gaps:

- **Token lifetime** is not stated; threat-model.md S-1 mitigation says "< 1 h." Make this contractual.
- **Multi-tenant isolation** is a critical security property (threat-model.md I-2). D-1 acceptance criteria should explicitly mention "integration tests verify cross-tenant isolation at the repository layer."
- **Conditional access / IP allow-listing per tenant** (S-1 mitigation) is not in the SOW. **SHOULD-FIX**: surface as a configurable feature in D-1 or add to A-12-equivalent assumption.

### 4.2 Network controls

- Private endpoints are mentioned in threat-model.md (I-1, T-5 mitigations) but the SOW does not commit them. **MUST-FIX**: state in D-7 (Bicep IaC) that private endpoints are configured for Cosmos DB, Blob Storage, Key Vault, Azure OpenAI (where supported), Azure AI Foundry, and Service Bus.
- Front Door / APIM WAF rate limiting is named in §16.1 but tier (Standard vs. Premium for Bot Manager) is unspecified. Premium is recommended for biometric-adjacent endpoints. **SHOULD-FIX**.
- DDoS Protection plan: §16.1 lists "WAF, rate limiting, TLS termination" but no Azure DDoS Protection Standard / Network reference. Threat-model.md D-1 mitigation lists DDoS Protection. **MUST-FIX**: align.

### 4.3 Cryptography

- TLS 1.2+ enforced (threat-model.md). The SOW does not state this. **SHOULD-FIX**: add to D-1 acceptance.
- At-rest encryption: implicit via Azure defaults. **SHOULD-FIX**: state customer-managed key (CMK) policy — accept Microsoft-managed keys for v1, treat CMK as a v2 change order, and document.
- Key rotation: not addressed. Key Vault keys / secrets rotation policy should be a D-7 acceptance criterion.

### 4.4 Logging and audit integrity

- Immutable audit container (threat-model.md T-4) is critical but not in SOW acceptance criteria. **MUST-FIX**: D-9 must require "tamper-evident audit log (append-only, immutable Cosmos container, hash-chain or equivalent)."
- PII scrubbing in telemetry (I-3 mitigation) — make this an explicit D-9 acceptance criterion.

### 4.5 Supply chain (CI/CD)

D-8 is strong: SAST + SCA + SBOM (CycloneDX) + Trivy + Notation signing. Recommended additions:

- **Pinned base images** with digest references (not floating tags). Make this an acceptance bullet.
- **Signed commits / branch protection** rules on `main` — make explicit.
- **Secret scanning** (GitHub Advanced Security / TruffleHog) — currently implied via SCA but worth calling out.
- **Dependency review action** — single line addition to CI.

**SHOULD-FIX**: Update D-8 acceptance criteria.

### 4.6 Container runtime hardening

- Container Apps runs the workload — `runAsNonRoot`, read-only root FS, dropped capabilities are golden-path defaults but not committed in the SOW. **SHOULD-FIX**: add to D-7 acceptance.

### 4.7 Secrets and configuration

- Key Vault and App Configuration are named (§16.1). The SOW does not require Key Vault references (not literal secrets) in container app environment variables. **SHOULD-FIX**: add to D-7.

---

## 5. AI/ML Specific Risks

### 5.1 Model risk and hallucination

The threat model lists **AI-5 Hallucinated measurements** as Medium/High but the SOW does not contractually address liability when the model is confidently wrong. Critical because BO-1 (≥ 20% return reduction) is a business outcome and could be reverse-engineered by Walmart Legal into a claim if returns increase due to bad recommendations.

- Existing protections: 70% confidence threshold + disclaimer (D-2), physiological plausibility checks (AI-5 mitigation), model card (D-11).
- Missing: a contractual disclaimer that **fit recommendations are advisory** and Walmart's storefront must convey "AI suggestion — not a guarantee." **MUST-FIX**: add to §17 or §18 as A-18 — "Walmart's storefront presents fit recommendations as advisory and includes the < 70% confidence disclaimer where applicable. Microsoft's liability is limited to delivering the confidence score and disclaimer string; final UX presentation is Walmart-owned."

### 5.2 Bias and fairness (AI-4)

AI-4 (Medium/High in threat model) — per-demographic accuracy is a model card concern. D-11 commits to a model card but does not require **per-demographic accuracy reporting**. **MUST-FIX**: D-11 acceptance criteria must include "report measurement accuracy stratified by body type, skin tone, and gender presentation on the calibration set, consistent with NIST AI RMF Measure function."

### 5.3 Prompt injection and adversarial input (E-3, AI-1, AI-2)

The threat model lists three related threats, all rated Medium. The SOW addresses this implicitly via D-2 (structured JSON output, temperature 0). **SHOULD-FIX**: D-2 acceptance criteria should include "image metadata is stripped before AI processing" and "system prompt is treated as a versioned, regression-tested code artefact."

### 5.4 Model drift and lifecycle

- D-9 commits dashboards but does not require **drift detection** against a ground-truth benchmark. AI-3 (model poisoning) and R-001 (accuracy) mitigations both reference drift detection.
- **MUST-FIX**: D-9 acceptance criteria add — "drift detection job runs weekly against the calibration set; ≥ ±2 cm degradation triggers an alert."

### 5.5 AI sub-processor data use

A-11 says photos are not used for training. This is a strong default but must be **contractual**, not just an assumption. **MUST-FIX**: convert A-11 from assumption to a binding Microsoft commitment, backed by Azure OpenAI service tier configuration committed in D-7 (Bicep modules) and verified in D-13 (DPIA package).

### 5.6 EU AI Act readiness (forward-looking)

A-15 excludes EU AI Act high-risk classification. Useful, but:

- VirtualMirror is **likely Annex III** (biometric categorisation / employment / education are high-risk; biometric measurement for retail is borderline but the regulator has flagged "biometric identification" broadly).
- Recommend documenting the position now so a future Change Order has a baseline. **SHOULD-FIX**: Add an Appendix M or note in §18.2 — "Microsoft's position is that VirtualMirror is not 'biometric identification' under EU AI Act Art. 3(33) because it does not match individuals against a database. This position will be revisited if the European Commission issues clarifying guidance."

---

## 6. Resilience, Availability & Incident Response

### 6.1 SLO commitments

§7 references "~99.9% availability SLO" (A-10). Strong. However:

- Service Level **Agreement** (with credits) vs. Service Level **Objective** (operational target) is conflated. Make explicit — this is an SLO without credit refunds.
- Composite SLO with sub-processor SLAs (Azure OpenAI ~99.9% Standard, Cosmos DB 99.99% multi-region with 99.999% read) is not computed. **SHOULD-FIX**: state the composite SLO math in §16 or §7.

### 6.2 DR and BCDR

- D-12 commits RTO < 1 h, RPO < 15 min for tenant config. Good.
- **Gap**: Per-tenant data DR (profile, garments, audit logs) is not specified. Cosmos DB defaults to local-redundant or zone-redundant; multi-region replication is excluded (§5 OOS). State the v1 stance: "zone-redundant Cosmos DB with single-region recovery; audit logs replicated to a second region via Change Feed (recommend)."

### 6.3 Incident response and breach notification — MAJOR GAP

§14 covers operational escalation (Levels 1–4) but **does not specify**:

| Element                                              | GDPR / CCPA / Industry expectation                  | SOW today                                                                 |
| ---------------------------------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------- |
| Security incident detection SLA                      | < 24 h from confirmed event                         | ❌ Missing                                                                |
| Customer notification SLA                            | ≤ 72 h after Microsoft becomes aware (GDPR Art. 33) | ❌ Missing                                                                |
| Incident classification (Sev 0–3, security-specific) | Required                                            | ❌ Missing — §11.3 covers defect severity, not security incident severity |
| Forensic preservation obligation                     | Required                                            | ❌ Missing                                                                |
| Joint IR playbook                                    | Recommended                                         | ❌ Missing                                                                |
| Right of audit                                       | Required by GDPR Art. 28(3)(h)                      | ❌ Missing                                                                |

**MUST-FIX**: Add §14.A "Security Incident Response and Breach Notification" with at minimum:

1. Security incident severity matrix (Sec-Sev 0/1/2/3).
2. Detection and notification SLAs (e.g., Sec-Sev 0 confirmed → customer notice within 24 h; preliminary forensic report within 5 business days).
3. Joint IR contact list and on-call escalation.
4. Walmart's right to audit security controls annually with reasonable notice.
5. Forensic preservation obligation triggered on suspected incident.

### 6.4 Hypercare vs. P1 SLA inconsistency — MUST-FIX

- §11.3 promises P1 fix within 4 hours.
- §17.2 says hypercare is "best-effort within business hours unless a managed-services SOW is signed."
- §19 trigger 1 says "hypercare period (30 calendar days post-go-live) is bounded and on-call response is best-effort within business hours."

**Resolve**: Either commit to 24×7 P1 response during hypercare (recommended given biometric data) OR explicitly state P1 SLAs apply only to defect tickets raised by Walmart and that production incident response is best-effort. The current text is contradictory.

---

## 7. Testing & Assurance

### 7.1 Penetration test — ownership gap (MUST-FIX)

§11.1 — "Penetration test | External vendor (Walmart-procured) | Pre-GA (Sprint 9)"
§17.2 — Walmart "manages" pen-test procurement.
§13.1 — Penetration test risk is not in the risk register.

Issues:

1. **Findings remediation responsibility**: §18.3 A-14 says findings "remediated within Sprint 9 or deferred via documented risk acceptance." Reasonable, but no capacity is reserved. **MUST-FIX**: add Sprint 9 buffer or a named contingency.
2. **Pen-test scope**: API, mobile, web, infrastructure, social engineering? Specify minimum scope (OWASP Web + API Security Top 10, ASVS L2 verification).
3. **Re-test obligation**: are critical / high findings re-tested before GA? Not stated. **MUST-FIX**.
4. **Pen-test timing risk**: a Sprint 9 pen-test that uncovers critical findings has no contingency window before GA. **SHOULD-FIX**: move pen-test start to Sprint 8 with retest in Sprint 9.

### 7.2 Compliance attestations and evidence package

D-12 / D-13 deliver DR plan and DPIA inputs. Missing:

- **Compliance evidence package** for Walmart's SOC 2 auditor — control evidence (auth, audit, encryption, change management, monitoring). **SHOULD-FIX**: add to D-14 (KT package).
- **ASVS L2 self-assessment** — see §2.1 above. **MUST-FIX**.
- **Threat model update at GA** — threat-model.md is dated 2026-05-14 (today); commit to refreshing at end of Sprint 8. **SHOULD-FIX**: add to D-12.

### 7.3 Coverage gates — security-critical paths

§11.4 — "≥ 80% line, ≥ 90% on critical paths." "Critical paths" is undefined.

**MUST-FIX**: Define "critical paths" enumeratively:

- Auth middleware (JWT validation, scope enforcement, tenant extraction)
- Multi-tenant repository base class (cross-tenant isolation guard)
- Profile deletion cascade (24 h SLA enforcement)
- Audit log writer (append-only invariants)
- Image purge logic (60 s TTL)
- Confidence threshold + degradation ladder logic
- Content Safety integration (refusal path for minors / unsafe content)

### 7.4 Chaos and load testing — adequate but extend

D-10 covers 500 concurrent + chaos. Add:

- **Soak test minimum 4 hours** (30 min is in current scope; useful but short for memory-leak detection).
- **Tenant-isolation chaos**: induce a misconfigured tenant claim and verify cross-tenant access is denied. **SHOULD-FIX**.

---

## 8. Contractual & Legal

### 8.1 Controller / processor allocation

The SOW does not state Microsoft's role under GDPR / CCPA. Given the architecture, Microsoft is a **processor** to Walmart-the-controller (with Azure OpenAI / Florence-2 as sub-processors).

**MUST-FIX**: Add §17.4 (or amend §2.3 Engagement Model) — "Roles under GDPR/CCPA: Walmart is the data controller; Microsoft Industry Solutions Delivery is a processor delivering the service on Walmart's instructions; Azure OpenAI Service, Azure AI Foundry (Florence-2), and Azure AI Content Safety are sub-processors as defined in their respective Product Terms / DPA. The Microsoft Online Services Data Protection Addendum (DPA) governs sub-processor obligations."

### 8.2 Indemnities, warranties, limitation of liability

Out of scope for this SOW since these are typically in the Master Services Agreement (MSA). However:

- **AI-specific carve-out**: most MSAs were written before LLM hallucination risk. Confirm with Microsoft Legal whether the MSA's IP indemnity and warranty disclaim AI hallucination liability. Document in §20 Appendix.
- **Copyright assist (training data warranty)**: Azure OpenAI offers "Customer Copyright Commitment." Flag in the SOW that this commitment carries through, conditional on Walmart following the use guidelines (no opt-out from content filtering, etc.).

### 8.3 Data deletion on exit (MUST-FIX)

§19 lists 5 completion triggers, including termination (5). The SOW is silent on:

- **What happens to shopper profiles, assessment history, audit logs, and tenant config on termination?**
- **What's Microsoft's data-return obligation?**
- **What's the destruction timeline and certificate of destruction?**

**MUST-FIX**: Add §19.A "Data return and destruction" — "On engagement completion or termination, Microsoft will, at Walmart's election within 30 days, (a) export tenant data in agreed formats, (b) destroy production data per the agreed retention schedule (audit logs retained 7 years; biometric-derived data destroyed within 30 days; tenant config destroyed within 30 days), and (c) provide a certificate of destruction."

### 8.4 Insurance and assurance

Optional but recommended: state minimum insurance carriage (cyber liability) — often handled in the MSA, but for biometric-adjacent workloads worth confirming the MSA covers BIPA-style statutory damages.

---

## 9. Scope, Estimation, and Risk Hygiene

### 9.1 Scope-trap completeness (Worksheet B.3)

ST-1 through ST-10 are reasonable. Missing:

- **ST-11**: Increased biometric law exposure (additional state biometric privacy laws coming online — NY, CA SB 1189, etc.). +5–10 PD for compliance review and consent flow updates.
- **ST-12**: AI Act high-risk classification triggered by regulatory clarification mid-engagement. Already partially captured via A-15; restate as scope trap.
- **ST-13**: Mandatory third-party security assessment beyond pen test (e.g., HITRUST, ISO 27001 readiness). +30–60 PD.

### 9.2 Risk register coverage of SOW-level risks

§13.1 / 13.2 are good but should add the following plan-level risks:

| New PR | Risk                                                                               | Severity | Mitigation                                                       |
| ------ | ---------------------------------------------------------------------------------- | -------- | ---------------------------------------------------------------- |
| PR-7   | BIPA / state biometric law exposure higher than assumed                            | **HIGH** | Legal opinion in Sprint 1; A-16 consent capture; D-11 model card |
| PR-8   | Azure OpenAI quota / PTU not provisioned by Sprint 3                               | **HIGH** | Already covered partially by C-2 but escalate to a risk          |
| PR-9   | Security incident in production during hypercare                                   | MEDIUM   | §14.A IR playbook; Sec-Sev runbook                               |
| PR-10  | Sub-processor change (Azure OpenAI / Florence-2 region or terms) during engagement | MEDIUM   | DPA tracking; named sub-processor list in §17.3                  |

---

## 10. Recommended Changes Before Signature

### 10.1 MUST-FIX (block signature)

|  #  | Change                                                                                                               | Section             |
| :-: | -------------------------------------------------------------------------------------------------------------------- | ------------------- |
|  1  | State controller/processor roles under GDPR/CCPA; reference Microsoft DPA                                            | §2.3 / §17.4 (new)  |
|  2  | Name sub-processors handling biometric-adjacent data; commit to Azure OpenAI abuse-monitoring opt-out where eligible | §17.3 (new) / D-13  |
|  3  | Document biometric law assumption (BIPA, TX CUBI, WA HB1155) and storefront consent capture obligation               | A-16 (new)          |
|  4  | Add Security Incident Response & Breach Notification section with Sec-Sev matrix, 72-h notification SLA, audit right | §14.A (new)         |
|  5  | Resolve hypercare vs. P1 SLA inconsistency                                                                           | §11.3 / §17.2 / §19 |
|  6  | Reserve pen-test remediation capacity; require re-test for Critical/High                                             | §11.1 / §18.3 A-14  |
|  7  | Add ASVS L2 self-assessment / gap report as D-15                                                                     | §15 / Worksheet B.1 |
|  8  | Convert A-11 (no training on shopper data) from assumption to binding commitment                                     | §18.2               |
|  9  | Add data-return and destruction clause on termination                                                                | §19.A (new)         |
| 10  | Define "critical paths" enumeratively for the 90% coverage gate                                                      | §11.4               |
| 11  | Specify private endpoints, DDoS Standard, TLS 1.2+ enforcement, container hardening in D-7 acceptance                | D-7                 |
| 12  | D-11 model card must report per-demographic accuracy stratification (NIST AI RMF Measure)                            | D-11                |
| 13  | D-9 dashboards must include drift detection and 60-s photo purge SLO                                                 | D-9                 |
| 14  | Add advisory-disclaimer obligation on Walmart's storefront (AI fit recommendation framing)                           | A-18 (new)          |
| 15  | State retention for assessment results (365 d) and audit logs (≥ 12 mo, ideally 7 y) in SOW                          | §15 / D-12          |
| 16  | Confirm DSAR responsibilities: read/export = Walmart, deletion = Microsoft API                                       | §17.4               |
| 17  | Audit log tamper-evidence (immutable container + hash chain) as D-9 acceptance                                       | D-9                 |

### 10.2 SHOULD-FIX (negotiate but don't block)

|  #  | Change                                                                        | Section           |
| :-: | ----------------------------------------------------------------------------- | ----------------- |
| 18  | Map deliverables to SOC 2 TSC and NIST CSF 2.0 functions                      | §3.2 / Appendix L |
| 19  | Add EU AI Act risk classification memo                                        | Appendix M (new)  |
| 20  | Cross-border processing assumption (single-region East US 2)                  | A-17 (new)        |
| 21  | Compute composite SLO with sub-processor SLAs                                 | §7 / §16          |
| 22  | Extend soak test from 30 min to ≥ 4 h                                         | D-10              |
| 23  | Tenant-isolation chaos test scenario                                          | D-10              |
| 24  | Pinned base image digests, signed commits, secret scanning, dependency review | D-8               |
| 25  | Front Door tier (Premium for Bot Manager)                                     | §16.1             |
| 26  | Customer-managed key (CMK) policy stance for v1 vs. v2                        | D-7               |
| 27  | Key rotation policy for Key Vault                                             | D-7               |
| 28  | Branch protection rules and signed commits                                    | D-8               |
| 29  | Add PR-7..PR-10 to risk register                                              | §13.1             |
| 30  | Add ST-11..ST-13 to scope traps                                               | Worksheet B.3     |
| 31  | Threat model refresh at end of Sprint 8                                       | D-12              |
| 32  | Compliance evidence package for Walmart SOC 2 auditor                         | D-14              |

### 10.3 NICE-TO-HAVE (post-signature)

- ISO 27001 / 27701 control mapping for future certification path.
- NIST AI RMF Govern/Map/Measure/Manage mapping in model card.
- Privacy notice template for Walmart's storefront UX (Walmart Legal owns, but Microsoft can draft from DPIA inputs).
- Continuous control monitoring via Defender for Cloud regulatory compliance dashboard.

---

## 11. Approval

| Reviewer | Role                                     | Decision                                               | Date       |
| -------- | ---------------------------------------- | ------------------------------------------------------ | ---------- |
| _TBD_    | Microsoft ISD Security & Compliance Lead | Conditional Pass — see §10.1 MUST-FIX before signature | 2026-05-14 |
| _TBD_    | Walmart CISO / Privacy Office            | Pending                                                | _TBD_      |
| _TBD_    | Microsoft Legal                          | Pending — §8 items                                     | _TBD_      |
| _TBD_    | Walmart Legal                            | Pending                                                | _TBD_      |

---

## Version history

| Version | Date       | Reviewer                                   | Status | Summary                                        |
| ------: | ---------- | ------------------------------------------ | ------ | ---------------------------------------------- |
|   0.1.0 | 2026-05-14 | Microsoft ISD Security & Compliance Review | Draft  | Initial review of Virtual-Mirror-SOW.md v0.1.0 |

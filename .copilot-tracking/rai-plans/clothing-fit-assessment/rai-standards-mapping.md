# RAI Standards Mapping: AI Clothing Fit Assessment Agent

**Project Slug**: `clothing-fit-assessment`
**Assessment Date**: 2026-05-14
**Framework**: NIST AI Risk Management Framework 1.0 (NIST.AI.100-1)
**Depth Tier**: Comprehensive

## Trustworthiness Characteristic Mapping

### 1. Valid and Reliable (MS-2.5) — Base Characteristic

| Aspect | Assessment |
|--------|-----------|
| **Component** | GPT-5.2 Vision (measurement extraction) |
| **Validity concern** | ±2–4 cm accuracy is a hypothesis (H1) not yet validated; non-deterministic LLM output means repeated assessments of the same photo may yield different measurements |
| **Reliability concern** | No ground-truth validation dataset; accuracy may degrade with model version updates; no regression testing baseline established |
| **Existing controls** | Confidence scoring (0.0–1.0); 70% low-confidence threshold with disclaimer; model version tracked per assessment |
| **Gaps** | No demographic-segmented accuracy benchmarking; no regression test suite for model updates; no accuracy monitoring in production |
| **NIST subcategories** | MS-2.5 (validity demonstration), MS-2.3 (deployment conditions), MS-2.13 (TEVV effectiveness) |

| Aspect | Assessment |
|--------|-----------|
| **Component** | Florence-2 (people detection) |
| **Validity concern** | Bounding box detection accuracy across body types and photo conditions not validated |
| **Reliability concern** | 70% frame height threshold may reject valid photos from wheelchair users or seated individuals |
| **Existing controls** | Detection confidence scoring; multi-person rejection |
| **Gaps** | No accessibility testing for detection thresholds; no false-positive/false-negative rate tracking |

**Suggested Status**: Partially addressed — confidence scoring exists but no validation against ground truth or demographic segments.

---

### 2. Safe (MS-2.6)

| Aspect | Assessment |
|--------|-----------|
| **Physical safety** | Not safety-critical — clothing recommendations only |
| **Psychological safety** | Body-related AI output could affect self-image; system directly comments on human body fit ("Too Tight at Hips") |
| **Vulnerable populations** | Users with eating disorders, body dysmorphia, or body image concerns; adolescents near the 16-year boundary |
| **Existing controls** | Minor detection (under-16 blocked); constitution prohibits body-shaming language; low-confidence disclaimer; human escalation path |
| **Gaps** | No language review framework for fit recommendation phrasing; no user testing with body-image-sensitive populations; no opt-out for body-specific commentary |
| **Failure modes** | Degradation ladder (L1–L5) handles AI unavailability; no specific degradation for body-sensitivity scenarios |
| **NIST subcategories** | MS-2.6 (safety evaluation), GV-4.1 (safety-first mindset) |

**Suggested Status**: Partially addressed — physical safety is not a concern but psychological safety controls are incomplete.

---

### 3. Secure and Resilient (MS-2.7)

| Aspect | Assessment |
|--------|-----------|
| **Adversarial robustness** | No adversarial robustness testing for GPT-5.2 Vision (manipulated images to produce desired measurements) |
| **Prompt injection** | Image metadata could contain prompt injection payloads targeting GPT-5.2 structured output |
| **Model integrity** | Pre-trained models served via Azure managed endpoints; no model weight tampering risk in v1 |
| **Data poisoning** | Inference-only system; no training loop — data poisoning is limited to garment data ingestion |
| **Resilience** | Polly resilience pipelines, AI failover (primary/secondary), degradation ladder (L1–L5), DLQ processing |
| **Existing controls** | Content Safety filtering, input validation (format, size, MIME), rate limiting, tenant bulkhead |
| **Gaps** | No adversarial image testing; no prompt injection defense in measurement extraction prompt; no EXIF metadata stripping before AI processing |
| **NIST subcategories** | MS-2.7 (security evaluation), GV-6.2 (third-party contingency) |

**Suggested Status**: Partially addressed — strong resilience infrastructure but adversarial AI attack surface not tested.

---

### 4. Accountable and Transparent (MS-2.8) — Cross-Cutting Vertical

| Aspect | Assessment |
|--------|-----------|
| **Audit trail** | Every assessment logged with model version, tenant, shopperRef, correlationId, confidence, processing duration |
| **Decision traceability** | Fit recommendation traceable to specific model version + input photo + garment data |
| **AI disclosure** | FR-015 requires informing users they are interacting with AI; `isLowConfidence` + `disclaimer` fields in API response |
| **Organizational accountability** | Constitution defines AI Ethics Review Board approval for model deployment changes |
| **Third-party transparency** | Azure OpenAI data processing documented; data not used for training |
| **Existing controls** | Immutable audit logs (Cosmos), model version tracking, OpenTelemetry tracing, structured logging |
| **Gaps** | No public-facing transparency note or model card (user declined optional artifact); no shopper-accessible explanation of how measurements are derived |
| **NIST subcategories** | MS-2.8 (transparency assessment), GV-2.1 (roles and responsibilities), GV-1.4 (transparent policies) |

**Suggested Status**: Mostly addressed — strong audit and traceability but no public-facing transparency documentation.

---

### 5. Explainable and Interpretable (MS-2.9)

| Aspect | Assessment |
|--------|-----------|
| **Model explainability** | GPT-5.2 is a black-box LLM; measurement extraction process is opaque; no explanation of how body dimensions are derived from the photo |
| **Output interpretability** | Per-area fit scores (5-point scale) are interpretable; confidence percentage provides uncertainty signal |
| **User understanding** | Shoppers see fit results but cannot understand why the AI measured their body in a particular way |
| **Recourse** | Low-confidence results include disclaimer + escalation URL; no mechanism for shoppers to dispute or correct measurements |
| **Existing controls** | Confidence scoring, per-area breakdown, low-confidence disclaimer, escalation path |
| **Gaps** | No measurement explanation (why shoulder width = X cm); no measurement dispute/correction mechanism; no visualization of detected body landmarks |
| **NIST subcategories** | MS-2.9 (explainability evaluation), MP-2.2 (knowledge limits) |

**Suggested Status**: Partially addressed — outputs are interpretable but the extraction process is a black box with no dispute mechanism.

---

### 6. Privacy-Enhanced (MS-2.10)

| Aspect | Assessment |
|--------|-----------|
| **Data classification** | Body photos classified as biometric-adjacent / special category (GDPR Art. 9); derived measurements as Confidential |
| **Data minimization** | Photos processed transiently (60s TTL); only derived measurements stored; opaque shopper IDs; no PII in telemetry |
| **Consent** | Explicit consent required for profile storage (`saveProfile` flag + `consentGrantedAt` timestamp); photo processing requires frontend consent capture |
| **Right to erasure** | Hard delete within 24h; audit log entry retained; cascading purge across containers |
| **Data processing location** | Single-region Azure deployment; international transfer via SCCs |
| **Third-party processing** | Azure OpenAI: data not used for training, not shared; AES-256 encryption at rest |
| **DPIA** | Required before processing new categories of personal data (constitution Principle I) |
| **Existing controls** | Transient blob storage, opaque IDs, consent gating, hard delete, 24h fulfillment, DPA templates |
| **Gaps** | No completed DPIA on file; consent flow ownership unclear (frontend vs API boundary); abuse monitoring data retention in Azure OpenAI not addressed |
| **NIST subcategories** | MS-2.10 (privacy risk assessment), GV-1.1 (legal requirements) |

**Suggested Status**: Mostly addressed — strong privacy-by-design architecture but DPIA not yet completed and consent boundary not formalized.

---

### 7. Fair with Harmful Bias Managed (MS-2.11)

| Aspect | Assessment |
|--------|-----------|
| **Bias sources** | GPT-5.2 pre-training data may underrepresent certain body types, skin tones, or cultural contexts; Florence-2 detection may perform unevenly across demographics |
| **Demographic coverage** | Body types (hourglass, pear, apple, rectangular, athletic), body sizes (petite to plus-size), skin tones (Fitzpatrick I–VI), gender presentation, age (18–70+), disabilities, cultural dress, pregnancy |
| **Measurement accuracy parity** | No demographic-segmented accuracy benchmarking planned; ±2–4 cm may be worse for certain groups |
| **Output fairness** | Fit recommendation quality directly depends on measurement accuracy — if accuracy varies by demographic, service quality is unequal |
| **Language fairness** | Constitution prohibits body-shaming; but fit scale terminology ("Too Tight", "Too Loose") has not been evaluated for implicit judgment |
| **Existing controls** | Constitution Principle III requires bias evaluation before deployment; model accuracy per demographic segment tracking planned |
| **Gaps** | No bias evaluation dataset or methodology defined; no accuracy parity thresholds established; no disparate impact testing plan; no language sensitivity review for fit recommendation phrasing |
| **NIST subcategories** | MS-2.11 (fairness evaluation), GV-3.1 (diverse teams), GV-3.2 (human oversight) |

**Suggested Status**: Not yet addressed — bias evaluation is acknowledged as a requirement but no methodology, dataset, or thresholds are defined.

---

## Regulatory Jurisdiction Assessment

| Regulation | Applicability | Key Obligations |
|------------|--------------|-----------------|
| **GDPR** (EU) | High — body photos are special category biometric data (Art. 9) | Explicit consent, DPIA, data minimization, right to erasure, 72h breach notification, DPA with processors |
| **CCPA** (California) | High — body measurements are personal information; potential biometric data | Right to delete, right to know, right to opt-out, notice at collection |
| **EU AI Act** | Medium-High — body-image AI processing may qualify as high-risk AI system | Risk classification assessment, conformity assessment, human oversight, transparency obligations |
| **State biometric privacy laws** (IL BIPA, TX CUBI, WA) | Medium — if deployed for tenants in these states | Written consent before collection, data retention/destruction policies, private right of action (BIPA) |
| **FTC Section 5** | Medium — deceptive AI practices or unfair data handling | Fair and non-deceptive AI disclosures; no unfair or deceptive practices |

**Note**: Detailed regulatory obligation mapping for EU AI Act, specific state laws, and sector-specific regulations should be delegated to legal counsel. This mapping identifies applicability, not compliance determination.

## NIST Subcategory Coverage Summary

| Function | Category | Coverage | Evidence |
|----------|----------|----------|----------|
| Govern | GV-1 (Policies) | Partial | Constitution defines principles; no formal AI risk management policy document |
| Govern | GV-2 (Accountability) | Partial | AI Ethics Board referenced; specific roles not assigned |
| Govern | GV-3 (DEI&A) | Gap | No diverse team requirement documented; no accessibility testing |
| Govern | GV-4 (Risk culture) | Partial | Constitution + risk register; no incident sharing protocol |
| Govern | GV-5 (Stakeholder engagement) | Gap | No external feedback mechanism for shoppers |
| Govern | GV-6 (Third-party risk) | Partial | Azure OpenAI CoC processed; Florence-2 terms unknown |
| Map | MP-1 (Context) | Covered | System definition pack complete |
| Map | MP-2 (Categorization) | Covered | AI component inventory with knowledge limits noted |
| Map | MP-3 (Capabilities) | Partial | Benefits documented; negative impacts partially assessed |
| Map | MP-4 (Third-party) | Partial | Azure dependency documented; IP/legal risk not fully mapped |
| Map | MP-5 (Impact) | Partial | Stakeholder impact map created; quantified impact assessment pending |
| Measure | MS-1 (Methods) | Gap | No TEVV methodology or metrics defined |
| Measure | MS-2.5 (Valid/Reliable) | Partial | Confidence scoring exists; no validation dataset |
| Measure | MS-2.6 (Safe) | Partial | Minor detection + degradation; no psychological safety testing |
| Measure | MS-2.7 (Secure/Resilient) | Partial | Strong resilience infra; no adversarial AI testing |
| Measure | MS-2.8 (Accountable/Transparent) | Mostly | Audit trail + model versioning; no public transparency note |
| Measure | MS-2.9 (Explainable) | Partial | Output interpretable; extraction process opaque |
| Measure | MS-2.10 (Privacy) | Mostly | Privacy by design; DPIA not completed |
| Measure | MS-2.11 (Fair/Bias) | Gap | No bias methodology, dataset, or parity thresholds |
| Measure | MS-2.12 (Environmental) | Gap | No environmental impact assessment |
| Manage | MN-1 (Prioritization) | Pending | Phase 5 |
| Manage | MN-2 (Benefit/Impact) | Pending | Phase 5 |
| Manage | MN-3 (Third-party) | Pending | Phase 5 |
| Manage | MN-4 (Documentation) | Pending | Phase 5 |

## Principle Tracker Summary

| Characteristic | Status | Mapped | Key Gap |
|----------------|--------|--------|---------|
| Valid and Reliable | Partially addressed | ✅ | No validation dataset or regression testing |
| Safe | Partially addressed | ✅ | No psychological safety testing for body-image-sensitive users |
| Secure and Resilient | Partially addressed | ✅ | No adversarial AI testing |
| Accountable and Transparent | Mostly addressed | ✅ | No public-facing transparency documentation |
| Explainable and Interpretable | Partially addressed | ✅ | Black-box extraction; no dispute mechanism |
| Privacy-Enhanced | Mostly addressed | ✅ | DPIA not completed; consent boundary unclear |
| Fair with Harmful Bias Managed | Not yet addressed | ✅ | No bias methodology, dataset, or parity thresholds defined |

# RAI Threat Addendum: AI Clothing Fit Assessment Agent

**Project Slug**: `clothing-fit-assessment`
**Assessment Date**: 2026-05-14
**Framework**: NIST AI Risk Management Framework 1.0
**Depth Tier**: Comprehensive
**Entry Mode**: from-prd (no Security Planner cross-references)

## Applicable AI Element Types

| Element Type | System Component | Present? |
|-------------|-----------------|----------|
| Training Data Store | N/A — inference-only system; no custom training | No |
| Model Artifact | GPT-5.2 Vision, Florence-2, Content Safety (pre-trained, managed by Azure) | Yes (managed) |
| Inference Endpoint | Azure OpenAI endpoint, AI Foundry managed endpoint, Content Safety endpoint | Yes |
| Feature Pipeline | Image pre-processing (validation, format check, MIME, luminance) | Yes |
| Feedback Loop | N/A — v1 has no feedback-to-retraining loop | No |
| Human Review Queue | Low-confidence escalation path (< 70% → disclaimer + escalation URL) | Yes (partial) |
| Monitoring Dashboard | OpenTelemetry → Azure Monitor (model drift, accuracy, latency) | Yes (planned) |
| Orchestration Layer | VirtualMirrormentService pipeline (validate → extract → compare → audit) | Yes |

## Applicable Trust Boundaries

| Trust Boundary | System Location | Relevance |
|---------------|----------------|-----------|
| Inference Boundary | Client request → Image validation → GPT-5.2 / Florence-2 processing | Primary threat surface |
| Model Boundary | Azure-managed model internals ↔ API response | Managed by Azure; limited control |
| Human Oversight Boundary | Automated fit recommendation ↔ shopper decision | Accountability transfer point |

## Threat Table

| RAI ID | STRIDE | NIST Characteristic | NIST AI RMF | Description | AI Element | Trust Boundary | Threat Origin | Concern Level | Mitigation |
|--------|--------|-------------------|-------------|-------------|-----------|---------------|---------------|---------------|------------|
| T-RAI-001 | Tampering | Fair with Harmful Bias Managed | MS-2.11 | **Demographic accuracy disparity**: GPT-5.2 measurement extraction may be less accurate for certain body types, skin tones, sizes, or cultural dress, creating unequal service quality | Inference Endpoint | Inference Boundary | Model | High Concern | Demographic-segmented accuracy benchmarking; parity threshold definition; diverse validation dataset; ongoing production monitoring per segment |
| T-RAI-002 | Tampering | Valid and Reliable | MS-2.5 | **Adversarial image manipulation**: Crafted images designed to produce desired measurements (e.g., manipulated photos to get a specific fit recommendation) | Inference Endpoint | Inference Boundary | Interface | Moderate Concern | EXIF metadata stripping; image integrity validation; anomaly detection on measurement distributions; Content Safety pre-screening |
| T-RAI-003 | Elevation of Privilege | Secure and Resilient | MS-2.7 | **Prompt injection via image metadata**: EXIF, IPTC, or XMP metadata in uploaded photos could contain prompt injection payloads targeting GPT-5.2 structured output schema | Inference Endpoint | Inference Boundary | Interface | High Concern | Strip all image metadata before AI processing; validate structured output schema conformance; prompt hardening with system message boundaries |
| T-RAI-004 | Information Disclosure | Privacy-Enhanced | MS-2.10 | **Model inversion / measurement leakage**: Repeated queries with slightly modified inputs could allow reconstruction of another shopper's body measurements or reveal model behavior patterns | Inference Endpoint | Model Boundary | Model | Moderate Concern | Rate limiting per shopperRef; no cross-tenant data access; stateless model (no memory); differential privacy considerations for future versions |
| T-RAI-005 | Tampering | Safe | MS-2.6 | **Body-image harm via fit language**: Fit recommendation terminology ("Too Tight at Hips", "Too Loose") could cause psychological distress for body-image-sensitive shoppers | Orchestration Layer | Human Oversight Boundary | Cross-cutting | High Concern | Language sensitivity review; user-tested phrasing alternatives; option for neutral measurement-only mode; content guidelines for fit output |
| T-RAI-006 | Repudiation | Accountable and Transparent | MS-2.8 | **Unattributable recommendation errors**: If a shopper receives a bad fit recommendation leading to a return, the system must trace the recommendation to model version + input data for accountability | Orchestration Layer | Human Oversight Boundary | Cross-cutting | Low Concern | Already mitigated: audit trail logs model version, correlationId, confidence, processing duration per assessment |
| T-RAI-007 | Tampering | Fair with Harmful Bias Managed | MS-2.11 | **Tolerance band bias**: Default tolerance bands (tight: 4cm, comfort: 2cm, loose: 5cm) may not be appropriate across all body sizes — applying the same absolute thresholds to petite and plus-size shoppers creates inequitable fit scoring | Orchestration Layer | Inference Boundary | Model | High Concern | Size-proportional tolerance bands; configurable per tenant + garment category; validation against diverse body size data |
| T-RAI-008 | Information Disclosure | Privacy-Enhanced | MS-2.10 | **Photo retention beyond 60s TTL**: Implementation bugs or storage failures could cause shopper photos to persist beyond the 60-second purge window, violating privacy commitments | Feature Pipeline | Inference Boundary | Infrastructure | Moderate Concern | Automated purge verification; blob lifecycle policy enforcement; alerting on photos older than 60s; periodic compliance audits |
| T-RAI-009 | Denial of Service | Valid and Reliable | MS-2.5 | **AI model degradation under load**: GPT-5.2 measurement accuracy may degrade under high concurrent load (token throttling, response truncation) without the system detecting the quality drop | Inference Endpoint | Inference Boundary | Infrastructure | Moderate Concern | Per-request confidence validation; load-dependent accuracy monitoring; circuit breaker + degradation ladder; accuracy regression alerts |
| T-RAI-010 | Spoofing | Valid and Reliable | MS-2.5 | **Non-deterministic output variance**: Same photo + height input may produce different measurements across requests due to LLM non-determinism, undermining user trust and repeatability | Inference Endpoint | Model Boundary | Model | Moderate Concern | Temperature=0 configuration; structured output schema enforcement; measurement caching for repeat assessments; variance monitoring |
| T-RAI-011 | Tampering | Explainable and Interpretable | MS-2.9 | **Opaque measurement extraction**: Shoppers cannot understand how the AI derived their body measurements, preventing meaningful consent and creating distrust when results feel wrong | Inference Endpoint | Human Oversight Boundary | Model | High Concern | Measurement explanation annotations (future); body landmark visualization (v2); dispute mechanism allowing measurement correction; size chart comparison view |
| T-RAI-012 | Tampering | Fair with Harmful Bias Managed | MS-2.11 | **Florence-2 detection bias**: People detection may perform unevenly for wheelchair users, users with prosthetics, users in loose/cultural garments, or users with certain body proportions, causing disproportionate image rejection | Feature Pipeline | Inference Boundary | Model | High Concern | Accessibility testing for Florence-2 detection thresholds; alternative validation paths for users who fail standard detection; rejection rate monitoring per demographic proxy |
| T-RAI-013 | Tampering | Safe | MS-2.6 | **Minor boundary exploitation**: Age detection at the 16-year boundary is imprecise; near-boundary individuals (15–17) may be incorrectly included or excluded | Feature Pipeline | Inference Boundary | Model | Moderate Concern | Content Safety age detection with conservative threshold; parental consent flow for near-boundary cases (future); audit logging of age detection decisions |
| T-RAI-014 | Repudiation | Accountable and Transparent | MS-2.8 | **Consent provenance gaps**: The API accepts a `saveProfile` flag and `consentGrantedAt` timestamp from the frontend, but has no way to verify that actual consent was obtained from the shopper | Orchestration Layer | Human Oversight Boundary | Interface | Moderate Concern | Consent receipt format specification; frontend SDK consent UX guidelines; audit trail includes consent metadata; contractual DPA obligations on tenants |

## Threat Origin Summary

### Model-Origin Threats (5)

| RAI ID | Concern | Summary |
|--------|---------|---------|
| T-RAI-001 | High | Demographic accuracy disparity in measurement extraction |
| T-RAI-004 | Moderate | Model inversion / measurement leakage via repeated queries |
| T-RAI-007 | High | Tolerance band bias across body sizes |
| T-RAI-010 | Moderate | Non-deterministic output variance undermining trust |
| T-RAI-011 | High | Opaque measurement extraction preventing meaningful consent |

### Interface-Origin Threats (3)

| RAI ID | Concern | Summary |
|--------|---------|---------|
| T-RAI-002 | Moderate | Adversarial image manipulation |
| T-RAI-003 | High | Prompt injection via image metadata |
| T-RAI-014 | Moderate | Consent provenance gaps from frontend |

### Cross-Cutting Threats (2)

| RAI ID | Concern | Summary |
|--------|---------|---------|
| T-RAI-005 | High | Body-image harm via fit recommendation language |
| T-RAI-006 | Low | Unattributable recommendation errors (already mitigated) |

### Infrastructure-Origin Threats (2)

| RAI ID | Concern | Summary |
|--------|---------|---------|
| T-RAI-008 | Moderate | Photo retention beyond 60s TTL |
| T-RAI-009 | Moderate | AI model accuracy degradation under load |

### Feature Pipeline Threats (2)

| RAI ID | Concern | Summary |
|--------|---------|---------|
| T-RAI-012 | High | Florence-2 detection bias against users with disabilities/cultural dress |
| T-RAI-013 | Moderate | Minor boundary exploitation at age 16 threshold |

## ML STRIDE Matrix (VirtualMirror-Specific)

Applied to VirtualMirror AI components with NIST characteristic annotations. Regulatory cross-references included for mixed audience.

| Component | Spoofing | Tampering | Repudiation | Info Disclosure | DoS | EoP |
|-----------|----------|-----------|-------------|-----------------|-----|-----|
| **GPT-5.2 Vision** (Inference) | Medium / Valid & Reliable — adversarial photos | High / Fair & Bias — demographic accuracy disparity | Medium / Accountable — audit trail exists | Medium / Privacy — model inversion risk | Medium / Valid & Reliable — load degradation | High / Secure — prompt injection via metadata |
| **Florence-2** (Validation) | Low | High / Fair & Bias — detection bias for disabilities/cultural dress | Low | Low | Low | Low |
| **Content Safety** (Moderation) | Low | Medium / Safe — minor boundary imprecision | Low | Low | Low | Low |
| **FitComparisonEngine** (Deterministic) | N/A | High / Fair & Bias — tolerance band bias across body sizes | Low | N/A | N/A | N/A |
| **VirtualMirrormentService** (Orchestration) | Low | High / Safe — body-image harm via language | Medium / Accountable — consent provenance | Low | Low | Low |

*Note*: EU AI Act may classify this system as high-risk AI given biometric-adjacent processing. GDPR Art. 9 obligations apply to photo processing. State biometric privacy laws (IL BIPA) may require written consent before collection.

## Concern Level Distribution

| Level | Count | Percentage |
|-------|-------|-----------|
| High Concern | 6 | 43% |
| Moderate Concern | 7 | 50% |
| Low Concern | 1 | 7% |
| **Total Threats** | **14** | |

The high proportion of High Concern threats (43%) reflects the biometric-adjacent nature of the system and body-image sensitivity of the outputs. The two dominant threat clusters are **fairness/bias** (T-RAI-001, T-RAI-007, T-RAI-012) and **body-image safety** (T-RAI-005, T-RAI-011).

# Risk Register: AI Clothing Fit Assessment Agent

**Version**: 1.0.0 | **Date**: 2026-05-13 | **Status**: Active
**Review cadence**: Monthly or after any severity change

## Risk Matrix

| Likelihood → | Low | Medium | High |
|--------------|-----|--------|------|
| **High Impact** | MEDIUM | HIGH | CRITICAL |
| **Medium Impact** | LOW | MEDIUM | HIGH |
| **Low Impact** | LOW | LOW | MEDIUM |

## Active Risks

### R-001: GPT-5.2 Vision Measurement Accuracy

| Field | Value |
|-------|-------|
| **Category** | Technical |
| **Impact** | High |
| **Likelihood** | High |
| **Severity** | CRITICAL |
| **Owner** | Engineering Lead |
| **Related ADR** | [ADR-001](decision-register.md#adr-001-body-measurement-extraction-approach) |

**Description**: Azure OpenAI GPT-5.2 Vision is a general-purpose multimodal LLM, not a body measurement specialist. Estimated accuracy is ±2–4 cm (under validation, expected improvement with GPT-5.2), which may be insufficient for tight-fitting garments. The model is non-deterministic — identical inputs can produce different measurements across calls. Migration to GPT-5.2 eliminates the prior GPT-4o retirement risk, but accuracy validation remains required.

**Mitigations**:

- Mandatory height input provides absolute scale reference (ADR-008)
- Confidence calibration against known measurement datasets during integration testing
- 70% confidence threshold triggers fallback with disclaimer and escalation URL
- Prompt engineering treated as a versioned code artifact with regression tests
- v2 path: custom SMPL body model on Azure AI Foundry (±1–2 cm)

**Trigger**: Integration testing shows > 15% of assessments produce measurements outside ±4 cm of ground truth.

**Contingency**: Engage third-party measurement API (3DLOOK) as interim bridge while custom model is developed. Accept higher per-call cost and data processing agreement overhead.

---

### R-002: Azure AI Vision 4.0 Deprecation (MITIGATED)

| Field | Value |
|-------|-------|
| **Category** | Technical / Vendor |
| **Impact** | Low |
| **Likelihood** | Low |
| **Severity** | LOW |
| **Owner** | Engineering Lead |
| **Related ADR** | [ADR-001](decision-register.md#adr-001-body-measurement-extraction-approach) |

**Description**: This risk is mitigated. Tier 1 image validation has been moved from Azure AI Vision 4.0 to Florence-2 on Azure AI Foundry managed endpoints, eliminating the retirement-driven migration risk for people detection and bounding box quality checks.

**Mitigations**:

- Florence-2 on Azure AI Foundry now handles Tier 1 person detection, multi-person rejection, and bounding box validation
- `IImageValidator` interface continues to abstract the underlying vision client, minimizing future model-swap effort
- Ongoing monitoring shifts to Azure AI Foundry model lifecycle and deployment guidance rather than Azure AI Vision retirement notices

**Trigger**: N/A — original Azure AI Vision deprecation exposure removed by Florence-2 adoption.

**Contingency**: Monitor Florence model catalog updates and switch between Florence-2-large and Florence-2-base, or another Foundry-hosted successor, if endpoint cost/latency or lifecycle guidance changes.

---

### R-003: GPT-5.2 Non-Deterministic Output

| Field | Value |
|-------|-------|
| **Category** | Technical |
| **Impact** | Medium |
| **Likelihood** | High |
| **Severity** | HIGH |
| **Owner** | Engineering Lead |
| **Related ADR** | [ADR-001](decision-register.md#adr-001-body-measurement-extraction-approach) |

**Description**: LLM-based measurement extraction produces different results for the same input across calls. This affects reproducibility of fit assessments and complicates testing.

**Mitigations**:

- Structured JSON output mode constrains response format
- Temperature set to 0 for maximum determinism
- Model version pinned per deployment (for example, a specific `gpt-5.2` release)
- Each assessment records the model version for audit traceability
- Snapshot testing (Verify.Xunit) captures expected output ranges, not exact values

**Trigger**: Assessment reproducibility drops below 90% (same photo + height produces different fit recommendation > 10% of calls).

**Contingency**: Introduce averaging across multiple GPT-5.2 calls (consensus mechanism) or accelerate Tier 3 custom model development.

---

### R-004: Shopper Photo Quality Variability

| Field | Value |
|-------|-------|
| **Category** | Operational |
| **Impact** | Medium |
| **Likelihood** | High |
| **Severity** | HIGH |
| **Owner** | Product Manager |
| **Related ADR** | — |

**Description**: Shoppers take photos in uncontrolled environments with varying lighting, angles, clothing, and backgrounds. SC-006 targets < 30% image rejection rate, but real-world quality may be worse.

**Mitigations**:

- Quantified image quality thresholds (bounding box ≥ 70% frame height, luminance ≥ 40/255)
- Actionable rejection feedback guides shoppers to retake photos
- SC-005 targets 90% first-attempt success rate — tracked and alerted
- Frontend can provide photo-taking guidance overlay (out of scope for backend)

**Trigger**: Image rejection rate exceeds 40% in the first 30 days of production.

**Contingency**: Relax quality thresholds with confidence penalty; provide video capture mode for frontend to extract best frame.

---

### R-005: Multi-Tenant Data Leakage

| Field | Value |
|-------|-------|
| **Category** | Security |
| **Impact** | High |
| **Likelihood** | Low |
| **Severity** | MEDIUM |
| **Owner** | Security Lead |
| **Related ADR** | [ADR-002](decision-register.md#adr-002-multi-tenant-data-isolation) |

**Description**: A bug in the repository layer or query construction could expose one tenant's data to another. This would violate data isolation guarantees and potentially breach data protection regulations.

**Mitigations**:

- Hierarchical partition keys physically isolate data per tenant in Cosmos DB
- Repository base class enforces tenant scoping on every query — compile-time constraint
- Tenant context injected from JWT claims via middleware (not user-supplied parameters)
- Integration tests validate cross-tenant query isolation
- Penetration testing includes tenant boundary testing (annually)

**Trigger**: Any cross-tenant data access detected in testing or production.

**Contingency**: Immediate incident response (Constitution Security — 4-hour triage). Audit log review for scope assessment. Potential container-per-tenant migration if pattern recurs.

---

### R-006: Azure OpenAI Service Availability and Throttling

| Field | Value |
|-------|-------|
| **Category** | Operational / Vendor |
| **Impact** | High |
| **Likelihood** | Medium |
| **Severity** | HIGH |
| **Owner** | Engineering Lead |
| **Related ADR** | [ADR-001](decision-register.md#adr-001-body-measurement-extraction-approach) |

**Description**: Azure OpenAI has per-deployment rate limits (tokens per minute / requests per minute). During peak traffic, the service may throttle requests or become temporarily unavailable. The entire measurement extraction pipeline depends on this single service.

**Mitigations**:

- Graceful degradation: VirtualMirrormentService returns fallback sizing guidance (size chart) when AI model is unavailable (FR-012)
- Circuit breaker pattern isolates Azure OpenAI failures from cascading
- Azure Service Bus queuing absorbs traffic spikes (ADR-010)
- Provisioned throughput tier selected based on capacity planning (3x peak load per Constitution IX)
- Multiple Azure OpenAI deployments across regions as failover (v2)

**Trigger**: Azure OpenAI returns 429 (throttled) or 503 for > 5% of requests in a 5-minute window.

**Contingency**: Activate queue-based async processing for all requests. If persistent, request quota increase or provision secondary deployment in alternate region.

---

### R-007: Regulatory and Compliance Exposure

| Field | Value |
|-------|-------|
| **Category** | Legal / Compliance |
| **Impact** | High |
| **Likelihood** | Medium |
| **Severity** | HIGH |
| **Owner** | Compliance Owner |
| **Related ADR** | — |

**Description**: The system processes biometric-adjacent data (body photos, derived measurements). EU AI Act, GDPR, CCPA, and evolving AI regulations may impose requirements beyond current constitution controls. Classification of body measurement extraction as "high-risk AI" under EU AI Act is possible.

**Mitigations**:

- Privacy by Design (Constitution I): photos purged < 60s, opaque shopper IDs, no PII in telemetry
- DPIA required before processing new data categories (Constitution I)
- Model card documents intended use, limitations, and biases (T104)
- AI transparency: users informed they interact with AI, shown confidence levels (FR-015)
- Regulatory monitoring: designated compliance owner tracks AI regulations (Constitution)
- SOC 2 Type II and ISO 27001 alignment planned

**Trigger**: Regulatory authority classifies body measurement extraction as high-risk AI, or a data subject complaint escalates to a DPA.

**Contingency**: Engage legal counsel for regulatory impact assessment. Implement additional controls (human-in-the-loop review, conformity assessment documentation) as required.

---

### R-008: Bias in Body Measurement Extraction

| Field | Value |
|-------|-------|
| **Category** | Ethical / AI Responsibility |
| **Impact** | High |
| **Likelihood** | Medium |
| **Severity** | HIGH |
| **Owner** | AI Ethics Lead |
| **Related ADR** | [ADR-001](decision-register.md#adr-001-body-measurement-extraction-approach) |

**Description**: GPT-5.2 Vision may perform differently across body types, skin tones, genders, and age groups. Accuracy disparity across demographic segments would violate Constitution III (AI Responsibility) and could cause reputational harm.

**Mitigations**:

- Constitution III mandates bias evaluation across body types, skin tones, genders, and age groups before deployment
- Model accuracy metrics tracked per demographic segment to detect disparity
- Model card (T104) documents known biases and limitations
- AI Ethics Review Board must approve model deployments that materially change behavior
- System must not produce body-shaming or judgmental output (Constitution III)

**Trigger**: Accuracy disparity > 10% between any two demographic segments detected during evaluation or production monitoring.

**Contingency**: Adjust prompt engineering for underperforming segments. If not resolvable via prompting, accelerate Tier 3 custom model with balanced training data.

---

### R-009: Supply Chain Vulnerability

| Field | Value |
|-------|-------|
| **Category** | Security |
| **Impact** | High |
| **Likelihood** | Low |
| **Severity** | MEDIUM |
| **Owner** | Engineering Lead |
| **Related ADR** | — |

**Description**: The .NET 8 project depends on multiple NuGet packages (Azure SDKs, xUnit, FluentAssertions, etc.). A compromised dependency or unpatched CVE could introduce vulnerabilities.

**Mitigations**:

- SBOM generated on each release via CycloneDX (T098)
- Dependencies scanned for vulnerabilities on every build (SAST/SCA in CI)
- Critical CVEs patched within 48 hours, high within 7 days (Constitution)
- Dependencies pinned to exact versions
- Container images scanned (Trivy) and signed (Notation/cosign)
- Monthly dependency update cycle with risk assessment for major upgrades

**Trigger**: Critical CVE reported in any direct dependency.

**Contingency**: Emergency patch pipeline (Constitution VIII — streamlined emergency change approval). Temporary mitigation (feature flag to disable affected path) if patch not immediately available.

---

### R-010: Peak Traffic Overwhelming Assessment Pipeline

| Field | Value |
|-------|-------|
| **Category** | Operational |
| **Impact** | Medium |
| **Likelihood** | Medium |
| **Severity** | MEDIUM |
| **Owner** | Engineering Lead |
| **Related ADR** | [ADR-010](decision-register.md#adr-010-async-queuing-under-load) |

**Description**: Events like Black Friday could generate traffic exceeding the auto-scaling capacity (10 replicas × Azure OpenAI rate limits). Even with queuing, wait times could exceed shopper patience.

**Mitigations**:

- Auto-scaling: 2–10 replicas on HTTP concurrent requests (threshold: 50)
- Service Bus queuing with HTTP 202 + estimated wait time (ADR-010)
- Capacity planning for 3x peak load (Constitution IX)
- Cached assessment results for repeat garment lookups (by-profile path avoids AI pipeline)

**Trigger**: Queue depth > 200 or estimated wait > 60 seconds sustained for > 10 minutes.

**Contingency**: Increase Container Apps max replicas. Request Azure OpenAI quota increase. Enable aggressive caching of profile-based assessments.

---

### R-011: Shopper Height Input Accuracy

| Field | Value |
|-------|-------|
| **Category** | Data Quality |
| **Impact** | Medium |
| **Likelihood** | Medium |
| **Severity** | MEDIUM |
| **Owner** | Product Manager |
| **Related ADR** | [ADR-008](decision-register.md#adr-008-mandatory-height-input) |

**Description**: Shoppers may provide inaccurate height values (wrong unit, guessing, or intentional misreporting). Since height is the absolute scale reference for all measurements, even a 5 cm error propagates proportionally to every derived measurement.

**Mitigations**:

- Input validation: 100–250 cm range rejects obviously wrong values
- Frontend can provide feet/inches converter to reduce unit confusion
- Confidence score accounts for measurement plausibility (e.g., shoulder-to-height ratio sanity check)
- v2 enhancement: cross-validate self-reported height against photo-estimated height ratio

**Trigger**: > 20% of low-confidence assessments correlate with implausible height-to-measurement ratios.

**Contingency**: Add height plausibility check in Tier 2 prompt (compare estimated proportions to reported height). Flag suspected inaccurate heights and request re-entry.

---

## Risk Summary

| Severity | Count | IDs |
|----------|-------|-----|
| CRITICAL | 1 | R-001 |
| HIGH | 6 | R-002, R-003, R-004, R-006, R-007, R-008 |
| MEDIUM | 4 | R-005, R-009, R-010, R-011 |
| LOW | 0 | — |
| **Total** | **11** | |

## Review History

| Date | Reviewer | Changes |
|------|----------|---------|
| 2026-05-13 | Initial creation | 11 risks identified from architecture and feasibility analysis |

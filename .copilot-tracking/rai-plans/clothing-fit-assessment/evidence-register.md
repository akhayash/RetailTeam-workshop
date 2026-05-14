# Evidence Register: AI Clothing Fit Assessment Agent

**Project Slug**: `clothing-fit-assessment`
**Assessment Date**: 2026-05-14

## Evidence Summary

| ID | NIST Characteristic | Evidence Type | Source | Status | Finding |
|----|-------------------|--------------|--------|--------|---------|
| E-001 | Valid and Reliable | Design document | spec.md: H1 hypothesis | Exists | GPT-5.2 accuracy ±2–4 cm is an unvalidated hypothesis; no ground-truth dataset exists |
| E-002 | Valid and Reliable | Design document | plan.md: confidence scoring | Exists | 70% low-confidence threshold defined; disclaimer and escalation path implemented |
| E-003 | Valid and Reliable | Design document | plan.md: model version tracking | Exists | Every assessment records modelVersion; audit trail in Cosmos DB |
| E-004 | Safe | Design document | constitution: Principle III | Exists | AI responsibility principle prohibits body-shaming; minor detection required |
| E-005 | Safe | Design document | spec.md: edge cases | Exists | Under-16 blocking with age-appropriate message; multi-person rejection |
| E-006 | Safe | Gap | No language sensitivity review | Missing | Fit recommendation phrasing not evaluated for psychological safety |
| E-007 | Safe | Gap | No user testing with vulnerable populations | Missing | No body-image-sensitive user research conducted |
| E-008 | Secure and Resilient | Design document | plan.md: resilience implementation | Exists | Polly pipelines, AI failover, degradation ladder (L1–L5), tenant bulkhead |
| E-009 | Secure and Resilient | Gap | No adversarial AI testing | Missing | No adversarial image testing; no prompt injection defense testing |
| E-010 | Secure and Resilient | Gap | No EXIF metadata stripping | Missing | Image metadata not stripped before AI processing |
| E-011 | Accountable and Transparent | Design document | spec.md: FR-010, FR-015 | Exists | Audit logging with model version traceability; AI disclosure to users |
| E-012 | Accountable and Transparent | Design document | data-model.md: VirtualMirrorment entity | Exists | Assessment results include correlationId, modelVersion, confidence, processingDurationMs |
| E-013 | Accountable and Transparent | Gap | No public transparency note | Missing | User declined optional artifact; no public-facing AI documentation |
| E-014 | Explainable and Interpretable | Design document | openapi.yaml: VirtualMirrormentResponse | Exists | Per-area fit scores, confidence percentage, isLowConfidence flag, disclaimer field |
| E-015 | Explainable and Interpretable | Gap | No measurement explanation | Missing | Shoppers cannot see how body measurements were derived |
| E-016 | Explainable and Interpretable | Gap | No dispute mechanism | Missing | No endpoint for shoppers to flag or correct inaccurate measurements |
| E-017 | Privacy-Enhanced | Design document | plan.md: transient blob storage | Exists | 60s TTL auto-purge; ZRS; photo never reaches long-term storage |
| E-018 | Privacy-Enhanced | Design document | spec.md: opaque shopper IDs | Exists | Frontend provides hashed shopperRef; service never resolves real identity |
| E-019 | Privacy-Enhanced | Design document | spec.md: consent + deletion | Exists | Explicit consent for profile storage; hard delete within 24h |
| E-020 | Privacy-Enhanced | Reference document | Azure OpenAI CoC: data processing | Exists | Prompts/completions not used for training; AES-256 at rest; data stays in customer geography |
| E-021 | Privacy-Enhanced | Gap | DPIA not completed | Missing | Constitution requires DPIA before processing new categories of personal data |
| E-022 | Privacy-Enhanced | Gap | Consent boundary unclear | Missing | Frontend captures consent but API cannot verify it was actually obtained |
| E-023 | Fair with Harmful Bias Managed | Design document | constitution: Principle III | Exists | Bias evaluation required before deployment; accuracy per demographic segment tracking planned |
| E-024 | Fair with Harmful Bias Managed | Gap | No bias evaluation dataset | Missing | No diverse validation dataset for demographic-segmented accuracy testing |
| E-025 | Fair with Harmful Bias Managed | Gap | No parity thresholds | Missing | No defined maximum accuracy gap across demographic segments |
| E-026 | Fair with Harmful Bias Managed | Gap | No disparate impact testing | Missing | No plan to measure whether rejection rates or accuracy vary by demographic |
| E-027 | Fair with Harmful Bias Managed | Gap | Florence-2 accessibility testing | Missing | No testing for wheelchair users, prosthetics, cultural garments |
| E-028 | Fair with Harmful Bias Managed | Gap | Tolerance band size proportionality | Missing | Default bands use absolute cm thresholds regardless of body size |

## Evidence Maturity

| NIST Characteristic | Evidence Items | Exists | Missing | Maturity |
|--------------------|---------------|--------|---------|----------|
| Valid and Reliable | 3 | 3 | 0 | Partial — design evidence only; no validation data |
| Safe | 4 | 2 | 2 | Partial — constitutional controls; no user testing |
| Secure and Resilient | 3 | 1 | 2 | Partial — strong resilience; adversarial testing absent |
| Accountable and Transparent | 3 | 2 | 1 | Mostly — audit trail strong; public transparency missing |
| Explainable and Interpretable | 3 | 1 | 2 | Weak — outputs interpretable; process opaque |
| Privacy-Enhanced | 6 | 4 | 2 | Mostly — strong architecture; DPIA and consent gaps |
| Fair with Harmful Bias Managed | 6 | 1 | 5 | Weak — acknowledged but not operationalized |
| **Total** | **28** | **14** | **14** | **50% evidence coverage** |

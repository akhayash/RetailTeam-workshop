# Control Surface Catalog: AI Clothing Fit Assessment Agent

**Project Slug**: `clothing-fit-assessment`
**Assessment Date**: 2026-05-14
**Threats Cataloged**: 14 (T-RAI-001 through T-RAI-014)

## Control Surface Summary

| RAI ID | Threat | Concern | Existing Controls | Control Adequacy | Gap Summary |
|--------|--------|---------|------------------|-----------------|-------------|
| T-RAI-001 | Demographic accuracy disparity | High | Confidence scoring; model version tracking | Inadequate | No demographic-segmented benchmarking, no parity thresholds, no diverse validation dataset |
| T-RAI-002 | Adversarial image manipulation | Moderate | Content Safety filtering; input validation (format, size, MIME) | Partial | No EXIF stripping; no adversarial image detection; no measurement anomaly detection |
| T-RAI-003 | Prompt injection via image metadata | High | Content Safety pre-screening; structured output schema | Inadequate | No metadata stripping before AI processing; no prompt injection defense in extraction prompt |
| T-RAI-004 | Model inversion / measurement leakage | Moderate | Rate limiting per tenant; stateless model; tenant data isolation | Partial | No per-shopperRef rate limiting; no differential privacy analysis |
| T-RAI-005 | Body-image harm via fit language | High | Constitution prohibits body-shaming; fit uses 5-point scale | Inadequate | No language sensitivity review; no user testing with body-image-sensitive populations; no neutral mode option |
| T-RAI-006 | Unattributable recommendation errors | Low | Immutable audit logs; model version + correlationId per assessment | Adequate | Existing controls sufficient |
| T-RAI-007 | Tolerance band bias across body sizes | High | Configurable tolerance bands per tenant + garment category | Partial | Default bands use absolute thresholds not proportional to body size; no size-proportional validation |
| T-RAI-008 | Photo retention beyond 60s TTL | Moderate | Blob lifecycle policy; 60s TTL auto-purge | Partial | No automated purge verification; no alerting on overage; no compliance audit procedure |
| T-RAI-009 | AI accuracy degradation under load | Moderate | Polly resilience pipelines; circuit breaker; degradation ladder | Partial | No per-request accuracy monitoring; no load-dependent quality regression alerts |
| T-RAI-010 | Non-deterministic output variance | Moderate | Structured output schema enforcement | Partial | Temperature setting not specified; no measurement caching; no variance monitoring |
| T-RAI-011 | Opaque measurement extraction | High | Per-area fit scores; confidence percentage | Inadequate | No measurement explanation; no dispute mechanism; no body landmark visualization |
| T-RAI-012 | Florence-2 detection bias | High | Multi-person rejection; bounding box quality check | Inadequate | No accessibility testing; no alternative validation paths; no rejection rate monitoring per demographic |
| T-RAI-013 | Minor boundary exploitation | Moderate | Content Safety minor detection; under-16 blocking | Partial | No conservative threshold tuning; no near-boundary handling protocol |
| T-RAI-014 | Consent provenance gaps | Moderate | saveProfile flag; consentGrantedAt timestamp; DPA obligations | Partial | No consent verification mechanism; consent metadata from frontend is trusted without validation |

## Adequacy Distribution

| Adequacy Level | Count | Threats |
|---------------|-------|---------|
| Adequate | 1 | T-RAI-006 |
| Partial | 8 | T-RAI-002, T-RAI-004, T-RAI-007, T-RAI-008, T-RAI-009, T-RAI-010, T-RAI-013, T-RAI-014 |
| Inadequate | 5 | T-RAI-001, T-RAI-003, T-RAI-005, T-RAI-011, T-RAI-012 |

## Priority Gap Actions

### Critical (Inadequate controls for High Concern threats)

| RAI ID | Gap | Recommended Action | Effort |
|--------|-----|-------------------|--------|
| T-RAI-001 | No demographic accuracy benchmarking | Create diverse validation dataset; define parity thresholds (e.g., max 1cm accuracy gap across segments); implement per-segment monitoring | Large |
| T-RAI-003 | No image metadata stripping | Strip all EXIF/IPTC/XMP metadata before sending to GPT-5.2; add prompt injection detection in pre-processing | Small |
| T-RAI-005 | No language sensitivity review | Conduct language review with body-image experts; user-test fit phrasing; implement neutral measurement-only response mode | Medium |
| T-RAI-011 | No measurement explanation or dispute mechanism | Add measurement breakdown annotations to response; implement dispute endpoint allowing shoppers to flag inaccurate measurements | Medium |
| T-RAI-012 | No accessibility testing for Florence-2 | Test Florence-2 detection across wheelchair users, prosthetics, cultural garments; define alternative validation paths for failed detection | Medium |

### Important (Partial controls for High or Moderate Concern threats)

| RAI ID | Gap | Recommended Action | Effort |
|--------|-----|-------------------|--------|
| T-RAI-007 | Absolute tolerance bands regardless of body size | Implement size-proportional tolerance calculation; validate against diverse body size data | Medium |
| T-RAI-002 | No EXIF stripping or adversarial detection | Combine with T-RAI-003 metadata stripping; add measurement distribution anomaly detection | Small |
| T-RAI-008 | No purge verification | Implement automated blob age check; alert on photos > 60s; quarterly compliance audit | Small |
| T-RAI-009 | No load-dependent accuracy monitoring | Add per-request confidence trending; alert when average confidence drops under load | Small |
| T-RAI-010 | Temperature not configured; no variance monitoring | Set temperature=0 for GPT-5.2; implement measurement variance tracking across repeat assessments | Small |
| T-RAI-013 | No conservative age threshold | Tune Content Safety age detection to conservative threshold (block 15–17 range); implement near-boundary audit log | Small |
| T-RAI-014 | No consent verification | Define consent receipt specification; add validation of consentGrantedAt recency; document in DPA | Small |

# RAI Backlog Items — GitHub Issue Format

**Project Slug**: `clothing-fit-assessment`
**Generated**: 2026-05-14
**Autonomy Tier**: Partial (draft for human review)

---

## {{RAI-TEMP-1}}: [RAI-FairBiasManaged] Demographic accuracy benchmarking dataset and parity thresholds

```yaml
---
rai_characteristic: Fair with Harmful Bias Managed
threat_id: T-RAI-001
suggested_priority: Immediate
suggested_horizon: Pre-Production
category: Remediation
depth_tier: Comprehensive
security_cross_ref:
---
```

**Labels**: `fair-bias-managed`, `rai`
**Milestone**: Pre-Production

## RAI Control: Demographic Accuracy Parity

**NIST Characteristic:** Fair with Harmful Bias Managed (MS-2.11)
**Threat:** T-RAI-001 - Demographic accuracy disparity across body types, skin tones, and cultural dress
**Control Surface:** Prevent - Bias testing with balanced validation data and algorithmic audits
**Suggested Priority:** Immediate
**Suggested Remediation Horizon:** Pre-Production

### Implementation

Create a diverse validation dataset covering body types (XS-5XL+), skin tones, gender presentations, cultural garments, and accessibility aids. Define maximum acceptable accuracy gap across demographic segments (suggested: ≤1 cm). Implement per-segment accuracy monitoring. Run baseline accuracy evaluation before production launch.

### Acceptance Criteria

* [ ] Validation dataset contains ≥500 images spanning defined demographic segments
* [ ] Parity threshold defined and documented (max accuracy gap across segments)
* [ ] Baseline accuracy report generated per demographic segment
* [ ] Monitoring dashboard displays per-segment accuracy metrics

> **Note** — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.
> - [ ] Reviewed and validated by a qualified human reviewer

---

## {{RAI-TEMP-2}}: [RAI-SecureResilient] Strip image metadata before AI processing

```yaml
---
rai_characteristic: Secure and Resilient
threat_id: T-RAI-003
suggested_priority: Immediate
suggested_horizon: Pre-Production
category: Control Implementation
depth_tier: Comprehensive
security_cross_ref:
---
```

**Labels**: `secure-resilient`, `rai`
**Milestone**: Pre-Production

## RAI Control: Image Metadata Stripping

**NIST Characteristic:** Secure and Resilient (MS-2.7)
**Threat:** T-RAI-003 - Prompt injection via EXIF/IPTC/XMP metadata
**Control Surface:** Prevent - Data sanitization before AI model ingestion
**Suggested Priority:** Immediate
**Suggested Remediation Horizon:** Pre-Production

### Implementation

Add image pre-processing step that strips all EXIF, IPTC, and XMP metadata before sending photos to GPT-5.2 Vision. Retain only raw pixel data and dimensions. Log metadata presence for threat detection.

### Acceptance Criteria

* [ ] All uploaded photos have EXIF/IPTC/XMP metadata stripped before AI processing
* [ ] Metadata stripping occurs before Content Safety and GPT-5.2 Vision calls
* [ ] Metadata presence is logged for anomaly detection
* [ ] Unit tests confirm metadata removal for common image formats (JPEG, PNG, HEIC, WebP)

> **Note** — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.
> - [ ] Reviewed and validated by a qualified human reviewer

---

## {{RAI-TEMP-3}}: [RAI-Safe] Fit language sensitivity review and neutral response mode

```yaml
---
rai_characteristic: Safe
threat_id: T-RAI-005
suggested_priority: Immediate
suggested_horizon: Pre-Production
category: Remediation
depth_tier: Comprehensive
security_cross_ref:
---
```

**Labels**: `safe`, `rai`
**Milestone**: Pre-Production

## RAI Control: Body-Image Safe Language

**NIST Characteristic:** Safe (MS-2.6)
**Threat:** T-RAI-005 - Body-image harm via fit recommendation language
**Control Surface:** Prevent - Safety boundary enforcement through language review
**Suggested Priority:** Immediate
**Suggested Remediation Horizon:** Pre-Production

### Implementation

Engage body-image experts to review all fit recommendation phrasing. Conduct user testing with body-image-sensitive populations. Implement a neutral measurement-only response mode. Define a prohibited language list for the GPT-5.2 system prompt.

### Acceptance Criteria

* [ ] Language sensitivity review completed by qualified expert
* [ ] User testing conducted with ≥10 participants from vulnerable populations
* [ ] Neutral measurement-only response mode available via API parameter
* [ ] Prohibited language list enforced in GPT-5.2 system prompt

> **Note** — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.
> - [ ] Reviewed and validated by a qualified human reviewer

---

## {{RAI-TEMP-4}}: [RAI-ExplainableInterpretable] Measurement explanation annotations and dispute mechanism

```yaml
---
rai_characteristic: Explainable and Interpretable
threat_id: T-RAI-011
suggested_priority: Near-term
suggested_horizon: Pre-Production
category: Control Implementation
depth_tier: Comprehensive
security_cross_ref:
---
```

**Labels**: `explainable-interpretable`, `rai`
**Milestone**: Pre-Production

## RAI Control: Measurement Explainability

**NIST Characteristic:** Explainable and Interpretable (MS-2.9)
**Threat:** T-RAI-011 - Opaque measurement extraction process
**Control Surface:** Prevent - Explanation interfaces for measurement derivation
**Suggested Priority:** Near-term
**Suggested Remediation Horizon:** Pre-Production

### Implementation

Add per-body-area measurement breakdown annotations to the assessment response. Implement a dispute endpoint allowing shoppers to flag inaccurate measurements. Track dispute volume and patterns for model improvement.

### Acceptance Criteria

* [ ] Assessment response includes per-area measurement breakdown with confidence per area
* [ ] Dispute endpoint accepts shopper feedback on measurement accuracy
* [ ] Dispute volume tracked and reported in monitoring dashboard
* [ ] Dispute patterns feed into accuracy improvement backlog

> **Note** — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.
> - [ ] Reviewed and validated by a qualified human reviewer

---

## {{RAI-TEMP-5}}: [RAI-FairBiasManaged] Florence-2 accessibility and demographic detection testing

```yaml
---
rai_characteristic: Fair with Harmful Bias Managed
threat_id: T-RAI-012
suggested_priority: Immediate
suggested_horizon: Pre-Production
category: Remediation
depth_tier: Comprehensive
security_cross_ref:
---
```

**Labels**: `fair-bias-managed`, `rai`
**Milestone**: Pre-Production

## RAI Control: Detection Bias Evaluation

**NIST Characteristic:** Fair with Harmful Bias Managed (MS-2.11)
**Threat:** T-RAI-012 - Florence-2 detection bias for wheelchair users, prosthetics, cultural garments
**Control Surface:** Prevent - Bias testing with diverse inputs
**Suggested Priority:** Immediate
**Suggested Remediation Horizon:** Pre-Production

### Implementation

Test Florence-2 person detection across wheelchair users, prosthetics, cultural garments, and diverse body presentations. Define alternative validation paths when detection fails. Monitor rejection rates per demographic segment.

### Acceptance Criteria

* [ ] Florence-2 tested against ≥50 images per accessibility/demographic category
* [ ] Detection success rate documented per category
* [ ] Alternative validation path defined for failed detections
* [ ] Rejection rate monitoring deployed with demographic segmentation

> **Note** — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.
> - [ ] Reviewed and validated by a qualified human reviewer

---

## {{RAI-TEMP-6}}: [RAI-PrivacyEnhanced] Complete Data Protection Impact Assessment

```yaml
---
rai_characteristic: Privacy-Enhanced
threat_id: T-RAI-008
suggested_priority: Immediate
suggested_horizon: Pre-Production
category: Remediation
depth_tier: Comprehensive
security_cross_ref:
---
```

**Labels**: `privacy-enhanced`, `rai`
**Milestone**: Pre-Production

## RAI Control: DPIA Completion

**NIST Characteristic:** Privacy-Enhanced (MS-2.10)
**Threat:** T-RAI-008 - Photo retention and T-RAI-014 - Consent provenance gaps
**Control Surface:** Prevent - Privacy impact assessment
**Suggested Priority:** Immediate
**Suggested Remediation Horizon:** Pre-Production

### Implementation

Complete DPIA covering: photo processing (body images), measurement extraction (body dimensions), profile storage (size history), and consent workflows. Assess lawful basis under GDPR Art. 6 and Art. 9. Document data flows, retention periods, and rights fulfillment mechanisms.

### Acceptance Criteria

* [ ] DPIA document completed covering all data processing activities
* [ ] Lawful basis determined for body image and measurement processing
* [ ] DPIA reviewed by data protection officer or legal counsel
* [ ] Remediation actions from DPIA tracked in backlog

> **Note** — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.
> - [ ] Reviewed and validated by a qualified human reviewer

---

## {{RAI-TEMP-7}}: [RAI-PrivacyEnhanced] Consent verification mechanism

```yaml
---
rai_characteristic: Privacy-Enhanced
threat_id: T-RAI-014
suggested_priority: Near-term
suggested_horizon: Pre-Production
category: Control Implementation
depth_tier: Comprehensive
security_cross_ref:
---
```

**Labels**: `privacy-enhanced`, `rai`
**Milestone**: Pre-Production

## RAI Control: Consent Integrity Verification

**NIST Characteristic:** Privacy-Enhanced (MS-2.10)
**Threat:** T-RAI-014 - Consent provenance gaps
**Control Surface:** Prevent - Consent management and verification
**Suggested Priority:** Near-term
**Suggested Remediation Horizon:** Pre-Production

### Implementation

Define consent receipt specification. Add server-side validation of consentGrantedAt recency. Document consent requirements in DPA. Consider consent receipt token signed by frontend SDK.

### Acceptance Criteria

* [ ] Consent receipt specification documented
* [ ] Server-side validation rejects stale consent timestamps
* [ ] DPA updated with consent verification requirements
* [ ] API rejects requests with missing or invalid consent metadata

> **Note** — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.
> - [ ] Reviewed and validated by a qualified human reviewer

---

## {{RAI-TEMP-8}}: [RAI-FairBiasManaged] Size-proportional tolerance band validation

```yaml
---
rai_characteristic: Fair with Harmful Bias Managed
threat_id: T-RAI-007
suggested_priority: Near-term
suggested_horizon: Pre-Production
category: Control Implementation
depth_tier: Comprehensive
security_cross_ref:
---
```

**Labels**: `fair-bias-managed`, `rai`
**Milestone**: Pre-Production

## RAI Control: Proportional Tolerance Bands

**NIST Characteristic:** Fair with Harmful Bias Managed (MS-2.11)
**Threat:** T-RAI-007 - Tolerance band bias across body sizes
**Control Surface:** Prevent - Bias testing with proportional thresholds
**Suggested Priority:** Near-term
**Suggested Remediation Horizon:** Pre-Production

### Implementation

Replace absolute cm tolerance thresholds with size-proportional calculations. Validate updated bands against diverse body size data. Document the proportional algorithm and test edge cases.

### Acceptance Criteria

* [ ] Tolerance bands use proportional calculation relative to body measurements
* [ ] Validated against body sizes XS through 5XL+
* [ ] Proportional algorithm documented and reviewed
* [ ] No statistically significant fit recommendation bias across size groups

> **Note** — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.
> - [ ] Reviewed and validated by a qualified human reviewer

---

## {{RAI-TEMP-9}}: [RAI-SecureResilient] Adversarial image detection and measurement anomaly alerting

```yaml
---
rai_characteristic: Secure and Resilient
threat_id: T-RAI-002
suggested_priority: Near-term
suggested_horizon: Pre-Production
category: Control Implementation
depth_tier: Comprehensive
security_cross_ref:
---
```

**Labels**: `secure-resilient`, `rai`
**Milestone**: Pre-Production

## RAI Control: Adversarial Input Detection

**NIST Characteristic:** Secure and Resilient (MS-2.7)
**Threat:** T-RAI-002 - Adversarial image manipulation
**Control Surface:** Detect - Anomaly monitoring for adversarial inputs
**Suggested Priority:** Near-term
**Suggested Remediation Horizon:** Pre-Production

### Implementation

Add measurement distribution anomaly detection. Implement EXIF stripping (shared with {{RAI-TEMP-2}}). Add adversarial input monitoring alerts when outputs fall outside physiologically plausible ranges.

### Acceptance Criteria

* [ ] Measurement anomaly detection flags outputs outside plausible ranges
* [ ] Alerting configured for anomalous measurement patterns
* [ ] Anomaly detection tested against known adversarial image techniques

> **Note** — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.
> - [ ] Reviewed and validated by a qualified human reviewer

---

## {{RAI-TEMP-10}}: [RAI-FairBiasManaged] Disparate impact testing methodology

```yaml
---
rai_characteristic: Fair with Harmful Bias Managed
threat_id: T-RAI-001
suggested_priority: Near-term
suggested_horizon: Pre-Production
category: Remediation
depth_tier: Comprehensive
security_cross_ref:
---
```

**Labels**: `fair-bias-managed`, `rai`
**Milestone**: Pre-Production

## RAI Control: Disparate Impact Measurement

**NIST Characteristic:** Fair with Harmful Bias Managed (MS-2.11)
**Threat:** T-RAI-001 - Demographic accuracy disparity
**Control Surface:** Detect - Demographic parity monitoring
**Suggested Priority:** Near-term
**Suggested Remediation Horizon:** Pre-Production

### Implementation

Define disparate impact testing methodology covering rejection rates, accuracy, and confidence scores across demographic segments. Implement automated reporting. Set alert thresholds for statistically significant disparities.

### Acceptance Criteria

* [ ] Disparate impact methodology documented and reviewed
* [ ] Automated reporting for rejection rate, accuracy, and confidence by segment
* [ ] Alert thresholds defined for statistically significant disparities
* [ ] Baseline report generated before production launch

> **Note** — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.
> - [ ] Reviewed and validated by a qualified human reviewer

---

## {{RAI-TEMP-11}}: [RAI-PrivacyEnhanced] Photo purge verification and compliance audit

```yaml
---
rai_characteristic: Privacy-Enhanced
threat_id: T-RAI-008
suggested_priority: Planned
suggested_horizon: Early Operations
category: Monitoring Setup
depth_tier: Comprehensive
security_cross_ref:
---
```

**Labels**: `privacy-enhanced`, `rai`
**Milestone**: Early Operations

## RAI Control: Photo Purge Verification

**NIST Characteristic:** Privacy-Enhanced (MS-2.10)
**Threat:** T-RAI-008 - Photo retention beyond 60s TTL
**Control Surface:** Detect - Data leakage detection
**Suggested Priority:** Planned
**Suggested Remediation Horizon:** Early Operations

### Implementation

Implement automated blob age check that alerts on photos exceeding 60s TTL. Add quarterly compliance audit procedure. Create operational runbook for TTL violation incidents.

### Acceptance Criteria

* [ ] Automated alert fires when any blob exceeds 60s age
* [ ] Quarterly compliance audit procedure documented
* [ ] Operational runbook for TTL violations created

> **Note** — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.
> - [ ] Reviewed and validated by a qualified human reviewer

---

## {{RAI-TEMP-12}}: [RAI-ValidReliable] Load-dependent accuracy monitoring and alerting

```yaml
---
rai_characteristic: Valid and Reliable
threat_id: T-RAI-009
suggested_priority: Planned
suggested_horizon: Early Operations
category: Monitoring Setup
depth_tier: Comprehensive
security_cross_ref:
---
```

**Labels**: `valid-reliable`, `rai`
**Milestone**: Early Operations

## RAI Control: Load-Quality Regression Detection

**NIST Characteristic:** Valid and Reliable (MS-2.5)
**Threat:** T-RAI-009 - AI accuracy degradation under load
**Control Surface:** Detect - Performance degradation alerts
**Suggested Priority:** Planned
**Suggested Remediation Horizon:** Early Operations

### Implementation

Add per-request confidence trending that correlates with system load. Alert when average confidence drops below threshold during high-traffic periods.

### Acceptance Criteria

* [ ] Confidence trending correlated with request volume
* [ ] Alert configured for confidence drops during high load
* [ ] Dashboard displays load-accuracy correlation

> **Note** — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.
> - [ ] Reviewed and validated by a qualified human reviewer

---

## {{RAI-TEMP-13}}: [RAI-ValidReliable] GPT-5.2 temperature pinning and output variance monitoring

```yaml
---
rai_characteristic: Valid and Reliable
threat_id: T-RAI-010
suggested_priority: Planned
suggested_horizon: Early Operations
category: Control Implementation
depth_tier: Comprehensive
security_cross_ref:
---
```

**Labels**: `valid-reliable`, `rai`
**Milestone**: Early Operations

## RAI Control: Non-Deterministic Output Control

**NIST Characteristic:** Valid and Reliable (MS-2.5)
**Threat:** T-RAI-010 - Non-deterministic output variance
**Control Surface:** Prevent - Failsafe defaults; Detect - Variance monitoring
**Suggested Priority:** Planned
**Suggested Remediation Horizon:** Early Operations

### Implementation

Set temperature=0 for GPT-5.2 measurement extraction calls. Implement measurement variance tracking across repeat assessments. Alert on variance exceeding threshold.

### Acceptance Criteria

* [ ] Temperature=0 configured for all measurement extraction calls
* [ ] Variance tracking implemented for repeat assessments
* [ ] Alert threshold defined and tested

> **Note** — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.
> - [ ] Reviewed and validated by a qualified human reviewer

---

## {{RAI-TEMP-14}}: [RAI-Safe] Conservative minor detection threshold tuning

```yaml
---
rai_characteristic: Safe
threat_id: T-RAI-013
suggested_priority: Planned
suggested_horizon: Early Operations
category: Control Implementation
depth_tier: Comprehensive
security_cross_ref:
---
```

**Labels**: `safe`, `rai`
**Milestone**: Early Operations

## RAI Control: Minor Boundary Safety

**NIST Characteristic:** Safe (MS-2.6)
**Threat:** T-RAI-013 - Minor boundary exploitation
**Control Surface:** Prevent - Safety boundary enforcement
**Suggested Priority:** Planned
**Suggested Remediation Horizon:** Early Operations

### Implementation

Tune Content Safety age detection to block the 15-17 range conservatively. Implement near-boundary audit logging for ages estimated 14-18.

### Acceptance Criteria

* [ ] Conservative age threshold blocks estimated 15-17 age range
* [ ] Near-boundary (14-18) audit logging implemented
* [ ] Escalation protocol documented for edge cases

> **Note** — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.
> - [ ] Reviewed and validated by a qualified human reviewer

---

## {{RAI-TEMP-15}}: [RAI-AccountableTransparent] Public transparency note and model card

```yaml
---
rai_characteristic: Accountable and Transparent
threat_id:
suggested_priority: Backlog
suggested_horizon: Ongoing Governance
category: Documentation
depth_tier: Comprehensive
security_cross_ref:
---
```

**Labels**: `accountable-transparent`, `rai`
**Milestone**: Ongoing Governance

## RAI Control: Public AI Documentation

**NIST Characteristic:** Accountable and Transparent (MS-2.8)
**Threat:** N/A — documentation gap
**Control Surface:** Prevent - Model cards and decision audit trails
**Suggested Priority:** Backlog
**Suggested Remediation Horizon:** Ongoing Governance

### Implementation

Create a public-facing transparency note covering what the AI does, how it works, known limitations, accuracy bounds, and how to report concerns. Publish model card documenting accuracy per garment category and known biases.

### Acceptance Criteria

* [ ] Transparency note published and accessible to shoppers
* [ ] Model card documents accuracy bounds and known limitations
* [ ] Report-a-concern mechanism linked from transparency note

> **Note** — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.
> - [ ] Reviewed and validated by a qualified human reviewer

---

## {{RAI-TEMP-16}}: [RAI-ExplainableInterpretable] SMPL model roadmap for v2 explainability

```yaml
---
rai_characteristic: Explainable and Interpretable
threat_id: T-RAI-011
suggested_priority: Backlog
suggested_horizon: Ongoing Governance
category: Enhancement
depth_tier: Comprehensive
security_cross_ref:
---
```

**Labels**: `explainable-interpretable`, `rai`, `tradeoff`
**Milestone**: Ongoing Governance

## RAI Control: Explainable Measurement Extraction

**NIST Characteristic:** Explainable and Interpretable (MS-2.9)
**Threat:** T-RAI-011 - Opaque measurement extraction
**Control Surface:** Prevent - Interpretable model selection
**Suggested Priority:** Backlog
**Suggested Remediation Horizon:** Ongoing Governance

### Implementation

Evaluate SMPL model as alternative or complement to GPT-5.2 for body measurement extraction. Create technical feasibility assessment and v2 roadmap.

### Acceptance Criteria

* [ ] SMPL model feasibility assessment completed
* [ ] Accuracy comparison: SMPL vs GPT-5.2 documented
* [ ] V2 roadmap with explainability milestones defined

> **Note** — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.
> - [ ] Reviewed and validated by a qualified human reviewer

---

## {{RAI-TEMP-17}}: [RAI-AccountableTransparent] Azure OpenAI CoC biometric boundary legal review

```yaml
---
rai_characteristic: Accountable and Transparent
threat_id:
suggested_priority: Planned
suggested_horizon: Ongoing Governance
category: Documentation
depth_tier: Comprehensive
security_cross_ref:
---
```

**Labels**: `accountable-transparent`, `rai`
**Milestone**: Ongoing Governance

## RAI Control: CoC Compliance Verification

**NIST Characteristic:** Accountable and Transparent (MS-2.8)
**Threat:** N/A — regulatory compliance gap
**Control Surface:** Prevent - Compliance monitoring
**Suggested Priority:** Planned
**Suggested Remediation Horizon:** Ongoing Governance

### Implementation

Engage legal counsel to review whether functional body measurement extraction for clothing fit constitutes "biometric categorization" under Azure OpenAI CoC restriction #10. Document the legal opinion.

### Acceptance Criteria

* [ ] Legal opinion obtained on biometric vs. functional measurement boundary
* [ ] Opinion documented and accessible to engineering and compliance teams
* [ ] Any required usage modifications implemented

> **Note** — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.
> - [ ] Reviewed and validated by a qualified human reviewer

---

## {{RAI-TEMP-18}}: [RAI-AccountableTransparent] Appropriate reliance framing in API responses

```yaml
---
rai_characteristic: Accountable and Transparent
threat_id:
suggested_priority: Backlog
suggested_horizon: Ongoing Governance
category: Enhancement
depth_tier: Comprehensive
security_cross_ref:
---
```

**Labels**: `accountable-transparent`, `rai`, `tradeoff`
**Milestone**: Ongoing Governance

## RAI Control: Trust Calibration Messaging

**NIST Characteristic:** Accountable and Transparent (MS-2.8)
**Threat:** N/A — appropriate reliance gap
**Control Surface:** Prevent - Decision documentation
**Suggested Priority:** Backlog
**Suggested Remediation Horizon:** Ongoing Governance

### Implementation

Add contextual framing to API response or frontend SDK guidance: "This recommendation is based on AI measurement extraction and may not be exact. We suggest also checking the size chart for this brand."

### Acceptance Criteria

* [ ] Contextual framing text included in API response or SDK documentation
* [ ] Guidance documented for frontend teams on presenting confidence information
* [ ] Size chart cross-reference suggested alongside AI recommendation

> **Note** — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.
> - [ ] Reviewed and validated by a qualified human reviewer

# RAI Backlog Items — ADO Format

**Project Slug**: `clothing-fit-assessment`
**Generated**: 2026-05-14
**Autonomy Tier**: Partial (draft for human review)

---

## WI-RAI-001: [RAI] Demographic accuracy benchmarking dataset and parity thresholds

<div>
  <h3>RAI Control: Demographic Accuracy Parity</h3>
  <p><strong>NIST Characteristic:</strong> Fair with Harmful Bias Managed (MS-2.11)</p>
  <p><strong>Threat:</strong> T-RAI-001 - Demographic accuracy disparity across body types, skin tones, and cultural dress</p>
  <p><strong>Control Surface:</strong> Prevent - Bias testing with balanced validation data and algorithmic audits</p>
  <p><strong>Evidence:</strong> Gap — no validation dataset or parity thresholds exist</p>
  <p><strong>Suggested Remediation Horizon:</strong> Pre-Production</p>
  <h4>Implementation</h4>
  <p>Create a diverse validation dataset covering body types (XS-5XL+), skin tones, gender presentations, cultural garments, and accessibility aids. Define maximum acceptable accuracy gap across demographic segments (suggested: ≤1 cm). Implement per-segment accuracy monitoring. Run baseline accuracy evaluation before production launch.</p>
  <h4>Acceptance Criteria</h4>
  <ul>
    <li>Validation dataset contains ≥500 images spanning defined demographic segments</li>
    <li>Parity threshold defined and documented (max accuracy gap across segments)</li>
    <li>Baseline accuracy report generated per demographic segment</li>
    <li>Monitoring dashboard displays per-segment accuracy metrics</li>
  </ul>
  <blockquote>
  <p><strong>Note</strong> — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.</p>
  <ul><li><input type="checkbox" disabled /> Reviewed and validated by a qualified human reviewer</li></ul>
  </blockquote>
</div>

**Type**: User Story
**Priority**: Immediate
**Tags**: `rai:fair-bias-managed`
**RAI Owner**: TBD — assign during backlog refinement

---

## WI-RAI-002: [RAI] Strip image metadata before AI processing

<div>
  <h3>RAI Control: Image Metadata Stripping</h3>
  <p><strong>NIST Characteristic:</strong> Secure and Resilient (MS-2.7)</p>
  <p><strong>Threat:</strong> T-RAI-003 - Prompt injection via EXIF/IPTC/XMP metadata embedded in uploaded photos</p>
  <p><strong>Control Surface:</strong> Prevent - Data sanitization before AI model ingestion</p>
  <p><strong>Evidence:</strong> Gap — no metadata stripping implemented</p>
  <p><strong>Suggested Remediation Horizon:</strong> Pre-Production</p>
  <h4>Implementation</h4>
  <p>Add image pre-processing step in the assessment pipeline that strips all EXIF, IPTC, and XMP metadata before sending photos to GPT-5.2 Vision. Retain only raw pixel data and dimensions. Log metadata presence for threat detection.</p>
  <h4>Acceptance Criteria</h4>
  <ul>
    <li>All uploaded photos have EXIF/IPTC/XMP metadata stripped before AI processing</li>
    <li>Metadata stripping occurs before Content Safety and GPT-5.2 Vision calls</li>
    <li>Metadata presence is logged for anomaly detection</li>
    <li>Unit tests confirm metadata removal for common image formats (JPEG, PNG, HEIC, WebP)</li>
  </ul>
  <blockquote>
  <p><strong>Note</strong> — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.</p>
  <ul><li><input type="checkbox" disabled /> Reviewed and validated by a qualified human reviewer</li></ul>
  </blockquote>
</div>

**Type**: Task
**Priority**: Immediate
**Tags**: `rai:secure-resilient`
**RAI Owner**: TBD — assign during backlog refinement

---

## WI-RAI-003: [RAI] Fit language sensitivity review and neutral response mode

<div>
  <h3>RAI Control: Body-Image Safe Language</h3>
  <p><strong>NIST Characteristic:</strong> Safe (MS-2.6)</p>
  <p><strong>Threat:</strong> T-RAI-005 - Body-image harm via fit recommendation language</p>
  <p><strong>Control Surface:</strong> Prevent - Safety boundary enforcement through language review</p>
  <p><strong>Evidence:</strong> Gap — no language sensitivity review conducted</p>
  <p><strong>Suggested Remediation Horizon:</strong> Pre-Production</p>
  <h4>Implementation</h4>
  <p>Engage body-image experts to review all fit recommendation phrasing. Conduct user testing with body-image-sensitive populations. Implement a neutral measurement-only response mode as an alternative to descriptive fit language. Define a prohibited language list for the GPT-5.2 system prompt.</p>
  <h4>Acceptance Criteria</h4>
  <ul>
    <li>Language sensitivity review completed by qualified expert</li>
    <li>User testing conducted with ≥10 participants from vulnerable populations</li>
    <li>Neutral measurement-only response mode available via API parameter</li>
    <li>Prohibited language list enforced in GPT-5.2 system prompt</li>
  </ul>
  <blockquote>
  <p><strong>Note</strong> — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.</p>
  <ul><li><input type="checkbox" disabled /> Reviewed and validated by a qualified human reviewer</li></ul>
  </blockquote>
</div>

**Type**: User Story
**Priority**: Immediate
**Tags**: `rai:safe`
**RAI Owner**: TBD — assign during backlog refinement

---

## WI-RAI-004: [RAI] Measurement explanation annotations and dispute mechanism

<div>
  <h3>RAI Control: Measurement Explainability</h3>
  <p><strong>NIST Characteristic:</strong> Explainable and Interpretable (MS-2.9)</p>
  <p><strong>Threat:</strong> T-RAI-011 - Opaque measurement extraction process</p>
  <p><strong>Control Surface:</strong> Prevent - Explanation interfaces for measurement derivation</p>
  <p><strong>Evidence:</strong> Gap — no measurement explanation or dispute mechanism</p>
  <p><strong>Suggested Remediation Horizon:</strong> Pre-Production</p>
  <h4>Implementation</h4>
  <p>Add per-body-area measurement breakdown annotations to the assessment response. Implement a dispute endpoint allowing shoppers to flag inaccurate measurements with optional corrected values. Track dispute volume and patterns for model improvement.</p>
  <h4>Acceptance Criteria</h4>
  <ul>
    <li>Assessment response includes per-area measurement breakdown with confidence per area</li>
    <li>Dispute endpoint accepts shopper feedback on measurement accuracy</li>
    <li>Dispute volume tracked and reported in monitoring dashboard</li>
    <li>Dispute patterns feed into accuracy improvement backlog</li>
  </ul>
  <blockquote>
  <p><strong>Note</strong> — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.</p>
  <ul><li><input type="checkbox" disabled /> Reviewed and validated by a qualified human reviewer</li></ul>
  </blockquote>
</div>

**Type**: User Story
**Priority**: Near-term
**Tags**: `rai:explainable-interpretable`
**RAI Owner**: TBD — assign during backlog refinement

---

## WI-RAI-005: [RAI] Florence-2 accessibility and demographic detection testing

<div>
  <h3>RAI Control: Detection Bias Evaluation</h3>
  <p><strong>NIST Characteristic:</strong> Fair with Harmful Bias Managed (MS-2.11)</p>
  <p><strong>Threat:</strong> T-RAI-012 - Florence-2 detection bias for wheelchair users, prosthetics, cultural garments</p>
  <p><strong>Control Surface:</strong> Prevent - Bias testing with diverse inputs</p>
  <p><strong>Evidence:</strong> Gap — no accessibility or demographic detection testing</p>
  <p><strong>Suggested Remediation Horizon:</strong> Pre-Production</p>
  <h4>Implementation</h4>
  <p>Test Florence-2 person detection across wheelchair users, prosthetics, cultural garments, and diverse body presentations. Define alternative validation paths when detection fails. Monitor rejection rates per demographic segment.</p>
  <h4>Acceptance Criteria</h4>
  <ul>
    <li>Florence-2 tested against ≥50 images per accessibility/demographic category</li>
    <li>Detection success rate documented per category</li>
    <li>Alternative validation path defined for failed detections</li>
    <li>Rejection rate monitoring deployed with demographic segmentation</li>
  </ul>
  <blockquote>
  <p><strong>Note</strong> — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.</p>
  <ul><li><input type="checkbox" disabled /> Reviewed and validated by a qualified human reviewer</li></ul>
  </blockquote>
</div>

**Type**: User Story
**Priority**: Immediate
**Tags**: `rai:fair-bias-managed`
**RAI Owner**: TBD — assign during backlog refinement

---

## WI-RAI-006: [RAI] Complete Data Protection Impact Assessment

<div>
  <h3>RAI Control: DPIA Completion</h3>
  <p><strong>NIST Characteristic:</strong> Privacy-Enhanced (MS-2.10)</p>
  <p><strong>Threat:</strong> T-RAI-008 - Photo retention and T-RAI-014 - Consent provenance gaps</p>
  <p><strong>Control Surface:</strong> Prevent - Privacy impact assessment before processing personal data</p>
  <p><strong>Evidence:</strong> Gap — Constitution requires DPIA but none completed</p>
  <p><strong>Suggested Remediation Horizon:</strong> Pre-Production</p>
  <h4>Implementation</h4>
  <p>Complete DPIA covering: photo processing (body images), measurement extraction (body dimensions), profile storage (size history), and consent workflows. Assess lawful basis under GDPR Art. 6 and Art. 9 (special category data). Document data flows, retention periods, and rights fulfillment mechanisms.</p>
  <h4>Acceptance Criteria</h4>
  <ul>
    <li>DPIA document completed covering all data processing activities</li>
    <li>Lawful basis determined for body image and measurement processing</li>
    <li>DPIA reviewed by data protection officer or legal counsel</li>
    <li>Remediation actions from DPIA tracked in backlog</li>
  </ul>
  <blockquote>
  <p><strong>Note</strong> — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.</p>
  <ul><li><input type="checkbox" disabled /> Reviewed and validated by a qualified human reviewer</li></ul>
  </blockquote>
</div>

**Type**: User Story
**Priority**: Immediate
**Tags**: `rai:privacy-enhanced`
**RAI Owner**: TBD — assign during backlog refinement

---

## WI-RAI-007: [RAI] Consent verification mechanism

<div>
  <h3>RAI Control: Consent Integrity Verification</h3>
  <p><strong>NIST Characteristic:</strong> Privacy-Enhanced (MS-2.10)</p>
  <p><strong>Threat:</strong> T-RAI-014 - Consent provenance gaps</p>
  <p><strong>Control Surface:</strong> Prevent - Consent management and verification</p>
  <p><strong>Evidence:</strong> Gap — API trusts frontend-provided consent without validation</p>
  <p><strong>Suggested Remediation Horizon:</strong> Pre-Production</p>
  <h4>Implementation</h4>
  <p>Define consent receipt specification. Add server-side validation of consentGrantedAt recency (reject if >24h old). Document consent requirements in DPA and API documentation. Consider consent receipt token signed by frontend SDK.</p>
  <h4>Acceptance Criteria</h4>
  <ul>
    <li>Consent receipt specification documented</li>
    <li>Server-side validation rejects stale consent timestamps</li>
    <li>DPA updated with consent verification requirements</li>
    <li>API rejects requests with missing or invalid consent metadata</li>
  </ul>
  <blockquote>
  <p><strong>Note</strong> — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.</p>
  <ul><li><input type="checkbox" disabled /> Reviewed and validated by a qualified human reviewer</li></ul>
  </blockquote>
</div>

**Type**: Task
**Priority**: Near-term
**Tags**: `rai:privacy-enhanced`
**RAI Owner**: TBD — assign during backlog refinement

---

## WI-RAI-008: [RAI] Size-proportional tolerance band validation

<div>
  <h3>RAI Control: Proportional Tolerance Bands</h3>
  <p><strong>NIST Characteristic:</strong> Fair with Harmful Bias Managed (MS-2.11)</p>
  <p><strong>Threat:</strong> T-RAI-007 - Tolerance band bias across body sizes</p>
  <p><strong>Control Surface:</strong> Prevent - Bias testing with proportional thresholds</p>
  <p><strong>Evidence:</strong> Partial — configurable bands exist but use absolute thresholds</p>
  <p><strong>Suggested Remediation Horizon:</strong> Pre-Production</p>
  <h4>Implementation</h4>
  <p>Replace absolute cm tolerance thresholds with size-proportional calculations. Validate updated bands against diverse body size data. Document the proportional algorithm and test edge cases (petite, tall, plus-size).</p>
  <h4>Acceptance Criteria</h4>
  <ul>
    <li>Tolerance bands use proportional calculation relative to body measurements</li>
    <li>Validated against body sizes XS through 5XL+</li>
    <li>Proportional algorithm documented and reviewed</li>
    <li>No statistically significant fit recommendation bias across size groups</li>
  </ul>
  <blockquote>
  <p><strong>Note</strong> — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.</p>
  <ul><li><input type="checkbox" disabled /> Reviewed and validated by a qualified human reviewer</li></ul>
  </blockquote>
</div>

**Type**: Task
**Priority**: Near-term
**Tags**: `rai:fair-bias-managed`
**RAI Owner**: TBD — assign during backlog refinement

---

## WI-RAI-009: [RAI] Adversarial image detection and measurement anomaly alerting

<div>
  <h3>RAI Control: Adversarial Input Detection</h3>
  <p><strong>NIST Characteristic:</strong> Secure and Resilient (MS-2.7)</p>
  <p><strong>Threat:</strong> T-RAI-002 - Adversarial image manipulation</p>
  <p><strong>Control Surface:</strong> Detect - Anomaly monitoring for adversarial inputs</p>
  <p><strong>Evidence:</strong> Partial — Content Safety filtering exists; no adversarial-specific detection</p>
  <p><strong>Suggested Remediation Horizon:</strong> Pre-Production</p>
  <h4>Implementation</h4>
  <p>Add measurement distribution anomaly detection to flag statistically unlikely body measurements. Implement EXIF stripping (shared with WI-RAI-002). Add adversarial input monitoring alerts when measurement outputs fall outside physiologically plausible ranges.</p>
  <h4>Acceptance Criteria</h4>
  <ul>
    <li>Measurement anomaly detection flags outputs outside plausible ranges</li>
    <li>Alerting configured for anomalous measurement patterns</li>
    <li>Anomaly detection tested against known adversarial image techniques</li>
  </ul>
  <blockquote>
  <p><strong>Note</strong> — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.</p>
  <ul><li><input type="checkbox" disabled /> Reviewed and validated by a qualified human reviewer</li></ul>
  </blockquote>
</div>

**Type**: Task
**Priority**: Near-term
**Tags**: `rai:secure-resilient`
**RAI Owner**: TBD — assign during backlog refinement

---

## WI-RAI-010: [RAI] Disparate impact testing methodology

<div>
  <h3>RAI Control: Disparate Impact Measurement</h3>
  <p><strong>NIST Characteristic:</strong> Fair with Harmful Bias Managed (MS-2.11)</p>
  <p><strong>Threat:</strong> T-RAI-001 - Demographic accuracy disparity</p>
  <p><strong>Control Surface:</strong> Detect - Demographic parity monitoring and disparate impact alerts</p>
  <p><strong>Evidence:</strong> Gap — no disparate impact testing plan</p>
  <p><strong>Suggested Remediation Horizon:</strong> Pre-Production</p>
  <h4>Implementation</h4>
  <p>Define disparate impact testing methodology covering rejection rates, accuracy, and confidence scores across demographic segments. Implement automated reporting. Set alert thresholds for statistically significant disparities.</p>
  <h4>Acceptance Criteria</h4>
  <ul>
    <li>Disparate impact methodology documented and reviewed</li>
    <li>Automated reporting for rejection rate, accuracy, and confidence by segment</li>
    <li>Alert thresholds defined for statistically significant disparities</li>
    <li>Baseline report generated before production launch</li>
  </ul>
  <blockquote>
  <p><strong>Note</strong> — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.</p>
  <ul><li><input type="checkbox" disabled /> Reviewed and validated by a qualified human reviewer</li></ul>
  </blockquote>
</div>

**Type**: User Story
**Priority**: Near-term
**Tags**: `rai:fair-bias-managed`
**RAI Owner**: TBD — assign during backlog refinement

---

## WI-RAI-011: [RAI] Photo purge verification and compliance audit

<div>
  <h3>RAI Control: Photo Purge Verification</h3>
  <p><strong>NIST Characteristic:</strong> Privacy-Enhanced (MS-2.10)</p>
  <p><strong>Threat:</strong> T-RAI-008 - Photo retention beyond 60s TTL</p>
  <p><strong>Control Surface:</strong> Detect - Data leakage detection and consent compliance monitoring</p>
  <p><strong>Evidence:</strong> Partial — 60s TTL lifecycle policy exists; no verification or alerting</p>
  <p><strong>Suggested Remediation Horizon:</strong> Early Operations</p>
  <h4>Implementation</h4>
  <p>Implement automated blob age check that alerts on photos exceeding 60s TTL. Add quarterly compliance audit procedure. Create operational runbook for TTL violation incidents.</p>
  <h4>Acceptance Criteria</h4>
  <ul>
    <li>Automated alert fires when any blob exceeds 60s age</li>
    <li>Quarterly compliance audit procedure documented</li>
    <li>Operational runbook for TTL violations created</li>
  </ul>
  <blockquote>
  <p><strong>Note</strong> — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.</p>
  <ul><li><input type="checkbox" disabled /> Reviewed and validated by a qualified human reviewer</li></ul>
  </blockquote>
</div>

**Type**: Task
**Priority**: Planned
**Tags**: `rai:privacy-enhanced`
**RAI Owner**: TBD — assign during backlog refinement

---

## WI-RAI-012: [RAI] Load-dependent accuracy monitoring and alerting

<div>
  <h3>RAI Control: Load-Quality Regression Detection</h3>
  <p><strong>NIST Characteristic:</strong> Valid and Reliable (MS-2.5)</p>
  <p><strong>Threat:</strong> T-RAI-009 - AI accuracy degradation under load</p>
  <p><strong>Control Surface:</strong> Detect - Performance degradation alerts and anomaly monitoring</p>
  <p><strong>Evidence:</strong> Partial — resilience pipelines exist; no per-request accuracy monitoring</p>
  <p><strong>Suggested Remediation Horizon:</strong> Early Operations</p>
  <h4>Implementation</h4>
  <p>Add per-request confidence trending that correlates with system load. Alert when average confidence drops below threshold during high-traffic periods. Integrate with existing resilience monitoring.</p>
  <h4>Acceptance Criteria</h4>
  <ul>
    <li>Confidence trending correlated with request volume</li>
    <li>Alert configured for confidence drops during high load</li>
    <li>Dashboard displays load-accuracy correlation</li>
  </ul>
  <blockquote>
  <p><strong>Note</strong> — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.</p>
  <ul><li><input type="checkbox" disabled /> Reviewed and validated by a qualified human reviewer</li></ul>
  </blockquote>
</div>

**Type**: Task
**Priority**: Planned
**Tags**: `rai:valid-reliable`
**RAI Owner**: TBD — assign during backlog refinement

---

## WI-RAI-013: [RAI] GPT-5.2 temperature pinning and output variance monitoring

<div>
  <h3>RAI Control: Non-Deterministic Output Control</h3>
  <p><strong>NIST Characteristic:</strong> Valid and Reliable (MS-2.5)</p>
  <p><strong>Threat:</strong> T-RAI-010 - Non-deterministic output variance</p>
  <p><strong>Control Surface:</strong> Prevent - Failsafe defaults for temperature setting; Detect - Variance monitoring</p>
  <p><strong>Evidence:</strong> Partial — structured output schema enforced; temperature not specified</p>
  <p><strong>Suggested Remediation Horizon:</strong> Early Operations</p>
  <h4>Implementation</h4>
  <p>Set temperature=0 for GPT-5.2 measurement extraction calls. Implement measurement variance tracking across repeat assessments of the same image. Alert on variance exceeding threshold.</p>
  <h4>Acceptance Criteria</h4>
  <ul>
    <li>Temperature=0 configured for all measurement extraction calls</li>
    <li>Variance tracking implemented for repeat assessments</li>
    <li>Alert threshold defined and tested</li>
  </ul>
  <blockquote>
  <p><strong>Note</strong> — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.</p>
  <ul><li><input type="checkbox" disabled /> Reviewed and validated by a qualified human reviewer</li></ul>
  </blockquote>
</div>

**Type**: Task
**Priority**: Planned
**Tags**: `rai:valid-reliable`
**RAI Owner**: TBD — assign during backlog refinement

---

## WI-RAI-014: [RAI] Conservative minor detection threshold tuning

<div>
  <h3>RAI Control: Minor Boundary Safety</h3>
  <p><strong>NIST Characteristic:</strong> Safe (MS-2.6)</p>
  <p><strong>Threat:</strong> T-RAI-013 - Minor boundary exploitation</p>
  <p><strong>Control Surface:</strong> Prevent - Safety boundary enforcement with conservative thresholds</p>
  <p><strong>Evidence:</strong> Partial — Content Safety minor detection exists; threshold not tuned conservatively</p>
  <p><strong>Suggested Remediation Horizon:</strong> Early Operations</p>
  <h4>Implementation</h4>
  <p>Tune Content Safety age detection to block the 15-17 range conservatively. Implement near-boundary audit logging for ages estimated 14-18. Define escalation protocol for edge cases.</p>
  <h4>Acceptance Criteria</h4>
  <ul>
    <li>Conservative age threshold blocks estimated 15-17 age range</li>
    <li>Near-boundary (14-18) audit logging implemented</li>
    <li>Escalation protocol documented for edge cases</li>
  </ul>
  <blockquote>
  <p><strong>Note</strong> — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.</p>
  <ul><li><input type="checkbox" disabled /> Reviewed and validated by a qualified human reviewer</li></ul>
  </blockquote>
</div>

**Type**: Task
**Priority**: Planned
**Tags**: `rai:safe`
**RAI Owner**: TBD — assign during backlog refinement

---

## WI-RAI-015: [RAI] Public transparency note and model card

<div>
  <h3>RAI Control: Public AI Documentation</h3>
  <p><strong>NIST Characteristic:</strong> Accountable and Transparent (MS-2.8)</p>
  <p><strong>Threat:</strong> N/A — documentation gap</p>
  <p><strong>Control Surface:</strong> Prevent - Model cards and decision audit trails</p>
  <p><strong>Evidence:</strong> Gap — no public-facing transparency note or model card</p>
  <p><strong>Suggested Remediation Horizon:</strong> Ongoing Governance</p>
  <h4>Implementation</h4>
  <p>Create a public-facing transparency note covering: what the AI does, how it works (without prompt details), known limitations, accuracy bounds, and how to report concerns. Publish model card documenting accuracy per garment category and known biases.</p>
  <h4>Acceptance Criteria</h4>
  <ul>
    <li>Transparency note published and accessible to shoppers</li>
    <li>Model card documents accuracy bounds and known limitations</li>
    <li>Report-a-concern mechanism linked from transparency note</li>
  </ul>
  <blockquote>
  <p><strong>Note</strong> — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.</p>
  <ul><li><input type="checkbox" disabled /> Reviewed and validated by a qualified human reviewer</li></ul>
  </blockquote>
</div>

**Type**: User Story
**Priority**: Backlog
**Tags**: `rai:accountable-transparent`
**RAI Owner**: TBD — assign during backlog refinement

---

## WI-RAI-016: [RAI] SMPL model roadmap for v2 explainability

<div>
  <h3>RAI Control: Explainable Measurement Extraction</h3>
  <p><strong>NIST Characteristic:</strong> Explainable and Interpretable (MS-2.9)</p>
  <p><strong>Threat:</strong> T-RAI-011 - Opaque measurement extraction</p>
  <p><strong>Control Surface:</strong> Prevent - Interpretable model selection</p>
  <p><strong>Evidence:</strong> Tradeoff documented — black-box GPT-5.2 accepted for v1; SMPL model planned for v2</p>
  <p><strong>Suggested Remediation Horizon:</strong> Ongoing Governance</p>
  <h4>Implementation</h4>
  <p>Evaluate SMPL (Skinned Multi-Person Linear) model as an alternative or complement to GPT-5.2 for body measurement extraction. SMPL provides explicit body landmark points, improving explainability. Create technical feasibility assessment and roadmap.</p>
  <h4>Acceptance Criteria</h4>
  <ul>
    <li>SMPL model feasibility assessment completed</li>
    <li>Accuracy comparison: SMPL vs GPT-5.2 documented</li>
    <li>V2 roadmap with explainability milestones defined</li>
  </ul>
  <blockquote>
  <p><strong>Note</strong> — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.</p>
  <ul><li><input type="checkbox" disabled /> Reviewed and validated by a qualified human reviewer</li></ul>
  </blockquote>
</div>

**Type**: User Story
**Priority**: Backlog
**Tags**: `rai:explainable-interpretable`, `rai:tradeoff`
**RAI Owner**: TBD — assign during backlog refinement

---

## WI-RAI-017: [RAI] Azure OpenAI CoC biometric boundary legal review

<div>
  <h3>RAI Control: CoC Compliance Verification</h3>
  <p><strong>NIST Characteristic:</strong> Accountable and Transparent (MS-2.8)</p>
  <p><strong>Threat:</strong> N/A — regulatory compliance gap</p>
  <p><strong>Control Surface:</strong> Prevent - Compliance monitoring and approval workflows</p>
  <p><strong>Evidence:</strong> Gap — legal review needed on whether body measurement extraction constitutes biometric categorization under Azure OpenAI CoC restriction #10</p>
  <p><strong>Suggested Remediation Horizon:</strong> Ongoing Governance</p>
  <h4>Implementation</h4>
  <p>Engage legal counsel to review whether functional body measurement extraction for clothing fit constitutes "biometric categorization" under Azure OpenAI CoC restriction #10. Document the legal opinion and any required mitigations or usage modifications.</p>
  <h4>Acceptance Criteria</h4>
  <ul>
    <li>Legal opinion obtained on biometric vs. functional measurement boundary</li>
    <li>Opinion documented and accessible to engineering and compliance teams</li>
    <li>Any required usage modifications implemented</li>
  </ul>
  <blockquote>
  <p><strong>Note</strong> — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.</p>
  <ul><li><input type="checkbox" disabled /> Reviewed and validated by a qualified human reviewer</li></ul>
  </blockquote>
</div>

**Type**: Task
**Priority**: Planned
**Tags**: `rai:accountable-transparent`
**RAI Owner**: TBD — assign during backlog refinement

---

## WI-RAI-018: [RAI] Appropriate reliance framing in API responses

<div>
  <h3>RAI Control: Trust Calibration Messaging</h3>
  <p><strong>NIST Characteristic:</strong> Accountable and Transparent (MS-2.8)</p>
  <p><strong>Threat:</strong> N/A — appropriate reliance gap from tradeoff analysis</p>
  <p><strong>Control Surface:</strong> Prevent - Decision documentation and explanation interfaces</p>
  <p><strong>Evidence:</strong> Partial — isLowConfidence flag and disclaimer exist; no calibration guidance</p>
  <p><strong>Suggested Remediation Horizon:</strong> Ongoing Governance</p>
  <h4>Implementation</h4>
  <p>Add contextual framing to API response or frontend SDK guidance: "This recommendation is based on AI measurement extraction and may not be exact. We suggest also checking the size chart for this brand." Define guidance for when to trust vs. question the AI output.</p>
  <h4>Acceptance Criteria</h4>
  <ul>
    <li>Contextual framing text included in API response or SDK documentation</li>
    <li>Guidance documented for frontend teams on presenting confidence information</li>
    <li>Size chart cross-reference suggested alongside AI recommendation</li>
  </ul>
  <blockquote>
  <p><strong>Note</strong> — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.</p>
  <ul><li><input type="checkbox" disabled /> Reviewed and validated by a qualified human reviewer</li></ul>
  </blockquote>
</div>

**Type**: Task
**Priority**: Backlog
**Tags**: `rai:accountable-transparent`, `rai:tradeoff`
**RAI Owner**: TBD — assign during backlog refinement

# Responsible AI Assessment Report

## VirtualMirror AI Clothing Fit Assessment Agent

| Field | Value |
|-------|-------|
| **Assessment Date** | 2026-05-14 |
| **Framework** | NIST AI Risk Management Framework 1.0 |
| **Depth Tier** | Comprehensive |
| **Entry Mode** | From PRD |
| **Suggested Review Status** | Additional attention suggested |
| **Work Items Generated** | 18 |

---

## Executive Summary

This Responsible AI assessment evaluates the VirtualMirror AI Clothing Fit Assessment Agent against the NIST AI Risk Management Framework 1.0. The system uses three AI components — GPT-5.2 Vision (measurement extraction), Florence-2 (people detection), and Azure AI Content Safety (minor/content filtering) — to generate clothing fit recommendations from shopper-uploaded body photos.

All three risk indicators activated during classification, placing the system at the **Comprehensive** depth tier. The assessment identified **14 RAI-specific threats** (6 High, 7 Moderate, 1 Low concern), cataloged **28 evidence items** (50% coverage), and documented **5 trustworthiness tradeoffs**. Of 14 threats evaluated for control adequacy, **5 have inadequate controls**, **8 have partial controls**, and **1 has adequate controls**.

The dominant harm vector is **body image sensitivity** — the system generates AI-driven language about human bodies, creating psychological safety risk if phrasing is inappropriate. The least mature characteristic is **Fair with Harmful Bias Managed**, which has constitutional intent but zero operational controls.

**18 remediation work items** are recommended: 10 Pre-Production, 4 Early Operations, and 4 Ongoing Governance.

---

## 1. System Overview

### 1.1 AI Components

| Component | Purpose | Model | Deployment |
|-----------|---------|-------|------------|
| GPT-5.2 Vision | Extract body measurements from photos; generate fit recommendations | Azure OpenAI GPT-5.2 | Azure OpenAI Service |
| Florence-2 | Detect and validate single-person photos | Azure AI Foundry Florence-2 | Azure Container Apps |
| Azure AI Content Safety | Detect minors; filter harmful content | Azure AI Content Safety | Azure Cognitive Services |

### 1.2 Data Flow Summary

```
Shopper photo → Blob Storage (60s TTL) → Florence-2 (person detection)
  → Content Safety (minor/content check) → GPT-5.2 Vision (measurement extraction)
  → Fit recommendation → Cosmos DB (assessment record) → API response
```

### 1.3 Stakeholders

| Stakeholder | Role | Vulnerability |
|-------------|------|--------------|
| Shoppers | End users receiving fit recommendations | **High** — body image sensitivity, demographic accuracy disparity |
| Retail partners | Tenants configuring tolerance bands and garment data | Medium — reputation risk from AI errors |
| Frontend teams | Integrate SDK and present results | Low — implementation complexity |
| Customer service | Handle complaints about AI recommendations | Medium — escalation volume |
| Regulators | GDPR, CCPA, EU AI Act oversight | Medium — compliance enforcement |
| Body-image advocacy groups | Monitor AI systems affecting body perception | Medium — public scrutiny |

---

## 2. Risk Classification

### 2.1 Prohibited Uses Gate

**Status**: PASS

10 prohibited uses declared from Azure OpenAI Code of Conduct v4.0 and VirtualMirror Constitution. Key restrictions:

| ID | Prohibited Use | Source |
|----|---------------|--------|
| PU-001 | Body-shaming or appearance-based discrimination | Constitution Principle III |
| PU-002 | Biometric categorization for identification | Azure OpenAI CoC #10 |
| PU-003 | Sensitive attribute inference (race, ethnicity, sexual orientation) | Azure OpenAI CoC #11 |
| PU-004 | Identity verification or facial recognition | Azure OpenAI CoC #15 |
| PU-005 | Persistent tracking across sessions without consent | Azure OpenAI CoC #17 |

> **Legal review required**: The boundary between "biometric categorization" (prohibited under CoC #10) and "functional body measurement for clothing fit" requires legal opinion.

### 2.2 Risk Indicators

| Indicator | Method | Activated | Observation |
|-----------|--------|-----------|-------------|
| Safety and Reliability | Binary | **Yes** | Psychological harm via body-related AI output; measurement inaccuracy affects purchasing decisions |
| Rights, Fairness, and Privacy | Categorical | **Yes** | Biometric-adjacent data processing; GDPR Art. 9 special category implications; demographic accuracy disparity risk |
| Security and Explainability | Continuous | **Yes** | Black-box LLM extraction; adversarial surface via image uploads; prompt injection vectors |

**Activated Count**: 3 of 3 → **Comprehensive** depth tier

---

## 3. Standards Mapping

### 3.1 NIST AI RMF Trustworthiness Characteristics

| Characteristic | Maturity | Key Gap |
|----------------|----------|---------|
| Valid and Reliable | Developing | No validation dataset; accuracy hypothesis (±2-4 cm) unvalidated |
| Safe | Developing | No language sensitivity review; no user testing with vulnerable populations |
| Secure and Resilient | Developing | No adversarial AI testing; no EXIF metadata stripping |
| Accountable and Transparent | Established | No public transparency note or model card |
| Explainable and Interpretable | Foundational | Black-box extraction; no measurement explanation or dispute mechanism |
| Privacy-Enhanced | Established | DPIA not completed; consent verification gap |
| Fair with Harmful Bias Managed | Foundational | No bias evaluation dataset, parity thresholds, or disparate impact testing |

### 3.2 Regulatory Jurisdiction Assessment

| Regulation | Relevance | Key Concern |
|------------|-----------|-------------|
| GDPR | High | Body photos as special category data (Art. 9); 60s TTL processing; cross-border data flows |
| CCPA | High | Consumer right to deletion; opt-out of AI processing; data broker implications |
| EU AI Act | Medium-High | Potential high-risk classification for biometric-adjacent processing |
| State Biometric Laws | Medium | Illinois BIPA, Texas CUBI, Washington state biometric provisions |
| FTC | Medium | Algorithmic fairness enforcement; unfair/deceptive practices |

---

## 4. Threat Analysis

### 4.1 Threat Summary

14 threats identified using AI STRIDE taxonomy with dual threat ID convention.

#### High Concern (6)

| ID | Threat | Component | Control Adequacy |
|----|--------|-----------|-----------------|
| T-RAI-001 | Demographic accuracy disparity across body types, skin tones, cultural dress | GPT-5.2 Vision | **Inadequate** |
| T-RAI-003 | Prompt injection via EXIF/IPTC/XMP metadata in uploaded photos | GPT-5.2 Vision | **Inadequate** |
| T-RAI-005 | Body-image harm via fit recommendation language | GPT-5.2 Vision | **Inadequate** |
| T-RAI-007 | Tolerance band bias — absolute thresholds disadvantage non-average body sizes | Assessment Engine | Partial |
| T-RAI-011 | Opaque measurement extraction — shoppers cannot understand derivation | GPT-5.2 Vision | **Inadequate** |
| T-RAI-012 | Florence-2 detection bias — wheelchair users, prosthetics, cultural garments | Florence-2 | **Inadequate** |

#### Moderate Concern (7)

| ID | Threat | Component | Control Adequacy |
|----|--------|-----------|-----------------|
| T-RAI-002 | Adversarial image manipulation to produce incorrect measurements | GPT-5.2 Vision | Partial |
| T-RAI-004 | Model inversion / measurement leakage via repeated queries | GPT-5.2 Vision | Partial |
| T-RAI-008 | Photo retention beyond 60s TTL policy | Blob Storage | Partial |
| T-RAI-009 | AI accuracy degradation under high traffic load | GPT-5.2 Vision | Partial |
| T-RAI-010 | Non-deterministic output variance across identical inputs | GPT-5.2 Vision | Partial |
| T-RAI-013 | Minor boundary exploitation — near-threshold age detection | Content Safety | Partial |
| T-RAI-014 | Consent provenance gaps — frontend-provided consent trusted without validation | Assessment Engine | Partial |

#### Low Concern (1)

| ID | Threat | Component | Control Adequacy |
|----|--------|-----------|-----------------|
| T-RAI-006 | Unattributable recommendation errors | Assessment Engine | Adequate |

### 4.2 Control Adequacy Distribution

| Adequacy | Count | Percentage |
|----------|-------|------------|
| Adequate | 1 | 7% |
| Partial | 8 | 57% |
| Inadequate | 5 | 36% |

---

## 5. Impact Assessment

### 5.1 Evidence Register Summary

| NIST Characteristic | Evidence Items | Exists | Missing | Maturity |
|--------------------|---------------|--------|---------|----------|
| Valid and Reliable | 3 | 3 | 0 | Partial — design evidence only |
| Safe | 4 | 2 | 2 | Partial — constitutional controls only |
| Secure and Resilient | 3 | 1 | 2 | Partial — resilience strong, adversarial absent |
| Accountable and Transparent | 3 | 2 | 1 | Mostly — audit trail strong |
| Explainable and Interpretable | 3 | 1 | 2 | Weak — outputs interpretable, process opaque |
| Privacy-Enhanced | 6 | 4 | 2 | Mostly — strong architecture |
| Fair with Harmful Bias Managed | 6 | 1 | 5 | Weak — acknowledged but not operationalized |
| **Total** | **28** | **14** | **14** | **50% evidence coverage** |

### 5.2 Trustworthiness Tradeoffs

| # | Tradeoff | Current Position | Recommendation |
|---|----------|-----------------|----------------|
| 1 | **Privacy vs. Accuracy** — 60s TTL prevents validation dataset building | Privacy wins | Use consented opt-in research program or synthetic images for benchmarking |
| 2 | **Explainability vs. Performance** — GPT-5.2 black-box provides best accuracy | Accuracy wins | Accept for v1; plan SMPL model for v2 with explicit body landmarks |
| 3 | **Fairness vs. Complexity** — Demographic parity requires model fine-tuning | Simplicity wins for v1 | Pre-launch: build diverse dataset and measure baseline parity |
| 4 | **Safety vs. Utility** — Conservative thresholds reduce assessment volume | Safety wins | Maintain for launch; adjust only with production evidence |
| 5 | **Transparency vs. IP** — Full methodology disclosure aids adversaries | Partial transparency | Publish model card without prompt engineering details |

### 5.3 Appropriate Reliance

| Dimension | Assessment |
|-----------|-----------|
| Over-reliance risk | Shoppers may treat AI fit recommendation as definitive |
| Under-reliance risk | Frequent disclaimers may cause feature abandonment |
| Trust calibration | Confidence percentage + per-area breakdown + low-confidence disclaimer |
| Human-in-the-loop | Shopper retains full decision authority; recommendation is advisory only |
| Gap | No guidance for when to trust vs. question the AI; no size chart comparison framing |

---

## 6. Review Quality

| Dimension | Status | Rationale |
|-----------|--------|-----------|
| Standards Alignment | Addressed | All 7 NIST characteristics mapped; 5 regulatory jurisdictions assessed; subcategory cross-references (MS-2.5 through MS-2.11) |
| Threat Completeness | Addressed | 14 threats with AI STRIDE taxonomy; ML STRIDE matrix completed; dual threat ID convention established |
| Control Effectiveness | Addressed | All 14 threats evaluated across Prevent/Detect/Respond; adequacy distribution documented |
| Evidence Quality | Addressed | 28 evidence items cataloged with source references; gaps identified per characteristic |
| Tradeoff Resolution | Addressed | 5 tradeoffs with tension, current choice, impact analysis, and recommendations |
| Risk Classification | Addressed | All 3 indicators activated; Comprehensive tier confirmed; prohibited uses gate passed with 10 declarations |

**Suggested Review Status**: **Additional attention suggested** — Fair with Harmful Bias Managed and Explainable and Interpretable are at Foundational maturity with multiple open items requiring remediation before production deployment.

---

## 7. Remediation Backlog

### 7.1 Horizon Summary

| Horizon | Count | Priority Mix |
|---------|-------|-------------|
| **Pre-Production** | 10 | 5 Immediate, 5 Near-term |
| **Early Operations** | 4 | 4 Planned |
| **Ongoing Governance** | 4 | 1 Planned, 3 Backlog |

### 7.2 Pre-Production Items (Immediate)

| ID | Title | Characteristic | Threat |
|----|-------|---------------|--------|
| WI-RAI-001 | Demographic accuracy benchmarking dataset and parity thresholds | Fair with Harmful Bias Managed | T-RAI-001 |
| WI-RAI-002 | Strip image metadata before AI processing | Secure and Resilient | T-RAI-003 |
| WI-RAI-003 | Fit language sensitivity review and neutral response mode | Safe | T-RAI-005 |
| WI-RAI-005 | Florence-2 accessibility and demographic detection testing | Fair with Harmful Bias Managed | T-RAI-012 |
| WI-RAI-006 | Complete Data Protection Impact Assessment | Privacy-Enhanced | T-RAI-008/014 |

### 7.3 Pre-Production Items (Near-term)

| ID | Title | Characteristic | Threat |
|----|-------|---------------|--------|
| WI-RAI-004 | Measurement explanation annotations and dispute mechanism | Explainable and Interpretable | T-RAI-011 |
| WI-RAI-007 | Consent verification mechanism | Privacy-Enhanced | T-RAI-014 |
| WI-RAI-008 | Size-proportional tolerance band validation | Fair with Harmful Bias Managed | T-RAI-007 |
| WI-RAI-009 | Adversarial image detection and measurement anomaly alerting | Secure and Resilient | T-RAI-002 |
| WI-RAI-010 | Disparate impact testing methodology | Fair with Harmful Bias Managed | T-RAI-001 |

### 7.4 Early Operations Items

| ID | Title | Characteristic | Threat |
|----|-------|---------------|--------|
| WI-RAI-011 | Photo purge verification and compliance audit | Privacy-Enhanced | T-RAI-008 |
| WI-RAI-012 | Load-dependent accuracy monitoring and alerting | Valid and Reliable | T-RAI-009 |
| WI-RAI-013 | GPT-5.2 temperature pinning and output variance monitoring | Valid and Reliable | T-RAI-010 |
| WI-RAI-014 | Conservative minor detection threshold tuning | Safe | T-RAI-013 |

### 7.5 Ongoing Governance Items

| ID | Title | Characteristic | Threat |
|----|-------|---------------|--------|
| WI-RAI-015 | Public transparency note and model card | Accountable and Transparent | — |
| WI-RAI-016 | SMPL model roadmap for v2 explainability | Explainable and Interpretable | T-RAI-011 |
| WI-RAI-017 | Azure OpenAI CoC biometric boundary legal review | Accountable and Transparent | — |
| WI-RAI-018 | Appropriate reliance framing in API responses | Accountable and Transparent | — |

---

## 8. Assessment Artifacts

| Phase | Artifact | Description |
|-------|----------|-------------|
| 1 | `system-definition-pack.md` | AI system overview, component inventory, data flows, prohibited uses |
| 1 | `stakeholder-impact-map.md` | Stakeholder classification and impact assessment |
| 3 | `rai-standards-mapping.md` | NIST AI RMF characteristic mapping and regulatory assessment |
| 4 | `rai-threat-addendum.md` | 14 RAI-specific threats with ML STRIDE matrix |
| 5 | `control-surface-catalog.md` | Control adequacy evaluation for all 14 threats |
| 5 | `evidence-register.md` | 28 evidence items with coverage status |
| 5 | `rai-tradeoffs.md` | 5 trustworthiness tradeoffs with appropriate reliance assessment |
| 6 | `rai-review-summary.md` | Review quality assessment and remediation horizon summary |
| 6 | `backlog-ado.md` | 18 ADO-format work items |
| 6 | `backlog-github.md` | 18 GitHub-format issues |
| Ref | `references/azure-openai-code-of-conduct.md` | Azure OpenAI CoC v4.0 summary |

---

> **Note** — The author created this content with assistance from AI. All outputs should be reviewed and validated before use.
> - [ ] Reviewed and validated by a qualified human reviewer

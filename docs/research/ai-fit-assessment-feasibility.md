# AI Clothing Fit Assessment: Feasibility & Industry Research

**Date**: 2026-05-13
**Purpose**: Evaluate the technical feasibility, industry success rates, and risks of using AI/ML for clothing fit assessment from shopper photos.

> **⚠️ NOTE**: This feasibility study informed [ADR-001](../architecture/decision-register.md#adr-001-body-measurement-extraction-approach). The final architecture adopted **Florence-2 on Azure AI Foundry** (Tier 1 validation, replacing Azure AI Vision 4.0) and **Azure OpenAI GPT-5.2 Vision** (Tier 2 extraction, replacing GPT-4o which retired March 2026). See the [solution architecture](../architecture/solution-architecture.md) for the current design.

---

## Executive Summary

AI-powered fit assessment from 2D photos is a **proven but challenging** technology. Industry leaders report 20-40% return reductions, but accuracy varies significantly based on approach. The key finding of this research is that **Azure AI Vision does NOT provide body landmark extraction** — the implementation requires either a custom ML pipeline, Azure OpenAI multimodal models, or third-party body measurement APIs.

**Verdict**: Feasible with realistic expectations (70-85% accuracy) but requires architecture revision to address the Azure AI Vision gap.

---

## 1. Industry Landscape

### 1.1 Major Players & Reported Results

| Company | Approach | Claimed Results | Notable Clients |
|---------|----------|-----------------|-----------------|
| **3DLOOK** | 2D photo → 3D body model (SMPL-based) | ±1.5cm accuracy, 30% return reduction | Levi's, 1822 Denim |
| **Bold Metrics** | Statistical model + purchase history | 20-25% return reduction, 85% size accuracy | Hugo Boss, Canada Goose |
| **True Fit** | Collaborative filtering (no photo needed) | 22% fewer returns, 2x conversion | Macy's, Nordstrom |
| **Fit Analytics** (acquired by Snap) | Purchase data + body surveys | 28% return reduction | ASOS, The North Face |
| **Virtusize** | Garment silhouette comparison | 26% return reduction | Balenciaga, United Arrows |
| **MySizeID** | Smartphone sensor body measurement | ±2cm accuracy | Levi's, PVH Corp |
| **Amazon (Just Walk Out → Made for You)** | Custom body scan (retired 2022) | Insufficient accuracy (product discontinued) | Internal only |
| **Nike Fit** | AR foot scanning (feet only) | 60% reduction in incorrect shoe sizes | Nike stores |

### 1.2 Market Context

- Global virtual fitting room market: ~$5.7B (2025), projected $19.2B by 2030 (CAGR ~27%)
- Online clothing return rate: 25-40% (industry average), with "wrong fit" cited as reason in 52% of returns
- Cost per return: $10-30 processing cost + lost revenue
- Retailer ROI for AI sizing tools: 3-5x within first year (vendor-reported)

---

## 2. Technical Approaches

### 2.1 Photo-Based Body Measurement (Our Approach)

**How it works**: Single or dual 2D photos → pose estimation → body landmark extraction → anthropometric measurement estimation → garment comparison.

**Academic State of the Art**:

| Method | Year | Accuracy (cm MAE) | Notes |
|--------|------|-------------------|-------|
| HMR (Human Mesh Recovery) | 2018 | ±3-5cm | First viable 2D→3D approach |
| SPIN (Self-Improving Network) | 2019 | ±2-4cm | Iterative regression |
| SMPL-X (body model) | 2019 | ±2-3cm | Industry standard body representation |
| PyMAF (Pyramidal Mesh Alignment) | 2021 | ±1.5-3cm | Improved alignment |
| BodyMap (3DLOOK) | 2022 | ±1-2cm (claimed) | Commercial; requires 2 photos |
| 4DHumans / TokenHMR | 2023-24 | ±1.5-2.5cm | Latest research models |
| GPT-4 Vision + estimation | 2024+ | ±3-5cm (estimated) | No dedicated training; general reasoning |

**Key Insight**: Best-in-class 2D-to-measurement accuracy is **±1.5-2cm** with purpose-trained models. General vision APIs achieve ±3-5cm at best.

### 2.2 Statistical/Collaborative Filtering (No Photo)

Uses purchase history, returns data, and user-reported measurements to predict fit. Simpler to implement, lower accuracy ceiling, but higher user adoption (no photo friction).

### 2.3 Hybrid Approaches

Combine photo-based measurement with purchase history and garment-specific data. Most commercially successful implementations use hybrid approaches.

---

## 3. Critical Technical Finding: Azure AI Vision Gap

### 3.1 What Azure AI Vision 4.0 Actually Provides

Based on current Microsoft documentation:

- **People Detection**: Bounding boxes + confidence scores only
- **NO pose estimation** from cloud API
- **NO body landmark extraction**
- **NO anthropometric measurement**
- Service is **being deprecated** (retiring September 2028)

### 3.2 What Azure Kinect Body Tracking Provides

- 32-joint skeleton with 3D coordinates
- Requires **physical Kinect DK hardware** (depth camera)
- NOT available as a cloud API for 2D photo analysis
- Product is in "previous versions" (end of life)

### 3.3 Viable Microsoft-Stack Alternatives

| Option | Pros | Cons | Accuracy |
|--------|------|------|----------|
| **Azure OpenAI GPT-4o Vision** | Easy integration; can estimate proportions from photo; Microsoft stack | Not trained for precise measurement; ±3-5cm; non-deterministic | Low-Medium |
| **Custom ML model on Azure ML** | Full control; can train SMPL-based model; best accuracy potential | High development cost; needs training data; 3-6 months | High |
| **MediaPipe Pose (containerized)** | Free; 33 landmarks; well-tested; runs in container | Google library (not Microsoft); 2D landmarks only (no depth) | Medium |
| **Third-party API (3DLOOK, Bold Metrics)** | Proven accuracy; fast to integrate | External dependency; per-call cost; data privacy concerns | High |
| **Azure AI Custom Model + Florence 2** | Microsoft-native; customizable | Requires significant ML expertise; newer model | Medium-High |

### 3.4 Recommended Architecture Revision

**Primary**: Azure OpenAI GPT-4o multimodal for initial measurement estimation + custom calibration layer.
**Secondary**: MediaPipe Pose for landmark detection (containerized within Azure Container Apps), with SMPL body model inference for measurement extraction.
**Fallback**: Third-party API (3DLOOK) for validated production accuracy while custom model matures.

---

## 4. Success Factors & Failure Modes

### 4.1 What Makes Implementations Succeed

1. **Realistic accuracy expectations**: 70-85% fit prediction accuracy is achievable; 95%+ is not
2. **Garment-specific training**: Generic body measurements alone are insufficient — garment construction, fabric stretch, and brand sizing variance matter
3. **Feedback loops**: Systems that learn from actual keep/return decisions improve over time (cold-start problem)
4. **User guidance**: Quality of input photo dramatically affects output — guided photo capture UX is critical
5. **Fallback strategy**: Low-confidence results should gracefully degrade to size charts (already in our design)
6. **Tolerance bands per category**: Dresses have tighter tolerance than outerwear (already in our data model)

### 4.2 Common Failure Modes

| Failure Mode | Frequency | Impact | Mitigation |
|--------------|-----------|--------|------------|
| Clothing occlusion in photo | Very High | Can't see body contours under loose clothing | Require form-fitting clothing or silhouette guidance |
| 2D→3D depth ambiguity | High | Shoulder width vs. camera angle confusion | Require front-facing, arms at sides |
| Scale reference missing | High | No way to determine absolute measurements from single photo | Require height input OR reference object |
| Extreme body proportions outside training data | Medium | Model extrapolates poorly | Confidence threshold + fallback (our 70% threshold) |
| Brand sizing inconsistency | High | Same "M" varies 5-8cm between brands | Require actual garment measurements (our approach) |
| Photo quality (lighting, blur, partial body) | High | Garbage in, garbage out | ImageValidator pipeline (our T042) |
| Fabric stretch not modeled | Medium | Stretch denim fits differently than rigid denim | Require fabric composition in garment data |

### 4.3 Critical Risk: Height/Scale Problem

**The single biggest technical challenge**: From a 2D photo alone, it's impossible to determine absolute body dimensions without a known reference (height, object in frame, or dual-camera depth). All successful commercial solutions require at least one of:
- User-provided height
- Known reference object in photo
- Dual photo (front + side)
- Phone sensor data (accelerometer for distance estimation)

**Our spec does not currently address this.** This is a gap that must be resolved.

---

## 5. Accuracy Benchmarks

### 5.1 What "85% accuracy" means (our SC-002)

"85% accuracy in fit predictions validated against return/keep decisions" is:
- **Achievable** for broad categories (correct/incorrect) with hybrid approaches
- **Aggressive** for per-body-area 5-point scale predictions from photos alone
- **Realistic** if the system also uses stored profile data and purchase history over time

### 5.2 Industry Benchmark Comparison

| Metric | Industry Average | Best-in-Class | Our Target |
|--------|-----------------|---------------|------------|
| Size recommendation accuracy | 60-70% | 80-85% | 85% (aggressive) |
| Return rate reduction | 15-25% | 30-40% | 20% (realistic) |
| User completion rate (photo flow) | 30-50% | 60-70% | 90% (very aggressive) |
| Body measurement accuracy | ±3-5cm | ±1-2cm | Not specified |
| Fit prediction per body area | 55-65% | 70-80% | Not benchmarked |

### 5.3 Confidence Calibration

Our 70% confidence threshold is well-aligned with industry practice:
- Below 50%: essentially random
- 50-70%: directional but unreliable
- 70-85%: commercially useful with disclaimer
- 85%+: high-confidence recommendation

---

## 6. Ethical & Privacy Considerations (Validated)

Our constitution's privacy protections are **well above industry standard**:

| Concern | Industry Norm | Our Approach | Assessment |
|---------|---------------|--------------|------------|
| Photo retention | 24h-30 days | 60 seconds (transient) | Excellent |
| Body data storage | Full profile until deletion | Measurements only; opaque ID | Excellent |
| Minor detection | Rare implementation | Explicit under-16 rejection | Above standard |
| Bias evaluation | Rarely disclosed | Mandated per-demographic tracking | Above standard |
| User transparency | "AI-powered" label | Confidence scores + disclaimer | Above standard |

---

## 7. Recommendations & Impact on Implementation

### 7.1 Critical Architecture Decisions Needed

| # | Decision | Options | Recommendation |
|---|----------|---------|----------------|
| 1 | Body measurement extraction source | Azure OpenAI GPT-4o / MediaPipe + SMPL / Third-party API | **Hybrid**: GPT-4o for estimation + MediaPipe for landmark validation |
| 2 | Height/scale reference | User-provided height / Dual photo / Reference object | **User-provided height** (simplest, most reliable) |
| 3 | Minimum input requirements | Single photo / Dual photo (front+side) / Photo + height | **Single front photo + height input** (balances UX and accuracy) |
| 4 | Cold start garment data | Require full measurements / Infer from size charts / Hybrid | **Require actual measurements** (already in spec — correct) |
| 5 | Accuracy improvement strategy | Static model / Feedback loop / A/B testing | **Feedback loop** from keep/return signals over time |

### 7.2 Impact on Existing Spec

| Area | Current Assumption | Reality | Severity |
|------|-------------------|---------|----------|
| research.md R1 | "Azure AI Vision for body analysis" | Azure AI Vision doesn't do body landmarks | **HIGH** — needs revision |
| spec.md FR-002 | "extract body measurements using computer vision" | Requires custom ML pipeline, not just Azure Vision | MEDIUM — intent is correct, implementation differs |
| plan.md | AzureAIVisionClient wrapper | This client can't extract body landmarks | HIGH — needs architectural rework |
| tasks.md T043 | "body landmark extraction" from Azure AI Vision | API doesn't support this | HIGH — task needs redesign |
| SC-005 | "90% complete flow on first attempt" | Industry best is 60-70% for photo flows | MEDIUM — very aggressive target |
| Data model | No height field on ShopperProfile | Height is required for absolute measurements | MEDIUM — add field |

### 7.3 Revised Technology Recommendation

Replace the Azure AI Vision dependency with:

```text
Photo Input → ImageValidator (our existing pipeline)
     ↓
MediaPipe Pose (containerized) → 33 body landmarks (2D pixel coordinates)
     ↓
Height normalization (user-provided height) → absolute measurements
     ↓
SMPL body model fitting → 3D body shape estimation
     ↓
Measurement extraction → shoulder, chest, waist, hip, inseam
     ↓
FitComparisonEngine (our existing pipeline) → 5-point scale
```

**Alternative (faster to market)**:
```text
Photo + Height → Azure OpenAI GPT-4o Vision
     ↓
Structured output: estimated measurements + confidence
     ↓
FitComparisonEngine → 5-point scale (with lower confidence)
```

---

## 8. Conclusion

| Aspect | Assessment |
|--------|------------|
| **Overall feasibility** | ✅ Proven technology; multiple commercial successes |
| **Our accuracy target (85%)** | ⚠️ Achievable over time with feedback loops; aggressive for day-1 |
| **Return reduction target (20%)** | ✅ Conservative and realistic |
| **Azure AI Vision assumption** | ❌ Does not support body landmarks — architecture change required |
| **5-second latency target** | ✅ Achievable with efficient pipeline |
| **Privacy approach** | ✅ Industry-leading |
| **Commercial viability** | ✅ Strong market demand; growing market |
| **Day-1 user completion (90%)** | ⚠️ Very aggressive; plan for 50-60% initially |

### Bottom Line

The AI fit assessment approach is commercially proven and technically feasible, but our implementation plan has a **critical dependency gap**: Azure AI Vision cannot perform body measurement extraction. The architecture needs revision to use either Azure OpenAI multimodal models (faster path, lower accuracy) or a custom ML pipeline with MediaPipe/SMPL (better accuracy, longer development). Adding a **mandatory height input** to the API contract is also required for absolute measurement derivation.

The 20% return reduction target and multi-tenant B2B model are well-validated by industry precedent. The aggressive 85% accuracy target is achievable at scale with a feedback loop but will likely start at 65-75% accuracy on day 1.

---

## References & Sources

1. Azure AI Vision Image Analysis v4.0 — Microsoft Learn (2025)
2. Azure AI Vision People Detection — Microsoft Learn (2025)
3. Azure Kinect Body Tracking Joints — Microsoft Learn (archived, 2019)
4. SMPL: A Skinned Multi-Person Linear Model — Loper et al., ACM TOG 2015
5. HMR: End-to-end Recovery of Human Shape and Pose — Kanazawa et al., CVPR 2018
6. 3DLOOK YourFit documentation and case studies (2023-2025)
7. Bold Metrics published retail integration results (2024)
8. True Fit Fashion Genome published metrics (2023)
9. Virtual Fitting Room Market Report — Grand View Research (2025)
10. "The State of Fashion Technology" — McKinsey & Company (2024)
11. National Retail Federation: Return rates and cost analysis (2024)
12. MediaPipe Pose estimation documentation — Google (2024)

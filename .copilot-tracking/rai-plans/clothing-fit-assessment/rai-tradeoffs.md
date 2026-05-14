# RAI Tradeoffs: AI Clothing Fit Assessment Agent

**Project Slug**: `clothing-fit-assessment`
**Assessment Date**: 2026-05-14

## Trustworthiness Characteristic Tradeoffs

### Tradeoff 1: Privacy vs. Accuracy (Valid and Reliable ↔ Privacy-Enhanced)

| Dimension | Assessment |
|-----------|-----------|
| **Tension** | Processing photos in-memory with 60s TTL limits the ability to build a validation dataset for accuracy improvement. Retaining photos would improve measurement accuracy benchmarking but violates privacy-by-design principles. |
| **Current choice** | Privacy wins — photos purged within 60s; no persistent image storage without explicit consent |
| **Impact on accuracy** | Cannot build demographic-segmented accuracy baselines from production data; validation must use consented opt-in data or synthetic datasets |
| **Recommendation** | Maintain privacy-first posture. Create a separate, consented opt-in research program for accuracy validation. Use synthetic body images for initial benchmarking. |

### Tradeoff 2: Explainability vs. Performance (Explainable and Interpretable ↔ Valid and Reliable)

| Dimension | Assessment |
|-----------|-----------|
| **Tension** | GPT-5.2 Vision as a black-box LLM provides measurement accuracy (±2–4 cm) but zero explainability of how measurements are derived. A more explainable approach (e.g., explicit landmark detection + geometric calculation) would sacrifice accuracy or require a custom model. |
| **Current choice** | Accuracy wins — GPT-5.2 provides the best available accuracy without requiring custom ML training |
| **Impact on explainability** | Shoppers cannot understand measurement derivation; dispute resolution is difficult without visible reasoning |
| **Recommendation** | Accept black-box extraction for v1. Add measurement confidence annotations per body area. Plan v2 with SMPL model that provides explicit landmark points, improving both accuracy and explainability. |

### Tradeoff 3: Fairness vs. Model Complexity (Fair with Harmful Bias Managed ↔ Valid and Reliable)

| Dimension | Assessment |
|-----------|-----------|
| **Tension** | Achieving demographic accuracy parity may require model fine-tuning, demographic-specific calibration, or ensemble approaches that increase system complexity, cost, and maintenance burden. |
| **Current choice** | Simplicity wins for v1 — single GPT-5.2 model with uniform processing; bias monitoring deferred to post-launch |
| **Impact on fairness** | Unknown accuracy variance across demographics until validated; potential for unequal service quality |
| **Recommendation** | Pre-launch: build diverse validation dataset and measure baseline parity. If >1cm accuracy gap exists between demographic segments, prioritize demographic-aware calibration for v1.1. |

### Tradeoff 4: Safety vs. Utility (Safe ↔ Valid and Reliable)

| Dimension | Assessment |
|-----------|-----------|
| **Tension** | Conservative safety controls (aggressive minor detection, strict image rejection, cautious confidence thresholds) reduce the number of shoppers who receive fit assessments, hurting adoption metrics (SC-005, SC-006). |
| **Current choice** | Safety wins — 70% confidence threshold with disclaimer; under-16 blocking; strict image quality requirements |
| **Impact on utility** | Estimated 30% image rejection rate (SC-006 target); low-confidence disclaimers may reduce shopper trust |
| **Recommendation** | Maintain safety-first for launch. Monitor rejection rate and low-confidence rate in production. Adjust thresholds only with data evidence that safety is maintained. |

### Tradeoff 5: Transparency vs. Intellectual Property (Accountable and Transparent ↔ Secure and Resilient)

| Dimension | Assessment |
|-----------|-----------|
| **Tension** | Full transparency about the measurement extraction prompt, tolerance band algorithms, and model behavior could help adversaries craft manipulated inputs. Opacity protects against adversarial exploitation. |
| **Current choice** | Partial transparency — shoppers see results and confidence but not extraction methodology |
| **Recommendation** | Acceptable balance for v1. Publish a model card documenting accuracy bounds, limitations, and known biases (T144 in tasks.md) without revealing prompt engineering details. |

## Appropriate Reliance Assessment

| Dimension | Assessment |
|-----------|-----------|
| **Over-reliance risk** | Shoppers may treat AI fit recommendation as definitive, purchasing without cross-checking with size charts or reading garment reviews |
| **Under-reliance risk** | Low confidence scores or frequent disclaimers may cause shoppers to abandon the feature entirely |
| **Trust calibration** | Confidence percentage + per-area breakdown provides calibration signals; low-confidence disclaimer with escalation URL supports appropriate reliance |
| **Human-in-the-loop** | Shopper retains full decision authority; recommendation is advisory only; no automated purchasing |
| **Existing controls** | isLowConfidence flag, disclaimer text, escalation URL, model version transparency |
| **Gaps** | No guidance for shoppers on when to trust vs. question the AI; no "how confident should I be?" framing; no comparison with size chart accuracy |
| **Recommendation** | Add contextual framing in API response or frontend SDK: "This recommendation is based on AI measurement extraction and may not be exact. We suggest also checking the size chart for this brand." |

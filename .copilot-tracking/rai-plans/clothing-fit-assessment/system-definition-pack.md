# System Definition Pack: AI Clothing Fit Assessment Agent

**Project Slug**: `clothing-fit-assessment`
**Assessment Date**: 2026-05-14
**Entry Mode**: from-prd
**Framework**: NIST AI Risk Management Framework 1.0

## AI System Overview

### Purpose

Multi-tenant AI-powered clothing fit assessment service that accepts shopper photos, extracts body measurements using computer vision AI, compares them against garment size data, and returns a personalized 5-point fit recommendation per body area. Deployed as a standalone .NET 8 Web API on Azure Container Apps.

### Intended Use Context

- Online shoppers upload a full-body photo and receive fit guidance before purchasing clothing
- Retail partners integrate via B2B API to embed fit assessment in their e-commerce storefronts
- The system augments shopper decision-making; humans retain accountability for purchase decisions
- The system provides confidence-scored recommendations with escalation paths — it supports decisions, never replaces them

### Out-of-Scope Uses (Declared in Architecture)

- Virtual try-on / augmented reality visualization (handled by Zeekit separately)
- Retailer-operated capture endpoints or POS integrations
- Automatic garment data ingestion from supplier feeds (v1)
- Support for non-clothing categories (shoes, accessories)
- Medical body assessment or health diagnosis
- Insurance underwriting or employment screening
- Biometric identification or identity verification
- Social scoring or discriminatory profiling
- Body-shaming, judgmental commentary, or appearance-based categorization

### Prohibited Uses (Derived from Azure OpenAI CoC + Constitution)

| ID | Prohibited Use | Source |
|----|---------------|--------|
| PU-001 | Biometric categorization by protected characteristics (race, ethnicity, gender, religion, sexual orientation) | Azure OpenAI CoC #10 |
| PU-002 | Sensitive attribute inference (gender, race, nationality, religion, specific age) from body photos | Azure OpenAI CoC #11 |
| PU-003 | Emotional state inference from physical characteristics | Azure OpenAI CoC #12 |
| PU-004 | Identity verification or facial recognition from shopper photos | Azure OpenAI CoC #15 |
| PU-005 | Persistent tracking of individuals without valid consent | Azure OpenAI CoC #17 |
| PU-006 | Processing images of minors (under 16) for body measurement | VirtualMirror Constitution III + spec edge case |
| PU-007 | Body-shaming or judgmental statements in any system output | VirtualMirror Constitution III |
| PU-008 | Using shopper photos for model training without anonymization and informed opt-in consent | VirtualMirror Constitution I |
| PU-009 | Sharing raw shopper images with third parties without explicit consent and DPA | VirtualMirror Constitution VII |
| PU-010 | Making consequential decisions without human oversight affecting legal/financial position | Azure OpenAI CoC #5 |

## AI Component Inventory

### Component 1: Azure OpenAI GPT-5.2 Vision

| Attribute | Value |
|-----------|-------|
| **Type** | Multimodal Large Language Model (inference-only) |
| **Provider** | Microsoft Azure OpenAI Service |
| **Training Approach** | Pre-trained by Microsoft/OpenAI; prompt-calibrated (not fine-tuned) for v1 |
| **Role** | Body measurement extraction from shopper photos using height as scale reference |
| **Input** | Photo bytes + height in cm + structured output schema |
| **Output** | JSON: shoulderWidth, chestCircumference, waistCircumference, hipCircumference, inseam, armLength, confidence |
| **Accuracy** | ±2–4 cm (hypothesis H1, under validation) |
| **Autonomy Level** | Automated extraction with confidence scoring; low-confidence results (< 70%) trigger human escalation |
| **Applicable CoC** | Azure OpenAI Service Code of Conduct v4.0 |

### Component 2: Florence-2 (Azure AI Foundry)

| Attribute | Value |
|-----------|-------|
| **Type** | Vision Foundation Model (managed endpoint) |
| **Provider** | Azure AI Foundry |
| **Training Approach** | Pre-trained; used as-is for inference |
| **Role** | Image validation — people detection, bounding box quality check, multi-person rejection |
| **Input** | Photo bytes |
| **Output** | Bounding boxes, person count, detection confidence |
| **Autonomy Level** | Automated gating — rejects invalid images with actionable guidance |
| **Applicable CoC** | To be confirmed — may fall under separate Azure AI Foundry terms |

### Component 3: Azure AI Content Safety

| Attribute | Value |
|-----------|-------|
| **Type** | Content Moderation API |
| **Provider** | Microsoft Azure |
| **Role** | Minor/age detection, inappropriate content filtering |
| **Input** | Photo bytes |
| **Output** | Safety categories with severity scores |
| **Autonomy Level** | Automated blocking — rejects photos of minors and inappropriate content |

### Non-AI Components (Assessment Boundary Exclusions)

- **FitComparisonEngine**: Deterministic algorithm comparing body measurements against garment data using configurable tolerance bands. No ML/AI — pure mathematical comparison
- **Cosmos DB / Blob Storage / Service Bus**: Data infrastructure with no AI behavior
- **Rate Limiting / Authentication**: Standard middleware with no AI components

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Runtime | .NET 8.0 (LTS) / ASP.NET Core Web API |
| Hosting | Azure Container Apps (Linux containers, 3–10 replicas) |
| AI Inference | Azure OpenAI GPT-5.2 Vision, Florence-2 (AI Foundry), Azure AI Content Safety |
| Data | Azure Cosmos DB (multi-tenant, hierarchical partition keys) |
| Storage | Azure Blob Storage (ZRS, transient 60s TTL) |
| Messaging | Azure Service Bus (async overflow queue) |
| Auth | Microsoft Entra ID (OAuth 2.0, B2B) |
| Observability | OpenTelemetry → Azure Monitor |

## Data Flow Summary

```text
Shopper Photo (biometric-adjacent)
  → Blob Storage (transient, 60s TTL, ZRS)
    → Florence-2 (people detection, bounding box)
    → Content Safety (minor detection, content filter)
    → GPT-5.2 Vision (measurement extraction)
      → Derived Measurements (non-biometric)
        → FitComparisonEngine (deterministic)
          → Fit Recommendation (5-point scale per area)
            → Cosmos DB (assessment result, TTL 365d)

Photo purged within 60 seconds. Only derived measurements persist.
```

## Demographic Representation Concerns

Given this is a clothing fit assessment system, bias evaluation is a primary concern across:

| Dimension | Concern |
|-----------|---------|
| **Body types** | Accuracy across different body shapes (hourglass, pear, apple, rectangular, athletic) |
| **Body sizes** | Performance for petite, standard, plus-size, and tall body frames |
| **Skin tones** | Computer vision accuracy across Fitzpatrick scale (I–VI) |
| **Gender presentation** | Accuracy for masculine, feminine, androgynous body presentations |
| **Age groups** | Adult range accuracy (18–70+); minors explicitly excluded |
| **Disabilities** | Accuracy for users with physical disabilities, prosthetics, mobility aids, wheelchairs |
| **Cultural dress** | Impact of clothing worn during photo (head coverings, loose garments, religious attire) |
| **Pregnancy** | Accuracy during pregnancy; system should not make assumptions about body state |

## Assessment Output Preferences

| Setting | Value |
|---------|-------|
| Target audience | Mixed (technical + leadership/compliance) |
| Target backlog system | Both (Azure DevOps + GitHub Issues) |
| Output detail level | Standard |
| Optional artifacts | None (no transparency note, monitoring summary, or artifact signing) |

## Risk Classification Screening

**Completed**: 2026-05-14 | **Depth Tier**: Comprehensive (3/3 indicators activated)

### Prohibited Uses Gate

**Status**: PASS — 10 prohibited uses declared and architecturally enforced. Open item: legal review needed on biometric/functional measurement boundary (Azure OpenAI CoC #10).

### Risk Indicators

| Indicator | Method | Status | Key Concern |
|-----------|--------|--------|-------------|
| Safety & Reliability | Binary | Activated | Psychological harm via body-related AI output; vulnerable populations with body image concerns |
| Rights, Fairness & Privacy | Categorical | Activated | Biometric-adjacent data processing; demographic accuracy parity; GDPR Art. 9 special category data |
| Security & Explainability | Continuous | Activated | Black-box LLM; adversarial attack surface; limited explainability of measurement extraction |

### Depth Tier Assignment

All three indicators activated → **Comprehensive** assessment. Driven by:

1. Biometric-adjacent nature of body photo processing
2. Body-image sensitivity of AI outputs targeting vulnerable populations
3. Demographic fairness requirements across body types, sizes, skin tones
4. Privacy obligations under GDPR Art. 9 and emerging EU AI Act
5. Black-box AI with limited explainability and adversarial attack surface

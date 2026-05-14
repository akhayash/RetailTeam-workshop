# Solution Architecture: AI Clothing Fit Assessment Agent

**Version**: 2.0.0 | **Date**: 2026-05-13 | **Status**: Approved for Implementation

## Executive Summary

Multi-tenant AI-powered clothing fit assessment service that accepts shopper photos with mandatory height input, extracts body measurements using a three-tier Microsoft AI pipeline, compares them against garment size data, and returns a 5-point fit recommendation per body area. Deployed as a standalone .NET 8 Web API on Azure Container Apps.

AI augments shopper decision-making; **humans retain accountability** for purchase decisions. The system provides confidence-scored recommendations with escalation paths — it supports decisions, never replaces them.

---

## Retail Industry Personas

Three personas represent the primary stakeholders affected by the architecture.

### Persona 1: Online Shopper (Frontline / Operational)

| Field | Detail |
|-------|--------|
| **Role** | Consumer browsing an e-commerce clothing store |
| **Goal** | Buy clothes that fit without visiting a physical store |
| **Constraints** | Limited technical knowledge; impatient (< 5s tolerance); privacy-conscious about body photos |
| **Friction** | High return rates (25–40%); size chart confusion across brands; no way to try before buying |
| **How technology helps** | AI copilot extracts body measurements from a single photo and provides per-area fit guidance — reducing guesswork and returns |
| **How technology hinders** | Accuracy concerns erode trust; photo upload friction; privacy anxiety about body images |

### Persona 2: Retail Digital Transformation Leader

| Field | Detail |
|-------|--------|
| **Role** | VP of Digital / E-Commerce at a retail partner |
| **Goal** | Reduce return rates (currently 25–40%), increase conversion, differentiate the online experience |
| **Constraints** | Must integrate with existing e-commerce platform; limited AI/ML team; ROI must be demonstrable within 6 months |
| **Friction** | Legacy catalog systems lack standardized measurement data; organizational resistance to AI-driven features |
| **How technology helps** | API-first integration layer allows embedding fit assessment without rebuilding the storefront; multi-tenant model enables rapid onboarding |
| **How technology hinders** | Measurement accuracy (±2–4 cm) may not satisfy premium/tailored segments; requires garment data standardization effort |

### Persona 3: Risk / Compliance / Privacy Officer

| Field | Detail |
|-------|--------|
| **Role** | Chief Privacy Officer or Data Protection Lead at a retail partner |
| **Goal** | Ensure AI-powered features comply with GDPR, CCPA, and emerging EU AI Act; prevent biometric data exposure |
| **Constraints** | Body photos are biometric-adjacent data; AI must be explainable and auditable; data residency requirements |
| **Friction** | Unclear regulatory classification of body measurement extraction; vendor trust concerns for AI services |
| **How technology helps** | Privacy by design — photos purged < 60s, opaque shopper IDs, no PII in telemetry, DPIA-ready architecture |
| **How technology hinders** | Dependency on Azure OpenAI raises questions about data processing locations and third-party access |

---

## Three Architecture Concept Diagrams

### Concept A: Cloud-Centric Platform Architecture

**Focus**: Modern data foundation, scalable services, governed AI/ML platform, integration backbone.

This is the **primary v1 implementation concept** — a cloud-native API service on Azure with managed AI services, serverless container hosting, and governed multi-tenant data isolation.

```text
┌─────────────────────────────────────────────────────────────────────┐
│                    CLOUD-CENTRIC PLATFORM                           │
│                                                                     │
│  ┌──────────────┐    ┌──────────────────────────────────────────┐  │
│  │  Retail       │    │         Azure Container Apps             │  │
│  │  Frontend     │───▶│  FitAssess API (.NET 8, 2-10 replicas) │  │
│  │  (B2B OAuth)  │    │  ├── Auth Middleware (Entra ID JWT)     │  │
│  │               │    │  ├── Rate Limiting (per tenant tier)    │  │
│  └──────────────┘    │  └── OpenTelemetry (traces + metrics)   │  │
│                       └───────┬──────────┬──────────┬───────────┘  │
│                               │          │          │              │
│  ┌────────────────────────────▼──┐  ┌────▼────┐  ┌─▼────────────┐│
│  │  Azure AI Services (Managed)  │  │Cosmos DB│  │ Blob Storage ││
│  │  ├── AI Vision (Tier 1)       │  │(multi-  │  │ (60s TTL     ││
│  │  ├── Content Safety (Tier 1)  │  │ tenant) │  │  auto-purge) ││
│  │  ├── OpenAI GPT-4o (Tier 2)   │  │         │  │              ││
│  │  └── AI Foundry (Tier 3, v2)  │  └─────────┘  └──────────────┘│
│  └───────────────────────────────┘                                 │
│                                                                     │
│  ┌──────────────┐  ┌─────────────┐  ┌──────────────┐              │
│  │ Service Bus   │  │ Key Vault   │  │ Azure Monitor│              │
│  │ (async queue) │  │ (zero-      │  │ (OTel → AI)  │              │
│  │               │  │  secret)    │  │              │              │
│  └──────────────┘  └─────────────┘  └──────────────┘              │
└─────────────────────────────────────────────────────────────────────┘
```

**Tradeoffs**: Maximum managed-service utilization reduces operational burden but creates vendor lock-in to Azure. Single-region v1 limits geographic reach.

### Concept B: Edge + AI Agent-Enabled Operations

**Focus**: Decisioning at the edge, agentic workflows, human-in-the-loop control, latency- and safety-aware patterns.

This concept extends the platform into **in-store and real-time scenarios** where an AI agent assists shoppers and store associates at the point of decision — fitting rooms, kiosks, and mobile devices.

```text
┌──────────────────────────────────────────────────────────────┐
│                  EDGE + AI AGENT OPERATIONS                   │
│                                                               │
│  ┌──────────────────────┐    ┌─────────────────────────────┐ │
│  │  In-Store Kiosk /     │    │   Store Associate Mobile    │ │
│  │  Fitting Room Camera  │    │   AI Copilot App            │ │
│  │  ├── Local inference  │    │   ├── "This shopper needs   │ │
│  │  │   (pose detection) │    │   │    a size M in slim"    │ │
│  │  ├── Edge caching     │    │   ├── Inventory check       │ │
│  │  │   (garment data)   │    │   └── Suggest alternatives  │ │
│  │  └── Privacy: process │    └─────────────┬───────────────┘ │
│  │      locally, send    │                  │                  │
│  │      only measurements│                  │                  │
│  └──────────┬───────────┘                  │                  │
│             │                               │                  │
│             ▼                               ▼                  │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │            FitAssess API (Cloud Backend)                  │ │
│  │  ├── Full AI pipeline (when edge confidence < threshold) │ │
│  │  ├── Model updates pushed to edge devices                │ │
│  │  └── Aggregated analytics for store operations           │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                               │
│  Human-in-the-Loop: Store associate reviews AI suggestion     │
│  before advising shopper. AI recommends — human decides.      │
└──────────────────────────────────────────────────────────────┘
```

**Agentic AI scenario**: An AI copilot assists the *store associate* by synthesizing *shopper body measurements and garment fit data*, flagging *poor fit areas and low-confidence predictions*, and recommending *alternative sizes or garments* — while the **human associate retains accountability** for the advice given to the shopper.

**Tradeoffs**: Edge inference requires device management and model distribution. Privacy benefits (local processing) offset by hardware investment and synchronization complexity.

### Concept C: Data Fabric / Intelligence Layer

**Focus**: Unified semantic layer, lineage and governance, AI-ready data products powering decisions across domains.

This concept positions the fit assessment data as part of a **unified retail intelligence layer** that connects shopper insights, garment analytics, and return predictions across the entire retail operation.

```text
┌──────────────────────────────────────────────────────────────┐
│              DATA FABRIC / INTELLIGENCE LAYER                 │
│                                                               │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────┐ │
│  │  Shopper     │  │  Garment     │  │  Return & Exchange  │ │
│  │  Measurement │  │  Catalog     │  │  Transaction Data   │ │
│  │  Profiles    │  │  (sizes,     │  │  (outcomes,         │ │
│  │  (anonymized)│  │   materials) │  │   reasons, costs)   │ │
│  └──────┬──────┘  └──────┬───────┘  └──────────┬──────────┘ │
│         │                │                      │             │
│         ▼                ▼                      ▼             │
│  ┌──────────────────────────────────────────────────────────┐│
│  │           Unified Semantic Layer (Microsoft Fabric)       ││
│  │  ├── Data lineage: measurement → assessment → outcome    ││
│  │  ├── Governance: PII classification, retention policies  ││
│  │  ├── AI-ready data products (curated, cataloged)         ││
│  │  └── Cross-domain joins (fit score ↔ return rate)        ││
│  └──────────────────────────────────────────────────────────┘│
│         │                │                      │             │
│         ▼                ▼                      ▼             │
│  ┌──────────────┐ ┌───────────────┐ ┌──────────────────────┐│
│  │  FitAssess   │ │  Return       │ │  Merchandising       ││
│  │  API         │ │  Prediction   │ │  Intelligence        ││
│  │  (real-time  │ │  Model        │ │  (size distribution, ││
│  │   assessment)│ │  (batch/ML)   │ │   trend analysis)    ││
│  └──────────────┘ └───────────────┘ └──────────────────────┘│
│                                                               │
│  Fabric IQ: Trusted data foundation enables AI models and     │
│  business intelligence to operate on the same governed data.  │
└──────────────────────────────────────────────────────────────┘
```

**Tradeoffs**: Requires Microsoft Fabric investment and data engineering effort beyond the fit assessment scope. Maximum long-term value but slower time-to-insight for v1.

---

## Persona-Driven AI Scenarios

### Scenario 1: Online Shopper + AI Fit Assessment (Concept A)

> "An AI copilot that assists the **online shopper** by synthesizing **a single photo and self-reported height into body measurements**, flagging **low-confidence predictions and poor fit areas**, and recommending **the best size with per-area fit breakdown** — while the **shopper retains accountability** for the purchase decision."

| Element | Detail |
|---------|--------|
| **What the AI agent does** | Extracts body measurements from photo; compares against garment data; produces 5-point fit scale per body area |
| **Decisions it supports** | Size selection; whether to purchase or look for alternatives |
| **Human-AI collaboration** | AI provides confidence-scored recommendation; shopper decides whether to trust it or consult size chart |
| **New interfaces** | Fit assessment widget embedded in product page; visual per-area fit overlay |

### Scenario 2: Store Associate + AI Copilot (Concept B)

> "An AI copilot that assists the **store associate** by synthesizing **real-time shopper measurements and inventory data**, flagging **fit issues before the shopper tries the garment on**, and recommending **alternative sizes and similar-fit items in stock** — while the **associate retains accountability** for styling advice."

| Element | Detail |
|---------|--------|
| **What the AI agent does** | Captures measurements via fitting room camera; cross-references in-store inventory; suggests alternatives |
| **Decisions it supports** | Which sizes to pull for try-on; which alternative garments to suggest |
| **Human-AI collaboration** | AI pre-filters options; associate uses judgment and shopper preferences to make final recommendation |
| **New roles** | "AI-Assisted Stylist" — store associate armed with real-time fit intelligence |

### Scenario 3: Merchandising Analyst + Intelligence Layer (Concept C)

> "An AI copilot that assists the **merchandising analyst** by synthesizing **fit assessment outcomes, return data, and size distribution trends**, flagging **garments with high return-due-to-fit rates**, and recommending **size chart adjustments and inventory rebalancing** — while the **analyst retains accountability** for catalog decisions."

| Element | Detail |
|---------|--------|
| **What the AI agent does** | Correlates fit assessment confidence with actual return outcomes; identifies size chart inaccuracies; models inventory impact |
| **Decisions it supports** | Size chart corrections; garment redesign priorities; inventory allocation across sizes |
| **Human-AI collaboration** | AI surfaces patterns and anomalies; analyst validates against supplier relationships and business constraints |
| **New interfaces** | Merchandising dashboard with fit-informed analytics; automated size chart drift alerts |

---

## C-Suite Relevance — "So What?"

### CIO / VP of Technology

| Concept | Value Proposition |
|---------|-------------------|
| **A. Cloud-Centric Platform** | Modernize the sizing experience with a scalable, API-first AI platform that integrates into any storefront without rebuilding infrastructure. Managed Azure services minimize operational overhead. |
| **B. Edge + AI Agent** | Extend digital capabilities into physical stores. Edge inference preserves shopper privacy while reducing cloud dependency for latency-sensitive scenarios. |
| **C. Data Fabric** | Unify fragmented retail data (fit, returns, inventory) into a governed intelligence layer that powers AI models across the entire business — not just one feature. |

### Business / Operations Leader (VP of E-Commerce)

| Concept | Value Proposition |
|---------|-------------------|
| **A. Cloud-Centric Platform** | Reduce return rates by 20–30% ($2–6M annual savings for mid-size retailer). Increase conversion through purchase confidence. Measurable ROI within 6 months. |
| **B. Edge + AI Agent** | Elevate the in-store experience — associates armed with AI-driven fit intelligence spend less time on size runs and more time on relationship selling. |
| **C. Data Fabric** | Turn return data from a cost center into a strategic asset. Fit-informed merchandising decisions reduce overstock and optimize size curve purchasing. |

### Risk / Compliance / Sustainability Leader

| Concept | Value Proposition |
|---------|-------------------|
| **A. Cloud-Centric Platform** | Privacy by design — photos purged in < 60s, opaque identities, DPIA-ready. AI transparency via confidence scores and escalation paths. Audit trail for every assessment. |
| **B. Edge + AI Agent** | Local photo processing eliminates cloud transmission of body images. Strongest privacy posture. Compliant with strictest data residency requirements. |
| **C. Data Fabric** | Full data lineage from measurement to outcome. PII classification labels. Retention policies enforced at the platform level. Supports regulatory reporting (GDPR Article 30). |

---

## Business Value Driver Mapping

| Value Driver | Technology Capability | Alignment |
|-------------|----------------------|-----------|
| **Decision Velocity & Confidence** | GPT-4o Vision structured output; 5-point fit scale; confidence scoring; < 5s assessment | Shoppers make faster, more confident purchase decisions. Retailers see fewer returns and higher conversion. |
| **Workforce Productivity & Focus** | API-first integration; profile reuse; batch garment ingestion; async queuing | Retail ops teams onboard faster. Shoppers skip repeat photo uploads. Store associates focus on selling, not size guessing. |
| **Operational Resilience & Risk** | Multi-AZ deployment; circuit breakers; graceful degradation; 60s image purge; audit trail | 99.9% availability SLO. Regulatory compliance built-in. AI failures degrade gracefully to size chart fallback. |
| **Growth Enablement & Innovation** | Multi-tenant architecture; v2 custom model path; Data Fabric integration; edge expansion | New retail partners onboard via API. Architecture supports evolution from single feature to retail intelligence platform. |

### IQ Framework Alignment

| IQ Layer | How It Manifests |
|----------|-----------------|
| **Work IQ** | Intelligence embedded in the shopper's daily workflow — fit recommendations appear at the point of purchase decision, not in a separate tool. Store associates receive AI suggestions in their mobile workflow. |
| **Foundry IQ** | Azure OpenAI GPT-4o Vision and the three-tier AI pipeline create insights (body measurements, fit scores, confidence) from raw inputs (photos, height). Prompt engineering and model versioning enable continuous refinement. |
| **Fabric IQ** | Cosmos DB with hierarchical partition keys, Blob Storage lifecycle policies, and audit trails form the governed data foundation. Concept C extends this into Microsoft Fabric for cross-domain analytics. |

---

## System Context

```text
┌─────────────────────────────────────────────────────────────────────┐
│                        Retail Frontend Store                        │
│  (e-commerce storefront — owns shopper auth, passes opaque refs)   │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ REST API (OAuth 2.0 B2B)
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     FitAssess API (v1)                               │
│  ASP.NET Core 8.0 · Azure Container Apps · Multi-tenant             │
│                                                                     │
│  ┌───────────┐  ┌──────────────┐  ┌────────────┐  ┌─────────────┐ │
│  │ Assessments│  │   Profiles   │  │  Garments  │  │   Health    │ │
│  │ Controller │  │  Controller  │  │ Controller │  │ Controller  │ │
│  └─────┬─────┘  └──────┬───────┘  └─────┬──────┘  └─────────────┘ │
│        │               │                │                           │
│  ┌─────▼───────────────▼────────────────▼──────────────────────┐   │
│  │                    Service Layer                             │   │
│  │  FitAssessmentService · ImageValidator · BodyMeasurement-   │   │
│  │  Extractor · FitComparisonEngine · ShopperProfileService ·  │   │
│  │  GarmentService                                             │   │
│  └─────┬───────────────────────────────────────────────────────┘   │
│        │                                                            │
│  ┌─────▼───────────────────────────────────────────────────────┐   │
│  │                  Infrastructure Layer                        │   │
│  │  AzureAIVisionClient · ContentSafetyClient · AzureOpenAI-  │   │
│  │  MeasurementClient · CosmosRepository<T> · BlobStorage-     │   │
│  │  Service · AssessmentQueueService · AuditLogger             │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
         │              │              │              │
         ▼              ▼              ▼              ▼
   ┌──────────┐  ┌───────────┐  ┌──────────┐  ┌──────────────┐
   │ Azure AI │  │  Azure    │  │ Azure    │  │   Azure      │
   │ Services │  │ Cosmos DB │  │ Blob     │  │ Service Bus  │
   │          │  │           │  │ Storage  │  │              │
   └──────────┘  └───────────┘  └──────────┘  └──────────────┘
```

## Three-Tier AI Pipeline (Concept A Detail)

```text
┌──────────────────────────────────────────────────────────────────┐
│  TIER 1 — Validation                                             │
│                                                                  │
│  ┌─────────────────────┐    ┌──────────────────────────────┐    │
│  │ Azure AI Vision 4.0 │    │ Azure AI Content Safety      │    │
│  │ • People detection   │    │ • Minor/age detection        │    │
│  │ • Multi-person reject│    │ • Inappropriate content      │    │
│  │ • Bounding box check │    │ • Malware scan (Defender)    │    │
│  └─────────┬───────────┘    └──────────────┬───────────────┘    │
│            │ PASS                           │ PASS               │
│            └───────────────┬────────────────┘                    │
│                            ▼                                     │
├──────────────────────────────────────────────────────────────────┤
│  TIER 2 — Measurement Extraction                                 │
│                                                                  │
│  ┌──────────────────────────────────────────────────────┐       │
│  │ Azure OpenAI GPT-4o Vision (Structured Output)       │       │
│  │ Input: Photo (bytes) + Height (cm)                   │       │
│  │ Output: { shoulderWidth, chestCircumference,         │       │
│  │           waistCircumference, hipCircumference,      │       │
│  │           inseam, armLength, confidence }             │       │
│  │ Prompt: version-controlled at Prompts/ directory     │       │
│  └──────────────────────────────────────────────────────┘       │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│  TIER 3 — Future (v2)                                            │
│                                                                  │
│  ┌──────────────────────────────────────────────────────┐       │
│  │ Custom SMPL Body Model on Azure AI Foundry            │       │
│  │ • ±1-2cm accuracy (vs ±2-4cm from GPT-4o)           │       │
│  │ • Deterministic output                               │       │
│  │ • Managed endpoint deployment                        │       │
│  └──────────────────────────────────────────────────────┘       │
└──────────────────────────────────────────────────────────────────┘
```

## Fit Comparison Engine

```text
For each body area:
  delta = shopper_measurement - garment_measurement

  Too Tight:      delta < -tight_threshold
  Slightly Tight: -tight_threshold ≤ delta < -comfort_threshold
  Good Fit:       -comfort_threshold ≤ delta ≤ +comfort_threshold
  Slightly Loose: +comfort_threshold < delta ≤ +loose_threshold
  Too Loose:      delta > +loose_threshold

  Overall recommendation = worst-scoring area (conservative)
  Confidence = min(extraction_confidence, measurement_coverage_%)
```

Tolerance bands are configurable per tenant and garment category. System defaults: tight 4 cm, comfort 2 cm, loose 5 cm.

## Azure Service Map

| Service | Purpose | SKU (prod) |
|---------|---------|------------|
| Azure Container Apps | API host (2–10 replicas, multi-AZ) | Consumption |
| Azure Cosmos DB | Multi-tenant document store (hierarchical partition keys) | Autoscale 400–4000 RU/s |
| Azure Blob Storage | Transient image processing (60s TTL auto-purge) | Standard LRS |
| Azure OpenAI | GPT-4o Vision for body measurement extraction | Standard S0 |
| Azure AI Vision 4.0 | People detection and bounding box validation | Standard S1 |
| Azure AI Content Safety | Minor detection, inappropriate content filter | Standard S0 |
| Azure Service Bus | Async assessment queuing under high load | Standard |
| Microsoft Entra ID | OAuth 2.0 / OIDC (B2B tenant auth + managed identity) | — |
| Azure Key Vault | Secrets, certificates, encryption keys | Standard |
| Azure App Configuration | Feature flags for progressive rollouts | Standard |
| Azure Monitor | OpenTelemetry traces, metrics, logs, alerts | Log Analytics workspace |

## Multi-Tenant Data Architecture

```text
Cosmos DB Account
│
├── Database: fitassess
│   │
│   ├── Container: tenants
│   │   Partition key: /id
│   │   Entities: Tenant configuration, tolerance bands, rate limit tiers
│   │
│   ├── Container: garments
│   │   Partition key: /tenantId
│   │   Entities: Garment SKUs with per-size measurements (versioned)
│   │
│   ├── Container: profiles
│   │   Partition key: /tenantId
│   │   Entities: Shopper body measurements (derived, not photos)
│   │   Deletion: Hard delete within 24h of request
│   │
│   ├── Container: assessments
│   │   Partition key: /tenantId
│   │   Entities: Fit assessment results with model version traceability
│   │   TTL: 365 days (configurable per tenant)
│   │
│   └── Container: audit
│       Partition key: /tenantId
│       Entities: Immutable audit log entries (tamper-evident)
│
└── Hierarchical partition keys: /tenantId → /entityType → /entityId
```

**Isolation guarantee**: Repository base class enforces tenant scoping on every query. Queries without tenant context fail at compile time via generic constraints.

## Assessment Request Flow

```text
1. Frontend sends POST /api/v1/assessments
   (shopperRef, garmentId, sizeLabel, heightCm, image, saveProfile?)
                          │
2. Middleware pipeline     │
   ├── JWT validation (Entra ID)
   ├── Tenant extraction from claims
   ├── Correlation ID injection
   ├── Rate limit check (per tenant tier)
   └── Request validation (FluentValidation)
                          │
3. FitAssessmentService   │
   ├── Check load → if queue depth > 50 or p95 > 4s:
   │     enqueue to Service Bus, return HTTP 202 + poll URL
   │
   ├── Upload image to Blob (if > 4 MB) or stream in-memory
   │
   ├── TIER 1: Validate image
   │   ├── Azure AI Vision: people detection, multi-person reject,
   │   │   bounding box ≥ 70% frame height
   │   ├── Content Safety: minor detection, inappropriate content
   │   ├── Malware scan (Defender for Storage)
   │   └── Local checks: format, size, MIME type, luminance ≥ 40
   │
   ├── TIER 2: Extract measurements
   │   ├── Azure OpenAI GPT-4o Vision (structured JSON output)
   │   ├── Input: photo bytes + heightCm as scale reference
   │   └── Output: body measurements + confidence score
   │
   ├── Compare measurements vs garment data (FitComparisonEngine)
   │   ├── Per-area 5-point scale using tolerance bands
   │   └── Overall = worst-scoring area (conservative)
   │
   ├── If confidence < 70%: attach disclaimer + escalation URL
   │
   ├── Audit log: model version, tenant, shopperRef, correlationId
   │
   ├── If saveProfile=true: persist measurements to profiles container
   │
   └── Purge image from Blob (< 60s TTL enforced by lifecycle policy)
                          │
4. Return FitAssessmentResponse (200)
   or FallbackResponse (503) if AI unavailable
```

## Network and Security Architecture

```text
┌──────────────────────────────────────────────────────┐
│  Internet                                             │
│                                                       │
│  Frontend Store ──── TLS 1.2+ ────┐                  │
│                                    │                  │
│                          ┌─────────▼──────────┐      │
│                          │  ACA Ingress        │      │
│                          │  (HTTPS only)       │      │
│                          └─────────┬──────────┘      │
│                                    │                  │
│  ┌─────────────────────────────────▼───────────────┐ │
│  │  Container Apps Environment (multi-AZ)          │ │
│  │                                                  │ │
│  │  ┌──────────────────────────────────────┐       │ │
│  │  │  FitAssess API (2-10 replicas)       │       │ │
│  │  │  • Managed Identity (no secrets)     │       │ │
│  │  │  • Entra ID JWT validation           │       │ │
│  │  │  • Rate limiting middleware          │       │ │
│  │  └──────┬────────┬───────┬──────────────┘       │ │
│  │         │        │       │                       │ │
│  └─────────┼────────┼───────┼───────────────────────┘ │
│            │        │       │                          │
│  ┌─────────▼──┐ ┌───▼────┐ ┌▼──────────────────────┐ │
│  │ Cosmos DB  │ │Key Vault│ │ Azure AI Services     │ │
│  │ (private   │ │(private │ │ (managed identity     │ │
│  │  endpoint) │ │endpoint)│ │  authentication)      │ │
│  └────────────┘ └────────┘ └────────────────────────┘ │
└──────────────────────────────────────────────────────┘
```

**Zero-trust model**: Every service call authenticated via managed identity. No shared secrets. Private endpoints for data services.

## API Contract Summary

| Endpoint | Method | Purpose | Auth |
|----------|--------|---------|------|
| `/api/v1/assessments` | POST | Create fit assessment from photo | FitAssess.Write |
| `/api/v1/assessments/{id}` | GET | Retrieve previous assessment | FitAssess.Read |
| `/api/v1/assessments/by-profile` | POST | Assessment from saved profile | FitAssess.Write |
| `/api/v1/profiles/{shopperRef}` | GET | Retrieve measurement profile | FitAssess.Read |
| `/api/v1/profiles/{shopperRef}` | DELETE | Delete profile (24h fulfillment) | FitAssess.Write |
| `/api/v1/garments` | POST | Upsert garment data | FitAssess.Write |
| `/api/v1/garments` | GET | List garments (paginated) | FitAssess.Read |
| `/api/v1/garments/batch` | POST | Bulk upsert (max 100) | FitAssess.Write |
| `/api/v1/health` | GET | Health check | None |

Full contract: [openapi.yaml](../specs/001-clothing-fit-assessment/contracts/openapi.yaml)

## Project Structure

```text
src/
├── FitAssess.Api/              # ASP.NET Core Web API host
├── FitAssess.Core/             # Domain models & interfaces (zero dependencies)
├── FitAssess.Services/         # Business logic
├── FitAssess.Infrastructure/   # Azure SDK integrations
└── FitAssess.AppHost/          # .NET Aspire orchestrator

tests/
├── FitAssess.Api.Tests/        # Integration (WebApplicationFactory)
├── FitAssess.Core.Tests/       # Unit (domain logic)
├── FitAssess.Services.Tests/   # Unit (services)
├── FitAssess.Infrastructure.Tests/  # Integration (external deps)
├── FitAssess.Contract.Tests/   # OpenAPI contract validation
└── FitAssess.Load.Tests/       # NBomber performance

infra/
├── main.bicep                  # Root deployment
├── modules/                    # Per-resource Bicep modules
└── parameters/                 # dev.json, staging.json, prod.json
```

**Architecture pattern**: Clean Architecture (Api → Services → Core ← Infrastructure). Core has zero external dependencies. Infrastructure depends on Core interfaces only.

## Deployment Pipeline

```text
Push to feature branch
  │
  ├── Lint + Build
  ├── Unit Tests + Integration Tests
  ├── Contract Tests (OpenAPI validation)
  ├── SAST + SCA (dependency scan)
  ├── Code Coverage Gates (≥ 80% business, ≥ 90% critical)
  ├── SBOM Generation (CycloneDX)
  ├── Container Build + Trivy Scan + Notation Sign
  │
  ├── Deploy to Staging
  ├── DAST Scan (OWASP ZAP)
  ├── E2E Smoke Tests
  │
  └── Deploy to Production (manual gate)
      ├── Canary rollout via feature flags
      └── Azure Monitor alerts for regression detection
```

**Environments**: dev → staging → production (identical Bicep, differing only in scale and secrets).

## SLOs and Operational Targets

| Metric | Target | Monitoring |
|--------|--------|------------|
| Availability | 99.9% monthly | Azure Monitor |
| API latency (p95) | < 2 seconds | OpenTelemetry + alerts |
| End-to-end assessment (p95) | < 5 seconds | NBomber validation |
| Concurrent capacity | 500 requests | Auto-scale 2–10 replicas |
| Error rate (5xx) | < 0.1% | Azure Monitor alert |
| Image purge compliance | < 60 seconds | Blob lifecycle + audit |
| Data deletion fulfillment | < 24 hours | Audit log verification |
| RPO | < 1 hour | Cosmos DB continuous backup |
| RTO | < 30 minutes | Multi-AZ failover |

## Key Constraints

- **Single-region v1**: Multi-region deferred; architecture supports future expansion
- **No PII storage**: Service stores measurements only; raw photos purged within 60 seconds
- **Opaque shopper identity**: Frontend owns shopper auth; service receives only hashed reference
- **Mandatory height input**: Required for absolute measurement derivation from 2D photos (100–250 cm)
- **GPT-4o accuracy**: ±2–4 cm estimated; v2 custom model targets ±1–2 cm
- **70% confidence threshold**: Below this, system returns disclaimer + escalation URL + size chart fallback

## Key Tradeoffs

Tradeoffs are named explicitly per the workshop quality bar — not hidden behind decisions.

| Tradeoff | Choice Made | What We Gain | What We Accept |
|----------|-------------|-------------|----------------|
| GPT-4o Vision vs custom model | GPT-4o for v1; custom SMPL for v2 | Rapid time-to-market; no ML team required for v1 | ±2–4 cm accuracy (vs ±1–2 cm); non-deterministic output |
| Mandatory height input vs reference object | Require shopper-reported height | Reliable scale reference for all measurements | Added UX friction; accuracy depends on self-reported honesty |
| Cloud-only vs edge processing | Cloud-only for v1; edge exploration for v2 | Simpler architecture; no device management | Cannot serve in-store scenarios; requires network connectivity |
| Single-region vs multi-region | Single-region v1 | Lower cost and complexity | Geo-redundancy deferred; higher latency for distant shoppers |
| Middleware rate limiting vs APIM | ASP.NET Core middleware for v1 | No additional infrastructure cost | Per-instance state (not distributed); limited gateway analytics |
| Worst-area scoring vs weighted average | Conservative worst-area approach | Fewer false "good fit" recommendations; builds trust | More "too tight/loose" results; may reduce conversion initially |
| Azure vendor lock-in vs multi-cloud | Azure-native stack (Cosmos, ACA, OpenAI) | Deepest integration; managed identity; unified billing | Migration to other clouds requires significant rework |

## Hypothesis Register

Key assumptions that must be validated during implementation. Per workshop quality bar: every claim labeled as hypothesis or verified.

| ID | Hypothesis | Validation Method | Risk if Wrong |
|----|-----------|-------------------|---------------|
| H1 | GPT-4o Vision can extract body measurements within ±2–4 cm using height as scale | Ground-truth comparison with known measurements (T043b spike) | Core value proposition fails; escalate to Tier 3 or third-party API |
| H2 | 70% confidence threshold balances accuracy vs coverage | A/B testing with shopper feedback and return data | Too high → low coverage; too low → inaccurate recommendations |
| H3 | 4 MB in-memory streaming threshold avoids memory pressure | Load testing at 500 concurrent requests (NBomber) | OOM under load; lower threshold or always use Blob Storage |
| H4 | Tolerance band defaults (tight: 4, comfort: 2, loose: 5 cm) produce meaningful fit ratings | Comparison with industry size charts and garment supplier feedback | Misaligned ratings lead to shopper distrust |
| H5 | Auto-scaling threshold of 50 concurrent HTTP requests is optimal | Load testing with production-like traffic patterns | Under-provisioned → latency spikes; over-provisioned → wasted cost |
| H6 | Image rejection rate stays below 30% (SC-006) | Production monitoring in first 30 days | UX friction; shoppers abandon the feature |

# Research: AI Clothing Fit Assessment Agent

**Phase**: 0 — Research & Technology Decisions
**Date**: 2026-05-13
**Feature**: [spec.md](spec.md)

> **Confidence labeling**: Each claim below is marked **[Verified]** (confirmed via documentation or testing) or **[Hypothesis]** (inferred from public information, not yet validated). Treat hypotheses as directional — validate during implementation.

---

## Owners → Domains (Retail Partner Organization)

Mapping of typical retail partner executive roles to the architectural areas they influence.

| Role | Architectural Domain | Relevance to Fit Assessment |
|------|---------------------|----------------------------|
| VP of E-Commerce / Digital | Frontend integration, shopper UX, conversion metrics | Primary stakeholder for API integration and fit widget embedding |
| CTO / VP of Engineering | Platform architecture, cloud strategy, AI/ML adoption | Owns technical evaluation, SLA requirements, and build-vs-buy decisions |
| Chief Privacy Officer / DPO | Data governance, GDPR/CCPA, biometric data classification | Approves data processing approach; validates 60s image purge and PII controls |
| VP of Merchandising | Garment catalog, size charts, return analytics | Provides garment measurement data; consumes fit-informed merchandising insights |
| VP of Store Operations | In-store technology, associate workflows, inventory | Stakeholder for Concept B (Edge + AI Agent); owns associate enablement |

---

## Emerging Retail Architecture Patterns

Modern reference architectures and design patterns emerging in the retail industry.

| Pattern | Relevance | Adoption Status |
|---------|-----------|-----------------|
| **Composable Commerce** (MACH Alliance) | API-first, microservices, cloud-native, headless — aligns with our standalone API approach | **[Verified]** — industry standard; adopted by Shopify, commercetools, Salesforce Commerce Cloud |
| **Unified Commerce Data Fabric** | Single governed data layer across online, in-store, and supply chain — aligns with Concept C | **[Hypothesis]** — Microsoft Fabric emerging but retail adoption is early-stage |
| **AI-Augmented Sizing** (virtual try-on) | 2D photo → body measurement → fit recommendation — our exact approach | **[Verified]** — proven by 3DLOOK, Bold Metrics, True Fit; 20–40% return reduction reported |
| **Edge AI for Retail** | On-device inference for fitting rooms, smart mirrors, kiosks — aligns with Concept B | **[Hypothesis]** — pilots at Nike, Amazon Go, Zara; not yet mainstream for body measurement |
| **Agentic AI in Retail** | AI agents that synthesize data and recommend actions while humans decide — aligns with our human-in-the-loop model | **[Hypothesis]** — early adoption in customer service; body measurement agents are novel |

---

## R1: Body Measurement Extraction from Photos

> **⚠️ SUPERSEDED**: This research informed [ADR-001](../../docs/architecture/decision-register.md#adr-001-body-measurement-extraction-approach). The final architecture uses **Florence-2 on Azure AI Foundry** (Tier 1, replacing Azure AI Vision 4.0) and **Azure OpenAI GPT-5.2 Vision** (Tier 2, replacing GPT-4o which retired March 2026). See the decision register and [solution-architecture.md](../../docs/architecture/solution-architecture.md) for the current design.

**Decision**: Three-tier Microsoft AI pipeline — Florence-2 on Azure AI Foundry (validation) + Azure OpenAI GPT-5.2 Vision (measurement extraction) + Azure AI Content Safety (content moderation)

**Rationale**: Azure AI Vision 4.0 provides people detection (bounding boxes, multi-person detection) but does NOT provide body landmark extraction or pose estimation **[Verified]** — confirmed via Azure AI Vision 4.0 API documentation (May 2026). This led to its replacement by Florence-2 on Azure AI Foundry (per ADR-001), which provides equivalent detection capabilities within the AI Foundry ecosystem without the September 2028 retirement risk. Azure OpenAI GPT-5.2 Vision (successor to GPT-4o, retired March 2026) provides native structured output with JSON schema validation for measurement extraction, using mandatory height input as scale reference **[Hypothesis]** — accuracy (±2–4 cm under validation, expected improvement with GPT-5.2) inferred from analogous multimodal tasks; requires validation with ground-truth measurement datasets. Azure AI Content Safety provides minor detection and inappropriate content filtering **[Verified]** — GA feature. All services are first-party Microsoft, integrated via Azure AI Foundry.

**Why not Azure AI Vision alone**: Azure AI Vision 4.0 only returns people bounding boxes and confidence scores — it cannot extract body landmarks, skeleton joints, or anthropometric measurements. Azure Kinect Body Tracking (32-joint skeleton) requires physical depth-camera hardware and is not available as a cloud API. Azure AI Vision is also being deprecated (retiring September 2028).

**Alternatives considered**:
- **Azure AI Vision Custom Model**: Only supports object detection/classification, not body measurement extraction. Cannot be trained to output centimeter measurements from 2D images. Rejected.
- **MediaPipe Pose (Google, containerized)**: Open-source 33-landmark body pose estimation. Strong accuracy for 2D landmark detection but requires self-hosting, GPU management, and SMPL body model integration for 3D measurement derivation. Stack misalignment (Google library). Considered as v2 enhancement layer.
- **Custom SMPL body model on Azure AI Foundry**: Maximum accuracy (±1-2cm) but requires 3-6 months development, training data collection, and ML expertise. Planned for v2 — hosted as Azure AI Foundry managed endpoint.
- **Third-party API (3DLOOK, Bold Metrics)**: Proven commercial accuracy but adds external dependency, per-call cost, and data privacy concerns (sending shopper photos to third party). Rejected per constitution (VII. Data Minimization).

**Architecture (three tiers)**:

```text
Tier 1 — Validation (Florence-2 on Azure AI Foundry):
  Photo → People Detection → multi-person rejection, bounding box quality check
  Photo → Azure AI Content Safety → minor detection, inappropriate content filter

Tier 2 — Measurement Extraction (Azure OpenAI GPT-5.2 Vision):
  Photo + Height (cm) → GPT-5.2 native structured output (JSON schema) →
    { shoulderWidth, chestCircumference, waistCircumference,
      hipCircumference, inseam, armLength, confidence }
  Height is the mandatory scale reference (no absolute measurements without it)

Tier 3 — Future Enhancement (Azure AI Foundry, v2):
  Custom SMPL body model trained on measurement datasets →
    Higher accuracy (±1-2cm vs ±2-4cm from GPT-5.2)
    Deterministic output (vs non-deterministic LLM)
    Deployed as Azure AI Foundry managed endpoint
```

**Key design decisions**:
1. **Mandatory height input** **[Verified]**: From a 2D photo alone, it is impossible to determine absolute body dimensions. Height (user-provided in cm) serves as the scale reference for all other measurements.
2. **Structured output mode** **[Verified]**: Azure OpenAI GPT-5.2 supports native structured output with JSON schema validation, ensuring consistent measurement output format.
3. **Confidence calibration** **[Hypothesis]**: GPT-5.2's self-reported confidence is calibrated against known measurement datasets during integration testing. Low-confidence results (< 70%) trigger the fallback path. Calibration accuracy TBD.
4. **Model versioning** **[Verified]**: Each GPT-5.2 model deployment is version-pinned and tracked per assessment for audit traceability.
5. **Prompt engineering** **[Verified]**: The measurement extraction prompt is version-controlled, tested, and treated as a code artifact — not an ad-hoc string.

**Implementation approach**:
1. Use Florence-2 on Azure AI Foundry for image validation (people detection, multi-person rejection, bounding box quality)
2. Use Azure AI Content Safety for minor/age detection and inappropriate content filtering
3. Use Azure OpenAI GPT-5.2 Vision with native structured output for body measurement extraction, using height as scale reference
4. Derive confidence from GPT-5.2's self-assessment + image quality metrics from Tier 1
5. FitComparisonEngine compares extracted measurements against garment data (unchanged — deterministic delta calculation)
6. v2 path: Deploy custom SMPL body model on Azure AI Foundry for improved accuracy

---

## R2: Multi-Tenant Data Isolation in Cosmos DB

**Decision**: Partition key strategy using hierarchical partition keys (tenant ID + entity type)

**Rationale**: Azure Cosmos DB supports hierarchical partition keys (GA since 2023) **[Verified]**, enabling efficient multi-tenant data isolation without separate databases per tenant. Data is physically co-located per tenant for query performance while maintaining logical isolation **[Verified]** — confirmed via Cosmos DB documentation. Row-level security is enforced at the application layer via the repository pattern.

**Alternatives considered**:
- **Database-per-tenant**: Maximum isolation but expensive at scale and complex to manage. Rejected for v1 (< 50 tenants expected).
- **Container-per-tenant**: Good isolation but partition key management becomes complex. Rejected — hierarchical keys achieve equivalent isolation with less overhead.
- **Shared container with tenant ID filter**: Simplest but risk of cross-tenant data leakage if filter is missed. Rejected — hierarchical partition keys provide the same simplicity with physical isolation guarantees.

**Implementation approach**:
1. Hierarchical partition key: `/tenantId` → `/entityType` → `/entityId`
2. Repository base class enforces tenant scoping on all queries
3. Tenant context injected via middleware from authenticated JWT claims
4. Cosmos DB throughput provisioned at database level with autoscale (400–4000 RU/s)

---

## R3: Image Processing Pipeline & Transient Storage

**Decision**: Azure Blob Storage with lifecycle management (auto-delete after 60 seconds) + in-memory streaming

**Rationale**: Images must be uploaded to a temporary location for AI processing. Both Florence-2 (people detection) and Azure OpenAI GPT-5.2 Vision (measurement extraction) accept image byte streams or URLs **[Verified]** — both services accept byte arrays. Using Azure Blob Storage with a 1-minute lifecycle policy ensures automatic purging **[Verified]** — Blob Storage lifecycle management is GA. For images under 4 MB, direct byte stream to the AI endpoints avoids blob storage entirely **[Hypothesis]** — 4 MB threshold based on estimated memory pressure; validate under load testing.

**Alternatives considered**:
- **In-memory only**: Ideal for privacy but large images (up to 10 MB) risk memory pressure under concurrent load when streamed to multiple AI services (Florence-2 + GPT-5.2 + Content Safety). Hybrid approach chosen.
- **Azure Queue + background processing**: Adds latency and complexity. Rejected — synchronous processing meets the 5-second SLA.
- **Disk-based temp files in container**: Ephemeral but harder to audit and purge reliably. Rejected.

**Implementation approach**:
1. Images ≤ 4 MB: Stream directly to AI services in-memory (no blob storage)
2. Images > 4 MB: Upload to transient blob container with 60-second TTL, pass SAS URL to AI endpoints, confirm deletion after processing
3. Blob container has immutable lifecycle policy preventing TTL modification
4. Audit log entry written on upload and deletion for compliance

---

## R4: Authentication & Authorization Architecture

**Decision**: Microsoft Entra ID with app registrations per tenant + managed identity for service-to-service

**Rationale**: Entra ID provides enterprise-grade OAuth 2.0 / OIDC with native support for multi-tenant app registrations **[Verified]**. Each retail partner (tenant) gets a registered app with client credentials. The fit assessment service uses managed identity for accessing Azure resources (Cosmos DB, Blob Storage, Key Vault, AI services), eliminating secret management **[Verified]** — managed identity supported across all target Azure services.

**Alternatives considered**:
- **API key-based auth**: Simpler but doesn't support token expiration, refresh, or fine-grained scopes. Rejected per constitution (II. Security First).
- **Azure API Management with subscription keys**: Good for rate limiting but adds infrastructure complexity and cost for v1. Rejected for MVP — ASP.NET Core middleware handles rate limiting per tenant tier. Can be introduced in v2 if cross-cutting gateway concerns justify the cost.
- **Third-party IdP (Auth0, Okta)**: Unnecessary cost and complexity when Entra ID is already the enterprise standard. Rejected.

**Implementation approach**:
1. Entra ID multi-tenant app registration for the VirtualMirror API
2. Each tenant registered as a service principal with specific API permissions (scopes)
3. JWT validation middleware in ASP.NET Core with tenant claim extraction
4. Managed identity for all Azure resource access (zero secrets in config)
5. Rate limiting implemented via ASP.NET Core middleware per tenant tier (v1); Azure API Management gateway deferred to v2

---

## R5: Fit Comparison Algorithm

**Decision**: Measurement delta calculation with tolerance bands per garment fit type

**Rationale**: The fit recommendation compares shopper body measurements against garment measurements per area **[Verified]** — standard approach in the sizing industry. Each garment fit type (slim, regular, relaxed) defines different tolerance bands. A delta outside the band maps to the 5-point scale. This is deterministic (not ML) and highly testable. **[Hypothesis]**: Default tolerance thresholds (tight: 4 cm, comfort: 2 cm, loose: 5 cm) are estimated; validate with garment industry data and real return outcomes.

**Alternatives considered**:
- **ML-based fit prediction**: Higher accuracy potential but requires training data (actual return/keep decisions). Can be added as v2 enhancement once data is collected. Rejected for MVP — insufficient training data at launch.
- **Size chart lookup only**: Too simplistic — doesn't account for individual body variation or garment fit type. Rejected.
- **Ensemble (delta + ML)**: Best accuracy but over-engineering for launch. Planned for v2.

**Implementation approach**:
1. For each body area: `delta = shopper_measurement - garment_measurement`
2. Map delta against tolerance bands (configurable per garment fit type):
   - Too Tight: delta < -tight_threshold
   - Slightly Tight: -tight_threshold ≤ delta < -comfort_threshold
   - Good Fit: -comfort_threshold ≤ delta ≤ +comfort_threshold
   - Slightly Loose: +comfort_threshold < delta ≤ +loose_threshold
   - Too Loose: delta > +loose_threshold
3. Overall recommendation = worst-scoring area (conservative approach)
4. Confidence = minimum of (image extraction confidence, measurement coverage percentage)
5. Tolerance bands stored per garment category in Cosmos DB (configurable by tenant)

---

## R6: Observability Stack

**Decision**: OpenTelemetry SDK → Azure Monitor (Application Insights) + Azure Monitor Alerts

**Rationale**: OpenTelemetry is the CNCF standard for distributed tracing and metrics **[Verified]**. Azure Monitor natively ingests OTLP data and provides dashboards, alerting, and log analytics **[Verified]**. .NET 8 has built-in OpenTelemetry support via `Microsoft.Extensions.Diagnostics` **[Verified]**.

**Alternatives considered**:
- **Datadog/New Relic**: More feature-rich APM but adds cost and external dependency. Microsoft stack preference makes Azure Monitor the natural choice. Rejected.
- **ELK Stack (self-hosted)**: Maximum control but high operational burden. Rejected per constitution (X. IaC — prefer managed services).
- **Prometheus + Grafana**: Excellent for Kubernetes but Azure Monitor integrates more tightly with ACA. Rejected for v1.

**Implementation approach**:
1. OpenTelemetry SDK configured in Program.cs (traces, metrics, logs)
2. Correlation ID propagated via `Activity` (W3C trace context)
3. Custom metrics: `virtualmirror.assessment.duration`, `virtualmirror.assessment.confidence`, `virtualmirror.image.rejection_rate`
4. Azure Monitor alerts on: p95 > 5s, error rate > 0.1%, model confidence drift
5. Runbooks linked to each alert in Azure Monitor action groups

---

## R7: Deployment & Infrastructure

**Decision**: Azure Container Apps with Bicep IaC, deployed via GitHub Actions

**Rationale**: Azure Container Apps provides serverless container hosting with built-in auto-scaling, ingress, and Dapr integration — without the complexity of full AKS **[Verified]**. Bicep is the native Azure IaC language with first-class tooling in VS Code **[Verified]**. GitHub Actions provides CI/CD with native Azure integration **[Verified]**. **[Hypothesis]**: Auto-scaling threshold of 50 concurrent HTTP requests is estimated; validate under load testing.

**Alternatives considered**:
- **Azure Kubernetes Service (AKS)**: More control but over-engineered for a single service with < 10 containers. Rejected for v1 — can migrate if scale demands it.
- **Azure App Service**: Simpler but less container-native and limited auto-scaling. Rejected.
- **Terraform**: Well-known IaC but Bicep has better Azure-native type safety and no state file management. Rejected per Microsoft stack preference.

**Implementation approach**:
1. Bicep modules: Container App Environment, Container App, Cosmos DB account, Storage account, Key Vault, Entra ID app registrations, Azure OpenAI, Azure AI Content Safety, Azure Service Bus
2. Three environments: dev (Basic tier), staging (mirrors prod), prod (Standard tier with multi-zone)
3. GitHub Actions workflow: build → test → scan → deploy-staging → smoke-test → deploy-prod
4. Auto-scaling: 2 min replicas, 10 max, scaling on HTTP concurrent requests (threshold: 50)

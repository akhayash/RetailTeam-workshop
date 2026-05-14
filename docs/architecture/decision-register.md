# Decision Register: AI Clothing Fit Assessment Agent

**Version**: 1.1.0 | **Date**: 2026-05-14 | **Status**: Active

## Decision Log

| ID | Date | Decision | Status |
|----|------|----------|--------|
| [ADR-001](#adr-001-body-measurement-extraction-approach) | 2026-05-13 | Three-tier Microsoft AI pipeline for body measurement extraction | Accepted |
| [ADR-002](#adr-002-multi-tenant-data-isolation) | 2026-05-13 | Cosmos DB hierarchical partition keys for tenant isolation | Accepted |
| [ADR-003](#adr-003-image-processing-and-transient-storage) | 2026-05-13 | Hybrid in-memory / Blob Storage with 60s TTL | Accepted |
| [ADR-004](#adr-004-authentication-architecture) | 2026-05-13 | Microsoft Entra ID with managed identity, APIM deferred to v2 | Accepted |
| [ADR-005](#adr-005-fit-comparison-algorithm) | 2026-05-13 | Deterministic tolerance band delta calculation | Accepted |
| [ADR-006](#adr-006-observability-stack) | 2026-05-13 | OpenTelemetry SDK to Azure Monitor | Accepted |
| [ADR-007](#adr-007-deployment-infrastructure) | 2026-05-13 | Azure Container Apps with Bicep IaC | Accepted |
| [ADR-008](#adr-008-mandatory-height-input) | 2026-05-13 | Require shopper height as mandatory API input | Accepted |
| [ADR-009](#adr-009-rate-limiting-strategy) | 2026-05-13 | ASP.NET Core middleware for v1, APIM gateway deferred | Accepted |
| [ADR-010](#adr-010-async-queuing-under-load) | 2026-05-13 | Azure Service Bus for overflow queuing | Accepted |
| [ADR-011](#adr-011-clean-architecture-project-structure) | 2026-05-13 | 4-project Clean Architecture + Aspire host | Accepted |
| [ADR-012](#adr-012-malware-scanning-on-uploads) | 2026-05-13 | Microsoft Defender for Storage or ClamAV sidecar | Accepted |

---

## ADR-001: Body Measurement Extraction Approach

**Context**: The system must extract body measurements from 2D shopper photos and perform Tier 1 image validation before measurement extraction. The validation layer needs person detection, multi-person rejection, and bounding box quality checks with no near-term deprecation risk.

**Problem**: Azure AI Vision 4.0 only provides people bounding boxes and confidence scores, cannot extract body landmarks or anthropometric measurements, and is retiring in September 2028. The architecture also needs a Tier 1 validator that fits the Microsoft AI Foundry ecosystem and can evolve beyond simple detection if requirements expand.

**Decision**: Adopt a three-tier Microsoft AI pipeline:

- **Tier 1 (Validation)**: Florence-2-large on an Azure AI Foundry managed online endpoint, invoked via `Azure.AI.Inference`, for person detection, object counting, multi-person rejection, and bounding box quality validation; Azure AI Content Safety for minor detection and content moderation
- **Tier 2 (Extraction)**: Azure OpenAI GPT-5.2 Vision with native structured output (JSON schema validation) for measurement extraction, using mandatory height input as scale reference
- **Tier 3 (v2 Future)**: Custom SMPL body model on Azure AI Foundry managed endpoint for improved accuracy (±1–2 cm vs ±2–4 cm)

**Alternatives rejected**:

| Alternative | Reason |
|-------------|--------|
| Azure AI Vision 4.0 | Retiring September 2028; legacy people-detection service when Florence-2 covers Tier 1 validation within Azure AI Foundry |
| Azure AI Vision Custom Model | Only object detection/classification, not centimeter output |
| MediaPipe Pose (Google) | Self-hosting required, GPU management, Google stack misalignment |
| Third-party API (3DLOOK, Bold Metrics) | External dependency, per-call cost, privacy concerns (Constitution VII) |
| Custom SMPL model immediately | 3–6 month development timeline, insufficient for MVP |

**Consequences**: GPT-5.2 Vision (successor to GPT-4o Vision, whose standard Azure OpenAI deployments retired in March 2026) remains non-deterministic (LLM-based), so confidence calibration and prompt versioning are still required. Florence-2 removes the Azure AI Vision retirement risk, keeps Tier 1 behind the existing `IImageValidator` abstraction, and adds future flexibility for richer vision tasks such as dense captioning or fine-tuning in Azure AI Foundry.

---

## ADR-002: Multi-Tenant Data Isolation

**Context**: The service is multi-tenant from day one. Each retail partner requires isolated garment catalogs, shopper profiles, and assessment data.

**Decision**: Azure Cosmos DB with hierarchical partition keys (`/tenantId` → `/entityType` → `/entityId`). Row-level security enforced at the application layer via a repository base class with compile-time tenant scoping.

**Alternatives rejected**:

| Alternative | Reason |
|-------------|--------|
| Database per tenant | Expensive at scale, complex management (< 50 tenants expected) |
| Container per tenant | Partition key management complexity |
| Shared container with filter | Risk of cross-tenant leakage if filter missed |

**Consequences**: Autoscale 400–4000 RU/s at database level. Physical co-location per tenant ensures query performance. Must ensure every query path includes tenant context.

---

## ADR-003: Image Processing and Transient Storage

**Context**: Uploaded photos must be available to multiple AI services for processing, then purged within 60 seconds per constitution (VII. Data Minimization).

**Decision**: Hybrid approach. Images ≤ 4 MB streamed directly to AI services in-memory. Images > 4 MB uploaded to Azure Blob Storage with 60-second TTL lifecycle policy, SAS URL passed to AI endpoints, deletion confirmed after processing.

**Alternatives rejected**:

| Alternative | Reason |
|-------------|--------|
| In-memory only | Memory pressure under concurrent load with 10 MB images across three AI services |
| Azure Queue + background | Adds latency, violates 5-second SLA |
| Disk-based temp files | Hard to audit and purge reliably |

**Consequences**: Blob container has immutable lifecycle policy preventing TTL modification. Audit log entry written on upload and deletion.

---

## ADR-004: Authentication Architecture

**Context**: The service authenticates frontend systems (B2B), not individual shoppers. Rate limiting and request correlation are cross-cutting concerns.

**Decision**: Microsoft Entra ID with per-tenant app registrations and client credentials. Managed identity for all Azure resource access (zero secrets in config). Rate limiting via ASP.NET Core middleware per tenant tier for v1.

**APIM deferral**: Azure API Management was considered for gateway-level rate limiting, request correlation, and caching. Deferred to v2 — ASP.NET Core middleware handles rate limiting adequately for v1 scale. APIM can be introduced when cross-cutting gateway concerns justify the infrastructure cost.

**Alternatives rejected**:

| Alternative | Reason |
|-------------|--------|
| API key-based auth | No token expiration, refresh, or fine-grained scopes (Constitution II) |
| Third-party IdP (Auth0, Okta) | Unnecessary cost/complexity with Entra ID available |

**Consequences**: Each tenant requires Entra ID app registration setup during onboarding. JWT validation middleware extracts tenant claims for scoping.

---

## ADR-005: Fit Comparison Algorithm

**Context**: The system must compare derived body measurements against garment size data and produce a fit recommendation.

**Decision**: Deterministic measurement delta calculation with configurable tolerance bands per garment fit type (Slim, Regular, Relaxed). Overall recommendation uses worst-scoring area (conservative approach).

**Alternatives rejected**:

| Alternative | Reason |
|-------------|--------|
| ML-based fit prediction | Requires training data (return/keep decisions) — unavailable at launch |
| Size chart lookup only | Too simplistic, ignores body variation and fit type |
| Ensemble (delta + ML) | Over-engineering for MVP; planned for v2 |

**Consequences**: Highly testable and deterministic. Tolerance bands configurable per tenant and garment category. Accuracy depends on measurement extraction quality.

---

## ADR-006: Observability Stack

**Context**: Constitution VI requires structured logging, SLO dashboards, model drift monitoring, and runbooks for every alert.

**Decision**: OpenTelemetry SDK exporting traces, metrics, and logs to Azure Monitor (Application Insights). Custom metrics for assessment duration, confidence, and image rejection rate. Azure Monitor alerts with linked runbooks.

**Alternatives rejected**:

| Alternative | Reason |
|-------------|--------|
| Datadog / New Relic | External dependency, cost, Microsoft stack preference |
| ELK Stack (self-hosted) | High operational burden (Constitution X — prefer managed) |
| Prometheus + Grafana | Better for Kubernetes; Azure Monitor integrates tighter with ACA |

**Consequences**: .NET 8 has built-in OpenTelemetry support. W3C trace context propagation via `Activity`. 90-day hot + 1-year cold log retention per constitution.

---

## ADR-007: Deployment Infrastructure

**Context**: The service runs as a containerized .NET 8 API requiring auto-scaling, health checks, and multi-AZ deployment.

**Decision**: Azure Container Apps (serverless container hosting) with Bicep IaC deployed via GitHub Actions. Three environments: dev, staging, production.

**Alternatives rejected**:

| Alternative | Reason |
|-------------|--------|
| Azure Kubernetes Service | Over-engineered for single service with < 10 containers |
| Azure App Service | Less container-native, limited auto-scaling |
| Terraform | Bicep has better Azure-native type safety and no state file |

**Consequences**: Auto-scaling 2–10 replicas on HTTP concurrent requests (threshold: 50). Multi-AZ in production. Can migrate to AKS if scale demands.

---

## ADR-008: Mandatory Height Input

**Context**: From a 2D photo alone, it is impossible to determine absolute body dimensions. Every pixel-to-centimeter conversion requires a known scale reference.

**Decision**: Require shoppers to provide their height in centimeters (100–250 cm range) as a mandatory API input. Height serves as the absolute scale reference for deriving all other measurements.

**Alternatives considered**:

| Alternative | Reason for rejection |
|-------------|---------------------|
| Reference object in photo | Unreliable — shoppers unlikely to include ruler or standard object |
| Camera metadata (distance) | Not available from standard smartphone photos |
| Statistical height estimation | Too inaccurate across demographics |

**Consequences**: Adds friction to the user flow (shopper must know their height). Frontend can provide a feet/inches converter. Assumption documented: shoppers know their height or can convert.

---

## ADR-009: Rate Limiting Strategy

**Context**: Constitution IV requires rate limiting. Decision needed between middleware-based and API gateway-based approaches.

**Decision**: ASP.NET Core rate limiting middleware per tenant tier (Basic: 100/min, Standard: 500/min, Premium: 2000/min) for v1. Azure API Management deferred to v2.

**Rationale**: Middleware is sufficient for v1 scale and avoids additional infrastructure cost. APIM introduces gateway-level benefits (caching, request correlation, analytics) that become valuable as the number of consuming frontends grows.

**Consequences**: Rate limiting state is per-instance (not distributed) in v1. Acceptable given 2–10 replica range. v2 with APIM provides distributed rate limiting.

---

## ADR-010: Async Queuing Under Load

**Context**: The system must handle peak traffic (e.g., Black Friday) without failing. Constitution IX requires graceful degradation.

**Decision**: Azure Service Bus queue for overflow. When queue depth exceeds 50 pending requests or p95 exceeds 4 seconds, new requests are enqueued and callers receive HTTP 202 with a poll URL and estimated wait time.

**Consequences**: Adds complexity to the assessment pipeline (sync + async paths). Requires a queue consumer process and status polling endpoint.

---

## ADR-011: Clean Architecture Project Structure

**Context**: The service requires separation of concerns for testability, maintainability, and dependency management.

**Decision**: 4-project Clean Architecture (Api, Core, Services, Infrastructure) plus .NET Aspire orchestrator host. Core has zero external dependencies. Infrastructure implements Core interfaces.

**Consequences**: Follows Microsoft's recommended .NET architecture patterns. Enables independent unit testing of business logic without Azure SDK dependencies.

---

## ADR-012: Malware Scanning on Uploads

**Context**: Constitution Security Requirements mandate malware scanning on all uploaded content.

**Decision**: Integrate Microsoft Defender for Storage (preferred) or ClamAV as a sidecar container for malware scanning of uploaded images before AI processing.

**Consequences**: Adds latency to the image validation pipeline (typically 100–500 ms). Defender for Storage integrates natively with Azure Blob Storage. ClamAV sidecar is the fallback for in-memory streaming paths.

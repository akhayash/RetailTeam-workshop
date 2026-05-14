# Implementation Plan: AI Clothing Fit Assessment Agent

**Branch**: `001-clothing-fit-assessment` | **Date**: 2026-05-14 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-clothing-fit-assessment/spec.md`

## Summary

Build a multi-tenant AI-powered clothing fit assessment service that accepts shopper photos, extracts body measurements using Azure OpenAI GPT-5.2 Vision (with mandatory height input as scale reference), compares them against garment size data, and returns a 5-point fit recommendation per body area. Florence-2 on Azure AI Foundry handles image validation (people detection, multi-person rejection, bounding box quality checks) and Azure AI Content Safety provides content moderation. Deployed as a standalone .NET 8 Web API on Azure Container Apps with Azure Cosmos DB for multi-tenant data isolation, Azure Blob Storage for transient image processing, and Microsoft Entra ID for B2B authentication.

## Technical Context

**Language/Version**: C# / .NET 8.0 (LTS)
**Primary Dependencies**: ASP.NET Core Web API, Azure.AI.OpenAI (GPT-5.2 Vision), Florence-2 on Azure AI Foundry (people detection, bounding box validation), Azure.AI.Inference, Azure.AI.ContentSafety, Azure.Identity, Microsoft.Azure.Cosmos, Azure.Storage.Blobs, Swashbuckle (OpenAPI), Aspire (orchestration)
**Resilience Dependencies**: Microsoft.Extensions.Http.Resilience (Polly v8), Microsoft.Extensions.Diagnostics.HealthChecks, Azure.Messaging.ServiceBus (DLQ processing)
**Storage**: Azure Cosmos DB (multi-tenant document store with hierarchical partition keys per tenant), Azure Blob Storage (ZRS, transient image processing only)
**Testing**: xUnit, FluentAssertions, NSubstitute, Microsoft.AspNetCore.Mvc.Testing, NBomber (load), Verify (snapshot)
**Target Platform**: Linux containers on Azure Container Apps (ACA)
**Project Type**: Web service (REST API)
**Performance Goals**: p95 < 5 seconds end-to-end fit assessment, 500 concurrent requests
**Constraints**: Images purged after processing (< 60s retention), 10 MB max upload, 99.9% availability SLO (achievable ~99.7% single-region; 99.9% requires v2 multi-region)
**Scale/Scope**: Multi-tenant, single-region v1, horizontal auto-scaling 3–10 instances (min 3 for multi-AZ coverage)
**Resilience Targets**: RTO < 30 min, RPO < 1 hour, AI failover < 5s detection, circuit breaker recovery < 30s

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| # | Principle | Status | Evidence |
|---|-----------|--------|----------|
| I | Privacy by Design | ✅ PASS | Images processed in-memory/transient blob only; opaque shopper IDs; deletion within 24h; no PII in telemetry |
| II | Security First | ✅ PASS | Entra ID OAuth 2.0; input validation at boundary; Key Vault for secrets; TLS 1.2+; container scanning in CI |
| III | AI Responsibility | ✅ PASS | 70% confidence threshold with fallback; model versioning; transparency disclaimer; bias evaluation plan |
| IV | API-First Architecture | ✅ PASS | OpenAPI 3.x spec-first; stateless service; versioned endpoints; health checks; rate limiting via ASP.NET Core middleware per tenant tier |
| V | Test-Driven Development | ✅ PASS | xUnit TDD; contract tests; integration tests; SAST/SCA in CI; NBomber load tests |
| VI | Observability | ✅ PASS | OpenTelemetry + Azure Monitor; structured logging; SLO dashboards; drift alerting |
| VII | Data Minimization | ✅ PASS | Transient blob storage auto-purge; tenant-scoped data; audit logs; no raw images to third parties |
| VIII | Change Management | ✅ PASS | Feature flags via Azure App Configuration; canary deployments; rollback < 15 min |
| IX | Resilience | ⚠️ PARTIAL | Multi-AZ Container Apps; auto-scaling. **Gaps identified**: No AI failover, no retry/timeout policies, no tenant bulkhead, no health probe differentiation. See [resiliency-review.md](../../docs/architecture/resiliency-review.md) |
| X | Infrastructure as Code | ✅ PASS | Bicep templates; environment promotion dev→staging→prod; drift detection |

**Gate Result**: 9 PASS + 1 PARTIAL (IX Resilience) — proceeding to Phase 0. Resiliency gaps addressed in Phase 2 (Foundational) and Phase 7 (Polish).

### Post-Phase 1 Re-Check

| # | Principle | Status | Design Evidence |
|---|-----------|--------|-----------------|
| I | Privacy by Design | ✅ PASS | ShopperProfile stores measurements only (not photos); opaque shopperRef; hard delete within 24h; transient blob with 60s TTL |
| II | Security First | ✅ PASS | Entra ID OAuth scopes per operation; input validation in OpenAPI schema; managed identity for Azure resources |
| III | AI Responsibility | ✅ PASS | `isLowConfidence` + `disclaimer` fields in API response; `modelVersion` tracked per assessment |
| IV | API-First | ✅ PASS | OpenAPI 3.0.3 contract defined; versioned (v1); health endpoint; rate limiting per tier |
| VII | Data Minimization | ✅ PASS | Cosmos TTL on assessments; no raw image persistence; tenant-scoped partition keys |
| IX | Resilience | ✅ PASS | Polly resilience pipelines per dependency; AI endpoint failover (primary/secondary); liveness/readiness/startup probes; degradation ladder (5 modes); tenant bulkhead; DLQ processing; min 3 replicas multi-AZ |
| X | IaC | ✅ PASS | Bicep modules defined; 3-environment promotion in project structure |

## Project Structure

### Documentation (this feature)

```text
specs/001-clothing-fit-assessment/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (OpenAPI spec)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
src/
├── VirtualMirror.Api/                    # ASP.NET Core Web API host
│   ├── Controllers/                  # API controllers (v1)
│   ├── HealthChecks/                 # Liveness, readiness, startup probes
│   ├── Middleware/                    # Auth, rate limiting, correlation ID, tenant bulkhead
│   ├── Filters/                      # Validation, exception handling
│   └── Program.cs                    # Host configuration + resilience pipeline registration
├── VirtualMirror.Core/                   # Domain models & interfaces
│   ├── Models/                       # Entities (ShopperProfile, Garment, VirtualMirrorment, Tenant)
│   ├── Interfaces/                   # Service contracts
│   └── Enums/                        # FitScale, GarmentCategory, etc.
├── VirtualMirror.Services/               # Business logic
│   ├── Assessment/                   # Fit comparison engine + degradation ladder
│   ├── ImageProcessing/              # Image validation & measurement extraction
│   ├── Garments/                     # Catalog management
│   └── Profiles/                     # Shopper profile CRUD
├── VirtualMirror.Infrastructure/         # External integrations
│   ├── AzureAI/                      # Azure OpenAI GPT-5.2 Vision (primary + failover) + Florence-2 (primary + failover) + Content Safety
│   ├── Cosmos/                       # Cosmos DB repositories
│   ├── BlobStorage/                  # Transient image storage (ZRS)
│   ├── Messaging/                    # Azure Service Bus (async queue + DLQ processor)
│   ├── Resilience/                   # Polly pipelines, circuit breaker configs, AI failover clients
│   └── Configuration/               # App Config, Key Vault, Feature Flags
└── VirtualMirror.AppHost/                # .NET Aspire orchestrator

tests/
├── VirtualMirror.Api.Tests/              # Integration tests (WebApplicationFactory)
├── VirtualMirror.Core.Tests/             # Unit tests (domain logic)
├── VirtualMirror.Services.Tests/         # Unit tests (services)
├── VirtualMirror.Infrastructure.Tests/   # Integration tests (external deps)
├── VirtualMirror.Contract.Tests/         # API contract validation
└── VirtualMirror.Load.Tests/             # NBomber performance tests

infra/
├── main.bicep                        # Root Bicep deployment
├── modules/                          # Bicep modules (ACA, Cosmos, Blob, Entra)
└── parameters/                       # Per-environment parameter files
```

**Structure Decision**: Clean Architecture with 4 projects (Api, Core, Services, Infrastructure) + Aspire host. This separates domain logic from infrastructure concerns, enables independent testing, and follows Microsoft's recommended .NET architecture patterns for enterprise services.

## Resiliency Implementation Plan

Cross-cutting resilience patterns identified in the [Resiliency Review](../../docs/architecture/resiliency-review.md). These are woven into Phases 2, 3, and 7 of the task list.

### Resilience Patterns

| Pattern | Implementation | Phase |
|---------|---------------|-------|
| **Polly resilience pipelines** | Timeout + retry + circuit breaker per external dependency (Florence-2, GPT-5.2, Content Safety, Service Bus) | Phase 2 (Foundational) |
| **AI endpoint failover** | Primary/secondary Azure OpenAI and Florence-2 resources with health-check switching | Phase 2 (Foundational) |
| **Health probe differentiation** | `/health/live` (liveness), `/health/ready` (readiness with dependency checks), `/health/startup` (cold start) | Phase 2 (Foundational) |
| **Degradation ladder** | 5 failure modes mapped to specific degraded responses (cached profile, skip validation, queue safety review, 503, size chart fallback) | Phase 3 (US1) |
| **Tenant bulkhead** | Per-tenant concurrency limiter (`SemaphoreSlim`) capping concurrent AI pipeline calls | Phase 2 (Foundational) |
| **DLQ processing** | Dead letter queue handler with max delivery count = 3, alerting, and manual retry | Phase 7 (Polish) |
| **Scale-in stabilization** | 5-minute stabilization window; minimum 3 replicas for multi-AZ; KEDA HTTP scaler target = 25 | Phase 7 (IaC) |

### Polly Pipeline Configuration

```text
Florence-2:     Timeout 3s → Retry 2x (exponential + jitter) → CB: open after 5 failures/30s
Content Safety: Timeout 2s → Retry 1x → CB: open after 5 failures/30s
GPT-5.2 Vision: Timeout 8s → Retry 1x (idempotent only) → CB: open after 3 failures/60s
Service Bus:    Timeout 3s → Retry 3x (exponential) → CB: open after 10 failures/60s
End-to-end:     Request timeout budget 12s (abort if budget exceeded before SLO breach)
```

### Degradation Ladder

| Level | Failure Mode | Response Strategy | HTTP Status |
|-------|-------------|-------------------|-------------|
| L1 | Content Safety unavailable | Queue for async safety review; proceed with assessment | 200 (with safety_review_pending flag) |
| L2 | Florence-2 unavailable | Skip person detection; proceed with GPT-5.2 (accept higher bad-image risk) | 200 (with validation_skipped flag) |
| L3 | GPT-5.2 unavailable, profile exists | Return fit comparison from cached profile measurements | 200 (with cached_profile flag) |
| L4 | GPT-5.2 unavailable, no profile | Return size chart redirect + garment data | 503 + fallback body |
| L5 | Cosmos DB unavailable | Reject with retry guidance | 503 + Retry-After header |

### Composite Availability Model

Single-region dependency chain (v1):

| Service | Individual SLA | Role |
|---------|---------------|------|
| Azure Container Apps | 99.95% | Compute |
| Azure Cosmos DB | 99.99% | Data |
| Azure OpenAI | 99.9% | AI extraction |
| Florence-2 (AI Foundry) | 99.9% | AI validation |
| Azure AI Content Safety | 99.9% | Moderation |
| Azure Service Bus | 99.95% | Messaging |

**Without failover**: ~99.6% composite (below 99.9% SLO)
**With AI failover** (primary/secondary): ~99.85% composite (approaches SLO)
**V2 multi-region**: 99.95%+ achievable

## Hypothesis Validation Plan

Key architectural assumptions from the [solution-architecture.md § Hypothesis Register](../../docs/architecture/solution-architecture.md#hypothesis-register) that require validation during implementation.

| ID | Hypothesis | Validation Phase | Task Reference | Go/No-Go Gate |
|----|-----------|-----------------|----------------|---------------|
| H1 | GPT-5.2 body measurement accuracy ±2–4 cm | Phase 3 (US1 implementation) | T043b integration spike | > 15% outside ±4 cm → escalate to Tier 3 |
| H2 | 70% confidence threshold | Phase 7 (Polish) | Load/accuracy testing | Evaluate after 30-day production data |
| H3 | 4 MB in-memory threshold | Phase 7 (Polish) | NBomber load tests | OOM at 500 concurrent → lower threshold |
| H4 | Tolerance band defaults | Phase 3 (US1 implementation) | T045 FitComparisonEngine | Compare against industry size charts |
| H5 | Auto-scale threshold: 25 concurrent per replica | Phase 7 (Polish) | NBomber load tests | p95 > 5s at 500 concurrent → tune KEDA target |
| H6 | Image rejection rate < 30% | Post-launch (30 days) | Production monitoring | > 40% → relax thresholds with confidence penalty |
| H7 | AI failover detection < 5s with Polly CB | Phase 2 (Foundational) | Resilience integration tests | > 10s failover → switch to active-active |
| H8 | Degradation ladder maintains > 90% request success during partial outage | Phase 3 (US1) | Chaos testing / fault injection | < 80% → revisit degradation strategy |

**Gates**:

- H1 must pass before Phase 3 completion. If GPT-5.2 accuracy is insufficient, escalate to Tier 3 custom model before Phase 4.
- H7 must pass before Phase 3 begins. AI failover is a foundational resilience capability.

## Complexity Tracking

No constitution violations detected — no justifications required.

## Cross-References

| Artifact | Relevance |
|----------|-----------|
| [Solution Architecture](../../docs/architecture/solution-architecture.md) | Authoritative architecture document; system context, AI pipeline, SLOs |
| [Resiliency Review](../../docs/architecture/resiliency-review.md) | 10 findings (F-001–F-010) driving resilience implementation in this plan |
| [Decision Register](../../docs/architecture/decision-register.md) | ADR-001 (AI pipeline), ADR-007 (ACA), ADR-009 (rate limiting), ADR-010 (Service Bus) |
| [Risk Register](../../docs/architecture/risk-register.md) | R-001 (GPT-5.2 accuracy), R-007 (Azure outage) map to H1, H7 |
| [OpenAPI Contract](contracts/openapi.yaml) | API contract driving implementation |
| [Data Model](data-model.md) | Entity definitions and relationships |

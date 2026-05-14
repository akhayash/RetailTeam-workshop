# Implementation Plan: AI Clothing Fit Assessment Agent

**Branch**: `001-clothing-fit-assessment` | **Date**: 2026-05-13 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-clothing-fit-assessment/spec.md`

## Summary

Build a multi-tenant AI-powered clothing fit assessment service that accepts shopper photos, extracts body measurements using Azure OpenAI GPT-4o Vision (with mandatory height input as scale reference), compares them against garment size data, and returns a 5-point fit recommendation per body area. Azure AI Vision handles image validation (people detection, multi-person rejection) and Azure AI Content Safety provides content moderation. Deployed as a standalone .NET 8 Web API on Azure Container Apps with Azure Cosmos DB for multi-tenant data isolation, Azure Blob Storage for transient image processing, and Microsoft Entra ID for B2B authentication.

## Technical Context

**Language/Version**: C# / .NET 8.0 (LTS)
**Primary Dependencies**: ASP.NET Core Web API, Azure.AI.OpenAI (GPT-4o Vision), Azure.AI.Vision.ImageAnalysis (people detection), Azure.AI.ContentSafety, Azure.Identity, Microsoft.Azure.Cosmos, Azure.Storage.Blobs, Swashbuckle (OpenAPI), Aspire (orchestration)
**Storage**: Azure Cosmos DB (multi-tenant document store with partition keys per tenant), Azure Blob Storage (transient image processing only)
**Testing**: xUnit, FluentAssertions, NSubstitute, Microsoft.AspNetCore.Mvc.Testing, NBomber (load), Verify (snapshot)
**Target Platform**: Linux containers on Azure Container Apps (ACA)
**Project Type**: Web service (REST API)
**Performance Goals**: p95 < 5 seconds end-to-end fit assessment, 500 concurrent requests
**Constraints**: Images purged after processing (< 60s retention), 10 MB max upload, 99.9% availability SLO
**Scale/Scope**: Multi-tenant, single-region v1, horizontal auto-scaling 2–10 instances

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
| IX | Resilience | ✅ PASS | Multi-AZ Container Apps; circuit breakers; graceful degradation; auto-scaling |
| X | Infrastructure as Code | ✅ PASS | Bicep templates; environment promotion dev→staging→prod; drift detection |

**Gate Result**: ALL PASS — proceeding to Phase 0.

### Post-Phase 1 Re-Check

| # | Principle | Status | Design Evidence |
|---|-----------|--------|-----------------|
| I | Privacy by Design | ✅ PASS | ShopperProfile stores measurements only (not photos); opaque shopperRef; hard delete within 24h; transient blob with 60s TTL |
| II | Security First | ✅ PASS | Entra ID OAuth scopes per operation; input validation in OpenAPI schema; managed identity for Azure resources |
| III | AI Responsibility | ✅ PASS | `isLowConfidence` + `disclaimer` fields in API response; `modelVersion` tracked per assessment |
| IV | API-First | ✅ PASS | OpenAPI 3.0.3 contract defined; versioned (v1); health endpoint; rate limiting per tier |
| VII | Data Minimization | ✅ PASS | Cosmos TTL on assessments; no raw image persistence; tenant-scoped partition keys |
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
├── FitAssess.Api/                    # ASP.NET Core Web API host
│   ├── Controllers/                  # API controllers (v1)
│   ├── Middleware/                    # Auth, rate limiting, correlation ID
│   ├── Filters/                      # Validation, exception handling
│   └── Program.cs                    # Host configuration
├── FitAssess.Core/                   # Domain models & interfaces
│   ├── Models/                       # Entities (ShopperProfile, Garment, FitAssessment, Tenant)
│   ├── Interfaces/                   # Service contracts
│   └── Enums/                        # FitScale, GarmentCategory, etc.
├── FitAssess.Services/               # Business logic
│   ├── Assessment/                   # Fit comparison engine
│   ├── ImageProcessing/              # Image validation & measurement extraction
│   ├── Garments/                     # Catalog management
│   └── Profiles/                     # Shopper profile CRUD
├── FitAssess.Infrastructure/         # External integrations
│   ├── AzureAI/                      # Azure OpenAI GPT-4o Vision (measurement extraction) + Azure AI Vision (validation) + Content Safety
│   ├── Cosmos/                       # Cosmos DB repositories
│   ├── BlobStorage/                  # Transient image storage
│   ├── Messaging/                    # Azure Service Bus (async assessment queue)
│   └── Configuration/               # App Config, Key Vault, Feature Flags
└── FitAssess.AppHost/                # .NET Aspire orchestrator

tests/
├── FitAssess.Api.Tests/              # Integration tests (WebApplicationFactory)
├── FitAssess.Core.Tests/             # Unit tests (domain logic)
├── FitAssess.Services.Tests/         # Unit tests (services)
├── FitAssess.Infrastructure.Tests/   # Integration tests (external deps)
├── FitAssess.Contract.Tests/         # API contract validation
└── FitAssess.Load.Tests/             # NBomber performance tests

infra/
├── main.bicep                        # Root Bicep deployment
├── modules/                          # Bicep modules (ACA, Cosmos, Blob, Entra)
└── parameters/                       # Per-environment parameter files
```

**Structure Decision**: Clean Architecture with 4 projects (Api, Core, Services, Infrastructure) + Aspire host. This separates domain logic from infrastructure concerns, enables independent testing, and follows Microsoft's recommended .NET architecture patterns for enterprise services.

## Complexity Tracking

No constitution violations detected — no justifications required.

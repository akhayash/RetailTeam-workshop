# Tasks: AI Clothing Fit Assessment Agent

**Input**: Design documents from `/specs/001-clothing-fit-assessment/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/openapi.yaml

**Organization**: Tasks grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Solution structure, project scaffolding, and dependency configuration

- [ ] T001 Create solution file and project structure per implementation plan at src/FitAssess.sln
- [ ] T002 Create FitAssess.Core class library project at src/FitAssess.Core/FitAssess.Core.csproj
- [ ] T003 [P] Create FitAssess.Services class library project at src/FitAssess.Services/FitAssess.Services.csproj
- [ ] T004 [P] Create FitAssess.Infrastructure class library project at src/FitAssess.Infrastructure/FitAssess.Infrastructure.csproj
- [ ] T005 Create FitAssess.Api web project with ASP.NET Core 8.0 at src/FitAssess.Api/FitAssess.Api.csproj
- [ ] T006 Create FitAssess.AppHost Aspire orchestrator project at src/FitAssess.AppHost/FitAssess.AppHost.csproj
- [ ] T007 [P] Create test projects (xUnit) at tests/FitAssess.Core.Tests, tests/FitAssess.Services.Tests, tests/FitAssess.Api.Tests, tests/FitAssess.Infrastructure.Tests, tests/FitAssess.Contract.Tests, tests/FitAssess.Load.Tests
- [ ] T008 [P] Add NuGet dependencies: Azure.AI.Vision.ImageAnalysis, Azure.Identity, Microsoft.Azure.Cosmos, Azure.Storage.Blobs, Swashbuckle.AspNetCore to appropriate projects
- [ ] T009 [P] Add test NuGet dependencies: xUnit, FluentAssertions, NSubstitute, Microsoft.AspNetCore.Mvc.Testing, Verify.Xunit, NBomber to test projects
- [ ] T010 [P] Configure Directory.Build.props for shared build settings (nullable, implicit usings, TreatWarningsAsErrors) at src/Directory.Build.props
- [ ] T011 [P] Create .editorconfig for C# coding conventions at root .editorconfig
- [ ] T012 [P] Create docker-compose.yml for local development (Cosmos DB emulator + Azurite) at docker-compose.yml

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T013 Define FitScale enum (TooTight, SlightlyTight, GoodFit, SlightlyLoose, TooLoose) at src/FitAssess.Core/Enums/FitScale.cs
- [ ] T014 [P] Define GarmentCategory enum (Top, Bottom, Dress, Outerwear, Underwear) at src/FitAssess.Core/Enums/GarmentCategory.cs
- [ ] T015 [P] Define GarmentFitType enum (Slim, Regular, Relaxed) at src/FitAssess.Core/Enums/GarmentFitType.cs
- [ ] T016 [P] Define TenantStatus enum (Onboarding, Active, Suspended) at src/FitAssess.Core/Enums/TenantStatus.cs
- [ ] T017 [P] Define RateLimitTier enum (Basic, Standard, Premium) at src/FitAssess.Core/Enums/RateLimitTier.cs
- [ ] T018 Create Tenant domain model at src/FitAssess.Core/Models/Tenant.cs
- [ ] T019 [P] Create BodyMeasurements value object at src/FitAssess.Core/Models/BodyMeasurements.cs
- [ ] T020 [P] Create GarmentMeasurements value object at src/FitAssess.Core/Models/GarmentMeasurements.cs
- [ ] T021 [P] Create AreaScores value object at src/FitAssess.Core/Models/AreaScores.cs
- [ ] T022 Create ShopperProfile domain model at src/FitAssess.Core/Models/ShopperProfile.cs
- [ ] T023 [P] Create Garment domain model at src/FitAssess.Core/Models/Garment.cs
- [ ] T024 [P] Create FitAssessmentResult domain model at src/FitAssess.Core/Models/FitAssessmentResult.cs
- [ ] T025 Define ITenantContext interface for multi-tenant scoping at src/FitAssess.Core/Interfaces/ITenantContext.cs
- [ ] T026 [P] Define ICosmosRepository<T> generic repository interface at src/FitAssess.Core/Interfaces/ICosmosRepository.cs
- [ ] T027 [P] Define IImageValidator interface at src/FitAssess.Core/Interfaces/IImageValidator.cs
- [ ] T028 [P] Define IBodyMeasurementExtractor interface at src/FitAssess.Core/Interfaces/IBodyMeasurementExtractor.cs
- [ ] T029 [P] Define IFitComparisonEngine interface at src/FitAssess.Core/Interfaces/IFitComparisonEngine.cs
- [ ] T030 [P] Define IBlobStorageService interface at src/FitAssess.Core/Interfaces/IBlobStorageService.cs
- [ ] T030a [P] Define IAuditLogger interface for immutable audit trail at src/FitAssess.Core/Interfaces/IAuditLogger.cs
- [ ] T030b [P] Define IAssessmentQueue interface for async request queuing at src/FitAssess.Core/Interfaces/IAssessmentQueue.cs
- [ ] T031 Implement CosmosRepository<T> base class with tenant-scoped queries at src/FitAssess.Infrastructure/Cosmos/CosmosRepository.cs
- [ ] T032 [P] Implement TenantContext middleware that extracts tenant ID from JWT claims at src/FitAssess.Api/Middleware/TenantContextMiddleware.cs
- [ ] T033 [P] Implement CorrelationIdMiddleware for request tracing at src/FitAssess.Api/Middleware/CorrelationIdMiddleware.cs
- [ ] T034 Configure Microsoft Entra ID JWT authentication in Program.cs at src/FitAssess.Api/Program.cs
- [ ] T035 [P] Implement global exception handling filter at src/FitAssess.Api/Filters/GlobalExceptionFilter.cs
- [ ] T036 [P] Implement request validation filter using FluentValidation at src/FitAssess.Api/Filters/ValidationFilter.cs
- [ ] T037 [P] Implement rate limiting middleware per tenant tier at src/FitAssess.Api/Middleware/RateLimitingMiddleware.cs
- [ ] T038 Configure OpenTelemetry (traces, metrics, logs) export to Azure Monitor at src/FitAssess.Api/Program.cs
- [ ] T038a Implement AuditLogger service writing immutable audit entries (model version, shopper ref, tenant, timestamp) to dedicated Cosmos container at src/FitAssess.Infrastructure/Cosmos/AuditLogger.cs
- [ ] T038b Configure Azure App Configuration feature flag integration for progressive rollouts at src/FitAssess.Infrastructure/Configuration/FeatureFlagService.cs
- [ ] T038c Implement AssessmentQueueService using Azure Service Bus for async request queuing under high load at src/FitAssess.Infrastructure/Messaging/AssessmentQueueService.cs
- [ ] T039 [P] Implement BlobStorageService with transient upload and auto-purge at src/FitAssess.Infrastructure/BlobStorage/BlobStorageService.cs
- [ ] T040 [P] Configure Aspire AppHost with Cosmos DB, Blob Storage, and API references at src/FitAssess.AppHost/Program.cs
- [ ] T041 Implement health check endpoint with Cosmos DB, Blob, and AI model checks at src/FitAssess.Api/Controllers/HealthController.cs

**Checkpoint**: Foundation ready — user story implementation can now begin in parallel

---

## Phase 3: User Story 1 — Photo-Based Fit Assessment (Priority: P1) 🎯 MVP

**Goal**: A shopper uploads a photo and receives a personalized 5-point fit recommendation per body area within 5 seconds

**Independent Test**: POST /api/v1/assessments with a photo and garment ID returns a structured fit response with confidence score

**TDD Enforcement**: For each implementation task below, write the corresponding unit/integration test FIRST (Red), then implement to pass (Green), then refactor. Test tasks (T059–T062) define the expected behavior; write them before T042–T056.

- [ ] T042 [US1] Implement ImageValidator service (format, size, quality checks) at src/FitAssess.Services/ImageProcessing/ImageValidator.cs
- [ ] T042a [US1] Implement minor/age detection logic in ImageValidator — reject images detected as under-16 with age-appropriate message at src/FitAssess.Services/ImageProcessing/ImageValidator.cs
- [ ] T042b [US1] Implement multi-person detection logic in ImageValidator — reject images with multiple people at src/FitAssess.Services/ImageProcessing/ImageValidator.cs
- [ ] T043 [US1] Implement AzureAIVisionClient wrapper for body landmark extraction at src/FitAssess.Infrastructure/AzureAI/AzureAIVisionClient.cs
- [ ] T044 [US1] Implement BodyMeasurementExtractor that converts AI landmarks to measurements at src/FitAssess.Services/ImageProcessing/BodyMeasurementExtractor.cs
- [ ] T045 [US1] Implement FitComparisonEngine with tolerance band logic per fit type at src/FitAssess.Services/Assessment/FitComparisonEngine.cs
- [ ] T046 [US1] Implement FitAssessmentService orchestrating the full assessment pipeline at src/FitAssess.Services/Assessment/FitAssessmentService.cs
- [ ] T047 [US1] Implement AssessmentsController with POST /api/v1/assessments endpoint at src/FitAssess.Api/Controllers/AssessmentsController.cs
- [ ] T048 [US1] Implement CreateAssessmentRequest DTO with validation at src/FitAssess.Api/Models/CreateAssessmentRequest.cs
- [ ] T049 [P] [US1] Implement FitAssessmentResponse DTO mapping at src/FitAssess.Api/Models/FitAssessmentResponse.cs
- [ ] T050 [P] [US1] Implement ImageQualityError response model at src/FitAssess.Api/Models/ImageQualityError.cs
- [ ] T051 [P] [US1] Implement FallbackResponse for graceful degradation at src/FitAssess.Api/Models/FallbackResponse.cs
- [ ] T052 [US1] Implement AssessmentRepository (Cosmos DB) for storing results at src/FitAssess.Infrastructure/Cosmos/AssessmentRepository.cs
- [ ] T053 [US1] Implement GarmentRepository (Cosmos DB) for garment lookups at src/FitAssess.Infrastructure/Cosmos/GarmentRepository.cs
- [ ] T054 [US1] Add graceful degradation logic when AI model is unavailable in FitAssessmentService at src/FitAssess.Services/Assessment/FitAssessmentService.cs
- [ ] T055 [US1] Add low-confidence threshold check (< 70%) with disclaimer in response at src/FitAssess.Services/Assessment/FitAssessmentService.cs
- [ ] T055a [US1] Integrate AuditLogger into FitAssessmentService — log every assessment with model version, tenant, shopper ref, and correlation ID at src/FitAssess.Services/Assessment/FitAssessmentService.cs
- [ ] T055b [US1] Implement queued assessment flow — when load exceeds threshold, enqueue via AssessmentQueueService and return HTTP 202 with poll URL at src/FitAssess.Services/Assessment/FitAssessmentService.cs
- [ ] T056 [US1] Wire up dependency injection for US1 services in Program.cs at src/FitAssess.Api/Program.cs
- [ ] T057 [US1] Create sample garment test fixture data for integration tests at tests/FitAssess.Api.Tests/Fixtures/SampleGarments.cs
- [ ] T058 [US1] Create sample photo test fixture (valid full-body image) at tests/FitAssess.Api.Tests/Fixtures/sample-photo.jpg
- [ ] T059 [US1] Write integration tests for POST /api/v1/assessments (happy path, bad image, low confidence) at tests/FitAssess.Api.Tests/AssessmentsControllerTests.cs
- [ ] T060 [P] [US1] Write unit tests for FitComparisonEngine tolerance band logic at tests/FitAssess.Services.Tests/Assessment/FitComparisonEngineTests.cs
- [ ] T061 [P] [US1] Write unit tests for ImageValidator at tests/FitAssess.Services.Tests/ImageProcessing/ImageValidatorTests.cs
- [ ] T062 [P] [US1] Write unit tests for BodyMeasurementExtractor at tests/FitAssess.Services.Tests/ImageProcessing/BodyMeasurementExtractorTests.cs

---

## Phase 4: User Story 2 — Measurement Profile Storage (Priority: P2)

**Goal**: A returning shopper can save their body measurements and get fit recommendations without re-uploading a photo

**Independent Test**: Complete assessment via US1 with saveProfile=true, then POST /api/v1/assessments/by-profile returns fit result using stored measurements

**TDD Enforcement**: Write T072–T073 test expectations FIRST, then implement T063–T071.

- [ ] T063 [US2] Implement ProfileRepository (Cosmos DB) for shopper profiles at src/FitAssess.Infrastructure/Cosmos/ProfileRepository.cs
- [ ] T064 [US2] Implement ShopperProfileService with save, get, and delete operations at src/FitAssess.Services/Profiles/ShopperProfileService.cs
- [ ] T065 [US2] Implement ProfilesController with GET and DELETE /api/v1/profiles/{shopperRef} at src/FitAssess.Api/Controllers/ProfilesController.cs
- [ ] T066 [US2] Add saveProfile logic to FitAssessmentService (persist measurements when flag is true) at src/FitAssess.Services/Assessment/FitAssessmentService.cs
- [ ] T067 [US2] Implement POST /api/v1/assessments/by-profile endpoint in AssessmentsController at src/FitAssess.Api/Controllers/AssessmentsController.cs
- [ ] T068 [US2] Implement profile deletion with 24-hour fulfillment guarantee and audit log at src/FitAssess.Services/Profiles/ShopperProfileService.cs
- [ ] T069 [P] [US2] Implement ShopperProfileResponse DTO at src/FitAssess.Api/Models/ShopperProfileResponse.cs
- [ ] T070 [P] [US2] Implement DeletionAccepted response DTO at src/FitAssess.Api/Models/DeletionAccepted.cs
- [ ] T071 [US2] Wire up dependency injection for US2 services in Program.cs at src/FitAssess.Api/Program.cs
- [ ] T072 [US2] Write integration tests for profile CRUD and assessment-by-profile at tests/FitAssess.Api.Tests/ProfilesControllerTests.cs
- [ ] T073 [P] [US2] Write unit tests for ShopperProfileService at tests/FitAssess.Services.Tests/Profiles/ShopperProfileServiceTests.cs

---

## Phase 5: User Story 3 — Frontend Integration Layer (Priority: P2)

**Goal**: A retail frontend team can integrate via a well-documented, authenticated API with proper error handling and OpenAPI documentation

**Independent Test**: API endpoints return correct OpenAPI schema; auth rejection returns 401 with no data leakage; rate limiting responds with 429 and Retry-After header

**TDD Enforcement**: Write T079–T081 contract and integration tests FIRST, then implement T074–T078.

- [ ] T074 [US3] Configure Swashbuckle for OpenAPI 3.x generation with Entra ID security scheme at src/FitAssess.Api/Program.cs
- [ ] T075 [US3] Add XML documentation comments to all controller actions for OpenAPI descriptions at src/FitAssess.Api/Controllers/*.cs
- [ ] T076 [US3] Implement API versioning (v1) using ASP.NET Core API Versioning package at src/FitAssess.Api/Program.cs
- [ ] T077 [US3] Configure CORS policy for frontend origins at src/FitAssess.Api/Program.cs
- [ ] T078 [P] [US3] Implement AssessmentQueued response for high-load scenarios (HTTP 202) at src/FitAssess.Api/Models/AssessmentQueued.cs
- [ ] T079 [US3] Write contract tests validating generated OpenAPI matches contracts/openapi.yaml at tests/FitAssess.Contract.Tests/OpenApiContractTests.cs
- [ ] T080 [P] [US3] Write integration tests for auth rejection (401) and rate limiting (429) at tests/FitAssess.Api.Tests/SecurityIntegrationTests.cs
- [ ] T081 [P] [US3] Write integration tests for graceful degradation (503 with fallback) at tests/FitAssess.Api.Tests/ResilienceIntegrationTests.cs

---

## Phase 6: User Story 4 — Garment Data Ingestion (Priority: P3)

**Goal**: A retail operations team can onboard garment catalog data with size measurements per SKU

**Independent Test**: POST /api/v1/garments creates a garment; POST /api/v1/garments/batch bulk-creates; GET /api/v1/garments lists with pagination

**TDD Enforcement**: Write T089–T090 tests FIRST, then implement T082–T088.

- [ ] T082 [US4] Implement GarmentService with upsert, batch upsert, and list operations at src/FitAssess.Services/Garments/GarmentService.cs
- [ ] T083 [US4] Implement GarmentsController with POST, GET, and batch endpoints at src/FitAssess.Api/Controllers/GarmentsController.cs
- [ ] T084 [US4] Implement GarmentUpsertRequest DTO with FluentValidation rules at src/FitAssess.Api/Models/GarmentUpsertRequest.cs
- [ ] T085 [P] [US4] Implement GarmentResponse and GarmentListResponse DTOs at src/FitAssess.Api/Models/GarmentResponse.cs
- [ ] T086 [P] [US4] Implement BatchUpsertResponse DTO at src/FitAssess.Api/Models/BatchUpsertResponse.cs
- [ ] T087 [US4] Add garment version tracking on update in GarmentRepository at src/FitAssess.Infrastructure/Cosmos/GarmentRepository.cs
- [ ] T088 [US4] Wire up dependency injection for US4 services in Program.cs at src/FitAssess.Api/Program.cs
- [ ] T089 [US4] Write integration tests for garment CRUD and batch operations at tests/FitAssess.Api.Tests/GarmentsControllerTests.cs
- [ ] T090 [P] [US4] Write unit tests for GarmentService validation logic at tests/FitAssess.Services.Tests/Garments/GarmentServiceTests.cs

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Infrastructure as Code, CI/CD, observability dashboards, and production readiness

**Note**: Tasks T098 configures Program.cs-related settings (Swagger, versioning, CORS) that build incrementally on earlier Phase 2 work in T034/T038. These are additive registrations in the same file — not duplications.

- [ ] T091 Create root Bicep template with module references at infra/main.bicep
- [ ] T092 [P] Create Bicep module for Azure Container Apps environment at infra/modules/container-app.bicep
- [ ] T093 [P] Create Bicep module for Cosmos DB account with hierarchical partition keys at infra/modules/cosmos-db.bicep
- [ ] T094 [P] Create Bicep module for Storage account (blob lifecycle policy) at infra/modules/storage.bicep
- [ ] T095 [P] Create Bicep module for Key Vault at infra/modules/key-vault.bicep
- [ ] T096 [P] Create Bicep module for Entra ID app registration at infra/modules/entra-app.bicep
- [ ] T096a [P] Create Bicep module for Azure Service Bus namespace and queue at infra/modules/service-bus.bicep
- [ ] T097 Create dev/staging/prod parameter files at infra/parameters/dev.json, staging.json, prod.json
- [ ] T098 Create GitHub Actions CI workflow (build, test, scan, container sign, deploy) at .github/workflows/ci.yml — include container image scanning (Trivy) and signing (Notation/cosign) steps
- [ ] T099 [P] Create Dockerfile for FitAssess.Api at src/FitAssess.Api/Dockerfile
- [ ] T100 [P] Create .dockerignore at root .dockerignore
- [ ] T101 [P] Configure Azure Monitor alert rules for SLO violations in Bicep at infra/modules/alerts.bicep
- [ ] T102 Write NBomber load test simulating 500 concurrent assessments at tests/FitAssess.Load.Tests/ConcurrentAssessmentLoadTest.cs
- [ ] T102a Write end-to-end smoke tests validating the full user journey (upload → assess → profile save → assess-by-profile) against staging environment at tests/FitAssess.Api.Tests/E2E/SmokeTests.cs
- [ ] T103 Create README.md with project overview, setup instructions, and architecture diagram at README.md

---

## Dependencies

```text
Phase 1 (Setup)
  └──► Phase 2 (Foundational)
         ├──► Phase 3 (US1: Photo Assessment) 🎯 MVP
         │      └──► Phase 4 (US2: Profile Storage) [depends on US1 pipeline]
         ├──► Phase 5 (US3: Integration Layer) [parallel with US1]
         └──► Phase 6 (US4: Garment Ingestion) [parallel with US1]

Phase 7 (Polish) can start after Phase 2, runs in parallel with Phases 3-6
```

## Parallel Execution Opportunities

### Within Phase 2 (Foundational):
- T013–T017 (all enums) → parallel
- T018–T024 (models, after enums) → T019/T020/T021 parallel, T22/T23/T24 parallel
- T025–T030 (interfaces) → all parallel
- T031–T041 (infrastructure) → T032/T033/T035/T036/T37/T39/T40 parallel after T031

### Within Phase 3 (US1):
- T042/T043 parallel (image validator + AI client independent)
- T048/T049/T050/T051 (DTOs) → all parallel
- T060/T061/T062 (unit tests) → all parallel

### Across Phases:
- Phase 5 (US3) can start immediately after Phase 2 (no dependency on US1)
- Phase 6 (US4) can start immediately after Phase 2 (uses GarmentRepository from T053)
- Phase 7 (IaC/CI) can start after Phase 2

## Implementation Strategy

1. **MVP Scope**: Phase 1 + Phase 2 + Phase 3 (User Story 1) delivers a working fit assessment API that accepts photos and returns recommendations
2. **Incremental Delivery**:
   - Sprint 1: Phases 1–2 (project setup + foundation)
   - Sprint 2: Phase 3 (MVP — photo-based fit assessment)
   - Sprint 3: Phases 4 + 5 in parallel (profiles + integration polish)
   - Sprint 4: Phase 6 + Phase 7 (garment ingestion + production readiness)
3. **Risk Mitigation**: Azure AI Vision accuracy is the highest technical risk — T043/T044 should be spiked early in Sprint 1 to validate feasibility

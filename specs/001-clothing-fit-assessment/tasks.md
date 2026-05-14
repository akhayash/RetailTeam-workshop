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

- [ ] T001 Create solution file and project structure per implementation plan at src/VirtualMirror.sln
- [ ] T002 Create VirtualMirror.Core class library project at src/VirtualMirror.Core/VirtualMirror.Core.csproj
- [ ] T003 [P] Create VirtualMirror.Services class library project at src/VirtualMirror.Services/VirtualMirror.Services.csproj
- [ ] T004 [P] Create VirtualMirror.Infrastructure class library project at src/VirtualMirror.Infrastructure/VirtualMirror.Infrastructure.csproj
- [ ] T005 Create VirtualMirror.Api web project with ASP.NET Core 8.0 at src/VirtualMirror.Api/VirtualMirror.Api.csproj
- [ ] T006 Create VirtualMirror.AppHost Aspire orchestrator project at src/VirtualMirror.AppHost/VirtualMirror.AppHost.csproj
- [ ] T007 [P] Create test projects (xUnit) at tests/VirtualMirror.Core.Tests, tests/VirtualMirror.Services.Tests, tests/VirtualMirror.Api.Tests, tests/VirtualMirror.Infrastructure.Tests, tests/VirtualMirror.Contract.Tests, tests/VirtualMirror.Load.Tests
- [ ] T008 [P] Add NuGet dependencies: Azure.AI.OpenAI, Azure.AI.Vision.ImageAnalysis, Azure.AI.ContentSafety, Azure.Identity, Microsoft.Azure.Cosmos, Azure.Storage.Blobs, Swashbuckle.AspNetCore to appropriate projects
- [ ] T009 [P] Add test NuGet dependencies: xUnit, FluentAssertions, NSubstitute, Microsoft.AspNetCore.Mvc.Testing, Verify.Xunit, NBomber to test projects
- [ ] T010 [P] Configure Directory.Build.props for shared build settings (nullable, implicit usings, TreatWarningsAsErrors) at src/Directory.Build.props
- [ ] T011 [P] Create .editorconfig for C# coding conventions at root .editorconfig
- [ ] T012 [P] Create docker-compose.yml for local development (Cosmos DB emulator + Azurite) at docker-compose.yml

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T013 Define FitScale enum (TooTight, SlightlyTight, GoodFit, SlightlyLoose, TooLoose) at src/VirtualMirror.Core/Enums/FitScale.cs
- [ ] T014 [P] Define GarmentCategory enum (Top, Bottom, Dress, Outerwear, Underwear) at src/VirtualMirror.Core/Enums/GarmentCategory.cs
- [ ] T015 [P] Define GarmentFitType enum (Slim, Regular, Relaxed) at src/VirtualMirror.Core/Enums/GarmentFitType.cs
- [ ] T016 [P] Define TenantStatus enum (Onboarding, Active, Suspended) at src/VirtualMirror.Core/Enums/TenantStatus.cs
- [ ] T017 [P] Define RateLimitTier enum (Basic, Standard, Premium) at src/VirtualMirror.Core/Enums/RateLimitTier.cs
- [ ] T018 Create Tenant domain model at src/VirtualMirror.Core/Models/Tenant.cs
- [ ] T019 [P] Create BodyMeasurements value object at src/VirtualMirror.Core/Models/BodyMeasurements.cs
- [ ] T020 [P] Create GarmentMeasurements value object at src/VirtualMirror.Core/Models/GarmentMeasurements.cs
- [ ] T021 [P] Create AreaScores value object at src/VirtualMirror.Core/Models/AreaScores.cs
- [ ] T022 Create ShopperProfile domain model at src/VirtualMirror.Core/Models/ShopperProfile.cs
- [ ] T023 [P] Create Garment domain model at src/VirtualMirror.Core/Models/Garment.cs
- [ ] T024 [P] Create VirtualMirrormentResult domain model at src/VirtualMirror.Core/Models/VirtualMirrormentResult.cs
- [ ] T025 Define ITenantContext interface for multi-tenant scoping at src/VirtualMirror.Core/Interfaces/ITenantContext.cs
- [ ] T026 [P] Define ICosmosRepository<T> generic repository interface at src/VirtualMirror.Core/Interfaces/ICosmosRepository.cs
- [ ] T027 [P] Define IImageValidator interface at src/VirtualMirror.Core/Interfaces/IImageValidator.cs
- [ ] T028 [P] Define IBodyMeasurementExtractor interface at src/VirtualMirror.Core/Interfaces/IBodyMeasurementExtractor.cs
- [ ] T028a [P] Define IOpenAIMeasurementClient interface for GPT-5.2 Vision measurement extraction at src/VirtualMirror.Core/Interfaces/IOpenAIMeasurementClient.cs
- [ ] T028b [P] Define IContentSafetyClient interface for Azure AI Content Safety at src/VirtualMirror.Core/Interfaces/IContentSafetyClient.cs
- [ ] T029 [P] Define IFitComparisonEngine interface at src/VirtualMirror.Core/Interfaces/IFitComparisonEngine.cs
- [ ] T030 [P] Define IBlobStorageService interface at src/VirtualMirror.Core/Interfaces/IBlobStorageService.cs
- [ ] T030a [P] Define IAuditLogger interface for immutable audit trail at src/VirtualMirror.Core/Interfaces/IAuditLogger.cs
- [ ] T030b [P] Define IAssessmentQueue interface for async request queuing at src/VirtualMirror.Core/Interfaces/IAssessmentQueue.cs
- [ ] T031 Implement CosmosRepository<T> base class with tenant-scoped queries at src/VirtualMirror.Infrastructure/Cosmos/CosmosRepository.cs
- [ ] T032 [P] Implement TenantContext middleware that extracts tenant ID from JWT claims at src/VirtualMirror.Api/Middleware/TenantContextMiddleware.cs
- [ ] T033 [P] Implement CorrelationIdMiddleware for request tracing at src/VirtualMirror.Api/Middleware/CorrelationIdMiddleware.cs
- [ ] T034 Configure Microsoft Entra ID JWT authentication in Program.cs at src/VirtualMirror.Api/Program.cs
- [ ] T035 [P] Implement global exception handling filter at src/VirtualMirror.Api/Filters/GlobalExceptionFilter.cs
- [ ] T036 [P] Implement request validation filter using FluentValidation at src/VirtualMirror.Api/Filters/ValidationFilter.cs
- [ ] T037 [P] Implement rate limiting middleware per tenant tier at src/VirtualMirror.Api/Middleware/RateLimitingMiddleware.cs
- [ ] T038 Configure OpenTelemetry (traces, metrics, logs) export to Azure Monitor at src/VirtualMirror.Api/Program.cs
- [ ] T038a Implement AuditLogger service writing immutable audit entries (model version, shopper ref, tenant, timestamp) to dedicated Cosmos container at src/VirtualMirror.Infrastructure/Cosmos/AuditLogger.cs
- [ ] T038b Configure Azure App Configuration feature flag integration for progressive rollouts at src/VirtualMirror.Infrastructure/Configuration/FeatureFlagService.cs
- [ ] T038c Implement AssessmentQueueService using Azure Service Bus for async request queuing under high load at src/VirtualMirror.Infrastructure/Messaging/AssessmentQueueService.cs
- [ ] T039 [P] Implement BlobStorageService with transient upload and auto-purge at src/VirtualMirror.Infrastructure/BlobStorage/BlobStorageService.cs
- [ ] T040 [P] Configure Aspire AppHost with Cosmos DB, Blob Storage, Azure OpenAI, Azure AI Content Safety, Azure Service Bus, and API references at src/VirtualMirror.AppHost/Program.cs
- [ ] T041 Implement health check endpoint with Cosmos DB, Blob, and AI model checks at src/VirtualMirror.Api/Controllers/HealthController.cs

**Checkpoint**: Foundation ready — user story implementation can now begin in parallel

---

## Phase 3: User Story 1 — Photo-Based Fit Assessment (Priority: P1) 🎯 MVP

**Goal**: A shopper uploads a photo and receives a personalized 5-point fit recommendation per body area within 5 seconds

**Independent Test**: POST /api/v1/assessments with a photo, height, and garment ID returns a structured fit response with confidence score

**TDD Enforcement**: For each implementation task below, write the corresponding unit/integration test FIRST (Red), then implement to pass (Green), then refactor. Test tasks (T059–T062) define the expected behavior; write them before T042–T056.

- [ ] T042 [US1] Implement ImageValidator service (format, size, MIME type validation, luminance check, bounding box coverage ≥ 70% frame height) at src/VirtualMirror.Services/ImageProcessing/ImageValidator.cs
- [ ] T042a [US1] Implement minor/age detection using Azure AI Content Safety in ImageValidator — reject images detected as under-16 with age-appropriate message at src/VirtualMirror.Services/ImageProcessing/ImageValidator.cs
- [ ] T042b [US1] Implement multi-person detection using Azure AI Vision 4.0 People Detection in ImageValidator — reject images with multiple people at src/VirtualMirror.Services/ImageProcessing/ImageValidator.cs
- [ ] T042c [US1] Integrate malware scanning for uploaded images (Microsoft Defender for Storage or ClamAV sidecar) before AI processing at src/VirtualMirror.Services/ImageProcessing/ImageValidator.cs
- [ ] T043 [US1] Implement AzureAIVisionClient wrapper for people detection (bounding box, multi-person check) at src/VirtualMirror.Infrastructure/AzureAI/AzureAIVisionClient.cs
- [ ] T043a [US1] Implement ContentSafetyClient wrapper for Azure AI Content Safety (minor detection, inappropriate content) at src/VirtualMirror.Infrastructure/AzureAI/ContentSafetyClient.cs
- [ ] T043b [US1] Implement AzureOpenAIMeasurementClient wrapper for GPT-5.2 Vision native structured output — sends photo + height, receives body measurements JSON at src/VirtualMirror.Infrastructure/AzureAI/AzureOpenAIMeasurementClient.cs
- [ ] T043c [US1] Create and version-control the measurement extraction prompt template (system + user prompt with structured output schema) at src/VirtualMirror.Infrastructure/AzureAI/Prompts/MeasurementExtractionPrompt.cs
- [ ] T044 [US1] Implement BodyMeasurementExtractor that orchestrates GPT-5.2 call with height normalization and confidence calibration at src/VirtualMirror.Services/ImageProcessing/BodyMeasurementExtractor.cs
- [ ] T045 [US1] Implement FitComparisonEngine with tolerance band logic per fit type at src/VirtualMirror.Services/Assessment/FitComparisonEngine.cs
- [ ] T046 [US1] Implement VirtualMirrormentService orchestrating the full assessment pipeline at src/VirtualMirror.Services/Assessment/VirtualMirrormentService.cs
- [ ] T047 [US1] Implement AssessmentsController with POST /api/v1/assessments and GET /api/v1/assessments/{assessmentId} endpoints at src/VirtualMirror.Api/Controllers/AssessmentsController.cs
- [ ] T048 [US1] Implement CreateAssessmentRequest DTO with validation (including mandatory heightCm: 100-250 cm) at src/VirtualMirror.Api/Models/CreateAssessmentRequest.cs
- [ ] T049 [P] [US1] Implement VirtualMirrormentResponse DTO mapping at src/VirtualMirror.Api/Models/VirtualMirrormentResponse.cs
- [ ] T050 [P] [US1] Implement ImageQualityError response model at src/VirtualMirror.Api/Models/ImageQualityError.cs
- [ ] T051 [P] [US1] Implement FallbackResponse for graceful degradation at src/VirtualMirror.Api/Models/FallbackResponse.cs
- [ ] T052 [US1] Implement AssessmentRepository (Cosmos DB) for storing results at src/VirtualMirror.Infrastructure/Cosmos/AssessmentRepository.cs
- [ ] T053 [US1] Implement GarmentRepository (Cosmos DB) for garment lookups at src/VirtualMirror.Infrastructure/Cosmos/GarmentRepository.cs
- [ ] T054 [US1] Add graceful degradation logic when AI model is unavailable in VirtualMirrormentService at src/VirtualMirror.Services/Assessment/VirtualMirrormentService.cs
- [ ] T055 [US1] Add low-confidence threshold check (< 70%) with disclaimer and escalation URI (e.g., tenant-configured support URL) in response at src/VirtualMirror.Services/Assessment/VirtualMirrormentService.cs
- [ ] T055a [US1] Integrate AuditLogger into VirtualMirrormentService — log every assessment with model version, tenant, shopper ref, and correlation ID at src/VirtualMirror.Services/Assessment/VirtualMirrormentService.cs
- [ ] T055b [US1] Implement queued assessment flow — when load exceeds threshold, enqueue via AssessmentQueueService and return HTTP 202 with poll URL at src/VirtualMirror.Services/Assessment/VirtualMirrormentService.cs
- [ ] T056 [US1] Wire up dependency injection for US1 services in Program.cs at src/VirtualMirror.Api/Program.cs
- [ ] T057 [US1] Create sample garment test fixture data for integration tests at tests/VirtualMirror.Api.Tests/Fixtures/SampleGarments.cs
- [ ] T058 [US1] Create sample photo test fixture (valid full-body image) at tests/VirtualMirror.Api.Tests/Fixtures/sample-photo.jpg
- [ ] T059 [US1] Write integration tests for POST /api/v1/assessments (happy path, bad image, low confidence) at tests/VirtualMirror.Api.Tests/AssessmentsControllerTests.cs
- [ ] T060 [P] [US1] Write unit tests for FitComparisonEngine tolerance band logic at tests/VirtualMirror.Services.Tests/Assessment/FitComparisonEngineTests.cs
- [ ] T061 [P] [US1] Write unit tests for ImageValidator at tests/VirtualMirror.Services.Tests/ImageProcessing/ImageValidatorTests.cs
- [ ] T062 [P] [US1] Write unit tests for BodyMeasurementExtractor at tests/VirtualMirror.Services.Tests/ImageProcessing/BodyMeasurementExtractorTests.cs

---

## Phase 4: User Story 2 — Measurement Profile Storage (Priority: P2)

**Goal**: A returning shopper can save their body measurements and get fit recommendations without re-uploading a photo

**Independent Test**: Complete assessment via US1 with saveProfile=true, then POST /api/v1/assessments/by-profile returns fit result using stored measurements

**TDD Enforcement**: Write T072–T073 test expectations FIRST, then implement T063–T071.

- [ ] T063 [US2] Implement ProfileRepository (Cosmos DB) for shopper profiles at src/VirtualMirror.Infrastructure/Cosmos/ProfileRepository.cs
- [ ] T064 [US2] Implement ShopperProfileService with save, get, and delete operations at src/VirtualMirror.Services/Profiles/ShopperProfileService.cs
- [ ] T065 [US2] Implement ProfilesController with GET and DELETE /api/v1/profiles/{shopperRef} at src/VirtualMirror.Api/Controllers/ProfilesController.cs
- [ ] T066 [US2] Add saveProfile logic to VirtualMirrormentService (persist measurements when flag is true) at src/VirtualMirror.Services/Assessment/VirtualMirrormentService.cs
- [ ] T067 [US2] Implement POST /api/v1/assessments/by-profile endpoint in AssessmentsController at src/VirtualMirror.Api/Controllers/AssessmentsController.cs
- [ ] T068 [US2] Implement profile deletion with 24-hour fulfillment guarantee and audit log at src/VirtualMirror.Services/Profiles/ShopperProfileService.cs
- [ ] T069 [P] [US2] Implement ShopperProfileResponse DTO at src/VirtualMirror.Api/Models/ShopperProfileResponse.cs
- [ ] T070 [P] [US2] Implement DeletionAccepted response DTO at src/VirtualMirror.Api/Models/DeletionAccepted.cs
- [ ] T071 [US2] Wire up dependency injection for US2 services in Program.cs at src/VirtualMirror.Api/Program.cs
- [ ] T072 [US2] Write integration tests for profile CRUD and assessment-by-profile at tests/VirtualMirror.Api.Tests/ProfilesControllerTests.cs
- [ ] T073 [P] [US2] Write unit tests for ShopperProfileService at tests/VirtualMirror.Services.Tests/Profiles/ShopperProfileServiceTests.cs

---

## Phase 5: User Story 3 — Frontend Integration Layer (Priority: P2)

**Goal**: A retail frontend team can integrate via a well-documented, authenticated API with proper error handling and OpenAPI documentation

**Independent Test**: API endpoints return correct OpenAPI schema; auth rejection returns 401 with no data leakage; rate limiting responds with 429 and Retry-After header

**TDD Enforcement**: Write T079–T081 contract and integration tests FIRST, then implement T074–T078.

- [ ] T074 [US3] Configure Swashbuckle for OpenAPI 3.x generation with Entra ID security scheme at src/VirtualMirror.Api/Program.cs
- [ ] T075 [US3] Add XML documentation comments to all controller actions for OpenAPI descriptions at src/VirtualMirror.Api/Controllers/*.cs
- [ ] T076 [US3] Implement API versioning (v1) using ASP.NET Core API Versioning package at src/VirtualMirror.Api/Program.cs
- [ ] T077 [US3] Configure CORS policy for frontend origins at src/VirtualMirror.Api/Program.cs
- [ ] T078 [P] [US3] Implement AssessmentQueued response for high-load scenarios (HTTP 202) at src/VirtualMirror.Api/Models/AssessmentQueued.cs
- [ ] T079 [US3] Write contract tests validating generated OpenAPI matches contracts/openapi.yaml at tests/VirtualMirror.Contract.Tests/OpenApiContractTests.cs
- [ ] T080 [P] [US3] Write integration tests for auth rejection (401) and rate limiting (429) at tests/VirtualMirror.Api.Tests/SecurityIntegrationTests.cs
- [ ] T081 [P] [US3] Write integration tests for graceful degradation (503 with fallback) at tests/VirtualMirror.Api.Tests/ResilienceIntegrationTests.cs

---

## Phase 6: User Story 4 — Garment Data Ingestion (Priority: P3)

**Goal**: A retail operations team can onboard garment catalog data with size measurements per SKU

**Independent Test**: POST /api/v1/garments creates a garment; POST /api/v1/garments/batch bulk-creates; GET /api/v1/garments lists with pagination

**TDD Enforcement**: Write T089–T090 tests FIRST, then implement T082–T088.

- [ ] T082 [US4] Implement GarmentService with upsert, batch upsert, and list operations at src/VirtualMirror.Services/Garments/GarmentService.cs
- [ ] T083 [US4] Implement GarmentsController with POST, GET, and batch endpoints at src/VirtualMirror.Api/Controllers/GarmentsController.cs
- [ ] T084 [US4] Implement GarmentUpsertRequest DTO with FluentValidation rules at src/VirtualMirror.Api/Models/GarmentUpsertRequest.cs
- [ ] T085 [P] [US4] Implement GarmentResponse and GarmentListResponse DTOs at src/VirtualMirror.Api/Models/GarmentResponse.cs
- [ ] T086 [P] [US4] Implement BatchUpsertResponse DTO at src/VirtualMirror.Api/Models/BatchUpsertResponse.cs
- [ ] T087 [US4] Add garment version tracking on update in GarmentRepository at src/VirtualMirror.Infrastructure/Cosmos/GarmentRepository.cs
- [ ] T088 [US4] Wire up dependency injection for US4 services in Program.cs at src/VirtualMirror.Api/Program.cs
- [ ] T089 [US4] Write integration tests for garment CRUD and batch operations at tests/VirtualMirror.Api.Tests/GarmentsControllerTests.cs
- [ ] T090 [P] [US4] Write unit tests for GarmentService validation logic at tests/VirtualMirror.Services.Tests/Garments/GarmentServiceTests.cs

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
- [ ] T096b [P] Create Bicep module for Azure OpenAI resource with GPT-5.2 deployment at infra/modules/openai.bicep
- [ ] T096c [P] Create Bicep module for Azure AI Content Safety resource at infra/modules/content-safety.bicep
- [ ] T097 Create dev/staging/prod parameter files at infra/parameters/dev.json, staging.json, prod.json
- [ ] T098 Create GitHub Actions CI workflow (build, test, SAST/SCA scan, DAST scan against staging, code coverage gates ≥ 80%/90% critical paths, SBOM generation via CycloneDX, container image scanning via Trivy, container signing via Notation/cosign, deploy) at .github/workflows/ci.yml
- [ ] T099 [P] Create Dockerfile for VirtualMirror.Api at src/VirtualMirror.Api/Dockerfile
- [ ] T100 [P] Create .dockerignore at root .dockerignore
- [ ] T101 [P] Configure Azure Monitor alert rules for SLO violations in Bicep at infra/modules/alerts.bicep
- [ ] T101a [P] Create operational runbooks for each alert rule (p95 latency, error rate, confidence drift, availability SLO) at docs/runbooks/
- [ ] T102 Write NBomber load test simulating 500 concurrent assessments at tests/VirtualMirror.Load.Tests/ConcurrentAssessmentLoadTest.cs
- [ ] T102a Write end-to-end smoke tests validating the full user journey (upload → assess → profile save → assess-by-profile) against staging environment at tests/VirtualMirror.Api.Tests/E2E/SmokeTests.cs
- [ ] T103 Create README.md with project overview, setup instructions, and architecture diagram at README.md
- [ ] T104 [P] Create model card for GPT-5.2 Vision measurement extraction documenting intended use, accuracy bounds (±2-4cm under validation, expected improvement with GPT-5.2), limitations, known biases, and training data provenance at docs/model-card.md
- [ ] T105 [P] Apply data classification tags to all Azure resources in Bicep modules (Cosmos DB: Confidential, Blob Storage: Restricted, Logs: Internal, AI services: Confidential) at infra/modules/*.bicep
- [ ] T106 [P] Create disaster recovery plan and test procedures documenting RPO/RTO validation at docs/dr-plan.md

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
3. **Risk Mitigation**: GPT-5.2 Vision measurement accuracy is the highest technical risk — T043b/T044 should be spiked early in Sprint 1 to validate feasibility with known-height test images

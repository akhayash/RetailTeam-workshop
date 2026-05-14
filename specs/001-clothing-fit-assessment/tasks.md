# Tasks: AI Clothing Fit Assessment Agent

**Input**: Design documents from `/specs/001-clothing-fit-assessment/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/openapi.yaml, quickstart.md

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
- [ ] T008 [P] Add NuGet dependencies: Azure.AI.OpenAI, Azure.AI.Inference, Azure.AI.ContentSafety, Azure.Identity, Microsoft.Azure.Cosmos, Azure.Storage.Blobs, Azure.Messaging.ServiceBus, Swashbuckle.AspNetCore, Microsoft.Extensions.Http.Resilience, Microsoft.Extensions.Diagnostics.HealthChecks to appropriate projects
- [ ] T009 [P] Add test NuGet dependencies: xUnit, FluentAssertions, NSubstitute, Microsoft.AspNetCore.Mvc.Testing, Verify.Xunit, NBomber to test projects
- [ ] T010 [P] Configure Directory.Build.props for shared build settings (nullable, implicit usings, TreatWarningsAsErrors) at src/Directory.Build.props
- [ ] T011 [P] Create .editorconfig for C# coding conventions at root .editorconfig
- [ ] T012 [P] Create docker-compose.yml for local development (Cosmos DB emulator + Azurite) at docker-compose.yml

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure, domain models, interfaces, resilience plumbing — MUST be complete before ANY user story

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Domain Models & Enums

- [ ] T013 Define FitScale enum (TooTight, SlightlyTight, GoodFit, SlightlyLoose, TooLoose) at src/VirtualMirror.Core/Enums/FitScale.cs
- [ ] T014 [P] Define GarmentCategory enum (Top, Bottom, Dress, Outerwear, Underwear) at src/VirtualMirror.Core/Enums/GarmentCategory.cs
- [ ] T015 [P] Define GarmentFitType enum (Slim, Regular, Relaxed) at src/VirtualMirror.Core/Enums/GarmentFitType.cs
- [ ] T016 [P] Define TenantStatus enum (Onboarding, Active, Suspended) at src/VirtualMirror.Core/Enums/TenantStatus.cs
- [ ] T017 [P] Define RateLimitTier enum (Basic, Standard, Premium) at src/VirtualMirror.Core/Enums/RateLimitTier.cs
- [ ] T018 Create Tenant domain model with ToleranceBands sub-object at src/VirtualMirror.Core/Models/Tenant.cs
- [ ] T019 [P] Create BodyMeasurements value object (shoulderWidth, chestCircumference, waistCircumference, hipCircumference, height, inseam, armLength) at src/VirtualMirror.Core/Models/BodyMeasurements.cs
- [ ] T020 [P] Create GarmentMeasurements value object (shoulderWidth, chestCircumference, waistCircumference, hipCircumference, length, inseam, sleeveLength) at src/VirtualMirror.Core/Models/GarmentMeasurements.cs
- [ ] T021 [P] Create AreaScores value object (shoulders, chest, waist, hips, length as FitScale) at src/VirtualMirror.Core/Models/AreaScores.cs
- [ ] T022 Create ShopperProfile domain model at src/VirtualMirror.Core/Models/ShopperProfile.cs
- [ ] T023 [P] Create Garment domain model with version tracking at src/VirtualMirror.Core/Models/Garment.cs
- [ ] T024 [P] Create VirtualMirrormentResult domain model at src/VirtualMirror.Core/Models/VirtualMirrormentResult.cs

### Interfaces

- [ ] T025 Define ITenantContext interface for multi-tenant scoping at src/VirtualMirror.Core/Interfaces/ITenantContext.cs
- [ ] T026 [P] Define ICosmosRepository<T> generic repository interface at src/VirtualMirror.Core/Interfaces/ICosmosRepository.cs
- [ ] T027 [P] Define IImageValidator interface at src/VirtualMirror.Core/Interfaces/IImageValidator.cs
- [ ] T028 [P] Define IBodyMeasurementExtractor interface at src/VirtualMirror.Core/Interfaces/IBodyMeasurementExtractor.cs
- [ ] T029 [P] Define IOpenAIMeasurementClient interface for GPT-5.2 Vision at src/VirtualMirror.Core/Interfaces/IOpenAIMeasurementClient.cs
- [ ] T030 [P] Define IContentSafetyClient interface for Azure AI Content Safety at src/VirtualMirror.Core/Interfaces/IContentSafetyClient.cs
- [ ] T031 [P] Define IFitComparisonEngine interface at src/VirtualMirror.Core/Interfaces/IFitComparisonEngine.cs
- [ ] T032 [P] Define IBlobStorageService interface at src/VirtualMirror.Core/Interfaces/IBlobStorageService.cs
- [ ] T033 [P] Define IAuditLogger interface for immutable audit trail at src/VirtualMirror.Core/Interfaces/IAuditLogger.cs
- [ ] T034 [P] Define IAssessmentQueue interface for async request queuing at src/VirtualMirror.Core/Interfaces/IAssessmentQueue.cs
- [ ] T035 [P] Define IFlorenceVisionClient interface for Florence-2 at src/VirtualMirror.Core/Interfaces/IFlorenceVisionClient.cs

### Infrastructure — Data & Messaging

- [ ] T036 Implement CosmosRepository<T> base class with tenant-scoped queries and hierarchical partition keys at src/VirtualMirror.Infrastructure/Cosmos/CosmosRepository.cs
- [ ] T037 [P] Implement BlobStorageService with transient upload and 60s auto-purge at src/VirtualMirror.Infrastructure/BlobStorage/BlobStorageService.cs
- [ ] T038 [P] Implement AuditLogger service writing immutable entries to dedicated Cosmos container at src/VirtualMirror.Infrastructure/Cosmos/AuditLogger.cs
- [ ] T039 [P] Implement AssessmentQueueService using Azure Service Bus for async queuing under load at src/VirtualMirror.Infrastructure/Messaging/AssessmentQueueService.cs
- [ ] T040 [P] Implement DeadLetterQueueProcessor background service (max delivery = 3, alerting, retry) at src/VirtualMirror.Infrastructure/Messaging/DeadLetterQueueProcessor.cs

### Infrastructure — Resilience

- [ ] T041 Implement Polly resilience pipeline for Florence-2 (timeout 3s, retry 2x exponential+jitter, CB open after 5 failures/30s) at src/VirtualMirror.Infrastructure/Resilience/FlorenceResiliencePipeline.cs
- [ ] T042 [P] Implement Polly resilience pipeline for GPT-5.2 Vision (timeout 8s, retry 1x, CB open after 3 failures/60s) at src/VirtualMirror.Infrastructure/Resilience/OpenAIResiliencePipeline.cs
- [ ] T043 [P] Implement Polly resilience pipeline for Content Safety (timeout 2s, retry 1x, CB open after 5 failures/30s) at src/VirtualMirror.Infrastructure/Resilience/ContentSafetyResiliencePipeline.cs
- [ ] T044 [P] Implement Polly resilience pipeline for Service Bus (timeout 3s, retry 3x exponential, CB open after 10 failures/60s) at src/VirtualMirror.Infrastructure/Resilience/ServiceBusResiliencePipeline.cs
- [ ] T045 Implement AI failover client for GPT-5.2 (primary/secondary endpoint with health-check switching) at src/VirtualMirror.Infrastructure/Resilience/OpenAIFailoverClient.cs
- [ ] T046 [P] Implement AI failover client for Florence-2 (primary/secondary endpoint with health-check switching) at src/VirtualMirror.Infrastructure/Resilience/FlorenceFailoverClient.cs
- [ ] T047 [P] Implement end-to-end request timeout budget middleware (12s cap) at src/VirtualMirror.Api/Middleware/RequestTimeoutMiddleware.cs

### API Middleware & Cross-Cutting

- [ ] T048 Implement TenantContext middleware extracting tenant ID from JWT claims at src/VirtualMirror.Api/Middleware/TenantContextMiddleware.cs
- [ ] T049 [P] Implement CorrelationIdMiddleware for request tracing at src/VirtualMirror.Api/Middleware/CorrelationIdMiddleware.cs
- [ ] T050 [P] Implement TenantBulkheadMiddleware (per-tenant SemaphoreSlim concurrency limiter) at src/VirtualMirror.Api/Middleware/TenantBulkheadMiddleware.cs
- [ ] T051 Configure Microsoft Entra ID JWT authentication in Program.cs at src/VirtualMirror.Api/Program.cs
- [ ] T052 [P] Implement global exception handling filter at src/VirtualMirror.Api/Filters/GlobalExceptionFilter.cs
- [ ] T053 [P] Implement request validation filter using FluentValidation at src/VirtualMirror.Api/Filters/ValidationFilter.cs
- [ ] T054 [P] Implement rate limiting middleware per tenant tier (Basic: 100/min, Standard: 500/min, Premium: 2000/min) at src/VirtualMirror.Api/Middleware/RateLimitingMiddleware.cs
- [ ] T055 Configure OpenTelemetry (traces, metrics, logs) export to Azure Monitor at src/VirtualMirror.Api/Program.cs

### Health Probes

- [ ] T056 Implement liveness probe at /health/live (process alive, no dependency checks) at src/VirtualMirror.Api/HealthChecks/LivenessCheck.cs
- [ ] T057 [P] Implement readiness probe at /health/ready (Cosmos DB + Azure OpenAI + Florence-2 reachable) at src/VirtualMirror.Api/HealthChecks/ReadinessCheck.cs
- [ ] T058 [P] Implement startup probe at /health/startup (longer timeout for AI SDK initialization) at src/VirtualMirror.Api/HealthChecks/StartupCheck.cs
- [ ] T059 Register health check endpoints in Program.cs (MapHealthChecks with liveness/readiness/startup paths) at src/VirtualMirror.Api/Program.cs

### Configuration & Orchestration

- [ ] T060 Configure Azure App Configuration feature flag integration at src/VirtualMirror.Infrastructure/Configuration/FeatureFlagService.cs
- [ ] T061 [P] Configure Aspire AppHost with Cosmos DB, Blob Storage, Azure OpenAI, Florence-2, Content Safety, Service Bus at src/VirtualMirror.AppHost/Program.cs
- [ ] T062 Register all resilience pipelines and DI services in Program.cs at src/VirtualMirror.Api/Program.cs

**Checkpoint**: Foundation ready — resilience pipelines active, health probes responding, user story implementation can begin

---

## Phase 3: User Story 1 — Photo-Based Fit Assessment (Priority: P1) 🎯 MVP

**Goal**: A shopper uploads a photo and receives a personalized 5-point fit recommendation per body area within 5 seconds

**Independent Test**: POST /api/v1/assessments with a photo, height, and garment ID returns a structured fit response with confidence score

**TDD Enforcement**: Write tests (T088–T093) FIRST (Red), then implement to pass (Green), then refactor.

### Implementation

- [ ] T063 [US1] Implement FlorenceVisionClient wrapper for Florence-2 people detection (bounding box, multi-person check) at src/VirtualMirror.Infrastructure/AzureAI/FlorenceVisionClient.cs
- [ ] T064 [P] [US1] Implement ContentSafetyClient wrapper for minor detection and inappropriate content filtering at src/VirtualMirror.Infrastructure/AzureAI/ContentSafetyClient.cs
- [ ] T065 [P] [US1] Implement AzureOpenAIMeasurementClient wrapper for GPT-5.2 Vision native structured output at src/VirtualMirror.Infrastructure/AzureAI/AzureOpenAIMeasurementClient.cs
- [ ] T066 [P] [US1] Create and version-control the measurement extraction prompt template (system + user with JSON schema) at src/VirtualMirror.Infrastructure/AzureAI/Prompts/MeasurementExtractionPrompt.cs
- [ ] T067 [US1] Implement ImageValidator service (format, size, MIME, luminance ≥ 40, bounding box ≥ 70% frame height) at src/VirtualMirror.Services/ImageProcessing/ImageValidator.cs
- [ ] T068 [US1] Integrate minor/age detection in ImageValidator — reject under-16 with age-appropriate message at src/VirtualMirror.Services/ImageProcessing/ImageValidator.cs
- [ ] T069 [US1] Integrate multi-person detection using Florence-2 in ImageValidator at src/VirtualMirror.Services/ImageProcessing/ImageValidator.cs
- [ ] T070 [US1] Integrate malware scanning (Microsoft Defender for Storage or ClamAV sidecar) at src/VirtualMirror.Services/ImageProcessing/ImageValidator.cs
- [ ] T071 [US1] Implement BodyMeasurementExtractor orchestrating GPT-5.2 with height normalization and confidence calibration at src/VirtualMirror.Services/ImageProcessing/BodyMeasurementExtractor.cs
- [ ] T072 [US1] Implement FitComparisonEngine with configurable tolerance bands per tenant and garment category at src/VirtualMirror.Services/Assessment/FitComparisonEngine.cs
- [ ] T073 [US1] Implement VirtualMirrormentService orchestrating the full assessment pipeline (validate → extract → compare → audit) at src/VirtualMirror.Services/Assessment/VirtualMirrormentService.cs
- [ ] T074 [US1] Implement degradation ladder in VirtualMirrormentService (L1–L5 failure modes mapped to responses) at src/VirtualMirror.Services/Assessment/VirtualMirrormentService.cs
- [ ] T075 [US1] Add low-confidence threshold check (< 70%) with disclaimer and escalation URI at src/VirtualMirror.Services/Assessment/VirtualMirrormentService.cs
- [ ] T076 [US1] Integrate AuditLogger — log every assessment with model version, tenant, shopperRef, correlationId at src/VirtualMirror.Services/Assessment/VirtualMirrormentService.cs
- [ ] T077 [US1] Implement queued assessment flow — enqueue via Service Bus when load > threshold, return HTTP 202 + poll URL at src/VirtualMirror.Services/Assessment/VirtualMirrormentService.cs
- [ ] T078 [US1] Implement AssessmentsController with POST /api/v1/assessments and GET /api/v1/assessments/{assessmentId} at src/VirtualMirror.Api/Controllers/AssessmentsController.cs
- [ ] T079 [P] [US1] Implement CreateAssessmentRequest DTO with validation (mandatory heightCm: 100–250 cm, image ≤ 10 MB) at src/VirtualMirror.Api/Models/CreateAssessmentRequest.cs
- [ ] T080 [P] [US1] Implement VirtualMirrormentResponse DTO (assessmentId, overallRecommendation, areaScores, confidence, modelVersion, degradation flags) at src/VirtualMirror.Api/Models/VirtualMirrormentResponse.cs
- [ ] T081 [P] [US1] Implement ImageQualityError response model with actionable guidance at src/VirtualMirror.Api/Models/ImageQualityError.cs
- [ ] T082 [P] [US1] Implement FallbackResponse for graceful degradation (size chart URL, garment data) at src/VirtualMirror.Api/Models/FallbackResponse.cs
- [ ] T083 [US1] Implement AssessmentRepository (Cosmos DB, TTL 365 days, partition /tenantId) at src/VirtualMirror.Infrastructure/Cosmos/AssessmentRepository.cs
- [ ] T084 [US1] Implement GarmentRepository (Cosmos DB, partition /tenantId) for garment lookups at src/VirtualMirror.Infrastructure/Cosmos/GarmentRepository.cs
- [ ] T085 [US1] Wire up dependency injection for US1 services in Program.cs at src/VirtualMirror.Api/Program.cs

### Test Fixtures & Tests

- [ ] T086 [US1] Create sample garment test fixture data at tests/VirtualMirror.Api.Tests/Fixtures/SampleGarments.cs
- [ ] T087 [P] [US1] Create sample photo test fixture (valid full-body image) at tests/VirtualMirror.Api.Tests/Fixtures/sample-photo.jpg
- [ ] T088 [US1] Write integration tests for POST /api/v1/assessments (happy path, bad image, low confidence, degraded mode) at tests/VirtualMirror.Api.Tests/AssessmentsControllerTests.cs
- [ ] T089 [P] [US1] Write unit tests for FitComparisonEngine tolerance band logic (all 5 FitScale outcomes) at tests/VirtualMirror.Services.Tests/Assessment/FitComparisonEngineTests.cs
- [ ] T090 [P] [US1] Write unit tests for ImageValidator (format, size, luminance, multi-person, minor detection) at tests/VirtualMirror.Services.Tests/ImageProcessing/ImageValidatorTests.cs
- [ ] T091 [P] [US1] Write unit tests for BodyMeasurementExtractor (confidence calibration, height normalization) at tests/VirtualMirror.Services.Tests/ImageProcessing/BodyMeasurementExtractorTests.cs
- [ ] T092 [P] [US1] Write unit tests for degradation ladder (L1–L5 failure scenarios) at tests/VirtualMirror.Services.Tests/Assessment/DegradationLadderTests.cs
- [ ] T093 [P] [US1] Write integration tests for AI failover (primary down → secondary used) at tests/VirtualMirror.Infrastructure.Tests/Resilience/AIFailoverTests.cs

**Checkpoint**: MVP complete — photo-based fit assessment functional with resilience and degradation

---

## Phase 4: User Story 2 — Measurement Profile Storage (Priority: P2)

**Goal**: A returning shopper can save body measurements and get fit recommendations without re-uploading a photo

**Independent Test**: Complete assessment via US1 with saveProfile=true, then POST /api/v1/assessments/by-profile returns fit result using stored measurements

**TDD Enforcement**: Write T103–T104 tests FIRST, then implement T094–T102.

### Implementation

- [ ] T094 [US2] Implement ProfileRepository (Cosmos DB, partition /tenantId, hard delete) at src/VirtualMirror.Infrastructure/Cosmos/ProfileRepository.cs
- [ ] T095 [US2] Implement ShopperProfileService with save, get, and delete operations at src/VirtualMirror.Services/Profiles/ShopperProfileService.cs
- [ ] T096 [US2] Implement ProfilesController with GET and DELETE /api/v1/profiles/{shopperRef} at src/VirtualMirror.Api/Controllers/ProfilesController.cs
- [ ] T097 [US2] Add saveProfile logic to VirtualMirrormentService (persist measurements when flag is true + consent timestamp) at src/VirtualMirror.Services/Assessment/VirtualMirrormentService.cs
- [ ] T098 [US2] Implement POST /api/v1/assessments/by-profile endpoint in AssessmentsController at src/VirtualMirror.Api/Controllers/AssessmentsController.cs
- [ ] T099 [US2] Implement profile deletion with 24-hour fulfillment guarantee and audit log entry at src/VirtualMirror.Services/Profiles/ShopperProfileService.cs
- [ ] T100 [P] [US2] Implement ShopperProfileResponse DTO at src/VirtualMirror.Api/Models/ShopperProfileResponse.cs
- [ ] T101 [P] [US2] Implement DeletionAccepted response DTO at src/VirtualMirror.Api/Models/DeletionAccepted.cs
- [ ] T102 [US2] Wire up dependency injection for US2 services in Program.cs at src/VirtualMirror.Api/Program.cs

### Tests

- [ ] T103 [US2] Write integration tests for profile CRUD and assessment-by-profile at tests/VirtualMirror.Api.Tests/ProfilesControllerTests.cs
- [ ] T104 [P] [US2] Write unit tests for ShopperProfileService (save, get, delete, consent validation) at tests/VirtualMirror.Services.Tests/Profiles/ShopperProfileServiceTests.cs

**Checkpoint**: Profile storage functional — returning shoppers skip photo re-upload

---

## Phase 5: User Story 3 — Frontend Integration Layer (Priority: P2)

**Goal**: A retail frontend team can integrate via a documented, authenticated API with proper error handling and OpenAPI spec

**Independent Test**: API endpoints return correct OpenAPI schema; auth rejection returns 401; rate limiting returns 429 + Retry-After

**TDD Enforcement**: Write T110–T112 tests FIRST, then implement T105–T109.

### Implementation

- [ ] T105 [US3] Configure Swashbuckle for OpenAPI 3.x generation with Entra ID security scheme at src/VirtualMirror.Api/Program.cs
- [ ] T106 [US3] Add XML documentation comments to all controller actions for OpenAPI descriptions at src/VirtualMirror.Api/Controllers/*.cs
- [ ] T107 [US3] Implement API versioning (v1) using ASP.NET Core API Versioning package at src/VirtualMirror.Api/Program.cs
- [ ] T108 [US3] Configure CORS policy for frontend origins at src/VirtualMirror.Api/Program.cs
- [ ] T109 [P] [US3] Implement AssessmentQueued response DTO for HTTP 202 high-load scenarios at src/VirtualMirror.Api/Models/AssessmentQueued.cs

### Tests

- [ ] T110 [US3] Write contract tests validating generated OpenAPI matches contracts/openapi.yaml at tests/VirtualMirror.Contract.Tests/OpenApiContractTests.cs
- [ ] T111 [P] [US3] Write integration tests for auth rejection (401) and rate limiting (429 + Retry-After) at tests/VirtualMirror.Api.Tests/SecurityIntegrationTests.cs
- [ ] T112 [P] [US3] Write integration tests for graceful degradation responses (503 + fallback body) at tests/VirtualMirror.Api.Tests/ResilienceIntegrationTests.cs

**Checkpoint**: API integration-ready — frontend teams can consume with full documentation

---

## Phase 6: User Story 4 — Garment Data Ingestion (Priority: P3)

**Goal**: A retail operations team can onboard garment catalog with size measurements per SKU

**Independent Test**: POST /api/v1/garments creates a garment; POST /api/v1/garments/batch bulk-creates; GET /api/v1/garments lists with pagination

**TDD Enforcement**: Write T120–T121 tests FIRST, then implement T113–T119.

### Implementation

- [ ] T113 [US4] Implement GarmentService with upsert, batch upsert (max 100), and list operations at src/VirtualMirror.Services/Garments/GarmentService.cs
- [ ] T114 [US4] Implement GarmentsController with POST, GET (paginated), and /batch endpoints at src/VirtualMirror.Api/Controllers/GarmentsController.cs
- [ ] T115 [US4] Implement GarmentUpsertRequest DTO with FluentValidation (brand, category, measurements required) at src/VirtualMirror.Api/Models/GarmentUpsertRequest.cs
- [ ] T116 [P] [US4] Implement GarmentResponse and GarmentListResponse DTOs (with continuationToken) at src/VirtualMirror.Api/Models/GarmentResponse.cs
- [ ] T117 [P] [US4] Implement BatchUpsertResponse DTO (success count, failure details) at src/VirtualMirror.Api/Models/BatchUpsertResponse.cs
- [ ] T118 [US4] Add garment version tracking on update in GarmentRepository at src/VirtualMirror.Infrastructure/Cosmos/GarmentRepository.cs
- [ ] T119 [US4] Wire up dependency injection for US4 services in Program.cs at src/VirtualMirror.Api/Program.cs

### Tests

- [ ] T120 [US4] Write integration tests for garment CRUD and batch operations at tests/VirtualMirror.Api.Tests/GarmentsControllerTests.cs
- [ ] T121 [P] [US4] Write unit tests for GarmentService validation logic at tests/VirtualMirror.Services.Tests/Garments/GarmentServiceTests.cs

**Checkpoint**: Garment ingestion complete — retail teams can onboard catalogs

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Infrastructure as Code, CI/CD, observability, DLQ processing, production readiness

### Infrastructure as Code (Bicep)

- [ ] T122 Create root Bicep template with module references at infra/main.bicep
- [ ] T123 [P] Create Bicep module for Azure Container Apps environment (min 3 replicas, multi-AZ, scale-in stabilization 5 min, KEDA HTTP scaler target 25) at infra/modules/container-app.bicep
- [ ] T124 [P] Create Bicep module for Cosmos DB account with hierarchical partition keys and burst capacity at infra/modules/cosmos-db.bicep
- [ ] T125 [P] Create Bicep module for Storage account (ZRS, blob lifecycle policy 60s TTL) at infra/modules/storage.bicep
- [ ] T126 [P] Create Bicep module for Key Vault at infra/modules/key-vault.bicep
- [ ] T127 [P] Create Bicep module for Entra ID app registration at infra/modules/entra-app.bicep
- [ ] T128 [P] Create Bicep module for Azure Service Bus namespace and queue (DLQ enabled, max delivery 3) at infra/modules/service-bus.bicep
- [ ] T129 [P] Create Bicep module for primary Azure OpenAI resource with GPT-5.2 deployment at infra/modules/openai-primary.bicep
- [ ] T130 [P] Create Bicep module for secondary Azure OpenAI resource (failover) at infra/modules/openai-secondary.bicep
- [ ] T131 [P] Create Bicep module for Azure AI Content Safety resource at infra/modules/content-safety.bicep
- [ ] T132 [P] Create Bicep module for Florence-2 managed endpoints (primary + secondary) at infra/modules/florence-endpoints.bicep
- [ ] T133 Create dev/staging/prod parameter files at infra/parameters/dev.json, staging.json, prod.json

### CI/CD & Deployment

- [ ] T134 Create GitHub Actions CI workflow (build, test, SAST/SCA, code coverage ≥ 80%/90% critical, SBOM via CycloneDX, Trivy scan, Notation sign, deploy) at .github/workflows/ci.yml
- [ ] T135 [P] Create Dockerfile for VirtualMirror.Api at src/VirtualMirror.Api/Dockerfile
- [ ] T136 [P] Create .dockerignore at root .dockerignore

### Observability & Alerting

- [ ] T137 Configure Azure Monitor alert rules for SLO violations (p95 latency > 5s, error rate > 0.1%, availability < 99.9%, Cosmos 429 rate > 1%) at infra/modules/alerts.bicep
- [ ] T138 [P] Create operational runbook for p95 latency alert at docs/runbooks/latency-alert.md
- [ ] T139 [P] Create operational runbook for AI failover alert at docs/runbooks/ai-failover-alert.md
- [ ] T140 [P] Create operational runbook for DLQ depth alert at docs/runbooks/dlq-depth-alert.md

### Load Testing & Validation

- [ ] T141 Write NBomber load test simulating 500 concurrent assessments (validate p95 < 5s, no OOM) at tests/VirtualMirror.Load.Tests/ConcurrentAssessmentLoadTest.cs
- [ ] T142 [P] Write chaos/fault injection tests for degradation ladder (simulate AI outage, verify L1–L5 responses) at tests/VirtualMirror.Load.Tests/ResilienceChaosTests.cs

### Documentation & Compliance

- [ ] T143 Create README.md with project overview, setup instructions, and architecture diagram at README.md
- [ ] T144 [P] Create model card for GPT-5.2 Vision documenting accuracy bounds (±2–4 cm), limitations, bias at docs/model-card.md
- [ ] T145 [P] Apply data classification tags to all Azure resources in Bicep (Cosmos: Confidential, Blob: Restricted, AI: Confidential) at infra/modules/*.bicep
- [ ] T146 [P] Create disaster recovery plan with RPO/RTO validation procedures at docs/dr-plan.md
- [ ] T147 [P] Write end-to-end smoke tests (upload → assess → profile save → assess-by-profile) for staging at tests/VirtualMirror.Api.Tests/E2E/SmokeTests.cs

---

## Dependencies

```text
Phase 1 (Setup)
  └──► Phase 2 (Foundational: models + interfaces + resilience + health probes)
         ├──► Phase 3 (US1: Photo Assessment) 🎯 MVP
         │      └──► Phase 4 (US2: Profile Storage) [depends on US1 pipeline]
         ├──► Phase 5 (US3: Integration Layer) [parallel with US1]
         └──► Phase 6 (US4: Garment Ingestion) [parallel with US1]

Phase 7 (Polish) can start after Phase 2, runs in parallel with Phases 3–6
```

## Parallel Execution Opportunities

### Within Phase 2 (Foundational)

- T013–T017 (all enums) → parallel
- T018–T024 (models, after enums) → T019/T020/T021 parallel, T022/T023/T024 parallel
- T025–T035 (interfaces) → all parallel
- T036–T040 (data infrastructure) → T037/T038/T039/T040 parallel after T036
- T041–T046 (resilience) → T042/T043/T044/T046 parallel after T041
- T048–T054 (middleware) → T049/T050/T052/T053/T054 parallel after T048
- T056–T058 (health probes) → all parallel

### Within Phase 3 (US1)

- T063/T064/T065/T066 (AI clients) → parallel
- T079/T080/T081/T082 (DTOs) → all parallel
- T089/T090/T091/T092/T093 (tests) → all parallel

### Across Phases

- Phase 5 (US3) can start immediately after Phase 2 (no dependency on US1)
- Phase 6 (US4) can start immediately after Phase 2 (uses GarmentRepository from T084)
- Phase 7 (IaC/CI) can start after Phase 2

## Implementation Strategy

1. **MVP Scope**: Phase 1 + Phase 2 + Phase 3 (User Story 1) delivers a working fit assessment API with resilience and degradation
2. **Incremental Delivery**:
   - Sprint 1: Phases 1–2 (project setup + foundation + resilience plumbing)
   - Sprint 2: Phase 3 (MVP — photo-based fit assessment with degradation ladder)
   - Sprint 3: Phases 4 + 5 in parallel (profiles + integration polish)
   - Sprint 4: Phase 6 + Phase 7 (garment ingestion + production readiness)
3. **Risk Mitigation**:
   - H7 (AI failover) validated in Phase 2 before US1 begins
   - H1 (GPT-5.2 accuracy) spiked early via T065/T071 in Sprint 2
   - H8 (degradation ladder) validated via T092/T142 chaos tests
4. **Hypothesis Gates**:
   - H7 must PASS after Phase 2 (AI failover < 5s)
   - H1 must PASS before Phase 3 completion (measurement accuracy)

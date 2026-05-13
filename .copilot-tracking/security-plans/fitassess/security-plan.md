# Security Plan: FitAssess AI — Clothing Fit Assessment Agent

**Project Slug**: fitassess
**Date**: 2026-05-13
**Entry Mode**: Capture (with spec artifacts)
**Phase**: 2 — Bucket Analysis

---

## Phase 1: Scope Summary

| Area | Details |
|------|---------|
| **Application** | Multi-tenant B2B REST API — AI-powered clothing fit assessment |
| **Stack** | C# / .NET 8, ASP.NET Core, Azure Container Apps (Linux) |
| **Authentication** | Microsoft Entra ID (OAuth 2.0 / OIDC), managed identity |
| **Data stores** | Azure Cosmos DB (4 containers), Azure Blob Storage (transient) |
| **AI components** | Azure AI Vision, Azure ML endpoint (body landmark extraction) |
| **Messaging** | Azure Service Bus (async assessment queue) |
| **Secrets** | Azure Key Vault, managed identity (zero secrets in config) |
| **Gateway** | Azure API Management (rate limiting, correlation) |
| **Region** | Single-region v1, multi-AZ within Container Apps |
| **Scale** | 500 concurrent requests, auto-scale 2–10 instances |
| **Data classification** | Photos: Highly Confidential (transient). Measurements: Confidential. Garment catalog: Internal |
| **Compliance** | CCPA/CPRA, Illinois BIPA (biometric), SOC 2 Type II, FTC Act §5, GDPR (potential) |

---

## Phase 2: Operational Bucket Analysis

### 1. infra

**Components:**

- Azure Container Apps environment (Linux containers, multi-AZ)
- Azure Virtual Network (ACA managed VNet)
- Azure DNS / Load Balancer (ACA built-in ingress)
- Azure Monitor / Log Analytics workspace

**Data flows:**

- Inbound: HTTPS traffic from API Management → ACA ingress → container
- Outbound: Container → Cosmos DB, Blob Storage, AI Vision, Service Bus, Key Vault (all over Azure backbone)

**Integration points:**

- Connects to **web/UI/reporting** via ACA ingress (receives API traffic)
- Connects to **data** via Azure private endpoints (Cosmos DB, Blob Storage)
- Connects to **ai-ml** via Azure private endpoints (AI Vision, ML endpoint)
- Connects to **devops/platform-ops** via Bicep deployments and container image pulls

**Identified gaps:**

- Network segmentation: Are Cosmos DB, Blob Storage, Key Vault, AI endpoints behind private endpoints or accessible over public internet?
- DDoS protection tier (Azure DDoS Standard vs Basic)
- Container runtime security policies (seccomp/AppArmor profiles) not specified
- Egress filtering — are outbound connections restricted to known Azure endpoints?

---

### 2. devops/platform-ops

**Components:**

- CI/CD pipeline (assumed GitHub Actions or Azure DevOps — not yet specified)
- Bicep IaC templates (infra/ directory)
- .NET Aspire orchestrator (FitAssess.AppHost)
- Azure App Configuration (feature flags, canary deployments)
- Container registry (assumed Azure Container Registry)

**Data flows:**

- Inbound: Source code commits → build triggers → pipeline execution
- Outbound: Container images → ACR → ACA deployment; Bicep → ARM → Azure resources

**Integration points:**

- Connects to **infra** via Bicep deployments (provisions Azure resources)
- Connects to **build** via CI pipeline (compiles, tests, packages)
- Connects to **identity/auth** via deployment service principal

**Identified gaps:**

- CI/CD pipeline not yet defined — no pipeline security controls in place
- Container image signing and provenance (SLSA, Notary) not specified
- Deployment approval gates between environments not defined
- Secret injection into pipeline (Key Vault integration for CI secrets)
- Branch protection and signed commits not confirmed

---

### 3. build

**Components:**

- .NET 8 SDK (compilation toolchain)
- NuGet package manager (dependency resolution)
- Container image build (Dockerfile)
- Azure SDK packages (Azure.AI.Vision, Azure.Identity, Microsoft.Azure.Cosmos, etc.)

**Data flows:**

- Inbound: NuGet packages from nuget.org / private feeds → build environment
- Outbound: Compiled assemblies → container image → container registry

**Integration points:**

- Connects to **devops/platform-ops** via CI pipeline (build triggers)
- Feeds **infra** with deployable container images

**Identified gaps:**

- Dependency pinning strategy (lock files, version pinning) not specified
- SAST/SCA scanning mentioned in constitution but tooling not defined
- NuGet package source allow-listing not confirmed
- Reproducible builds not addressed
- Container base image selection and update policy not defined

---

### 4. messaging

**Components:**

- Azure Service Bus namespace (async assessment queue)
- Dead-letter queue (implied by async pattern)

**Data flows:**

- Inbound: Assessment requests queued when load exceeds threshold (queue depth > 50 or p95 > 4s)
- Outbound: Queued messages consumed by assessment worker for processing

**Integration points:**

- Connects to **web/UI/reporting** (API controller publishes to queue, returns HTTP 202)
- Connects to **ai-ml** (worker processes queued assessments through AI pipeline)
- Connects to **data** (worker persists results to Cosmos DB)

**Identified gaps:**

- Message encryption at rest and in transit (Service Bus TLS + Azure encryption)
- Message payload content — does it contain shopper photos or just references?
- Dead-letter queue monitoring and alerting
- Message replay/idempotency controls (correlationId uniqueness)
- Queue access policies — are SAS tokens or managed identity used?

---

### 5. data

**Components:**

- Azure Cosmos DB — `tenants` container (partition key: `/id`)
- Azure Cosmos DB — `garments` container (partition key: `/tenantId`)
- Azure Cosmos DB — `profiles` container (partition key: `/tenantId`)
- Azure Cosmos DB — `assessments` container (partition key: `/tenantId`, TTL: 365 days)
- Azure Blob Storage — transient image container (lifecycle policy: 60s TTL)
- Azure Key Vault (secrets, keys, certificates)

**Data flows:**

- Inbound: Shopper measurements written from assessment pipeline; garment data from ingestion API; photos uploaded for processing
- Outbound: Measurement profiles read for profile-based assessments; assessment results returned via API; photos streamed to AI endpoint then auto-purged

**Integration points:**

- Connects to **web/UI/reporting** (API reads/writes via repository layer)
- Connects to **ai-ml** (blob SAS URL or byte stream passed to AI Vision)
- Connects to **identity/auth** (managed identity access; tenant-scoped partition keys)
- Connects to **messaging** (assessment worker writes results)

**Identified gaps:**

- Cosmos DB customer-managed keys (CMK) vs service-managed encryption
- Cross-tenant data isolation enforcement — relies on application-layer tenant scoping. What if a bug bypasses the repository base class?
- Blob Storage access: SAS token scope and duration for transient images
- Backup encryption and access controls for Cosmos DB
- Data residency — single-region confirmed, but is data replication crossing boundaries?
- Profile deletion audit trail — hard delete within 24h, but is the audit log immutable?
- Assessment TTL (365 days) — is this appropriate given BIPA's data minimization requirements?

---

### 6. web/UI/reporting

**Components:**

- ASP.NET Core Web API (FitAssess.Api) — controllers, middleware, filters
- Azure API Management (gateway, rate limiting, request correlation)
- OpenAPI 3.0.3 contract (public API surface)
- Health check endpoint (`/health`)
- Swashbuckle (API documentation)

**Data flows:**

- Inbound: HTTPS requests from retail partner frontends → APIM → Web API (multipart/form-data with photos, JSON for profile-based assessments, garment CRUD)
- Outbound: JSON responses (fit assessments, profiles, garment data), error responses, rate limit headers

**Integration points:**

- Connects to **identity/auth** (JWT validation middleware, Entra ID token verification)
- Connects to **data** (Cosmos DB reads/writes via repository layer)
- Connects to **ai-ml** (image processing pipeline)
- Connects to **messaging** (publishes to Service Bus under load)

**Identified gaps:**

- Input validation: 10 MB file upload — is multipart parsing hardened against zip bombs or malformed payloads?
- Image content validation: is the uploaded file truly an image? (magic byte validation vs extension-only)
- CORS policy not defined (B2B API may not need CORS, but should be explicitly restricted)
- Response headers: HSTS, X-Content-Type-Options, X-Frame-Options not specified
- API versioning strategy for breaking changes
- Swagger/OpenAPI endpoint exposure in production (should be disabled or restricted)
- Error response information leakage (stack traces, internal IDs in 4xx/5xx responses)
- Rate limiting bypass — is APIM the only path, or can ACA ingress be hit directly?

---

### 7. identity/auth

**Components:**

- Microsoft Entra ID (multi-tenant app registration)
- Per-tenant service principal with scoped API permissions
- JWT validation middleware (ASP.NET Core)
- Managed identity (for service-to-Azure-resource access)
- OAuth 2.0 scopes: `FitAssess.Read`, `FitAssess.Write`

**Data flows:**

- Inbound: Bearer tokens from retail partner frontends → APIM → JWT middleware → tenant claim extraction
- Outbound: Managed identity tokens → Azure resources (Cosmos, Blob, AI, Key Vault, Service Bus)

**Integration points:**

- Connects to **web/UI/reporting** (JWT middleware in API pipeline)
- Connects to **data** (managed identity for Cosmos DB, Blob Storage, Key Vault)
- Connects to **ai-ml** (managed identity for AI Vision, ML endpoint)
- Connects to **messaging** (managed identity for Service Bus)

**Identified gaps:**

- OAuth scope granularity: only `Read` and `Write` — are these sufficient for RBAC? (e.g., garment ingestion vs assessment creation vs profile deletion)
- Tenant isolation in JWT claims: what claim maps to tenant ID? Is it validated against the Cosmos tenant registry?
- Token lifetime and refresh policy not specified
- Suspended tenant enforcement — does JWT validation check tenant status on every request or is it cached?
- Service principal key/certificate rotation policy
- Break-glass access for operations team not defined
- No MFA mentioned for operational/admin access

---

### 8. ai-ml

**Components:**

- Azure AI Vision (image quality validation, person detection, multi-person rejection, minor detection)
- Azure AI Custom Vision / Azure ML endpoint (body landmark extraction — 17+ key points)
- Anthropometric scaling algorithm (deterministic measurement derivation)
- Model versioning (`YYYY-MM-DD-vN` format tracked per assessment)

**Data flows:**

- Inbound: Shopper body photos (byte stream or SAS URL) → AI Vision → landmark model
- Outbound: Extracted body landmarks → measurement derivation → fit comparison engine → assessment result

**Integration points:**

- Connects to **web/UI/reporting** (called from assessment pipeline in API)
- Connects to **data** (reads photos from Blob Storage via SAS URL for large images)
- Connects to **identity/auth** (managed identity for Azure AI service access)

**Identified gaps:**

- Adversarial image attacks: can crafted images cause incorrect landmark detection or bypass minor detection?
- Model extraction: can repeated queries reconstruct the body measurement model?
- Content safety: beyond minor detection, are there guardrails for inappropriate/explicit image content?
- AI model update process: how are model versions deployed? Is there A/B testing or canary rollout?
- Training data provenance: what data was used to train/fine-tune the body landmark model?
- Bias evaluation: accuracy across diverse body types, skin tones, clothing (spec mentions plan but no details)
- SAS URL for blob → AI Vision: is the SAS scoped minimally (read-only, single blob, short expiry)?
- Fallback behavior: when AI model returns < 70% confidence, does the fallback path have its own security posture?

---

## Cross-Cutting: General Security (GS)

| GS Concern | Affected Buckets | Status |
|---|---|---|
| **Logging & monitoring** | All | OpenTelemetry + Azure Monitor planned; SIEM integration TBD |
| **Incident response** | All | No runbook or escalation path defined |
| **Compliance (CCPA/BIPA/SOC 2)** | data, identity/auth, ai-ml, web | BIPA consent tracking needed; SOC 2 evidence collection TBD |
| **Key management** | data, identity/auth, messaging | Key Vault planned; rotation policy not defined |
| **Certificate lifecycle** | infra, web | TLS certificates for ACA ingress and APIM; renewal automation TBD |
| **Container security** | infra, devops, build | Image scanning mentioned; runtime policies, base image policy not defined |
| **API security** | web, identity/auth | Rate limiting via APIM; input validation in OpenAPI schema; hardening gaps noted |
| **Supply chain (AI model)** | ai-ml, build | Model provenance, dataset lineage, weight signing not addressed |
| **Bias & fairness** | ai-ml | Evaluation plan mentioned but not defined |
| **Data retention & erasure** | data, ai-ml | 60s image TTL, 24h profile deletion, 365d assessment TTL — BIPA alignment TBD |

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

---

## Phase 3: Standards Mapping

Standards mapped using embedded OWASP Top 10 (2025), OWASP LLM Top 10, NIST 800-53, NIST AI RMF, and delegated WAF/CAF/CIS research.

### 1. infra (Azure Container Apps, VNet, Azure Monitor)

**Applicable Standards:**

- **OWASP A05:2025** — Security Misconfiguration: Container Apps default configs (public ingress enabled, no network isolation) must be hardened. ACA managed VNet requires NSG rules, egress lockdown, and disabled public access.
- **OWASP A06:2025** — Vulnerable and Outdated Components: Container base images must be patched, tracked, and rebuilt. Alpine/Chiselled Ubuntu with regular rebuild cadence.
- **NIST CM** — Configuration Management: Baseline configs for ACA environment, VNet NSGs, Azure Monitor diagnostic settings. Drift detection via Azure Policy.
- **NIST PE** — Physical and Environmental: Azure region/AZ selection and DDoS protection tier.
- **NIST SC** — System and Communications Protection: Network segmentation via private VNet, TLS 1.2+ enforcement, mTLS between services.
- **NIST SI** — System and Information Integrity: Container runtime integrity monitoring, image scanning, security patching cadence.
- **CIS §2** — Enable Defender for Cloud; configure security contact; auto-provisioning of monitoring agent.
- **CIS §5** — Diagnostic settings for Container Apps environments → Log Analytics; activity log alerts.
- **CIS §6** — NSGs on ACA VNet subnet; deny inbound from internet (private only); Network Watcher flow logs.

**WAF/CAF Findings:** SE:01 (security baseline), SE:04 (segmentation — private VNet, NSGs), SE:06 (private endpoints, UDR egress via Firewall), SE:08 (minimal base images, mTLS), SE:10 (OpenTelemetry, Azure Monitor). CAF: enable Defender, IaC drift detection, AZ support, health probes.

**Gap Analysis:**

- No WAF layer — ACA does not natively support WAF. Route through Application Gateway WAF v2 or Front Door.
- DDoS Standard not confirmed on VNet.
- Egress not locked down — need Azure Firewall with FQDN filtering.
- Defender for Containers not enabled.

---

### 2. devops/platform-ops (CI/CD, Bicep, .NET Aspire, ACR)

**Applicable Standards:**

- **OWASP A05:2025** — Security Misconfiguration: Pipeline configs, ACR settings (quarantine disabled, admin account enabled) are common misconfig vectors.
- **OWASP A06:2025** — Vulnerable and Outdated Components: NuGet and Docker dependency scanning must be automated in CI.
- **OWASP A08:2025** — Software and Data Integrity Failures: Container image signing, provenance attestation (SLSA), and pipeline integrity are critical. Unsigned images can be tampered.
- **NIST CA** — Assessment, Authorization, Monitoring: Security scan gates before deployment approval.
- **NIST CM** — Configuration Management: Bicep linting, IaC security scanning (Checkov/PSRule), change control.
- **NIST SA** — System and Services Acquisition: Secure SDLC integration, third-party component governance.
- **NIST SI** — System and Information Integrity: SAST/SCA scanning, vulnerability remediation in CI.
- **CIS §2** — Enable Defender for Containers on ACR; integrate Defender for DevOps with GitHub.
- **CIS §10** — Resource locks on production resources; tagging strategy enforcement.

**WAF/CAF Findings:** SE:02 (SDL — SAST, DAST, SCA in pipeline), SE:08 (multi-stage Dockerfiles, non-root user, Defender for Containers), SE:09 (OIDC federation — no stored secrets), SE:11 (security scanning steps). CAF: quarantine pattern for NuGet, immutable ACR tags, Defender for DevOps in PRs. MCSB DS-1 through DS-7 (threat modeling, supply chain, pipeline enforcement, deployment logging).

**Gap Analysis:**

- No SBOM generation — required for SOC 2 and supply chain transparency.
- No IaC security scanning (Checkov/PSRule) mentioned.
- No OIDC federation for GitHub Actions → Azure (still relying on stored credentials).
- ACR quarantine pattern not enabled.

---

### 3. build (.NET 8 SDK, NuGet, Dockerfile)

**Applicable Standards:**

- **OWASP A06:2025** — Vulnerable and Outdated Components: NuGet packages and Docker base images must be scanned for known CVEs. Dependency pinning with lock files required.
- **OWASP A08:2025** — Software and Data Integrity Failures: Build reproducibility, package signature validation, and container layer integrity. Compromised NuGet packages are a supply chain risk.
- **NIST SA** — System and Services Acquisition: Third-party component inventory, vulnerability tracking, license compliance.
- **NIST SI** — System and Information Integrity: `dotnet nuget audit` in CI; fail builds on known vulnerabilities.
- **CIS** — Build-time controls outside CIS Azure scope; covered by MCSB DS-2 (supply chain).

**WAF/CAF Findings:** SE:02 (.NET code analyzers, `dotnet audit`), SE:08 (trimming, AOT, disable XXE), SE:11 (security-critical path unit tests, DAST). CAF: quarantine pattern for NuGet, version pinning, no sensitive data in build artifacts. MCSB DS-2 (supply chain), DS-3 (build agent security), PV-6 (Dependabot/Renovate).

**Gap Analysis:**

- Dockerfile security unspecified — must enforce multi-stage builds, non-root user, no secrets in layers, minimal base image.
- No Dependabot/Renovate for automated dependency updates.
- `dotnet nuget audit` not integrated into CI pipeline.
- Floating Azure SDK version ranges create unpredictable builds.

---

### 4. messaging (Azure Service Bus)

**Applicable Standards:**

- **OWASP A01:2025** — Broken Access Control: Queue access policies must enforce least privilege. Managed identity with sender/receiver roles instead of SAS keys.
- **OWASP A03:2025** — Injection: Message payload deserialization must validate schema before processing to prevent deserialization attacks.
- **OWASP A08:2025** — Software and Data Integrity Failures: Message integrity validation; idempotent processing; duplicate detection.
- **NIST AC** — Access Control: Managed identity for Service Bus; role assignments (`Azure Service Bus Data Sender/Receiver`); disable SAS key auth.
- **NIST SC** — System and Communications Protection: Private endpoint; TLS 1.2 in transit; infrastructure encryption (double encryption at rest).
- **NIST SI** — System and Information Integrity: Message schema validation on dequeue; dead-letter monitoring.

**WAF/CAF Findings:** SE:04 (separate queues by type), SE:05 (managed identity, disable SAS), SE:06 (private endpoint, no public access), SE:07 (double encryption, TLS 1.2), SE:09 (eliminate SAS tokens), SE:10 (diagnostic logs, queue depth monitoring). CAF: application-level payload encryption for biometric-adjacent data, duplicate detection, Premium tier for VNet integration.

**Gap Analysis:**

- Message payload encryption at application level not implemented — assessment references may link to biometric data.
- SAS vs managed identity not confirmed — must disable SAS key authentication.
- Dead-letter queue monitoring and alerting not configured.
- Service Bus tier not confirmed — Premium required for VNet integration and CMEK.

---

### 5. data (Cosmos DB, Blob Storage, Key Vault)

**Applicable Standards:**

- **OWASP A01:2025** — Broken Access Control: Cross-tenant data isolation relies on application-layer tenant scoping via hierarchical partition keys. A bug bypassing the repository base class could expose tenant data.
- **OWASP A02:2025** — Cryptographic Failures: Encryption at rest (service-managed vs CMK), blob SAS token scope, TLS enforcement on all connections.
- **OWASP A03:2025** — Injection: Cosmos DB NoSQL query parameterization to prevent injection. Blob Storage access via SAS with minimal scope.
- **NIST AC** — Access Control: Disable Cosmos DB key-based auth; use Entra ID RBAC; managed identity for all access.
- **NIST AU** — Audit and Accountability: Cosmos DB control plane audit logs; Blob Storage diagnostic logs; Key Vault audit logs.
- **NIST SC** — System and Communications Protection: Private endpoints on all three services; CMK evaluation for BIPA compliance.
- **NIST SI** — System and Information Integrity: Defender for Cosmos DB, Storage, Key Vault; continuous backup with PITR.
- **CIS §3** — Storage: HTTPS-only, blob encryption, lifecycle management, no public blob access, private endpoints.
- **CIS §4** — Database: Cosmos DB disable key auth, diagnostic logging, firewall rules, private endpoints, Defender.
- **CIS §5** — Key Vault logging, Cosmos DB diagnostics, Storage Analytics logging.
- **CIS §8** — Key Vault: soft delete, purge protection, RBAC, logging, key expiration, private endpoint.

**WAF/CAF Findings:** SE:03 (data classification — Purview integration), SE:04 (hierarchical partition keys, separate blob containers), SE:05 (disable key auth, Entra RBAC), SE:06 (private endpoints all), SE:07 (CMK via Key Vault, HSM-backed for BIPA), SE:08 (disable local auth, CORS, anonymous access), SE:09 (all secrets in KV, audit, rotation), SE:10 (Defender for all data services). MCSB DP-1 through DP-7 (classify, monitor, encrypt transit/rest, CMK, key management).

**Gap Analysis:**

- **CRITICAL — BIPA §15(a)**: Must publish written biometric data retention/destruction policy before collecting body photos.
- **CRITICAL — BIPA §15(b)**: API must verify consent claim in request before processing photos; log consent evidence.
- CMK not decided — needed for SOC 2 and BIPA evidence.
- Microsoft Purview not integrated for automated data classification.
- Cosmos DB continuous backup not configured (PITR needed).
- Key Vault purge protection and soft delete not confirmed.
- Assessment TTL (365 days) must be validated against BIPA data minimization requirements.

---

### 6. web/UI/reporting (ASP.NET Core Web API, API Management, OpenAPI)

**Applicable Standards:**

- **OWASP A01:2025** — Broken Access Control: Tenant isolation in API responses; ensure no cross-tenant data leakage through improper authorization checks.
- **OWASP A02:2025** — Cryptographic Failures: HTTPS-only, TLS 1.2 minimum, disable weak cipher suites.
- **OWASP A03:2025** — Injection: 10 MB multipart file upload parsing must be hardened against zip bombs, malformed payloads, and content-type spoofing. Magic byte validation required.
- **OWASP A05:2025** — Security Misconfiguration: Swagger/OpenAPI endpoint in production, missing security headers (HSTS, CSP, X-Content-Type-Options), verbose error responses.
- **OWASP A07:2025** — Identification and Authentication Failures: JWT validation completeness (issuer, audience, expiration, signature, tenant claim).
- **OWASP A10:2025** — SSRF: If the API fetches external resources (e.g., garment image URLs from tenant data), URL validation is required.
- **NIST AC** — Access Control: Per-tenant authorization; rate limiting per tenant tier; API key management via APIM.
- **NIST IA** — Identification and Authentication: JWT middleware validation; Entra ID token verification.
- **NIST SC** — System and Communications Protection: TLS enforcement; security headers; CORS restriction; request size limits.
- **NIST SI** — System and Information Integrity: Input validation middleware; error response sanitization; content-type enforcement.
- **CIS §6** — APIM VNet integration; private endpoints; NSG rules.

**WAF/CAF Findings:** SE:01 (security headers — HSTS, CSP, X-Content-Type-Options, X-Frame-Options), SE:05 (JWT, tenant claims, rate limiting), SE:06 (APIM VNet, WAF policy), SE:07 (HTTPS-only, TLS 1.2), SE:08 (disable unused endpoints, request size limits, sanitize errors), SE:11 (OWASP API Security Top 10 testing, fuzzing, pen test). CAF: APIM policies for rate limiting/JWT/CORS, no PII in errors, OpenAPI contract validation.

**Gap Analysis:**

- APIM deferred to v2 — without it, no centralized WAF, throttling, or API key management. Weakens SOC 2 evidence.
- Security headers middleware not implemented (HSTS, CSP, X-Content-Type-Options, X-Frame-Options, Referrer-Policy).
- Swagger endpoint exposure in production not addressed.
- CORS policy not explicitly restricted.
- Error response information leakage (stack traces, internal IDs) not confirmed handled.
- DSAR endpoint for CCPA right-to-know/right-to-delete not implemented.

---

### 7. identity/auth (Entra ID, OAuth 2.0/OIDC, Managed Identity, JWT)

**Applicable Standards:**

- **OWASP A01:2025** — Broken Access Control: OAuth scope granularity (only Read/Write) may be insufficient for fine-grained RBAC. Tenant isolation must be enforced via `tid` claim validation.
- **OWASP A02:2025** — Cryptographic Failures: Token signing algorithm enforcement; reject `alg: none`; certificate-based credentials over secrets.
- **OWASP A07:2025** — Identification and Authentication Failures: Multi-tenant token validation must check tenant ID against registered tenants. Suspended tenant enforcement on every request.
- **NIST AC** — Access Control: Least-privilege OAuth scopes; managed identity for service-to-service; monthly access reviews.
- **NIST IA** — Identification and Authentication: MFA for admin access; Conditional Access policies; Entra ID sign-in risk policies.
- **NIST PS** — Personnel Security: Service principal key/certificate rotation; break-glass account procedures; tenant onboarding security review.
- **CIS §1** — IAM: MFA enabled for all users (1.1); Conditional Access policies (1.2); block legacy authentication (1.3); restrict user consent (1.4); restrict guest access (1.6).

**WAF/CAF Findings:** SE:05 (multi-tenant app registration, per-tenant SP, least privilege, disable legacy auth, managed identity for all Azure access, JWT validation — issuer/audience/expiry/signature/tid), SE:08 (certificate-based credentials, short token lifetime, token replay protection), SE:09 (no client secrets in config, Key Vault for tenant onboarding secrets). CAF: Zero Trust alignment, Continuous Access Evaluation (CAE), app roles for fine-grained permissions. MCSB IM-1 through IM-8 (centralized IdP, managed identities, MFA, conditional access, credential exposure prevention).

**Gap Analysis:**

- **CRITICAL** — Multi-tenant `tid` claim validation not confirmed. Tokens from unregistered tenants must be rejected.
- OAuth scope granularity too coarse — only `FitAssess.Read` and `FitAssess.Write`. Need finer roles (e.g., `GarmentCatalog.Write`, `Admin.Manage`).
- Tenant onboarding process lacks documented security review and credential rotation policy.
- Continuous Access Evaluation (CAE) not enabled for near-real-time token revocation.
- Break-glass admin access not defined.
- Consent metadata not flowing through auth chain — BIPA requires consent verification before photo processing.

---

### 8. ai-ml (Azure AI Vision, Azure ML, Body Landmark Extraction)

**Applicable Standards:**

- **OWASP A04:2025** — Insecure Design: AI pipeline lacks threat modeling for adversarial inputs, model extraction, and bias amplification.
- **OWASP A06:2025** — Vulnerable and Outdated Components: AI model versioning and update cadence; Azure SDK dependency tracking.
- **OWASP A08:2025** — Software and Data Integrity Failures: Model provenance, dataset lineage, and weight signing not addressed.
- **OWASP LLM01** — Prompt Injection: GPT-4o Vision measurement extraction is vulnerable to crafted images containing adversarial text or manipulated EXIF metadata.
- **OWASP LLM02** — Insecure Output Handling: Measurement values from AI must be validated against physiologically valid ranges before persisting.
- **OWASP LLM04** — Model Denial of Service: Large or complex images could consume excessive compute. Enforce image dimension/size limits before AI processing.
- **OWASP LLM05** — Supply Chain Vulnerabilities: Model weights and Azure AI service dependencies must be tracked for vulnerabilities.
- **OWASP LLM06** — Sensitive Information Disclosure: AI service must not retain or log biometric photo data. Verify DPA covers biometric data.
- **OWASP LLM09** — Overreliance: Confidence thresholds (≥70%) exist but fallback path security posture is unverified.
- **NIST SA** — System and Services Acquisition: AI model procurement, Azure AI service SLAs, third-party model governance.
- **NIST SI** — System and Information Integrity: Output validation, anomaly detection on measurement values, model drift monitoring.
- **NIST RA** — Risk Assessment: Bias evaluation across body types, skin tones; adversarial robustness testing.
- **NIST AI RMF GV-1** — AI governance policies for body measurement processing.
- **NIST AI RMF MS-2.5 through MS-2.11** — Privacy (photo handling), security (adversarial attacks), resilience (fallback paths), explanation (confidence scores), bias (demographic accuracy).
- **CIS §2** — Defender recommendations for AI services.
- **CIS §5** — Diagnostic settings on AI services; track all API calls.
- **CIS §6** — Private endpoints for AI services; no public access.

**WAF/CAF Findings:** SE:03 (photos = Highly Confidential; AI service DPA must cover biometric data), SE:05 (managed identity, RBAC `Cognitive Services User`, disable key auth), SE:06 (private endpoints all AI services), SE:07 (TLS 1.2), SE:08 (Content Safety for minor detection, content filtering medium+, system message constraints), SE:10 (log all AI calls with model version/latency/confidence), SE:11 (red-team measurement extraction prompt). MCSB AI-1 through AI-7 (inventory, data protection, model deployment, access, content protection, monitoring, red-teaming).

**Gap Analysis:**

- **CRITICAL — BIPA DPA verification**: Must confirm Azure AI Vision and OpenAI DPA covers biometric data processing; opt-out of Abuse Monitoring human review.
- **CRITICAL — Prompt injection defense**: GPT-4o Vision extraction vulnerable to adversarial images. Need input validation, output schema validation, and anomalous measurement alerting.
- Minor detection enforcement order not verified in code flow — Content Safety must process BEFORE measurement extraction.
- AI model explainability insufficient for SOC 2 and CCPA automated decision requirements.
- No regular AI red-teaming process scheduled.
- Training data provenance and bias evaluation across demographics not documented.
- Output validation for physiologically valid measurement ranges not implemented.
- Model version + prompt hash + confidence not stored per assessment for audit trail.

---

### Cross-Cutting Compliance Standards

#### CCPA/CPRA

| Requirement | Mapped Controls | Gap |
|---|---|---|
| Right to know | A01, AC, SE:05 | Need DSAR API endpoint |
| Right to delete | AC, AU, SE:03 | Confirm cascade deletion across all stores |
| Right to opt out | A01, SE:03 | Document in privacy policy |
| Data minimization | SE:03, DP-1 | Verify no photo data in logs, AI caches, telemetry |
| Risk assessment | A04, RA, MS-2 | Conduct DPIA before production |

#### Illinois BIPA

| Requirement | Mapped Controls | Gap |
|---|---|---|
| §15(a) Written policy | SE:03, DP-1 | **BLOCKER**: Must publish before collecting biometric data |
| §15(b) Informed consent | A01, AC, SE:05 | **BLOCKER**: API must verify consent claim |
| §15(c) No profit | Contractual | Ensure B2B terms prohibit biometric data monetization |
| §15(d) No disclosure | SC, SE:06 | Verify AI service DPA; no data egress to unauthorized parties |
| §15(e) Reasonable security | All controls | Document security controls in BIPA compliance filing |

#### SOC 2 Type II

| Category | Mapped Controls |
|---|---|
| CC6 — Logical/Physical Access | SE:05, IM-1–IM-9, CIS §1, AC, IA |
| CC7 — System Operations | SE:10, SE:12, LT-1–LT-7, AU, IR |
| CC8 — Change Management | SE:02, DS-1–DS-7, CM, SA |
| CC9 — Risk Mitigation | SE:01, SE:11, PV-1–PV-6, RA |
| A1 — Availability | AZ support, health probes, autoscaling |
| C1 — Confidentiality | SE:03, SE:07, DP-1–DP-7, SC |
| P1 — Privacy | BIPA/CCPA controls, AU |

---

### Phase 3 Priority Summary

| Priority | Count | Top Items |
|---|---|---|
| **Critical (Pre-Production Blockers)** | 6 | BIPA written policy, consent verification, AI DPA verification, private endpoints everywhere, prompt injection defense, private VNet deployment |
| **High (SOC 2 Readiness)** | 7 | Defender for Cloud, diagnostic settings, OIDC federation, disable Cosmos key auth, Key Vault hardening, DSAR endpoint, SBOM generation |
| **Medium (Hardening)** | 7 | WAF layer, security headers, JWT tid validation, AI red-teaming, Purview integration, egress lockdown, container image scanning |

---

## Phase 4: Security Model Analysis (STRIDE)

STRIDE-based threat identification per operational bucket. Risk calculated using Likelihood × Impact matrix: H×H=Critical, H×M/M×H=High, M×M=Medium, L×any=Low.

### Data Flow Overview

```
                    ┌──────────────────────────────────────────────┐
                    │              Trust Boundary: Internet         │
                    └──────────────────┬───────────────────────────┘
                                       │ HTTPS
                              ┌────────▼─────────┐
                              │  API Management   │ ← Rate limit, correlation
                              │   (web bucket)    │
                              └────────┬──────────┘
                                       │ HTTPS
                    ┌──────────────────────────────────────────────┐
                    │     Trust Boundary: Azure VNet (private)     │
                    │                                              │
                    │  ┌──────────────────────────┐               │
                    │  │  Container Apps (infra)   │               │
                    │  │  ┌──────────────────────┐ │               │
                    │  │  │ ASP.NET Core API      │ │               │
                    │  │  │ JWT Middleware (auth)  │ │               │
                    │  │  └──────┬───────────────┘ │               │
                    │  └─────────┼─────────────────┘               │
                    │            │                                  │
                    │  ┌─────────▼──────────┐                     │
                    │  │  Assessment Pipeline │                    │
                    │  └──┬──────┬──────┬───┘                     │
                    │     │      │      │                          │
                    │ ┌───▼──┐ ┌─▼───┐ ┌▼────────────┐           │
                    │ │Cosmos│ │Blob │ │AI Vision/ML  │           │
                    │ │  DB  │ │Store│ │(ai-ml bucket)│           │
                    │ │(data)│ │(data)│ └──────────────┘          │
                    │ └──────┘ └─────┘                            │
                    │                  ┌──────────────┐           │
                    │                  │ Service Bus  │           │
                    │                  │ (messaging)  │           │
                    │                  └──────────────┘           │
                    │                  ┌──────────────┐           │
                    │                  │  Key Vault   │           │
                    │                  └──────────────┘           │
                    └──────────────────────────────────────────────┘
                    ┌──────────────────────────────────────────────┐
                    │   Trust Boundary: CI/CD (devops/build)       │
                    │   GitHub Actions → ACR → Container Apps      │
                    └──────────────────────────────────────────────┘
```

**Trust Boundaries:**

1. Internet → APIM: External tenant frontends cross into Azure. All input untrusted.
2. APIM → VNet: Gateway to private network. JWT must be validated before crossing.
3. API → AI Services: Biometric photos cross to Azure AI. DPA boundary.
4. API → Data Stores: Tenant-scoped data access. Partition key isolation boundary.
5. CI/CD → Production: Build artifacts deployed to production. Supply chain boundary.
6. User Input → AI Model: Prompt injection boundary (photos with embedded adversarial content).

**AI-Specific Data Flows:**

- Shopper photo (byte stream) → Content Safety filter → AI Vision (quality/person/minor detection) → ML endpoint (landmark extraction) → Measurement derivation (deterministic) → Fit comparison → Assessment result
- Photo stored in Blob (60s TTL) → SAS URL passed to AI Vision → Photo auto-purged

---

### 1. infra — Threat Table

| ID | STRIDE | Description | Component | Likelihood | Impact | Risk | Mitigation | Standards |
|---|---|---|---|---|---|---|---|---|
| T-INFRA-001 | Tampering | Config drift via manual Azure portal changes bypassing IaC | ACA Environment | Medium | High | **High** | Immutable IaC deployments; Azure Policy deny portal changes; drift detection | NIST CM-3, SE:08 |
| T-INFRA-002 | DoS | DDoS attack on public ACA ingress; no WAF/DDoS Standard | ACA Ingress | High | High | **Critical** | Deploy behind App Gateway WAF v2; enable DDoS Standard on VNet | OWASP A05, CIS §6, SE:06 |
| T-INFRA-003 | EoP | Container escape via unpatched runtime or misconfigured security context | ACA Container | Low | High | **Low** | Minimal base images; read-only root FS; drop all capabilities; Defender for Containers | NIST SI-2, SE:08 |
| T-INFRA-004 | Info Disclosure | Azure Monitor logs containing PII (shopper measurements, tenant IDs) exposed via overly broad RBAC | Log Analytics | Medium | Medium | **Medium** | Restrict Log Analytics RBAC; obfuscate PII in telemetry; data masking rules | NIST AU-9, OWASP A02, SE:10 |
| T-INFRA-005 | Tampering | Egress to unauthorized endpoints if outbound not filtered (data exfil path) | VNet/NSG | Medium | High | **High** | Azure Firewall with FQDN allow-list; deny all outbound by default | NIST SC-7, SE:06 |

---

### 2. devops/platform-ops — Threat Table

| ID | STRIDE | Description | Component | Likelihood | Impact | Risk | Mitigation | Standards |
|---|---|---|---|---|---|---|---|---|
| T-DEVOPS-001 | Tampering | Pipeline poisoning — malicious code injected via compromised GitHub Action or workflow modification | CI/CD Pipeline | Medium | High | **High** | Pin action versions by SHA; require PR reviews; branch protection on main; signed commits | OWASP A08, NIST SA-12, DS-6 |
| T-DEVOPS-002 | EoP | Stored service principal credentials in GitHub secrets leaked or compromised | GitHub Secrets | Medium | High | **High** | Migrate to OIDC workload identity federation (zero stored credentials) | SE:09, NIST IA-5, IM-8 |
| T-DEVOPS-003 | Spoofing | Malicious container image pushed to ACR impersonating legitimate build output | ACR | Low | High | **Low** | Enable content trust / Notary; ACR quarantine pattern; image signing | OWASP A08, NIST SI-7, DS-2 |
| T-DEVOPS-004 | Info Disclosure | Build logs or artifacts containing secrets, connection strings, or internal URLs | CI Pipeline Output | Medium | Medium | **Medium** | Secret scanning in pipeline; mask sensitive values; no secrets in Bicep parameters | NIST SI-12, SE:09 |
| T-DEVOPS-005 | Tampering | IaC (Bicep) modified without security review, deploying insecure configurations | Bicep Templates | Medium | High | **High** | IaC scanning (Checkov/PSRule); PR approval gates; `what-if` preview before deployment | NIST CM-3, DS-6, SE:02 |

---

### 3. build — Threat Table

| ID | STRIDE | Description | Component | Likelihood | Impact | Risk | Mitigation | Standards |
|---|---|---|---|---|---|---|---|---|
| T-BUILD-001 | Tampering | Dependency substitution — malicious NuGet package typosquatting Azure SDK packages | NuGet Packages | Medium | High | **High** | Pin exact versions; use lock files; private NuGet feed; package signature validation | OWASP A06, NIST SA-12, DS-2 |
| T-BUILD-002 | Tampering | Compromised Docker base image (supply chain attack on mcr.microsoft.com) | Dockerfile | Low | High | **Low** | Pin image digest; verify image signatures; rebuild on schedule; Defender for Containers scan | OWASP A08, NIST SI-7 |
| T-BUILD-003 | Info Disclosure | Secrets baked into container image layers (connection strings, API keys in Dockerfile) | Container Image | Medium | High | **High** | Multi-stage builds; no COPY of secret files; scan layers with tools like Trivy/Grype | NIST SI-12, SE:09 |
| T-BUILD-004 | Tampering | Build not reproducible — different outputs from same source due to floating dependency versions | Build Pipeline | Medium | Medium | **Medium** | Lock files (`packages.lock.json`); deterministic restore; SBOM generation | OWASP A08, NIST SA-10 |

---

### 4. messaging — Threat Table

| ID | STRIDE | Description | Component | Likelihood | Impact | Risk | Mitigation | Standards |
|---|---|---|---|---|---|---|---|---|
| T-MSG-001 | Spoofing | Unauthorized message injection into assessment queue via compromised SAS token | Service Bus Queue | Medium | High | **High** | Disable SAS auth; use managed identity exclusively; RBAC sender/receiver roles | OWASP A01, NIST AC-3, SE:05 |
| T-MSG-002 | Tampering | Message payload modified in transit or at rest (assessment ID references altered) | Service Bus Message | Low | Medium | **Low** | TLS 1.2 in transit; infrastructure encryption at rest; application-level payload signing | NIST SC-8, SE:07 |
| T-MSG-003 | Repudiation | Assessment processing events not logged — cannot prove a message was processed or failed | Dead Letter Queue | Medium | Medium | **Medium** | Log all message processing events with correlation ID; immutable audit trail in Log Analytics | NIST AU-3, SE:10 |
| T-MSG-004 | Info Disclosure | Message payload containing shopper references readable by operators with broad Service Bus access | Service Bus Payload | Medium | Medium | **Medium** | Application-level encryption of message bodies; restrict RBAC to Data Receiver/Sender only | OWASP A02, NIST SC-28, SE:07 |
| T-MSG-005 | DoS | Queue flooding via rapid API calls exceeding rate limit → assessment backlog grows unbounded | Service Bus Queue | Medium | Medium | **Medium** | Queue depth monitoring; auto-scaling consumers; circuit breaker when depth > threshold; APIM rate limiting | SE:06, NIST SC-5 |

---

### 5. data — Threat Table

| ID | STRIDE | Description | Component | Likelihood | Impact | Risk | Mitigation | Standards |
|---|---|---|---|---|---|---|---|---|
| T-DATA-001 | Info Disclosure | Cross-tenant data leakage via application-layer bug bypassing partition key scoping | Cosmos DB | Medium | High | **High** | Repository base class enforces tenantId filter; integration tests for tenant isolation; Cosmos DB RBAC (not key auth) | OWASP A01, NIST AC-3, SE:04 |
| T-DATA-002 | Info Disclosure | Blob SAS token with overly broad scope/duration exposes photos beyond 60s TTL | Blob Storage | Medium | High | **High** | SAS: read-only, single-blob, 90s expiry max; stored access policy; lifecycle hard-delete at 60s | OWASP A02, NIST SC-28, CIS §3 |
| T-DATA-003 | Tampering | Unauthorized write to garment catalog altering measurements → incorrect fit assessments for all shoppers | Cosmos DB (garments) | Medium | High | **High** | Separate write scope (`GarmentCatalog.Write`); audit all writes; change-feed monitoring for anomalies | OWASP A01, NIST AC-6, AU-3 |
| T-DATA-004 | Repudiation | Profile deletion (24h SLA) without immutable audit trail — cannot prove deletion occurred for BIPA | Cosmos DB (profiles) | Medium | High | **High** | Immutable audit log for all deletes; include timestamp, entity ID, requesting identity; retain audit beyond entity TTL | NIST AU-3, AU-9, BIPA §15(a) |
| T-DATA-005 | Info Disclosure | Cosmos DB key-based auth credentials leaked → full read/write to all tenant data | Cosmos DB Keys | Medium | High | **High** | Disable key-based auth; use Entra ID RBAC only; managed identity | NIST IA-5, CIS §4, SE:05 |
| T-DATA-006 | Tampering | Key Vault access policy modified to grant unauthorized identity access to encryption keys | Key Vault | Low | High | **Low** | Enable purge protection; RBAC-based access (not access policies); Azure Policy enforcement; audit logging | CIS §8, NIST AC-6, SE:09 |
| T-DATA-007 | Info Disclosure | Photo data persists in telemetry, logs, or exception traces beyond 60s TTL | Log Analytics / App Insights | Medium | High | **High** | Scrub photo bytes and measurement data from all logging; structured logging with redaction; telemetry sampling exclusions | NIST AU-9, OWASP A09, BIPA §15(a) |

---

### 6. web/UI/reporting — Threat Table

| ID | STRIDE | Description | Component | Likelihood | Impact | Risk | Mitigation | Standards |
|---|---|---|---|---|---|---|---|---|
| T-WEB-001 | Spoofing | JWT token replay or stolen token used from different client | API Endpoint | Medium | High | **High** | Short token lifetime; token binding; Continuous Access Evaluation (CAE); validate `aud` and `tid` claims | OWASP A07, NIST IA-5, SE:05 |
| T-WEB-002 | Tampering | Malicious file upload disguised as image (zip bomb, polyglot file, executable) | Photo Upload (multipart) | High | High | **Critical** | Magic byte validation; file size limits enforced before parsing; Content-Type verification; image re-encoding | OWASP A03, NIST SI-10, SE:08 |
| T-WEB-003 | Info Disclosure | Verbose error responses leaking stack traces, internal paths, or Cosmos DB entity IDs | Error Handling | High | Medium | **High** | Custom error middleware; production exception handler returns generic 500; correlationId for internal tracing only | OWASP A05, NIST SI-11, SE:08 |
| T-WEB-004 | DoS | Photo upload endpoint abused for resource exhaustion (10 MB × many concurrent) | API Upload | High | Medium | **High** | Rate limiting per tenant/IP; request body size middleware; APIM throttling; auto-scale with ceiling | NIST SC-5, SE:06 |
| T-WEB-005 | Info Disclosure | Swagger/OpenAPI endpoint exposed in production revealing full API surface | Swashbuckle | Medium | Medium | **Medium** | Disable Swagger in production; or restrict to authenticated internal users only | OWASP A05, SE:08 |
| T-WEB-006 | EoP | Missing CORS restriction allows cross-origin requests from malicious frontend | CORS Policy | Medium | Medium | **Medium** | Explicit CORS allow-list (tenant-registered origins only); deny `*` | OWASP A05, NIST AC-4, SE:08 |
| T-WEB-007 | Tampering | Request body injection via batch garment import (malicious JSON in bulk upload) | Batch Endpoint | Medium | High | **High** | Schema validation (OpenAPI); input sanitization; max batch size (100 items per spec); parameterized Cosmos queries | OWASP A03, NIST SI-10 |

---

### 7. identity/auth — Threat Table

| ID | STRIDE | Description | Component | Likelihood | Impact | Risk | Mitigation | Standards |
|---|---|---|---|---|---|---|---|---|
| T-AUTH-001 | Spoofing | Tenant impersonation — valid Entra token from registered tenant used to access another tenant's data | JWT / Tenant Claims | High | High | **Critical** | Validate `tid` claim against Cosmos tenant registry on every request; reject mismatched tenants; integration tests for isolation | OWASP A01, NIST AC-3, SE:05 |
| T-AUTH-002 | EoP | Coarse OAuth scopes (Read/Write only) allow garment ingestion user to delete profiles | OAuth Scopes | Medium | High | **High** | Define fine-grained app roles: `Assessment.Read`, `Assessment.Write`, `GarmentCatalog.Write`, `Profile.Delete`, `Admin.Manage` | OWASP A01, NIST AC-6, SE:05 |
| T-AUTH-003 | Spoofing | Suspended tenant's cached token continues to authorize requests | Tenant Status Check | Medium | High | **High** | Check tenant status (Active) on every request against Cosmos; cache with short TTL (≤5 min); CAE for revocation | OWASP A07, NIST AC-2, SE:05 |
| T-AUTH-004 | Repudiation | Authentication events (login, token issuance, permission changes) not captured in audit log | Entra ID Audit | Medium | Medium | **Medium** | Enable Entra ID audit + sign-in logs → Log Analytics; SOC 2 CC7 evidence | NIST AU-2, SE:10, CIS §1 |
| T-AUTH-005 | EoP | Service principal credential (secret or cert) compromised → full API access as tenant | Service Principal | Low | High | **Low** | Certificate-based credentials (not secrets); short validity; Key Vault storage; rotation policy; monitor for anomalous SP sign-ins | NIST IA-5, SE:09, IM-6 |
| T-AUTH-006 | Spoofing | No BIPA consent verification in auth flow — photos processed without confirmed consent | Consent Verification | High | High | **Critical** | Require consent claim or header in assessment requests; reject if absent; log consent evidence | BIPA §15(b), OWASP A01, AC-3 |

---

### 8. ai-ml — Threat Table

| ID | STRIDE | Description | Component | Likelihood | Impact | Risk | Mitigation | Standards |
|---|---|---|---|---|---|---|---|---|
| T-AIML-001 | Tampering | Adversarial image crafted to produce incorrect body landmarks (targeted misclassification) | ML Endpoint | Medium | High | **High** | Input image validation (dimensions, format, quality); output range validation; confidence threshold enforcement (≥70%); anomaly detection on measurements | OWASP LLM01, NIST SI-10, AI-5 |
| T-AIML-002 | Info Disclosure | Model extraction via repeated queries reconstructing body measurement model behavior | ML Endpoint | Medium | Medium | **Medium** | Rate limit per-tenant API calls to AI endpoint; monitor query patterns; avoid returning raw model internals | OWASP LLM10, NIST RA-5, AI-6 |
| T-AIML-003 | EoP | Prompt injection via embedded text in photo EXIF/metadata bypasses Content Safety and manipulates measurement output | AI Vision + ML | High | High | **Critical** | Strip all EXIF/metadata before AI processing; Content Safety filter before landmark extraction; output schema validation | OWASP LLM01, SE:08, AI-5 |
| T-AIML-004 | Info Disclosure | AI service retains/logs biometric photo data beyond processing — violates BIPA | Azure AI Services | Medium | High | **High** | Verify DPA data handling; opt-out of Abuse Monitoring human review; confirm no data retention for training | OWASP LLM06, BIPA §15(d), AI-2 |
| T-AIML-005 | DoS | Large/complex adversarial image causes excessive AI compute, exhausting quota or increasing costs | AI Vision | Medium | Medium | **Medium** | Enforce max image dimensions (4096×4096 per spec); resize before submission; set AI service compute timeout; cost alerting | OWASP LLM04, NIST SC-5, AI-3 |
| T-AIML-006 | Repudiation | AI model version and confidence score not recorded per assessment — cannot audit decision lineage | Assessment Pipeline | Medium | Medium | **Medium** | Store model version (`YYYY-MM-DD-vN`), prompt hash, confidence score in FitAssessment entity; immutable once written | NIST AU-3, AI-6, SOC 2 CC7 |
| T-AIML-AI-001 | Tampering | Training data poisoning — biased or manipulated training dataset produces systematically inaccurate measurements for certain body types | Training Pipeline | Low | High | **Low** | Document training data provenance; bias evaluation across demographics; periodic accuracy audits; dataset versioning | OWASP LLM03, NIST AI RMF MS-2.10, AI-3 |
| T-AIML-AI-002 | Info Disclosure | Sensitive training data memorized by model and leaked via specific query patterns | ML Model | Low | High | **Low** | Training data scrubbing; differential privacy techniques if fine-tuning; output filtering; membership inference testing | OWASP LLM06, NIST AI RMF MS-2.5, AI-2 |
| T-AIML-AI-003 | EoP | Minor detection bypass — adversarial image evades Content Safety minor detection, allowing processing of minor's photo | Content Safety Filter | Medium | High | **High** | Defense-in-depth: Content Safety + secondary age estimation check; reject ambiguous cases; human review escalation path | SE:08, BIPA, AI-5 |

---

### Security Model Summary

**Total Threats by STRIDE Category:**

| Category | Count |
|---|---|
| Spoofing | 6 |
| Tampering | 10 |
| Repudiation | 4 |
| Information Disclosure | 11 |
| Denial of Service | 4 |
| Elevation of Privilege | 7 |
| **Total** | **42** |

**Risk Distribution:**

| Rating | Count |
|---|---|
| Critical | 5 |
| High | 20 |
| Medium | 11 |
| Low | 6 |

**Top 5 Highest-Risk Threats:**

| Rank | ID | Description | Risk |
|---|---|---|---|
| 1 | T-AUTH-001 | Tenant impersonation via `tid` claim bypass — cross-tenant data access | **Critical** |
| 2 | T-WEB-002 | Malicious file upload (zip bomb, polyglot) bypassing image validation | **Critical** |
| 3 | T-AIML-003 | Prompt injection via photo EXIF/metadata manipulating AI measurement output | **Critical** |
| 4 | T-AUTH-006 | No BIPA consent verification — processing photos without confirmed consent | **Critical** |
| 5 | T-INFRA-002 | DDoS on public ACA ingress without WAF/DDoS Standard protection | **Critical** |

**Coverage Assessment:** All 8 buckets have threats identified across all applicable STRIDE categories. AI-specific extensions applied to ai-ml bucket with 3 additional AI-specific threats (T-AIML-AI-001 through T-AIML-AI-003). No unmapped threats.

---

## Phase 5: Backlog Generation

**Format:** GitHub Issues (`{{SEC-TEMP-N}}`)
**Autonomy Tier:** Partial (generated for review, pending user approval for creation)
**Handoff File:** `backlog-handoff.md` (same directory)

### Work Item Summary

| Priority | Count | Description |
|---|---|---|
| P1 — Critical | 7 | Pre-production blockers (BIPA consent, tenant isolation, upload hardening, prompt injection, DDoS/WAF, BIPA policy, private network) |
| P2 — High | 22 | SOC 2 readiness and core security controls |
| P3 — Medium | 15 | Hardening, monitoring, and compliance gaps |
| P4 — Low | 8 | Defense-in-depth and supply chain |
| **Total** | **52** | |

### By Bucket

| Bucket | P1 | P2 | P3 | P4 | Total |
|---|---|---|---|---|---|
| identity/auth | 2 | 3 | 1 | 1 | 7 |
| data | 1 | 5 | 1 | 1 | 8 |
| web/UI/reporting | 1 | 4 | 4 | — | 9 |
| ai-ml | 1 | 3 | 3 | 2 | 9 |
| infra | 2 | 2 | 2 | 1 | 7 |
| devops/platform-ops | — | 2 | 1 | 1 | 4 |
| build | — | 2 | 1 | 1 | 4 |
| messaging | — | 1 | 3 | 1 | 5 |

### Dependency Chain (Critical Path)

1. **{{SEC-TEMP-6}}** BIPA written policy → must exist before any photo collection
2. **{{SEC-TEMP-1}}** Consent verification → depends on BIPA policy
3. **{{SEC-TEMP-7}}** Private network deployment → enables private endpoints for all services
4. **{{SEC-TEMP-2}}** Tenant ID validation → foundational auth control
5. **{{SEC-TEMP-3}}** Upload hardening → must precede AI processing
6. **{{SEC-TEMP-4}}** Prompt injection defense → depends on EXIF stripping from upload hardening

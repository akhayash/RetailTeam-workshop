# Product Definition: AI Clothing Fit Assessment Agent

## Problem

Online clothing returns remain one of the highest-cost challenges in e-commerce retail. A significant portion of returns in the clothing category stem from fit issues — customers cannot accurately judge how a garment will fit before purchasing. This drives up logistics costs, erodes margins, and creates a poor customer experience.

## Vision

Provide shoppers with a real-time, AI-powered fit assessment that uses their own photos to predict garment fit — reducing uncertainty at purchase time and cutting return rates.

## Product Overview

A standalone AI Fit Assessment Agent that accepts shopper-provided photo material, extracts body measurements, and compares them against garment sizing data to deliver a personalized fit recommendation. The agent exposes an integration layer for frontend store embedding.

## Target Users

| Persona | Description |
|---------|-------------|
| Online Shopper | Wants confidence that a garment will fit before buying |
| Retail Frontend Team | Needs a drop-in integration to surface fit guidance in the product detail page |
| Merchandising / Catalog Team | Maintains garment sizing data consumed by the agent |

## Core Capabilities

### 1. Photo-Based Body Estimation

- Accept one or more photos uploaded by the shopper (front and side views).
- Use computer vision models to estimate key body dimensions (chest, waist, hips, inseam, shoulder width).
- Support common smartphone camera resolutions; no special hardware required.

### 2. Fit Prediction Engine

- Map estimated body dimensions against the garment's size chart and construction tolerances.
- Return a fit score per available size (e.g., "Size M — Ideal Fit", "Size S — Tight at Hips").
- Account for garment-specific fit intent (slim, regular, relaxed).

### 3. Recommendation Delivery

- Present a clear size recommendation with confidence indicator.
- Surface contextual guidance (e.g., "This item runs small — we suggest sizing up").
- Optionally show a visual overlay illustrating fit areas of concern.

### 4. Integration Layer (API)

- RESTful API with OpenAPI specification for frontend consumption.
- Stateless request model — each assessment is self-contained.
- Endpoints: photo upload, assessment request, recommendation retrieval.
- Authentication via API key or OAuth token scoped to the storefront.

## Non-Functional Requirements

| Attribute | Target |
|-----------|--------|
| Latency | Fit recommendation returned within 5 seconds of photo submission |
| Availability | 99.9% uptime SLA |
| Privacy | Photos processed in-memory only; no persistent storage of biometric data unless user opts in |
| Scalability | Handle peak traffic of 500 concurrent assessments |
| Security | TLS in transit, encrypted at rest for any temporarily cached data; GDPR/CCPA compliant |

## Success Metrics

| Metric | Baseline | Target |
|--------|----------|--------|
| Fit-related return rate | Current baseline (measure) | 30% reduction within 6 months of launch |
| Assessment adoption | — | 20% of clothing PDPs show an initiated assessment |
| Recommendation accuracy | — | ≥ 85% of users who follow the recommendation report satisfactory fit |
| Net Promoter Score (feature) | — | ≥ 40 |

## Scope Boundaries

### In Scope

- Standalone microservice with exposed REST API.
- AI model for body measurement estimation from photos.
- Size mapping engine consuming structured garment size data.
- SDK / widget reference implementation for frontend integration.

### Out of Scope (v1)

- Virtual try-on / augmented reality visualization.
- Integration with in-store kiosks or POS systems.
- Automatic garment data ingestion from supplier feeds (manual catalog import for v1).
- Support for non-clothing categories (shoes, accessories).

## Architecture

### Architectural Style

The Fit Assessment Agent is a **stateless, multi-tenant microservice** built on Clean Architecture
principles and exposed via an API-first contract. It follows a **request-scoped processing pipeline**:
each assessment is a self-contained transaction with no session state, enabling horizontal scaling and
predictable latency under bursty retail traffic.

Key style decisions:

- **API-first**: The OpenAPI 3.x contract is the source of truth; client SDKs and the service implementation
  are generated/validated against it.
- **Multi-tenant by partition**: Tenant isolation is enforced at the data layer (Cosmos DB partition keys)
  and at the auth layer (Entra ID scopes per storefront).
- **Ephemeral data plane for biometrics**: Photos never reach long-term storage. They flow through a
  short-lived blob with a 60-second TTL and are purged immediately after measurement extraction.

### High-Level Component Diagram

```
                       ┌───────────────────────────┐
                       │       Storefront          │
                       │  (PDP widget / SDK)       │
                       └──────────────┬────────────┘
                                      │ HTTPS + OAuth2 (Entra ID)
                                      ▼
                       ┌───────────────────────────┐
                       │    API Gateway / WAF      │
                       │  (rate limit, TLS term.)  │
                       └──────────────┬────────────┘
                                      │
                       ┌──────────────▼────────────┐
                       │   Fit Assessment API      │
                       │   (ASP.NET Core, ACA)     │
                       │  ┌─────────────────────┐  │
                       │  │ Controllers (v1)    │  │
                       │  │ Auth / Validation   │  │
                       │  │ Correlation / OTel  │  │
                       │  └─────────┬───────────┘  │
                       └────────────┼──────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌────────────────┐         ┌─────────────────┐         ┌──────────────────┐
│ Image Pipeline │         │ Assessment      │         │ Catalog &        │
│  - Validation  │         │  Engine         │         │ Profile Services │
│  - Transient   │◀───────▶│  - Size mapping │◀───────▶│  - Garments      │
│    Blob (60s)  │         │  - Fit scoring  │         │  - Shopper refs  │
│  - Azure AI    │         │  - Confidence   │         │  - Tenants       │
│    Vision      │         │    & disclaimer │         │                  │
└──────┬─────────┘         └────────┬────────┘         └─────────┬────────┘
       │                            │                            │
       ▼                            ▼                            ▼
┌────────────────┐         ┌─────────────────┐         ┌──────────────────┐
│ Azure Blob     │         │  Telemetry &    │         │  Azure Cosmos DB │
│ (transient,    │         │  Audit Sink     │         │  (multi-tenant,  │
│  TTL purge)    │         │  (App Insights, │         │   partitioned,   │
│                │         │   Log Analytics)│         │   TTL on assess.)│
└────────────────┘         └─────────────────┘         └──────────────────┘
```

### Logical Components

| Component | Responsibility | Key Technology |
|-----------|----------------|----------------|
| API Gateway / WAF | TLS termination, rate limiting per tenant tier, OWASP rules | Azure Front Door / APIM |
| Fit Assessment API | Stateless REST endpoints, auth, request orchestration | ASP.NET Core 8 on Azure Container Apps |
| Image Pipeline | Photo validation (size, format, quality), upload to transient blob, body measurement extraction | Azure AI Vision (Image Analysis), Azure Blob Storage |
| Assessment Engine | Maps measurements to garment size charts, applies fit-intent rules, computes per-area fit score and confidence | .NET domain services (VirtualMirror.Services) |
| Catalog Service | CRUD for garment size data, normalization across brands, fit-intent metadata | Cosmos DB container `garments` (partition: tenantId) |
| Shopper Profile Service | Optional opt-in profile storage (measurements only, never photos), pseudonymous shopper reference | Cosmos DB container `profiles` (partition: tenantId) |
| Tenant Service | Tenant onboarding, API scopes, configuration overrides | Cosmos DB container `tenants` + Azure App Configuration |
| Telemetry & Audit Sink | Structured logs, distributed traces, SLO metrics, model-drift signals | OpenTelemetry → Azure Monitor / App Insights |
| Secrets & Config | Connection strings, model endpoints, feature flags | Azure Key Vault, Azure App Configuration |
| Orchestration / Local Dev | Multi-service composition for local + integration testing | .NET Aspire AppHost |

### Request Flow: Fit Assessment

1. **Client request** — Storefront widget calls `POST /v1/assessments` with garment ID and photo(s),
   authenticated via Entra ID bearer token scoped to the tenant.
2. **Gateway** — TLS terminated; rate-limit and WAF rules applied; request forwarded to the API.
3. **API host** — Validates token, extracts `tenantId`, applies request-level OpenTelemetry correlation ID.
4. **Image validation** — Synchronous checks for format (JPEG/PNG/HEIC), size (≤ 10 MB), and quality
   heuristics (resolution, blur, exposure). Failed validation returns `400` with actionable guidance.
5. **Transient upload** — Image streamed to a tenant-scoped Azure Blob container with a 60-second TTL
   and a per-request SAS URL.
6. **Measurement extraction** — Azure AI Vision is invoked to estimate body landmarks → derived
   measurements (chest, waist, hips, inseam, shoulder). The image reference is then deleted explicitly,
   and TTL serves as a defense-in-depth purge guarantee.
7. **Garment lookup** — Catalog Service fetches the garment's normalized size chart and fit intent
   (`slim` / `regular` / `relaxed`) from Cosmos DB.
8. **Fit scoring** — Assessment Engine compares measurements to each available size, applies tolerance
   bands per body area, and produces a 5-point fit scale per area plus an overall recommended size.
9. **Confidence gating** — If model confidence is below threshold (~70%), the response includes
   `isLowConfidence: true` and a user-facing `disclaimer` rather than a hard recommendation.
10. **Response** — JSON payload returned to the storefront; assessment record persisted to Cosmos with
    a TTL (no raw image, no biometric raw vectors).
11. **Telemetry** — Trace, metrics, and audit log emitted; PII / biometrics never leave the in-memory
    boundary.

Target end-to-end p95 latency: **< 5 seconds**.

### Data Architecture

| Store | Purpose | Retention | Isolation |
|-------|---------|-----------|-----------|
| Azure Blob (transient) | Photo bytes during inference only | 60-second TTL + explicit delete | Per-tenant container, SAS-scoped |
| Cosmos DB `assessments` | Assessment results & audit metadata | TTL (e.g., 24h–30d, tenant-configurable) | Partition key = `tenantId` |
| Cosmos DB `garments` | Normalized size charts, fit intent, brand metadata | Tenant-managed | Partition key = `tenantId` |
| Cosmos DB `profiles` | Opt-in shopper measurements (no photos) | Until shopper revokes consent | Partition key = `tenantId`; opaque `shopperRef` |
| Cosmos DB `tenants` | Tenant config, scopes, feature flags | Lifecycle of tenant | Single shared container, tenant ID as id |
| Azure Key Vault | Secrets (Cosmos keys, AI endpoints) | Versioned, rotated | Managed Identity from ACA |
| App Configuration | Feature flags, model version pinning | Versioned | Tenant overrides via labels |

What is **never** stored: raw photos, raw biometric embeddings, derived measurements outside an opted-in
profile, and any direct PII (name, email) — the storefront supplies only an opaque `shopperRef`.

### Security & Privacy Boundaries

- **AuthN/AuthZ**: Entra ID OAuth 2.0 client credentials per storefront; per-operation scopes
  (`assessments.write`, `garments.read`, etc.); managed identities for all Azure-to-Azure calls.
- **Transport**: TLS 1.2+ enforced end-to-end; HSTS at the gateway.
- **Input validation**: OpenAPI schema validation + custom validators at the controller boundary;
  image content sniffing to reject disguised payloads.
- **Tenant isolation**: Enforced in the data access layer — every repository query requires a
  `tenantId` and is rejected if missing; Cosmos partition keys prevent cross-tenant reads.
- **Privacy**: Photos are processed in-memory and the ephemeral blob; no biometric persistence by
  default. Opt-in profile storage requires explicit consent recorded in the audit log.
- **Audit**: All assessment requests emit an immutable audit event (tenant, opaque shopperRef,
  garmentId, modelVersion, confidence, outcome) — never the image or raw measurements unless opted in.
- **Threat surface**: Aligned to OWASP Top 10 — SAST/SCA in CI, container image scanning, dependency
  pinning, and rate limiting to mitigate scraping/abuse.

### Compliance & Industry Baseline Alignment

The security plan is designed to align with the following industry baselines. The Fit Assessment
service does **not** itself process payment card data, but it is intended to be embedded in retail
storefronts that do — so its controls are designed to live cleanly inside a PCI DSS environment
without expanding the cardholder data scope.

#### PCI DSS v4.0 (payments-adjacent posture)

The service is **out of scope for cardholder data** by design (no PAN, CVV, or payment instrument is
ever accepted, transmitted, or stored). Controls are implemented so that embedding the widget on a
PCI-regulated PDP does **not** drag the storefront into expanded scope:

| PCI DSS Requirement | How the service satisfies it |
|---------------------|------------------------------|
| Req 1 — Network security controls | Private endpoints, WAF at the edge, egress restrictions on Container Apps |
| Req 2 — Secure configurations | Hardened base images, no default credentials, IaC-only configuration via Bicep |
| Req 3 — Protect stored data | No CHD ever stored; biometrics are ephemeral; Cosmos data encrypted at rest with CMK option |
| Req 4 — Encrypt transmission | TLS 1.2+ enforced; strong ciphers only; HSTS |
| Req 5 — Anti-malware | Container image scanning in CI; managed runtime base updates |
| Req 6 — Secure development | SAST, SCA, peer review, OWASP ASVS aligned, signed builds |
| Req 7 — Least privilege | Per-operation OAuth scopes; managed identities with minimum RBAC |
| Req 8 — Identify and authenticate | Entra ID with MFA for human admin access; service principals for workloads |
| Req 9 — Physical access | Inherited from Azure (PCI DSS attested) |
| Req 10 — Log and monitor | OpenTelemetry → Azure Monitor; immutable audit log; 12-month retention |
| Req 11 — Test security | Quarterly DAST; annual penetration test; continuous dependency scanning |
| Req 12 — Information security policy | Documented in this product definition + repository constitution; reviewed annually |

#### SOC 2 Type II (Trust Services Criteria)

| TSC | Implementation |
|-----|---------------|
| **Security (CC)** | Defense-in-depth controls listed above; documented incident response runbooks; access reviews quarterly |
| **Availability (A)** | 99.9% SLO; multi-AZ deployment; auto-scaling; documented RTO < 1h / RPO < 15min for tenant config |
| **Processing Integrity (PI)** | Schema-validated inputs; deterministic fit-scoring with `modelVersion` recorded; confidence gating prevents silent low-quality output |
| **Confidentiality (C)** | Encryption in transit/at rest; tenant isolation; principle of least privilege; data classification labels |
| **Privacy (P)** | Mapped to GDPR/CCPA controls below; consent capture; data minimization by default |

Operational evidence (logs, change tickets, access reviews, vulnerability scans, training records) is
collected continuously to support an annual SOC 2 Type II audit.

#### NIST Cybersecurity Framework 2.0

| Function | Mapping |
|----------|---------|
| **Govern (GV)** | Security policy in repo constitution; risk register maintained per release; defined roles for security owner / privacy owner |
| **Identify (ID)** | Asset inventory via IaC; data flow diagrams; threat model per feature (STRIDE) |
| **Protect (PR)** | IAM (Entra ID + RBAC), data security (encryption + ephemeral handling), platform security (private endpoints, WAF), training |
| **Detect (DE)** | OpenTelemetry traces, Azure Monitor alerts, anomaly detection on auth failures and rate-limit hits, model drift alerts |
| **Respond (RS)** | Documented incident response plan; on-call rotation; tenant breach notification SLAs aligned to GDPR's 72-hour rule |
| **Recover (RC)** | Backup of tenant configuration; IaC-driven environment rebuild; disaster recovery exercise at least annually |

#### OWASP ASVS v4 (Level 2) and OWASP Top 10

OWASP ASVS Level 2 is the application security baseline. Key chapters and how they map:

| ASVS Chapter | Control |
|--------------|---------|
| V1 — Architecture | Threat model maintained per feature; Clean Architecture enforces trust boundaries |
| V2 — Authentication | Entra ID OAuth 2.0 client credentials; no passwords accepted by the service |
| V3 — Session Management | Stateless API — no server-side sessions to compromise |
| V4 — Access Control | Tenant-scoped authorization at the data access layer; deny-by-default |
| V5 — Validation, Sanitization, Encoding | OpenAPI schema validation, content-type sniffing, output encoding for any JSON error messages |
| V7 — Error Handling & Logging | Structured logs, no sensitive data in errors, correlation IDs propagated |
| V8 — Data Protection | Ephemeral biometric handling; encryption at rest; Key Vault for secrets |
| V9 — Communications | TLS 1.2+, strong cipher suites only |
| V10 — Malicious Code | Image content sniffing; container image signing and scanning |
| V12 — File & Resources | Upload size cap (10 MB), allow-listed MIME types, scanned before processing |
| V13 — API & Web Service | OpenAPI-first contract; rate limiting; per-operation scopes |
| V14 — Configuration | IaC, no secrets in code, App Configuration with audit trail |

OWASP Top 10 (2021) coverage is verified continuously in CI through SAST + SCA + DAST and reviewed
during threat modeling for each release.

#### GDPR & CCPA (customer data)

The service is built on **data minimization** and **privacy by design** so that retailer-tenants
remain compliant when they embed it.

| Right / Obligation | Implementation |
|--------------------|----------------|
| Lawful basis (GDPR Art. 6) | Storefront captures consent before invoking the service; consent reference passed in request and recorded in audit log |
| Special-category data (GDPR Art. 9 — biometrics) | Photos and derived measurements treated as special-category data; processed only with explicit consent; ephemeral by default |
| Data minimization (Art. 5(1)(c)) | No PII accepted; opaque `shopperRef`; no raw image persistence; only measurements stored on opt-in |
| Purpose limitation (Art. 5(1)(b)) | Data used solely for fit assessment; never shared with third parties; no profiling for advertising |
| Storage limitation (Art. 5(1)(e)) | Cosmos TTL on assessments; 60-second blob TTL; opt-in profiles deleted on revocation |
| Right of access / portability (Art. 15, 20) | Tenant-facing API to export a shopper's stored profile in machine-readable JSON |
| Right to erasure (Art. 17) — "Right to delete" (CCPA §1798.105) | Hard delete endpoint per `shopperRef`; cascading purge across containers; verifiable within 30 days |
| Right to rectification (Art. 16) | Profile update endpoint; audit trail of changes |
| Right to opt out of sale/sharing (CCPA §1798.120) | No data sale or sharing — documented and enforced architecturally |
| Notice at collection (CCPA §1798.100) | Storefront SDK surfaces privacy notice template; categories of data collected disclosed |
| Breach notification (GDPR Art. 33 — 72h) | Incident response runbook triggers tenant notification within 72 hours of confirmed breach |
| International transfers (Chapter V) | Single-region deployment per tenant; EU tenants pinned to EU regions; SCCs in DPAs |
| Data Protection Impact Assessment (Art. 35) | DPIA completed for biometric processing; reviewed per major release |
| Records of processing (Art. 30) | Maintained centrally; data flow diagrams kept current |
| Data Processing Agreement | Standard DPA template provided to all tenants; sub-processor list published |

The service operates as a **Processor** (GDPR) / **Service Provider** (CCPA); the retailer-tenant
remains the Controller / Business and owns the consumer relationship.

#### Compliance Operating Model

- **Continuous control monitoring** via Azure Monitor + Defender for Cloud Regulatory Compliance
  dashboards (PCI DSS, ISO 27001, SOC 2, NIST CSF templates enabled).
- **Annual third-party assessments**: SOC 2 Type II audit and penetration test.
- **Quarterly internal reviews**: access reviews, vulnerability remediation SLAs, DPIA refresh.
- **Per-release gates**: threat model review, security checklist signoff, IaC `what-if` review,
  changelog of security-relevant changes.

### Deployment Topology

- **Compute**: Azure Container Apps, single region for v1, with multi-AZ replicas; auto-scale 2–10
  instances driven by HTTP concurrency and CPU.
- **Networking**: Private endpoints for Cosmos DB, Blob Storage, Key Vault; egress restricted via
  Container Apps environment.
- **Observability stack**: OpenTelemetry SDK in-app → Azure Monitor; SLO dashboards for latency,
  error rate, confidence distribution, and model drift signals.
- **CI/CD**: GitHub Actions pipeline → build, test (unit + contract + integration + NBomber load
  smoke), Bicep `what-if`, then canary deploy to staging → prod with feature-flag-gated rollout and
  automated rollback under 15 minutes.
- **Infrastructure as Code**: Bicep modules per resource (ACA, Cosmos, Blob, Key Vault, App Config,
  Front Door); environment promotion via parameter files (`dev` → `staging` → `prod`); drift
  detection on a schedule.

### Integration Surfaces

- **REST API (v1)** — Versioned, OpenAPI-described, JSON over HTTPS. Primary integration for
  storefronts.
- **Frontend SDK / Widget** — Reference TypeScript SDK and embeddable PDP widget that handles photo
  capture guidance, consent UX, and result rendering.
- **Catalog ingestion** — v1 manual import endpoint (`POST /v1/garments`) for merchandising teams;
  future-state event-driven ingestion is out of scope for v1.
- **Telemetry export** — Azure Monitor workbooks plus optional tenant-scoped metrics export for
  retailers who want to embed adoption KPIs into their own analytics.

### Cross-Cutting Concerns

| Concern | Approach |
|---------|----------|
| Resilience | Circuit breakers around Azure AI Vision; retries with jitter; graceful degradation to size-chart-only recommendation if vision fails |
| Performance | Streamed uploads; warm container instances; pinned model version to avoid cold-start regressions |
| Versioning | URI-versioned API (`/v1/...`); backward-compatible Cosmos document schemas with `schemaVersion` field |
| Feature flags | Azure App Configuration with tenant-scoped labels; safe rollout of new model versions and scoring rules |
| Model governance | `modelVersion` recorded on every assessment; periodic bias/accuracy evaluation against a held-out diverse dataset |
| Cost control | Auto-scale floor of 2 instances; transient blob TTL prevents storage bloat; Cosmos autoscale RUs per container |

## Key Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Low photo quality leads to inaccurate estimates | Poor recommendations, loss of trust | Provide real-time photo guidance; reject unusable images with actionable feedback |
| Garment size data inconsistency across brands | Incorrect mapping | Normalize size data on ingestion; flag gaps for merchandising review |
| User privacy concerns around body photos | Low adoption | Process photos ephemerally; communicate privacy posture clearly in UX |
| Model bias across body types | Inequitable experience | Train and validate on diverse body datasets; monitor accuracy across demographic segments |

## Release Strategy

| Phase | Scope | Timeline Indicator |
|-------|-------|--------------------|
| Alpha | Internal testing with synthetic + employee photo data | Phase 1 |
| Beta | Limited rollout to 10% of traffic on select categories | Phase 2 |
| GA | Full rollout across clothing categories with SDK for partner stores | Phase 3 |

## Open Questions

1. What garment size data format do catalog teams currently maintain, and what normalization is required?
2. Which ML framework and hosting infrastructure aligns with the platform team's standards?
3. Are there existing customer consent flows that can be extended for photo upload, or is a new consent UX needed?
4. What is the acceptable cold-start latency for the ML model, and does the platform support GPU inference at scale?

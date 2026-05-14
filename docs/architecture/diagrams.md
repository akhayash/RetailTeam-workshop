# Architecture Diagrams: AI Clothing Fit Assessment Agent

**Version**: 1.0.0 | **Date**: 2026-05-13 | **Status**: Reference

Index of canonical ASCII architecture diagrams. Each diagram is built from the artifacts in `specs/001-clothing-fit-assessment/` and `docs/architecture/solution-architecture.md`.

## Diagrams in this document

1. [System Context](#1-system-context)
2. [Container View — VirtualMirror API](#2-container-view--virtualmirror-api)
3. [Three-Tier AI Pipeline](#3-three-tier-ai-pipeline)
4. [Assessment Request Sequence](#4-assessment-request-sequence)
5. [Multi-Tenant Data Architecture](#5-multi-tenant-data-architecture)
6. [Network and Security Topology](#6-network-and-security-topology)
7. [Deployment Topology](#7-deployment-topology)
8. [CI/CD Pipeline](#8-cicd-pipeline)
9. [Concept A — Cloud-Centric Platform](#9-concept-a--cloud-centric-platform)
10. [Concept B — Edge + AI Agent Operations](#10-concept-b--edge--ai-agent-operations)
11. [Concept C — Data Fabric / Intelligence Layer](#11-concept-c--data-fabric--intelligence-layer)
12. [Entity Relationship Model](#12-entity-relationship-model)

---

## 1. System Context

External actors and the VirtualMirror API boundary.

```text
+=================================================================+
|                         External Actors                          |
|                                                                  |
|  +----------------+   +-----------------+   +----------------+   |
|  |  Online        |   |  Retail         |   |  Operations    |   |
|  |  Shopper       |   |  Frontend       |   |  Team          |   |
|  |  (consumer)    |   |  Store (B2B)    |   |  (catalog mgmt)|   |
|  +-------+--------+   +--------+--------+   +--------+-------+   |
|          |                     |                     |           |
+----------|---------------------|---------------------|-----------+
           |                     |                     |
           |  (browser)          | REST/HTTPS          | REST/HTTPS
           |                     | OAuth 2.0 B2B       | OAuth 2.0
           |                     v                     v
           |          +------------------------------------+
           +--------->|         VirtualMirror API (v1)         |
                      |  Multi-tenant, .NET 8, stateless   |
                      +-----------------+------------------+
                                        |
                                        | Managed Identity
                                        v
              +-------------------------+--------------------------+
              |              Azure Service Plane                    |
              |                                                     |
              |  +----------+  +----------+  +----------+           |
              |  | Azure AI |  | Cosmos   |  | Blob     |           |
              |  | Services |  | DB       |  | Storage  |           |
              |  +----------+  +----------+  +----------+           |
              |                                                     |
              |  +----------+  +----------+  +----------+           |
              |  | Service  |  | Key      |  | Azure    |           |
              |  | Bus      |  | Vault    |  | Monitor  |           |
              |  +----------+  +----------+  +----------+           |
              +-----------------------------------------------------+
```

### Legend

| Arrow | Meaning |
|-------|---------|
| `--->` | Synchronous request / dependency |
| `===` | External boundary |

### Key Relationships

- Online Shopper interacts only through the Retail Frontend (never directly with VirtualMirror API)
- Retail Frontend authenticates to VirtualMirror API via Entra ID B2B (OAuth 2.0)
- Operations Team submits garment catalog data via the same API surface
- VirtualMirror API uses managed identity for all downstream Azure service calls (zero secrets)

---

## 2. Container View — VirtualMirror API

Logical layering inside the .NET 8 Web API following Clean Architecture.

```text
+===================================================================+
|                       VirtualMirror API (.NET 8)                       |
|                                                                    |
|  :--- Presentation Layer (VirtualMirror.Api) -----------------------:  |
|  :                                                              :  |
|  :  +----------------+  +----------------+  +----------------+  :  |
|  :  | Assessments    |  | Profiles       |  | Garments       |  :  |
|  :  | Controller     |  | Controller     |  | Controller     |  :  |
|  :  +-------+--------+  +-------+--------+  +-------+--------+  :  |
|  :          |                   |                   |           :  |
|  :          | +------------------------------+                  :  |
|  :          | | Middleware Pipeline          |                  :  |
|  :          | | * JWT validation             |                  :  |
|  :          | | * Tenant claim extraction    |                  :  |
|  :          | | * Correlation ID injection   |                  :  |
|  :          | | * Rate limiting (per tier)   |                  :  |
|  :          | | * FluentValidation           |                  :  |
|  :          | +------------------------------+                  :  |
|  :----------v-------------------v-------------------v-----------:  |
|                                                                    |
|  :--- Service Layer (VirtualMirror.Services) -----------------------:  |
|  :                                                              :  |
|  :  +-------------------+  +-----------------------+            :  |
|  :  | VirtualMirrorment     |  | ShopperProfile        |            :  |
|  :  | Service           |  | Service               |            :  |
|  :  +-------+-----------+  +-----------+-----------+            :  |
|  :          |                          |                        :  |
|  :  +-------v-----------+  +-----------v-----------+            :  |
|  :  | ImageValidator    |  | GarmentService        |            :  |
|  :  | BodyMeasurement   |  | (catalog mgmt)        |            :  |
|  :  | Extractor         |  +-----------------------+            :  |
|  :  | FitComparison     |                                       :  |
|  :  | Engine            |                                       :  |
|  :  +-------------------+                                       :  |
|  :--------------+-----------------------------------------------:  |
|                 |                                                  |
|  :--- Core Layer (VirtualMirror.Core) - zero deps -----------------:   |
|  :                                                              :  |
|  :  Models: Tenant, ShopperProfile, Garment, VirtualMirrorment      :  |
|  :  Interfaces: IRepository<T>, IAIClient, IBlobStore           :  |
|  :  Enums: FitScale, GarmentCategory, AssessmentStatus          :  |
|  :--------------+-----------------------------------------------:  |
|                 ^                                                  |
|  :--- Infrastructure Layer (VirtualMirror.Infrastructure) ---------:   |
|  :                                                              :  |
|  :  +--------------------+ +-------------------+               :   |
|  :  | FlorenceVision     | | ContentSafety     |               :   |
|  :  | Client (Foundry)   | | Client            |               :   |
|  :  +--------------------+ +-------------------+               :   |
|  :  +--------------------+ +-------------------+               :   |
|  :  | AzureOpenAI        | | CosmosRepository  |               :   |
|  :  | MeasurementClient  | | <T>               |               :   |
|  :  +--------------------+ +-------------------+               :   |
|  :  +--------------------+ +-------------------+               :   |
|  :  | BlobStorageService | | AssessmentQueue   |               :   |
|  :  | (60s TTL)          | | Service (SB)      |               :   |
|  :  +--------------------+ +-------------------+               :   |
|  :  +-------------------------------------------+              :   |
|  :  | AuditLogger / FeatureFlagsClient          |              :   |
|  :  +-------------------------------------------+              :   |
|  :--------------------------------------------------------------:  |
+===================================================================+
```

### Legend

- `:---:` Layer boundary (logical, not physical)
- `===` Service boundary (deployment unit)

### Key Relationships

- Presentation depends on Service interfaces only
- Service depends on Core interfaces only
- Infrastructure implements Core interfaces (dependency inversion)
- Core has zero external dependencies (testable in isolation)

---

## 3. Three-Tier AI Pipeline

The three tiers of AI processing with current (v1) and future (v2) services.

```text
+=================================================================+
|  TIER 1  ----  Validation (parallel)                            |
|                                                                 |
|  +----------------------+        +--------------------------+   |
|  | Florence-2 (Foundry) |        | Azure AI Content Safety  |   |
|  | * people detection   |        | * minor/age detection    |   |
|  | * bounding box check |        | * inappropriate content  |   |
|  | * multi-person reject|        | * moderation             |   |
|  +----------+-----------+        +-------------+------------+   |
|             |                                  |                |
|             |   +-------------------------+    |                |
|             |   | Defender for Storage    |    |                |
|             |   | * malware scan          |    |                |
|             |   +-----------+-------------+    |                |
|             |               |                  |                |
|             |  +------------v---+              |                |
|             |  | Local checks:  |              |                |
|             |  | * MIME type    |              |                |
|             |  | * size (10MB)  |              |                |
|             |  | * luminance>=40|              |                |
|             |  +----------------+              |                |
|             |                                  |                |
|             |  PASS         PASS               |                |
|             +------------+---------------------+                |
|                          v                                      |
+=========================|====================================== +
                          |
+=========================v=======================================+
|  TIER 2  ----  Measurement Extraction (v1)                      |
|                                                                 |
|  +-----------------------------------------------------------+  |
|  |     Azure OpenAI  GPT-5.2 Vision (native structured output)|  |
|  |                                                           |  |
|  |  Input  : photo bytes  +  heightCm  +  versioned prompt   |  |
|  |  Output : {                                               |  |
|  |             shoulderWidth, chestCircumference,            |  |
|  |             waistCircumference, hipCircumference,         |  |
|  |             inseam, armLength, confidence,                |  |
|  |             modelVersion                                  |  |
|  |           }                                               |  |
|  +---------------------------+-------------------------------+  |
|                              |                                  |
+=============================|===================================+
                              |
+=============================v===================================+
|  TIER 3  ----  Future / v2 (planned)                            |
|                                                                 |
|  +-----------------------------------------------------------+  |
|  | Custom SMPL Body Model  -  Azure AI Foundry Endpoint     |  |
|  |   * +/- 1-2 cm target accuracy (vs +/- 2-4 cm GPT-5.2)   |  |
|  |   * deterministic output                                  |  |
|  |   * trained on balanced demographic dataset              |  |
|  +-----------------------------------------------------------+  |
+=================================================================+
                              |
                              v
                  +-------------------------+
                  | FitComparisonEngine     |
                  | (deterministic, Core)   |
                  +-------------------------+
```

### Legend

- `===` Tier boundary
- `--->` Pipeline progression (only when prior tier PASSes)
- `- - >` Future / not in v1

### Key Relationships

- Tier 1 services run in parallel; ALL must PASS to advance
- Tier 2 receives only validated, malware-clean images plus mandatory height
- Tier 3 is a drop-in replacement for Tier 2 (same input/output contract via `IAIClient`)
- Failures at any tier short-circuit to a fallback response with disclaimer

---

## 4. Assessment Request Sequence

End-to-end request flow showing happy path and decision points.

```text
Frontend          API           Service        AI Tier 1    AI Tier 2     Cosmos    Blob
   |               |               |              |             |           |        |
   | POST          |               |              |             |           |        |
   | /assessments  |               |              |             |           |        |
   |-------------->|               |              |             |           |        |
   |               | JWT validate  |              |             |           |        |
   |               | rate limit    |              |             |           |        |
   |               |-------------->|              |             |           |        |
   |               |               | check queue  |             |           |        |
   |               |               | depth/p95    |             |           |        |
   |               |               |--+           |             |           |        |
   |               |               |  |           |             |           |        |
   |               |               |<-+           |             |           |        |
   |               |               |              |             |           |        |
   |               |               | upload if    |             |           |        |
   |               |               | image > 4MB  |             |           |        |
   |               |               |---------------------------------------------->| |
   |               |               | (SAS URL)    |             |           |        |
   |               |               |<----------------------------------------------| |
   |               |               |              |             |           |        |
   |               |               | validate img |             |           |        |
   |               |               |------------->|             |           |        |
   |               |               |              | * people    |           |        |
   |               |               |              | * content   |           |        |
   |               |               |              | * malware   |           |        |
   |               |               |<-------------|             |           |        |
   |               |               | PASS         |             |           |        |
   |               |               |              |             |           |        |
   |               |               | extract      |             |           |        |
   |               |               | measurements |             |           |        |
   |               |               | + heightCm   |             |           |        |
   |               |               |----------------------------+>|         |        |
   |               |               |              |             |           |        |
   |               |               |<----------------------------|           |        |
   |               |               | { meas, conf }             |           |        |
   |               |               |              |             |           |        |
   |               |               | compare vs   |             |           |        |
   |               |               | garment data |             |           |        |
   |               |               |--------------------------------------->|        |
   |               |               |<---------------------------------------|        |
   |               |               |              |             |           |        |
   |               |               | persist      |             |           |        |
   |               |               | assessment   |             |           |        |
   |               |               |--------------------------------------->|        |
   |               |               |              |             |           |        |
   |               |               | delete blob  |             |           |        |
   |               |               |---------------------------------------------->| |
   |               |               |              |             |           |        |
   |               |<--------------|              |             |           |        |
   |<--------------|               |              |             |           |        |
   |  200 OK       |               |              |             |           |        |
   |  + fit result |               |              |             |           |        |
   |  + confidence |               |              |             |           |        |
   |  + escalation |               |              |             |           |        |
   |    URL if low |               |              |             |           |        |
   |    confidence |               |              |             |           |        |
```

### Alternate Flows

- **Image rejected** at Tier 1: respond 422 with specific rejection reason and retake guidance
- **Low confidence** (< 70%) from Tier 2: respond 200 with `isLowConfidence: true`, disclaimer, escalation URL, and size chart fallback
- **Queue overflow** (depth > 50 or p95 > 4s): enqueue to Service Bus, respond 202 with poll URL and estimated wait time
- **AI service unavailable**: circuit breaker trips, respond 503 with fallback to size chart guidance

---

## 5. Multi-Tenant Data Architecture

Cosmos DB layout with hierarchical partition keys for tenant isolation.

```text
+=================================================================+
|                  Azure Cosmos DB Account                         |
|                                                                  |
|  +------------------------------------------------------------+  |
|  |  Database: virtualmirror                                        | |
|  |  (Autoscale 400-4000 RU/s shared throughput)                | |
|  |                                                             | |
|  |  :--- Container: tenants ----------------------------:      | |
|  |  :  Partition key: /id                                :     | |
|  |  :  Entities:                                         :     | |
|  |  :    * Tenant config                                 :     | |
|  |  :    * ToleranceBands (per garment category)         :     | |
|  |  :    * Rate limit tier                               :     | |
|  |  :----------------------------------------------------:     | |
|  |                                                             | |
|  |  :--- Container: garments --------------------------:       | |
|  |  :  Partition key: /tenantId                          :     | |
|  |  :  Entities:                                         :     | |
|  |  :    * Garment SKU (per tenant + size + version)    :      | |
|  |  :    * Measurements sub-object                       :     | |
|  |  :  Version history maintained                        :     | |
|  |  :----------------------------------------------------:     | |
|  |                                                             | |
|  |  :--- Container: profiles --------------------------:       | |
|  |  :  Partition key: /tenantId                          :     | |
|  |  :  Entities:                                         :     | |
|  |  :    * ShopperProfile (measurements only, no PII)    :     | |
|  |  :    * Opaque shopperRef                             :     | |
|  |  :  Deletion: hard delete <= 24h                      :     | |
|  |  :----------------------------------------------------:     | |
|  |                                                             | |
|  |  :--- Container: assessments -----------------------:       | |
|  |  :  Partition key: /tenantId                          :     | |
|  |  :  Entities:                                         :     | |
|  |  :    * VirtualMirrorment (result + modelVersion +        :     | |
|  |  :      correlationId)                                :     | |
|  |  :  TTL: 365 days (configurable per tenant)           :     | |
|  |  :----------------------------------------------------:     | |
|  |                                                             | |
|  |  :--- Container: audit -----------------------------:       | |
|  |  :  Partition key: /tenantId                          :     | |
|  |  :  Entities:                                         :     | |
|  |  :    * Tamper-evident audit log entries              :     | |
|  |  :  Immutable (Cosmos point-in-time restore)          :     | |
|  |  :----------------------------------------------------:     | |
|  +------------------------------------------------------------+  |
+==================================================================+

Hierarchical partition key strategy:  /tenantId -> /entityType -> /entityId

Repository<T> base class enforces tenant context on every query
(compile-time generic constraint).  Cross-tenant queries fail to compile.
```

### Legend

- `:---:` Cosmos container boundary
- `===` Azure account boundary

### Key Relationships

- Every container except `tenants` partitions by `/tenantId` for physical isolation
- `tenants` partitioned by `/id` because cross-tenant lookup is required at the admin layer
- TTL on `assessments` enables automatic compliance with data retention policy
- Audit container is immutable; entries are append-only

---

## 6. Network and Security Topology

Zero-trust topology with private endpoints and managed identity.

```text
+=================================================================+
|  Internet                                                        |
|                                                                  |
|  +---------------+                                               |
|  | Retail        |                                               |
|  | Frontend Store|                                               |
|  +-------+-------+                                               |
|          |                                                       |
|          | TLS 1.2+                                              |
|          | OAuth 2.0 (Entra ID)                                  |
|          v                                                       |
+----------|-------------------------------------------------------+
           |
+----------v-------------------------------------------------------+
|  Azure Subscription (production)                                 |
|                                                                  |
|  :--- Public Surface ----------------------------------------:   |
|  :  +-----------------------+                                :   |
|  :  | ACA Ingress (HTTPS)   |  WAF / rate limit at ingress  :   |
|  :  +----------+------------+                                :   |
|  :-------------|----------------------------------------------:  |
|                |                                                 |
|  :--- Container Apps Environment (Private VNet) -------------:   |
|  :  multi-AZ, /23 CIDR                                       :   |
|  :                                                           :   |
|  :  +---------------------------------------------+          :   |
|  :  | VirtualMirror API   replicas 2-10               |          :   |
|  :  | * managed identity (no secrets in env)      |          :   |
|  :  | * Entra ID JWT validation                   |          :   |
|  :  | * tenant claim extraction                   |          :   |
|  :  | * rate limit middleware                     |          :   |
|  :  +-----+---------+----------+----------+-------+          :   |
|  :        |         |          |          |                  :   |
|  :--------|---------|----------|----------|------------------:   |
|           |         |          |          |                      |
|  :--- Private Endpoint Subnet --------------------------:        |
|  :        |         |          |          |             :       |
|  :        v         v          v          v             :       |
|  :  +---------+ +--------+ +---------+ +-----------+   :        |
|  :  |Cosmos DB| |Key Vlt | | Blob    | | Service   |   :        |
|  :  |(private)| |private | | Storage | | Bus       |   :        |
|  :  +---------+ +--------+ +---------+ +-----------+   :        |
|  :--------|---------|----------|----------|-------------:        |
|           |         |          |          |                      |
|  :--- Azure AI Plane (managed identity auth) ---------:          |
|  :  +-----------+ +-------------+ +------------------+ :         |
|  :  | OpenAI    | | Florence-2  | | Content Safety   | :         |
|  :  | (MI auth) | | (MI auth)   | | (MI auth)        | :         |
|  :  +-----------+ +-------------+ +------------------+ :         |
|  :-----------------------------------------------------:         |
|                                                                  |
|  :--- Observability Plane ------------------------------:        |
|  :  +----------------+  +----------------------+        :        |
|  :  | Azure Monitor  |  | Log Analytics        |        :        |
|  :  | (App Insights) |  | (90d hot, 1y cold)   |        :        |
|  :  +----------------+  +----------------------+        :        |
|  :-------------------------------------------------------:       |
+==================================================================+
```

### Legend

- `===` Subscription / Internet boundary
- `:---:` Subnet or service plane
- `--->` Authenticated traffic (TLS 1.2+, managed identity unless noted)

### Key Relationships

- Only ACA Ingress is internet-exposed; all other services use private endpoints
- Managed identity replaces secrets for all service-to-service auth
- Tenant isolation is enforced at the application layer (JWT claims) — not network layer
- Private endpoint subnet has NSG denying all egress except to Azure service IPs

---

## 7. Deployment Topology

Multi-AZ production topology with environment promotion.

```text
+=================================================================+
|  GitHub Repository                                               |
|  +--------------------+                                          |
|  | main / 001-feature |                                          |
|  +--------+-----------+                                          |
+-----------|------------------------------------------------------+
            |
            | GitHub Actions
            v
+=================================================================+
|  Azure - Dev Environment (subscription dev)                      |
|                                                                  |
|  +-------------------+  +-----------+  +----------+              |
|  | ACA (1 replica)   |  | Cosmos DB |  | Blob     |              |
|  | Basic tier        |  | Free/Std  |  | Storage  |              |
|  +-------------------+  +-----------+  +----------+              |
|  Purpose: developer testing, fast feedback                       |
+==================================+===============================+
                                   |
                                   | manual gate / smoke tests
                                   v
+=================================================================+
|  Azure - Staging Environment (subscription staging)              |
|                                                                  |
|  +-------------------+  +-----------+  +----------+              |
|  | ACA (2 replicas)  |  | Cosmos DB |  | Blob     |              |
|  | Standard          |  | Standard  |  | Storage  |              |
|  +-------------------+  +-----------+  +----------+              |
|  Purpose: prod-parity, DAST, E2E tests, load testing             |
+==================================+===============================+
                                   |
                                   | manual prod gate
                                   v
+=================================================================+
|  Azure - Production Environment (subscription prod)              |
|                                                                  |
|  :--- Region: West Europe (primary) -----------------------:     |
|  :                                                          :    |
|  :  +-----------+        +-----------+        +---------+   :    |
|  :  |  AZ 1     |        |  AZ 2     |        |  AZ 3   |   :    |
|  :  | ACA       |        | ACA       |        | ACA     |   :    |
|  :  | replicas  |<------>| replicas  |<------>| replicas|   :    |
|  :  | (auto 2-10)        | (auto 2-10)        | (2-10)  |   :    |
|  :  +-----------+        +-----------+        +---------+   :    |
|  :                                                          :    |
|  :  +-------------------+  +---------------------+          :    |
|  :  | Cosmos DB         |  | Blob Storage        |          :    |
|  :  | Autoscale 400-4k  |  | LRS, 60s lifecycle  |          :    |
|  :  | continuous backup |  | immutable policy    |          :    |
|  :  +-------------------+  +---------------------+          :    |
|  :                                                          :    |
|  :  +-------------------+  +---------------------+          :    |
|  :  | Service Bus       |  | Key Vault           |          :    |
|  :  | Standard          |  | Standard            |          :    |
|  :  +-------------------+  +---------------------+          :    |
|  :----------------------------------------------------------:    |
|                                                                  |
|  RPO: < 1h (Cosmos continuous backup)                            |
|  RTO: < 30min (multi-AZ failover)                                |
+==================================================================+
```

### Legend

- `===` Subscription boundary
- `:---:` Region boundary
- `--->` Promotion path
- `<--->` Multi-AZ replication

### Key Relationships

- Each environment is an isolated Azure subscription with identical Bicep
- Promotion is unidirectional (dev → staging → prod) with manual gates
- Production runs across three availability zones for high availability
- Cosmos DB continuous backup provides point-in-time restore within 30 days

---

## 8. CI/CD Pipeline

Build, test, scan, and deploy stages.

```text
Developer
   |
   | git push (feature branch)
   v
+=================================================================+
|  GitHub Actions Workflow                                         |
|                                                                  |
|  +------------+  +----------------+  +---------------------+     |
|  | 1. Lint    |->| 2. Build       |->| 3. Unit Tests       |     |
|  | format     |  | dotnet build   |  | dotnet test         |     |
|  +------------+  +----------------+  +----------+----------+     |
|                                                  |               |
|                                                  v               |
|  +------------+  +----------------+  +---------------------+     |
|  | 4. Integ.  |  | 5. Contract    |  | 6. Coverage Gate    |     |
|  | Tests      |->| Tests          |->| >= 80% / 90%        |     |
|  | (Testcont) |  | (OpenAPI)      |  |                     |     |
|  +------------+  +----------------+  +----------+----------+     |
|                                                  |               |
|                                                  v               |
|  +--------------------+  +------------------+  +-------------+   |
|  | 7. SAST            |  | 8. SCA           |  | 9. SBOM     |   |
|  | (CodeQL/Semgrep)   |->| (dependency scan)|->| (CycloneDX) |   |
|  +--------------------+  +------------------+  +-----+-------+   |
|                                                      |           |
|                                                      v           |
|  +--------------------+  +------------------+                    |
|  | 10. Container Build|  | 11. Trivy Scan + |                    |
|  | (Docker)           |->| Notation Sign    |                    |
|  +--------------------+  +--------+---------+                    |
|                                   |                              |
+===================================|==============================+
                                    |
                                    v
+=================================================================+
|  Deploy to Staging                                               |
|                                                                  |
|  +-----------------+  +-----------------+  +----------------+    |
|  | 12. Bicep Deploy|->| 13. DAST Scan   |->| 14. E2E Smoke  |    |
|  | (what-if)       |  | (OWASP ZAP)     |  | Tests          |    |
|  +-----------------+  +-----------------+  +-------+--------+    |
+===========================================|=====================+
                                            |
                                            | manual gate
                                            v
+=================================================================+
|  Deploy to Production (canary rollout)                           |
|                                                                  |
|  +---------------------+  +----------------------+               |
|  | 15. Bicep Deploy    |->| 16. Feature Flag     |               |
|  | + Canary (10%)      |  | Progressive Rollout  |               |
|  +---------------------+  +-----------+----------+               |
|                                       |                          |
|                                       v                          |
|  +-------------------------------------+                         |
|  | 17. Azure Monitor                   |                         |
|  | * regression detection              |                         |
|  | * auto-rollback on SLO breach       |                         |
|  +-------------------------------------+                         |
+==================================================================+
```

### Legend

- `===` Pipeline stage group
- `--->` Sequential dependency

### Key Relationships

- Any failure short-circuits the pipeline; no progression past failed gates
- SAST / SCA / DAST / SBOM are mandatory per constitution (Security First)
- Container images are signed (Notation/cosign) and only signed images deploy to prod
- Production deployments are canary-first with auto-rollback on SLO regression

---

## 9. Concept A — Cloud-Centric Platform

Reference: this is the v1 implementation. See [solution-architecture.md](solution-architecture.md#concept-a-cloud-centric-platform-architecture) for the full description.

```text
+=================================================================+
|                  Concept A: Cloud-Centric Platform               |
|                                                                  |
|  +--------------+        +---------------------------------+     |
|  | Retail       |        |  Azure Container Apps           |     |
|  | Frontend     |------->|  VirtualMirror API (.NET 8)         |     |
|  | (B2B OAuth)  | HTTPS  |  * 2-10 replica auto-scale      |     |
|  +--------------+        |  * managed identity             |     |
|                          +--+----------+----------+--------+     |
|                             |          |          |              |
|                             v          v          v              |
|  +------------------+  +----------+ +-------+ +--------------+   |
|  | Azure AI Plane   |  | Cosmos DB| | Blob  | | Service Bus  |   |
|  | * Florence-2(T1) |  | (multi-  | | (60s  | | (async queue)|   |
|  | * Content Safety |  | tenant)  | | TTL)  | |              |   |
|  | * OpenAI GPT-5.2 |  +----------+ +-------+ +--------------+   |
|  | * AI Foundry(v2) |                                            |
|  +------------------+  +----------+ +----------+                 |
|                        | Key Vault| | Azure    |                 |
|                        | (secrets)| | Monitor  |                 |
|                        +----------+ +----------+                 |
+=================================================================+
```

### Tradeoffs

- **Gain**: Fastest time-to-market, lowest ops burden, fully managed services
- **Accept**: Azure vendor lock-in, single-region v1, cloud network dependency

---

## 10. Concept B — Edge + AI Agent Operations

Reference: future-state for in-store scenarios. See [solution-architecture.md](solution-architecture.md#concept-b-edge--ai-agent-enabled-operations).

```text
+=================================================================+
|              Concept B: Edge + AI Agent Operations               |
|                                                                  |
|  :--- In-Store Edge -----------------------------------:         |
|  :                                                     :         |
|  :  +-------------------+   +----------------------+   :         |
|  :  | Fitting Room      |   | Store Associate      |   :         |
|  :  | Camera / Kiosk    |   | Mobile AI Copilot    |   :         |
|  :  | * local pose      |   | * "size M slim"      |   :         |
|  :  |   detection       |   | * inventory check    |   :         |
|  :  | * edge cache      |   | * alternatives       |   :         |
|  :  | * privacy: local  |   | * human decides      |   :         |
|  :  +---------+---------+   +----------+-----------+   :         |
|  :            |                        |               :         |
|  :------------|------------------------|---------------:         |
|               |                        |                         |
|               | measurements only      | API call                |
|               | (not raw images)       |                         |
|               v                        v                         |
|  +-------------------------------------------------+             |
|  |          VirtualMirror API (Cloud Backend)          |             |
|  |  * fallback when edge confidence < threshold    |             |
|  |  * model updates pushed to edge                 |             |
|  |  * aggregated analytics for store ops           |             |
|  +-------------------------------------------------+             |
|                                                                  |
|  Human-in-the-loop:  AI recommends  -  associate decides  -      |
|                      shopper accepts or asks for alternatives    |
+=================================================================+
```

### Tradeoffs

- **Gain**: Strongest privacy (local processing), lower cloud cost per assessment, in-store applicability
- **Accept**: Device fleet management, model distribution complexity, hardware investment

---

## 11. Concept C — Data Fabric / Intelligence Layer

Reference: long-term vision for unified retail intelligence. See [solution-architecture.md](solution-architecture.md#concept-c-data-fabric--intelligence-layer).

```text
+=================================================================+
|         Concept C: Data Fabric / Intelligence Layer              |
|                                                                  |
|  :--- Source Domains ----------------------------------------:   |
|  :                                                            :  |
|  :  +-----------+   +----------+   +---------------------+   :   |V
|  :  | Shopper   |   | Garment  |   | Return & Exchange   |   :   |
|  :  | Measure-  |   | Catalog  |   | Transactions        |   :   |
|  :  | ments     |   |          |   |                     |   :   |
|  :  +-----+-----+   +----+-----+   +----------+----------+   :   |
|  :        |              |                    |              :   |
|  :--------|--------------|--------------------|--------------:   |
|           |              |                    |                  |
|           v              v                    v                  |
|  +-------------------------------------------------------+       |
|  |   Microsoft Fabric  -  Unified Semantic Layer         |       |
|  |   * lineage: measurement -> assessment -> outcome     |       |
|  |   * governance: PII classification, retention         |       |
|  |   * AI-ready data products (curated, cataloged)       |       |
|  |   * cross-domain joins: fit score <-> return rate     |       |
|  +-------+---------------+---------------+---------------+       |
|          |               |               |                       |
|          v               v               v                       |
|  +-------------+  +----------------+  +-----------------------+  |
|  | VirtualMirror   |  | Return         |  | Merchandising         |  |
|  | API         |  | Prediction     |  | Intelligence          |  |
|  | (real-time) |  | Model (batch)  |  | (size dist., trends)  |  |
|  +-------------+  +----------------+  +-----------------------+  |
+=================================================================+
```

### Tradeoffs

- **Gain**: Strategic data asset, cross-domain insights, AI/BI on same governed data
- **Accept**: Significant Microsoft Fabric investment, data engineering effort beyond fit assessment, longer time-to-value

---

## 12. Entity Relationship Model

Domain entities and their relationships.

```text
+--------------+         +------------------+
|              |         |                  |
|   Tenant     |---1:N-->|     Garment      |
|              |         |  (per size)      |
|  /id (PK)    |         |  /tenantId (PK)  |
|              |         |  /garmentId      |
+------+-------+         |  /sizeLabel      |
       |                 +--------+---------+
       |                          |
       |                          |
       | 1:N                      | referenced by
       v                          v
+------+---------+        +---------------------+
|                |        |                     |
| ShopperProfile |------->|   VirtualMirrorment     |
|                |  1:N   |                     |
|  /tenantId(PK) |        |  /tenantId (PK)     |
|  shopperRef    |        |  shopperRef         |
|  measurements  |        |  garmentRef         |
|  heightCm      |        |  perAreaFit         |
|                |        |  overallFit         |
+----------------+        |  confidence         |
                          |  modelVersion       |
                          |  correlationId      |
                          |  isLowConfidence    |
                          |  escalationUrl      |
                          +---------+-----------+
                                    |
                                    | writes to
                                    v
                          +---------------------+
                          |                     |
                          |   AuditLog          |
                          |                     |
                          |  /tenantId (PK)     |
                          |  immutable          |
                          +---------------------+
```

### Legend

- `--->` Foreign key reference
- `1:N` Cardinality

### Key Relationships

- One Tenant has many Garments and ShopperProfiles
- One ShopperProfile produces many VirtualMirrorments (one per garment evaluated)
- Every VirtualMirrorment writes an immutable AuditLog entry
- `shopperRef` is an opaque hash provided by the frontend — never PII

---

## Diagram Sources

These diagrams are derived from:

- [solution-architecture.md](solution-architecture.md) — system narrative and concept descriptions
- [research.md](../../specs/001-clothing-fit-assessment/research.md) — technology decisions R1–R7
- [data-model.md](../../specs/001-clothing-fit-assessment/data-model.md) — entity schemas
- [plan.md](../../specs/001-clothing-fit-assessment/plan.md) — project structure
- [tasks.md](../../specs/001-clothing-fit-assessment/tasks.md) — Bicep module list

When IaC files are created (tasks T091–T096c), these diagrams should be regenerated from the Bicep modules to ensure infrastructure-as-code parity.

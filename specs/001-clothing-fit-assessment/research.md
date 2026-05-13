# Research: AI Clothing Fit Assessment Agent

**Phase**: 0 — Research & Technology Decisions
**Date**: 2026-05-13
**Feature**: [spec.md](spec.md)

## R1: Body Measurement Extraction from Photos

**Decision**: Azure AI Vision (Custom Model) + Azure AI Body Tracking

**Rationale**: Azure AI Vision provides pre-built image analysis capabilities including person detection and segmentation. Combined with custom model training via Azure AI Custom Vision or Azure Machine Learning, we can fine-tune body landmark detection for measurement extraction. This aligns with the Microsoft stack requirement and integrates natively with Entra ID for authentication.

**Alternatives considered**:
- **MediaPipe (Google)**: Open-source body pose estimation. Strong accuracy but requires self-hosting, GPU management, and doesn't integrate with Azure identity. Rejected due to operational complexity and stack misalignment.
- **AWS Rekognition**: Competitive offering but violates Microsoft stack requirement.
- **Custom PyTorch model on Azure ML**: Maximum flexibility but significantly higher development cost and time-to-market. Could be a v2 enhancement if Azure AI Vision accuracy is insufficient.

**Implementation approach**:
1. Use Azure AI Vision for image quality validation (lighting, completeness, person detection)
2. Use Azure AI Custom Vision or Azure ML endpoint for body landmark extraction (17+ key points)
3. Derive measurements from landmark positions using anthropometric scaling algorithms
4. Confidence score derived from landmark detection confidence + image quality metrics

---

## R2: Multi-Tenant Data Isolation in Cosmos DB

**Decision**: Partition key strategy using hierarchical partition keys (tenant ID + entity type)

**Rationale**: Azure Cosmos DB supports hierarchical partition keys (GA since 2023), enabling efficient multi-tenant data isolation without separate databases per tenant. Data is physically co-located per tenant for query performance while maintaining logical isolation. Row-level security is enforced at the application layer via the repository pattern.

**Alternatives considered**:
- **Database-per-tenant**: Maximum isolation but expensive at scale and complex to manage. Rejected for v1 (< 50 tenants expected).
- **Container-per-tenant**: Good isolation but partition key management becomes complex. Rejected — hierarchical keys achieve equivalent isolation with less overhead.
- **Shared container with tenant ID filter**: Simplest but risk of cross-tenant data leakage if filter is missed. Rejected — hierarchical partition keys provide the same simplicity with physical isolation guarantees.

**Implementation approach**:
1. Hierarchical partition key: `/tenantId` → `/entityType` → `/entityId`
2. Repository base class enforces tenant scoping on all queries
3. Tenant context injected via middleware from authenticated JWT claims
4. Cosmos DB throughput provisioned at database level with autoscale (400–4000 RU/s)

---

## R3: Image Processing Pipeline & Transient Storage

**Decision**: Azure Blob Storage with lifecycle management (auto-delete after 60 seconds) + in-memory streaming

**Rationale**: Images must be uploaded to a temporary location for the AI model to process (Azure AI Vision requires a URL or byte stream). Using Azure Blob Storage with a 1-minute lifecycle policy ensures automatic purging. For images under 4 MB, direct byte stream to the AI endpoint avoids blob storage entirely.

**Alternatives considered**:
- **In-memory only**: Ideal for privacy but Azure AI Vision SDK requires either a URL or a stream. Large images (up to 10 MB) risk memory pressure under concurrent load. Hybrid approach chosen.
- **Azure Queue + background processing**: Adds latency and complexity. Rejected — synchronous processing meets the 5-second SLA.
- **Disk-based temp files in container**: Ephemeral but harder to audit and purge reliably. Rejected.

**Implementation approach**:
1. Images ≤ 4 MB: Stream directly to Azure AI Vision (no blob storage)
2. Images > 4 MB: Upload to transient blob container with 60-second TTL, pass SAS URL to AI endpoint, confirm deletion after processing
3. Blob container has immutable lifecycle policy preventing TTL modification
4. Audit log entry written on upload and deletion for compliance

---

## R4: Authentication & Authorization Architecture

**Decision**: Microsoft Entra ID with app registrations per tenant + managed identity for service-to-service

**Rationale**: Entra ID provides enterprise-grade OAuth 2.0 / OIDC with native support for multi-tenant app registrations. Each retail partner (tenant) gets a registered app with client credentials. The fit assessment service uses managed identity for accessing Azure resources (Cosmos DB, Blob Storage, Key Vault, AI services), eliminating secret management.

**Alternatives considered**:
- **API key-based auth**: Simpler but doesn't support token expiration, refresh, or fine-grained scopes. Rejected per constitution (II. Security First).
- **Azure API Management with subscription keys**: Good for rate limiting but adds another layer. Decision: Use APIM as the gateway but authentication stays with Entra ID.
- **Third-party IdP (Auth0, Okta)**: Unnecessary cost and complexity when Entra ID is already the enterprise standard. Rejected.

**Implementation approach**:
1. Entra ID multi-tenant app registration for the FitAssess API
2. Each tenant registered as a service principal with specific API permissions (scopes)
3. JWT validation middleware in ASP.NET Core with tenant claim extraction
4. Managed identity for all Azure resource access (zero secrets in config)
5. Azure API Management as gateway for rate limiting, request correlation, and caching

---

## R5: Fit Comparison Algorithm

**Decision**: Measurement delta calculation with tolerance bands per garment fit type

**Rationale**: The fit recommendation compares shopper body measurements against garment measurements per area. Each garment fit type (slim, regular, relaxed) defines different tolerance bands. A delta outside the band maps to the 5-point scale. This is deterministic (not ML) and highly testable.

**Alternatives considered**:
- **ML-based fit prediction**: Higher accuracy potential but requires training data (actual return/keep decisions). Can be added as v2 enhancement once data is collected. Rejected for MVP — insufficient training data at launch.
- **Size chart lookup only**: Too simplistic — doesn't account for individual body variation or garment fit type. Rejected.
- **Ensemble (delta + ML)**: Best accuracy but over-engineering for launch. Planned for v2.

**Implementation approach**:
1. For each body area: `delta = shopper_measurement - garment_measurement`
2. Map delta against tolerance bands (configurable per garment fit type):
   - Too Tight: delta < -tight_threshold
   - Slightly Tight: -tight_threshold ≤ delta < -comfort_threshold
   - Good Fit: -comfort_threshold ≤ delta ≤ +comfort_threshold
   - Slightly Loose: +comfort_threshold < delta ≤ +loose_threshold
   - Too Loose: delta > +loose_threshold
3. Overall recommendation = worst-scoring area (conservative approach)
4. Confidence = minimum of (image extraction confidence, measurement coverage percentage)
5. Tolerance bands stored per garment category in Cosmos DB (configurable by tenant)

---

## R6: Observability Stack

**Decision**: OpenTelemetry SDK → Azure Monitor (Application Insights) + Azure Monitor Alerts

**Rationale**: OpenTelemetry is the CNCF standard for distributed tracing and metrics. Azure Monitor natively ingests OTLP data and provides dashboards, alerting, and log analytics. .NET 8 has built-in OpenTelemetry support via `Microsoft.Extensions.Diagnostics`.

**Alternatives considered**:
- **Datadog/New Relic**: More feature-rich APM but adds cost and external dependency. Microsoft stack preference makes Azure Monitor the natural choice. Rejected.
- **ELK Stack (self-hosted)**: Maximum control but high operational burden. Rejected per constitution (X. IaC — prefer managed services).
- **Prometheus + Grafana**: Excellent for Kubernetes but Azure Monitor integrates more tightly with ACA. Rejected for v1.

**Implementation approach**:
1. OpenTelemetry SDK configured in Program.cs (traces, metrics, logs)
2. Correlation ID propagated via `Activity` (W3C trace context)
3. Custom metrics: `fitassess.assessment.duration`, `fitassess.assessment.confidence`, `fitassess.image.rejection_rate`
4. Azure Monitor alerts on: p95 > 5s, error rate > 0.1%, model confidence drift
5. Runbooks linked to each alert in Azure Monitor action groups

---

## R7: Deployment & Infrastructure

**Decision**: Azure Container Apps with Bicep IaC, deployed via GitHub Actions

**Rationale**: Azure Container Apps provides serverless container hosting with built-in auto-scaling, ingress, and Dapr integration — without the complexity of full AKS. Bicep is the native Azure IaC language with first-class tooling in VS Code. GitHub Actions provides CI/CD with native Azure integration.

**Alternatives considered**:
- **Azure Kubernetes Service (AKS)**: More control but over-engineered for a single service with < 10 containers. Rejected for v1 — can migrate if scale demands it.
- **Azure App Service**: Simpler but less container-native and limited auto-scaling. Rejected.
- **Terraform**: Well-known IaC but Bicep has better Azure-native type safety and no state file management. Rejected per Microsoft stack preference.

**Implementation approach**:
1. Bicep modules: Container App Environment, Container App, Cosmos DB account, Storage account, Key Vault, Entra ID app registrations, API Management
2. Three environments: dev (Basic tier), staging (mirrors prod), prod (Standard tier with multi-zone)
3. GitHub Actions workflow: build → test → scan → deploy-staging → smoke-test → deploy-prod
4. Auto-scaling: 2 min replicas, 10 max, scaling on HTTP concurrent requests (threshold: 50)

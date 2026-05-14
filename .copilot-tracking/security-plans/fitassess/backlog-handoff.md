# Security Backlog Handoff: FitAssess AI

**Project**: fitassess
**Date**: 2026-05-14
**Format**: GitHub Issues
**Autonomy Tier**: Partial (review before creation)
**Source**: Security plan Phases 1–4

---

## P1 — Critical (Pre-Production Blockers)

### {{SEC-TEMP-1}}: [Security] identity/auth: Implement BIPA consent verification in API request flow

```yaml
---
threat_id: T-AUTH-006
stride_category: Spoofing
risk_level: Critical
bucket: identity/auth
standards: [OWASP A01:2025, NIST AC-3, BIPA §15(b)]
---
```

## Security Control: BIPA Consent Verification

**Threat:** T-AUTH-006 — No BIPA consent verification — photos processed without confirmed consent. Illinois BIPA §15(b) requires informed written consent before collecting biometric data. Statutory damages: $1,000–$5,000 per violation.
**Bucket:** identity/auth
**Standards:** OWASP A01:2025, NIST AC-3, BIPA §15(b)
**Risk Level:** Critical

### Implementation

- Add a required `X-Consent-Token` header or `consentToken` field to `POST /assessments` and `POST /assessments/by-profile` endpoints.
- Validate consent token against tenant's consent management system before proceeding with photo processing.
- Reject requests without valid consent proof with HTTP 403 and descriptive error code (`CONSENT_REQUIRED`).
- Log consent evidence (token, timestamp, shopper reference, tenant ID) in immutable audit trail.
- Update OpenAPI contract to document the consent requirement.

### Acceptance Criteria

- [ ] Assessment endpoints reject requests without consent proof (HTTP 403)
- [ ] Consent token validation occurs before any photo processing or AI service call
- [ ] Consent evidence logged immutably with correlation to assessment ID
- [ ] OpenAPI spec updated with consent parameter documentation
- [ ] Integration tests verify consent enforcement for all assessment paths

**Labels:** `security`, `identity/auth`, `P1-critical`, `cia:privacy`, `compliance:bipa`

---

### {{SEC-TEMP-2}}: [Security] identity/auth: Enforce tenant ID claim validation to prevent cross-tenant impersonation

```yaml
---
threat_id: T-AUTH-001
stride_category: Spoofing
risk_level: Critical
bucket: identity/auth
standards: [OWASP A01:2025, NIST AC-3, SE:05]
---
```

## Security Control: Tenant ID Claim Validation

**Threat:** T-AUTH-001 — Tenant impersonation via `tid` claim bypass — valid Entra token from one registered tenant used to access another tenant's data.
**Bucket:** identity/auth
**Standards:** OWASP A01:2025, NIST AC-3, WAF SE:05
**Risk Level:** Critical

### Implementation

- Extract `tid` (tenant ID) claim from JWT on every request in authentication middleware.
- Validate extracted `tid` against registered tenants in Cosmos DB `tenants` container.
- Reject tokens from unregistered tenants with HTTP 401.
- Ensure all data access paths use the validated tenant ID from the token — never from request body or query parameters.
- Add integration tests that verify cross-tenant isolation (Tenant A's token cannot access Tenant B's data).

### Acceptance Criteria

- [ ] JWT middleware extracts and validates `tid` claim on every request
- [ ] Tokens from unregistered tenants return HTTP 401
- [ ] Tenant ID for data scoping derived exclusively from JWT claim, not request input
- [ ] Integration tests verify cross-tenant isolation for all endpoints
- [ ] Suspended tenants (status ≠ Active) return HTTP 403

**Labels:** `security`, `identity/auth`, `P1-critical`, `cia:confidentiality`, `cia:integrity`

---

### {{SEC-TEMP-3}}: [Security] web: Harden file upload against malicious payloads (zip bombs, polyglot files)

```yaml
---
threat_id: T-WEB-002
stride_category: Tampering
risk_level: Critical
bucket: web/UI/reporting
standards: [OWASP A03:2025, NIST SI-10, SE:08]
---
```

## Security Control: Malicious Upload Defense

**Threat:** T-WEB-002 — Malicious file upload disguised as image (zip bomb, polyglot file, executable) bypassing image validation.
**Bucket:** web/UI/reporting
**Standards:** OWASP A03:2025, NIST SI-10, WAF SE:08
**Risk Level:** Critical

### Implementation

- Validate file magic bytes (first 8 bytes) against allowed image formats (JPEG: `FF D8 FF`, PNG: `89 50 4E 47`).
- Enforce Content-Type matches magic bytes — reject mismatches.
- Enforce file size limit (10 MB) at middleware level before full body parsing.
- Re-encode uploaded image through `System.Drawing` or `ImageSharp` to strip embedded payloads.
- Reject files with EXIF data containing script tags or excessively large metadata sections.
- Return HTTP 422 with error code `INVALID_IMAGE_FORMAT` for rejected uploads.

### Acceptance Criteria

- [ ] Magic byte validation rejects non-image files regardless of extension or Content-Type
- [ ] File size limit enforced before multipart parsing begins
- [ ] Image re-encoding strips embedded payloads and normalizes format
- [ ] EXIF metadata sanitized or stripped before AI processing
- [ ] Unit tests cover: valid JPEG, valid PNG, zip bomb, polyglot, oversized file, wrong extension

**Labels:** `security`, `web/UI/reporting`, `P1-critical`, `cia:integrity`, `cia:availability`

---

### {{SEC-TEMP-4}}: [Security] ai-ml: Defend against prompt injection via photo metadata in AI measurement extraction

```yaml
---
threat_id: T-AIML-003
stride_category: Elevation of Privilege
risk_level: Critical
bucket: ai-ml
standards: [OWASP LLM01, SE:08, MCSB AI-5]
---
```

## Security Control: Prompt Injection Defense

**Threat:** T-AIML-003 — Prompt injection via embedded text in photo EXIF/metadata bypasses Content Safety and manipulates AI measurement output.
**Bucket:** ai-ml
**Standards:** OWASP LLM01, WAF SE:08, MCSB AI-5
**Risk Level:** Critical

### Implementation

- Strip ALL EXIF/metadata from uploaded photos before passing to any AI service.
- Apply Content Safety filter BEFORE measurement extraction pipeline.
- Validate AI output against strict JSON schema for measurement values.
- Enforce physiologically valid ranges for all measurements (e.g., shoulder width 25–65 cm, chest 50–180 cm, waist 40–200 cm, inseam 50–110 cm).
- Alert on measurements outside ±3 standard deviations from historical per-garment-category averages.
- Log all rejected/anomalous measurements for security review.

### Acceptance Criteria

- [ ] All EXIF/metadata stripped from photos before AI processing
- [ ] Content Safety runs before landmark extraction (enforced in pipeline order)
- [ ] AI output validated against JSON schema with typed measurement fields
- [ ] Measurements outside physiological range rejected with error code
- [ ] Anomaly detection alerts on statistical outliers
- [ ] Red-team test: submit photo with embedded adversarial text, verify no measurement manipulation

**Labels:** `security`, `ai-ml`, `P1-critical`, `cia:integrity`, `cia:confidentiality`
**RAI Principle:** reliability and safety
**RAI Priority:** Critical

---

### {{SEC-TEMP-5}}: [Security] infra: Deploy WAF and DDoS Standard protection for public-facing ingress

```yaml
---
threat_id: T-INFRA-002
stride_category: Denial of Service
risk_level: Critical
bucket: infra
standards: [OWASP A05:2025, CIS §6, SE:06]
---
```

## Security Control: DDoS and WAF Protection

**Threat:** T-INFRA-002 — DDoS attack on public ACA ingress with no WAF or DDoS Standard protection.
**Bucket:** infra
**Standards:** OWASP A05:2025, CIS §6, WAF SE:06
**Risk Level:** Critical

### Implementation

- Deploy Azure Application Gateway with WAF v2 policy in front of Container Apps, OR use Azure Front Door with WAF.
- Enable Azure DDoS Protection Standard on the VNet.
- Configure WAF rules: OWASP Core Rule Set 3.2+, bot protection, rate limiting.
- Configure custom WAF rules for photo upload endpoint (max body size, content type restriction).
- Add Bicep modules for WAF and DDoS resources.

### Acceptance Criteria

- [ ] WAF v2 or Front Door WAF deployed in front of Container Apps
- [ ] DDoS Standard enabled on VNet
- [ ] OWASP Core Rule Set active with no false-positive exclusions that weaken security
- [ ] Custom rules for upload endpoint enforce size and content-type limits
- [ ] Infrastructure defined in Bicep (IaC)
- [ ] Load test validates WAF does not degrade p95 latency beyond acceptable threshold

**Labels:** `security`, `infra`, `P1-critical`, `cia:availability`

---

### {{SEC-TEMP-6}}: [Security] data: Publish BIPA §15(a) written biometric data retention and destruction policy

```yaml
---
threat_id: N/A (compliance gap)
stride_category: N/A
risk_level: Critical
bucket: data
standards: [BIPA §15(a), CCPA, SE:03]
---
```

## Security Control: BIPA Written Policy

**Threat:** Compliance gap — Illinois BIPA §15(a) requires a publicly available written policy for retention and destruction of biometric data BEFORE collecting any biometric identifiers.
**Bucket:** data
**Standards:** BIPA §15(a), CCPA/CPRA, WAF SE:03
**Risk Level:** Critical (legal blocker)

### Implementation

- Draft written biometric data policy covering: types of biometric data collected (body photos for measurement extraction), purpose, retention schedule (photos: 60 seconds, derived measurements: per tenant agreement), destruction method (automated lifecycle deletion with audit), and guidelines for permanent destruction.
- Publish policy at a tenant-accessible URL.
- Include policy reference in API documentation and tenant onboarding materials.
- Legal review required before publication.

### Acceptance Criteria

- [ ] Written policy published covering all BIPA §15(a) requirements
- [ ] Policy documents 60-second photo retention and automated destruction
- [ ] Policy reviewed and approved by legal counsel
- [ ] Policy URL accessible to all tenant partners
- [ ] Tenant onboarding documentation references the policy

**Labels:** `security`, `data`, `P1-critical`, `cia:privacy`, `compliance:bipa`

---

### {{SEC-TEMP-7}}: [Security] infra: Deploy Container Apps in private VNet with private endpoints for all Azure services

```yaml
---
threat_id: T-INFRA-002, T-INFRA-005
stride_category: Information Disclosure, Denial of Service
risk_level: Critical
bucket: infra
standards: [SE:06, CIS §6, NIST SC-7]
---
```

## Security Control: Private Network Deployment

**Threat:** Multiple — public network exposure of ACA and Azure services creates attack surface for DDoS, data exfiltration, and unauthorized access.
**Bucket:** infra
**Standards:** WAF SE:06, CIS §6, NIST SC-7
**Risk Level:** Critical

### Implementation

- Deploy Container Apps environment with internal-only ingress (no public IP).
- Enable private endpoints for: Cosmos DB, Blob Storage, Key Vault, AI Vision, ML endpoint, Service Bus.
- Disable public network access on all Azure services.
- Configure Azure Firewall or NAT Gateway for controlled egress with FQDN allow-list.
- Update Bicep modules for private endpoint resources, DNS zones, and network rules.

### Acceptance Criteria

- [ ] Container Apps environment has internal ingress only
- [ ] Private endpoints enabled for all 6 Azure services
- [ ] Public network access disabled on each service (verified via Azure Policy)
- [ ] Egress filtered through Azure Firewall with FQDN allow-list
- [ ] All Bicep modules updated and tested
- [ ] Connectivity verified end-to-end in staging environment

**Labels:** `security`, `infra`, `P1-critical`, `cia:confidentiality`, `cia:availability`

---

## P2 — High

### {{SEC-TEMP-8}}: [Security] data: Prevent cross-tenant data leakage with defense-in-depth isolation

```yaml
---
threat_id: T-DATA-001
stride_category: Information Disclosure
risk_level: High
bucket: data
standards: [OWASP A01:2025, NIST AC-3, SE:04]
---
```

## Security Control: Cross-Tenant Isolation

**Threat:** T-DATA-001 — Application-layer bug bypassing partition key scoping could expose another tenant's data.
**Bucket:** data
**Standards:** OWASP A01:2025, NIST AC-3, WAF SE:04
**Risk Level:** High

### Implementation

- Repository base class enforces `tenantId` filter on every query — no override possible.
- Add Cosmos DB stored procedure or server-side validation that rejects queries without partition key.
- Integration test suite: create data for Tenant A and Tenant B, verify Tenant A's token cannot read Tenant B's data across all endpoints.
- Consider Cosmos DB row-level security or RBAC scoping per tenant (v2 enhancement).

### Acceptance Criteria

- [ ] Repository base class enforces tenantId on all CRUD operations
- [ ] Integration tests verify cross-tenant isolation for every endpoint
- [ ] No Cosmos DB query can execute without partition key filter
- [ ] Code review checklist includes tenant isolation verification

**Labels:** `security`, `data`, `P2-high`, `cia:confidentiality`

---

### {{SEC-TEMP-9}}: [Security] data: Harden Blob Storage SAS token scope for transient photos

```yaml
---
threat_id: T-DATA-002
stride_category: Information Disclosure
risk_level: High
bucket: data
standards: [OWASP A02:2025, NIST SC-28, CIS §3]
---
```

## Security Control: SAS Token Hardening

**Threat:** T-DATA-002 — Overly broad SAS token scope/duration could expose photos beyond 60s lifecycle.
**Bucket:** data
**Standards:** OWASP A02:2025, NIST SC-28, CIS §3
**Risk Level:** High

### Implementation

- Generate SAS tokens scoped to: single blob, read-only permission, 90-second maximum expiry.
- Use stored access policy on blob container for centralized revocation.
- Enforce blob lifecycle hard-delete at 60 seconds.
- Log SAS generation events with blob path and expiry for audit.

### Acceptance Criteria

- [ ] SAS tokens are single-blob, read-only, ≤90s expiry
- [ ] Stored access policy enables emergency revocation
- [ ] Lifecycle policy verified to hard-delete at 60s
- [ ] SAS generation audit logged

**Labels:** `security`, `data`, `P2-high`, `cia:confidentiality`

---

### {{SEC-TEMP-10}}: [Security] data: Immutable audit trail for profile deletion (BIPA compliance)

```yaml
---
threat_id: T-DATA-004
stride_category: Repudiation
risk_level: High
bucket: data
standards: [NIST AU-3, AU-9, BIPA §15(a)]
---
```

## Security Control: Deletion Audit Trail

**Threat:** T-DATA-004 — Profile deletion without immutable audit trail — cannot prove deletion occurred for BIPA.
**Bucket:** data
**Standards:** NIST AU-3, AU-9, BIPA §15(a)
**Risk Level:** High

### Implementation

- Log all delete operations with: timestamp, entity ID, entity type, requesting identity, tenant ID, correlation ID.
- Store audit records in a separate immutable log (append-only Cosmos container or Azure Table Storage with immutable policy).
- Retain deletion audit records for 3 years (beyond BIPA statute of limitations).
- Include cascade deletion evidence (profile → assessments → blobs).

### Acceptance Criteria

- [ ] All delete operations produce immutable audit records
- [ ] Audit records include complete deletion evidence chain
- [ ] Audit retention set to 3 years minimum
- [ ] Audit records cannot be modified or deleted (immutable storage)

**Labels:** `security`, `data`, `P2-high`, `cia:integrity`, `cia:privacy`, `compliance:bipa`

---

### {{SEC-TEMP-11}}: [Security] data: Disable Cosmos DB key-based authentication — use Entra ID RBAC only

```yaml
---
threat_id: T-DATA-005
stride_category: Information Disclosure
risk_level: High
bucket: data
standards: [NIST IA-5, CIS §4, SE:05]
---
```

## Security Control: Disable Cosmos DB Key Auth

**Threat:** T-DATA-005 — Leaked Cosmos DB key credentials grant full read/write to all tenant data.
**Bucket:** data
**Standards:** NIST IA-5, CIS §4, WAF SE:05
**Risk Level:** High

### Implementation

- Set `disableLocalAuth: true` on Cosmos DB account via Bicep.
- Assign managed identity RBAC roles (`Cosmos DB Built-in Data Reader/Contributor`) scoped to specific containers.
- Update all application code to use `DefaultAzureCredential` (already planned per spec).
- Enforce via Azure Policy: deny Cosmos DB accounts with local auth enabled.

### Acceptance Criteria

- [ ] Cosmos DB local auth disabled in Bicep template
- [ ] Managed identity RBAC configured for data plane access
- [ ] Application uses `DefaultAzureCredential` for all Cosmos DB operations
- [ ] Azure Policy enforces `disableLocalAuth` across subscription

**Labels:** `security`, `data`, `P2-high`, `cia:confidentiality`

---

### {{SEC-TEMP-12}}: [Security] data: Scrub photo and measurement data from all logs and telemetry

```yaml
---
threat_id: T-DATA-007
stride_category: Information Disclosure
risk_level: High
bucket: data
standards: [NIST AU-9, OWASP A09:2025, BIPA §15(a)]
---
```

## Security Control: Telemetry Data Scrubbing

**Threat:** T-DATA-007 — Photo bytes or measurement data persists in telemetry, logs, or exception traces beyond 60s TTL.
**Bucket:** data
**Standards:** NIST AU-9, OWASP A09:2025, BIPA §15(a)
**Risk Level:** High

### Implementation

- Configure structured logging with explicit redaction of photo byte arrays and measurement values.
- Add telemetry processor to strip `body`, `imageBytes`, `measurements` fields from Application Insights.
- Ensure exception handling never logs request bodies for assessment endpoints.
- Audit Log Analytics for any retained biometric data monthly.

### Acceptance Criteria

- [ ] No photo data appears in Application Insights, Log Analytics, or console logs
- [ ] Measurement values redacted from exception telemetry
- [ ] Telemetry processor configured and tested
- [ ] Monthly audit process documented

**Labels:** `security`, `data`, `P2-high`, `cia:confidentiality`, `cia:privacy`, `compliance:bipa`

---

### {{SEC-TEMP-13}}: [Security] web: Sanitize error responses to prevent information leakage

```yaml
---
threat_id: T-WEB-003
stride_category: Information Disclosure
risk_level: High
bucket: web/UI/reporting
standards: [OWASP A05:2025, NIST SI-11, SE:08]
---
```

## Security Control: Error Response Sanitization

**Threat:** T-WEB-003 — Verbose error responses leaking stack traces, internal paths, or Cosmos DB entity IDs.
**Bucket:** web/UI/reporting
**Standards:** OWASP A05:2025, NIST SI-11, WAF SE:08
**Risk Level:** High

### Implementation

- Custom exception handling middleware returns generic error responses in production.
- Map internal exceptions to standardized error codes (e.g., `ASSESSMENT_FAILED`, `INVALID_INPUT`).
- Include only correlation ID in client-facing error response — full details in server-side logs.
- Disable developer exception page in production.

### Acceptance Criteria

- [ ] No stack traces, internal paths, or entity IDs in production error responses
- [ ] Correlation ID returned for client troubleshooting
- [ ] All error responses use standardized error code schema
- [ ] Integration test verifies no information leakage in 4xx/5xx responses

**Labels:** `security`, `web/UI/reporting`, `P2-high`, `cia:confidentiality`

---

### {{SEC-TEMP-14}}: [Security] identity/auth: Define fine-grained OAuth scopes and app roles

```yaml
---
threat_id: T-AUTH-002
stride_category: Elevation of Privilege
risk_level: High
bucket: identity/auth
standards: [OWASP A01:2025, NIST AC-6, SE:05]
---
```

## Security Control: Fine-Grained OAuth Scopes

**Threat:** T-AUTH-002 — Coarse OAuth scopes (Read/Write only) allow garment ingestion user to delete profiles.
**Bucket:** identity/auth
**Standards:** OWASP A01:2025, NIST AC-6, WAF SE:05
**Risk Level:** High

### Implementation

- Define app roles in Entra ID: `Assessment.Read`, `Assessment.Write`, `GarmentCatalog.Write`, `Profile.Read`, `Profile.Delete`, `Admin.Manage`.
- Update JWT middleware to check role claims per endpoint.
- Update per-tenant service principal assignments with scoped roles.
- Document role assignments in tenant onboarding process.

### Acceptance Criteria

- [ ] App roles defined in Entra ID app manifest
- [ ] Each API endpoint validates required role claim
- [ ] Integration tests verify role-based access for each endpoint
- [ ] Tenant onboarding documents role assignment requirements

**Labels:** `security`, `identity/auth`, `P2-high`, `cia:integrity`

---

### {{SEC-TEMP-15}}: [Security] identity/auth: Enforce suspended tenant check on every request

```yaml
---
threat_id: T-AUTH-003
stride_category: Spoofing
risk_level: High
bucket: identity/auth
standards: [OWASP A07:2025, NIST AC-2, SE:05]
---
```

## Security Control: Tenant Status Enforcement

**Threat:** T-AUTH-003 — Suspended tenant's cached token continues to authorize requests.
**Bucket:** identity/auth
**Standards:** OWASP A07:2025, NIST AC-2, WAF SE:05
**Risk Level:** High

### Implementation

- Check tenant status (Active) from Cosmos DB on every request.
- Cache tenant status with short TTL (≤5 minutes) for performance.
- Enable Continuous Access Evaluation (CAE) for near-real-time token revocation.
- Return HTTP 403 with error code `TENANT_SUSPENDED` for non-active tenants.

### Acceptance Criteria

- [ ] Tenant status checked on every request (cached ≤5 min)
- [ ] Suspended tenants receive HTTP 403 immediately
- [ ] CAE enabled on Entra ID app registration
- [ ] Integration test verifies suspended tenant rejection

**Labels:** `security`, `identity/auth`, `P2-high`, `cia:confidentiality`

---

### {{SEC-TEMP-16}}: [Security] devops: Secure CI/CD pipeline — pin actions, branch protection, IaC scanning

```yaml
---
threat_id: T-DEVOPS-001, T-DEVOPS-005
stride_category: Tampering
risk_level: High
bucket: devops/platform-ops
standards: [OWASP A08:2025, NIST SA-12, DS-6]
---
```

## Security Control: Pipeline Security Hardening

**Threat:** T-DEVOPS-001 — Pipeline poisoning via compromised GitHub Actions. T-DEVOPS-005 — IaC modified without security review.
**Bucket:** devops/platform-ops
**Standards:** OWASP A08:2025, NIST SA-12, MCSB DS-6
**Risk Level:** High

### Implementation

- Pin all GitHub Actions by commit SHA (not tag).
- Enable branch protection on `main`: require PR reviews, status checks, signed commits.
- Add IaC scanning step (Checkov or PSRule for Azure) in CI pipeline.
- Add `az deployment what-if` preview step before production deployments.
- Require manual approval gate for production deployments.

### Acceptance Criteria

- [ ] All GitHub Actions pinned by SHA
- [ ] Branch protection enforces PR reviews and status checks
- [ ] IaC scanning runs on every PR
- [ ] Production deployments require approval gate
- [ ] `what-if` preview step in deployment workflow

**Labels:** `security`, `devops/platform-ops`, `P2-high`, `cia:integrity`

---

### {{SEC-TEMP-17}}: [Security] devops: Migrate to OIDC workload identity federation — eliminate stored credentials

```yaml
---
threat_id: T-DEVOPS-002
stride_category: Elevation of Privilege
risk_level: High
bucket: devops/platform-ops
standards: [SE:09, NIST IA-5, MCSB IM-8]
---
```

## Security Control: OIDC Federation

**Threat:** T-DEVOPS-002 — Stored service principal credentials in GitHub secrets could be leaked or compromised.
**Bucket:** devops/platform-ops
**Standards:** WAF SE:09, NIST IA-5, MCSB IM-8
**Risk Level:** High

### Implementation

- Configure OIDC workload identity federation between GitHub Actions and Azure.
- Remove stored `AZURE_CLIENT_SECRET` from GitHub repository secrets.
- Use `azure/login@v2` with OIDC token exchange.
- Restrict federation to specific repository, branch, and environment.

### Acceptance Criteria

- [ ] OIDC federation configured for GitHub Actions → Azure
- [ ] No stored Azure credentials in GitHub secrets
- [ ] Federation restricted to `main` branch and production environment
- [ ] Deployment workflow updated and tested

**Labels:** `security`, `devops/platform-ops`, `P2-high`, `cia:confidentiality`

---

### {{SEC-TEMP-18}}: [Security] build: Pin NuGet dependencies and integrate vulnerability scanning

```yaml
---
threat_id: T-BUILD-001
stride_category: Tampering
risk_level: High
bucket: build
standards: [OWASP A06:2025, NIST SA-12, DS-2]
---
```

## Security Control: Dependency Security

**Threat:** T-BUILD-001 — Dependency substitution via malicious NuGet packages typosquatting Azure SDK packages.
**Bucket:** build
**Standards:** OWASP A06:2025, NIST SA-12, MCSB DS-2
**Risk Level:** High

### Implementation

- Enable NuGet lock files (`packages.lock.json`) in all projects.
- Pin exact package versions (no floating ranges).
- Add `dotnet nuget audit` to CI pipeline — fail build on known vulnerabilities.
- Enable GitHub Dependabot for NuGet dependency updates.
- Configure private NuGet feed or Azure Artifacts as primary package source.

### Acceptance Criteria

- [ ] Lock files present and committed for all projects
- [ ] No floating version ranges in `.csproj` files
- [ ] `dotnet nuget audit` runs in CI and fails on vulnerabilities
- [ ] Dependabot configured for NuGet
- [ ] SBOM generated in CI pipeline

**Labels:** `security`, `build`, `P2-high`, `cia:integrity`

---

### {{SEC-TEMP-19}}: [Security] build: Scan container images for secrets in layers

```yaml
---
threat_id: T-BUILD-003
stride_category: Information Disclosure
risk_level: High
bucket: build
standards: [NIST SI-12, SE:09]
---
```

## Security Control: Container Image Secrets Scanning

**Threat:** T-BUILD-003 — Secrets baked into container image layers.
**Bucket:** build
**Standards:** NIST SI-12, WAF SE:09
**Risk Level:** High

### Implementation

- Enforce multi-stage Dockerfile (build stage separate from runtime stage).
- Run Trivy or Grype container scan in CI pipeline.
- Scan for secrets in image layers using tools like `ggshield` or `trufflehog`.
- Use non-root user in runtime image.
- Base on `mcr.microsoft.com/dotnet/aspnet:8.0-alpine` or chiselled variant.

### Acceptance Criteria

- [ ] Multi-stage Dockerfile with no secrets in runtime layer
- [ ] Container image scanning in CI (Trivy/Grype)
- [ ] Secret scanning on image layers
- [ ] Non-root user configured
- [ ] Minimal base image used

**Labels:** `security`, `build`, `P2-high`, `cia:confidentiality`

---

### {{SEC-TEMP-20}}: [Security] messaging: Disable SAS auth on Service Bus — use managed identity

```yaml
---
threat_id: T-MSG-001
stride_category: Spoofing
risk_level: High
bucket: messaging
standards: [OWASP A01:2025, NIST AC-3, SE:05]
---
```

## Security Control: Service Bus Managed Identity

**Threat:** T-MSG-001 — Unauthorized message injection via compromised SAS token.
**Bucket:** messaging
**Standards:** OWASP A01:2025, NIST AC-3, WAF SE:05
**Risk Level:** High

### Implementation

- Disable SAS key authentication on Service Bus namespace.
- Assign managed identity roles: `Azure Service Bus Data Sender` for API, `Azure Service Bus Data Receiver` for worker.
- Configure in Bicep: `disableLocalAuth: true`.
- Use private endpoint for Service Bus.

### Acceptance Criteria

- [ ] SAS auth disabled on Service Bus namespace
- [ ] Managed identity roles assigned with least privilege
- [ ] Application uses `DefaultAzureCredential` for Service Bus access
- [ ] Private endpoint enabled

**Labels:** `security`, `messaging`, `P2-high`, `cia:integrity`

---

### {{SEC-TEMP-21}}: [Security] web: Implement upload rate limiting and request size enforcement

```yaml
---
threat_id: T-WEB-004
stride_category: Denial of Service
risk_level: High
bucket: web/UI/reporting
standards: [NIST SC-5, SE:06]
---
```

## Security Control: Upload Rate Limiting

**Threat:** T-WEB-004 — Photo upload endpoint abused for resource exhaustion.
**Bucket:** web/UI/reporting
**Standards:** NIST SC-5, WAF SE:06
**Risk Level:** High

### Implementation

- ASP.NET Core request body size middleware enforces 10 MB limit before parsing.
- Rate limiting per tenant (based on `RateLimitTier`: Standard 100/min, Premium 500/min, Enterprise 2000/min per spec).
- Rate limiting per IP as fallback.
- Return HTTP 429 with `Retry-After` header.

### Acceptance Criteria

- [ ] Request body size enforced at middleware level (before full body read)
- [ ] Per-tenant rate limiting based on tier
- [ ] HTTP 429 with Retry-After for exceeded limits
- [ ] Load test validates rate limiting under stress

**Labels:** `security`, `web/UI/reporting`, `P2-high`, `cia:availability`

---

### {{SEC-TEMP-22}}: [Security] web: Validate batch garment import against injection and schema attacks

```yaml
---
threat_id: T-WEB-007
stride_category: Tampering
risk_level: High
bucket: web/UI/reporting
standards: [OWASP A03:2025, NIST SI-10]
---
```

## Security Control: Batch Input Validation

**Threat:** T-WEB-007 — Request body injection via batch garment import (malicious JSON in bulk upload).
**Bucket:** web/UI/reporting
**Standards:** OWASP A03:2025, NIST SI-10
**Risk Level:** High

### Implementation

- Validate batch payload against OpenAPI schema.
- Enforce max batch size (100 items per spec).
- Parameterize all Cosmos DB queries (no string interpolation).
- Sanitize garment names and descriptions for injection characters.

### Acceptance Criteria

- [ ] Schema validation rejects malformed batch payloads
- [ ] Max batch size enforced (100)
- [ ] All Cosmos queries parameterized
- [ ] Injection test suite covers SQL, NoSQL, and XSS vectors

**Labels:** `security`, `web/UI/reporting`, `P2-high`, `cia:integrity`

---

### {{SEC-TEMP-23}}: [Security] web: JWT token replay protection

```yaml
---
threat_id: T-WEB-001
stride_category: Spoofing
risk_level: High
bucket: web/UI/reporting
standards: [OWASP A07:2025, NIST IA-5, SE:05]
---
```

## Security Control: Token Replay Protection

**Threat:** T-WEB-001 — JWT token replay or stolen token used from different client.
**Bucket:** web/UI/reporting
**Standards:** OWASP A07:2025, NIST IA-5, WAF SE:05
**Risk Level:** High

### Implementation

- Configure short token lifetime (≤1 hour) in Entra ID.
- Enable Continuous Access Evaluation (CAE).
- Validate `iss`, `aud`, `exp`, and `nbf` claims strictly.
- Log all authentication events with client IP for anomaly detection.

### Acceptance Criteria

- [ ] Token lifetime ≤1 hour configured
- [ ] CAE enabled
- [ ] All required JWT claims validated
- [ ] Auth event logging includes client IP

**Labels:** `security`, `web/UI/reporting`, `P2-high`, `cia:confidentiality`

---

### {{SEC-TEMP-24}}: [Security] infra: IaC drift detection and immutable deployments

```yaml
---
threat_id: T-INFRA-001
stride_category: Tampering
risk_level: High
bucket: infra
standards: [NIST CM-3, SE:08]
---
```

## Security Control: IaC Drift Detection

**Threat:** T-INFRA-001 — Config drift via manual Azure portal changes bypassing IaC.
**Bucket:** infra
**Standards:** NIST CM-3, WAF SE:08
**Risk Level:** High

### Implementation

- Azure Policy: deny manual modifications to production resources (deny portal edits).
- Scheduled `az deployment what-if` drift detection.
- Resource locks on critical resources (Cosmos DB, Key Vault).
- Alert on Azure Activity Log resource modification events not triggered by CI/CD service principal.

### Acceptance Criteria

- [ ] Azure Policy denies manual production changes
- [ ] Drift detection scheduled (daily or weekly)
- [ ] Resource locks on critical resources
- [ ] Alerts on non-CI/CD modifications

**Labels:** `security`, `infra`, `P2-high`, `cia:integrity`

---

### {{SEC-TEMP-25}}: [Security] infra: Egress lockdown via Azure Firewall

```yaml
---
threat_id: T-INFRA-005
stride_category: Tampering
risk_level: High
bucket: infra
standards: [NIST SC-7, SE:06]
---
```

## Security Control: Egress Filtering

**Threat:** T-INFRA-005 — Unfiltered egress enables data exfiltration to unauthorized endpoints.
**Bucket:** infra
**Standards:** NIST SC-7, WAF SE:06
**Risk Level:** High

### Implementation

- Deploy Azure Firewall with FQDN allow-list.
- Allow only: `*.cosmos.azure.com`, `*.blob.core.windows.net`, `*.cognitiveservices.azure.com`, `*.servicebus.windows.net`, `*.vault.azure.net`, `login.microsoftonline.com`.
- Deny all other outbound by default.
- Log all egress traffic for audit.

### Acceptance Criteria

- [ ] Azure Firewall deployed with UDR from Container Apps subnet
- [ ] FQDN allow-list covers only required Azure services
- [ ] Default deny for all other outbound traffic
- [ ] Egress logging enabled

**Labels:** `security`, `infra`, `P2-high`, `cia:confidentiality`

---

### {{SEC-TEMP-26}}: [Security] data: Protect garment catalog write authorization

```yaml
---
threat_id: T-DATA-003
stride_category: Tampering
risk_level: High
bucket: data
standards: [OWASP A01:2025, NIST AC-6, AU-3]
---
```

## Security Control: Garment Write Authorization

**Threat:** T-DATA-003 — Unauthorized garment catalog writes alter measurements → incorrect fit assessments for all shoppers.
**Bucket:** data
**Standards:** OWASP A01:2025, NIST AC-6, AU-3
**Risk Level:** High

### Implementation

- Require `GarmentCatalog.Write` role for garment creation/update endpoints.
- Audit log all garment writes with before/after values.
- Cosmos DB change feed monitoring for anomalous garment measurement changes.

### Acceptance Criteria

- [ ] Garment write endpoints require `GarmentCatalog.Write` role
- [ ] All garment writes audit logged
- [ ] Change feed monitoring for anomalous updates

**Labels:** `security`, `data`, `P2-high`, `cia:integrity`

---

### {{SEC-TEMP-27}}: [Security] ai-ml: Validate AI measurement output against physiological ranges

```yaml
---
threat_id: T-AIML-001
stride_category: Tampering
risk_level: High
bucket: ai-ml
standards: [OWASP LLM01, NIST SI-10, MCSB AI-5]
---
```

## Security Control: AI Output Validation

**Threat:** T-AIML-001 — Adversarial image produces incorrect body landmarks (targeted misclassification).
**Bucket:** ai-ml
**Standards:** OWASP LLM01, NIST SI-10, MCSB AI-5
**Risk Level:** High

### Implementation

- Validate all measurement outputs against physiologically valid ranges before persisting.
- Reject assessments where any measurement falls outside valid bounds.
- Alert on confidence scores near threshold (70–75% zone).
- Log all rejected assessments for security review.

### Acceptance Criteria

- [ ] Measurement range validation for all body dimensions
- [ ] Assessments rejected when outside valid ranges
- [ ] Near-threshold confidence alerts configured
- [ ] Rejected assessment logging operational

**Labels:** `security`, `ai-ml`, `P2-high`, `cia:integrity`
**RAI Principle:** reliability and safety

---

### {{SEC-TEMP-28}}: [Security] ai-ml: Verify Azure AI DPA covers biometric data under BIPA

```yaml
---
threat_id: T-AIML-004
stride_category: Information Disclosure
risk_level: High
bucket: ai-ml
standards: [OWASP LLM06, BIPA §15(d), MCSB AI-2]
---
```

## Security Control: AI Service DPA Verification

**Threat:** T-AIML-004 — AI service retains/logs biometric photo data beyond processing, violating BIPA.
**Bucket:** ai-ml
**Standards:** OWASP LLM06, BIPA §15(d), MCSB AI-2
**Risk Level:** High

### Implementation

- Review Azure AI Vision and Azure OpenAI Data Processing Addendum (DPA) for biometric data classification.
- Confirm opt-out of Abuse Monitoring human review for the deployment.
- Verify no training data retention for customer images.
- Document DPA compliance evidence for SOC 2 audit.
- Requires legal review.

### Acceptance Criteria

- [ ] DPA reviewed and confirmed to cover biometric data
- [ ] Abuse Monitoring human review opt-out enabled
- [ ] No customer data retained for training (verified in writing)
- [ ] Compliance evidence documented

**Labels:** `security`, `ai-ml`, `P2-high`, `cia:privacy`, `compliance:bipa`
**RAI Principle:** privacy and security

---

### {{SEC-TEMP-29}}: [Security] ai-ml: Defense-in-depth for minor detection bypass

```yaml
---
threat_id: T-AIML-AI-003
stride_category: Elevation of Privilege
risk_level: High
bucket: ai-ml
standards: [SE:08, BIPA, MCSB AI-5]
---
```

## Security Control: Minor Detection Defense-in-Depth

**Threat:** T-AIML-AI-003 — Adversarial image evades Content Safety minor detection, allowing processing of a minor's photo.
**Bucket:** ai-ml
**Standards:** WAF SE:08, BIPA, MCSB AI-5
**Risk Level:** High

### Implementation

- Content Safety minor detection as first pipeline stage (Tier 1 per spec).
- Add secondary age estimation check as defense-in-depth.
- Reject ambiguous cases (low confidence on age).
- Human review escalation path for flagged but uncertain cases.
- Log all minor detection events for compliance audit.

### Acceptance Criteria

- [ ] Content Safety runs before any measurement extraction
- [ ] Secondary age estimation check implemented
- [ ] Ambiguous cases rejected (not processed)
- [ ] All detection events logged for audit

**Labels:** `security`, `ai-ml`, `P2-high`, `cia:privacy`, `compliance:bipa`
**RAI Principle:** fairness, reliability and safety

---

## P3 — Medium

### {{SEC-TEMP-30}}: [Security] web: Implement security headers middleware (HSTS, CSP, X-Content-Type-Options)

```yaml
---
threat_id: N/A (standards gap)
stride_category: N/A
risk_level: Medium
bucket: web/UI/reporting
standards: [SE:01, OWASP A05:2025]
---
```

## Security Control: Security Response Headers

**Threat:** Standards gap — missing security headers increase attack surface.
**Bucket:** web/UI/reporting
**Risk Level:** Medium

### Implementation

Add ASP.NET Core middleware for: `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Content-Security-Policy: default-src 'none'`, `Referrer-Policy: strict-origin-when-cross-origin`.

### Acceptance Criteria

- [ ] All 5 security headers present in every response
- [ ] Headers verified via automated test

**Labels:** `security`, `web/UI/reporting`, `P3-medium`

---

### {{SEC-TEMP-31}}: [Security] web: Restrict or disable Swagger endpoint in production

```yaml
---
threat_id: T-WEB-005
stride_category: Information Disclosure
risk_level: Medium
bucket: web/UI/reporting
standards: [OWASP A05:2025, SE:08]
---
```

### Acceptance Criteria

- [ ] Swagger disabled in production or restricted to authenticated internal users

**Labels:** `security`, `web/UI/reporting`, `P3-medium`, `cia:confidentiality`

---

### {{SEC-TEMP-32}}: [Security] web: Configure explicit CORS allow-list

```yaml
---
threat_id: T-WEB-006
stride_category: Elevation of Privilege
risk_level: Medium
bucket: web/UI/reporting
standards: [OWASP A05:2025, NIST AC-4, SE:08]
---
```

### Acceptance Criteria

- [ ] CORS restricted to tenant-registered origins only
- [ ] Wildcard `*` origin denied

**Labels:** `security`, `web/UI/reporting`, `P3-medium`, `cia:integrity`

---

### {{SEC-TEMP-33}}: [Security] identity/auth: Enable authentication event audit logging for SOC 2

```yaml
---
threat_id: T-AUTH-004
stride_category: Repudiation
risk_level: Medium
bucket: identity/auth
standards: [NIST AU-2, SE:10, CIS §1]
---
```

### Acceptance Criteria

- [ ] Entra ID audit and sign-in logs sent to Log Analytics
- [ ] SOC 2 CC7 evidence collection process documented

**Labels:** `security`, `identity/auth`, `P3-medium`, `cia:integrity`

---

### {{SEC-TEMP-34}}: [Security] messaging: Dead-letter queue monitoring and alerting

```yaml
---
threat_id: T-MSG-003
stride_category: Repudiation
risk_level: Medium
bucket: messaging
standards: [NIST AU-3, SE:10]
---
```

### Acceptance Criteria

- [ ] Dead-letter queue monitoring configured
- [ ] Alert on DLQ depth > threshold
- [ ] All message processing events logged with correlation ID

**Labels:** `security`, `messaging`, `P3-medium`, `cia:integrity`

---

### {{SEC-TEMP-35}}: [Security] messaging: Application-level message payload encryption

```yaml
---
threat_id: T-MSG-004
stride_category: Information Disclosure
risk_level: Medium
bucket: messaging
standards: [OWASP A02:2025, NIST SC-28, SE:07]
---
```

### Acceptance Criteria

- [ ] Message bodies encrypted at application level before enqueue
- [ ] RBAC restricted to Data Sender/Receiver roles only

**Labels:** `security`, `messaging`, `P3-medium`, `cia:confidentiality`

---

### {{SEC-TEMP-36}}: [Security] messaging: Queue flooding defense with circuit breaker

```yaml
---
threat_id: T-MSG-005
stride_category: Denial of Service
risk_level: Medium
bucket: messaging
standards: [SE:06, NIST SC-5]
---
```

### Acceptance Criteria

- [ ] Queue depth monitoring with auto-scaling consumers
- [ ] Circuit breaker when queue exceeds threshold

**Labels:** `security`, `messaging`, `P3-medium`, `cia:availability`

---

### {{SEC-TEMP-37}}: [Security] infra: Log Analytics PII masking and RBAC restriction

```yaml
---
threat_id: T-INFRA-004
stride_category: Information Disclosure
risk_level: Medium
bucket: infra
standards: [NIST AU-9, OWASP A02:2025, SE:10]
---
```

### Acceptance Criteria

- [ ] PII obfuscated in telemetry
- [ ] Log Analytics RBAC restricted to security/ops team

**Labels:** `security`, `infra`, `P3-medium`, `cia:confidentiality`

---

### {{SEC-TEMP-38}}: [Security] devops: Pipeline secret scanning for leaked credentials

```yaml
---
threat_id: T-DEVOPS-004
stride_category: Information Disclosure
risk_level: Medium
bucket: devops/platform-ops
standards: [NIST SI-12, SE:09]
---
```

### Acceptance Criteria

- [ ] Secret scanning enabled in GitHub repository settings
- [ ] CI pipeline masks sensitive output

**Labels:** `security`, `devops/platform-ops`, `P3-medium`, `cia:confidentiality`

---

### {{SEC-TEMP-39}}: [Security] build: SBOM generation and reproducible builds

```yaml
---
threat_id: T-BUILD-004
stride_category: Tampering
risk_level: Medium
bucket: build
standards: [OWASP A08:2025, NIST SA-10]
---
```

### Acceptance Criteria

- [ ] SBOM generated in CI pipeline (SPDX or CycloneDX format)
- [ ] Build reproducibility verified with lock files

**Labels:** `security`, `build`, `P3-medium`, `cia:integrity`

---

### {{SEC-TEMP-40}}: [Security] ai-ml: Rate limit AI endpoint to prevent model extraction

```yaml
---
threat_id: T-AIML-002
stride_category: Information Disclosure
risk_level: Medium
bucket: ai-ml
standards: [OWASP LLM10, NIST RA-5, MCSB AI-6]
---
```

### Acceptance Criteria

- [ ] Per-tenant rate limiting on AI-backed endpoints
- [ ] Query pattern monitoring for extraction attempts

**Labels:** `security`, `ai-ml`, `P3-medium`, `cia:confidentiality`
**RAI Principle:** privacy and security

---

### {{SEC-TEMP-41}}: [Security] ai-ml: AI compute DoS defense — enforce image dimension limits

```yaml
---
threat_id: T-AIML-005
stride_category: Denial of Service
risk_level: Medium
bucket: ai-ml
standards: [OWASP LLM04, NIST SC-5, MCSB AI-3]
---
```

### Acceptance Criteria

- [ ] Max image dimensions enforced (4096×4096) before AI submission
- [ ] AI service timeout configured
- [ ] Cost alerting on AI resource consumption

**Labels:** `security`, `ai-ml`, `P3-medium`, `cia:availability`

---

### {{SEC-TEMP-42}}: [Security] ai-ml: AI decision audit trail — model version and confidence per assessment

```yaml
---
threat_id: T-AIML-006
stride_category: Repudiation
risk_level: Medium
bucket: ai-ml
standards: [NIST AU-3, MCSB AI-6, SOC 2 CC7]
---
```

### Acceptance Criteria

- [ ] Model version, prompt hash, and confidence stored per assessment
- [ ] Audit records immutable once written

**Labels:** `security`, `ai-ml`, `P3-medium`, `cia:integrity`
**RAI Principle:** transparency, accountability

---

### {{SEC-TEMP-43}}: [Security] data/web: Implement DSAR endpoint for CCPA right-to-know and right-to-delete

```yaml
---
threat_id: N/A (compliance gap)
stride_category: N/A
risk_level: Medium
bucket: web/UI/reporting, data
standards: [CCPA/CPRA, SE:03]
---
```

### Acceptance Criteria

- [ ] DSAR API endpoint for data subject access requests
- [ ] Cascade deletion verified across all stores
- [ ] Response within CCPA-mandated timeframe documented

**Labels:** `security`, `web/UI/reporting`, `data`, `P3-medium`, `cia:privacy`, `compliance:ccpa`

---

### {{SEC-TEMP-44}}: [Security] all: Enable Defender for Cloud across all Azure services

```yaml
---
threat_id: N/A (standards gap)
stride_category: N/A
risk_level: Medium
bucket: infra
standards: [SE:10, CIS §2, MCSB LT-1]
---
```

### Acceptance Criteria

- [ ] Defender enabled: Containers, Storage, Cosmos DB, Key Vault, AI Services
- [ ] Diagnostic settings configured for all resources → Log Analytics
- [ ] Security contact configured

**Labels:** `security`, `infra`, `P3-medium`, `cia:confidentiality`, `cia:integrity`, `cia:availability`

---

## P4 — Low

### {{SEC-TEMP-45}}: [Security] infra: Container runtime hardening

```yaml
---
threat_id: T-INFRA-003
stride_category: Elevation of Privilege
risk_level: Low
bucket: infra
standards: [NIST SI-2, SE:08]
---
```

### Acceptance Criteria

- [ ] Minimal base image; read-only root FS; non-root user; drop all capabilities

**Labels:** `security`, `infra`, `P4-low`

---

### {{SEC-TEMP-46}}: [Security] devops: Container image signing and provenance

```yaml
---
threat_id: T-DEVOPS-003
stride_category: Spoofing
risk_level: Low
bucket: devops/platform-ops
standards: [OWASP A08:2025, NIST SI-7, DS-2]
---
```

### Acceptance Criteria

- [ ] Image signing enabled (Notary v2 or Sigstore)
- [ ] ACR quarantine pattern enabled

**Labels:** `security`, `devops/platform-ops`, `P4-low`, `cia:integrity`

---

### {{SEC-TEMP-47}}: [Security] build: Docker base image supply chain hardening

```yaml
---
threat_id: T-BUILD-002
stride_category: Tampering
risk_level: Low
bucket: build
standards: [OWASP A08:2025, NIST SI-7]
---
```

### Acceptance Criteria

- [ ] Base image pinned by digest
- [ ] Scheduled rebuild for base image updates

**Labels:** `security`, `build`, `P4-low`, `cia:integrity`

---

### {{SEC-TEMP-48}}: [Security] data: Key Vault RBAC and purge protection hardening

```yaml
---
threat_id: T-DATA-006
stride_category: Tampering
risk_level: Low
bucket: data
standards: [CIS §8, NIST AC-6, SE:09]
---
```

### Acceptance Criteria

- [ ] Key Vault uses RBAC (not access policies)
- [ ] Purge protection and soft delete enabled
- [ ] Azure Policy enforces Key Vault settings

**Labels:** `security`, `data`, `P4-low`, `cia:integrity`

---

### {{SEC-TEMP-49}}: [Security] identity/auth: Service principal credential hardening

```yaml
---
threat_id: T-AUTH-005
stride_category: Spoofing
risk_level: Low
bucket: identity/auth
standards: [NIST IA-5, SE:09, IM-6]
---
```

### Acceptance Criteria

- [ ] Certificate-based credentials (not secrets)
- [ ] Key Vault storage with rotation policy
- [ ] Anomalous SP sign-in monitoring

**Labels:** `security`, `identity/auth`, `P4-low`, `cia:confidentiality`

---

### {{SEC-TEMP-50}}: [Security] messaging: Message integrity in transit

```yaml
---
threat_id: T-MSG-002
stride_category: Tampering
risk_level: Low
bucket: messaging
standards: [NIST SC-8, SE:07]
---
```

### Acceptance Criteria

- [ ] TLS 1.2 confirmed for all Service Bus connections
- [ ] Infrastructure encryption enabled

**Labels:** `security`, `messaging`, `P4-low`, `cia:integrity`

---

### {{SEC-TEMP-51}}: [Security] ai-ml: Training data poisoning defense

```yaml
---
threat_id: T-AIML-AI-001
stride_category: Tampering
risk_level: Low
bucket: ai-ml
standards: [OWASP LLM03, NIST AI RMF MS-2.10, MCSB AI-3]
---
```

### Acceptance Criteria

- [ ] Training data provenance documented
- [ ] Bias evaluation across demographics conducted
- [ ] Dataset versioning enabled

**Labels:** `security`, `ai-ml`, `P4-low`, `cia:integrity`
**RAI Principle:** fairness

---

### {{SEC-TEMP-52}}: [Security] ai-ml: Training data memorization defense

```yaml
---
threat_id: T-AIML-AI-002
stride_category: Information Disclosure
risk_level: Low
bucket: ai-ml
standards: [OWASP LLM06, NIST AI RMF MS-2.5, MCSB AI-2]
---
```

### Acceptance Criteria

- [ ] Training data scrubbing processes documented
- [ ] Membership inference testing planned

**Labels:** `security`, `ai-ml`, `P4-low`, `cia:confidentiality`
**RAI Principle:** privacy and security

---

## Handoff Summary

| Metric | Count |
|---|---|
| **Total Issues** | 52 |
| **P1 — Critical** | 7 |
| **P2 — High** | 22 |
| **P3 — Medium** | 15 |
| **P4 — Low** | 8 |

### By Bucket

| Bucket | Count |
|---|---|
| identity/auth | 8 |
| data | 9 |
| web/UI/reporting | 9 |
| ai-ml | 10 |
| infra | 7 |
| devops/platform-ops | 5 |
| build | 4 |
| messaging | 5 |

### By STRIDE Category

| Category | Count |
|---|---|
| Spoofing | 6 |
| Tampering | 12 |
| Repudiation | 5 |
| Information Disclosure | 12 |
| Denial of Service | 5 |
| Elevation of Privilege | 5 |
| Compliance Gap | 4 |
| Standards Gap | 3 |

### Sanitization Log

- No `.copilot-tracking/` paths in work item content
- No internal file paths in work item content
- No secrets, credentials, or PII in work item content

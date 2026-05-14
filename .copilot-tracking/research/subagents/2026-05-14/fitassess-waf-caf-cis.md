# WAF / CAF / CIS Security Controls: AI Clothing Fit Assessment

**Status**: Complete
**Date**: 2026-05-14
**Scope**: Map WAF Security pillar, CAF Security controls, and CIS Azure Foundations Benchmark to 8 operational buckets for the FitAssess multi-tenant B2B API.
**Source Architecture**: docs/architecture/solution-architecture.md, specs/001-clothing-fit-assessment/spec.md

---

## Research Questions

1. Which WAF Security pillar recommendations (SE:01–SE:12) apply to each operational bucket?
2. Which CAF Secure methodology controls apply?
3. Which CIS Microsoft Azure Foundations Benchmark v6.0 controls apply?
4. What specific gaps or recommendations exist for this architecture given its data classification and compliance requirements (CCPA/CPRA, IL BIPA, SOC 2 Type II)?

---

## Framework Reference Summary

### WAF Security Pillar (SE:01–SE:12)

| ID | Title | Summary |
|----|-------|---------|
| SE:01 | Security baseline | Align to compliance requirements, industry standards, platform recommendations |
| SE:02 | Secure development lifecycle | SDL throughout SDLC; security-first mindset |
| SE:03 | Data classification | Classify and label all workload data; influence design from classification |
| SE:04 | Segmentation | Intentional segmentation in architecture; networks, roles, identities, resources |
| SE:05 | Identity and access management | Strict, conditional, auditable IAM; least privilege; modern auth standards |
| SE:06 | Network controls | Isolate, filter, control traffic; defense-in-depth at all boundaries |
| SE:07 | Encryption | Encrypt data at rest and in transit; align scope with data classification |
| SE:08 | Hardening | Reduce attack surface; tighten configurations |
| SE:09 | Application secrets | Harden secret storage; restrict access; audit; automate rotation |
| SE:10 | Monitoring and threat detection | Holistic monitoring; modern threat detection; integration with SecOps |
| SE:11 | Security testing | Comprehensive testing; prevent issues, validate prevention, test detection |
| SE:12 | Incident response | Effective IR procedures; clear ownership; spectrum of incident types |

### CAF Secure Methodology Domains

- Security posture modernization (Zero Trust alignment)
- Incident preparedness and response
- Confidentiality (encryption, classification, data protection)
- Integrity (hashing, signing, immutable storage, supply chain)
- Availability (redundancy, fault isolation, DR)
- Security posture sustainment (Defender for Cloud secure score, drift detection)
- Governance enforcement (Azure Policy, RBAC, tagging, IaC)

### CIS Microsoft Azure Foundations Benchmark v6.0 Sections

| Section | Domain |
|---------|--------|
| 1 | Identity and Access Management |
| 2 | Microsoft Defender for Cloud |
| 3 | Storage Accounts |
| 4 | Database Services |
| 5 | Logging and Monitoring |
| 6 | Networking |
| 7 | Virtual Machines (limited applicability — Container Apps) |
| 8 | Key Vault |
| 9 | App Service (limited applicability — Container Apps) |
| 10 | Miscellaneous |

### MCSB v3 Security Domains (Mapped to CIS)

| Domain | ID Prefix | Description |
|--------|-----------|-------------|
| Network Security | NS-1 through NS-10 | Network segmentation, NSGs, firewalls, DDoS |
| Identity Management | IM-1 through IM-9 | Centralized IdP, managed identities, MFA, conditional access |
| Privileged Access | PA-1 through PA-8 | JIT, PIM, emergency accounts |
| Data Protection | DP-1 through DP-8 | Classification, encryption at rest/transit, key management |
| Asset Management | AM-1 through AM-5 | Inventory, ownership, security updates |
| Logging and Threat Detection | LT-1 through LT-7 | Diagnostic settings, SIEM integration, threat detection |
| Incident Response | IR-1 through IR-6 | IR plans, playbooks, post-incident analysis |
| Posture and Vulnerability Management | PV-1 through PV-6 | Vulnerability scanning, remediation, secure config |
| Endpoint Security | ES-1 through ES-3 | EDR, anti-malware |
| Backup and Recovery | BR-1 through BR-4 | Backup, validation, protection |
| DevOps Security | DS-1 through DS-7 | Secure SDLC, CI/CD, IaC scanning |
| Governance and Strategy | GS-1 through GS-10 | Governance framework, risk management |
| Artificial Intelligence Security | AI-1 through AI-7 | AI content filtering, data governance, model security (MCSB v2 preview) |

---

## Bucket 1: Infrastructure (Azure Container Apps, VNet, Azure Monitor/Log Analytics)

### WAF Security Pillar

| WAF ID | Recommendation | Application |
|--------|---------------|-------------|
| SE:01 | Security baseline | Apply Azure Container Apps security baseline; align with MCSB; track via Defender for Cloud |
| SE:04 | Segmentation | Deploy Container Apps in a private VNet; use NSGs for east-west traffic; isolate Container Apps environment from public internet using internal ingress |
| SE:06 | Network controls | Enable private endpoints for Container Apps environment; disable public network access; use UDR for egress via Azure Firewall or NAT Gateway; enforce HTTPS |
| SE:08 | Hardening | Use lean/minimal base images (Alpine, Chiselled Ubuntu); remove unused components; enable mTLS between services; enforce `allowInsecure: false` |
| SE:10 | Monitoring | Send system/console logs to Log Analytics; configure Azure Monitor alerts for anomalous activity; use OpenTelemetry agent for distributed tracing |

### CAF Controls

- **Posture modernization**: Enable Defender for Cloud on subscription; track Container Apps security baseline compliance via regulatory compliance dashboard
- **Confidentiality**: Deploy in private VNet with no public ingress; encrypt all traffic in transit (TLS 1.2+)
- **Integrity**: Use IaC (Bicep) for immutable infra deployments; detect configuration drift via Azure Policy
- **Availability**: Enable availability zone support for Container Apps; configure health probes (liveness, readiness, startup)
- **Governance**: Enforce Azure Policy built-in definitions for Container Apps (network injection required, public access disabled, HTTPS enforced, managed identity enabled, authentication enabled)

### CIS Azure Foundations Benchmark

| CIS Section | Controls | Application |
|-------------|----------|-------------|
| 2 | Defender for Cloud | Enable Defender for Cloud on subscription; configure security contact; enable auto-provisioning of monitoring agent |
| 5 | Logging and Monitoring | Enable diagnostic settings for Container Apps environments; send logs to Log Analytics; configure activity log alerts for resource changes |
| 6 | Networking | Use NSGs on Container Apps VNet subnet; deny inbound from internet to Container Apps (private only); enable Network Watcher flow logs |

### Gaps and Recommendations

- **GAP**: Container Apps does not natively support WAF. If public-facing, route through Azure Application Gateway with WAF v2 or Azure Front Door with WAF policies.
- **GAP**: DDoS protection — if using a public IP, enable Azure DDoS Protection Standard on the VNet.
- **REC**: Enable Defender for Containers to detect runtime threats on container images.
- **REC**: Implement egress lockdown via Azure Firewall with FQDN filtering to limit outbound traffic to only required Azure service endpoints.

---

## Bucket 2: DevOps / Platform Ops (CI/CD, Bicep IaC, .NET Aspire, ACR)

### WAF Security Pillar

| WAF ID | Recommendation | Application |
|--------|---------------|-------------|
| SE:02 | Secure development lifecycle | Integrate security into GitHub Actions pipeline; implement SAST, DAST, SCA scanning; code review gates |
| SE:08 | Hardening | Use minimal Dockerfiles; multi-stage builds; non-root container user; scan images in ACR with Defender for Containers |
| SE:09 | Secrets management | No secrets in CI/CD pipeline code; use GitHub Secrets + Azure Key Vault; use OIDC federation for GitHub Actions → Azure authentication (no stored credentials) |
| SE:11 | Security testing | Add security scanning steps: `dotnet format` analyzers, container image scanning, dependency vulnerability scanning, Bicep linting (`az bicep lint`) |

### CAF Controls

- **Governance (RM01)**: Use Bicep for all resource deployments; store IaC in source control; enforce via policy
- **Security governance (SC03)**: Use designated GitHub organization; enforce branch protection rules
- **Security governance (SC04)**: Adopt quarantine pattern for NuGet packages from public sources
- **Integrity**: Sign container images; verify image integrity before deployment; use immutable tags in ACR
- **Posture sustainment**: Integrate Defender for DevOps to surface security findings in pull requests

### CIS Azure Foundations Benchmark

| CIS Section | Controls | Application |
|-------------|----------|-------------|
| 2 | Defender for Cloud | Enable Defender for Containers on ACR; integrate Defender for DevOps with GitHub |
| 10 | Miscellaneous | Ensure resource locks on production resources; enforce tagging strategy |

### MCSB Controls

| MCSB ID | Control | Application |
|---------|---------|-------------|
| DS-1 | Conduct threat modeling | Threat model CI/CD pipeline; identify credential exposure, supply chain, injection risks |
| DS-2 | Ensure software supply chain security | Pin NuGet/Docker dependencies; use lock files; scan for known vulnerabilities |
| DS-6 | Enforce security of workload through CI/CD pipeline | Gate deployments on security scan pass; enforce IaC scanning |
| DS-7 | Ensure logging and monitoring in DevOps | Audit pipeline execution; log all deployments and approvals |

### Gaps and Recommendations

- **GAP**: No mention of SBOM generation — required for SOC 2 and supply chain transparency. Generate SBOM in CI/CD pipeline (e.g., `dotnet sbom` or Syft).
- **GAP**: No IaC security scanning mentioned — add Bicep validation with `az deployment what-if` and tools like Checkov or PSRule for Azure.
- **REC**: Use OIDC workload identity federation for GitHub Actions → Azure, eliminating stored service principal secrets.
- **REC**: Enable ACR quarantine pattern — images pushed to ACR are quarantined until vulnerability scan passes.

---

## Bucket 3: Build (.NET 8 SDK, NuGet, Dockerfile, Azure SDK packages)

### WAF Security Pillar

| WAF ID | Recommendation | Application |
|--------|---------------|-------------|
| SE:02 | Secure development lifecycle | Enable .NET code analyzers (security rules); use `dotnet audit` for NuGet vulnerability scanning; enforce code review |
| SE:08 | Hardening | .NET 8 runtime hardening: enable trimming where safe; use ahead-of-time (AOT) compilation for smaller attack surface; disable XML external entity processing; configure secure HTTP headers |
| SE:11 | Security testing | Unit test security-critical paths (auth middleware, tenant isolation, input validation); run OWASP ZAP or equivalent DAST against staging |

### CAF Controls

- **Security governance (SC04)**: Quarantine pattern for NuGet packages — evaluate packages before allowing into internal feed
- **Integrity**: Pin package versions in `.csproj` files; use lock files (`packages.lock.json`); validate package signatures
- **Data governance (DG01)**: Ensure no sensitive data in build artifacts or logs

### CIS Azure Foundations Benchmark

| CIS Section | Controls | Application |
|-------------|----------|-------------|
| N/A | Build-time controls are outside CIS Azure scope | Covered by MCSB DS-2 (supply chain security) and SE:02 (SDL) |

### MCSB Controls

| MCSB ID | Control | Application |
|---------|---------|-------------|
| DS-2 | Software supply chain security | Audit NuGet dependencies; use private NuGet feed or Azure Artifacts; scan Dockerfile base images |
| DS-3 | Secure DevOps infrastructure | Protect build agents; limit network access; use ephemeral build agents |
| PV-6 | Rapidly and automatically remediate vulnerabilities | Automate Dependabot/Renovate for NuGet and Docker base image updates |

### Gaps and Recommendations

- **GAP**: Dockerfile security — ensure multi-stage builds, non-root user, no secrets baked into layers, minimal base image (mcr.microsoft.com/dotnet/aspnet:8.0-alpine or chiselled).
- **REC**: Enable GitHub Dependabot for NuGet and Docker; configure auto-merge for patch-level updates.
- **REC**: Use `dotnet nuget audit` in CI pipeline to fail builds on known vulnerabilities.
- **REC**: Pin Azure SDK package versions; avoid floating version ranges.

---

## Bucket 4: Messaging (Azure Service Bus)

### WAF Security Pillar

| WAF ID | Recommendation | Application |
|--------|---------------|-------------|
| SE:04 | Segmentation | Use separate Service Bus queues per message type; isolate dead-letter queues |
| SE:05 | IAM | Use managed identity for Service Bus access; assign `Azure Service Bus Data Sender/Receiver` roles (not `Owner`); disable SAS key authentication |
| SE:06 | Network controls | Enable private endpoint for Service Bus; disable public network access; restrict via VNet service endpoints |
| SE:07 | Encryption | Enable infrastructure encryption (double encryption at rest); TLS 1.2 enforced in transit |
| SE:09 | Secrets | Eliminate SAS tokens; use managed identity exclusively; if SAS required, store in Key Vault with rotation |
| SE:10 | Monitoring | Enable diagnostic logs for Service Bus; monitor queue depth, dead-letter count, throttling |

### CAF Controls

- **Confidentiality**: Encrypt message payloads containing shopper references at application level before enqueue (defense in depth)
- **Integrity**: Validate message schema on dequeue; implement idempotent processing; use duplicate detection
- **Availability**: Use Premium tier for predictable performance; enable geo-disaster recovery for production
- **Governance**: Enforce Azure Policy for Service Bus (private endpoint required, minimum TLS version)

### CIS Azure Foundations Benchmark

| CIS Section | Controls | Application |
|-------------|----------|-------------|
| 5 | Logging | Enable diagnostic settings for Service Bus namespace; send to Log Analytics |
| 6 | Networking | Private endpoint required; public network access disabled |

### Gaps and Recommendations

- **GAP**: Message payload encryption — Service Bus encrypts at rest but application-level encryption of message bodies containing assessment references adds defense in depth, especially for biometric-adjacent data under BIPA.
- **REC**: Use Service Bus Premium tier for VNet integration and CMEK support.
- **REC**: Configure dead-letter queue monitoring and alerting — abandoned messages may contain assessment IDs that need audit tracking.

---

## Bucket 5: Data (Azure Cosmos DB, Azure Blob Storage, Azure Key Vault)

### WAF Security Pillar

| WAF ID | Recommendation | Application |
|--------|---------------|-------------|
| SE:03 | Data classification | Classify: Photos = Highly Confidential (transient 60s), Measurements = Confidential, Garment catalog = Internal; apply labels in Purview |
| SE:04 | Segmentation | Hierarchical partition keys enforce tenant isolation (tenantId/entityType/entityId); separate blob containers per data type |
| SE:05 | IAM | Disable Cosmos DB key-based auth; use Entra ID RBAC for data plane; managed identity for all service access; RBAC for Blob Storage |
| SE:06 | Network | Private endpoints for Cosmos DB, Blob Storage, and Key Vault; disable public access on all three |
| SE:07 | Encryption | Cosmos DB: encryption at rest (service-managed or CMK via Key Vault); Blob Storage: encryption at rest + TLS 1.2 in transit; Key Vault: HSM-backed keys for BIPA compliance |
| SE:08 | Hardening | Cosmos DB: disable local auth, restrict CORS, configure IP firewall rules; Blob Storage: disable anonymous access, enforce HTTPS-only, immutable lifecycle policy on transient container; Key Vault: enable purge protection and soft delete |
| SE:09 | Secrets | All secrets/keys/certificates in Key Vault; enable audit logging; automate key rotation; no secrets in app configuration |
| SE:10 | Monitoring | Enable Cosmos DB control plane audit logs; Blob Storage diagnostic logs; Key Vault audit logs; enable Defender for Cosmos DB, Defender for Storage, Defender for Key Vault |

### CAF Controls

- **Data governance (DG01)**: Encryption at rest and in transit for all sensitive data
- **Data governance (DG02)**: Lifecycle policies on Blob Storage (60s TTL for photos); Cosmos DB TTL for transient assessment data
- **Confidentiality**: Azure Purview data classification for Cosmos DB and Blob Storage; information protection labels
- **Integrity**: Cosmos DB continuous backup with point-in-time restore; Blob Storage immutable policy on transient container; Key Vault soft delete + purge protection
- **Posture sustainment**: Enable Defender for all data services; track secure score recommendations

### CIS Azure Foundations Benchmark

| CIS Section | Controls | Application |
|-------------|----------|-------------|
| 3 | Storage Accounts | Require secure transfer (HTTPS only); enable blob encryption; configure storage lifecycle management; disable public blob access; enable storage logging; use private endpoints |
| 4 | Database Services | Cosmos DB: disable key-based authentication; enable diagnostic logging; configure firewall rules; use private endpoints; enable Defender for Cosmos DB |
| 5 | Logging | Enable Key Vault logging; Cosmos DB diagnostic settings; Storage Analytics logging |
| 8 | Key Vault | Enable soft delete; enable purge protection; configure RBAC access policy; enable logging; set key expiration; restrict network access to private endpoint |

### MCSB Controls

| MCSB ID | Control | Application |
|---------|---------|-------------|
| DP-1 | Discover, classify, label sensitive data | Use Purview to classify photo blobs, measurement documents, garment data |
| DP-2 | Monitor anomalies and threats to sensitive data | Enable Defender for Storage, Cosmos DB, Key Vault |
| DP-3 | Encrypt sensitive data in transit | TLS 1.2+ for all connections; enforce minimum TLS version |
| DP-4 | Enable data at rest encryption by default | Cosmos DB and Storage default encryption; evaluate CMK for BIPA data |
| DP-5 | Use customer-managed key option when applicable | Consider CMK for Cosmos DB and Blob Storage containing measurement data (BIPA compliance) |
| DP-7 | Use secure key management | Key Vault with HSM; key rotation policies; certificate management |

### Gaps and Recommendations

- **CRITICAL GAP**: **BIPA compliance** — Illinois BIPA requires explicit written consent before collecting biometric data and a published data retention/destruction policy. Architecture addresses 60s photo purge but MUST ensure: (a) consent capture before photo upload, (b) written biometric data policy published per BIPA §15, (c) audit trail of consent and destruction.
- **GAP**: **CMK evaluation** — For SOC 2 Type II and BIPA, evaluate whether customer-managed keys (CMK) are needed for Cosmos DB and Blob Storage. CMK adds compliance evidence but increases operational complexity.
- **GAP**: **Purview integration** — No data classification/labeling tooling configured. Microsoft Purview should be integrated for automated classification of Confidential/Highly Confidential data.
- **REC**: Enable Cosmos DB continuous backup (7-day or 30-day retention) for point-in-time recovery.
- **REC**: Configure Blob Storage immutable policy with legal hold on transient container to prevent TTL policy modification (already in architecture as spec).
- **REC**: Use Azure Key Vault Managed HSM for production keys if BIPA requires higher key protection assurance.

---

## Bucket 6: Web / UI / Reporting (ASP.NET Core Web API, API Management, OpenAPI 3.0.3)

### WAF Security Pillar

| WAF ID | Recommendation | Application |
|--------|---------------|-------------|
| SE:01 | Security baseline | Apply ASP.NET Core security best practices; configure security headers (HSTS, X-Content-Type-Options, X-Frame-Options, CSP) |
| SE:05 | IAM | JWT validation middleware; tenant claim extraction; per-tenant authorization; rate limiting per tenant tier |
| SE:06 | Network | API Management (v2) with VNet integration as API gateway; WAF policy on Application Gateway; IP filtering |
| SE:07 | Encryption | HTTPS-only; TLS 1.2 minimum; disable TLS 1.0/1.1 |
| SE:08 | Hardening | Disable unused API endpoints; enforce request size limits (10 MB max for photo upload); validate Content-Type headers; sanitize error responses to prevent information leakage |
| SE:11 | Security testing | OWASP API Security Top 10 testing; fuzzing on API endpoints; pen testing before production launch |

### CAF Controls

- **Security governance**: API Management policies for rate limiting, JWT validation, CORS, request/response transformation
- **Confidentiality**: No PII in API response error messages; strip internal headers; mask sensitive data in logs
- **Integrity**: OpenAPI contract validation; request schema validation; input sanitization against injection
- **Governance**: API versioning strategy; deprecation policies; API subscription key management (if APIM used)

### CIS Azure Foundations Benchmark

| CIS Section | Controls | Application |
|-------------|----------|-------------|
| 6 | Networking | APIM: VNet integration; private endpoint for internal APIs; NSG rules |
| 9 | App Service (partial) | Applicable security headers and TLS configuration patterns apply to Container Apps hosting ASP.NET Core |

### Gaps and Recommendations

- **GAP**: **APIM deferred to v2** — current architecture uses ASP.NET Core middleware for rate limiting. Without APIM, the API lacks WAF protection, centralized throttling, and API key management. Recommend accelerating APIM adoption for SOC 2 audit evidence.
- **GAP**: **OpenAPI security scheme** — Ensure OpenAPI 3.0.3 spec documents OAuth 2.0 security schemes with correct Entra ID token endpoints per tenant.
- **REC**: Implement ASP.NET Core security headers middleware (HSTS, CSP, X-Content-Type-Options, X-Frame-Options, Referrer-Policy).
- **REC**: Configure request validation middleware to reject payloads exceeding 10 MB and invalid MIME types before reaching business logic.
- **REC**: Implement OWASP API Security Top 10 controls: broken authentication, excessive data exposure, injection, improper asset management.
- **REC**: For SOC 2 evidence, log all API authentication events (success/failure) with correlation IDs.

---

## Bucket 7: Identity / Auth (Microsoft Entra ID, OAuth 2.0/OIDC, Managed Identity, JWT)

### WAF Security Pillar

| WAF ID | Recommendation | Application |
|--------|---------------|-------------|
| SE:05 | IAM | Multi-tenant Entra ID app registration; per-tenant service principals with scoped API permissions; least-privilege roles; disable legacy auth protocols |
| SE:05 | IAM | Managed identity for all Azure resource access (Cosmos DB, Blob, Key Vault, AI services, Service Bus) — zero secrets |
| SE:05 | IAM | JWT validation: validate issuer, audience, expiration, signature, tenant ID claim; reject tokens with wrong tenant |
| SE:08 | Hardening | Disable app credential secrets where possible; prefer certificate-based credentials; set short token lifetimes; implement token replay protection |
| SE:09 | Secrets | No client secrets in application configuration; use managed identity; if client secrets needed for tenant onboarding, store in Key Vault with rotation |

### CAF Controls

- **Security governance (SC01)**: MFA required for all administrative users accessing Entra ID admin portal
- **Security governance (SC02)**: Monthly access reviews for API permissions and service principal assignments
- **Identity governance**: Enable Conditional Access policies for administrative access; enable sign-in risk policies
- **Posture modernization**: Align with Zero Trust — verify explicitly (JWT on every request), least privilege (scoped roles), assume breach (log everything)

### CIS Azure Foundations Benchmark

| CIS Section | Controls | Application |
|-------------|----------|-------------|
| 1 | Identity and Access Management | 1.1: Ensure MFA is enabled for all users; 1.2: Ensure Conditional Access policies; 1.3: Block legacy authentication; 1.4: Restrict user consent to managed apps; 1.5: Disable self-service group management for external users; 1.6: Ensure guest access is restricted; 1.21: Ensure security defaults enabled (or Conditional Access) |

### MCSB Controls

| MCSB ID | Control | Application |
|---------|---------|-------------|
| IM-1 | Centralized identity | Microsoft Entra ID as sole IdP; no custom identity stores |
| IM-2 | Protect identity systems | Entra ID Identity Secure Score; address all recommendations |
| IM-3 | Managed application identities | Managed identity on Container Apps for all Azure service access |
| IM-4 | Authenticate server and services | TLS everywhere; certificate validation |
| IM-6 | Strong authentication | OAuth 2.0 client credentials with certificate; block password-based auth for service accounts |
| IM-7 | Conditional access | Conditional Access for admin portal access; location/device-based policies |
| IM-8 | Restrict credential exposure | Zero secrets architecture via managed identity; GitHub secret scanning enabled |

### Gaps and Recommendations

- **GAP**: **Multi-tenant token validation** — Must validate `tid` (tenant ID) claim in JWT tokens against registered tenants; reject tokens from unregistered tenants. This is a critical cross-tenant isolation control.
- **GAP**: **Tenant onboarding security** — Process for registering new tenant service principals must include security review; revocable access; credential rotation policy.
- **REC**: Implement Entra ID Continuous Access Evaluation (CAE) for near-real-time token revocation.
- **REC**: Configure app roles in Entra ID app registration to define fine-grained API permissions (e.g., `FitAssessment.Read`, `GarmentCatalog.Write`, `Admin.Manage`).
- **REC**: Enable Entra ID audit logs and sign-in logs; send to Log Analytics for SOC 2 evidence.
- **REC**: For BIPA compliance, ensure consent metadata flows through the auth chain — the API must verify consent was captured before processing photos.

---

## Bucket 8: AI/ML (Azure AI Vision, Azure ML Endpoint, Body Landmark Extraction)

### WAF Security Pillar

| WAF ID | Recommendation | Application |
|--------|---------------|-------------|
| SE:03 | Data classification | Photos sent to AI services = Highly Confidential; ensure AI service data processing agreement covers biometric data handling |
| SE:05 | IAM | Managed identity for Azure AI Vision and Azure OpenAI access; disable key-based auth where supported; use RBAC roles (`Cognitive Services User`) |
| SE:06 | Network | Private endpoints for all AI services; VNet integration; disable public access |
| SE:07 | Encryption | TLS 1.2 for AI service calls; data at rest encryption on AI service side (Microsoft-managed) |
| SE:08 | Hardening | Configure Azure AI Content Safety for minor detection and inappropriate content filtering; set content filtering to medium or higher; apply system messages for GPT-4o to constrain behavior |
| SE:10 | Monitoring | Log all AI service calls with model version, latency, confidence scores; monitor for abuse patterns; enable AI abuse monitoring |
| SE:11 | Security testing | Red-team the measurement extraction prompt for prompt injection, jailbreak, data exfiltration; test Content Safety filters |

### CAF Controls

- **AI governance (AI01)**: Content filtering configuration set to medium or higher
- **AI governance (AI02)**: Monthly red-teaming of customer-facing AI systems
- **AI governance**: Apply Azure AI security baseline; use system messages to constrain behavior; configure data loss prevention for AI services
- **Confidentiality**: Photos MUST NOT be stored or logged by AI services beyond processing; verify Azure AI Vision and OpenAI data processing commitments; confirm opt-out of human review for abuse monitoring
- **Integrity**: Version-pin AI models (e.g., `gpt-4o-2024-08-06`); track model version per assessment for audit traceability

### CIS Azure Foundations Benchmark

| CIS Section | Controls | Application |
|-------------|----------|-------------|
| 2 | Defender for Cloud | Enable Defender recommendations for AI services |
| 5 | Logging | Diagnostic settings on Azure AI services; track all API calls |
| 6 | Networking | Private endpoints for AI services; no public access |

### MCSB Controls (AI Security Domain — v2 Preview)

| MCSB ID | Control | Application |
|---------|---------|-------------|
| AI-1 | Discover and inventory AI workloads | Catalog all AI service instances (AI Vision, OpenAI, Content Safety); document data flows |
| AI-2 | Protect AI data processing | Ensure photos are not retained by AI services; verify data residency; opt out of human review |
| AI-3 | Secure AI model deployment | Version-pin models; validate model outputs; implement confidence thresholds |
| AI-4 | Secure AI access | Managed identity; RBAC; private endpoints |
| AI-5 | Protect AI-generated content | Content Safety filtering; output validation; confidence scoring |
| AI-6 | Monitor AI systems | Log all AI interactions; track model drift; alert on anomalous patterns |
| AI-7 | Red-team AI systems | Regular adversarial testing; prompt injection testing; bias testing |

### Gaps and Recommendations

- **CRITICAL GAP**: **BIPA — biometric data processing by AI services** — Azure OpenAI and AI Vision process body photos that may constitute biometric identifiers under Illinois BIPA. MUST verify: (a) Microsoft DPA covers biometric data processing, (b) data is not retained for training, (c) opt-out of Abuse Monitoring human review is enabled for the deployment.
- **CRITICAL GAP**: **Prompt injection defense** — GPT-4o Vision measurement extraction is vulnerable to prompt injection via crafted images or manipulated metadata. Implement input validation, output schema validation, and monitor for anomalous measurement values.
- **GAP**: **AI model explainability** — SOC 2 and CCPA require explainability for automated decisions. Ensure confidence scores and per-area breakdowns provide sufficient transparency for audit.
- **GAP**: **Minor detection** — Content Safety minor detection MUST be applied BEFORE photo reaches measurement extraction. Architecture has this in Tier 1, but must be enforced in code flow.
- **REC**: Apply Azure AI Content Safety with custom blocklists for inappropriate content categories.
- **REC**: Implement output validation — reject measurement values outside physiologically valid ranges (e.g., shoulder width < 20 cm or > 70 cm).
- **REC**: Store AI model version, prompt version hash, and confidence score per assessment for SOC 2 audit trail.

---

## Cross-Cutting Compliance Mapping

### CCPA/CPRA Requirements

| Requirement | Architecture Coverage | Gap |
|-------------|----------------------|-----|
| Right to know (data collected) | Opaque shopper IDs; measurement profiles queryable | Need API endpoint for data subject access requests (DSAR) |
| Right to delete | FR-006: profile deletion within 24h | Confirm cascade deletion across Cosmos DB, Blob, and any cached data |
| Right to opt out of sale/sharing | No data sale/sharing by design | Document in privacy policy; no cross-tenant data sharing |
| Data minimization | Photos purged <60s; only measurements retained | Verify no photo data persists in logs, AI service caches, or telemetry |
| Risk assessment for high-risk processing | Body measurement extraction is high-risk | Conduct DPIA before production launch |

### Illinois BIPA Requirements

| Requirement | Architecture Coverage | Gap |
|-------------|----------------------|-----|
| §15(a) Written policy for retention/destruction | 60s photo purge; 24h deletion SLA | MUST publish written biometric data policy |
| §15(b) Informed written consent | Architecture assumes frontend captures consent | API MUST verify consent claim in request; log consent evidence |
| §15(c) No profit from biometric data | B2B service charges for API usage, not biometric data | Ensure contract terms prohibit biometric data monetization |
| §15(d) No disclosure without consent | No third-party sharing by design | Verify AI services DPA; ensure no data egress to unauthorized parties |
| §15(e) Store/transmit/protect with reasonable standard | Encryption at rest/transit; managed identity; private endpoints | Document security controls in BIPA compliance filing |

### SOC 2 Type II Control Categories

| Category | Mapped Controls | Evidence Sources |
|----------|----------------|-----------------|
| CC6 — Logical and Physical Access | SE:05 (IAM), IM-1 through IM-9, CIS §1 | Entra ID sign-in logs, RBAC assignments, Conditional Access policies |
| CC7 — System Operations | SE:10 (monitoring), SE:12 (IR), LT-1 through LT-7 | Azure Monitor alerts, Log Analytics queries, incident response runbooks |
| CC8 — Change Management | SE:02 (SDL), DS-1 through DS-7, CAF RM01 | GitHub PR history, CI/CD pipeline logs, Bicep deployment history |
| CC9 — Risk Mitigation | SE:01 (baseline), SE:11 (testing), PV-1 through PV-6 | Defender for Cloud secure score, vulnerability scan reports, pen test reports |
| A1 — Availability | Availability zones, health probes, autoscaling | Container Apps metrics, SLA reports |
| C1 — Confidentiality | SE:03 (classification), SE:07 (encryption), DP-1 through DP-7 | Purview classification reports, encryption configuration evidence |
| P1 — Privacy | CCPA/BIPA controls above, data lifecycle policies | DSAR fulfillment logs, consent records, photo purge audit trail |

---

## Priority Action Matrix

### Critical (Pre-Production Blockers)

| # | Action | Bucket | Framework |
|---|--------|--------|-----------|
| 1 | Publish BIPA §15(a) written biometric data retention/destruction policy | Data, AI/ML | BIPA |
| 2 | Implement consent verification in API request flow (BIPA §15(b)) | Identity, Web | BIPA, CCPA |
| 3 | Verify Azure OpenAI DPA covers biometric data; opt out of human review | AI/ML | BIPA |
| 4 | Enable private endpoints for ALL Azure services (Cosmos DB, Blob, KV, AI, Service Bus) | All | SE:06, CIS §6 |
| 5 | Implement prompt injection defense for GPT-4o Vision | AI/ML | SE:11, AI-7 |
| 6 | Deploy Container Apps in private VNet with internal ingress only | Infra | SE:06, CIS §6 |

### High (SOC 2 Readiness)

| # | Action | Bucket | Framework |
|---|--------|--------|-----------|
| 7 | Enable Defender for Cloud across all services (Containers, Storage, Cosmos, KV, AI) | All | SE:10, CIS §2 |
| 8 | Configure diagnostic settings on ALL Azure resources → Log Analytics | All | SE:10, CIS §5 |
| 9 | Implement OIDC federation for GitHub Actions → Azure (eliminate stored credentials) | DevOps | SE:09, IM-8 |
| 10 | Disable key-based auth on Cosmos DB; use Entra ID RBAC only | Data | SE:05, CIS §4 |
| 11 | Enable Key Vault soft delete + purge protection + audit logging | Data | SE:09, CIS §8 |
| 12 | Implement DSAR API endpoint for CCPA right-to-know and right-to-delete | Web | CCPA/CPRA |
| 13 | Generate SBOM in CI/CD pipeline | DevOps | DS-2, SOC 2 CC8 |

### Medium (Hardening)

| # | Action | Bucket | Framework |
|---|--------|--------|-----------|
| 14 | Add WAF (Application Gateway WAF v2 or APIM with WAF policies) | Infra, Web | SE:06 |
| 15 | Implement ASP.NET Core security headers (HSTS, CSP, X-Content-Type-Options) | Web | SE:08 |
| 16 | Configure multi-tenant JWT validation with `tid` claim verification | Identity | SE:05, IM-1 |
| 17 | Set up monthly AI red-teaming process | AI/ML | AI-7, CAF AI02 |
| 18 | Integrate Microsoft Purview for data classification | Data | SE:03, DP-1 |
| 19 | Configure egress lockdown via Azure Firewall with FQDN filtering | Infra | SE:06, NS-2 |
| 20 | Implement container image scanning in CI/CD pipeline (Defender for Containers) | DevOps | SE:08, DS-2 |

---

## Follow-On Questions (Cannot Be Resolved by Research Alone)

1. **Azure OpenAI DPA scope**: Does the current Microsoft DPA/addendum explicitly classify body photos processed via Azure OpenAI as biometric data under BIPA? Legal review required.
2. **Human review opt-out**: Has Abuse Monitoring human review opt-out been approved for this Azure OpenAI deployment? Requires Azure support request.
3. **CMK decision**: Will the organization use customer-managed keys for Cosmos DB and Blob Storage? Impacts cost and operational complexity.
4. **APIM timeline**: Is Azure API Management adoption being accelerated to v1, or remaining v2 scope? Affects SOC 2 evidence for centralized API governance.
5. **Penetration testing**: Has a pre-production penetration test been scheduled? Required for SOC 2 Type II evidence.

---

## References

- WAF Security Pillar Checklist: https://learn.microsoft.com/en-us/azure/well-architected/security/checklist
- WAF Container Apps Service Guide: https://learn.microsoft.com/en-us/azure/well-architected/service-guides/azure-container-apps
- WAF Cosmos DB Service Guide: https://learn.microsoft.com/en-us/azure/well-architected/service-guides/cosmos-db
- CAF Secure Overview: https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/secure/
- CAF Governance Enforcement: https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/govern/security-baseline/
- MCSB Introduction: https://learn.microsoft.com/en-us/security/benchmark/azure/introduction
- MCSB Identity Management: https://learn.microsoft.com/en-us/security/benchmark/azure/security-controls-v3-identity-management
- CIS Azure Foundations Benchmark v6.0: https://www.cisecurity.org/benchmark/azure
- Azure Container Apps Security Baseline: https://learn.microsoft.com/en-us/security/benchmark/azure/baselines/azure-container-apps-security-baseline
- Azure Cosmos DB Security Baseline: https://learn.microsoft.com/en-us/security/benchmark/azure/baselines/azure-cosmos-db-security-baseline

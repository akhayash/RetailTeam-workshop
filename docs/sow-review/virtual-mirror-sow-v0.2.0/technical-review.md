# Technical Review — Virtual-Mirror-SOW.md (Azure Architect Perspective)

| Field                     | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Document under review** | [docs/Virtual-Mirror-SOW.md](../../Virtual-Mirror-SOW.md) v0.2.0 (2026-05-14, Draft for internal review)                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **Review scope**          | Azure service naming accuracy, solution-architecture soundness, SKU/tier specificity, SLO/SLA realism, multi-tenant data design, identity, networking & edge, observability, IaC/CI-CD supply chain, regional availability, and AI model deployment correctness. Compliance/security topics are reviewed separately in [compliance-and-security-review.md](compliance-and-security-review.md).                                                                                                                                        |
| **Reviewer**              | Microsoft — Azure Solution Architecture Review                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **Review date**           | 2026-05-14                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **Verdict**               | **Conditional Pass.** Version 0.2.0 improves business-priority clarity, MVP cutline governance, risk ownership, D-13 DPIA acceptance, and delivery RACI. The Azure architecture blockers from the earlier review largely remain: AI model naming/access assumptions, ambiguous "Azure Front Door / APIM" notation, missing SKU/tier specificity, single-region SLO/RTO/RPO realism, and Cosmos DB API / partition strategy. Address Critical and High items before signature; Medium and Low items can be tracked in the ADR backlog. |
| **Evidence basis**        | **Microsoft Learn MCP-backed review.** Microsoft documentation tools were activated and used on 2026-05-14. Key Microsoft Learn pages were searched and fetched for Foundry / Azure OpenAI model naming, Foundry deployment types, Azure Container Apps reliability, Azure Cosmos DB hierarchical partition keys, and Front Door / APIM / WAF architecture. See section 5.                                                                                                                                                            |
| **Cross-references**      | [solution-architecture.md](../../architecture/solution-architecture.md) · [diagrams.md](../../architecture/diagrams.md) · [cost-estimate.md](../../architecture/cost-estimate.md) · [resiliency-review.md](../../architecture/resiliency-review.md) · [decision-register.md](../../architecture/decision-register.md)                                                                                                                                                                                                                 |

---

## 1. Severity Legend

**v0.2.0 delta**: The SOW now has better governance and acceptance mechanics, but the technical stack table and architecture assumptions still contain the same service-name and deployment-shape risks identified in v0.1.0. The most important unchanged phrases are `Azure OpenAI GPT-5.2 Vision`, `Florence-2`, `Azure Front Door / APIM`, `Azure Cosmos DB (multi-tenant document)`, `RTO < 1 h / RPO < 15 min`, and inconsistent hypercare boundaries.

**Microsoft Learn MCP re-run**: This review was re-validated on 2026-05-14 using Microsoft Learn MCP search/fetch results for Azure OpenAI reasoning model availability, Microsoft Foundry model deployment options, Azure Container Apps zone redundancy, Azure Front Door WAF + API Management, and Azure Cosmos DB multitenancy / hierarchical partition keys. The re-run did not remove any Critical or High findings; it strengthened the evidence behind F-1, F-2, F-3, F-5, and F-12.

|     Severity      | Definition                                                                                                                               | Action                                              |
| :---------------: | ---------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
|   **Critical**    | Naming or design is technically incorrect, will fail Azure validation/deployment, or materially misrepresents what Azure provides today. | Must fix before signature.                          |
|     **High**      | Ambiguity hides a decision that drives SLA, cost, or compliance. Risks downstream rework or scope creep.                                 | Must fix before signature or capture as an ADR.     |
|    **Medium**     | Service is named correctly but SKU/tier/region/SDK detail is missing or imprecise.                                                       | Resolve in Sprint 1 architecture finalisation.      |
|      **Low**      | Stylistic, alignment, or consistency issue with current Microsoft Learn nomenclature.                                                    | Track for next document revision.                   |
| **Informational** | Reasonable practice but worth flagging as an Azure-native alternative or upgrade path.                                                   | No action required; consider for v2 / Change Order. |

---

## 2. Findings Summary

|  #   | Finding                                                                                                                                                      |     Severity      | SOW section(s)                                               |
| :--: | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | :---------------: | ------------------------------------------------------------ |
| F-1  | "Azure OpenAI GPT-5.2 Vision" — naming, limited-access status, and regional availability not aligned with current Foundry catalog                            |   **Critical**    | §2.2, §3.2, §13.2, §16.1, §17.1 (C-2), §18.2 (A-6, A-7), D-2 |
| F-2  | Florence-2 deployment model unspecified (managed compute vs. serverless) and East US 2 availability not verified                                             |     **High**      | §2.2, §16.1, §17.1 (C-3), §18.2 (A-8)                        |
| F-3  | "Azure Front Door / APIM" slash notation hides whether one, the other, or both are deployed                                                                  |     **High**      | §16.1                                                        |
| F-4  | Composite SLO of ~99.9% for single-region v1 is not arithmetically defended; ACA zone-redundant SLA is 99.95% per service                                    |     **High**      | §5 (Architecture row), §18.2 (A-10), D-1, D-10               |
| F-5  | Azure Cosmos DB API flavor (NoSQL/SQL) and multi-tenant partition-key strategy unspecified                                                                   |     **High**      | §16.1, D-1, F (data-model.md reference)                      |
| F-6  | SKU/tier missing for Front Door, APIM, Key Vault, Service Bus, Blob redundancy, ACR, App Configuration                                                       |    **Medium**     | §16.1                                                        |
| F-7  | "Azure Monitor / Application Insights" slash conflates a platform service with one of its features                                                           |      **Low**      | §16.1                                                        |
| F-8  | Notation container signing key custody and Azure-native alternative (Azure Trusted Signing) not addressed                                                    |    **Medium**     | §11.1, §15.1, §17.1 (C-7), D-8                               |
| F-9  | Trivy chosen over Microsoft Defender for Containers / Defender for Cloud CLI without rationale                                                               | **Informational** | §11.1, §15.1, D-8                                            |
| F-10 | GitHub Actions → Azure authentication method (federated OIDC vs. service principal secret) not declared                                                      |    **Medium**     | §15.1, §16.1, D-8                                            |
| F-11 | RTO < 1 h / RPO < 15 min for a single-region v1 with no cross-region failover is over-stated                                                                 |     **High**      | §5, D-12                                                     |
| F-12 | ACA zone redundancy prerequisites (VNet integration, min replicas ≥ 2, workload profiles) not captured as customer dependency                                |    **Medium**     | §16.1, §16.2, §17.1                                          |
| F-13 | ".NET Aspire" listed under "Orchestration" without clarifying it is a dev-time inner-loop, not a production runtime                                          |      **Low**      | §16.1                                                        |
| F-14 | "Cosmos emulator" should be "Azure Cosmos DB Emulator" (Linux-based emulator now GA); Azurite is the Azure Storage emulator                                  |      **Low**      | §16.1, §16.2, WP1                                            |
| F-15 | Private networking posture (Private Endpoints, VNet, egress) not declared even though the service handles biometric data                                     |     **High**      | §16, D-1, D-7                                                |
| F-16 | Microsoft Foundry / Azure AI Foundry brand vs. legacy "Azure OpenAI Service" usage inconsistent across the SOW                                               |      **Low**      | §2.2, §16.1                                                  |
| F-17 | Cost estimate uses "$0.012–$0.018 per assessment" without naming the underlying Foundry deployment type (PAYG Standard, Global Standard, Provisioned, Batch) |    **Medium**     | §3.2, §16.4                                                  |
| F-18 | Microsoft Cloud Penetration Testing Rules of Engagement not referenced for the Walmart-procured pen test                                                     |    **Medium**     | §11.1, §17.1, §17.2                                          |
| F-19 | Azure region naming "East US 2" is canonical, but no fallback region or paired-region statement is made                                                      |    **Medium**     | §16.3, §18.2 (A-10)                                          |
| F-20 | Azure landing zone alignment (ALZ subscription topology, hub-and-spoke vs. Vnet-injection, policy assignment) implicit only                                  | **Informational** | §6, §17.1 (C-1)                                              |

---

## 3. Detailed Findings

### F-1 — "Azure OpenAI GPT-5.2 Vision": naming, access tier, regional availability · Severity: **Critical**

**Where it appears**: §2.2 ("Azure OpenAI GPT-5.2 Vision"), §16.1 stack table, §17.1 (C-2 "Azure OpenAI capacity / PTU allocation for GPT-5.2"), §18.2 (A-6 "GPT-5.2 Vision measurement accuracy ±2–4 cm", A-7 "Azure OpenAI GPT-5.2 is generally available in East US 2 by Sprint 3"), §13.2 (R-001).

**Observations from Microsoft Learn MCP (verified 2026-05-14)**

1. There is **no separate "GPT-5.2 Vision" SKU** in Microsoft Foundry. The current vision-enabled chat models are the **o-series, GPT-5 series, GPT-4.1 series, GPT-4.5, and GPT-4o series** (`https://learn.microsoft.com/azure/foundry/openai/how-to/gpt-with-vision`). Image input is a _capability_ exposed by these chat-completion models, not a distinct deployment name.
2. `gpt-5.2` is a real reasoning-series model (released 2025-12-11) and supports **Image input** per the feature-support matrix (`https://learn.microsoft.com/azure/foundry/openai/how-to/reasoning`). Its product name in tooling is simply `gpt-5.2`; "GPT-5.2 Vision" is not an Azure SKU.
3. Microsoft Learn MCP still reports `gpt-5.2` as **Limited Access**: "Request access: Limited access model application (`https://aka.ms/oai/gpt5access`). If you already have access to a limited access model no request is required." This contradicts SOW assumption A-7 ("generally available in East US 2 by Sprint 3"). GA timing for `gpt-5.2` cannot be assumed.
4. Regional availability for `gpt-5.2` is governed by the Foundry "Models sold directly by Azure" availability table — not a static "East US 2 by Sprint 3" statement. Current Microsoft Learn MCP results also show newer GPT-5-family reasoning models in the catalog, reinforcing that the SOW should specify a capability and fallback model family rather than hard-code an exact model SKU for the full contract term.
5. The service is now branded **"Azure OpenAI in Azure AI Foundry Models"** / **"Azure OpenAI in Microsoft Foundry Models"** in Microsoft Learn. Using the legacy "Azure OpenAI Service" name in a contract is acceptable in places, but the technical stack table should use the Foundry naming to avoid ambiguity with deployment types and model catalog availability.

**Recommended fixes**

- Rename to `Azure OpenAI in Microsoft Foundry — gpt-5.2 (image input)` throughout. Or, if there is freedom of choice, qualify as "an Azure OpenAI vision-enabled chat model (gpt-5.2, gpt-5, or gpt-4.1) selected at Sprint 3 based on H1 accuracy results and quota availability."
- In §18.2 A-7, change "generally available in East US 2 by Sprint 3" to: "Walmart has approved limited-access entitlement for `gpt-5.2` (or has accepted a fallback to GA-tier `gpt-5` / `gpt-4.1`) and capacity is allocatable in a supported region (East US 2 candidate; Foundry availability confirmed in Sprint 1)."
- In §17.1 C-2, add: "If `gpt-5.2` limited-access application is not granted by end of Sprint 2, fallback to a generally available vision model (`gpt-5`, `gpt-4.1`, or `gpt-4o`) under PR-1 / R-001 mitigation."
- In §13.2 R-001, restate as: "Vision-LMM measurement accuracy" (model-agnostic) rather than locking the risk to a specific SKU that may change.

---

### F-2 — Florence-2 deployment model and regional availability · Severity: **High**

**Where it appears**: §2.2, §16.1 ("Florence-2 on Azure AI Foundry"), §17.1 (C-3 "Florence-2 endpoint quota on Azure AI Foundry"), §18.2 (A-8 "Florence-2 on Azure AI Foundry is available in East US 2 with serverless billing for v1 volumes").

**Observations**

1. Florence-2 is a Microsoft vision foundation model distributed through the Foundry / Azure AI model catalog. Per the Microsoft Learn MCP result for the Foundry model deployment overview (`https://learn.microsoft.com/azure/foundry/concepts/foundry-models-overview`), models in the catalog deploy either via:
   - **Managed compute** — model weights deployed to dedicated VM instances (billed for VM core hours, e.g., `Standard_DS3_v2` instances), or
   - **Serverless deployment** — API access to Microsoft-hosted infrastructure; billing is typically based on inputs and outputs to the API. Microsoft Learn further breaks serverless / Foundry deployment types into Global Standard, Global Provisioned, Global Batch, Data Zone Standard, Data Zone Provisioned, Data Zone Batch, Standard, Regional Provisioned, and Developer deployment options.
2. Most Microsoft Research / Florence variants on the catalog have historically been deployed as **managed compute** (dedicated endpoints), not pay-per-token serverless. Assumption A-8 ("serverless billing") therefore needs verification — if Florence-2 is only available as managed compute in East US 2, the cost model in §16.4 (per-assessment cost) and the IaC scope (D-7) change materially.
3. Florence-2 capabilities (image captioning, dense captioning, OCR, segmentation, grounding) are also exposed through **Azure AI Vision Image Analysis 4.0** (Computer Vision API). If only the captioning / object-detection capabilities are needed, this is a simpler, GA-tier alternative that does not require a managed compute endpoint.

**Recommended fixes**

- In §18.2 A-8, replace "serverless billing" with the verified deployment mode (managed compute on `Standard_*` SKU **or** serverless if available for Florence-2). Reference the Foundry model card decision in an ADR.
- Add an evaluation task in Sprint 1: "Confirm Florence-2 deployment mode (managed compute vs. serverless) on Foundry in the chosen region and finalise cost estimate."
- Evaluate whether **Azure AI Vision Image Analysis 4.0** (GA Cognitive Services SKU) meets the image-quality / captioning needs; if yes, simplify the stack and remove Florence-2 dependency.
- In §16.1, change "Florence-2 on Azure AI Foundry" to either "Microsoft Florence-2 via Azure AI Foundry model catalog (managed compute, `<SKU>`)" or "Azure AI Vision Image Analysis 4.0 (Florence-powered)".

---

### F-3 — "Azure Front Door / APIM" slash notation · Severity: **High**

**Where it appears**: §16.1 stack table — "Edge | Azure Front Door / APIM (WAF, rate limiting, TLS termination)".

**Observations**

1. **Azure Front Door** and **Azure API Management (APIM)** are different services with overlapping but distinct concerns. Front Door is a global anycast CDN + reverse proxy with WAF (`Azure Web Application Firewall on Azure Front Door`, Standard / Premium tiers); APIM is an API gateway providing subscription keys, OAuth validation, transformations, developer portal, products and policies.
2. Microsoft's documented pattern for protecting API Management with WAF is **Azure Front Door Premium → APIM → backend** (`https://learn.microsoft.com/azure/web-application-firewall/afds/protect-api-hosted-apim-by-waf`). The Microsoft Learn page explicitly creates an Azure Front Door Premium profile and notes that the Microsoft-managed Default Rule Set is not available for Azure Front Door Standard. If the SOW requires managed rules / Bot Manager-style protection, this is a Premium-tier design decision.
3. The slash form leaves four interpretations unresolved: (a) Front Door only, (b) APIM only, (c) Front Door + APIM, (d) one or the other depending on rollout phase. Each has very different cost, IaC, identity, networking and ingress-control profiles.
4. Acceptance criterion D-7 references "12 Bicep modules + 3 environment parameter files for ACA, Cosmos, Blob, Key Vault, App Config, Front Door, observability, networking" — APIM is not listed. This implies "Front Door only" but contradicts §16.1.

**Recommended fixes**

- Pick one and reflect it everywhere (§16.1, §16.4 cost model, D-7 Bicep scope, diagrams.md). If the design is Front Door only, write "Azure Front Door Premium with Azure Web Application Firewall (managed rule set + rate limiting + TLS termination)".
- If APIM is in scope (recommended for multi-tenant per-operation OAuth scopes and product-based subscription, given §3.1 BO-3 multi-tenant target), name it as **Azure API Management (`Premium v2` or `StandardV2` tier)** and add the Front Door → APIM composition explicitly.
- Capture the choice as an ADR in `decision-register.md`.

---

### F-4 — Composite SLO claim of "~99.9% availability" for single-region v1 · Severity: **High**

**Where it appears**: §5 ("Multi-region active-active deployment (target ~99.95% composite SLA)" deferred to v2), §18.2 A-10 ("v1 supports a single Azure region (East US 2) with multi-AZ replicas; ~99.9% availability SLO"), D-10 (NBomber gate), D-12 (RTO/RPO).

**Observations from Microsoft Learn**

1. The Azure Container Apps availability SLA depends on scale rules; zone-redundant deployments (which the SOW assumes) qualify for a higher SLA. Per `https://learn.microsoft.com/azure/reliability/reliability-container-apps` and the [Azure SLA portal](https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services), zone-redundant ACA's published SLA is in the 99.95% range. The SOW's 99.9% is more conservative than what ACA alone offers.
2. The **composite SLO** for the service is the minimum of the chain — ACA × Cosmos DB × Service Bus × Front Door × Azure OpenAI × Azure AI Content Safety × Florence-2 endpoint. Multiplying single-9 SLAs across this chain drops the composite well below 99.9% if any leg is at 99.9% or less, and Azure OpenAI / Foundry models do **not** publish the same SLA as core platform services.
3. Single-region availability does not protect against region outages. The SOW correctly defers multi-region to v2 — but the v1 SLO statement should reflect that.
4. The Well-Architected Framework recommends interpreting SLAs as engineering signals, not guarantees, and to read each service's exclusions (`https://learn.microsoft.com/azure/reliability/concept-service-level-agreements`).

**Recommended fixes**

- Replace "~99.9% availability SLO" with a calculated composite expression: e.g., "Target SLO: 99.9% read availability for `POST /v1/assessments` measured at the Front Door edge, **excluding** Azure OpenAI / Foundry model downstream availability and customer storefront. Composite published-SLA arithmetic is documented in `resiliency-review.md`."
- In §13.2, add explicit risk for "downstream model outage" with degradation-ladder mitigation (already partially covered by D-6).
- In D-12, soften RTO/RPO claims (see F-11).

---

### F-5 — Cosmos DB API and multi-tenant partition strategy · Severity: **High**

**Where it appears**: §16.1 ("Azure Cosmos DB (multi-tenant document)"), §3.1 BO-3, D-1, D-3, D-5; data-model.md reference in §20 Appendix F.

**Observations from Microsoft Learn**

1. **"Azure Cosmos DB"** is a multi-API platform. The correct product name for the document/JSON variant is **Azure Cosmos DB for NoSQL**. Other APIs (MongoDB, Cassandra, Gremlin, Table, PostgreSQL) have different feature sets and SDKs. The SOW should commit.
2. For multi-tenant document stores at the scale BO-3 envisions (≥ 20 tenants at Scale tier), the Microsoft-recommended pattern is **hierarchical partition keys (HPK)** — e.g., `/tenantId/shopperRef/id` or `/tenantId/sku/id` — to break the 20 GB-per-logical-partition limit and avoid full fan-out queries. References:
   - `https://learn.microsoft.com/azure/cosmos-db/hierarchical-partition-keys`
   - `https://learn.microsoft.com/azure/cosmos-db/hierarchical-partition-keys-unlimited-scale`
   - `https://learn.microsoft.com/azure/architecture/guide/multitenant/service/cosmos-db`
3. HPK requires supported SDK versions (.NET v3 ≥ 3.33.0). The SOW does not pin the Microsoft.Azure.Cosmos SDK version.
4. RU/s consumption model is not stated (autoscale vs. provisioned, per-container vs. shared throughput).

**Recommended fixes**

- Rename to **Azure Cosmos DB for NoSQL** in §16.1.
- Add an explicit multi-tenancy ADR: HPK paths for each container (assessments, profiles, garments, audit-log), throughput model (recommend **autoscale** at v1 with a defined RU/s ceiling), and indexing policy.
- Pin SDK version in the dependencies appendix.
- Cross-reference `cosmosdb-best-practices` (this workspace's repo instructions) — partition-key cardinality (`tenantId` low cardinality at v1 with 1 tenant; HPK with `/id` as the last level ensures unlimited scale per tenant).

---

### F-6 — Missing SKU / tier specificity for edge, identity, and data services · Severity: **Medium**

**Where it appears**: §16.1 entire stack table; §16.4 cost model.

**Observations**

The cost estimate and SLA depend on tier; the SOW currently leaves these implicit:

| Service                  | Implicit in SOW               | Decision required                                                                                                                                                                                       |
| ------------------------ | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Azure Front Door         | Tier not stated               | **Premium** (managed WAF rule set + Private Link to origin); Standard does not include managed rules. Pricing differs materially (`https://learn.microsoft.com/azure/frontdoor/understanding-pricing`). |
| Azure API Management     | Inclusion ambiguous (see F-3) | If included, `StandardV2` or `Premium v2` for zone redundancy.                                                                                                                                          |
| Azure Key Vault          | Tier not stated               | **Premium** if biometric-derived secrets or HSM-backed keys are needed; otherwise Standard. SOW threat model treats data as biometric-adjacent.                                                         |
| Azure Service Bus        | Tier not stated               | **Premium** required for zone redundancy and VNet integration; Standard is multi-tenant.                                                                                                                |
| Azure Blob Storage       | Redundancy not stated         | **ZRS** or **GZRS** for zone-redundant durability inside East US 2; Premium block blob if 60-second TTL transient pattern warrants low latency.                                                         |
| Azure Container Registry | Not listed at all in §16.1    | Required for ACA images, Notation signing, and Trivy/Defender scans. **Premium** tier required for geo-replication and content-trust.                                                                   |
| Azure App Configuration  | Tier and replication unstated | **Standard** (the GA tier) with replicas in East US 2 / paired region for resilience.                                                                                                                   |
| Azure Cosmos DB          | Capacity mode unstated        | **Autoscale** at v1; **Provisioned throughput** at Scale tier. Multi-region writes disabled in v1.                                                                                                      |

**Recommended fixes**

- Update §16.1 with a "SKU / Tier" column and pin every line. This converts §16.4 cost from "estimated" to "auditable".
- Reflect the chosen SKUs in `cost-estimate.md` and Bicep parameter files (D-7).

---

### F-7 — "Azure Monitor / Application Insights" naming · Severity: **Low**

**Where it appears**: §16.1.

**Observations**

Application Insights is a feature of Azure Monitor (APM workspace-based). The slash treats them as alternatives; correct phrasing is "**Azure Monitor (Application Insights, Log Analytics workspace)**" or simply "Azure Monitor".

**Recommended fix**: rename to `Azure Monitor (Application Insights workspace-based, Log Analytics workspace)`.

---

### F-8 — Notation signing: key custody and Azure-native alternative · Severity: **Medium**

**Where it appears**: §11.1 ("SBOM generation (CycloneDX) and signing (Notation)"), §15.1, §17.1 (C-7 "Notation signing keys and access to container registry"), D-8.

**Observations**

1. **CNCF Notation** is correctly chosen — it is the official OCI artifact signing toolchain and integrates with Azure Container Registry. The keys it consumes are typically stored in **Azure Key Vault** (`AKV-keys` plugin) or — for Microsoft-managed PKI — **Azure Trusted Signing** (formerly Azure Code Signing).
2. The SOW makes Walmart provide "Notation signing keys" (C-7) but does not specify the key store, key type (ECDSA / RSA), key length, rotation policy, or CRL/OCSP strategy.
3. Verification at deploy time on the ACA side is not addressed: the consumer of a signed image must use a verification policy (`trustpolicy.json`) and trust-store. This is platform-glue work that should be in D-8.

**Recommended fixes**

- Add a clause in C-7: "Walmart-issued or Microsoft Trusted Signing certificate, with keys stored in Azure Key Vault Premium under HSM-backed key type; rotation policy: every 12 months; revocation strategy: documented in DR plan."
- Add to D-8 acceptance: "Signed images verified at deployment to staging and prod by Notation trust policy enforced via ACR or ACA admission control."

---

### F-9 — Trivy vs. Microsoft Defender for Containers · Severity: **Informational**

**Where it appears**: §11.1, §15.1, D-8.

**Observations**

1. **Aqua Trivy** is a defensible, popular open-source choice. There is nothing technically wrong with it.
2. The Azure-native alternative is **Microsoft Defender for Containers** (registry VA + runtime VA powered by Microsoft Defender Vulnerability Management) and the new **Microsoft Defender for Cloud CLI** which replaces MSDO and uses the Microsoft Container Security Scanner (MDVM-backed) instead of Trivy in pipelines (`https://learn.microsoft.com/azure/defender-for-cloud/defender-cli-overview`). Notably, Microsoft retired AWS Trivy-backed VA in Feb 2024 in favour of MDVM.
3. Defender for Containers also adds runtime VA (cluster scan), agentless image inventory, and integration with the cloud security graph — capabilities Trivy alone does not deliver.

**Recommendation**: keep Trivy in CI for fast PR-time gating, but add **Defender for Containers (registry VA + runtime VA)** on the ACR and ACA environment as a defense-in-depth layer. Capture as an ADR.

---

### F-10 — GitHub Actions → Azure authentication method · Severity: **Medium**

**Where it appears**: §15.1 ("GitHub Actions CI workflow with SAST/SCA/SBOM/Trivy/Notation"), §16.1, D-8.

**Observations**

The SOW does not declare how the GitHub Actions runner authenticates to Azure. The two real options are:

1. **Federated OIDC** via Microsoft Entra workload identity federation (recommended, keyless, no client secret rotation).
2. **Client-secret service principal** stored in GitHub secrets (legacy, secret-rotation burden).

This affects threat model (T-3 supply chain), Bicep deployment identity, and the IAM diagram.

**Recommended fix**: state "GitHub Actions authenticates to Azure via **Microsoft Entra workload identity federation (OIDC)**; no long-lived client secrets are stored in GitHub" in §16.1 and D-8.

---

### F-11 — RTO < 1 h / RPO < 15 min for single-region v1 · Severity: **High**

**Where it appears**: D-12 "DR plan & data classification — DR plan documenting RTO < 1 h, RPO < 15 min for tenant config".

**Observations**

1. In a single-region v1 (no cross-region active-passive, no Cosmos DB multi-region writes), an Azure region outage of more than a few minutes invalidates any RTO < 1 h target unless the engagement is committed to redeploy the whole stack to a different region within the hour. The SOW does not include cross-region rehydration tooling or a warm secondary; the latter is explicitly deferred to v2 (§5).
2. RPO < 15 min for "tenant config" implies Cosmos DB Continuous Backup (point-in-time-restore, retention up to 30 days for tier 1). Worth pinning.

**Recommended fixes**

- Scope the RTO/RPO to **planned events** (deployments, instance loss, zone outage) — not regional outages — in v1. For a regional outage, document the rebuild procedure with a realistic RTO (4–8 h) and call it out.
- Pin **Azure Cosmos DB continuous backup** (point-in-time restore mode) with retention window in the Bicep config and capture in D-12.

---

### F-12 — Azure Container Apps zone redundancy prerequisites · Severity: **Medium**

**Where it appears**: §16.1 ("Azure Container Apps (multi-AZ, KEDA HTTP scaler, 2–10 instances)"), §17.1.

**Observations from Microsoft Learn** (`https://learn.microsoft.com/azure/reliability/reliability-container-apps`)

ACA zone redundancy requires:

1. A region that supports availability zones — East US 2 does.
2. **Workload-profiles environment** in a VNet — Consumption-only environments need a `/23` subnet, workload-profiles need `/27` or larger.
3. **Min replicas ≥ 2**, configured at creation time (zone redundancy cannot be enabled afterwards). Microsoft Learn also recommends at least **three replicas** for ingress-exposed apps in reliability best-practice guidance, so the SOW's 2-replica minimum meets the platform prerequisite but is thin for a production API.
4. KEDA HTTP scaler is supported; not the only option.

The SOW says "2–10 instances" which satisfies the minimum platform prerequisite, and "multi-AZ" implies zone redundancy, but it does **not** state the VNet integration, subnet sizing, creation-time zone redundancy requirement, or whether v1 should use a 3-replica minimum to keep one warm replica per zone during normal operation.

**Recommended fix**: in §16.1 / §16.2, add VNet integration, subnet CIDR, and "workload-profiles environment with zone redundancy enabled at creation" as architecture commitments. Change the v1 production minimum replica target from 2 to **3** unless cost pressure explicitly accepts reduced zone-failure headroom. Add a customer dependency in §17.1 if Walmart provides the VNet.

---

### F-13 — ".NET Aspire" listed as orchestration · Severity: **Low**

**Where it appears**: §16.1 ("Orchestration (local + integration) | .NET Aspire").

**Observations**

.NET Aspire is a developer inner-loop and integration-testing technology (AppHost orchestrator for multi-service local dev, with a Service Defaults library for OTel and service discovery). It is **not** a production runtime — in production the workloads run on **Azure Container Apps**. The SOW already says "(local + integration)" which is correct, but this nuance is worth reinforcing because Aspire's name suggests something broader.

**Recommended fix**: rename to ".NET Aspire (inner-loop orchestration + integration testing only; production runs on Azure Container Apps)".

---

### F-14 — "Cosmos emulator" / "Azurite" naming · Severity: **Low**

**Where it appears**: §16.1 ("docker-compose for Cosmos emulator + Azurite"), §16.2, WP1.

**Observations**

The official name is **Azure Cosmos DB Emulator** (now with a Linux-based GA image, `mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator`). **Azurite** is the canonical name for the Azure Storage emulator and is correct as written.

**Recommended fix**: change "Cosmos emulator" → "Azure Cosmos DB Emulator (Linux image)".

---

### F-15 — Private networking posture not declared · Severity: **High**

**Where it appears**: §16, D-1, D-7. The SOW threat model treats photos as biometric-adjacent.

**Observations**

For a biometric-handling workload, the standard Azure baseline is:

1. **Private Endpoints** (or service endpoints) on Cosmos DB, Blob Storage, Key Vault, Service Bus, ACR, App Configuration, Azure OpenAI, Foundry model endpoints.
2. ACA workload-profiles environment integrated into the same VNet.
3. Front Door fronting ACA via **Private Link** origin (Front Door Premium feature).
4. Disabled public network access (PNA flag = Disabled) on data plane services.
5. No internet egress from ACA except via NAT Gateway / Azure Firewall to Foundry endpoints (which may need to remain on public IPs depending on private-link availability).

The SOW does not declare this posture; D-7 mentions "private endpoints verified" but in passing. For biometric-class data, this is a sign-off-grade gap.

**Recommended fix**: add an architecture clause in §16 declaring the private networking baseline and pin "private endpoints on all data plane services" as a D-7 acceptance criterion.

---

### F-16 — Foundry brand vs. legacy "Azure OpenAI Service" · Severity: **Low**

**Where it appears**: §2.2 ("Azure OpenAI GPT-5.2 Vision"), §16.1 ("Azure OpenAI GPT-5.2 Vision · Florence-2 on Azure AI Foundry").

**Observations**

Microsoft has consolidated Azure OpenAI Service, Azure AI Studio, and the model catalog under the **Microsoft Foundry / Azure AI Foundry** umbrella. The current product names are "Azure OpenAI in Microsoft Foundry Models" and "Azure AI Foundry Models". Mixing "Azure OpenAI" and "Azure AI Foundry" within the same paragraph reads as two different services.

**Recommended fix**: unify to **"Azure AI Foundry — Azure OpenAI models"** and **"Azure AI Foundry — Florence-2"** for consistency.

---

### F-17 — Cost-per-assessment without naming Foundry deployment type · Severity: **Medium**

**Where it appears**: §3.2 ($0.012–$0.018 per assessment), §16.4 cost table.

**Observations**

Foundry offers several deployment types: **Global Standard**, **Global Provisioned**, **Global Batch**, **Data Zone Standard**, **Data Zone Provisioned**, **Standard (Regional)**, **Regional Provisioned**, and **Developer**. Each has different per-token / per-call pricing and different data-residency guarantees (`https://learn.microsoft.com/azure/foundry/foundry-models/concepts/deployment-types`). The per-assessment cost is unauditable without naming the deployment type.

**Recommended fix**: pin the deployment type in §16.4 and cross-reference in `cost-estimate.md`. Recommended for v1: **Global Standard PAYG** for `gpt-5.2`, with a planned migration to **Provisioned** at Scale tier for predictable latency and PTU cost.

---

### F-18 — Microsoft Cloud Penetration Testing Rules of Engagement · Severity: **Medium**

**Where it appears**: §11.1 ("Penetration test — External vendor (Walmart-procured)"), §17.1 (no item).

**Observations**

All customer-initiated penetration testing of Azure resources must comply with the **Microsoft Cloud Penetration Testing Rules of Engagement** (`https://www.microsoft.com/msrc/pentest-rules-of-engagement`). A vendor-procured test that performs DDoS-style traffic, lateral-movement on shared infrastructure, or testing of multi-tenant services without notification may violate these rules.

**Recommended fix**: add a customer responsibility "C-13: Walmart-procured pen-test vendor will conduct testing within Microsoft's Cloud Penetration Testing Rules of Engagement, and will provide test plan to Microsoft Tech Lead 5 business days before execution."

---

### F-19 — Single canonical region with no paired-region fallback · Severity: **Medium**

**Where it appears**: §16.3 ("Primary: East US 2"), §18.2 A-10.

**Observations**

East US 2 is canonical Azure naming. However:

1. The Azure paired region for East US 2 is **Central US**. Naming the paired region helps planning for Cosmos DB geo-redundant backups (RA-GRS), App Configuration replication, ACR geo-replication, and DR rebuilds.
2. Some Foundry models (especially limited-access ones like `gpt-5.2`) may only be in **Global Standard** deployment — meaning the inference traffic exits East US 2 to a Microsoft-managed pool. Worth noting as a data-residency consideration alongside the DPIA.

**Recommended fix**: state Central US as the paired region and document Global Standard data-flow implications.

---

### F-20 — Azure landing zone alignment · Severity: **Informational**

**Where it appears**: §6, §17.1 C-1.

**Observations**

Walmart Cloud Platform "golden path" alignment is mentioned but the Azure landing-zone (ALZ) topology is not declared. Typical ALZ alignment for a workload like this is:

1. Subscription per environment (dev / staging / prod) under a corp-online-workload management group.
2. Hub-and-spoke networking with workload-injected VNets.
3. Azure Policy / PSRule for Azure governance.

The SOW already mentions "PSRule for Azure" (D-7) which is the right tool for policy compliance.

**Recommended fix** (optional v1, recommended v2): add a one-paragraph ALZ alignment statement referencing the Microsoft Container Apps Landing Zone Accelerator (`https://learn.microsoft.com/azure/cloud-adoption-framework/scenarios/app-platform/container-apps/`).

---

## 4. Recommended Pre-Signature Action Plan

| Priority | Action                                                                                                                                                                 | Severity Covered      | Owner                |
| :------: | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- | -------------------- |
|    1     | Rewrite all references to "Azure OpenAI GPT-5.2 Vision" using Foundry naming; soften assumption A-7 to limited-access reality; declare fallback path                   | F-1 (Critical), F-16  | Tech Lead            |
|    2     | Verify Florence-2 deployment mode (managed compute vs. serverless) and East US 2 availability; capture decision in an ADR; consider Azure AI Vision 4.0 as alternative | F-2                   | Tech Lead + ML Eng   |
|    3     | Resolve "Azure Front Door / APIM" ambiguity; pin SKUs (Front Door Premium; APIM tier if used); reflect choice across §16.1, D-7, diagrams                              | F-3, F-6              | Tech Lead            |
|    4     | Rewrite §18.2 A-10 with a calculated composite SLO and exclusions; align D-12 RTO/RPO to single-region reality                                                         | F-4, F-11             | Tech Lead + Security |
|    5     | Commit to **Azure Cosmos DB for NoSQL** with **hierarchical partition keys** (`/tenantId/.../id`); pin SDK and throughput model in `data-model.md` and ADR             | F-5                   | SDE #2 + Tech Lead   |
|    6     | Add a "SKU / Tier" column to §16.1 with every service pinned; sync `cost-estimate.md` and Bicep parameter files                                                        | F-6, F-12             | DevOps + Tech Lead   |
|    7     | Declare GitHub Actions → Azure auth as **Microsoft Entra workload identity federation (OIDC)**                                                                         | F-10                  | DevOps               |
|    8     | Pin private-networking posture (Private Endpoints on data plane services, ACA workload-profile env in VNet, PNA disabled)                                              | F-15                  | Security + DevOps    |
|    9     | Add Notation key custody, rotation, and Notation trust-policy enforcement to D-8 and C-7                                                                               | F-8                   | Security + DevOps    |
|    10    | Add Pen-test Rules of Engagement clause (new C-13)                                                                                                                     | F-18                  | Security             |
|    11    | Cosmetic fixes: Foundry naming, "Azure Cosmos DB Emulator", ".NET Aspire (inner-loop only)", paired region, App Insights phrasing                                      | F-7, F-13, F-14, F-19 | Tech Lead            |
|    12    | (v2 / Change Order) ALZ alignment statement, multi-region active-passive, Defender for Containers, Provisioned PTU at Scale tier                                       | F-9, F-17, F-20       | Architecture Review  |

---

## 5. Microsoft Learn MCP Evidence (verified 2026-05-14)

Microsoft Learn MCP was available in this VS Code session. The review used MCP
documentation search for the material Critical / High findings and fetched the
most relevant Microsoft Learn pages for ambiguous or high-impact claims.

| Claim area                                                                       | MCP query used                                                                                                                                                                             | Microsoft Learn page(s)                                                                                                                                                                                                                                    | How it affected the finding                                                                                                                                                                                   |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Azure OpenAI / Foundry model naming, image input, and limited-access assumptions | `Azure OpenAI in Azure AI Foundry gpt-5.2 image input limited access model availability Microsoft Learn`; `Azure OpenAI in Azure AI Foundry vision models GPT image input Microsoft Learn` | <https://learn.microsoft.com/azure/foundry/openai/how-to/gpt-with-vision>; <https://learn.microsoft.com/azure/foundry/openai/how-to/reasoning>                                                                                                             | Supports F-1: image input is a model capability, not a separate `GPT-5.2 Vision` SKU; access / availability must be verified through Foundry model availability rather than assumed in the SOW.               |
| Azure AI Foundry / Florence-2 deployment model                                   | `Azure AI Foundry Florence-2 serverless managed compute model deployment Microsoft Learn`                                                                                                  | <https://learn.microsoft.com/azure/foundry/concepts/foundry-models-overview>; <https://learn.microsoft.com/azure/ai-services/computer-vision/whats-new>                                                                                                    | Supports F-2: the SOW must state whether Florence-2 is used through serverless deployment, managed compute, or another Foundry deployment path, and must verify region / billing availability.                |
| Azure Front Door, WAF, and API Management architecture                           | `Azure Front Door WAF protect API Management rate limiting Premium SKU Microsoft Learn`                                                                                                    | <https://learn.microsoft.com/azure/web-application-firewall/afds/afds-overview>; <https://learn.microsoft.com/azure/web-application-firewall/afds/protect-api-hosted-apim-by-waf>; <https://learn.microsoft.com/azure/frontdoor/understanding-pricing>     | Supports F-3 and F-6: `Azure Front Door / APIM` is not an architecture decision; the SOW must state whether Front Door, APIM, or both are deployed and pin the required tiers.                                |
| Azure Cosmos DB for NoSQL partition strategy                                     | `Azure Cosmos DB for NoSQL hierarchical partition keys multitenancy partition strategy Microsoft Learn`                                                                                    | <https://learn.microsoft.com/azure/cosmos-db/hierarchical-partition-keys>; <https://learn.microsoft.com/azure/cosmos-db/hierarchical-partition-keys-unlimited-scale>; <https://learn.microsoft.com/azure/architecture/guide/multitenant/service/cosmos-db> | Supports F-5: the SOW must name Azure Cosmos DB for NoSQL and define tenant-aware hierarchical partition keys for the multi-tenant document model.                                                            |
| Azure Container Apps reliability, zone redundancy, and workload profiles         | `Azure Container Apps reliability zone redundancy SLA workload profiles minimum replicas Microsoft Learn`                                                                                  | <https://learn.microsoft.com/azure/reliability/reliability-container-apps>                                                                                                                                                                                 | Supports F-4, F-11, and F-12: a single-service SLA does not prove the workload composite SLO; zone-redundant ACA design has prerequisites that must be captured in SOW assumptions and customer dependencies. |

### Reference Pages

| Topic                                                       | Reference                                                                                                     |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Vision-enabled chat models in Foundry                       | <https://learn.microsoft.com/azure/foundry/openai/how-to/gpt-with-vision>                                     |
| Azure OpenAI reasoning model availability (`gpt-5.2` etc.)  | <https://learn.microsoft.com/azure/foundry/openai/how-to/reasoning>                                           |
| Foundry deployment types (Global Standard, Provisioned ...) | <https://learn.microsoft.com/azure/foundry/foundry-models/concepts/deployment-types>                          |
| Managed compute vs. serverless deployments                  | <https://learn.microsoft.com/azure/foundry/concepts/foundry-models-overview>                                  |
| Florence foundation model                                   | <https://learn.microsoft.com/azure/ai-services/computer-vision/whats-new>                                     |
| Reliability in Azure Container Apps (zone redundancy, SLA)  | <https://learn.microsoft.com/azure/reliability/reliability-container-apps>                                    |
| Azure Container Apps architecture best practices            | <https://learn.microsoft.com/azure/well-architected/service-guides/azure-container-apps>                      |
| Azure Container Apps Landing Zone Accelerator               | <https://learn.microsoft.com/azure/cloud-adoption-framework/scenarios/app-platform/container-apps/management> |
| WAF on Azure Front Door (rate limiting, managed rules)      | <https://learn.microsoft.com/azure/web-application-firewall/afds/afds-overview>                               |
| Protect APIM with Azure Front Door WAF                      | <https://learn.microsoft.com/azure/web-application-firewall/afds/protect-api-hosted-apim-by-waf>              |
| Azure Front Door pricing tiers                              | <https://learn.microsoft.com/azure/frontdoor/understanding-pricing>                                           |
| Hierarchical partition keys in Azure Cosmos DB              | <https://learn.microsoft.com/azure/cosmos-db/hierarchical-partition-keys>                                     |
| Unlimited logical partition storage with HPK                | <https://learn.microsoft.com/azure/cosmos-db/hierarchical-partition-keys-unlimited-scale>                     |
| Multitenancy and Azure Cosmos DB                            | <https://learn.microsoft.com/azure/architecture/guide/multitenant/service/cosmos-db>                          |
| Microsoft Defender for Containers vulnerability assessment  | <https://learn.microsoft.com/azure/defender-for-cloud/defender-for-containers-introduction>                   |
| Microsoft Defender for Cloud CLI (MDVM-backed)              | <https://learn.microsoft.com/azure/defender-for-cloud/defender-cli-overview>                                  |
| How to read an SLA                                          | <https://learn.microsoft.com/azure/reliability/concept-service-level-agreements>                              |

---

## 6. Version History

| Version | Date       | Author                                | Status | Summary of changes                                                                                                                                                                                                                                            |
| ------- | ---------- | ------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0.1.0   | 2026-05-14 | Microsoft Azure Solution Architecture | Draft  | Initial technical review of Virtual-Mirror-SOW.md v0.1.0                                                                                                                                                                                                      |
| 0.2.0   | 2026-05-14 | Microsoft Azure Solution Architecture | Draft  | Re-ran findings against Virtual-Mirror-SOW.md v0.2.0; governance and DPIA acceptance improvements noted, while Azure service naming, model access, SKU, SLO, Cosmos DB, and networking blockers remain open.                                                  |
| 0.2.1   | 2026-05-14 | Microsoft Azure Solution Architecture | Draft  | Re-ran technical review using updated Skill guidance and Microsoft Learn MCP evidence; added evidence basis / MCP query table and strengthened Foundry model access, deployment-type, Azure Front Door/APIM, Cosmos DB HPK, and ACA zone-redundancy findings. |

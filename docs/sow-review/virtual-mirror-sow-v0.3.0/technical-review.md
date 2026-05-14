# Technical Review - Virtual-Mirror-SOW.md v0.3.0

| Field                     | Value                                                                                                                                                                                                                                                                                                                                    |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Document under review** | [docs/Virtual-Mirror-SOW.md](../../Virtual-Mirror-SOW.md) v0.3.0 (2026-05-14, Draft for internal review)                                                                                                                                                                                                                                 |
| **Review scope**          | Azure service naming accuracy, Foundry and Azure OpenAI model correctness, SKU/tier specificity, single-region reliability, data design, identity, edge/networking, observability, IaC/CI-CD, and operational readiness.                                                                                                                 |
| **Reviewer**              | Microsoft - Azure Solution Architecture Review                                                                                                                                                                                                                                                                                           |
| **Review date**           | 2026-05-14                                                                                                                                                                                                                                                                                                                               |
| **Verdict**               | **Conditional Pass.** v0.3.0 aligns the header and section 1 version fields and improves defect-management language, but the Azure architecture blockers from v0.2.0 remain. The SOW should not be promoted to final signature until Critical and High findings are resolved or converted into explicit ADRs / Change Order assumptions. |
| **Evidence basis**        | Microsoft Learn MCP-backed recheck on 2026-05-14 for Azure OpenAI / Foundry model availability, Azure Front Door Premium + WAF + API Management patterns, Azure Cosmos DB for NoSQL hierarchical partition keys, and Azure Container Apps zone redundancy.                                                                               |
| **Cross-references**      | [compliance-and-security-review.md](compliance-and-security-review.md) - [template-review.md](template-review.md)                                                                                                                                                                                                                        |

---

## 1. v0.3.0 Delta

v0.3.0 fixes one previously observed document-control inconsistency: the top header and section 1 both now show `0.3.0`. However, the Version History still has no `0.3.0` entry, so release traceability remains incomplete. That issue is tracked in the template review and full review because it is primarily a document-control / approval-readiness issue.

The technical substance is largely unchanged. The following phrases remain in the SOW and continue to drive technical risk: `Azure OpenAI GPT-5.2 Vision`, `Florence-2 on Azure AI Foundry`, `Azure Front Door / APIM`, `Azure Cosmos DB`, `RTO < 1 h / RPO < 15 min`, and `Azure Container Apps (multi-AZ, KEDA HTTP scaler) | 2-10 instances`.

---

## 2. Findings Summary

| #    | Finding                                                                                                                                                             |     Severity      | SOW section(s)                                         |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------: | ------------------------------------------------------ |
| F-1  | `Azure OpenAI GPT-5.2 Vision` is not an Azure SKU name; `gpt-5.2` is a Foundry model with image processing capability and limited-access considerations.            |   **Critical**    | Sections 2.2, 3.2, 13.2, 16.1, 17.1, 18.2, Worksheet B |
| F-2  | Florence-2 deployment model and East US 2 serverless availability remain unverified.                                                                                |     **High**      | Sections 2.2, 16.1, 17.1, 18.2                         |
| F-3  | `Azure Front Door / APIM` still hides whether the design uses Front Door only, APIM only, or Front Door Premium in front of APIM.                                   |     **High**      | Section 16.1                                           |
| F-4  | Single-region availability and composite SLO / SLA math are not defended across ACA, Cosmos DB, Service Bus, Front Door, Azure OpenAI, Content Safety, and Foundry. |     **High**      | Sections 5, 16, 18.2, D-10, D-12                       |
| F-5  | The SOW does not specify **Azure Cosmos DB for NoSQL**, hierarchical partition keys, SDK version, throughput mode, or tenant isolation model.                       |     **High**      | Sections 16.1, D-1, D-3, D-5                           |
| F-6  | SKU/tier detail remains incomplete for Front Door, APIM, Key Vault, Service Bus, Blob redundancy, ACR, App Configuration, and Cosmos DB.                            |    **Medium**     | Section 16.1, cost model                               |
| F-7  | Private networking posture is not contractually declared for a biometric-adjacent workload.                                                                         |     **High**      | Sections 16, D-1, D-7                                  |
| F-8  | RTO `< 1 h` and RPO `< 15 min` are over-stated for a single-region v1 unless scoped to zone/instance failures rather than regional outage.                          |     **High**      | D-12, Section 18.2                                     |
| F-9  | ACA zone redundancy prerequisites are not captured: zone-redundant environment at creation, VNet/subnet sizing, workload profile choice, and minimum replica count. |    **Medium**     | Sections 16.1, 16.2, 17.1                              |
| F-10 | GitHub Actions to Azure authentication method is not declared as OIDC workload identity federation.                                                                 |    **Medium**     | D-8, Section 16.1                                      |
| F-11 | Container signing key custody and deploy-time Notation verification are underspecified.                                                                             |    **Medium**     | D-8, C-7                                               |
| F-12 | Azure Monitor / Application Insights terminology should be normalized to Azure Monitor with workspace-based Application Insights and Log Analytics.                 |      **Low**      | Section 16.1                                           |
| F-13 | `.NET Aspire` should be described as local / integration orchestration, not production orchestration.                                                               |      **Low**      | Section 16.1                                           |
| F-14 | Azure landing zone alignment remains implicit: subscription topology, policy assignments, hub/spoke or VNet-injection decisions, and private DNS.                   | **Informational** | Sections 6, 16, 17.1                                   |

---

## 3. Critical and High Findings

### F-1 - Azure OpenAI GPT-5.2 Vision naming and access

Microsoft Learn identifies `gpt-5.2` as a model under Azure OpenAI in Azure AI Foundry / Foundry Models. The Foundry model entry describes text and image processing capability, but the SOW phrase `GPT-5.2 Vision` reads like a separate SKU. Microsoft Learn availability results also show `gpt-5.2` as a limited-access model requiring access workflow, while the SOW assumes GA in East US 2 by Sprint 3.

**Required remediation:** Rename to `Azure OpenAI in Azure AI Foundry - gpt-5.2 with image input` or use a capability-based model clause such as `Azure OpenAI vision-capable model selected in Sprint 1/2 based on availability, quota, and H1 results`. Add a fallback to GA-tier `gpt-5`, `gpt-4.1`, or another approved model if limited access or quota is not available by Sprint 2.

### F-2 - Florence-2 deployment model

The SOW assumes `Florence-2 on Azure AI Foundry | serverless`. Foundry model catalog deployment can mean managed compute, serverless API deployment, Global Standard, Data Zone, Provisioned, or other deployment types depending on model and region. If Florence-2 requires managed compute, the cost estimate, Bicep modules, network controls, and operational support model change materially.

**Required remediation:** Add a Sprint 1 decision gate and ADR to verify Florence-2 deployment type, region, SKU, cost driver, and networking mode. If only image analysis / OCR / captioning is required, evaluate Azure AI Vision Image Analysis as a GA alternative.

### F-3 - Front Door / APIM ambiguity

Microsoft Learn documents Azure Front Door Premium with WAF in front of API Management, including APIM origin restrictions by `X-Azure-FDID` and WAF managed rules. The SOW's slash notation does not say whether APIM is actually in scope. D-7 names Front Door modules but not APIM modules.

**Required remediation:** Choose and document one architecture: Front Door Premium with WAF only, APIM only, or Front Door Premium -> APIM -> ACA. Reflect the same choice in Section 16.1, D-7, cost estimate, diagrams, and Bicep scope.

### F-4 - Composite SLO / SLA realism

Azure Container Apps can support zone redundancy, but the end-to-end service availability is a composite of all dependencies. A single-region design cannot make a regional-outage recovery promise equivalent to a multi-region service. The SOW should separate application SLO, Azure service SLAs, downstream model availability, zone failure behavior, and regional disaster recovery.

**Required remediation:** Add composite SLO math to the resiliency review and SOW. State exclusions clearly, including downstream model outages and customer storefront availability.

### F-5 - Cosmos DB API and partitioning

The correct product for this document model should be **Azure Cosmos DB for NoSQL**. Microsoft Learn recommends hierarchical partition keys for multitenant scenarios where tenant data can exceed the 20-GB logical partition limit or where targeted prefix queries matter.

**Required remediation:** Add a Cosmos DB ADR covering API (`for NoSQL`), container list, hierarchical partition key paths, SDK version (`Microsoft.Azure.Cosmos` supported for HPK), indexing policy, autoscale/provisioned RU strategy, and tenant isolation tests.

### F-7 - Private networking

The service handles shopper photos and biometric-adjacent derived measurements. The SOW does not bind private endpoints, private DNS, managed identities, restricted egress, or public-network-disablement for data and AI services.

**Required remediation:** Add private endpoint / VNet integration requirements for Cosmos DB, Blob Storage, Key Vault, Service Bus, Azure OpenAI / Foundry where supported, and ACA egress. Capture any service that must remain public as an explicit risk acceptance.

### F-8 - RTO and RPO scope

D-12 says `RTO < 1 h, RPO < 15 min` for tenant config. In single-region v1, this is plausible only for narrower failure modes such as instance, deployment, or zone-level issues, not full regional outage.

**Required remediation:** Scope RTO/RPO by failure mode. For regional outage, either add secondary-region rebuild capability or state a more realistic recovery target and Change Order path for active-passive / active-active v2.

---

## 4. Microsoft Learn Evidence Used

| Topic                               | Evidence applied                                                                                                                                                                                     |
| ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Azure OpenAI / Foundry model naming | Microsoft Learn results for Azure OpenAI reasoning models and Foundry Models sold directly by Azure show `gpt-5.2` as a model ID with text and image processing capability and limited-access notes. |
| Front Door + APIM                   | Microsoft Learn documents Azure Front Door Premium with WAF protecting APIs hosted on API Management, including APIM origin restriction and WAF managed rules.                                       |
| Cosmos DB HPK                       | Microsoft Learn recommends hierarchical partition keys for multitenant workloads and scaling beyond the 20-GB logical partition key limit; unique final level such as `/id` is a common pattern.     |
| Azure Container Apps                | Microsoft Learn reliability guidance says zone redundancy must be enabled at environment creation, requires VNet/subnet planning, and should use minimum replicas for zone distribution.             |

---

## 5. Pre-Signature Technical Action Plan

| Priority | Action                                                                                    | Owner                                          |
| -------- | ----------------------------------------------------------------------------------------- | ---------------------------------------------- |
| 1        | Replace `GPT-5.2 Vision` with official Foundry model wording and a fallback model clause. | Microsoft ML Eng + Customer Azure account team |
| 2        | Resolve Florence-2 deployment type and cost model.                                        | Microsoft ML Eng                               |
| 3        | Decide Front Door / APIM architecture and update D-7, diagrams, and costs.                | Microsoft Tech Lead + Customer Platform Eng    |
| 4        | Add Cosmos DB for NoSQL HPK and RU strategy ADR.                                          | Microsoft Tech Lead                            |
| 5        | Add private networking requirements and exceptions.                                       | Microsoft DevOps + Security Eng                |
| 6        | Re-scope SLO, RTO, and RPO by failure mode.                                               | Microsoft Architect + Customer Platform Eng    |

---

## 6. Version History

| Version | Date       | Author                                         | Status | Summary of changes                                                                                                                                                                |
| ------: | ---------- | ---------------------------------------------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|   0.3.0 | 2026-05-14 | Microsoft - Azure Solution Architecture Review | Draft  | Initial technical review for SOW v0.3.0; confirms version header alignment, carries forward v0.2.0 Azure blockers, and revalidates core issues with Microsoft Learn MCP evidence. |

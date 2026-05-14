# Technical Review - OLR-ControlRoom-SOW_Fictitious.docx v1.1

| Field | Value |
| ----- | ----- |
| **Document under review** | [docs/Inputs/OLR-ControlRoom-SOW_Fictitious.docx](../../Inputs/OLR-ControlRoom-SOW_Fictitious.docx) v1.1 - Amended; Draft pending Customer and Microsoft signature |
| **Review scope** | Azure service naming, AI / Foundry / Azure OpenAI deployment assumptions, OT/edge architecture, AKS/Karpenter, data plane, SLO/SLA realism, private networking, observability, and technical evidence traceability. |
| **Reviewer** | Microsoft ISD - Azure Technical Review |
| **Review date** | 2026-05-14 |
| **Evidence basis** | Microsoft Learn MCP-backed review. |
| **Verdict** | **Conditional Pass.** The architecture is directionally credible for an OT-adjacent industrial AI platform, but several service names, deployment models, capacity/SLA assumptions, and external technical baselines must be made explicit before signature. |
| **Cross-references** | [compliance-and-security-review.md](compliance-and-security-review.md) - [template-review.md](template-review.md) |

---

## 1. Severity Legend

| Severity | Definition | Action |
| :------: | ---------- | ------ |
| **Critical** | Technically incorrect, undeployable, or materially misleading. | Must fix before signature. |
| **High** | Ambiguity hides a decision that drives SLA, cost, security, compliance, or scope. | Fix before signature or capture as ADR / assumption. |
| **Medium** | Correct service pattern but missing SKU, region, tier, version, or operational detail. | Resolve in Mobilize / Sprint 0. |
| **Low** | Nomenclature, consistency, or documentation hygiene issue. | Track for next draft. |
| **Informational** | Valid pattern or useful improvement. | No blocking action. |

---

## 2. Findings Summary

| # | Area | Finding | Severity | SOW section(s) |
| :-: | ---- | ------- | :------: | -------------- |
| T-1 | Technical baseline | Schedule H is stated as authoritative but not attached, versioned, or reviewable in this package. | **Critical** | §2.3, §22 |
| T-2 | Azure service naming | Several names are shorthand or legacy: AOAI, Monitor + LA, Cosmos Gremlin, Front Door / APIM roles. | **High** | §4, §16, Glossary |
| T-3 | Foundry / Azure OpenAI | PTU reservations are referenced but deployment type, model family/version, region, quota, and capacity availability are not specified. | **High** | §5, §16, §18, §20 |
| T-4 | Azure IoT Operations | AIO at edge is plausible, but production prerequisites, Arc-enabled Kubernetes distribution, offline behavior, and layered-network constraints are not specified. | **High** | §4, §7, §16 |
| T-5 | AKS + Karpenter | AKS + Karpenter should be named as AKS node auto-provisioning (NAP) or a BYO Karpenter design; constraints are absent. | **Medium** | §4, §16 |
| T-6 | Edge/API perimeter | Front Door, APIM Premium, Azure Firewall Premium, ExpressRoute, and OT-DMZ roles need a concrete request path and trust-boundary diagram. | **High** | §4, §16 |
| T-7 | Data plane | OSDU + ADX + Fabric + Event Hubs + Event Grid + Service Bus is plausible but over-broad without ownership, data-contract, and duplication boundaries. | **High** | §4, §16 |
| T-8 | Cosmos DB Gremlin | Cosmos DB for Gremlin is valid, but use as safety graph needs partitioning, RU, traversal-limit, and OLTP-vs-OLAP constraints. | **Medium** | §4, §16 |
| T-9 | SLO / SLA | SLOs are listed by ID only; no targets or measurement definitions are present in the SOW. | **High** | §16.3 |
| T-10 | Observability | Monitor, Log Analytics, Sentinel, Grafana, and FinOps are named but ingestion volumes, retention, alert ownership, and cost controls are incomplete. | **Medium** | §13, §16 |
| T-11 | Private networking | OT no-write controls are good, but public network access posture, Private Link, DNS, egress, and identity-to-network controls need specification. | **High** | §16.4 |
| T-12 | Cost model | $4.8M Y1 BOM is too high-level for the named high-cost services. | **High** | §20.2 |

---

## 3. Detailed Findings

### T-1 - Schedule H is the technical baseline but is not reviewable - Severity: **Critical**

The SOW says the executed Schedule H PDF prevails on technical content and includes 9 ADRs, 28 components, 37 BOM rows, 60 WBS leaves, 17 NFRs, 7 SLOs, 5 OT controls, and the hostile-probe console. That may be acceptable contractually, but only if Schedule H is attached, immutable, and signed with the SOW.

**Required fix:** Attach Schedule H, give it a version/hash/date, and add a signed-baseline rule. The live OLR site must remain non-binding reference material unless changed through §12.

### T-2 - Azure service names need current official names - Severity: **High**

The SOW uses several shorthand terms: `AOAI`, `Monitor + LA`, `Cosmos Gremlin`, `Foundry RAG`, `AI Search`, `Front Door`, `AIO`, and `AKS + Karpenter`. These are recognizable to practitioners but should be expanded to official product names in the technology requirements table and glossary.

**Required fix:** Use current names such as Azure OpenAI in Azure AI Foundry Models / Microsoft Foundry, Azure Monitor, Log Analytics workspace, Azure Cosmos DB for Apache Gremlin, Azure AI Search, Azure Front Door Premium, Azure API Management Premium, Azure IoT Operations, and AKS node auto-provisioning where intended.

### T-3 - Foundry / Azure OpenAI PTU assumptions are incomplete - Severity: **High**

The SOW makes AOAI PTU reservations a customer responsibility and cost driver, but does not name the model, model version, deployment type, acceptable regions, PTU count, capacity reservation strategy, or fallback path if capacity is unavailable. Microsoft Learn states PTU quota is regional and quota does not guarantee capacity; capacity is allocated at deployment time.

**Required fix:** Add a model deployment table with model family/version, deployment type (Global Provisioned, Data Zone Provisioned, or Regional Provisioned), region(s), PTU estimate, quota owner, capacity check date, fallback model/deployment type, and benchmark plan.

### T-4 - Azure IoT Operations edge prerequisites are underspecified - Severity: **High**

Azure IoT Operations is the right conceptual service for Arc-enabled Kubernetes industrial edge data flows. The SOW should specify the supported Kubernetes distribution, Arc onboarding, custom locations, workload identity, layered network design, offline behavior, MQTT/OPC UA connector responsibilities, and Customer-owned edge hardware readiness.

**Required fix:** Add an AIO deployment prerequisites table by site, including cluster platform, OS, Arc state, network path, certificates, secrets, OPC UA / historian connector, outbound allow-list, and offline/reconnect behavior.

### T-5 - AKS + Karpenter terminology needs precision - Severity: **Medium**

Microsoft Learn describes AKS node auto-provisioning as automatically deploying and managing Karpenter on AKS clusters. If the SOW means managed NAP, say so. If it means self-managed Karpenter, that is a different operational responsibility and support model.

**Required fix:** Replace `AKS + Karpenter` with either `AKS node auto-provisioning (NAP)` or a specific BYO Karpenter design. Add constraints: managed identity, Standard Load Balancer, no Windows nodes, no cluster autoscaler coexistence, and CNI/subnet requirements where relevant.

### T-6 - Edge/API perimeter lacks a concrete flow - Severity: **High**

The SOW names Azure Front Door Premium, Azure API Management Premium, Azure Firewall Premium, ExpressRoute, AKS, AIO, and OT-DMZ. It does not show which traffic is internet-facing, which APIs are internal, where WAF policies apply, whether origins use Private Link, and how APIM, Front Door, and Firewall responsibilities differ.

**Required fix:** Add request-flow diagrams or a table: user/engineer/executive ingress, API ingress, OT-edge egress, cloud-to-OT deny controls, private endpoints, DNS, WAF policy, APIM policy, and egress inspection.

### T-7 - Data plane is plausible but needs ownership boundaries - Severity: **High**

OSDU, ADX, Fabric, Event Hubs, Event Grid, and Service Bus can all be appropriate, but the SOW does not define which system is source of truth for each domain, which services are streaming vs. eventing vs. command/workflow, and where semantic layer ownership lives.

**Required fix:** Add a data-contract and data-plane responsibility matrix: source, ingestion service, canonical schema, storage/analytics target, freshness SLO, owner, retention, and consumer.

### T-8 - Cosmos DB for Apache Gremlin use needs scale constraints - Severity: **Medium**

Azure Cosmos DB for Apache Gremlin is a valid managed graph database, but it is OLTP-oriented and has traversal and partitioning constraints. The safety graph is out of scope under CR, but the service still appears in the AI plane / stack pattern.

**Required fix:** Either remove it from in-scope stack patterns or define its exact retained use. If retained, specify partition key, RU/s or autoscale model, traversal limits, graph data model, and whether analytical graph work belongs in Microsoft Fabric Graph instead.

### T-9 - SLOs are not measurable from the SOW - Severity: **High**

The SOW lists SLO-01..07 but says targets and measurement methods are in Schedule H. Without attached Schedule H, a signer cannot verify latency, availability, RPO, RTO, freshness, or DR pass/fail criteria.

**Required fix:** Bring minimum target values and measurement definitions into §16.3 or attach Schedule H before signature. State explicitly that AKS SLA only covers API server uptime and does not equal workload availability.

### T-10 - Observability and SIEM cost controls need sizing - Severity: **Medium**

Azure Monitor is the right unified observability platform and supports Log Analytics, Sentinel, Defender for Cloud, Application Insights, Prometheus/OpenTelemetry, and agent monitoring. The SOW should size ingestion volumes, retention, alert ownership, DCR filtering, and FinOps controls, especially because Sentinel + Log Analytics 2x ingest is a named risk.

**Required fix:** Add monitoring architecture and cost guardrails: workspace topology, retention, daily ingest budget, DCR filters, Sentinel rule packs, alert owners, dashboard list, and escalation thresholds.

### T-11 - Private networking posture needs explicit defaults - Severity: **High**

The SOW has strong OT egress denial controls, but does not state default public network access posture for Azure PaaS resources, use of private endpoints, managed identity, Key Vault network rules, or DNS split-horizon requirements.

**Required fix:** Add an Azure networking baseline: private endpoints for data/AI resources where supported, public network access disabled by default or exception-based, managed identities, Key Vault Premium/HSM access model, DNS zones, and egress inspection.

### T-12 - BOM cost guardrail needs service-level traceability - Severity: **High**

The Year-1 BOM envelope is $4.8M after CR-14, but high-cost services such as AOAI/PTU, Fabric F64, Power BI Premium, Sentinel ingestion, ExpressRoute, Firewall Premium, AKS, AIO edge footprint, and ADX are not itemized in the SOW.

**Required fix:** Add a service-level BOM summary or attach Schedule B before signature, including quantity, SKU/tier, region, owner, unit-cost driver, and cost guardrail metric.

---

## 4. Pre-Signature Action Plan

| Priority | Action | Owner |
| :------: | ------ | ----- |
| 1 | Attach and freeze Schedule H; bring minimum SLO targets into the SOW. | Microsoft SA + Customer EA |
| 2 | Add official Azure service-name / SKU / region table. | Microsoft SA |
| 3 | Add Foundry/AOAI deployment table with PTU capacity validation. | Microsoft AI Engineer + Customer Platform |
| 4 | Add AIO site prerequisites and OT layered-network model. | Edge/OT Engineer + Customer OIMS |
| 5 | Add APIM/Front Door/Firewall/Private Link traffic-flow diagram. | Microsoft SA + Security Engineer |
| 6 | Add service-level BOM summary and FinOps thresholds. | Engagement Lead + Customer Finance/Platform |

---

## 5. Microsoft Learn MCP Evidence

| Claim area | MCP query used | Microsoft Learn page(s) | How it affected the finding |
| ---------- | -------------- | ------------------------ | --------------------------- |
| Azure IoT Operations | `Azure IoT Operations Arc-enabled Kubernetes overview Azure IoT Operations` | https://learn.microsoft.com/azure/iot-operations/overview-iot-operations | Confirmed AIO is an edge data plane on Arc-enabled Kubernetes, supports MQTT/OPC UA-style industrial scenarios, and has offline/degradation considerations. Informed T-4. |
| AKS + Karpenter | `Azure Kubernetes Service Karpenter Node Auto Provisioning overview Microsoft Learn` | https://learn.microsoft.com/azure/aks/node-auto-provisioning | Confirmed managed AKS NAP terminology and constraints. Informed T-5. |
| Foundry PTU | `Azure OpenAI provisioned throughput units PTU deployment types Azure AI Foundry Microsoft Learn` | https://learn.microsoft.com/azure/foundry/openai/concepts/provisioned-throughput | Confirmed PTU deployment types, regional quota, and capacity-not-guaranteed caveat. Informed T-3. |
| Azure AI Search / RAG | `Azure AI Foundry agent RAG Azure AI Search Azure Machine Learning Content Safety Microsoft Learn` | https://learn.microsoft.com/azure/search/search-what-is-azure-search | Confirmed Azure AI Search supports RAG / agentic retrieval and enterprise security patterns. Informed T-7 / AI architecture notes. |
| Cosmos DB Gremlin | `Azure Cosmos DB for Apache Gremlin Microsoft Learn graph database Gremlin API` | https://learn.microsoft.com/azure/cosmos-db/gremlin/overview | Confirmed official name and OLTP graph positioning; highlighted NoSQL/Fabric Graph alternatives for high-scale/OLAP. Informed T-8. |
| Front Door | `Azure Front Door Premium Web Application Firewall Azure API Management Premium internal VNet Microsoft Learn` | https://learn.microsoft.com/azure/frontdoor/front-door-overview | Confirmed Front Door edge/WAF/global ingress role and Private Link origin option. Informed T-6. |
| API Management | `Azure Front Door Premium Web Application Firewall Azure API Management Premium internal VNet Microsoft Learn` | https://learn.microsoft.com/azure/api-management/api-management-key-concepts | Confirmed APIM gateway, policy, rate limit, auth, and observability roles. Informed T-6. |
| AKS SLA | `Azure Kubernetes Service SLA availability zones uptime SLA Microsoft Learn` | https://learn.microsoft.com/azure/aks/uptime-sla | Confirmed AKS pricing tiers and API server uptime SLA scope. Informed T-9. |
| Azure Monitor | `Azure Monitor Application Insights Log Analytics workspace Microsoft Sentinel Microsoft Learn` | https://learn.microsoft.com/azure/azure-monitor/overview | Confirmed Azure Monitor unified observability, Log Analytics, Sentinel, Defender, OTel, Prometheus, and agent monitoring. Informed T-10. |
| Responsible AI | `Azure OpenAI data privacy abuse monitoring no training enterprise data Microsoft Learn` and Foundry RAI fetch | https://learn.microsoft.com/azure/ai-foundry/responsible-use-of-ai-overview | Confirmed Discover / Protect / Govern framing for AI systems. Informed cross-reference to compliance review. |

---

## 6. Version History

| Version | Date | Author | Status | Summary of changes |
| ------: | ---- | ------ | ------ | ------------------ |
| 1.0 | 2026-05-14 | Microsoft ISD - Azure Technical Review | Draft | Initial Microsoft Learn MCP-backed technical review for OLR Control Room SOW v1.1. |
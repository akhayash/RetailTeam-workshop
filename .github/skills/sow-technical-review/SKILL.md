---
name: sow-technical-review
description: "Perform an Azure architecture and technical review of a Statement of Work (SOW) for AI / cloud / data-handling engagements. Produces a structured Markdown review at docs/sow-review/<sow-slug>-<version>/technical-review.md covering Azure service naming accuracy, solution architecture correctness, SKU/tier specificity, SLO/SLA realism, multi-tenant data design, identity, private networking, observability, IaC/CI-CD, regional availability, and AI model deployment correctness. USE WHEN the user asks to technically review, Azure-architecture review, solution-architecture review, validate Azure services, check Microsoft Learn service names, or assess whether an SOW proposes the right Azure solution. DO NOT USE FOR compliance/legal review alone (use sow-compliance-security-review) or general code review."
---

# SOW Technical Review

This skill produces a rigorous, evidence-based technical review of a Statement
of Work (SOW) from an Azure Solution Architect perspective. The output is a
single Markdown file modeled on
[`docs/sow-review/technical-review.md`](../../../docs/sow-review/technical-review.md),
which is the canonical reference example for tone, structure, severity model,
and depth.

The review must verify that the SOW uses correct Microsoft service names,
proposes the right Azure services and deployment models, and does not hide
material architecture decisions behind ambiguous wording.

## When to use

Trigger this skill when the user asks to:

- Review an SOW from an Azure architect / solution architect perspective.
- Validate whether the proposed Azure architecture is technically correct.
- Check that Azure service names, SKUs, tiers, and deployment models match
  current Microsoft Learn documentation.
- Assess SLO/SLA realism, regional availability, failover posture, or cost
  assumptions in a cloud proposal.
- Review an AI / Foundry / Azure OpenAI architecture in an SOW.
- Produce a pre-signature technical go / no-go assessment with Critical / High
  issues.

Do **not** use this skill for: compliance-only review; legal contract review;
general code review; threat modelling from scratch. Use
`sow-compliance-security-review` for regulatory, privacy, and legal/compliance
gaps.

## Inputs you need

Before producing the review, confirm or discover:

1. **The SOW under review** — file path, version, status (draft / final / signed).
2. **Architecture artefacts** that the SOW should align with, e.g.:
   - Solution architecture
   - Diagrams
   - Cost estimate
   - Resiliency review
   - Decision register / ADRs
   - Data model / OpenAPI contract
   - Risk register
3. **Azure and AI service claims** in the SOW, including model names,
   deployment types, regions, SLOs, SKUs, and pricing claims.
4. **Reviewer identity** and review date.

If any input is missing and cannot be inferred from the repository, ask the user
once with a concise list. Do not fabricate values for the document header.

## Output naming policy

Place review outputs in an SOW-specific folder so the reviewed SOW is clear from
the path:

1. Derive `<sow-slug>` from the SOW filename without extension:
  - Lowercase.
  - Replace spaces and underscores with hyphens.
  - Remove characters other than `a-z`, `0-9`, and `-`.
  - Collapse repeated hyphens.
2. Derive `<version>` from the SOW header field named `Version`.
  - Preserve the leading `v` if present; otherwise prefix `v`.
  - Normalize dots as dots, e.g. `0.1.0` -> `v0.1.0`.
  - If no version is present, use the SOW document date as `yyyy-mm-dd`.
3. Write the output to:
  - `docs/sow-review/<sow-slug>-<version>/technical-review.md`

If the same SOW name and version are reviewed again, update / overwrite the same
file in that folder. Do not create timestamped duplicates unless the user asks
for archival snapshots.

## Required evidence sources

For all service-name, SKU, tier, model, region, and SLA claims, use official
Microsoft Learn / Microsoft documentation where available.

**Microsoft Learn MCP requirement**: Before writing or updating the technical
review, you MUST verify that the Microsoft Learn MCP tools are available by
calling the Microsoft documentation tool activation flow. If the MCP tools are
available, you MUST use `microsoft_docs_search` and, for high-value or ambiguous
results, `microsoft_docs_fetch` to ground the review. Do not rely only on
memory, old links, repo notes, or general web search for Microsoft service,
model, SKU, tier, region, or SLA claims.

If Microsoft Learn MCP is unavailable or fails, state that explicitly in the
technical review header and in the Microsoft Learn evidence section, then use
official Microsoft documentation through the best available fallback. A review
that did not use MCP must be labeled **MCP not used — fallback evidence** and
must not claim MCP-backed verification.

At minimum, verify with Microsoft Learn MCP:

- Azure OpenAI / Microsoft Foundry model names, model capabilities, access
  status, and regional availability.
- Foundry deployment type terminology (Global Standard, Standard, Provisioned,
  Data Zone, Batch, Developer, managed compute, serverless deployment).
- Azure Container Apps reliability, zone redundancy prerequisites, and SLA
  conditions.
- Azure Front Door, Azure Web Application Firewall, and Azure API Management
  SKU/tier distinctions.
- Azure Cosmos DB API name, hierarchical partition key guidance, and SDK
  requirements.
- Azure Monitor / Application Insights current naming.
- Microsoft Defender for Cloud / Defender for Containers and supply-chain
  scanning guidance, where relevant.

Record the MCP queries and documentation references in a dedicated section at
the end of the review. Do not cite blog posts when Microsoft Learn has an
authoritative page.

The technical review MUST include an evidence table like:

| Claim area | MCP query used | Microsoft Learn page(s) | How it affected the finding |
| ---------- | -------------- | ----------------------- | --------------------------- |
| Azure OpenAI / Foundry model naming | `<query>` | `<URL>` | Confirmed / refuted / constrained SOW claim |

## Procedure

Follow these steps in order.

### Step 1 — Read the SOW end-to-end

Read the entire SOW before writing anything. Capture:

- Azure services named in the stack
- AI model names, deployment models, and access / quota assumptions
- Edge / API gateway / WAF language
- Runtime, orchestration, IaC, CI/CD, and observability choices
- Data stores and multi-tenant isolation model
- SLOs, SLAs, RTO, RPO, load targets, and chaos targets
- Region and availability-zone assumptions
- Customer responsibilities and dependencies
- Acceptance criteria and deliverable IDs

### Step 2 — Read architecture cross-references

Read every architecture artefact linked from the SOW. Extract:

- Proposed logical and physical architecture
- Existing ADRs and unresolved decisions
- Cost drivers and SKU assumptions
- Resiliency posture and degradation paths
- Network topology and private-link assumptions
- Data model and partition-key design
- Any inconsistencies with the SOW

### Step 3 — Verify Microsoft service and model names

For each named Microsoft / Azure service or AI model, classify it as:

- **Correct** — current official name and deployment model.
- **Imprecise** — recognizable but missing qualifier, SKU, tier, or API.
- **Incorrect** — not an actual SKU/model/service name, or misleading.
- **Ambiguous** — slash notation or generic shorthand hides a design decision.

Pay special attention to:

- Azure OpenAI in Microsoft Foundry / Azure AI Foundry naming.
- Vision-enabled model names. Do not invent names like "GPT-x Vision" unless
  Microsoft Learn exposes that exact SKU.
- Foundry model deployment type (managed compute vs. serverless vs. Azure
  OpenAI deployment).
- Azure Cosmos DB API flavor (`for NoSQL`, `for MongoDB`, etc.).
- Azure Front Door vs. Azure API Management vs. Application Gateway.
- Azure Monitor vs. Application Insights.
- .NET Aspire as local / integration orchestration, not production runtime.

### Step 4 — Apply the technical review checklist

Produce findings across these categories:

1. **Executive summary** — verdict (Pass / Conditional Pass / Fail), strengths,
   and top technical blockers.
2. **Severity legend** — Critical / High / Medium / Low / Informational.
3. **Findings summary** — compact table of all findings.
4. **Detailed findings**:
   - Azure service naming accuracy
   - AI / Foundry / Azure OpenAI model correctness
   - SKU and tier specificity
   - SLO/SLA and composite availability realism
   - RTO/RPO and BCDR realism
   - Multi-tenant data design and Cosmos DB partition strategy
   - Identity and keyless authentication
   - Edge, WAF, API gateway, and rate limiting design
   - Private networking and egress posture
   - Observability and diagnostics
   - IaC and CI/CD supply chain
   - Regional availability and paired-region assumptions
   - Cost-model traceability
5. **Pre-signature action plan** — prioritized by severity and owner.
6. **Microsoft Learn MCP evidence** — MCP queries, fetched Microsoft Learn
  pages, official sources used, and how each source affected the finding.
7. **Version history**.

### Step 5 — Severity rules

Use the following severity model:

|     Severity      | Definition                                                                                                                               | Action                                              |
| :---------------: | ---------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
|   **Critical**    | Naming or design is technically incorrect, will fail Azure validation/deployment, or materially misrepresents what Azure provides today. | Must fix before signature.                          |
|     **High**      | Ambiguity hides a decision that drives SLA, cost, or compliance. Risks downstream rework or scope creep.                                 | Must fix before signature or capture as an ADR.     |
|    **Medium**     | Service is named correctly but SKU/tier/region/SDK detail is missing or imprecise.                                                       | Resolve in Sprint 1 architecture finalisation.      |
|      **Low**      | Stylistic, alignment, or consistency issue with current Microsoft Learn nomenclature.                                                    | Track for next document revision.                   |
| **Informational** | Reasonable practice but worth flagging as an Azure-native alternative or upgrade path.                                                   | No action required; consider for v2 / Change Order. |

### Step 6 — Write the review document

Write the review to `docs/sow-review/<sow-slug>-<version>/technical-review.md`
unless the user asks for a different filename. Create the folder if it does not
exist. If the same SOW name and version are reviewed again, update the existing
file in that folder.

The first table at the top of the document MUST capture:

| Field                     | Value                                                  |
| ------------------------- | ------------------------------------------------------ |
| **Document under review** | Relative link + version + status                       |
| **Review scope**          | Technical areas assessed                               |
| **Reviewer**              | Reviewer name or team                                  |
| **Review date**           | ISO date                                               |
| **Verdict**               | Pass / Conditional Pass / Fail with one-line rationale |
| **Cross-references**      | Relative links to architecture artefacts               |

### Step 7 — Self-check before returning

Before declaring the review complete, verify:

- [ ] Every Azure service named in the SOW appears in the technical analysis.
- [ ] Every AI model name is verified against Microsoft Learn / Foundry docs.
- [ ] Every slash-separated service choice is resolved or flagged.
- [ ] Every SLO/SLA/RTO/RPO claim is either justified or flagged.
- [ ] Every cost-sensitive service has a SKU/tier recommendation.
- [ ] Cosmos DB API and partition-key strategy are addressed.
- [ ] Private networking and public network access posture are addressed.
- [ ] GitHub Actions to Azure authentication method is addressed.
- [ ] Microsoft Learn MCP tools were activated and used, or explicit fallback
  evidence is documented.
- [ ] Microsoft Learn MCP queries are listed.
- [ ] Microsoft Learn references are listed with URLs.
- [ ] Each Critical / High technical finding cites at least one Microsoft Learn
  MCP-backed source or explicitly states why no authoritative source exists.

If any box is unchecked, fix the review before returning.

## Style & tone

- Write in clear, neutral, Azure-architecture English.
- Use current Microsoft product names and service terminology.
- Cite specific SOW sections, deliverables, assumptions, and risks.
- Use tables for summaries and action plans.
- Do not invent Microsoft service names, SKUs, model names, or SLA numbers.
- If Microsoft Learn cannot confirm a claim, mark it as an assumption to verify.

## Anti-patterns to avoid

- **Do not accept shorthand as architecture.** "Front Door / APIM" must be
  resolved into one or both services.
- **Do not treat model capability as a SKU.** Image input support does not make
  a separate "Vision" model unless Microsoft names it that way.
- **Do not treat a single service SLA as the workload composite SLO.** Account
  for every dependency in the request path.
- **Do not leave SKU/tier unspecified** for services that materially affect
  availability, cost, or private networking.
- **Do not recommend preview features for production** unless the SOW explicitly
  accepts preview risk and no-SLA implications.

## Example reference

The canonical example output of this skill is:
[`docs/sow-review/technical-review.md`](../../../docs/sow-review/technical-review.md).
Mirror its section ordering, table styles, severity model, and pre-signature
action plan structure.

## Output

A single Markdown file at
`docs/sow-review/<sow-slug>-<version>/technical-review.md` with these top-level
sections, in order:

1. Header table
2. Severity legend
3. Findings summary
4. Detailed findings
5. Recommended pre-signature action plan
6. Microsoft Learn MCP evidence
7. Version history

# Deliverable 1 | Three Architecture Concept Diagrams

**Industry**: Retail — Online Apparel
**Use case**: AI Clothing Fit Assessment Agent
**Date**: 2026-05-14
**Status**: Workshop deliverable

> *Show how agentic AI transforms workflows, decisions, safety, reliability, or optimization — appropriate to your industry.*

---

## Industry Context

Online apparel returns run at **25–40%**, and the dominant driver is fit uncertainty. Shoppers cannot judge how a garment will fit before purchasing, so they over-order, return, and lose trust. Returns are a margin killer (logistics, restocking, write-offs) and a sustainability problem (transport emissions, landfill apparel).

**Walmart-specific reality**: Walmart is the 3rd-largest U.S. apparel e-commerce retailer ($14.7B online apparel revenue, 2024). With an estimated 24–26% online clothing return rate and 53% of those driven by fit/sizing issues, the annual cost of fit-related returns runs into hundreds of millions. Walmart already invested in **Zeekit** (virtual try-on / visualization) — VirtualMirror complements this with **measurement-based fit confidence** ("will it fit?" vs "how does it look?"). The architecture integrates with Walmart's multi-hybrid cloud (Azure is a strategic partner at $500M+ annual spend), their Kubernetes-native internal developer platform, and existing catalog/PIM systems managed by Walmart Global Tech's 25,000+ engineering organization.

The three architecture concepts below show **how agentic AI transforms the retail value chain** — from the shopper's purchase decision, to the privacy-conscious home shopper's on-device recommendation, to the merchandiser's catalog and inventory strategy — while keeping **humans accountable** for the final decision in every loop.

| Dimension                  | Where agentic AI transforms it                                                                                 |
|----------------------------|----------------------------------------------------------------------------------------------------------------|
| **Workflows**              | Shoppers stop hunting size charts; privacy-conscious buyers get fit guidance without uploading photos; merchandisers stop guessing |
| **Decisions**              | Fit recommendations are confidence-scored, per-area, and explainable — not a single number                     |
| **Safety**                 | Photos purged in < 60s for cloud paths; opaque IDs; content safety filtering; Concept B images never leave the smartphone |
| **Reliability**            | Three-tier AI pipeline with graceful degradation; circuit breakers; 99.9% availability SLO                     |
| **Optimization**           | 20–30% reduction in fit-driven returns; better size curves; less overstock; lower emissions                    |

Anchoring artifacts: [Problem statement](docs/Sessions/Problem-statement.md) · [Product definition](docs/Sessions/Product-definition.md) · [Solution architecture](docs/architecture/solution-architecture.md) · [Risk register](docs/architecture/risk-register.md)

---

## A. Cloud-Centric Platform Architecture

> Modern data foundation, scalable services, governed AI/ML platform, integration backbone.

This is the **primary v1 implementation concept** — a cloud-native, multi-tenant API service on Azure with managed AI services, serverless container hosting, and zero-secret access via Managed Identity. The shopper's storefront calls a single API and gets back a confidence-scored fit recommendation in under five seconds.

```mermaid
graph TD
    subgraph "Concept A: Cloud-Centric Platform"
        Frontend["Retail Frontend<br/>(B2B OAuth)"] -->|HTTPS| API["Azure Container Apps<br/>VirtualMirror API (.NET 8)<br/>2-10 replica auto-scale<br/>managed identity"]
        API --> AI["Azure AI Plane<br/>• Florence-2 (T1)<br/>• Content Safety<br/>• OpenAI GPT-5.2<br/>• AI Foundry (v2)"]
        API --> Cosmos["Cosmos DB<br/>(multi-tenant)"]
        API --> Blob["Blob Storage<br/>(60s TTL)"]
        API --> Bus["Service Bus<br/>(async queue)"]
        API --> KV["Key Vault<br/>(secrets)"]
        API --> Monitor["Azure Monitor"]
    end
```

### How agentic AI transforms the shopper's workflow

> "An AI copilot that assists the **online shopper** by synthesizing **a single photo and self-reported height into body measurements**, flagging **low-confidence predictions and poor fit areas**, and recommending **the best size with per-area fit breakdown** — while the **shopper retains accountability** for the purchase decision."

| Dimension        | Concept A capability                                                                                                  |
|------------------|------------------------------------------------------------------------------------------------------------------------|
| **Workflow**     | Fit assessment embedded in the product detail page — no separate tool, no app install, no size chart hunting          |
| **Decision**     | 5-point fit scale per body area (chest, waist, hips, inseam, shoulders) + overall recommendation + confidence score   |
| **Safety**       | Photo purged within 60s (TTL + explicit delete); opaque `shopperRef`; Content Safety filter; no biometrics persisted  |
| **Reliability**  | Three-tier AI pipeline (Florence-2 → GPT-5.2 → Foundry) with confidence gating; degrades to size-chart fallback on failure |
| **Optimization** | Target: 20–30% reduction in fit-driven returns; $2–6M annual savings for a mid-size retailer; < 5s p95 latency        |

### Tradeoffs

- **Gain**: Fastest time-to-market, lowest ops burden, fully managed services, API-first integration with any storefront
- **Accept**: Azure vendor lock-in; single-region v1; cloud network dependency; measurement accuracy band of ±2–4 cm

Full detail: [solution-architecture.md § Concept A](docs/architecture/solution-architecture.md#concept-a-cloud-centric-platform-architecture)

---

## B. Edge + AI Agent-Enabled Operations

> Decisioning at the edge, agentic workflows, human-in-the-loop control, latency- and safety-aware patterns.

This concept extends the platform into an **at-home, smartphone-native experience** embedded in the retailer's shopping app. Pose detection and measurement extraction run **on the shopper's phone** so raw body images never traverse the network. Only **derived measurements** are sent to the cloud VirtualMirror API for garment comparison, and the **shopper stays in the loop** by deciding whether to trust the recommendation.

```mermaid
graph TD
    subgraph "Concept B: Edge + AI Agent Operations"
        Phone["Shopper Smartphone<br/>Native shopping app + SDK<br/>• on-device pose detection<br/>• local measurement extraction<br/>• privacy: raw images stay local"]
        Backend["VirtualMirror API (Cloud Backend)<br/>• garment fit comparison<br/>• model distribution metadata<br/>• aggregated mobile analytics"]
        Phone -->|"derived measurements only<br/>(not raw images)"| Backend
    end
    Note["Human-in-the-loop: AI recommends → shopper decides whether to trust, buy, or retake locally"]
```

### How agentic AI transforms the home shopper's workflow

> "An AI copilot that assists the **privacy-conscious home shopper** by synthesizing **on-device body measurements and cloud garment fit data**, flagging **poor fit areas and low-confidence predictions**, and recommending **the best size with explainable alternatives** — while the **shopper retains accountability** for whether to trust the recommendation and complete the purchase."

| Dimension        | Concept B capability                                                                                                           |
|------------------|--------------------------------------------------------------------------------------------------------------------------------|
| **Workflow**     | Shopper opens the retailer's native app at home, captures a photo with the smartphone camera, and gets a fit recommendation without uploading the raw image |
| **Decision**     | Recommended size + alternatives are presented with confidence; shopper decides whether to trust it, retake locally, or use the size chart |
| **Safety**       | **Strongest privacy posture**: raw images never leave the smartphone; only derived measurements are transmitted to the cloud |
| **Reliability**  | On-device measurement extraction works offline; only the garment comparison step requires cloud connectivity                  |
| **Optimization** | Sub-second measurement extraction on-device; lower upstream data transfer; broader adoption from shoppers who refuse cloud photo upload |

### Tradeoffs

- **Gain**: Strongest privacy (local processing), sub-second measurement extraction, offline measurement step, lower cloud transfer volume
- **Accept**: Requires a native mobile SDK; device hardware variability; model distribution to millions of devices; larger app size

Full detail: [solution-architecture.md § Concept B](docs/architecture/solution-architecture.md#concept-b-edge--ai-agent-enabled-operations)

---

## C. Data Fabric / Intelligence Layer

> Unified semantic layer, lineage + governance, AI-ready data products powering decisions across domains.

This concept positions fit assessment data as part of a **unified retail intelligence layer** in Microsoft Fabric. Measurement profiles, garment catalog, and return/exchange transactions are joined under a governed semantic model with full lineage, so the same trusted dataset powers the real-time API, batch return-prediction models, and merchandiser dashboards.

```mermaid
graph TD
    subgraph "Concept C: Data Fabric / Intelligence Layer"
        subgraph "Source Domains"
            Shopper["Shopper<br/>Measurements<br/>(anonymized)"]
            Garment["Garment<br/>Catalog<br/>(sizes, materials)"]
            Returns["Return & Exchange<br/>Transactions<br/>(outcomes, reasons, costs)"]
        end
        Shopper --> Fabric["Microsoft Fabric — Unified Semantic Layer<br/>• lineage: measurement → assessment → outcome<br/>• governance: PII classification, retention<br/>• AI-ready data products (curated, cataloged)<br/>• cross-domain joins: fit score ↔ return rate"]
        Garment --> Fabric
        Returns --> Fabric
        Fabric --> API["VirtualMirror API<br/>(real-time assessment)"]
        Fabric --> ReturnModel["Return Prediction<br/>Model (batch/ML)"]
        Fabric --> Merch["Merchandising Intelligence<br/>(size dist., trends)"]
    end
```

### How agentic AI transforms the merchandiser's workflow

> "An AI copilot that assists the **merchandising analyst** by synthesizing **fit assessment outcomes, return data, and size distribution trends**, flagging **garments with high return-due-to-fit rates**, and recommending **size chart adjustments and inventory rebalancing** — while the **analyst retains accountability** for catalog decisions."

| Dimension        | Concept C capability                                                                                                       |
|------------------|----------------------------------------------------------------------------------------------------------------------------|
| **Workflow**     | Automated drift alerts: "Style #245 fit-confidence drops below 70% — proposed size chart correction attached"              |
| **Decision**     | Cross-domain joins close the loop: assessment confidence ↔ actual return reason ↔ next-cycle size curve                    |
| **Safety**       | Full lineage from raw measurement → assessment → return outcome; PII classification labels; GDPR Article 30 evidence       |
| **Reliability**  | One governed source of truth for AI, BI, and operational reporting — no shadow datasets, no drift between models           |
| **Optimization** | Returns become a strategic signal (not a cost center): better size curves, fewer overstocks, lower transport emissions     |

### Tradeoffs

- **Gain**: Strategic data asset; cross-domain insights; AI and BI operate on the same governed data
- **Accept**: Significant Microsoft Fabric investment; data engineering effort beyond the fit assessment scope; longer time-to-value

Full detail: [solution-architecture.md § Concept C](docs/architecture/solution-architecture.md#concept-c-data-fabric--intelligence-layer)

---

## Concept Comparison

| Aspect                    | A. Cloud-Centric Platform                     | B. Edge + AI Agent                                | C. Data Fabric / Intelligence Layer            |
|---------------------------|-----------------------------------------------|---------------------------------------------------|-------------------------------------------------|
| **Primary user**          | Online shopper                                | Privacy-conscious home shopper (HITL)             | Merchandiser, data scientist                    |
| **Where AI runs**         | Azure managed services                        | Smartphone on-device AI + cloud comparison        | Cloud (real-time + batch on Fabric)             |
| **Human accountability**  | Shopper decides to buy                        | Shopper decides whether to trust and buy          | Analyst decides catalog & inventory changes     |
| **Latency profile**       | < 5s p95, network bound                       | Sub-second on-device; cloud only for comparison   | Real-time + batch; insight latency hours–days   |
| **Privacy posture**       | Strong — 60s TTL, opaque refs                 | **Strongest** — raw images never leave the device | Strong — full lineage + PII classification      |
| **Time to value**         | **Months** (v1 today)                         | 1–2 years (mobile SDK, model distribution)        | 1–2 years (Fabric build-out, source onboarding) |
| **Capex profile**         | Low — managed services, pay-per-use           | Higher — native SDK + model distribution          | Higher — Fabric capacity + data engineering     |
| **Return-rate impact**    | 20–30% reduction (direct)                     | Incremental — unlocks privacy-sensitive shoppers  | Compounding — improves the catalog itself       |
| **Vendor lock-in risk**   | High (Azure)                                  | Medium (edge runtime portable)                    | High (Microsoft Fabric)                         |
| **AI failure mode**       | Graceful degrade to size chart                | Graceful degrade to shopper judgment/size chart   | Stale data falls back to last good snapshot     |

---

## Recommended Sequencing

1. **Now (v1) — Build Concept A.** Ship the cloud-centric API. Prove the 20–30% return-rate reduction, validate confidence thresholds, and build the audit trail. Concept A is implementation-ready today.
2. **Next (v1.5) — Layer Concept C onto Concept A.** Land assessment outcomes and return transactions in Microsoft Fabric so the merchandising loop closes. Same governed data powers both real-time API and batch analytics.
3. **Later (v2) — Extend with Concept B into retailer mobile apps.** Once edge model footprint is small enough and the mobile SDK distribution strategy is clear, push measurement extraction onto shopper smartphones for the strongest privacy posture and an at-home native-app experience.

The three concepts are **complementary, not exclusive** — they form a sequenced transformation roadmap: Cloud → Insight → Edge.

---

## Source Artifacts

| Artifact                         | Path                                                                                              |
|----------------------------------|---------------------------------------------------------------------------------------------------|
| Problem statement                | [docs/Sessions/Problem-statement.md](docs/Sessions/Problem-statement.md)                          |
| Product definition               | [docs/Sessions/Product-definition.md](docs/Sessions/Product-definition.md)                        |
| Solution architecture (full)     | [docs/architecture/solution-architecture.md](docs/architecture/solution-architecture.md)          |
| Canonical diagrams (ASCII)       | [docs/architecture/diagrams.md](docs/architecture/diagrams.md)                                    |
| Canonical diagrams (Mermaid)     | [docs/architecture/diagrams-mermaid.md](docs/architecture/diagrams-mermaid.md)                    |
| Architecture decision register   | [docs/architecture/decision-register.md](docs/architecture/decision-register.md)                  |
| Risk register                    | [docs/architecture/risk-register.md](docs/architecture/risk-register.md)                          |
| AI feasibility research          | [docs/research/ai-fit-assessment-feasibility.md](docs/research/ai-fit-assessment-feasibility.md)  |
| Feature specification            | [specs/001-clothing-fit-assessment/spec.md](specs/001-clothing-fit-assessment/spec.md)            |
| API contract (OpenAPI)           | [specs/001-clothing-fit-assessment/contracts/openapi.yaml](specs/001-clothing-fit-assessment/contracts/openapi.yaml) |

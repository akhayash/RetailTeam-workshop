# Deliverable 2 | Persona-Driven Scenarios

**Industry**: Retail — Online Apparel
**Use case**: AI Clothing Fit Assessment Agent
**Date**: 2026-05-14
**Status**: Workshop deliverable

> *For each architecture concept, describe how humans and AI work together.*

For each concept below:

- **What an AI agent or copilot would do**
- **What decisions it supports (not replaces)**
- **How humans and AI work together**
- **What new roles, workflows, or hybrid interfaces emerge**

A single principle runs across all three: **AI augments the human; the human retains accountability.** The system produces confidence-scored recommendations with escalation paths — it never auto-executes a purchase, a store action, or a catalog change.

Anchoring artifacts: [Deliverable 1](Deliverable1.md) · [Solution architecture — Persona-Driven AI Scenarios](docs/architecture/solution-architecture.md#persona-driven-ai-scenarios) · [Product definition](docs/Sessions/Product-definition.md)

---

## Scenario A — Concept A: Online Shopper + AI Fit Assessment

> *An AI copilot that assists the **online shopper** by synthesizing **a single photo plus self-reported height into body measurements and a per-area fit profile**, flagging **low-confidence predictions and poor-fit areas**, and recommending **the best size with a confidence-scored, per-area fit breakdown** — while the **shopper retains accountability** for the purchase decision.*

### Filled framing template

| Slot          | Specifics for this scenario                                                                                                          |
|---------------|---------------------------------------------------------------------------------------------------------------------------------------|
| `<persona>`   | Online shopper on a retail partner's product detail page (PDP)                                                                       |
| `<data>`      | Shopper photo (front/side), self-reported height, garment normalized size chart, fit intent (slim/regular/relaxed), brand metadata    |
| `<risks>`     | Low model confidence; poor lighting or pose; size chart drift; ambiguous fit intent; biometric privacy concerns                       |
| `<actions>`   | Recommend size with 5-point per-area fit scale; surface "low confidence — consult size chart" disclaimer; suggest alternative items   |

### What the AI agent does

- Accepts one or two photos and a height value through the storefront's fit-assessment widget
- Calls the three-tier AI pipeline (Florence-2 → GPT-5.2 Vision → AI Foundry v2) to extract body landmarks and derive measurements
- Maps measurements against the garment's normalized size chart and fit intent
- Returns a recommended size **and** a 5-point fit scale per body area (chest, waist, hips, inseam, shoulders)
- Emits a `confidence` score and an `isLowConfidence` flag when below ~70%; substitutes a soft disclaimer for a hard recommendation

### Decisions it supports (not replaces)

- **Which size to add to cart** — the shopper, not the AI, places the order
- **Whether to consult the size chart instead** — surfaced when confidence is low or photo quality is poor
- **Whether to look at an alternative garment or brand** — the AI surfaces options; the shopper chooses

### How humans and AI work together

| Step | Human                                                              | AI                                                                          |
|------|--------------------------------------------------------------------|------------------------------------------------------------------------------|
| 1    | Uploads photo(s) and height                                        | Validates image (format, size, quality) and runs content-safety filter      |
| 2    | —                                                                  | Extracts measurements; compares to garment size chart; produces fit profile |
| 3    | Reviews the per-area fit overlay and confidence indicator          | Displays explainable, per-area scoring and a low-confidence disclaimer      |
| 4    | Decides to buy, swap size, or abandon                              | Logs assessment metadata (no raw image, no biometric vector)                |

### New roles, workflows, or hybrid interfaces

- **Hybrid interface**: a fit-assessment widget embedded in the PDP showing a visual per-area fit overlay (e.g., "tight at hips, ideal at chest")
- **New workflow**: "see fit before you buy" replaces "order three sizes, return two"
- **No new role on the shopper side**; on the retailer side, a lightweight **Catalog Steward** workflow keeps garment size charts and fit-intent metadata clean
- **Escalation path**: low-confidence results route the shopper to the size chart and an optional "talk to a stylist" channel, never to a silent failure

---

## Scenario B — Concept B: Store Associate + AI Copilot (Edge)

> *An AI copilot that assists the **store associate** by synthesizing **real-time fitting-room measurements and in-store inventory data**, flagging **fit issues and stock gaps before the shopper tries the garment on**, and recommending **alternative sizes and similar-fit items currently in stock** — while the **associate retains accountability** for the styling advice given to the shopper.*

### Filled framing template

| Slot          | Specifics for this scenario                                                                                                    |
|---------------|---------------------------------------------------------------------------------------------------------------------------------|
| `<persona>`   | In-store associate ("AI-assisted stylist") on a mobile copilot app; secondary user is the shopper in the fitting room          |
| `<data>`      | Edge-derived measurements (raw images never leave the kiosk), live inventory, garment fit intent, shopper preferences          |
| `<risks>`     | Edge model drift; offline scenarios; biometric privacy in a physical space; over-trust in AI suggestions; advice liability     |
| `<actions>`   | Suggest sizes to pull for try-on; flag likely-poor-fit items; recommend in-stock alternatives; escalate to cloud when uncertain |

### What the AI agent does

- Runs **local pose detection and measurement extraction** on the fitting-room camera or kiosk; raw images never leave the device
- Caches garment data and inventory at the edge for offline operation
- Sends **only derived measurements** (not images) to the cloud backend when edge confidence drops below threshold
- Pushes a ranked try-on set to the associate's mobile app: *"Size M slim recommended; also pull Size M regular and Style #245 in M"*
- Cross-references **live inventory** so suggestions reflect what is actually on the floor

### Decisions it supports (not replaces)

- **Which sizes to pull from the floor for try-on** — the associate selects from the AI-ranked set
- **Which alternative garments to suggest** — the associate weighs shopper preferences, brand knowledge, and styling judgment
- **Whether to escalate** — for a difficult fit, the associate decides whether to engage a senior stylist or alterations service

### How humans and AI work together

| Step | Human (shopper / associate)                              | AI (edge + cloud)                                                                  |
|------|----------------------------------------------------------|-------------------------------------------------------------------------------------|
| 1    | Shopper enters fitting room and opts in via signage      | Edge device captures pose; derives measurements locally; deletes frames immediately |
| 2    | —                                                        | Sends measurements + garment context to associate copilot; cloud fallback if needed |
| 3    | Associate reviews AI-ranked try-on set on mobile app     | Displays size + alternatives + confidence + inventory availability                   |
| 4    | Associate explains recommendation in the shopper's words | Logs anonymized aggregate signals for store-ops analytics                            |
| 5    | Shopper tries on and decides                              | Captures outcome (kept / swapped / declined) — no raw image, no biometric vector    |

### New roles, workflows, or hybrid interfaces

- **New role**: **"AI-Assisted Stylist"** — a store associate equipped with real-time fit intelligence on a mobile copilot
- **New workflow**: fewer size runs ("let me bring you the next size"), more relationship selling and outfit building
- **Hybrid interface**: an associate mobile app *and* an opt-in shopper-facing kiosk screen — the AI's suggestions are visible to both, building trust through transparency
- **New ops role**: **Edge Fleet & Model Steward** — pushes model updates, monitors device health, validates drift across stores
- **Escalation path**: when edge confidence is low, the flow transparently switches to the cloud pipeline and tells the associate so

---

## Scenario C — Concept C: Merchandising Analyst + Intelligence Layer

> *An AI copilot that assists the **merchandising analyst** by synthesizing **fit-assessment outcomes, return reasons, and size-distribution trends across brands and seasons**, flagging **garments with high return-due-to-fit rates and probable size-chart inaccuracies**, and recommending **size-chart corrections, inventory rebalancing, and garment redesign priorities** — while the **analyst retains accountability** for catalog and buying decisions.*

### Filled framing template

| Slot          | Specifics for this scenario                                                                                                                   |
|---------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| `<persona>`   | Merchandising analyst / catalog steward / buyer; secondary consumer is the digital transformation leader                                       |
| `<data>`      | Fit assessment outcomes, return-reason data, sales by size, supplier size charts, garment metadata — joined in Microsoft Fabric semantic layer |
| `<risks>`     | Spurious correlations; supplier-data quality gaps; over-rotation on a single season; biased models; PII leakage across domains                  |
| `<actions>`   | Propose size-chart adjustments; flag garments for redesign; rebalance inventory across sizes; trigger drift alerts to catalog stewards          |

### What the AI agent does

- Joins shopper measurement profiles (anonymized), garment catalog, and return/exchange transactions under a **governed semantic layer** in Microsoft Fabric
- Runs batch ML models to correlate fit-assessment confidence with **actual return outcomes** — closing the loop between prediction and reality
- Surfaces "drift alerts" when a garment's real-world fit pattern diverges from its published size chart
- Proposes **size-chart corrections** and **size-curve rebalancing** with quantified business impact (return cost, lost sales, sustainability)
- Generates lineage-backed evidence packs for governance and regulatory reporting (e.g., GDPR Article 30)

### Decisions it supports (not replaces)

- **Whether to amend a published size chart** — the analyst validates with the supplier before the change ships
- **Which garments to flag for redesign or to delist** — the analyst weighs commercial, brand, and supplier-relationship factors
- **How to rebalance the size curve for the next buy** — the analyst negotiates with suppliers on the final order

### How humans and AI work together

| Step | Human (analyst / steward)                                       | AI (Data Fabric / Intelligence Layer)                                                       |
|------|------------------------------------------------------------------|----------------------------------------------------------------------------------------------|
| 1    | Sets the question — "Which styles drive fit-related returns?"    | Runs cross-domain joins; surfaces ranked list with quantified return-cost impact            |
| 2    | Inspects drill-down: per-size, per-region, per-cohort breakdowns | Provides lineage trail (raw measurement → assessment → return outcome) for every data point  |
| 3    | Validates with supplier or commercial team                       | Holds a draft size-chart correction; tracks approval workflow                                |
| 4    | Approves the change                                              | Promotes the new size chart to the VirtualMirror API and notifies dependent storefronts          |
| 5    | Reviews post-change metrics after one cycle                      | Tracks lift on return rate and confidence score; auto-opens a follow-up if regression occurs |

### New roles, workflows, or hybrid interfaces

- **New role**: **Catalog Steward** — owns the human-in-the-loop approval of AI-suggested size-chart corrections
- **New role**: **Fit Data Scientist** — tunes return-prediction and drift models on the unified semantic layer
- **Hybrid interface**: merchandising dashboard with fit-informed analytics, automated drift alerts, and a one-click "propose size-chart correction" workflow
- **New workflow**: returns become a **strategic feedback loop** rather than a back-office cost — the catalog learns from every assessment outcome
- **Escalation path**: high-impact changes (e.g., affecting > N styles or a flagship brand) auto-route to a senior buyer for sign-off

---

## Cross-Concept Synthesis

| Aspect                       | A. Cloud-Centric (Shopper)                          | B. Edge + AI Agent (Associate)                      | C. Data Fabric (Analyst)                           |
|------------------------------|-----------------------------------------------------|------------------------------------------------------|-----------------------------------------------------|
| **Primary persona**          | Online shopper                                       | Store associate (HITL gate) + shopper               | Merchandising analyst / catalog steward             |
| **AI's job**                 | Predict per-area fit + recommend size               | Pre-filter try-on set + flag fit issues             | Correlate fit outcomes ↔ returns and propose fixes  |
| **What stays human**         | The purchase decision                                | The styling advice and final recommendation         | The catalog and buying decisions                    |
| **Decision horizon**         | Seconds (one purchase)                               | Minutes (one fitting-room session)                  | Days–weeks (next buying cycle)                      |
| **Key risk to manage**       | Biometric privacy; low-confidence over-trust        | Edge drift; in-store privacy; advice liability      | Spurious correlations; biased models; PII spillover |
| **Hybrid interface**         | PDP fit widget with per-area overlay                 | Associate mobile copilot + opt-in shopper kiosk     | Merchandising dashboard + drift-alert workbench     |
| **New role(s)**              | Catalog Steward (light)                              | AI-Assisted Stylist; Edge Fleet & Model Steward     | Catalog Steward; Fit Data Scientist                 |
| **Loop closes when**         | Shopper buys (or doesn't)                            | Associate adapts recommendation in real time        | Catalog updates feed back into the API for everyone |

A virtuous loop emerges across the three concepts: **Concept A** generates fit signal at scale, **Concept C** turns that signal into catalog improvements, and **Concept B** delivers the improved intelligence into physical retail — with a **human accountable at every gate**.

---

## Source Artifacts

| Artifact                                | Path                                                                                              |
|-----------------------------------------|---------------------------------------------------------------------------------------------------|
| Deliverable 1 — Architecture concepts   | [Deliverable1.md](Deliverable1.md)                                                                |
| Solution architecture (personas + scenarios) | [docs/architecture/solution-architecture.md](docs/architecture/solution-architecture.md)     |
| Product definition                      | [docs/Sessions/Product-definition.md](docs/Sessions/Product-definition.md)                        |
| Problem statement                       | [docs/Sessions/Problem-statement.md](docs/Sessions/Problem-statement.md)                          |
| Risk register                           | [docs/architecture/risk-register.md](docs/architecture/risk-register.md)                          |
| Architecture decision register          | [docs/architecture/decision-register.md](docs/architecture/decision-register.md)                  |
| AI feasibility research                 | [docs/research/ai-fit-assessment-feasibility.md](docs/research/ai-fit-assessment-feasibility.md)  |
| Feature specification                   | [specs/001-clothing-fit-assessment/spec.md](specs/001-clothing-fit-assessment/spec.md)            |

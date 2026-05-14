# Primary Research — Solution Architecture Presentation

**Date**: 2026-05-13
**Working directory**: `.copilot-tracking/ppt/2026-05-13/solution-architecture/`
**Deliverable**: PowerPoint deck presenting the AI Clothing Fit Assessment Agent solution architecture, aligned with the workshop guidance in `docs/Inputs/EX2_Technical_Architecture_Research.pptx`.

---

## 1. Source Material

| Source | Role | Path |
|--------|------|------|
| Workshop guidance PPTX | Framework, visual language, layout patterns | `docs/Inputs/EX2_Technical_Architecture_Research.pptx` |
| Solution architecture | Primary content (v2.0.0) | `docs/architecture/solution-architecture.md` |
| Decision register | ADRs ADR-001 through ADR-012 | `docs/architecture/decision-register.md` |
| Risk register | 11 risks, severity matrix | `docs/architecture/risk-register.md` |
| Architecture diagrams | 12 ASCII diagrams (reference) | `docs/architecture/diagrams.md` |
| Research notes | Phase 0 decisions R1–R7 | `specs/001-clothing-fit-assessment/research.md` |
| OpenAPI contract | 9 endpoints | `specs/001-clothing-fit-assessment/contracts/openapi.yaml` |
| Extracted style guide | From workshop PPTX | `content/global/style.yaml` |

## 2. Workshop Framework We Must Honour

The guidance deck mandates a **two-phase exercise** that our solution architecture deck must demonstrably follow:

- **Phase A — Research**: Tech Stack, Limitations, Architectural Patterns, Owners → Domains, Personas
- **Phase B — Design**: Three concept diagrams + Persona-driven AI scenarios + C-Suite "So What?"

The workshop quality bar:

1. **Hypotheses are labelled separately from facts** — every claim is `[Verified]`, `[Hypothesis]`, or `[Assumption]`.
2. **Sources are cited** — Microsoft docs, ADRs, the spec.
3. **Tradeoffs are explicit** — every concept names what it gains and what it loses.
4. **C-Suite framing is required** — every concept must translate to CIO / Ops / Risk language.
5. **AI + human collaboration is shown** — each persona scenario shows where AI augments, not replaces, the human.
6. **IQ Framework alignment** — Work IQ, Foundry IQ, Fabric IQ.

## 3. Visual Language (locked from `style.yaml`)

- **Format**: 16:9, 13.333" × 7.5"
- **Heading font**: Segoe Sans Display, 34pt
- **Body font**: Segoe Sans Display, 20pt body / 14–16pt cards / 11–12pt fine print
- **Primary brand**: navy `#14366E` — used for card header bars, numbered ovals, brand title
- **Secondary accent**: mid-blue `#0B5594` — eyebrow labels, step labels
- **Signature wash**: olive-green `#9BBB59` at 47–68% alpha, bounded by 0.5pt border `#DCE3EC`
- **Text**: body `#1F1F1F`, inverse `#FFFFFF`, eyebrow gray `#95C7E7`, italic gray `#6B6B6B`
- **Header rule**: thin left rail `#4F81BD` on cover only

**Layout patterns to reuse**:

1. Full-bleed cover with dark overlay and brand title
2. "Setup / Real Goal" two-up cards (navy + black headers, olive-wash bodies)
3. N-up step-card framework with navy numbered ovals (1, 2, 3...)
4. Wide tables (black header row + blue first-column labels)
5. Three-column concept rows
6. Two-pane workshop summary
7. Closing question with behaviors table

## 4. Audience and Intent

- **Audience**: Mixed retail leadership and technical reviewers (the workshop room) — CIO, VP of E-Commerce, Chief Privacy Officer, principal engineers, architects.
- **Length**: ~15 slides, designed to be presented in 15–20 minutes with discussion.
- **Tone**: Confident but humble — facts are cited, hypotheses are flagged, tradeoffs are explicit.
- **Outcome**: Reviewers can defend the v1 selection of Concept A, see the v2/v3 evolution path through Concepts B and C, and understand the risk and decision posture.

## 5. Deck Outline (15 slides)

| # | Slide | Layout pattern | Purpose |
|---|-------|---------------|---------|
| 1 | Cover | Hero cover with overlay | Title, subtitle, byline, brand framing |
| 2 | Executive Summary | Two-up "Setup / Real Goal" cards | What it is and what it is not |
| 3 | Phase A — 5 Research Lenses | 5-up step cards with numbered ovals | Tech Stack / Limitations / Patterns / Owners / Personas |
| 4 | Retail Industry Personas | 3-up column cards | Online Shopper / Digital Leader / Risk-Compliance |
| 5 | Phase B — Three Architecture Concepts (overview) | 3-up column header row | Introduce Concepts A, B, C |
| 6 | Concept A — Cloud-Centric Platform | Card + tradeoffs box | v1 implementation, named tradeoffs |
| 7 | Concept B — Edge + AI Agent | Card + tradeoffs box | Future expansion, named tradeoffs |
| 8 | Concept C — Data Fabric / Intelligence Layer | Card + tradeoffs box | Long-term, named tradeoffs |
| 9 | Three-Tier AI Pipeline (Concept A detail) | 3 stacked tier panels | Tier 1 Validation / Tier 2 Extraction / Tier 3 v2 |
| 10 | Assessment Request Flow | Numbered step ribbon | End-to-end happy path |
| 11 | C-Suite "So What?" | Wide table (black header + blue first column) | Each concept × CIO / Ops / Risk |
| 12 | Business Value & IQ Framework | Two-pane: 4 value drivers + IQ table | Work IQ / Foundry IQ / Fabric IQ alignment |
| 13 | Key Decisions and Top Risks | Two-up cards | 5 ADRs + 5 risks with severity |
| 14 | Tradeoffs and Hypotheses | Wide table with `[H]` / `[V]` badges | Hypothesis register named, validation method per row |
| 15 | Closing — Defending the Choice | Closing question + behaviors table | Workshop close with discussion prompts |

## 6. Per-Slide Content Brief

### Slide 1 — Cover

- **Eyebrow**: "SOLUTION ARCHITECTURE • RETAIL TEAM"
- **Title**: "AI Clothing Fit Assessment Agent"
- **Subtitle**: "Phase A Research + Phase B Future-State Design"
- **Tagline (white italic)**: "Microsoft AI stack, multi-tenant from day one, humans accountable for every decision."
- **Footer**: "Solution Architecture v2.0.0 · 2026-05-13"
- **Visual**: Solid navy background with thin `#4F81BD` left rail; no hero image (we have no licensed retail photo and `style.yaml` allows solid-fill covers).

### Slide 2 — Executive Summary (Setup vs Real Goal)

- **Left card (black header "The Problem")**: 25–40% online clothing return rate; no way to "try before you buy"; sizing chaos across brands; privacy concerns block easy biometric fixes.
- **Right card (navy header "The Solution")**: Multi-tenant .NET 8 API on Azure Container Apps; 3-tier AI pipeline (Microsoft-only); 5-point fit scale per body area; photos purged in < 60s; humans decide.

### Slide 3 — Phase A: Five Research Lenses

Five numbered olive-wash cards (mirroring the source deck slide 3 layout):

1. **Uncover the Tech Stack** — .NET 8, ASP.NET Core, Azure Container Apps, Cosmos DB, Azure OpenAI, Entra ID. `[Verified]` from ADR-001/007/011.
2. **Identify Limitations** — Azure AI Vision retires Sep 2028; GPT-4o is non-deterministic; ±2–4 cm accuracy ceiling. `[Verified]` from research.md R1.
3. **Spot Patterns** — Clean Architecture; multi-tenant from day one; zero-trust managed identity; async overflow queue. `[Verified]`.
4. **Map Owners → Domains** — Engineering Lead → AI pipeline; Platform → infra/Bicep; Data → Cosmos design; Security → Entra/KeyVault; Product → fit scale tuning.
5. **Profile the Personas** — Shopper / Digital Leader / Privacy Officer (preview to slide 4).

### Slide 4 — Retail Industry Personas (3-up)

Three column cards (navy header bar over olive-wash body):

| Column | Headline | One-line body |
|--------|----------|---------------|
| Online Shopper | "Buy clothes that fit without leaving home" | High-return-rate, privacy-conscious, < 5s patience |
| Digital Transformation Leader | "Reduce returns, increase conversion" | Needs measurable ROI in 6 months, integrates with legacy storefronts |
| Risk / Compliance Officer | "GDPR, EU AI Act, biometric exposure" | Demands DPIA-ready privacy by design, explainable AI |

Eyebrow line at bottom: "AI augments shoppers and associates. Humans retain accountability for every purchase, recommendation, and policy decision."

### Slide 5 — Phase B: Three Architecture Concepts (overview)

Three column headers (navy bars) with one-line summaries underneath:

- **Concept A — Cloud-Centric Platform** — Modern data foundation, scalable services, governed AI/ML. `[v1 implementation]`
- **Concept B — Edge + AI Agent Operations** — Decisioning at the edge, agentic workflows, in-store augmentation. `[v2 expansion]`
- **Concept C — Data Fabric / Intelligence Layer** — Unified semantic layer, lineage, AI-ready data products. `[v3 strategic]`

Eyebrow: "Three concepts, one architecture. Concept A ships v1; B and C are documented evolution paths, not parallel builds."

### Slide 6 — Concept A — Cloud-Centric Platform

- **Body card (olive wash)** — Lists the five service pillars: Container Apps · Cosmos DB (hierarchical PK) · Blob (60s TTL) · Azure AI Services (Vision + Content Safety + OpenAI) · Service Bus.
- **Tradeoffs box (navy header)** — Gains: managed-service utilization, fast to ship, zero secrets. Loses: Azure vendor lock-in, single-region in v1.
- **Hypothesis tag**: `[H-1 Verified by integration testing]` GPT-4o + height delivers ±2–4 cm; `[H-2 Hypothesis]` 70% confidence threshold is the right tradeoff for shopper trust.

### Slide 7 — Concept B — Edge + AI Agent Operations

- **Body card (olive wash)** — In-store kiosks + store associate mobile copilot. Local pose detection. Cloud sync for low-confidence cases. Inventory cross-check.
- **AI + Human paragraph** — "An AI copilot assists the store associate by synthesizing real-time measurements and inventory; flagging poor fit before try-on; recommending alternatives. The associate retains accountability for the styling advice."
- **Tradeoffs box** — Gains: privacy (local processing), latency, in-store reach. Loses: device management, model distribution complexity, hardware capex.

### Slide 8 — Concept C — Data Fabric / Intelligence Layer

- **Body card (olive wash)** — Shopper profiles + garment catalog + return transactions → Microsoft Fabric semantic layer → fit assessment / return prediction / merchandising intelligence.
- **AI + Human paragraph** — "An AI copilot assists the merchandising analyst by correlating fit confidence with returns; flagging high-return garments; recommending size chart corrections. The analyst retains accountability for catalog decisions."
- **Tradeoffs box** — Gains: cross-domain joins, governed lineage, AI-ready data products. Loses: Fabric capex, longer time-to-insight beyond the fit feature.

### Slide 9 — Three-Tier AI Pipeline (Concept A detail)

Three stacked tier panels (navy headers, olive body), matching workshop step-card aesthetic:

- **Tier 1 — Validation**: Azure AI Vision (people / multi-person / bounding box) + Content Safety (minor detection / moderation) + Defender for Storage (malware). Runs in parallel. Cited: ADR-001, ADR-012.
- **Tier 2 — Extraction**: Azure OpenAI GPT-4o Vision, structured JSON output, height as mandatory scale reference, prompts versioned in source. Cited: ADR-001, ADR-008.
- **Tier 3 — v2 future**: Custom SMPL body model on Azure AI Foundry, deterministic, ±1–2 cm. `[Hypothesis pending v1 production data]`.

### Slide 10 — Assessment Request Flow

A horizontal numbered ribbon (1 → 7) with brief verbs:

1. Frontend POST → 2. Auth + rate limit → 3. Image upload (in-memory or Blob) → 4. Tier 1 Validate → 5. Tier 2 Extract → 6. Compare vs garment data → 7. Return result + audit + purge image.

Bottom strip: "p95 latency target: < 5s. Async queue triggers above 50 depth or 4s p95."

### Slide 11 — C-Suite "So What?" Table

Wide table (black header row, blue first column matching workshop slide 4/10 pattern):

| | CIO / VP Tech | Business / Ops | Risk / Compliance |
|---|---------------|---------------|-------------------|
| **A. Cloud-Centric** | API-first, managed services, scalable | 20–30% return reduction, ROI in 6 months | Privacy by design, DPIA-ready |
| **B. Edge + Agent** | Extends digital into physical stores | Associates as AI-augmented stylists | Strongest privacy posture (local) |
| **C. Data Fabric** | Unified retail intelligence layer | Fit-informed merchandising | Full lineage, GDPR Article 30 |

### Slide 12 — Business Value & IQ Framework

Two-pane layout (split workshop slide 9 style):

- **Left pane — Four Value Drivers** (compact card list): Decision Velocity & Confidence · Workforce Productivity · Operational Resilience & Risk · Growth Enablement.
- **Right pane — IQ Framework Alignment** (small table): Work IQ (in-workflow recommendations) · Foundry IQ (the 3-tier pipeline) · Fabric IQ (governed data foundation, Concept C path).

### Slide 13 — Key Decisions and Top Risks

Two-up cards (navy + black headers, workshop slide 2 pattern):

- **Left card "Decisions That Shape v1" (5 ADRs)**: ADR-001 three-tier pipeline · ADR-002 hierarchical partition keys · ADR-004 Entra ID + managed identity, APIM deferred · ADR-008 mandatory height · ADR-011 Clean Architecture.
- **Right card "Risks We're Tracking" (5 risks with severity badges)**: R-001 GPT-4o accuracy [CRITICAL] · R-002 Vision deprecation [HIGH] · R-003 non-deterministic LLM [HIGH] · R-007 regulatory drift [HIGH] · R-005 multi-tenant leakage [MEDIUM].

### Slide 14 — Tradeoffs and Hypotheses

Wide table — named hypotheses, status, validation method, owner:

| ID | Hypothesis | Status | Validation Method |
|----|-----------|--------|-------------------|
| H-1 | GPT-4o + height delivers ±2–4 cm | Hypothesis | Integration testing vs ground-truth dataset |
| H-2 | 70% confidence is the right shopper-trust threshold | Hypothesis | A/B testing vs disclaimer escalation rate |
| H-3 | Hierarchical PK prevents tenant data leakage at scale | Verified | Schema + repository compile-time check |
| H-4 | 60s blob TTL satisfies privacy regulators | Hypothesis | DPIA + counsel review |
| H-5 | ASP.NET middleware rate limiting is sufficient for v1 | Hypothesis | Load test at 2× projected peak |
| H-6 | Edge inference (Concept B) is cost-justified vs cloud | Hypothesis | Per-store TCO model + pilot |

### Slide 15 — Closing — Defending the Choice

- **Big question (workshop slide 11 pattern)**: "Why this architecture, why now, what would change our mind?"
- **Behaviors table**:
  - "We will ship Concept A as v1 because measurable ROI in 6 months is the contract."
  - "We will reopen Tier 2 if H-1 fails integration testing."
  - "We will pilot Concept B in 12–18 months once shopper trust data exists."
  - "We will deepen into Concept C when fit data has demonstrated business value beyond returns."

## 7. Build Strategy

- **Mode**: Full rebuild (new deck from scratch) — we are not modifying the workshop guidance PPTX.
- **Template**: Use `--template` pointing to `docs/Inputs/EX2_Technical_Architecture_Research.pptx` to inherit the master/layout names (`4_Title and Content`, `Title Only`, `Blank`) so title placeholders work.
- **Output**: `slide-deck/solution-architecture.pptx` (15 slides).
- **Speaker notes**: Mandatory on every slide (style.yaml has `speaker_notes_required: true`).
- **Title placeholders**: Keep `_placeholder: true` on title boxes for slides 2+ to inherit master styling; slide 1 cover uses plain textboxes (matches source slide 1).
- **Fonts**: Replace any `+mj-lt` / `+mn-lt` placeholder tokens with `Segoe Sans Display` in content YAMLs.

## 8. Detected Gaps and Open Questions

1. **No hero photo available** — slide 1 will use a solid navy background with the brand title and overlay rule (acceptable per style.yaml; cleaner than the duplicated placeholder PNGs in the source deck).
2. **No real concept artwork for slides 6–8** — we substitute compact ASCII-style mini-diagrams rendered as textboxes inside the body card. This is consistent with the workshop's "scrappy at this stage" tone and avoids the source deck's duplicate-image antipattern.
3. **15 slides is one above the source deck's 11** — justified because our content has more concrete tradeoffs and decisions to defend; still within typical 15–20 min workshop slot.
4. **No further research subagent needed** — all source material is local and current.

## 9. Validation Criteria

Validation in Phase 3 must check:

- Slide dimensions = 13.333" × 7.5"
- Heading font Segoe Sans Display present on titles
- Color palette uses `#14366E`, `#9BBB59` wash, `#0B5594` accents
- Speaker notes present on all 15 slides
- No text overflow in column cards (slides 4, 5, 9)
- Table on slide 11 fits horizontally (3 concept rows × 3 C-suite columns)
- Decorative elements (left rail, header bars) don't collide with text after wrapping
- Slide 14 hypothesis table is readable at default zoom

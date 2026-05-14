# VirtualMirror AI — Project Plan

**Version**: 1.0.0 | **Date**: 2026-05-14 | **Status**: Draft for review
**Owner**: Engineering Lead / Product Manager
**Companion artifacts**: [Technical Implementation Plan](../specs/001-clothing-fit-assessment/plan.md) · [Tasks](../specs/001-clothing-fit-assessment/tasks.md) · [Solution Architecture](architecture/solution-architecture.md) · [Cost Estimate](architecture/cost-estimate.md) · [Risk Register](architecture/risk-register.md)

> This document is the **project-management view** of the build: work breakdown, effort, team, timeline, delivery model. The `plan.md` in the spec folder is the **technical** view (design + constitution gates). Both must stay in sync.

---

## Table of Contents

- [1. Project Summary](#1-project-summary)
- [2. Scope & Out of Scope](#2-scope--out-of-scope)
- [3. Delivery Model](#3-delivery-model)
- [4. Work Breakdown Structure (WBS)](#4-work-breakdown-structure-wbs)
- [5. Effort Summary](#5-effort-summary)
- [6. Team Composition & Capacity](#6-team-composition--capacity)
- [7. Timeline & Sprint Plan](#7-timeline--sprint-plan)
- [8. Hypothesis & Quality Gates](#8-hypothesis--quality-gates)
- [9. Dependencies & Critical Path](#9-dependencies--critical-path)
- [10. Risks to the Plan](#10-risks-to-the-plan)
- [11. Reporting & Governance](#11-reporting--governance)
- [12. Assumptions](#12-assumptions)

---

## 1. Project Summary

| Field | Value |
|-------|-------|
| **Product** | VirtualMirror AI — multi-tenant clothing fit assessment API |
| **Feature** | `001-clothing-fit-assessment` |
| **Target customer** | Walmart digital apparel (and other retail tenants) |
| **Build effort** | **~275 person-days** (~55 person-weeks) |
| **Calendar duration** | **18 weeks** (9 × 2-week sprints) |
| **MVP cutline** | End of Sprint 4 (Phase 1 + 2 + US1) — deployable photo-based fit assessment |
| **Go-live** | End of Sprint 9 — full feature set, IaC, CI/CD, load-validated |
| **Team size** | **5.75 FTE** average (peak 6.75 FTE during IaC + load) |
| **Architecture concept** | Concept A — Azure cloud-centric platform (v1) |
| **Reference tech** | .NET 8, ASP.NET Core, Azure Container Apps, Cosmos DB, Azure OpenAI GPT-5.2, Florence-2, Bicep |

---

## 2. Scope & Out of Scope

### In scope (v1)

- Multi-tenant REST API with Microsoft Entra ID OAuth 2.0 (US3)
- Photo + height → 5-point fit recommendation per body area (US1 — MVP)
- Stored shopper measurement profile with consent + 24h deletion SLA (US2)
- Garment catalog ingestion (single + batch) (US4)
- Three-tier AI pipeline (Florence-2 + Content Safety + GPT-5.2 Vision) with failover
- Resilience: Polly pipelines, AI failover, degradation ladder (L1–L5), tenant bulkhead, DLQ
- Observability: OpenTelemetry → Azure Monitor with SLO alerts and runbooks
- IaC via Bicep across dev / staging / prod
- CI/CD via GitHub Actions with SAST/SCA, SBOM (CycloneDX), Trivy, Notation signing
- Single-region (East US 2)

### Explicitly out of scope (deferred)

- Multi-region active-active (target ~99.95% composite — v2)
- Custom SMPL 3D body model on Azure AI Foundry (Tier 3 — v2)
- Native mobile SDK / on-device inference (Concept B — v2)
- Microsoft Fabric intelligence loop (Concept C — v3)
- Direct Zeekit integration (post-v1 partnership work)
- Order-history-driven sizing signals (v2)

---

## 3. Delivery Model

| Dimension | Choice | Rationale |
|-----------|--------|-----------|
| **Methodology** | Agile / Scrum, 2-week sprints | Aligns with Walmart Platform Engineering golden-path cadence; supports incremental delivery and hypothesis gating |
| **Branching** | Trunk-based with short-lived feature branches; feature flags via Azure App Configuration | Enables continuous deployment, safe partial-merge of WIP, supports canary rollout |
| **TDD** | Enforced per `plan.md` Phase 3+ (Red → Green → Refactor) | Constitution Principle V; risk-down on AI integration via Verify snapshot tests |
| **Definition of Done** | Code + tests (≥ 80% line, ≥ 90% on critical paths) + PR approved + IaC updated + telemetry instrumented + docs updated | Quality gate enforced in CI |
| **Definition of Ready** | Acceptance criteria documented + dependencies cleared + estimate confirmed + Walmart contact identified (where relevant) | Avoids mid-sprint blockers |
| **Promotion gates** | dev (auto on merge) → staging (sprint review approval) → prod (PO + sec sign-off + canary 5% → 25% → 100%) | Constitution Principle VIII (Change Management); rollback < 15 min |
| **Cadence** | Daily 15-min stand-up, sprint planning + review + retro every 2 weeks, weekly architecture sync, monthly risk review | Standard cadence with risk register linkage |
| **Walmart stakeholder demo** | End of every 2nd sprint (every 4 weeks) | Maintains stakeholder confidence and Catalog/Platform alignment |
| **Hypothesis gates** | H7 (Sprint 2), H1 (Sprint 3–4) — formal go/no-go reviews | Per `plan.md` Hypothesis Validation Plan |
| **Hosting of CI/CD** | GitHub Actions; deployable to Azure via Bicep | Aligned with project repository and Microsoft toolchain |

### Estimation method

- **Bottom-up** per task using a three-point reference scale calibrated to senior .NET / Azure engineer productivity
- **Reference task sizes**: S = 0.25–0.5 PD · M = 1–2 PD · L = 2–4 PD · XL = 3–5 PD
- **Cross-cutting overhead** (ceremony, PR review, refinement) modelled separately at 15% on top of build effort
- **Defect / UAT buffer** at 15% on top of build effort
- All estimates assume **senior individual contributor productivity** (not graduate level); junior-heavy teams should multiply by 1.3–1.5x

---

## 4. Work Breakdown Structure (WBS)

Eight work packages aligned to the 7 implementation phases in [tasks.md](../specs/001-clothing-fit-assessment/tasks.md) plus one for project-wide cross-cutting effort.

### WBS overview

```text
VirtualMirror AI v1
├── WP1  Setup & Scaffolding                    (~5 PD,  T001–T012)
├── WP2  Foundational Platform                  (~60 PD, T013–T062)
│   ├── WP2.1  Domain Models & Enums            (~6 PD,  T013–T024)
│   ├── WP2.2  Interfaces                       (~3 PD,  T025–T035)
│   ├── WP2.3  Data & Messaging Infrastructure  (~10 PD, T036–T040)
│   ├── WP2.4  Resilience Pipelines & Failover  (~14 PD, T041–T047)
│   ├── WP2.5  API Middleware & Auth            (~12 PD, T048–T055)
│   ├── WP2.6  Health Probes                    (~4 PD,  T056–T059)
│   └── WP2.7  Config & Aspire Orchestration    (~5 PD,  T060–T062)
├── WP3  US1 — Photo-Based Fit Assessment (MVP) (~60 PD, T063–T093)
│   ├── WP3.1  AI Service Clients               (~12 PD, T063–T066)
│   ├── WP3.2  Image Validation Pipeline        (~8 PD,  T067–T070)
│   ├── WP3.3  Measurement Extraction & Spike   (~8 PD,  T071, H1 spike)
│   ├── WP3.4  Fit Comparison Engine            (~3 PD,  T072)
│   ├── WP3.5  Assessment Orchestration         (~10 PD, T073–T077)
│   ├── WP3.6  API Surface (Controller + DTOs)  (~5 PD,  T078–T082)
│   ├── WP3.7  Repositories & DI                (~4 PD,  T083–T085)
│   └── WP3.8  Test Suite (US1)                 (~10 PD, T086–T093)
├── WP4  US2 — Measurement Profile Storage      (~17 PD, T094–T104)
├── WP5  US3 — Frontend Integration Layer       (~10 PD, T105–T112)
├── WP6  US4 — Garment Data Ingestion           (~13 PD, T113–T121)
├── WP7  Polish & Production Readiness          (~41 PD, T122–T147)
│   ├── WP7.1  Bicep IaC                        (~18 PD, T122–T133)
│   ├── WP7.2  CI/CD & Containerization         (~6 PD,  T134–T136)
│   ├── WP7.3  Observability & Runbooks         (~6 PD,  T137–T140)
│   ├── WP7.4  Load & Chaos Testing             (~6 PD,  T141–T142)
│   └── WP7.5  Docs, Model Card, DR Plan        (~5 PD,  T143–T147)
└── WP8  Project Cross-Cutting (always-on)      (~68 PD)
    ├── WP8.1  Ceremony & PR review (15%)       (~30 PD)
    ├── WP8.2  Defect / UAT buffer (15%)        (~30 PD)
    ├── WP8.3  Walmart integration alignment    (~8 PD)
    ├── WP8.4  Security review / DPIA / sign-off (~10 PD partly absorbed in WP8.2)
    └── WP8.5  Product / backlog management     (absorbed in PM allocation)
```

### WP1 — Setup & Scaffolding

**Goal**: Solution structure, project scaffolding, dependency configuration ready for development.
**Effort**: **~5 PD** · **Tasks**: T001–T012 · **Roles**: Tech Lead, 1 SDE · **Sprint**: 1

| Task | Description | Size | Effort (PD) | Notes |
|------|-------------|:----:|------------:|-------|
| T001 | `src/VirtualMirror.sln` solution file | S | 0.5 | Bootstrap |
| T002–T006 | 5 project skeletons (Core, Services, Infrastructure, Api, AppHost) | S | 1.25 | 0.25 PD each |
| T007 | 6 test projects (Core, Services, Api, Infrastructure, Contract, Load) | M | 0.5 | xUnit baseline |
| T008 | App NuGet dependencies (Azure SDK, Polly, etc.) | M | 0.5 | Pinned versions, central package management |
| T009 | Test NuGet dependencies (xUnit, NSubstitute, NBomber, Verify) | S | 0.25 | |
| T010 | `Directory.Build.props` (nullable, warnings as errors) | S | 0.25 | |
| T011 | `.editorconfig` (C# conventions) | S | 0.25 | |
| T012 | `docker-compose.yml` (Cosmos emulator + Azurite) | M | 0.5 | Local dev only |
| WP1 buffer | Integration / smoke run | — | 1.0 | — |
| **Total** | | | **~5.0** | |

### WP2 — Foundational Platform

**Goal**: Domain core, interfaces, resilience plumbing, middleware, and health probes — blocking prerequisite for all user stories. Sub-divided to enable parallel work.
**Effort**: **~60 PD** · **Tasks**: T013–T062 · **Roles**: Tech Lead, 2 SDEs, DevOps support · **Sprints**: 1–2

| Sub-WP | Tasks | Effort (PD) | Critical path? |
|--------|-------|------------:|:--------------:|
| WP2.1 Domain models & enums | T013–T024 (12 tasks) | 6 | No — fully parallel after enums |
| WP2.2 Interfaces | T025–T035 (11 tasks) | 3 | No — parallel |
| WP2.3 Data & messaging infra (Cosmos repo, Blob, Audit, Service Bus, DLQ) | T036–T040 (5 tasks) | 10 | **Yes** — Cosmos repo blocks downstream |
| WP2.4 Resilience pipelines (Polly per dep + AI failover + 12s budget) | T041–T047 (7 tasks) | 14 | **Yes** — H7 hypothesis gate |
| WP2.5 Middleware (Tenant, CorrelationId, Bulkhead, Auth, Exception, Validation, Rate limit, OTel) | T048–T055 (8 tasks) | 12 | **Yes** — auth blocks all API tests |
| WP2.6 Health probes (Liveness, Readiness, Startup) | T056–T059 (4 tasks) | 4 | No — parallel |
| WP2.7 Config & Aspire host | T060–T062 (3 tasks) | 5 | **Yes** — DI registration |
| WP2 integration | Smoke / contract | — | 6 |
| **Total** | | **~60** | |

**Key risks in WP2**: Polly v8 patterns (T041–T046), AI failover correctness under load (T045–T046), TenantBulkhead concurrency tuning (T050).

### WP3 — US1 — Photo-Based Fit Assessment (MVP)

**Goal**: Working photo + height → fit assessment via the full three-tier AI pipeline with degradation. The MVP cutline.
**Effort**: **~60 PD** · **Tasks**: T063–T093 + H1 spike · **Roles**: Tech Lead, 2 SDEs, ML Engineer · **Sprints**: 3–4

| Sub-WP | Tasks | Effort (PD) | Critical path? |
|--------|-------|------------:|:--------------:|
| WP3.1 AI clients (Florence, Content Safety, OpenAI, prompt template) | T063–T066 (4 tasks) | 12 | **Yes** — H1 gate |
| WP3.2 Image validation pipeline (format/luminance, minor, multi-person, malware) | T067–T070 (4 tasks) | 8 | **Yes** |
| WP3.3 Measurement extraction + **H1 accuracy spike** | T071 (1 task + 5 PD spike) | 8 | **Yes** — H1 hypothesis gate |
| WP3.4 Fit comparison engine (tolerance bands) | T072 (1 task) | 3 | No |
| WP3.5 Assessment orchestration (pipeline + degradation L1–L5 + queue + audit + low-conf) | T073–T077 (5 tasks) | 10 | **Yes** |
| WP3.6 API surface (controller + 4 DTOs) | T078–T082 (5 tasks) | 5 | No — DTOs parallel |
| WP3.7 Repositories (Assessment, Garment) + DI wiring | T083–T085 (3 tasks) | 4 | **Yes** |
| WP3.8 Tests (fixtures + integration + 4 unit + failover) | T086–T093 (8 tasks) | 10 | No — TDD parallel |
| **Total** | | **~60** | |

**Critical milestone**: **H1 (GPT-5.2 accuracy ±2–4 cm)** must clear by end of Sprint 3 to keep schedule. If outside ±4 cm on > 15% of test cases, trigger contingency (3DLOOK bridge, +2 weeks delay).

### WP4 — US2 — Measurement Profile Storage

**Goal**: Returning shoppers skip photo re-upload; consent + 24h hard delete.
**Effort**: **~17 PD** · **Tasks**: T094–T104 · **Roles**: 1 SDE · **Sprint**: 5

| Sub-WP | Tasks | Effort (PD) | Notes |
|--------|-------|------------:|-------|
| Profile repo + service + controller + delete fulfillment + `by-profile` endpoint + DTOs + DI | T094–T102 (9 tasks) | 14 | Cosmos partition / TTL design from data-model |
| Tests (integration + unit) | T103–T104 (2 tasks) | 3 | |
| **Total** | | **~17** | |

### WP5 — US3 — Frontend Integration Layer

**Goal**: Documented, authenticated, versioned API consumable by Walmart's frontend team.
**Effort**: **~10 PD** · **Tasks**: T105–T112 · **Roles**: 1 SDE · **Sprint**: 4 (parallel with WP3) — 5

| Sub-WP | Tasks | Effort (PD) | Notes |
|--------|-------|------------:|-------|
| Swashbuckle + XML docs + versioning + CORS + AssessmentQueued DTO | T105–T109 (5 tasks) | 5 | |
| Contract tests + auth/rate tests + degradation tests | T110–T112 (3 tasks) | 5 | Validates against `contracts/openapi.yaml` |
| **Total** | | **~10** | |

### WP6 — US4 — Garment Data Ingestion

**Goal**: Retail ops can onboard catalog (single + batch up to 100, paginated list).
**Effort**: **~13 PD** · **Tasks**: T113–T121 · **Roles**: 1 SDE · **Sprint**: 6

| Sub-WP | Tasks | Effort (PD) | Notes |
|--------|-------|------------:|-------|
| GarmentService + controller + DTOs + version tracking + DI | T113–T119 (7 tasks) | 10 | Batch endpoint with partial-failure semantics |
| Tests (integration + unit) | T120–T121 (2 tasks) | 3 | |
| **Total** | | **~13** | |

### WP7 — Polish & Production Readiness

**Goal**: Bicep IaC, CI/CD, observability, load + chaos validation, documentation. Pre-cutover hardening.
**Effort**: **~41 PD** · **Tasks**: T122–T147 · **Roles**: DevOps lead, Tech Lead, QA, SDE float · **Sprints**: 6–8 (overlaps user stories)

| Sub-WP | Tasks | Effort (PD) | Notes |
|--------|-------|------------:|-------|
| WP7.1 Bicep modules (root + 11 modules + 3 param files) | T122–T133 (12 tasks) | 18 | ACA multi-AZ, hierarchical partition keys, KEDA HTTP scaler tuned to 25 |
| WP7.2 CI workflow (build, test, SAST/SCA, SBOM, Trivy, Notation, deploy) + Dockerfile + .dockerignore | T134–T136 (3 tasks) | 6 | Coverage gate ≥ 80% / ≥ 90% critical |
| WP7.3 Alert rules + 3 runbooks (latency, AI failover, DLQ depth) | T137–T140 (4 tasks) | 6 | |
| WP7.4 NBomber 500-concurrent load test + chaos / fault injection | T141–T142 (2 tasks) | 6 | Validates H3, H5, H8 |
| WP7.5 README + model card + data classification tags + DR plan + E2E smoke | T143–T147 (5 tasks) | 5 | |
| **Total** | | **~41** | |

### WP8 — Project Cross-Cutting

**Goal**: Capture effort that doesn't fit a single technical task but is required to deliver.
**Effort**: **~68 PD** · **Roles**: All — primarily PM and Tech Lead

| Sub-WP | Description | Effort (PD) |
|--------|-------------|------------:|
| WP8.1 Ceremony & PR review (15% of WP1–7) | Stand-ups, planning, review, retro, code review queue | 30 |
| WP8.2 Defect / UAT / fix-it buffer (15% of WP1–7) | Triaged after each demo and during go-live week | 30 |
| WP8.3 Walmart integration alignment | Walmart Catalog Eng, Platform Eng, Privacy Office sync meetings + DPIA prep | 8 |
| WP8.4 Security & privacy review | Threat model updates, sec sign-off, DPIA review (Security Architect, partly inside WP8.2) | (10 absorbed) |
| WP8.5 PM / backlog grooming | Story refinement, ADO/Jira hygiene, stakeholder reporting (PM dedicated capacity) | (absorbed in PM allocation) |
| **Total** | | **~68** |

---

## 5. Effort Summary

### Build effort by work package

| WP | Title | Tasks | Effort (PD) | % of build |
|:---|-------|:-----:|------------:|-----------:|
| WP1 | Setup & Scaffolding | 12 | 5 | 2% |
| WP2 | Foundational Platform | 50 | 60 | 22% |
| WP3 | US1 — Photo-Based Fit Assessment (MVP) | 31 | 60 | 22% |
| WP4 | US2 — Measurement Profile Storage | 11 | 17 | 6% |
| WP5 | US3 — Frontend Integration Layer | 8 | 10 | 4% |
| WP6 | US4 — Garment Data Ingestion | 9 | 13 | 5% |
| WP7 | Polish & Production Readiness | 26 | 41 | 15% |
| WP8 | Project Cross-Cutting | n/a | 68 | 24% |
| **Total** | | **147** | **~274 PD** | **100%** |

### Effort by role (allocation across the project)

| Role | PD allocation | % of total | Sprints engaged |
|------|--------------:|-----------:|-----------------|
| Tech Lead / Architect | 65 | 24% | 1–9 |
| Senior .NET Engineer #1 | 70 | 25% | 1–9 |
| Senior .NET Engineer #2 | 65 | 24% | 1–9 |
| Cloud / DevOps Engineer | 45 | 16% | 1 (light) · 6–9 (heavy) |
| ML / AI Engineer | 18 | 7% | 3–4 (heavy), 7–8 (light) |
| QA / SDET | 25 | 9% | 2–9 |
| Security / Privacy Engineer (PT) | 8 | 3% | 1, 4, 7, 9 |
| Product Manager (PT) | (separate) | — | 1–9 |
| **Total build allocation** | **~296 PD** | | (slack: ~22 PD covers vacation + ceremony float) |

*Allocation > 274 PD reflects overlap and float; actual chargeable build is ~274 PD.*

---

## 6. Team Composition & Capacity

### Proposed team (average 5.75 FTE, peak 6.75 FTE)

| Role | FTE | When | Responsibilities | Key WPs |
|------|----:|------|------------------|---------|
| **Tech Lead / Architect** | 1.0 | All sprints | Architecture stewardship, code review, Walmart liaison, ~50% hands-on coding | WP2, WP3, WP7 |
| **Senior .NET Engineer #1** | 1.0 | All sprints | Core domain + services + assessment orchestration | WP1–WP6 |
| **Senior .NET Engineer #2** | 1.0 | All sprints | Infrastructure + AI clients + repositories | WP2.3, WP3.1, WP4, WP6 |
| **Cloud / DevOps Engineer** | 1.0 | Sprint 1 (light), 6–9 (full) | Bicep, GitHub Actions, ACA, observability | WP1 setup, WP7.1–7.3 |
| **ML / AI Engineer** | 0.5 | Sprints 3–4 (peak), 7–8 (light) | Prompt engineering, H1 accuracy spike, model card, drift evaluation | WP3.1, WP3.3, WP7.5 |
| **QA / SDET** | 1.0 | Sprints 2–9 | Test automation, NBomber, chaos tests, E2E smoke | WP3.8, WP7.4 |
| **Security / Privacy Engineer** | 0.25 | Sprints 1, 4, 7, 9 | Threat model updates, DPIA, Bicep hardening review | WP2.5, WP7.1, WP7.5 |
| **Product Manager** | 0.5 | All sprints | Backlog, stakeholders, KPI tracking, go-live readiness | All |
| **Engineering Manager / Delivery Lead** | 0.25 | All sprints | Risk + capacity tracking, reporting | All |

### Sprint capacity model

- **Sprint length**: 10 working days (2 weeks)
- **Sprint capacity per FTE** (net of ceremony/PR review): ~6.5 PD
- **Hands-on coding capacity per sprint** (Tech Lead 0.5 + SDE1 + SDE2 + DevOps + ML 0.5 + QA from sprint 2):
  - Sprint 1: 0.5 + 1 + 1 + 0.5 + 0 + 0 = 3.0 FTE → **~20 PD/sprint**
  - Sprints 2: 0.5 + 1 + 1 + 0.5 + 0 + 1 = 4.0 FTE → **~26 PD/sprint**
  - Sprints 3–4: 0.5 + 1 + 1 + 0.25 + 0.5 + 1 = 4.25 FTE → **~28 PD/sprint**
  - Sprints 5–6: 0.5 + 1 + 1 + 0.75 + 0 + 1 = 4.25 FTE → **~28 PD/sprint**
  - Sprints 7–8: 0.5 + 1 + 1 + 1 + 0.25 + 1 = 4.75 FTE → **~31 PD/sprint**
  - Sprint 9: 0.5 + 1 + 1 + 0.5 + 0 + 1 = 4.0 FTE → **~26 PD/sprint**
- **Total capacity** over 9 sprints: ~240 PD pure coding + ~30 PD ceremony already netted out

### Capacity-vs-load reconciliation

- Build effort (WP1–7): ~206 PD
- Available coding capacity over 9 sprints: ~240 PD
- Headroom: **~34 PD (≈ 14%)** for spikes, integration friction, and Walmart-side dependencies
- WP8 ceremony (30 PD) and defect buffer (30 PD) are **already netted out** of FTE capacity above

This implies the plan is **feasible but not slack-heavy**. Any of these will push the timeline:

- H1 contingency (3DLOOK bridge): **+2 weeks**
- Walmart catalog data feed delays for US4: **+1 week**
- Coverage gate enforcement causing rework: **+0.5–1 week**

---

## 7. Timeline & Sprint Plan

### Sprint-by-sprint allocation

| Sprint | Weeks | Primary work packages | Output / milestone | Gate |
|:------:|:-----:|----------------------|--------------------|------|
| **1** | 1–2 | WP1 complete + WP2.1, 2.2, partial 2.3, 2.5 | Solution scaffolded; domain + interfaces; auth middleware skeleton | — |
| **2** | 3–4 | WP2.3, 2.4, 2.5, 2.6, 2.7 complete | **Foundational platform done**; resilience pipelines, health probes, Aspire wired | 🚩 **H7 gate** — AI failover < 5s |
| **3** | 5–6 | WP3.1, 3.2, 3.3 (incl. H1 spike) | AI clients online; image validation in place; **accuracy spike result** | 🚩 **H1 gate** — measurement ±2–4 cm |
| **4** | 7–8 | WP3.4, 3.5, 3.6, 3.7, 3.8 complete + WP5 start | **MVP demoable**: POST `/assessments` returns 5-point fit; tests green | 🚩 **MVP demo to Walmart** |
| **5** | 9–10 | WP4 complete + WP5 complete | Profile CRUD + by-profile endpoint live; OpenAPI contract validated | — |
| **6** | 11–12 | WP6 complete + WP7.1 start (Bicep modules) | Garment ingestion live (single + batch); Bicep modules ~50% | — |
| **7** | 13–14 | WP7.1 complete + WP7.2 + WP7.3 | IaC complete (dev/staging/prod parameter files); CI workflow operational; alerts + runbooks | — |
| **8** | 15–16 | WP7.4 (load + chaos) + WP7.5 (docs) | **NBomber 500-concurrent run passes** (p95 < 5s); chaos tests validate degradation ladder; model card + DR plan | 🚩 **H3, H5, H8 gates** |
| **9** | 17–18 | UAT, fix-it, security sign-off, go-live readiness | Smoke tests on staging → prod canary 5% → 25% → 100% | 🚩 **Production go-live** |

### Gantt-style overview

```text
Sprint:           1     2     3     4     5     6     7     8     9
                 ┌──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐
WP1 Setup        │█████ │      │      │      │      │      │      │      │      │
WP2 Foundation   │██████│██████│      │      │      │      │      │      │      │
WP3 US1 (MVP)    │      │      │██████│██████│      │      │      │      │      │
WP4 US2          │      │      │      │      │██████│      │      │      │      │
WP5 US3          │      │      │      │██████│██████│      │      │      │      │
WP6 US4          │      │      │      │      │      │██████│      │      │      │
WP7 Polish       │      │      │      │      │      │██████│██████│██████│      │
WP8 Cross-cut    │██████│██████│██████│██████│██████│██████│██████│██████│██████│
Go-live readiness│      │      │      │      │      │      │      │      │██████│
                 └──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┘
Gates:                  H7              H1   MVP                          H3/5/8 GO-LIVE
                                              demo
```

### Key milestones

| # | Milestone | Sprint end | Acceptance |
|---|-----------|:----------:|-----------|
| M1 | Foundational platform ready (H7 cleared) | 2 | AI failover < 5s in integration test; all probes responding; resilience pipelines registered |
| M2 | H1 accuracy gate cleared | 3 | ≤ 15% of test photos > ±4 cm vs. ground truth on calibration set |
| M3 | **MVP demo** (US1 end-to-end) | 4 | Photo + height → fit response via live API; degradation ladder tested |
| M4 | All user stories feature-complete | 6 | US1–US4 all pass acceptance criteria in staging |
| M5 | Production-ready infra | 7 | dev / staging / prod deployable via Bicep; CI gates green |
| M6 | Load + chaos validated | 8 | NBomber 500-concurrent p95 < 5s; chaos tests show > 90% request success in partial outage |
| M7 | **Production go-live** | 9 | Canary 100% reached; SLO dashboard green for 24h; runbooks signed off |

---

## 8. Hypothesis & Quality Gates

Per the [Hypothesis Validation Plan](../specs/001-clothing-fit-assessment/plan.md#hypothesis-validation-plan). Each gate is a formal go/no-go review.

| Gate | Sprint | Owner | Pass criteria | Fail → contingency |
|------|:------:|-------|---------------|---------------------|
| **H7** AI failover detection | 2 | Tech Lead | Failover < 5s in integration test under simulated primary outage | Switch to active-active configuration (+1 sprint) |
| **H1** GPT-5.2 measurement accuracy | 3 | ML Engineer | ≤ 15% of calibration photos outside ±4 cm; reproducibility ≥ 90% | Engage 3DLOOK as bridge; defer Tier 3 SMPL to v2 (+2 weeks) |
| **MVP gate** | 4 | PM + Tech Lead | All US1 acceptance criteria pass; demo to Walmart | Replan US2–US4 in next sprint |
| **H3, H5** Load behaviour | 8 | DevOps + QA | NBomber 500-concurrent p95 < 5s, no OOM, KEDA scales correctly | Tune KEDA target / memory; +0.5–1 sprint |
| **H8** Degradation success rate | 8 | QA | > 90% request success during chaos / partial AI outage | Revisit L4/L5 strategy; expand cached profile fallback (+0.5 sprint) |
| **Coverage gate** | 7–9 | Tech Lead | ≥ 80% line, ≥ 90% on critical paths | Backlog test debt; risk-based deferral with PM sign-off |
| **Security sign-off** | 9 | Security Engineer | SAST/SCA clean; SBOM signed; threat-model items closed | Block go-live; remediate |
| **Privacy sign-off** | 9 | Privacy Engineer | DPIA approved; 24h delete SLA verified; transient blob purge confirmed | Block go-live; remediate |

---

## 9. Dependencies & Critical Path

### Internal critical path

```text
WP1 → WP2.3 (Cosmos repo) → WP2.4 (resilience) → WP2.5 (auth/middleware) →
WP3.1 (AI clients) → WP3.3 (H1 spike) → WP3.5 (orchestration) → WP3.6 (controller) →
US1 MVP → WP7.4 (load tests) → Go-live
```

Critical-path slack is **minimal between Sprints 2–4**. Any slip in WP2.4 (resilience) or WP3.3 (H1) cascades directly to MVP demo.

### External dependencies

| Dependency | Owner | Needed by | Status | Mitigation |
|------------|-------|:---------:|:------:|-----------|
| Walmart Azure subscription + RBAC + Entra ID tenant | Walmart Cloud Platform | Sprint 1 | TBD | Engage at project kickoff; fallback to dev MSDN subscription for first sprint |
| Azure OpenAI capacity / PTU allocation (GPT-5.2) | Microsoft Azure account team | Sprint 3 | TBD | PAYG with quota request; PTU upgrade pre-Sprint 9 |
| Florence-2 endpoint quota in AI Foundry | Microsoft | Sprint 3 | TBD | Serverless with managed-endpoint upgrade path |
| Walmart garment catalog feed (sample data) | Walmart Catalog Engineering | Sprint 5 | TBD | Synthetic catalog for US4 dev; real feed in Sprint 6 |
| Walmart Privacy Office DPIA review slot | Walmart Privacy Office | Sprint 4 + Sprint 8 | TBD | Book at project kickoff; iterate on findings |
| Walmart Platform Engineering integration review | Walmart Platform Eng | Sprint 7 | TBD | Share OpenAPI early (end of Sprint 3) |
| Notation signing keys + container registry | Walmart DevSecOps | Sprint 7 | TBD | Use project-owned registry until handover |

---

## 10. Risks to the Plan

(See also [risk-register.md](architecture/risk-register.md) for technical risks. These are **delivery / plan risks**.)

| ID | Risk | Likelihood | Impact | Severity | Mitigation |
|----|------|:----------:|:------:|:--------:|-----------|
| PR-1 | H1 (GPT-5.2 accuracy) fails | Medium | High | **HIGH** | Pre-Sprint 3 prompt engineering spike + calibration dataset prepared in Sprint 2 |
| PR-2 | Walmart Azure tenant provisioning delayed | Medium | High | **HIGH** | Run Sprint 1 against dev MSDN subscription; promote to Walmart tenant in Sprint 2 |
| PR-3 | Single tech lead becomes bottleneck on PR reviews | High | Medium | **HIGH** | Reserve 25% of Tech Lead time strictly for reviews; SDEs cross-review |
| PR-4 | DPIA / Privacy review finds blockers late | Low | High | MEDIUM | Sprint 4 mid-project privacy checkpoint; Sprint 8 final review |
| PR-5 | Bicep IaC complexity higher than estimated (12 modules) | Medium | Medium | MEDIUM | Reserve full DevOps FTE from Sprint 6; pair with Security Engineer for hardening |
| PR-6 | Walmart catalog feed delayed beyond Sprint 5 | Medium | Medium | MEDIUM | Synthetic catalog covers US4 dev; defer real-feed integration test to Sprint 8 |
| PR-7 | ML engineer unavailable during H1 spike | Low | High | MEDIUM | Identify backup ML resource in advance; Tech Lead has prompt-engineering fallback skill |
| PR-8 | NBomber load test reveals architecture rework | Low | High | MEDIUM | Sprint 7 buffer; KEDA target tunable without redeploy |
| PR-9 | Coverage gate (80% / 90%) drives last-minute rework | Medium | Medium | MEDIUM | TDD enforced from Sprint 3; weekly coverage report in CI |
| PR-10 | Holiday / vacation impact (project crosses calendar boundaries) | Medium | Medium | MEDIUM | 14% headroom budget absorbs typical PTO; rebaseline if > 20% of team OOO simultaneously |

---

## 11. Reporting & Governance

| Cadence | Forum | Audience | Output |
|---------|-------|----------|--------|
| Daily | Stand-up (15 min) | Build team | Blockers, today's plan |
| Weekly | Architecture sync (30 min) | Tech Lead + Architect + Security | ADR updates, design decisions |
| Bi-weekly | Sprint review + retro | Build team + PM + Walmart contact | Demo, velocity, action items |
| Monthly | Steering / risk review | Sponsors + PM + Tech Lead + Walmart leads | Risk register, hypothesis status, capacity vs plan |
| Per gate | Hypothesis review | Tech Lead + ML + sponsors | Go / no-go decision, recorded in [risk-register.md](architecture/risk-register.md) |
| Per release | Change Advisory review | PM + Tech Lead + Walmart Change Mgmt | Canary plan, rollback rehearsal, sign-offs |

**KPIs tracked weekly**:

- Velocity (PD completed vs. plan)
- Defect escape rate (post-merge bugs / sprint)
- Build success rate (CI green / total builds)
- Coverage trend (line + critical-path)
- Risk register movement (new / closed / severity changes)

---

## 12. Assumptions

1. Team members are **senior** (5+ years .NET / Azure). Junior-heavy team requires re-baseline at ×1.3–1.5.
2. Azure subscriptions and quotas are available by Sprint 1; otherwise Sprint 1 falls back to dev MSDN.
3. GPT-5.2 Vision pricing is at or near GPT-4o equivalent; enterprise agreement applies separately.
4. Walmart's Platform Engineering and Catalog Engineering are responsive within 2 business days for integration questions.
5. No major architecture pivot post-Sprint 2 (e.g., abandoning ACA for AKS would add ~1 sprint).
6. CI/CD compute is GitHub Actions cloud-hosted runners; self-hosted runners add ~0.5 sprint setup.
7. Constitutional gates in `plan.md` are enforceable in CI; deviations require explicit PR sign-off, not silent override.
8. Single region (East US 2) is acceptable for v1; multi-region SLO uplift is out of scope.
9. Defect and UAT buffer of 15% (WP8.2) is sufficient. Historically, AI-integration projects often need 20–25%; revisit at Sprint 5 retro.
10. Stakeholder demos happen biweekly with no major reprioritization mid-sprint. If Walmart introduces new requirements, they enter the backlog for the **next** sprint and may push scope to v1.1.

---

## Appendix A — Estimating Reference

| Size | PD range | Example tasks |
|:----:|:--------:|--------------|
| **S** | 0.25 – 0.5 | Enum, DTO, interface stub, config file, single-class data structure |
| **M** | 1 – 2 | Repository class, controller endpoint, single middleware, unit-test class |
| **L** | 2 – 4 | Resilience pipeline, AI client wrapper with failover, service orchestration class, Bicep module |
| **XL** | 3 – 5 | Degradation ladder integration, NBomber load suite, chaos test harness, IaC root composition |

Estimates assume:

- A working development environment from day 1 (covered in WP1)
- Pair-programming or PR review for any task ≥ L
- Test code authored alongside production code (TDD)
- Documentation co-located with code (XML doc comments) and updated in-flight

---

## Appendix B — How to use this plan

1. **At project kickoff**: use Sections 4–7 to onboard the team, claim WPs, set up the sprint board.
2. **At every sprint planning**: pull tasks from the WP for that sprint; verify WP8 ceremony / defect float is preserved.
3. **At every sprint review**: report velocity vs. plan in PD; update Section 5 actuals (a tracking column should be added).
4. **At every gate (H1, H7, etc.)**: go/no-go review using Section 8; record decision in `journal.md`.
5. **At every risk review**: re-rate PR-1 through PR-10 in Section 10; trigger mitigations as needed.
6. **At go-live**: archive this plan, snapshot actuals vs. estimates, and use the variance to recalibrate the next feature's plan.

---

*This plan reflects the architecture, risks, and tasks documented in this repository as of 2026-05-14. It must be re-baselined if scope, team, or external dependencies change materially.*

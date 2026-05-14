# Statement of Work — VirtualMirror AI Clothing Fit Assessment Service

| Field | Value |
|-------|-------|
| **Document** | Virtual-Mirror-SOW.md |
| **Version** | 0.1.0 |
| **Status** | Draft for internal review |
| **Date** | 2026-05-14 |
| **Prepared for** | Walmart Digital — Apparel & Marketplace |
| **Prepared by** | Microsoft Industry Solutions Delivery (ISD) |
| **Engagement** | VirtualMirror AI — Photo-based Fit Assessment (v1) |
| **Reference** | Feature branch `001-clothing-fit-assessment`; Workshop deliverable EX3 |
| **Validity** | This proposal is valid for 30 days from the date above |

> Every line item in this SOW traces back to a discovery artifact in this repository — `docs/Sessions/Problem-statement.md`, `docs/Sessions/Product-definition.md`, `specs/001-clothing-fit-assessment/`, `docs/architecture/`, and `docs/project-plan.md`. Where a section reflects a Microsoft default rather than a discovery finding, the rationale is called out explicitly as an assumption.

---

## Table of Contents

1. [Document Control](#1-document-control)
2. [Introduction](#2-introduction)
3. [Objectives and Scope](#3-objectives-and-scope)
4. [Structured Scope (Epics / Workstreams)](#4-structured-scope-epics--workstreams)
5. [Out of Scope](#5-out-of-scope)
6. [Delivery Approach](#6-delivery-approach)
7. [Timeline and Capacity Model](#7-timeline-and-capacity-model)
8. [Organization and Roles](#8-organization-and-roles)
9. [Governance Framework](#9-governance-framework)
10. [Delivery Execution (Sprint Model)](#10-delivery-execution-sprint-model)
11. [Testing and Quality Management](#11-testing-and-quality-management)
12. [Change Management](#12-change-management)
13. [Risk and Issue Management](#13-risk-and-issue-management)
14. [Escalation Path](#14-escalation-path)
15. [Work Products and Deliverables](#15-work-products-and-deliverables)
16. [Technical and Environment Requirements](#16-technical-and-environment-requirements)
17. [Customer Responsibilities](#17-customer-responsibilities)
18. [Assumptions](#18-assumptions)
19. [Program / Project Completion Criteria](#19-program--project-completion-criteria)
20. [Appendices and Supporting Material](#20-appendices-and-supporting-material)
21. [Worksheet A — SOW Header + Outcomes](#worksheet-a--sow-header--outcomes)
22. [Worksheet B — Deliverables, Acceptance Criteria, and Work Packages](#worksheet-b--deliverables-acceptance-criteria-and-work-packages)
23. [Version History](#version-history)

---

## 1. Document Control

| Item | Value |
|------|-------|
| Project / Program name | VirtualMirror AI — Clothing Fit Assessment Service (v1) |
| Customer | Walmart Digital — Apparel & Marketplace |
| Provider | Microsoft Industry Solutions Delivery (ISD) |
| Version | 0.1.0 |
| Status | Draft for internal review |
| Date | 2026-05-14 |
| Work Order reference | TBD upon countersignature |
| Validity / expiration | 30 days from the date above |
| Companion artifacts | [project-plan.md](project-plan.md) · [solution-architecture.md](architecture/solution-architecture.md) · [cost-estimate.md](architecture/cost-estimate.md) · [risk-register.md](architecture/risk-register.md) · [threat-model.md](architecture/threat-model.md) · [spec.md](../specs/001-clothing-fit-assessment/spec.md) |

---

## 2. Introduction

### 2.1 Context

Walmart is the **3rd-largest U.S. apparel e-commerce retailer** with **$14.7B in online clothing revenue (2024)**. Industry online apparel return rates run at **24–26%**, with **~53–70% driven by fit and sizing** — an estimated **$200–400M in annual avoidable cost** at Walmart's volume from fit-related returns alone (processing, reverse logistics, restocking, markdowns, and write-offs). Walmart already invested in **Zeekit** for virtual try-on visualization ("how does it look on me?") but shoppers still lack **measurement-based fit confidence** ("will it actually fit my body?"). This is the gap VirtualMirror AI closes.

*Source: [README.md](../README.md), [Sessions/Product-definition.md](Sessions/Product-definition.md) — Market Sizing & Addressable Savings.*

### 2.2 Purpose of Engagement

Microsoft ISD will partner with Walmart Digital to **design, build, harden, and go-live** a multi-tenant, API-first clothing fit assessment service on Azure. The engagement covers the v1 scope defined in feature branch `001-clothing-fit-assessment` — photo + height in, 5-point fit recommendation out — including the three-tier AI pipeline (Florence-2, Azure AI Content Safety, Azure OpenAI GPT-5.2 Vision), supporting data and identity services, observability, IaC, CI/CD, load and chaos validation, and a documented frontend integration contract.

The collaboration model is **joint delivery**: Microsoft executes within the agreed capacity, while Walmart's Product Owner prioritises the backlog and Walmart's Catalog, Platform Engineering, Privacy Office, and DevSecOps teams provide inputs, reviews, and acceptance.

### 2.3 Engagement Model

| Attribute | Value |
|-----------|-------|
| Engagement type | Agile, **fixed capacity + variable scope** within a defined backlog |
| Program vs project | Single project, single workstream |
| Team structure | One feature team (~5.75 FTE average) |
| Delivery cadence | 2-week sprints, 9 sprints planned (18 calendar weeks) |
| Pricing model | Time & materials within fixed-capacity envelope; not-to-exceed clause negotiated at Work Order signature |

*Source: [project-plan.md](project-plan.md) §3 Delivery Model.*

---

## 3. Objectives and Scope

### 3.1 Business Objectives (customer-owned, measurable)

These objectives **guide planning but are not contractually guaranteed within capacity**. Microsoft will instrument the service for measurement so Walmart can validate post-launch.

| ID | Objective | Measure | Target |
|----|-----------|---------|--------|
| BO-1 | Reduce fit-driven apparel returns | Return rate for SKUs where VirtualMirror was used, vs. control | **≥ 20% reduction** within 6 months of launch (target 30%) |
| BO-2 | Increase shopper conversion confidence on apparel PDPs | Add-to-cart and checkout conversion delta on enabled SKUs | **+3–5% conversion lift** within 6 months |
| BO-3 | Establish a reusable, multi-tenant fit assessment platform | Number of tenants onboarded with isolated data planes | **≥ 1 (Walmart) at GA**, architected for 20+ at Scale tier |

*Source: [Sessions/Product-definition.md](Sessions/Product-definition.md) — Success Metrics; [spec.md](../specs/001-clothing-fit-assessment/spec.md) — SC-002, SC-003.*

**Non-guarantee clause**: Business outcomes BO-1 and BO-2 depend on factors outside Microsoft's control (shopper adoption, merchandising decisions, Walmart marketing of the feature, catalog data quality). Microsoft commits to **delivering the capability and the measurement framework** to track these outcomes.

### 3.2 Value Themes

| Theme | Where it shows up |
|-------|-------------------|
| Data & AI enablement | Three-tier AI pipeline (Florence-2, Content Safety, GPT-5.2 Vision) with degradation ladder |
| Platform enablement | Multi-tenant Azure-native service with golden-path alignment |
| Application delivery | New ASP.NET Core 8 service on Azure Container Apps with OpenAPI contract |
| Security & governance | OWASP ASVS L2, PCI-DSS-adjacent posture, SOC 2 TSC mapping, NIST CSF 2.0 alignment, DPIA |
| Operational efficiency | Auto-scale 2–10 instances; estimated $0.012–$0.018 per assessment; observability + SLO dashboards |

*Source: [Sessions/Product-definition.md](Sessions/Product-definition.md) — Compliance & Industry Baseline Alignment; [cost-estimate.md](architecture/cost-estimate.md).*

### 3.3 Scope Model

- **Variable scope** governed by a single product backlog (epics defined in §4) and refined sprint-by-sprint.
- **Capacity-driven**: Microsoft delivers within ~274 person-days of build effort across 9 sprints with the team in §8.
- **Ownership**:
  - Walmart Product Owner prioritises the backlog.
  - Microsoft executes within capacity and flags items at risk of slipping the cutline.
- **MVP cutline** is end of Sprint 4 (foundational platform + photo-based fit assessment); **GA cutline** is end of Sprint 9.

---

## 4. Structured Scope (Epics / Workstreams)

The build is organised into **eight work packages (WP1–WP8)** that map to the implementation phases in `specs/001-clothing-fit-assessment/tasks.md`. Effort and acceptance criteria are detailed in [Worksheet B](#worksheet-b--deliverables-acceptance-criteria-and-work-packages).

| WP | Workstream | Epic category | Purpose |
|:--:|------------|---------------|---------|
| WP1 | Setup & Scaffolding | Foundation / Baseline / Intake | .NET solution, project skeletons, Directory.Build.props, docker-compose for Cosmos emulator + Azurite |
| WP2 | Foundational Platform | Architecture & Platform · Security & Identity | Domain models, interfaces, Cosmos/Blob/Audit/Service-Bus repositories, Polly resilience pipelines + AI failover, Entra ID auth middleware, health probes, Aspire orchestration |
| WP3 | US1 — Photo-Based Fit Assessment (MVP) | Core Build / Execution | Florence-2 + Content Safety + GPT-5.2 Vision clients, image validation pipeline, measurement extraction (H1 spike), fit comparison engine, assessment orchestration with L1–L5 degradation ladder |
| WP4 | US2 — Measurement Profile Storage | Core Build / Execution | Opt-in profile CRUD with 24h hard-delete SLA and consent capture |
| WP5 | US3 — Frontend Integration Layer | Core Build / Execution | OpenAPI 3.x docs (Swashbuckle), URI versioning, CORS, contract tests against `contracts/openapi.yaml` |
| WP6 | US4 — Garment Data Ingestion | Core Build / Execution | Single + batch garment ingestion (up to 100 items), version history, partial-failure semantics |
| WP7 | Polish & Production Readiness | Governance & Monitoring · Knowledge Transfer | 12 Bicep modules + 3 environment parameter files, GitHub Actions CI with SAST/SCA/SBOM/Trivy/Notation, alert rules + 3 runbooks, NBomber 500-concurrent load test, chaos tests, model card, DR plan |
| WP8 | Project Cross-Cutting | Governance | Ceremony, PR review, defect/UAT buffer, Walmart integration alignment, security & privacy review, PM and backlog management |

**Scope characteristics**: non-fixed, continuously reprioritised; the backlog drives sprint execution and delivery sequence. Tasks for each WP are pre-decomposed in [`tasks.md`](../specs/001-clothing-fit-assessment/tasks.md) (147 tasks; T001–T147).

*Source: [project-plan.md](project-plan.md) §4 WBS.*

---

## 5. Out of Scope

The following items are **explicitly excluded** from this engagement. Inclusion requires a Change Order (see §12).

| Category | Excluded item | Why |
|----------|--------------|-----|
| Architecture | Multi-region active-active deployment (target ~99.95% composite SLA) | Deferred to v2; single-region East US 2 in v1 |
| AI | Custom SMPL 3D body-model on Azure AI Foundry (Tier 3) | Deferred to v2 contingent on H1 outcome |
| Mobile | Native iOS/Android SDK and on-device inference (Concept B) | Deferred to v2 |
| Analytics | Microsoft Fabric intelligence loop / order-history-driven sizing (Concept C) | Deferred to v3 |
| Integration | Direct Zeekit integration | Post-v1 partnership work |
| Catalog | Automated supplier-feed ingestion / data cleansing of historical catalog | v1 uses manual catalog import via `POST /v1/garments` |
| Operations | Production support, on-call coverage, and operations beyond go-live + 30-day hypercare | Separate managed-services SOW |
| Change management | End-user training, in-store enablement, organisational change management | Walmart-owned |
| Performance | Customer-owned performance testing beyond Microsoft's NBomber sprint-8 run | Walmart Platform Eng owns ongoing perf testing |
| Hardware | Hardware / infrastructure provisioning beyond Azure resources | All compute is Azure-native |
| Third-party | Product licenses, subscriptions, or third-party SaaS implementations not listed in §16 | Walmart procures and grants access |
| Storefront | Walmart PDP UI implementation, A/B experimentation harness, or Zeekit widget changes | Walmart frontend team owns; Microsoft delivers reference SDK only if added via Change Order |

*Source: [project-plan.md](project-plan.md) §2; [Sessions/Product-definition.md](Sessions/Product-definition.md) — Scope Boundaries.*

---

## 6. Delivery Approach

### 6.1 Methodology

- **Agile Scrum** with 2-week sprints (Walmart Platform Engineering golden-path cadence).
- **Fixed capacity + variable scope**: Microsoft delivers ~274 PD of build effort over 9 sprints; backlog is reprioritised at each sprint planning.
- **Trunk-based development** with short-lived feature branches and feature flags via Azure App Configuration to enable canary rollout.
- **TDD** enforced from Sprint 3 onward per the repository constitution (Principle V) — Red → Green → Refactor with Verify snapshot tests around AI integration.

### 6.2 Core Mechanics

| Artifact | Owner | Purpose |
|----------|-------|---------|
| Product backlog | Walmart PO | Single source of prioritised work |
| Sprint backlog | Microsoft team | Sprint commitment |
| Sprint review demo | Tech Lead | Walk-through of working software every 2 weeks |
| Retrospective | Microsoft PM / Walmart DM | Continuous improvement |
| Risk register | Microsoft PM | Reviewed monthly; escalations weekly if HIGH+ |
| Roadmap / burn chart | Microsoft PM | Updated weekly |

### 6.3 Delivery Phases

| Phase | Sprints | Focus |
|-------|:-------:|-------|
| **Initiation** | 1 | Solution scaffolding, Walmart environment access, baseline planning |
| **Baseline build** | 2 | Foundational platform; H7 (AI failover) gate |
| **MVP build** | 3–4 | US1 photo-based fit assessment; H1 (measurement accuracy) gate; MVP demo |
| **Feature complete** | 5–6 | US2 profile storage, US3 frontend integration, US4 garment ingestion |
| **Hardening** | 7–8 | Bicep IaC, CI/CD, observability, NBomber 500-concurrent load + chaos; H3/H5/H8 gates |
| **Go-live** | 9 | UAT, security + privacy sign-off, canary 5% → 25% → 100%; production cutover |
| **Hypercare** | +2 weeks post Sprint 9 | Stabilisation and runbook handover (covered under WP8 buffer) |

### 6.4 Promotion Gates

```
dev (auto on merge) → staging (Sprint review approval) →
prod (PO + Security + Privacy sign-off + canary 5% → 25% → 100%; rollback < 15 min)
```

*Source: [project-plan.md](project-plan.md) §3 Delivery Model, §7 Sprint Plan.*

---

## 7. Timeline and Capacity Model

This is a **relative timeline**, not a fixed commitment. The timeline adapts as scope and capacity change (per change-management process in §12).

| Sprint | Calendar weeks | Headline output | Gate |
|:------:|:---:|------------------|------|
| 1 | 1–2 | Solution scaffolded; domain + interfaces; auth middleware skeleton | — |
| 2 | 3–4 | Foundational platform done; resilience pipelines, health probes, Aspire wired | 🚩 **H7** — AI failover < 5 s |
| 3 | 5–6 | AI clients online; image validation in place; accuracy spike result | 🚩 **H1** — measurement ±2–4 cm |
| 4 | 7–8 | **MVP demoable**: `POST /v1/assessments` returns 5-point fit; tests green | 🚩 **MVP demo to Walmart** |
| 5 | 9–10 | Profile CRUD + `by-profile` endpoint live; OpenAPI contract validated | — |
| 6 | 11–12 | Garment ingestion live (single + batch); Bicep modules ~50% | — |
| 7 | 13–14 | IaC complete (dev/staging/prod); CI workflow operational; alerts + runbooks | — |
| 8 | 15–16 | NBomber 500-concurrent passes (p95 < 5 s); chaos tests validate degradation ladder; model card + DR plan | 🚩 **H3, H5, H8** |
| 9 | 17–18 | UAT, fix-it, security + privacy sign-off, canary 5% → 25% → 100% | 🚩 **Production go-live** |

**Calendar duration**: **18 weeks** (9 × 2-week sprints).
**Hypercare**: 2 calendar weeks post-go-live, absorbed in WP8 buffer.

### Capacity model

| Field | Value |
|-------|-------|
| Total build effort (WP1–WP7) | ~206 PD |
| Cross-cutting (WP8) | ~68 PD |
| **Total estimated effort** | **~274 PD** (~55 person-weeks) |
| Average team size | 5.75 FTE (peak 6.75 FTE during Bicep + load test sprints 7–8) |
| Coding capacity available across 9 sprints | ~240 PD net of ceremony |
| Headroom | ~14% (~34 PD) for spikes and integration friction |
| Estimation method | Bottom-up, three-point reference scale calibrated to senior .NET/Azure engineer productivity, +15% ceremony, +15% defect/UAT buffer |

*Source: [project-plan.md](project-plan.md) §5 Effort Summary, §6 Team Capacity.*

---

## 8. Organization and Roles

### 8.1 Structural Model

```
Executive Steering Committee  (monthly)
       |
       v
Program Governance — Walmart Product Council + Microsoft Delivery Mgmt  (bi-weekly)
       |
       v
Feature team  (Microsoft + Walmart stakeholders)  (daily / sprint cadence)
```

### 8.2 Microsoft Delivery Roles

| Role | FTE | Engaged | Responsibilities |
|------|----:|---------|------------------|
| Engagement Lead / Delivery Management Executive | 0.25 | All sprints | Customer relationship, executive escalation, contract |
| Tech Lead / Solution Architect | 1.0 | All sprints | Architecture stewardship, code review, ~50% hands-on coding, Walmart liaison |
| Senior .NET Engineer #1 | 1.0 | All sprints | Core domain + services + assessment orchestration |
| Senior .NET Engineer #2 | 1.0 | All sprints | Infrastructure + AI clients + repositories |
| Cloud / DevOps Engineer | 1.0 | Sprint 1 light · 6–9 heavy | Bicep, GitHub Actions, ACA, observability |
| ML / AI Engineer | 0.5 | Sprints 3–4 peak · 7–8 light | Prompt engineering, H1 accuracy spike, model card, drift evaluation |
| QA / SDET | 1.0 | Sprints 2–9 | Test automation, NBomber, chaos tests, E2E smoke |
| Security / Privacy Engineer (PT) | 0.25 | Sprints 1, 4, 7, 9 | Threat model updates, DPIA, Bicep hardening review |
| Consulting Product Delivery Manager (CPdM) / Project Manager | 0.5 | All sprints | Backlog, stakeholders, KPI tracking, go-live readiness, risk + capacity tracking |

*Source: [project-plan.md](project-plan.md) §6 Team Composition.*

### 8.3 Customer (Walmart) Roles

| Role | Engagement | Responsibility |
|------|------------|---------------|
| Executive Sponsor | Steering Committee | Strategic alignment, scope adjudication |
| Product Owner (critical) | Daily / weekly | Backlog prioritisation, acceptance of demos |
| Catalog Engineering SME | Sprints 5–8 | Garment data, schema mapping (US4) |
| Platform Engineering SME | Sprints 1, 7 | Azure landing zone, golden-path standards, container registry handover |
| Privacy Office | Sprints 4, 8, 9 | DPIA review and approval |
| DevSecOps | Sprints 7, 9 | Notation signing keys, container registry, security sign-off |
| Frontend / PDP team | Sprints 4–9 | Consume OpenAPI contract, integration UAT |
| Identity / Entra ID admin | Sprint 1 | App registrations, scopes, RBAC |

*Source: [project-plan.md](project-plan.md) §9 External Dependencies.*

---

## 9. Governance Framework

### 9.1 Governance Bodies

| Body | Cadence | Membership |
|------|---------|------------|
| Executive Steering Committee | Monthly | Walmart Exec Sponsor, Microsoft Engagement Lead, Walmart Product VP |
| Product Council / Program Governance | Bi-weekly | Walmart PO, Microsoft Tech Lead, Microsoft PM, Walmart Platform Eng lead |
| Architecture Review (optional) | Per ADR | Microsoft Tech Lead, Walmart Architect (if assigned) |
| Daily team sync | Daily 15 min | Microsoft delivery team + Walmart PO (optional) |

### 9.2 Governance Functions

- Strategy and outcome alignment (SC and BO-1/2/3)
- Backlog prioritisation (Product Council)
- Issue resolution within defined SLA (see §14)
- Decision authority for scope, capacity, and timeline adjustments

### 9.3 Communication Model

| Artifact | Frequency | Owner |
|----------|-----------|-------|
| Sprint review demo | Every 2 weeks | Microsoft Tech Lead |
| Status report (RAG + burn chart + risks) | Weekly | Microsoft PM |
| Stakeholder review with Walmart Catalog / Platform / Privacy | Every 4 weeks | Microsoft PM |
| Communication plan | One-time at kickoff | Microsoft PM |
| Architecture Decision Records (ADRs) | As decided | Microsoft Tech Lead → committed to `docs/architecture/decision-register.md` |

---

## 10. Delivery Execution (Sprint Model)

### 10.1 Sprint Activities

| Ceremony | Duration | Participants |
|----------|----------|--------------|
| Sprint planning | 2 h | Full team + Walmart PO |
| Daily standup | 15 min | Microsoft team (Walmart optional) |
| Backlog refinement | 1 h / week | Tech Lead, PM, Walmart PO |
| Sprint review / demo | 1 h | Full team + stakeholders |
| Retrospective | 1 h | Microsoft team |
| Architecture sync | 1 h / week | Tech Lead, ML Eng, DevOps |
| Risk review | 30 min / month | PM, Tech Lead, Walmart PO |

### 10.2 Key Artifacts

| Artifact | Location |
|----------|----------|
| Product backlog | Walmart's tracking tool (Azure DevOps assumed) |
| Sprint backlog | Same tool, sprint-scoped board |
| Sprint completion report | Microsoft PM, archived weekly |
| Roadmap / burn chart | Updated weekly, included in status report |
| Decision register | [`docs/architecture/decision-register.md`](architecture/decision-register.md) |

---

## 11. Testing and Quality Management

### 11.1 Testing Types

| Test type | Owner | When |
|-----------|-------|------|
| Unit (xUnit + FluentAssertions + NSubstitute) | Microsoft team | Continuous, every PR |
| Contract tests against `contracts/openapi.yaml` | Microsoft team | Continuous, every PR |
| Integration tests (.NET Aspire harness, Cosmos emulator, Azurite) | Microsoft team | Continuous |
| Snapshot tests (Verify.Xunit) on AI integration | Microsoft team | Continuous |
| Load tests (NBomber, 500 concurrent) | Microsoft QA | Sprint 8 |
| Chaos / fault-injection (degradation ladder L1–L5) | Microsoft QA | Sprint 8 |
| SAST / SCA | GitHub Actions CI | Continuous |
| Container image scanning (Trivy) | GitHub Actions CI | Continuous |
| SBOM generation (CycloneDX) and signing (Notation) | GitHub Actions CI | Continuous |
| **UAT** | **Walmart** | **Sprint 9** |
| Penetration test | External vendor (Walmart-procured) | Pre-GA (Sprint 9) |
| Privacy / DPIA validation | Walmart Privacy Office | Sprints 4, 8, 9 |

### 11.2 Responsibility Model

- **Microsoft**: feature-level validation, integration, system testing, load and chaos testing, SAST/SCA/SBOM/Trivy gates.
- **Walmart**: UAT execution, penetration test procurement and validation, performance acceptance against Walmart's broader storefront SLOs.

### 11.3 Defect Management

| Priority | Definition | SLA (time to triage) | SLA (time to fix) |
|:--------:|------------|:--------------------:|:-----------------:|
| P1 | Production down or data loss | 1 hour | 4 hours |
| P2 | Major feature broken, no workaround | 4 hours | 1 business day |
| P3 | Feature degraded, workaround available | 1 business day | Next sprint |
| P4 | Cosmetic or low impact | 2 business days | Backlog |

Severity levels S1–S4 map to priority. Remediation is **backlog-driven** within sprint capacity; P1/P2 may interrupt sprint.

### 11.4 Quality Gates

- Coverage gate: **≥ 80% line, ≥ 90% on critical paths** (constitutional requirement; enforced in CI).
- Hypothesis gates: H1, H3, H5, H7, H8 must clear before downstream sprints — see §13 and [`project-plan.md`](project-plan.md) §8.

---

## 12. Change Management

### 12.1 Core Principle

All changes to scope, capacity, timeline, or resource allocation **must be formally requested, impact-analysed, and approved** in writing.

### 12.2 Trigger Conditions

- Capacity exhausted (sprint commitment cannot land)
- Scope expansion (new feature, new tenant, new compliance regime)
- Timeline extension (slip > 1 sprint cumulative)
- Resource changes (team composition change > 0.5 FTE)
- Material technical change (e.g., AI model swap)

### 12.3 Process

| Step | Owner | SLA |
|------|-------|:---:|
| 1. Written change request submitted | Either party | — |
| 2. Impact analysis (scope, cost, schedule, risk) | Microsoft Tech Lead + PM | 3 business days |
| 3. Approval by Product Council | Walmart PO + Microsoft Engagement Lead | 3 business days |
| 4. Backlog and SOW updated; version bump | Microsoft PM | 1 business day |

---

## 13. Risk and Issue Management

A **RAID log** (Risks, Actions, Issues, Decisions) is maintained continuously in [`docs/architecture/risk-register.md`](architecture/risk-register.md) (technical risks) and [`docs/project-plan.md`](project-plan.md) §10 (delivery risks). Reviewed monthly, with weekly escalation for HIGH+ items.

### 13.1 Top Plan Risks (carried into this SOW)

| ID | Risk | Severity | Mitigation |
|----|------|:--------:|------------|
| PR-1 | H1 (GPT-5.2 measurement accuracy) fails | **HIGH** | Pre-Sprint 3 prompt engineering spike + calibration dataset prepared in Sprint 2; contingency: 3DLOOK bridge (+2 weeks, Change Order) |
| PR-2 | Walmart Azure tenant provisioning delayed | **HIGH** | Sprint 1 against Microsoft MSDN subscription; promote in Sprint 2 |
| PR-3 | Single Tech Lead bottleneck on PR reviews | **HIGH** | Reserve 25% Tech Lead time for reviews; SDEs cross-review |
| PR-4 | DPIA / Privacy review finds blockers late | MEDIUM | Sprint 4 mid-project privacy checkpoint; Sprint 8 final review |
| PR-5 | Bicep IaC complexity higher than estimated | MEDIUM | Full DevOps FTE from Sprint 6; pair with Security Engineer |
| PR-6 | Walmart catalog feed delayed beyond Sprint 5 | MEDIUM | Synthetic catalog covers US4 dev; defer real-feed integration to Sprint 8 |

### 13.2 Top Technical Risks (carried into this SOW)

| ID | Risk | Severity | Mitigation |
|----|------|:--------:|------------|
| R-001 | GPT-5.2 Vision measurement accuracy | **CRITICAL** | Mandatory height input for absolute scale; 70% confidence threshold; H1 gate |
| R-003 | GPT-5.2 non-deterministic output | **HIGH** | Structured JSON; temperature 0; model version pinned; snapshot tests |
| R-004 | Shopper photo quality variability | MEDIUM | Real-time photo guidance UX; quality validation pre-AI |

---

## 14. Escalation Path

```
Level 1   Microsoft feature team                   →  resolve within 24 h
Level 2   Microsoft PM  /  Walmart Product Owner   →  resolve within 48 h
Level 3   Walmart Product Council / Program Mgr    →  resolve within 5 business days
Level 4   Executive Steering Committee             →  resolve within 10 business days
```

P1 production incidents skip directly to Level 2 with parallel Level 3 notification.

---

## 15. Work Products and Deliverables

### 15.1 Typical outputs (Microsoft-delivered)

| Deliverable | Type | Location |
|-------------|------|----------|
| Working source code for the API and supporting libraries | Code | `src/VirtualMirror.*` (planned) |
| Unit, contract, integration, snapshot, load, and chaos tests | Code | `tests/VirtualMirror.*` |
| Bicep modules (12) + parameter files for dev / staging / prod | IaC | `infra/` |
| GitHub Actions CI workflow with SAST/SCA/SBOM/Trivy/Notation | Pipeline | `.github/workflows/` |
| OpenAPI 3.0.3 specification | Contract | [`specs/001-clothing-fit-assessment/contracts/openapi.yaml`](../specs/001-clothing-fit-assessment/contracts/openapi.yaml) |
| Architecture diagrams (ASCII + Mermaid) | Doc | [`docs/architecture/diagrams.md`](architecture/diagrams.md), [`docs/architecture/diagrams-mermaid.md`](architecture/diagrams-mermaid.md) |
| Decision register (ADRs) | Doc | [`docs/architecture/decision-register.md`](architecture/decision-register.md) |
| Threat model (STRIDE + DREAD) | Doc | [`docs/architecture/threat-model.md`](architecture/threat-model.md) |
| Risk register | Doc | [`docs/architecture/risk-register.md`](architecture/risk-register.md) |
| Resiliency review | Doc | [`docs/architecture/resiliency-review.md`](architecture/resiliency-review.md) |
| Operational runbooks (latency, AI failover, DLQ depth) | Doc | `docs/runbooks/` (planned) |
| Model card | Doc | `docs/model-card.md` (planned) |
| DPIA input package | Doc | Shared with Walmart Privacy Office |
| Disaster recovery plan | Doc | `docs/dr-plan.md` (planned) |
| Sprint completion reports | Doc | Weekly status |
| Knowledge transfer artifacts | Doc + recorded sessions | Sprint 9 |

### 15.2 Acceptance Model

- **Backlog items** (sprint-scoped): validated through sprint review demo; **do not require formal sign-off** beyond Walmart PO acceptance recorded in the tracking tool.
- **Phase and gate deliverables** (H1, H3, H5, H7, H8, MVP, GA): require **written sign-off** by Walmart PO; security and privacy gates additionally require Walmart Security and Privacy Office sign-off.
- **GA cutover**: requires Executive Steering Committee approval.

Worksheet B (below) details deliverable-level acceptance criteria.

---

## 16. Technical and Environment Requirements

### 16.1 Stack

| Layer | Technology |
|-------|-----------|
| Runtime | .NET 8.0 (LTS), ASP.NET Core Web API |
| Orchestration (local + integration) | .NET Aspire |
| AI / ML | Azure OpenAI GPT-5.2 Vision · Florence-2 on Azure AI Foundry · Azure AI Content Safety |
| Data | Azure Cosmos DB (multi-tenant document) · Azure Blob Storage (transient images, 60 s TTL) |
| Messaging | Azure Service Bus (overflow queue, queue depth > 50 or p95 > 4 s) |
| Identity | Microsoft Entra ID (OAuth 2.0 / OpenID Connect) |
| Edge | Azure Front Door / APIM (WAF, rate limiting, TLS termination) |
| Secrets / config | Azure Key Vault · Azure App Configuration |
| Observability | OpenTelemetry → Azure Monitor / Application Insights |
| Compute | Azure Container Apps (multi-AZ, KEDA HTTP scaler, 2–10 instances) |
| IaC | Bicep |
| CI/CD | GitHub Actions |
| Testing | xUnit, FluentAssertions, NSubstitute, NBomber (load), Verify (snapshot) |

*Source: [`README.md`](../README.md) — Tech Stack; [`Sessions/Product-definition.md`](Sessions/Product-definition.md) — Logical Components.*

### 16.2 Environments

| Environment | Purpose | Owner |
|-------------|---------|-------|
| Local dev | Cosmos emulator + Azurite via docker-compose; mocked AI | Microsoft (developers) |
| `dev` | Auto-deploy on merge to feature branch | Microsoft, Walmart subscription |
| `staging` | Pre-production integration testing, full Azure services scaled down | Microsoft, Walmart subscription |
| `prod` | Production, multi-AZ, auto-scale 2–10 | Walmart, Microsoft granted RBAC |

### 16.3 Azure Region

- **Primary**: East US 2 (Walmart primary Azure region).
- **Single-region for v1**; multi-region is a v2 change order.

### 16.4 Estimated Azure Consumption

| Tier | Phase | Monthly cost (USD) | Cost per assessment |
|------|-------|-------------------:|--------------------:|
| Pilot | Months 1–3 | $180 | $0.018 |
| Growth | Months 4–9 | $1,155 | $0.012 |
| Scale | Months 10+ | $13,536 | $0.014 |

**Year 1 Azure consumption**: ~$48K (12-month ramp). Walmart bears Azure consumption costs directly; Microsoft does not resell Azure under this SOW.

*Source: [`cost-estimate.md`](architecture/cost-estimate.md).*

---

## 17. Customer Responsibilities

The estimates and timeline in this SOW assume Walmart provides the following. **Delays in any item below are an external dependency risk** (see §9 of [`project-plan.md`](project-plan.md)).

### 17.1 Provide

| # | Item | Needed by sprint | Owner |
|:-:|------|:---------------:|-------|
| C-1 | Azure subscription, resource group, RBAC, and Entra ID tenant with app registrations and per-operation scopes | 1 (with MSDN fallback for Sprint 1 if delayed) | Walmart Cloud Platform |
| C-2 | Azure OpenAI capacity / PTU allocation for GPT-5.2 | 3 (PAYG acceptable initially) | Walmart Azure account team |
| C-3 | Florence-2 endpoint quota on Azure AI Foundry | 3 | Walmart Azure account team |
| C-4 | Sample garment catalog data (≥ 50 SKUs with sizes) | 5 | Walmart Catalog Engineering |
| C-5 | Production catalog feed (≥ 1,000 SKUs) | 6 (synthetic acceptable if delayed; integration test in Sprint 8) | Walmart Catalog Engineering |
| C-6 | Calibration photo dataset for H1 (≥ 100 photos with ground-truth measurements; diverse body types) | 2 | Walmart (procured or anonymised internal) |
| C-7 | Notation signing keys and access to container registry | 7 | Walmart DevSecOps |
| C-8 | DPIA review slots (kickoff, Sprint 4, Sprint 8) | 1, 4, 8 | Walmart Privacy Office |
| C-9 | Platform Engineering integration review of OpenAPI contract | 7 (OpenAPI delivered end of Sprint 3) | Walmart Platform Eng |
| C-10 | UAT environment access and UAT executors | 9 | Walmart QA + business stakeholders |
| C-11 | Walmart-side SMEs (Catalog, Platform, Privacy, Identity) for ad-hoc questions, ≥ 4 h / week per SME | All sprints | Walmart |
| C-12 | Stakeholder availability for Steering Committee, Product Council, and demos | All sprints | Walmart |

### 17.2 Manage

- External dependencies (Walmart-side approvals, procurement of penetration test vendor).
- Organisational readiness (PDP frontend changes, merchandising decisions on which SKUs receive VirtualMirror).
- Third-party interactions (Zeekit, 3DLOOK if contingency invoked).
- Consumer consent flows on the storefront (the service captures consent reference passed in the API; the storefront owns the UX).
- Post-go-live production support (Microsoft hypercare ends 30 days after go-live unless a managed-services SOW is signed).

---

## 18. Assumptions

The estimates, timeline, and acceptance criteria in this SOW are **true if-and-only-if** the assumptions below hold. Each unmet assumption is a change-management trigger (§12).

### 18.1 Engagement assumptions

| # | Assumption |
|:-:|------------|
| A-1 | Team composition is **senior-IC heavy** (Tech Lead + 2 Senior SDEs + DevOps + 0.5 ML + QA + 0.25 Security + 0.5 PM). Junior-heavy substitution requires 1.3–1.5× effort multiplier. |
| A-2 | Sprint cadence is uninterrupted for 18 weeks. Holiday or vacation impact > 20% of team simultaneously triggers re-baselining. |
| A-3 | Walmart Product Owner is available **daily** for unblocking and weekly for backlog refinement. |
| A-4 | All Walmart inputs in §17.1 land by the indicated sprint. |
| A-5 | Microsoft has **no production support** obligation beyond go-live + 30-day hypercare. |

### 18.2 Technical assumptions

| # | Assumption |
|:-:|------------|
| A-6 | Azure OpenAI GPT-5.2 Vision **measurement accuracy lands within ±2–4 cm** on the calibration set (H1). Failure invokes 3DLOOK bridge contingency (+2 weeks, Change Order). |
| A-7 | Azure OpenAI GPT-5.2 is generally available in East US 2 by Sprint 3. PTU pricing is finalisable before Scale tier. |
| A-8 | Florence-2 on Azure AI Foundry is available in East US 2 with serverless billing for v1 volumes. |
| A-9 | Shopper-provided height (cm) is **always present and accurate** in the API request — it is the scale reference for derived measurements. |
| A-10 | v1 supports a **single Azure region** (East US 2) with multi-AZ replicas; ~99.9% availability SLO. |
| A-11 | Photos are processed **in-memory and via a 60-second-TTL blob**; no permanent biometric storage by default. |

### 18.3 Process assumptions

| # | Assumption |
|:-:|------------|
| A-12 | Walmart's preferred work-item tracker is Azure DevOps (or equivalent); Microsoft will conform. |
| A-13 | Walmart's DPIA process can complete within 5 business days per review slot. |
| A-14 | Penetration test is procured and executed in parallel with Sprint 8–9; findings remediated within Sprint 9 or deferred via documented risk acceptance. |
| A-15 | Compliance scope is PCI-DSS-adjacent (no CHD), SOC 2-aligned, NIST CSF 2.0 mapped, OWASP ASVS L2, GDPR/CCPA. Any additional regime (HIPAA, FedRAMP, EU AI Act high-risk classification) is a Change Order. |

---

## 19. Program / Project Completion Criteria

The engagement is considered **complete** when any of the following occurs:

| # | Trigger |
|:-:|---------|
| 1 | All Sprint 9 acceptance criteria are met, canary reaches 100% production traffic, SLO dashboard is green for 24 hours, and runbooks are signed off — **(planned completion path)**. |
| 2 | Capacity (~274 PD) is consumed and Walmart Product Owner accepts the delivered backlog state, regardless of completeness. |
| 3 | Backlog is complete and accepted prior to capacity exhaustion. |
| 4 | Timeline (18 weeks + hypercare) expires and parties either extend via Change Order or close the engagement. |
| 5 | Contract is terminated by either party per the Master Services Agreement. |

Hypercare period (30 calendar days post-go-live) is bounded and on-call response is best-effort within business hours unless a separate managed-services SOW is in place.

---

## 20. Appendices and Supporting Material

| Appendix | Reference |
|----------|-----------|
| A — Definitions and acronyms | See Glossary below |
| B — Architecture diagrams (ASCII + Mermaid) | [`docs/architecture/diagrams.md`](architecture/diagrams.md) · [`docs/architecture/diagrams-mermaid.md`](architecture/diagrams-mermaid.md) |
| C — Product backlog sample | [`specs/001-clothing-fit-assessment/tasks.md`](../specs/001-clothing-fit-assessment/tasks.md) |
| D — Solution architecture | [`docs/architecture/solution-architecture.md`](architecture/solution-architecture.md) |
| E — OpenAPI contract | [`specs/001-clothing-fit-assessment/contracts/openapi.yaml`](../specs/001-clothing-fit-assessment/contracts/openapi.yaml) |
| F — Data model | [`specs/001-clothing-fit-assessment/data-model.md`](../specs/001-clothing-fit-assessment/data-model.md) |
| G — Project plan | [`docs/project-plan.md`](project-plan.md) |
| H — Cost estimate | [`docs/architecture/cost-estimate.md`](architecture/cost-estimate.md) |
| I — Risk register | [`docs/architecture/risk-register.md`](architecture/risk-register.md) |
| J — Threat model | [`docs/architecture/threat-model.md`](architecture/threat-model.md) |
| K — Resiliency review | [`docs/architecture/resiliency-review.md`](architecture/resiliency-review.md) |
| L — Compliance mapping (PCI DSS, SOC 2, NIST CSF 2.0, OWASP ASVS L2, GDPR/CCPA) | [`docs/Sessions/Product-definition.md`](Sessions/Product-definition.md) — Compliance & Industry Baseline Alignment |

### Glossary (selected)

| Acronym | Definition |
|---------|-----------|
| ACA | Azure Container Apps |
| ADR | Architectural Decision Record |
| ASVS | Application Security Verification Standard (OWASP) |
| CHD | Cardholder Data (PCI DSS scope marker) |
| CPdM | Consulting Product Delivery Manager |
| DPIA | Data Protection Impact Assessment (GDPR Art. 35) |
| DLQ | Dead-letter Queue |
| FTE | Full-Time Equivalent |
| H1, H3, H5, H7, H8 | Hypothesis gates per `plan.md` Hypothesis Validation Plan |
| ISD | Industry Solutions Delivery (Microsoft) |
| KEDA | Kubernetes Event-Driven Autoscaling |
| MVP | Minimum Viable Product (Sprint 4 cutline) |
| PAYG | Pay-as-you-go (Azure consumption model) |
| PD | Person-day |
| PDP | Product Detail Page |
| PO | Product Owner |
| PTU | Provisioned Throughput Units (Azure OpenAI) |
| RAID | Risks, Actions, Issues, Decisions |
| RU/s | Request Units per second (Cosmos DB) |
| SBOM | Software Bill of Materials |
| SC-NNN | Success Criterion ID from `spec.md` |
| SLO | Service Level Objective |
| SMPL | Skinned Multi-Person Linear (3D body model) |
| TSC | Trust Services Criteria (SOC 2) |
| UAT | User Acceptance Testing |
| US1–US4 | User Stories from `spec.md` |
| WAF | Web Application Firewall |
| WP1–WP8 | Work Packages from `project-plan.md` |

---

## Worksheet A — SOW Header + Outcomes

### Engagement identification

| Field | Value |
|-------|-------|
| Customer / Company | Walmart Inc. — Digital, Apparel & Marketplace |
| Industry | Retail — apparel e-commerce |
| Microsoft team | Microsoft ISD — Retail vertical |
| Date | 2026-05-14 |
| Engagement code | TBD upon countersignature |

### Business Outcomes (customer-owned, measurable — 3)

| ID | Outcome | Measure | Target |
|----|---------|---------|--------|
| BO-1 | Reduce fit-driven apparel returns | Return rate on VirtualMirror-enabled SKUs vs. control | ≥ 20% reduction in 6 months (target 30%) |
| BO-2 | Increase apparel PDP conversion | Add-to-cart + checkout conversion delta on enabled SKUs | +3–5% conversion lift in 6 months |
| BO-3 | Establish reusable multi-tenant fit platform | Tenants onboardable on the same data plane | 1 at GA; architected for 20+ at Scale tier |

### In-Scope Boundaries — what Microsoft will deliver (3 anchors)

| ID | Boundary |
|----|----------|
| IS-1 | A multi-tenant, API-first fit assessment service on Azure delivering `POST /v1/assessments` (photo + height → 5-point fit recommendation), `POST /v1/profiles` (opt-in measurement profile with 24 h hard-delete), and `POST /v1/garments` (single + batch ≤ 100 ingestion), authenticated via Entra ID OAuth 2.0 with per-operation scopes. |
| IS-2 | Production-grade hardening: Bicep IaC (dev/staging/prod), GitHub Actions CI with SAST/SCA/SBOM/Trivy/Notation, OpenTelemetry observability with alert rules and 3 runbooks, NBomber 500-concurrent load validation, chaos validation of the L1–L5 degradation ladder, model card, DPIA input package, DR plan. |
| IS-3 | Knowledge transfer: signed-off architecture docs, OpenAPI contract for Walmart frontend integration, decision register, threat model, runbooks, and 2-week hypercare period post-go-live. |

### Out of Scope — explicit boundaries (3 anchors)

| ID | Exclusion |
|----|-----------|
| OOS-1 | Storefront UI changes, Zeekit integration, native mobile SDK, on-device inference (Concept B / v2). |
| OOS-2 | Multi-region active-active deployment, custom SMPL body model (Tier 3 / v2), Microsoft Fabric intelligence loop (Concept C / v3), order-history-driven sizing. |
| OOS-3 | Ongoing production support, on-call rotation, end-user / store-associate training, organisational change management, and supplier-feed-driven automated catalog ingestion. |

---

## Worksheet B — Deliverables, Acceptance Criteria, and Work Packages

### B.1 Deliverables → Acceptance Criteria → Outcomes Mapping

> **Rule**: If a deliverable has no acceptance criteria, it is not a deliverable. Each deliverable maps to a Business Outcome (BO-x) and traces to a feature ID (US1–US4, FR-NNN, SC-NNN).

| # | Deliverable | Description (customer language) | Acceptance Criteria | Outcome Supported | Trace |
|:-:|-------------|----------------------------------|---------------------|:-----------------:|-------|
| D-1 | Foundational platform | Cloud-ready service skeleton with Entra ID auth, Cosmos/Blob/Service Bus repositories, Polly resilience pipelines with AI failover, health probes, observability | All foundational integration tests green; **H7: AI failover < 5 s** in integration test under simulated primary outage; readiness probe responds < 1 s | BO-3 | WP1, WP2 |
| D-2 | Photo-based fit assessment (MVP) | `POST /v1/assessments` accepts photo + height, returns 5-point fit per body area with confidence and disclaimer when < 70% confidence, p95 < 5 s end-to-end | All US1 acceptance scenarios in `spec.md` pass; **H1: ≤ 15% of calibration photos > ±4 cm** vs. ground truth on diverse calibration set; demoable to Walmart PO | BO-1, BO-2 | WP3, US1, FR-001..005, SC-001 |
| D-3 | Measurement profile storage | `POST/GET/DELETE /v1/profiles/{shopperRef}` with explicit consent and 24-hour hard-delete SLA | All US2 acceptance scenarios pass; deletion cascades across containers and is verifiable; consent reference recorded in audit log | BO-1, BO-2 | WP4, US2, FR-006, FR-014 |
| D-4 | Frontend integration contract | OpenAPI 3.0.3 contract published, Swashbuckle UI live, URI versioning (`/v1/...`), CORS configured, contract tests against `contracts/openapi.yaml` | OpenAPI contract validated; Walmart Platform Eng integration review signs off; contract tests green in CI | BO-2, BO-3 | WP5, US3, FR-007, FR-008 |
| D-5 | Garment data ingestion | `POST /v1/garments` (single) and `POST /v1/garments:batch` (≤ 100) with per-SKU validation, partial-failure semantics, version history | All US4 acceptance scenarios pass; batch endpoint accepts 100 items, rejects invalid with field-level errors, maintains version history on update | BO-3 | WP6, US4, FR-009 |
| D-6 | Resilience / degradation ladder | L1–L5 graceful degradation: full pipeline → cached profile → size-chart fallback; Polly + circuit breaker + DLQ; Service Bus overflow queue when queue depth > 50 or p95 > 4 s | Chaos tests show **≥ 90% request success during partial AI outage (H8)**; 202 Accepted returned with queue position when overflow triggers | BO-1 | WP2.4, WP3.5, FR-012 |
| D-7 | Bicep IaC (dev / staging / prod) | 12 Bicep modules + 3 environment parameter files for ACA, Cosmos, Blob, Key Vault, App Config, Front Door, observability, networking | `az deployment group what-if` clean against all 3 environments; modules pass linting (PSRule for Azure); private endpoints verified | BO-3 | WP7.1 |
| D-8 | CI/CD pipeline | GitHub Actions: build → test (unit + contract + integration) → SAST + SCA → SBOM (CycloneDX) → container build + Trivy scan + Notation sign → deploy with canary | Pipeline green on `main`; coverage gate ≥ 80% line / ≥ 90% critical; SBOM artefact attached; signed image promoted to staging on green | BO-3 | WP7.2 |
| D-9 | Observability & runbooks | OTel → Azure Monitor; SLO dashboards (latency, error rate, confidence distribution, AI failover, DLQ depth); 3 runbooks (latency degradation, AI failover, DLQ depth) | Dashboards live; alert rules fire in test; runbooks reviewed by Walmart Platform Eng; correlation IDs propagate end-to-end | BO-3 | WP7.3, FR-010, FR-011 |
| D-10 | Load and chaos validation | NBomber 500-concurrent smoke + 30-minute soak; chaos / fault-injection on AI providers, Cosmos, Service Bus, Blob | **H3/H5: p95 < 5 s at 500 concurrent**; KEDA scales to 10 instances; no OOM; **H8: ≥ 90% success during chaos run** | BO-1, BO-3 | WP7.4, SC-004 |
| D-11 | Model card & responsible AI | Model card documenting prompt, model version, training context, bias considerations, known limitations, confidence thresholds | Model card reviewed and signed by ML Eng + Tech Lead; published in repo; minor-detection refusal logic verified | BO-1 | WP7.5, FR-015 |
| D-12 | DR plan & data classification | DR plan documenting RTO < 1 h, RPO < 15 min for tenant config; data classification labels (transient, ephemeral, opt-in, audit) | DR plan reviewed and signed by Security Eng; data classification matches `Sessions/Product-definition.md`; tabletop walkthrough recorded | BO-3 | WP7.5 |
| D-13 | DPIA input package | Inputs to Walmart's DPIA: data flow, lawful basis, retention, deletion, transfers, sub-processors, breach notification | Walmart Privacy Office accepts DPIA package as complete; no Open / High findings remain at GA | BO-1, BO-2, BO-3 | WP8.4 |
| D-14 | Knowledge transfer & hypercare | 2 recorded enablement sessions for Walmart Platform Eng, runbooks signed, hypercare on-call schedule for 2 weeks post-go-live | Sessions delivered and signed; runbooks acknowledged; on-call rota agreed; no P1 unresolved at end of hypercare | BO-3 | WP7.5, WP8 |

### B.2 Work Package Estimate Table

Estimate by work package first, then allocate hours to roles. Hours assume **senior IC productivity** at **6.5 PD per FTE-sprint** net of ceremony.

| WP | Phase | Key activities | Roles | Effort (PD) | Hours (8 h/PD) | Notes / dependencies |
|:--:|-------|----------------|-------|------------:|---------------:|----------------------|
| WP1 | Sprint 1 | Solution + 5 projects + 6 test projects + dependencies + docker-compose | Tech Lead, SDE#1 | 5 | 40 | Blocking pre-req for WP2 |
| WP2 | Sprints 1–2 | Domain + interfaces + repos + Polly + auth middleware + health + Aspire | Tech Lead, SDE#1, SDE#2, light DevOps | 60 | 480 | **H7 gate end of Sprint 2** |
| WP3 | Sprints 3–4 | AI clients (Florence/Content Safety/GPT-5.2) + image validation + H1 spike + fit engine + orchestration + API + tests | Tech Lead, SDE#1, SDE#2, ML Eng 0.5 | 60 | 480 | **H1 gate end of Sprint 3; MVP demo end of Sprint 4** |
| WP4 | Sprint 5 | Profile repo + service + controller + 24 h delete + by-profile + DTOs + DI + tests | SDE#1 | 17 | 136 | Depends on WP2 + WP3 |
| WP5 | Sprints 4–5 | Swashbuckle + XML docs + versioning + CORS + contract tests + auth/rate tests + degradation tests | SDE#2 | 10 | 80 | Parallel with WP3 tail |
| WP6 | Sprint 6 | GarmentService + controller + DTOs + batch + version tracking + tests | SDE#1 | 13 | 104 | Depends on WP2 |
| WP7 | Sprints 6–8 | 12 Bicep modules + 3 param files + CI workflow + alerts + 3 runbooks + NBomber 500-concurrent + chaos + docs + model card + DR plan | DevOps, Tech Lead, QA, SDE float, ML Eng light, Security PT | 41 | 328 | **H3/H5/H8 gates end of Sprint 8** |
| WP8 | All sprints | Ceremony (15%) + defect/UAT buffer (15%) + Walmart alignment + security/privacy review + PM/backlog | All — primarily PM, Tech Lead, Security PT | 68 | 544 | Always-on; absorbs slip if H1 contingency triggers |
| | | | **Total** | **~274 PD** | **~2,192 h** | |

#### Hours by role (allocation across WP1–WP8)

| Role | PD | Hours | % of total |
|------|---:|------:|-----------:|
| Tech Lead / Solution Architect | 65 | 520 | 24% |
| Senior .NET Engineer #1 | 70 | 560 | 25% |
| Senior .NET Engineer #2 | 65 | 520 | 24% |
| Cloud / DevOps Engineer | 45 | 360 | 16% |
| ML / AI Engineer | 18 | 144 | 7% |
| QA / SDET | 25 | 200 | 9% |
| Security / Privacy Engineer (PT) | 8 | 64 | 3% |
| Product Manager / CPdM | (PM allocation absorbed in WP8) | — | — |
| **Total build allocation** | **~296 PD** | **~2,368 h** | (slack ~22 PD covers vacation + ceremony float; actual chargeable build ~274 PD) |

#### Summary

| Field | Value |
|-------|-------|
| **Total estimated effort** | **~274 person-days (~2,192 hours)** |
| **Delivery duration** | **18 weeks** (9 × 2-week sprints) + 2 weeks hypercare |
| **Average team size** | 5.75 FTE (peak 6.75 FTE during Sprints 7–8) |
| **Estimation drivers** | Three-tier AI pipeline complexity · 12 Bicep modules · 500-concurrent load target · multi-tenant + privacy + DPIA · OWASP ASVS L2 + PCI-adjacent posture · IaC-driven canary deployment with < 15 min rollback |
| **Top 3 assumptions** | (1) **H1: GPT-5.2 measurement accuracy within ±2–4 cm** on calibration set; (2) **Senior IC team** as composed in §8 with no > 20% simultaneous OOO; (3) **Walmart inputs in §17.1** land by indicated sprint, especially calibration dataset (Sprint 2), Azure tenant + PTU (Sprints 1, 3), Notation keys + container registry (Sprint 7), and DPIA review slots (Sprints 4, 8, 9). |

### B.3 Scope Traps — what can expand hours quickly

> Items below are **not** included in the estimate. Each is a Change Order trigger.

| # | Scope trap | Likely cost |
|:-:|------------|-------------|
| ST-1 | H1 contingency (3DLOOK bridge) if GPT-5.2 accuracy fails | +20–30 PD, +2 weeks |
| ST-2 | Multi-region active-active (v2) | +60–90 PD |
| ST-3 | Native mobile SDK / on-device inference (Concept B) | +120 PD+ |
| ST-4 | Additional tenant onboarding during v1 (each new tenant beyond Walmart) | +5–10 PD per tenant |
| ST-5 | Catalog data quality remediation if supplier feeds are non-normalised | +10–25 PD |
| ST-6 | Storefront PDP widget / SDK reference implementation | +15–25 PD |
| ST-7 | HIPAA, FedRAMP, or EU AI Act high-risk compliance | +40 PD+ |
| ST-8 | Performance acceptance against Walmart's broader storefront SLOs beyond NBomber smoke | +10–15 PD |
| ST-9 | Production support / on-call beyond 2-week hypercare | Separate managed-services SOW |
| ST-10 | Direct Zeekit integration | +20–40 PD (partnership-dependent) |

---

## Version History

| Version | Date | Author | Status | Summary of changes |
|--------:|------|--------|--------|-------------------|
| 0.1.0 | 2026-05-14 | Microsoft ISD draft | Draft for internal review | Initial draft grounded in discovery artifacts: spec.md (US1–US4, FR-001..015, SC-001..007), Product-definition.md, project-plan.md (WBS WP1–WP8, ~274 PD over 18 weeks), cost-estimate.md (3-tier consumption model), risk-register.md (R-001..004), threat-model.md, solution-architecture.md, and EX3 SOW template structure (19 required sections + Worksheets A & B). |

### Versioning policy

Semantic Versioning applies to this document:

- **Major (1.0.0)**: contract-affecting changes — scope, pricing model, team size, timeline > 1 sprint, or removal of deliverables.
- **Minor (0.x.0)**: addition of deliverables, work packages, assumptions, or material clarifications that do not change the contract envelope.
- **Patch (0.0.x)**: editorial corrections, typo fixes, and reference updates with no semantic change.

**Promotion path**: `0.x.y` Draft → `1.0.0` Final-for-signature on Executive Steering Committee approval. Post-signature changes are managed via §12 Change Management and reflected as new minor or major versions with the change request ID logged in this table.

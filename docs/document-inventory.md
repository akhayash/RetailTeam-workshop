# Document Inventory

**Project**: VirtualMirror AI — Clothing Fit Assessment Service
**Last updated**: 2026-05-14

Complete index of all project documentation with descriptions and content sources.

---

## Workshop Deliverables

| Document | Path | Description |
|----------|------|-------------|
| Architecture Concepts | [Deliverable1.md](../Deliverable1.md) | Three architecture concept diagrams showing how agentic AI transforms retail workflows |
| Persona-Driven Scenarios | [Deliverable2.md](../Deliverable2.md) | Human-AI collaboration scenarios for each architecture concept |
| C-Suite Relevance | [Deliverable3.md](../Deliverable3.md) | Executive-level value articulation for CTO, CFO, and COO perspectives |

---

## Feature Specification (`specs/001-clothing-fit-assessment/`)

| Document | Path | Description |
|----------|------|-------------|
| Feature Specification | [spec.md](../specs/001-clothing-fit-assessment/spec.md) | Full requirements with user stories, acceptance criteria, edge cases, and priority assignments |
| Implementation Plan | [plan.md](../specs/001-clothing-fit-assessment/plan.md) | Technical design, project structure, constitution checks, and phased implementation approach |
| Research | [research.md](../specs/001-clothing-fit-assessment/research.md) | Phase 0 technology research with confidence-labeled findings for Azure AI services |
| Data Model | [data-model.md](../specs/001-clothing-fit-assessment/data-model.md) | Entity schemas, relationships, and Cosmos DB partition strategy |
| Tasks | [tasks.md](../specs/001-clothing-fit-assessment/tasks.md) | Dependency-ordered implementation tasks grouped by user story |
| Quickstart | [quickstart.md](../specs/001-clothing-fit-assessment/quickstart.md) | Developer setup guide with prerequisites, commands, and environment configuration |
| Requirements Checklist | [checklists/requirements.md](../specs/001-clothing-fit-assessment/checklists/requirements.md) | Specification quality validation checklist |
| OpenAPI Contract | [contracts/openapi.yaml](../specs/001-clothing-fit-assessment/contracts/openapi.yaml) | OpenAPI 3.0.3 specification defining all REST endpoints, schemas, and auth requirements |

---

## Architecture (`docs/architecture/`)

| Document | Path | Description |
|----------|------|-------------|
| Solution Architecture | [solution-architecture.md](architecture/solution-architecture.md) | Complete architecture document including personas, deployment model, AI pipeline, and multi-tenancy design |
| Architecture Diagrams | [diagrams.md](architecture/diagrams.md) | Canonical ASCII architecture diagrams (system context, component, deployment) |
| Mermaid Diagrams | [diagrams-mermaid.md](architecture/diagrams-mermaid.md) | Mermaid renditions of architecture diagrams for rendering in GitHub/tooling |
| Decision Register | [decision-register.md](architecture/decision-register.md) | Architectural Decision Records (ADRs) tracking all significant design choices |
| Risk Register | [risk-register.md](architecture/risk-register.md) | Identified risks with likelihood, impact, mitigations, and review cadence |
| Threat Model | [threat-model.md](architecture/threat-model.md) | STRIDE + DREAD threat analysis covering data flows and trust boundaries |
| Resiliency Review | [resiliency-review.md](architecture/resiliency-review.md) | Availability and resilience assessment with prioritized improvement recommendations |
| Cost Estimate | [cost-estimate.md](architecture/cost-estimate.md) | Azure resource cost projections across dev, staging, and production environments |
| Assessment Report | [assessmentreport.md](architecture/assessmentreport.md) | Architecture gap analysis against workshop quality bar and deliverable requirements |

---

## Project Management (`docs/`)

| Document | Path | Description |
|----------|------|-------------|
| Project Plan | [project-plan.md](project-plan.md) | WBS, effort estimates, team capacity, sprint timeline, delivery model, and quality gates for v1 delivery |

---

## Research (`docs/research/`)

| Document | Path | Description |
|----------|------|-------------|
| AI Feasibility Study | [ai-fit-assessment-feasibility.md](research/ai-fit-assessment-feasibility.md) | Technical feasibility evaluation of AI/ML for clothing fit assessment from photos, including industry benchmarks and risk analysis |

---

## Sessions & Discovery (`docs/Sessions/`)

| Document | Path | Description |
|----------|------|-------------|
| Problem Statement | [Problem-statement.md](Sessions/Problem-statement.md) | Original problem statement and initial product concept definition |
| Product Definition | [Product-definition.md](Sessions/Product-definition.md) | Expanded product definition with market sizing, addressable savings, and scope |
| Event Journal | [journal.md](Sessions/journal.md) | Append-only event log recording decisions, actions, and reasoning chains throughout development |

---

## Reference Inputs (`docs/Inputs/`)

| Document | Path | Description |
|----------|------|-------------|
| Technical Architecture Research | [EX2_Technical_Architecture_Research.pptx](Inputs/EX2_Technical_Architecture_Research.pptx) | Workshop framework PowerPoint used as input for architecture assessment and deliverable alignment |

---

## Project Configuration (root)

| Document | Path | Description |
|----------|------|-------------|
| README | [README.md](../README.md) | Project overview, tech stack, getting started guide, and success metrics |
| Project Manifest | [project-manifest.json](../project-manifest.json) | Machine-readable project metadata: technologies, environments, commands, and quality gates |
| License | [LICENSE](../LICENSE) | MIT License |
| Copilot Instructions | [.github/copilot-instructions.md](../.github/copilot-instructions.md) | AI coding assistant guidelines and project conventions |

---

## Internal Tracking (`.copilot-tracking/`)

These artifacts are generated by AI-assisted planning workflows and are not primary documentation.

| Area | Path | Description |
|------|------|-------------|
| Security Plans | `.copilot-tracking/security-plans/fitassess/` | Security planning artifacts including threat assessments and control mappings |
| RAI Plans | `.copilot-tracking/rai-plans/clothing-fit-assessment/` | Responsible AI assessment plans and impact evaluations |
| RAI References | `.copilot-tracking/rai-plans/references/` | Supporting reference materials for RAI assessments |
| Research Traces | `.copilot-tracking/research/` | Research session artifacts and findings |

---

## Traceability (`docs/traces/`)

| Area | Path | Description |
|------|------|-------------|
| Session Traces | `docs/traces/session-c0d37c88-*/` | JSONL trace logs capturing AI-assisted session interactions for audit and replay |

---

## Content Source Summary

| Source Type | Count | Purpose |
|-------------|-------|---------|
| Workshop deliverables | 3 | Executive-facing architecture communication |
| Feature specifications | 8 | Requirements, design, and implementation guidance |
| Architecture documents | 9 | Technical architecture, decisions, risks, and security |
| Project management | 1 | WBS, effort, capacity, timeline, delivery model |
| Research | 2 | Technology feasibility and validation |
| Session artifacts | 3 | Discovery, problem framing, and decision history |
| Reference inputs | 1 | External workshop framework material |
| Project configuration | 4 | Repository setup and developer guidance |
| Internal tracking | 4 | AI-assisted planning and compliance artifacts |
| Traceability | 1 | Audit trail for AI-assisted development |
| **Total** | **35** | |

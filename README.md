# RetailTeam Workshop — AI Clothing Fit Assessment

An AI-powered clothing fit assessment service that reduces online return rates by giving shoppers personalized fit recommendations based on their photos. Built on the Microsoft tech stack (.NET 8, Azure AI Services, Cosmos DB).

## Problem

Online clothing returns (25–40%) are driven by fit uncertainty. Shoppers cannot judge how a garment will fit before purchasing, leading to high logistics costs and poor customer experience.

## Solution

A standalone API service that accepts a shopper photo with height input, extracts body measurements using Azure AI Vision + GPT-4o, compares them against garment sizing data, and returns a per-area fit recommendation with confidence scores — all within 5 seconds.

## Repository Structure

```text
├── docs/
│   ├── architecture/          # Solution architecture, diagrams, ADRs, risk register
│   ├── research/              # Feasibility research and analysis
│   └── Sessions/              # Problem statement, product definition, journal
├── specs/
│   └── 001-clothing-fit-assessment/
│       ├── spec.md            # Feature specification with user stories
│       ├── plan.md            # Implementation plan
│       ├── tasks.md           # Task breakdown
│       ├── quickstart.md      # Developer setup guide
│       ├── data-model.md      # Entity schemas
│       ├── research.md        # Technical research
│       ├── contracts/
│       │   └── openapi.yaml   # API contract (OpenAPI 3.x)
│       └── checklists/
│           └── requirements.md
└── README.md
```

## Quick Navigation

| Looking for... | Go to |
|----------------|-------|
| How to run locally | [specs/001-clothing-fit-assessment/quickstart.md](specs/001-clothing-fit-assessment/quickstart.md) |
| API contract | [specs/001-clothing-fit-assessment/contracts/openapi.yaml](specs/001-clothing-fit-assessment/contracts/openapi.yaml) |
| Feature spec & user stories | [specs/001-clothing-fit-assessment/spec.md](specs/001-clothing-fit-assessment/spec.md) |
| Solution architecture | [docs/architecture/solution-architecture.md](docs/architecture/solution-architecture.md) |
| Architecture diagrams | [docs/architecture/diagrams.md](docs/architecture/diagrams.md) |
| Data model | [specs/001-clothing-fit-assessment/data-model.md](specs/001-clothing-fit-assessment/data-model.md) |
| Risk register | [docs/architecture/risk-register.md](docs/architecture/risk-register.md) |
| Problem statement | [docs/Sessions/Problem-statement.md](docs/Sessions/Problem-statement.md) |
| Product definition | [docs/Sessions/Product-definition.md](docs/Sessions/Product-definition.md) |
| AI feasibility research | [docs/research/ai-fit-assessment-feasibility.md](docs/research/ai-fit-assessment-feasibility.md) |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| API | ASP.NET Core Web API (.NET 8) |
| Orchestration | .NET Aspire |
| Body measurement | Azure AI Vision + Azure OpenAI GPT-4o |
| Content safety | Azure AI Content Safety |
| Data store | Azure Cosmos DB (multi-tenant) |
| Image storage | Azure Blob Storage (60s TTL auto-purge) |
| Identity | Microsoft Entra ID (OAuth 2.0) |
| Hosting | Azure Container Apps |
| Observability | OpenTelemetry + Application Insights |

## Getting Started

```powershell
git checkout 001-clothing-fit-assessment
dotnet restore src/FitAssess.sln
docker compose up -d
dotnet run --project src/FitAssess.AppHost
```

See the full [Quickstart Guide](specs/001-clothing-fit-assessment/quickstart.md) for prerequisites and detailed instructions.

## Key Design Decisions

- **Privacy by design** — photos purged within 60 seconds; no raw images stored; opaque shopper IDs only.
- **Three-tier AI pipeline** — Azure AI Vision (fast, cheap) → GPT-4o (reasoning) → AI Foundry (future custom models).
- **Multi-tenant isolation** — Cosmos DB partition key per tenant; tenant-scoped rate limiting.
- **API-first** — OpenAPI contract drives frontend integration; stateless request model.

## License

See [LICENSE](LICENSE) for details.
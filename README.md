# VirtualMirror AI — Clothing Fit Assessment Service

> Reducing online clothing returns through AI-powered fit recommendations.

## Problem

Online clothing returns cost retailers $10–30 per return, with "wrong fit" cited in 52% of cases. Return rates for online clothing sit between 25–40% industry-wide — costing billions annually and eroding customer confidence.

## Solution

VirtualMirror AI is a multi-tenant, standalone service that accepts a shopper's full-body photo and height, extracts body measurements using Azure OpenAI GPT-5.2 Vision, compares them against garment size data, and returns a **5-point fit recommendation** (Too Tight → Too Loose) per body area — all within 5 seconds.

### Key Capabilities

- 📷 **Photo-based body measurement extraction** — single photo + height → derived measurements
- 👕 **Per-area fit scoring** — shoulders, chest, waist, hips, length on a 5-point scale
- 🔒 **Privacy by design** — photos purged within 60 seconds; only anonymized measurements stored
- 🏢 **Multi-tenant** — isolated garment catalogs and shopper profiles per retail partner
- 🔌 **API-first** — RESTful API with OpenAPI 3.x documentation for seamless frontend integration
- ⚡ **Scalable** — 500 concurrent assessments, auto-scaling 2–10 instances on Azure Container Apps

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Runtime** | .NET 8.0 (LTS), ASP.NET Core Web API |
| **AI/ML** | Azure OpenAI GPT-5.2 Vision (measurement extraction), Florence-2 on Azure AI Foundry (image validation), Azure AI Content Safety |
| **Data** | Azure Cosmos DB (multi-tenant document store), Azure Blob Storage (transient images) |
| **Auth** | Microsoft Entra ID (OAuth 2.0 / OpenID Connect) |
| **Orchestration** | .NET Aspire |
| **Infrastructure** | Azure Container Apps, Bicep (IaC), Azure Service Bus (async queue) |
| **Testing** | xUnit, FluentAssertions, NSubstitute, NBomber (load), Verify (snapshot) |

## Project Structure

```
specs/001-clothing-fit-assessment/    # Feature spec, plan, API contracts, data model
docs/
├── architecture/                     # Solution architecture, decision register, diagrams
├── research/                         # AI feasibility study
└── Inputs/                           # Reference materials

src/                                  # (planned)
├── VirtualMirror.Api/                    # ASP.NET Core Web API host
├── VirtualMirror.Core/                   # Domain models & interfaces
├── VirtualMirror.Services/               # Business logic (assessment, image processing)
├── VirtualMirror.Infrastructure/         # Azure integrations (Cosmos, Blob, AI, Identity)
└── VirtualMirror.AppHost/                # .NET Aspire orchestrator

tests/                                # (planned)
├── VirtualMirror.Api.Tests/              # Integration tests
├── VirtualMirror.Services.Tests/         # Unit tests
├── VirtualMirror.Contract.Tests/         # API contract validation
└── VirtualMirror.Load.Tests/             # Performance tests (NBomber)

infra/                                # (planned)
├── main.bicep                        # Root deployment
├── modules/                          # Bicep modules
└── parameters/                       # Per-environment configs
```

## Getting Started

### Prerequisites

- .NET 8.0 SDK
- Azure CLI (`az`) authenticated
- Docker Desktop (for local Cosmos DB emulator + Azurite)
- Visual Studio 2022 or VS Code with C# Dev Kit

### Local Development

```powershell
# Restore dependencies
dotnet restore src/VirtualMirror.sln

# Start infrastructure (Cosmos DB emulator + Azurite)
docker compose up -d

# Run the Aspire AppHost
dotnet run --project src/VirtualMirror.AppHost
```

API available at `https://localhost:7001/api/v1` · Aspire dashboard at `https://localhost:15888`

### Quick Verification

```powershell
# Health check
curl https://localhost:7001/api/v1/health

# Run all tests
dotnet test src/VirtualMirror.sln
```

## Architecture Overview

The service follows **Clean Architecture** with four projects separating concerns:

```
API (Controllers, Middleware) → Services (Business Logic) → Core (Domain Models)
                                       ↓
                              Infrastructure (Azure AI, Cosmos, Blob)
```

Key design decisions:
- **Stateless service** — horizontally scalable, no session affinity required
- **Tenant isolation** — Cosmos DB partition keys enforce data boundaries
- **Graceful degradation** — falls back to size chart guidance when AI is unavailable
- **Confidence scoring** — assessments below 70% confidence trigger disclaimers and alternative guidance

## Documentation

| Document | Description |
|----------|-------------|
| [Feature Spec](specs/001-clothing-fit-assessment/spec.md) | Full requirements, user stories, acceptance criteria |
| [Implementation Plan](specs/001-clothing-fit-assessment/plan.md) | Technical design, project structure, constitution checks |
| [Solution Architecture](docs/architecture/solution-architecture.md) | Architecture diagrams, personas, deployment model |
| [Data Model](specs/001-clothing-fit-assessment/data-model.md) | Entity schemas and relationships |
| [API Contracts](specs/001-clothing-fit-assessment/contracts/) | OpenAPI 3.x specification |
| [Research](docs/research/ai-fit-assessment-feasibility.md) | AI feasibility study, industry benchmarks |
| [Quickstart](specs/001-clothing-fit-assessment/quickstart.md) | Detailed setup and commands |

## Success Metrics

| Metric | Target |
|--------|--------|
| End-to-end latency (p95) | < 5 seconds |
| Fit prediction accuracy | ≥ 85% (validated against return data) |
| Return rate reduction | ≥ 20% within 6 months |
| Concurrent capacity | 500 assessments |
| Availability | 99.9% monthly |
| Data deletion SLA | < 24 hours |

## License

See [LICENSE](LICENSE) for details.
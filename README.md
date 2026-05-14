# VirtualMirror AI — Clothing Fit Assessment Service

> Reducing online clothing returns through AI-powered fit recommendations.

| | Status |
|--|--------|
| **Branch** | `001-clothing-fit-assessment` |
| **Phase** | Design & Planning |
| **Runtime** | .NET 8.0 (LTS) |
| **Platform** | Azure Container Apps |
| **License** | MIT |

---

## Problem

Walmart is the **3rd-largest U.S. apparel e-commerce retailer** with $14.7B in online clothing revenue (2024). Like the broader industry, online apparel returns run at **24–26%**, with **53% driven by fit and sizing issues** — translating to an estimated **$200–400M in annual avoidable cost** from fit-related returns alone (processing, reverse logistics, restocking, markdowns, and write-offs).

The root cause: shoppers cannot judge how a garment will fit before purchasing. They resort to **"bracketing"** (buying multiple sizes, returning extras), eroding margins and generating unnecessary transport emissions. Traditional size charts fail because a "Medium" from one brand has different measurements than a "Medium" from another — and shoppers have no way to map their own body to those inconsistent charts.

Walmart already invested in **Zeekit** for virtual try-on visualization ("how does it look on me?"), but shoppers still lack **measurement-based fit confidence** ("will it actually fit my body?"). This gap between visual appeal and physical fit remains the primary driver of returns.

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
# Clone and checkout feature branch
git clone <repo-url>
cd RetailTeam-workshop
git checkout 001-clothing-fit-assessment

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

### Environment Variables

| Variable | Description | Local Default |
|----------|-------------|---------------|
| `AZURE_COSMOS_ENDPOINT` | Cosmos DB endpoint | `https://localhost:8081` |
| `AZURE_STORAGE_ENDPOINT` | Blob storage endpoint | `http://127.0.0.1:10000/devstoreaccount1` |
| `AZURE_AI_ENDPOINT` | Azure AI Vision endpoint | Mock in local dev |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI GPT-5.2 Vision endpoint | Mock in local dev |
| `AZURE_CONTENT_SAFETY_ENDPOINT` | Content Safety API endpoint | Mock in local dev |

## Architecture Overview

The service follows **Clean Architecture** with four projects separating concerns:

```
API (Controllers, Middleware) → Services (Business Logic) → Core (Domain Models)
                                       ↓
                              Infrastructure (Azure AI, Cosmos, Blob)
```

### AI Pipeline

The assessment flow uses a three-tier Microsoft AI pipeline:

1. **Florence-2** (Azure AI Foundry) — Image validation, people detection, bounding box quality checks
2. **Azure AI Content Safety** — Content moderation, minor detection
3. **Azure OpenAI GPT-5.2 Vision** — Body measurement extraction from validated photo + height

### Key Design Decisions

- **Stateless service** — horizontally scalable, no session affinity required
- **Tenant isolation** — Cosmos DB partition keys enforce data boundaries
- **Graceful degradation** — falls back to size chart guidance when AI is unavailable
- **Confidence scoring** — assessments below 70% confidence trigger disclaimers and alternative guidance
- **Privacy by design** — photos purged within 60 seconds; only anonymized measurements stored
- **Queue-based overflow** — Azure Service Bus absorbs traffic spikes beyond capacity thresholds

## API Overview

The service exposes a RESTful API documented with OpenAPI 3.0.3. Key endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/assessments` | Create a fit assessment from a shopper photo |
| `GET` | `/api/v1/assessments/{id}` | Retrieve assessment results |
| `POST` | `/api/v1/profiles` | Create/update a shopper measurement profile |
| `GET` | `/api/v1/profiles/{shopperRef}` | Retrieve stored measurements |
| `POST` | `/api/v1/garments` | Ingest garment measurement data |
| `GET` | `/api/v1/health` | Service health check (no auth) |

Full specification: [`specs/001-clothing-fit-assessment/contracts/openapi.yaml`](specs/001-clothing-fit-assessment/contracts/openapi.yaml)

## Deployment

### Environments

| Environment | Purpose | Infrastructure |
|-------------|---------|---------------|
| `dev` | Local + cloud development | Cosmos DB emulator, Azurite, mocked AI |
| `staging` | Integration testing, pre-production | Full Azure services, scaled down |
| `prod` | Production | Multi-AZ, auto-scaling 2–10 instances |

### Infrastructure as Code

```powershell
# Deploy to Azure (requires subscription + resource group)
az deployment group create -g virtualmirror-dev -f infra/main.bicep -p infra/parameters/dev.json
```

Bicep modules are organized under `infra/modules/` for Azure Container Apps, Cosmos DB, Storage, AI services, and networking.

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

## Security & Privacy

- **Authentication**: Microsoft Entra ID (OAuth 2.0 / OpenID Connect) with per-tenant scopes
- **Data minimization**: Photos purged within 60 seconds of processing; no raw images stored
- **Encryption**: TLS 1.2+ in transit; Azure-managed encryption at rest
- **Secrets**: Azure Key Vault for all service credentials
- **Content safety**: Azure AI Content Safety screens all uploaded images
- **Minor protection**: System refuses to process images detected as under 16 years old
- **Audit logging**: All data access and deletion requests logged for compliance

## Contributing

1. Create a feature branch from `main` using the pattern `NNN-feature-name`
2. Follow the established project structure and coding conventions
3. Ensure all tests pass: `dotnet test src/VirtualMirror.sln`
4. Submit a pull request with a clear description of changes

### Code Style

- C# conventions per `.editorconfig`
- XML documentation on public APIs
- Unit tests for all business logic (xUnit + FluentAssertions)
- Integration tests for API endpoints

## License

See [LICENSE](LICENSE) for details.
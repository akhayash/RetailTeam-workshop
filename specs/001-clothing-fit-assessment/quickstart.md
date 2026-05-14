# Quickstart: VirtualMirror AI

## Prerequisites

- .NET 8.0 SDK
- Azure CLI (`az`) authenticated
- Docker Desktop (for local Cosmos DB emulator)
- Visual Studio 2022 or VS Code with C# Dev Kit

## Local Development Setup

```powershell
# Clone and navigate
git clone <repo-url>
cd RetailTeam-workshop
git checkout 001-clothing-fit-assessment

# Restore dependencies
dotnet restore src/VirtualMirror.sln

# Start infrastructure (Cosmos DB emulator + Azurite for Blob Storage)
docker compose up -d

# Run the Aspire AppHost (orchestrates all services locally)
dotnet run --project src/VirtualMirror.AppHost
```

The API will be available at `https://localhost:7001/api/v1`.
Aspire dashboard at `https://localhost:15888`.

## Quick Test

```powershell
# Health check (no auth required)
curl https://localhost:7001/api/v1/health

# Create a fit assessment (requires auth token)
$token = az account get-access-token --resource api://virtualmirror-dev --query accessToken -o tsv

curl -X POST https://localhost:7001/api/v1/assessments `
  -H "Authorization: Bearer $token" `
  -F "shopperRef=abc123hash" `
  -F "garmentId=SKU-001" `
  -F "sizeLabel=M" `
  -F "image=@./tests/fixtures/sample-photo.jpg"
```

## Project Structure

| Project | Purpose |
|---------|---------|
| `VirtualMirror.Api` | ASP.NET Core Web API host |
| `VirtualMirror.Core` | Domain models, interfaces, enums |
| `VirtualMirror.Services` | Business logic (assessment, image processing) |
| `VirtualMirror.Infrastructure` | Azure integrations (Cosmos, Blob, AI, Identity) |
| `VirtualMirror.AppHost` | .NET Aspire orchestrator |

## Key Commands

```powershell
# Run all tests
dotnet test src/VirtualMirror.sln

# Run specific test project
dotnet test tests/VirtualMirror.Api.Tests

# Build for release
dotnet publish src/VirtualMirror.Api -c Release -o ./publish

# Deploy infrastructure (requires Azure subscription)
az deployment group create -g virtualmirror-dev -f infra/main.bicep -p infra/parameters/dev.json
```

## Environment Variables

| Variable | Description | Local Default |
|----------|-------------|---------------|
| `AZURE_COSMOS_ENDPOINT` | Cosmos DB endpoint | `https://localhost:8081` |
| `AZURE_STORAGE_ENDPOINT` | Blob storage endpoint | `http://127.0.0.1:10000/devstoreaccount1` |
| `AZURE_AI_ENDPOINT` | Azure AI Vision endpoint | Mock in local dev |
| `APPLICATIONINSIGHTS_CONNECTION_STRING` | App Insights | Empty (local logs to console) |

## Next Steps

1. Run `dotnet test` to verify all tests pass
2. Review [contracts/openapi.yaml](contracts/openapi.yaml) for the full API surface
3. See [data-model.md](data-model.md) for entity schemas
4. See [research.md](research.md) for architecture decisions

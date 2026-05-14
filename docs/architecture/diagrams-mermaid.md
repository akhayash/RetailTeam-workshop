# Mermaid Diagrams: AI Clothing Fit Assessment Agent

**Version**: 1.0.0 | **Date**: 2026-05-14 | **Status**: Reference

Mermaid renditions of the canonical architecture diagrams. Source: [diagrams.md](diagrams.md) and [solution-architecture.md](solution-architecture.md).

---

## 1. System Context

```mermaid
graph TB
    subgraph External Actors
        Shopper[Online Shopper<br/>consumer]
        RetailFE[Retail Frontend Store<br/>B2B]
        OpsTeam[Operations Team<br/>catalog mgmt]
    end

    API[FitAssess API v1<br/>.NET 8 · Multi-tenant · Stateless]

    subgraph Azure Service Plane
        AIServices[Azure AI Services]
        CosmosDB[Cosmos DB]
        BlobStorage[Blob Storage]
        ServiceBus[Service Bus]
        KeyVault[Key Vault]
        Monitor[Azure Monitor]
    end

    Shopper -->|browser| RetailFE
    RetailFE -->|REST/HTTPS<br/>OAuth 2.0 B2B| API
    OpsTeam -->|REST/HTTPS<br/>OAuth 2.0| API
    API -->|Managed Identity| AIServices
    API -->|Managed Identity| CosmosDB
    API -->|Managed Identity| BlobStorage
    API -->|Managed Identity| ServiceBus
    API -->|Managed Identity| KeyVault
    API -->|Managed Identity| Monitor
```

---

## 2. Container View — FitAssess API

```mermaid
graph TB
    subgraph Presentation Layer - FitAssess.Api
        AC[Assessments Controller]
        PC[Profiles Controller]
        GC[Garments Controller]
        MW[Middleware Pipeline<br/>JWT · Tenant Claim · Correlation ID · Rate Limit · Validation]
    end

    subgraph Service Layer - FitAssess.Services
        FAS[FitAssessment Service]
        SPS[ShopperProfile Service]
        IV[ImageValidator]
        BME[BodyMeasurement Extractor]
        FCE[FitComparison Engine]
        GS[GarmentService]
    end

    subgraph Core Layer - FitAssess.Core
        Models[Models: Tenant · ShopperProfile · Garment · FitAssessment]
        Interfaces[Interfaces: IRepository · IAIClient · IBlobStore]
        Enums[Enums: FitScale · GarmentCategory · AssessmentStatus]
    end

    subgraph Infrastructure Layer - FitAssess.Infrastructure
        VisionClient[AzureAIVisionClient<br/>people detection]
        SafetyClient[ContentSafety Client]
        OpenAIClient[AzureOpenAI MeasurementClient]
        CosmosRepo[CosmosRepository T]
        BlobSvc[BlobStorageService<br/>60s TTL]
        QueueSvc[AssessmentQueue Service]
        Audit[AuditLogger]
        Flags[FeatureFlagsClient]
    end

    AC --> MW
    PC --> MW
    GC --> MW
    MW --> FAS
    MW --> SPS
    MW --> GS
    FAS --> IV
    FAS --> BME
    FAS --> FCE
    SPS --> Models
    GS --> Models
    FAS --> Interfaces
    VisionClient -.->|implements| Interfaces
    SafetyClient -.->|implements| Interfaces
    OpenAIClient -.->|implements| Interfaces
    CosmosRepo -.->|implements| Interfaces
    BlobSvc -.->|implements| Interfaces
```

---

## 3. Three-Tier AI Pipeline

```mermaid
flowchart TB
    Input[Photo + HeightCm]

    subgraph "TIER 1 — Validation (parallel)"
        Vision[Azure AI Vision 4.0<br/>people detection · bounding box · multi-person reject]
        Safety[Azure AI Content Safety<br/>minor/age detection · inappropriate content]
        Defender[Defender for Storage<br/>malware scan]
        Local[Local Checks<br/>MIME type · size ≤10MB · luminance ≥40]
    end

    subgraph "TIER 2 — Measurement Extraction (v1)"
        GPT4o[Azure OpenAI GPT-4o Vision<br/>structured JSON output]
        Output2[shoulderWidth · chestCircumference<br/>waistCircumference · hipCircumference<br/>inseam · armLength · confidence · modelVersion]
    end

    subgraph "TIER 3 — Custom Model (v2 planned)"
        CustomModel[Custom SMPL Body Model<br/>Azure AI Foundry Endpoint<br/>±1-2 cm target accuracy]
    end

    FCE[FitComparisonEngine<br/>deterministic · Core layer]

    Input --> Vision
    Input --> Safety
    Input --> Defender
    Input --> Local
    Vision -->|PASS| GPT4o
    Safety -->|PASS| GPT4o
    Defender -->|PASS| GPT4o
    Local -->|PASS| GPT4o
    GPT4o --> Output2
    Output2 --> FCE
    GPT4o -.->|v2 replacement| CustomModel
    CustomModel -.-> FCE
```

---

## 4. Assessment Request Sequence

```mermaid
sequenceDiagram
    participant FE as Retail Frontend
    participant API as FitAssess API
    participant SVC as Service Layer
    participant T1 as AI Tier 1
    participant T2 as AI Tier 2 (GPT-4o)
    participant DB as Cosmos DB
    participant Blob as Blob Storage

    FE->>API: POST /assessments (photo + heightCm)
    API->>API: JWT validate + rate limit
    API->>SVC: Process assessment request
    SVC->>SVC: Check queue depth / p95
    
    alt Image > 4MB
        SVC->>Blob: Upload image
        Blob-->>SVC: SAS URL
    end

    SVC->>T1: Validate image (parallel)
    Note over T1: People detection<br/>Content safety<br/>Malware scan
    T1-->>SVC: PASS

    SVC->>T2: Extract measurements (photo + heightCm + prompt)
    T2-->>SVC: { measurements, confidence }

    SVC->>DB: Fetch garment data
    DB-->>SVC: Garment measurements
    SVC->>SVC: FitComparisonEngine (compare)

    SVC->>DB: Persist assessment result
    SVC->>Blob: Delete image

    SVC-->>API: Assessment result
    API-->>FE: 200 OK + fit result + confidence

    Note over FE,Blob: If confidence < 70%: isLowConfidence=true + escalation URL
```

---

## 5. Multi-Tenant Data Architecture

```mermaid
erDiagram
    Tenant ||--o{ Garment : "1:N"
    Tenant ||--o{ ShopperProfile : "1:N"
    Tenant ||--o{ FitAssessment : "1:N"
    Tenant ||--o{ AuditLog : "1:N"
    ShopperProfile ||--o{ FitAssessment : "1:N"
    Garment ||--o{ FitAssessment : "referenced by"
    FitAssessment ||--|| AuditLog : "writes to"

    Tenant {
        string id PK
        string displayName
        string entraAppId
        enum rateLimitTier
        enum status
        object toleranceBands
    }

    Garment {
        string id PK
        string tenantId FK
        string garmentId
        string brand
        enum category
        string sizeLabel
        enum fitType
        object measurements
        int version
    }

    ShopperProfile {
        string id PK
        string tenantId FK
        string shopperRef
        object measurements
        decimal extractionConfidence
        datetime consentGrantedAt
    }

    FitAssessment {
        string id PK
        string tenantId FK
        string shopperRef
        string garmentId
        enum overallRecommendation
        object areaScores
        decimal confidence
        string modelVersion
        string correlationId
    }

    AuditLog {
        string id PK
        string tenantId FK
        string action
        datetime timestamp
    }
```

---

## 6. Network and Security Topology

```mermaid
graph TB
    Internet[Internet]
    RetailFE[Retail Frontend Store]

    subgraph Azure Subscription - Production
        subgraph Public Surface
            Ingress[ACA Ingress<br/>HTTPS · WAF · Rate Limit]
        end

        subgraph Container Apps Environment - Private VNet
            API[FitAssess API<br/>2-10 replicas<br/>Managed Identity<br/>JWT validation<br/>Tenant claim extraction]
        end

        subgraph Private Endpoint Subnet
            Cosmos[(Cosmos DB)]
            KV[Key Vault]
            Blob[(Blob Storage)]
            SB[Service Bus]
        end

        subgraph Azure AI Plane - Managed Identity Auth
            OpenAI[Azure OpenAI]
            AIVision[AI Vision]
            ContentSafety[Content Safety]
        end

        subgraph Observability Plane
            AppInsights[Azure Monitor<br/>App Insights]
            LogAnalytics[Log Analytics<br/>90d hot · 1y cold]
        end
    end

    Internet --> RetailFE
    RetailFE -->|TLS 1.2+ · OAuth 2.0 Entra ID| Ingress
    Ingress --> API
    API --> Cosmos
    API --> KV
    API --> Blob
    API --> SB
    API --> OpenAI
    API --> AIVision
    API --> ContentSafety
    API --> AppInsights
    API --> LogAnalytics
```

---

## 7. Deployment Topology

```mermaid
flowchart TB
    Repo[GitHub Repository<br/>main / feature branches]

    subgraph Dev Environment
        DevACA[ACA · 1 replica · Basic]
        DevCosmos[Cosmos DB · Free/Std]
        DevBlob[Blob Storage]
    end

    subgraph Staging Environment
        StagingACA[ACA · 2 replicas · Standard]
        StagingCosmos[Cosmos DB · Standard]
        StagingBlob[Blob Storage]
    end

    subgraph Production - West Europe
        subgraph AZ1[Availability Zone 1]
            ProdACA1[ACA replicas<br/>auto 2-10]
        end
        subgraph AZ2[Availability Zone 2]
            ProdACA2[ACA replicas<br/>auto 2-10]
        end
        subgraph AZ3[Availability Zone 3]
            ProdACA3[ACA replicas<br/>auto 2-10]
        end
        ProdCosmos[(Cosmos DB<br/>Autoscale 400-4000 RU/s<br/>continuous backup)]
        ProdBlob[(Blob Storage<br/>LRS · 60s lifecycle)]
        ProdSB[Service Bus · Standard]
        ProdKV[Key Vault · Standard]
    end

    Repo -->|GitHub Actions| Dev Environment
    Dev Environment -->|manual gate<br/>smoke tests| Staging Environment
    Staging Environment -->|manual prod gate| Production - West Europe
    ProdACA1 <--> ProdACA2
    ProdACA2 <--> ProdACA3
```

---

## 8. CI/CD Pipeline

```mermaid
flowchart LR
    subgraph Build & Test
        Lint[1. Lint & Format]
        Build[2. dotnet build]
        Unit[3. Unit Tests]
        Integ[4. Integration Tests<br/>Testcontainers]
        Contract[5. Contract Tests<br/>OpenAPI]
        Coverage[6. Coverage Gate<br/>≥80%/90%]
    end

    subgraph Security Scan
        SAST[7. SAST<br/>CodeQL/Semgrep]
        SCA[8. SCA<br/>dependency scan]
        SBOM[9. SBOM<br/>CycloneDX]
    end

    subgraph Container
        Docker[10. Container Build]
        Trivy[11. Trivy Scan +<br/>Notation Sign]
    end

    subgraph Deploy Staging
        BicepStg[12. Bicep Deploy<br/>what-if]
        DAST[13. DAST<br/>OWASP ZAP]
        E2E[14. E2E Smoke Tests]
    end

    subgraph Deploy Production
        BicepProd[15. Bicep Deploy<br/>Canary 10%]
        FeatureFlag[16. Progressive Rollout]
        Monitoring[17. Azure Monitor<br/>auto-rollback on SLO breach]
    end

    Lint --> Build --> Unit --> Integ --> Contract --> Coverage
    Coverage --> SAST --> SCA --> SBOM
    SBOM --> Docker --> Trivy
    Trivy -->|manual gate| BicepStg --> DAST --> E2E
    E2E -->|manual gate| BicepProd --> FeatureFlag --> Monitoring
```

---

## 9. Concept A — Cloud-Centric Platform

```mermaid
graph TB
    RetailFE[Retail Frontend<br/>B2B OAuth]

    subgraph Azure Container Apps
        API[FitAssess API<br/>.NET 8 · 2-10 replicas<br/>Managed Identity]
    end

    subgraph Azure AI Plane
        Vision[AI Vision - Tier 1]
        Safety[Content Safety - Tier 1]
        GPT4o[OpenAI GPT-4o - Tier 2]
        Foundry[AI Foundry - Tier 3 v2]
    end

    Cosmos[(Cosmos DB<br/>multi-tenant)]
    Blob[(Blob Storage<br/>60s TTL)]
    SB[Service Bus<br/>async queue]
    KV[Key Vault<br/>zero-secret]
    Monitor[Azure Monitor<br/>OTel]

    RetailFE -->|HTTPS| API
    API --> Vision
    API --> Safety
    API --> GPT4o
    API -.-> Foundry
    API --> Cosmos
    API --> Blob
    API --> SB
    API --> KV
    API --> Monitor
```

---

## 10. Concept B — Edge + AI Agent Operations

```mermaid
graph TB
    subgraph In-Store Edge
        Kiosk[Fitting Room Camera / Kiosk<br/>local pose detection<br/>edge cache<br/>privacy: process locally]
        Associate[Store Associate Mobile<br/>AI Copilot<br/>size recommendation<br/>inventory check<br/>suggest alternatives]
    end

    API[FitAssess API<br/>Cloud Backend<br/>fallback when edge confidence < threshold<br/>model updates pushed to edge<br/>aggregated analytics]

    Kiosk -->|measurements only<br/>not raw images| API
    Associate -->|API call| API

    Note[Human-in-the-loop:<br/>AI recommends → associate decides → shopper accepts]

    style Note fill:#fff3cd,stroke:#856404
```

---

## 11. Concept C — Data Fabric / Intelligence Layer

```mermaid
graph TB
    subgraph Source Domains
        Shoppers[Shopper Measurements<br/>anonymized]
        Garments[Garment Catalog<br/>sizes · materials]
        Returns[Return & Exchange<br/>Transactions]
    end

    Fabric[Microsoft Fabric<br/>Unified Semantic Layer<br/>data lineage · governance<br/>AI-ready data products<br/>cross-domain joins]

    subgraph Consumers
        FitAPI[FitAssess API<br/>real-time assessment]
        ReturnModel[Return Prediction Model<br/>batch/ML]
        Merch[Merchandising Intelligence<br/>size distribution · trends]
    end

    Shoppers --> Fabric
    Garments --> Fabric
    Returns --> Fabric
    Fabric --> FitAPI
    Fabric --> ReturnModel
    Fabric --> Merch
```

---

## 12. Fit Assessment Domain Flow

```mermaid
stateDiagram-v2
    [*] --> Received: POST /assessments
    Received --> Validating: Tier 1 pipeline
    Validating --> Rejected: Validation fails
    Validating --> Extracting: All checks pass
    Extracting --> LowConfidence: confidence < 70%
    Extracting --> Comparing: measurements extracted
    Comparing --> Completed: fit scores calculated
    LowConfidence --> Completed: return with disclaimer
    Rejected --> [*]: 422 + retake guidance
    Completed --> [*]: 200 + fit result

    note right of Validating
        Parallel checks:
        - People detection
        - Content safety
        - Malware scan
        - MIME/size/luminance
    end note

    note right of LowConfidence
        isLowConfidence: true
        escalationUrl provided
        size chart fallback
    end note
```

---

## Diagram Sources

These Mermaid diagrams are derived from:

- [diagrams.md](diagrams.md) — ASCII reference diagrams
- [solution-architecture.md](solution-architecture.md) — system narrative and concept descriptions
- [data-model.md](../../specs/001-clothing-fit-assessment/data-model.md) — entity schemas
- [plan.md](../../specs/001-clothing-fit-assessment/plan.md) — project structure

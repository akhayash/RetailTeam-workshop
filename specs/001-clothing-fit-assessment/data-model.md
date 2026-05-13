# Data Model: AI Clothing Fit Assessment Agent

**Phase**: 1 — Design & Contracts
**Date**: 2026-05-13

## Entity Relationship Overview

```text
┌──────────┐       ┌─────────────────┐       ┌──────────────┐
│  Tenant  │──1:N──│    Garment      │       │   Shopper    │
│          │       │  (per size)     │       │   Profile    │
└──────────┘       └────────┬────────┘       └──────┬───────┘
      │                     │                        │
      │                     └────────┐  ┌────────────┘
      │                              │  │
      │                     ┌────────▼──▼────────┐
      └──────1:N───────────►│  Fit Assessment    │
                            │  (result record)   │
                            └────────────────────┘
```

## Entities

### Tenant

Represents a retail partner consuming the fit assessment service.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | string (GUID) | PK | Unique tenant identifier |
| displayName | string | Required, max 200 | Retail partner name |
| entraAppId | string (GUID) | Required, unique | Entra ID app registration ID |
| rateLimitTier | enum | Required | Throttling tier (Basic: 100 req/min, Standard: 500, Premium: 2000) |
| status | enum | Required | Active, Suspended, Onboarding |
| onboardingDate | datetime | Required | ISO 8601 UTC |
| contactEmail | string | Required, email format | Primary contact for notifications |
| toleranceBands | object | Optional | Custom fit tolerance overrides per garment category (defaults used if null). See ToleranceBands sub-object below. |
| createdAt | datetime | System-generated | ISO 8601 UTC |
| updatedAt | datetime | System-generated | ISO 8601 UTC |

**ToleranceBands sub-object** (per GarmentCategory):

| Field | Type | Unit | Description |
|-------|------|------|-------------|
| category | enum (GarmentCategory) | — | Which garment category this band applies to |
| tightThreshold | decimal | cm | Delta below which fit is "Too Tight" (negative delta magnitude) |
| comfortThreshold | decimal | cm | Delta range for "Good Fit" (+/- this value) |
| looseThreshold | decimal | cm | Delta above which fit is "Too Loose" |

Example: `{ "category": "Top", "tightThreshold": 3.0, "comfortThreshold": 2.0, "looseThreshold": 4.0 }`
When `toleranceBands` is null, system defaults apply (tightThreshold: 4cm, comfortThreshold: 2cm, looseThreshold: 5cm).

**Partition key**: `/id`
**Cosmos container**: `tenants`

---

### Garment

Represents a product SKU with physical measurements for a specific size.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | string | PK (composite: tenantId + garmentId + sizeLabel) | Unique within tenant |
| tenantId | string (GUID) | Required, FK → Tenant | Owning retail partner |
| garmentId | string | Required | External SKU/product identifier from retail partner |
| brand | string | Required, max 100 | Brand name |
| category | enum | Required | Top, Bottom, Dress, Outerwear, Underwear |
| sizeLabel | string | Required | Display size (e.g., "M", "10", "32W") |
| fitType | enum | Required | Slim, Regular, Relaxed |
| measurements | object | Required | See Measurements sub-object |
| isActive | bool | Required | Whether available for assessments |
| version | int | Required | Incremented on update |
| createdAt | datetime | System-generated | ISO 8601 UTC |
| updatedAt | datetime | System-generated | ISO 8601 UTC |

**Measurements sub-object**:

| Field | Type | Unit | Description |
|-------|------|------|-------------|
| shoulderWidth | decimal? | cm | Shoulder seam to seam |
| chestCircumference | decimal? | cm | Fullest part of chest |
| waistCircumference | decimal? | cm | Natural waist |
| hipCircumference | decimal? | cm | Fullest part of hips |
| length | decimal? | cm | Total garment length (shoulder to hem for tops, waist to hem for bottoms) |
| inseam | decimal? | cm | Crotch to hem (bottoms only) |
| sleeveLength | decimal? | cm | Shoulder to wrist (tops only) |

**Partition key**: `/tenantId`
**Cosmos container**: `garments`

---

### ShopperProfile

Represents a shopper's derived body measurements. No PII stored.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | string (GUID) | PK | System-generated profile ID |
| tenantId | string (GUID) | Required, FK → Tenant | Owning retail partner |
| shopperRef | string | Required, max 128 | Opaque hashed shopper ID from frontend |
| measurements | object | Required | See Body Measurements sub-object |
| extractionConfidence | decimal | Required, 0.0–1.0 | Confidence of the measurement extraction |
| consentGrantedAt | datetime | Required | When shopper consented to storage |
| createdAt | datetime | System-generated | ISO 8601 UTC |
| updatedAt | datetime | System-generated | ISO 8601 UTC |

**Body Measurements sub-object**:

| Field | Type | Unit | Description |
|-------|------|------|-------------|
| shoulderWidth | decimal | cm | Shoulder breadth |
| chestCircumference | decimal | cm | Chest at fullest |
| waistCircumference | decimal | cm | Natural waist |
| hipCircumference | decimal | cm | Hips at fullest |
| height | decimal | cm | Total height |
| inseam | decimal | cm | Crotch to floor |
| armLength | decimal | cm | Shoulder to wrist |

**Partition key**: `/tenantId`
**Cosmos container**: `profiles`

**Deletion behavior**: Hard delete within 24 hours of request; audit log entry retained.

---

### FitAssessment

Represents a single assessment result.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | string (GUID) | PK | System-generated assessment ID |
| tenantId | string (GUID) | Required, FK → Tenant | Owning retail partner |
| shopperRef | string | Required | Opaque shopper reference |
| garmentId | string | Required | Reference to garment assessed |
| garmentSizeLabel | string | Required | Size that was assessed |
| overallRecommendation | enum | Required | FitScale value (best size recommendation) |
| areaScores | object | Required | Per-area FitScale values |
| confidence | decimal | Required, 0.0–1.0 | Overall prediction confidence |
| modelVersion | string | Required | AI model version used (YYYY-MM-DD-vN) |
| processingDurationMs | int | Required | End-to-end time in milliseconds |
| correlationId | string | Required | Request tracing ID |
| createdAt | datetime | System-generated | ISO 8601 UTC |

**Area Scores sub-object**:

| Field | Type | Description |
|-------|------|-------------|
| shoulders | enum (FitScale) | Fit at shoulder area |
| chest | enum (FitScale) | Fit at chest area |
| waist | enum (FitScale) | Fit at waist area |
| hips | enum (FitScale) | Fit at hip area |
| length | enum (FitScale) | Fit for garment length |

**Partition key**: `/tenantId`
**Cosmos container**: `assessments`
**TTL**: 365 days (configurable per tenant)

---

## Enumerations

### FitScale

```text
TooTight = 1
SlightlyTight = 2
GoodFit = 3
SlightlyLoose = 4
TooLoose = 5
```

### GarmentCategory

```text
Top, Bottom, Dress, Outerwear, Underwear
```

### GarmentFitType

```text
Slim, Regular, Relaxed
```

### TenantStatus

```text
Onboarding, Active, Suspended
```

### RateLimitTier

```text
Basic (100 req/min), Standard (500 req/min), Premium (2000 req/min)
```

## Validation Rules

1. **ShopperRef**: Must be 32–128 characters (SHA-256 hash or equivalent). Validated via regex.
2. **Measurements**: At least 3 of 5 primary body areas (shoulder, chest, waist, hip, height) must be present for a valid profile.
3. **Garment measurements**: At least 2 areas relevant to the garment category must be present (e.g., bottoms require waist + hip or inseam).
4. **Confidence threshold**: If overall confidence < 0.70, the assessment is flagged as low-confidence and the API response includes a disclaimer.
5. **Tenant scoping**: All queries MUST include tenantId. Repository base class enforces this — queries without tenant context throw at compile time (via generic constraint).

## State Transitions

### Tenant Lifecycle

```text
Onboarding → Active → Suspended → Active (reactivation)
                    → (deleted — soft delete with 90-day retention)
```

### Assessment Flow

```text
ImageReceived → Validating → Extracting → Comparing → Complete
                    ↓              ↓            ↓
                Rejected     ExtractionFailed  LowConfidence
                (feedback)   (retry/fallback)  (disclaimer)
```

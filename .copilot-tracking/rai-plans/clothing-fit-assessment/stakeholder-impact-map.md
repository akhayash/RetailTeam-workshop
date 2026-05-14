# Stakeholder Impact Map: AI Clothing Fit Assessment Agent

**Project Slug**: `clothing-fit-assessment`
**Assessment Date**: 2026-05-14

## Stakeholder Classification

### Direct Stakeholders (Interact with the system)

| Stakeholder | Role | AI Interaction | Potential Impact | Vulnerability |
|-------------|------|----------------|-----------------|---------------|
| **Online Shoppers** | End users (via frontend) | Submit body photos; receive fit recommendations | High — receive AI-generated body assessments that influence purchase decisions | High — body image sensitivity; privacy of biometric-adjacent data; potential for inaccurate recommendations leading to poor fit and frustration |
| **Retail Partners (Tenants)** | B2B API consumers | Integrate fit assessment into storefronts; manage garment catalogs | Medium — business outcomes depend on recommendation quality; brand reputation tied to AI accuracy | Medium — liability for AI-driven customer experience; data processing obligations |
| **Retail Frontend Teams** | Technical integrators | Consume API; render fit results in UX | Low — technical integration only | Low |
| **Merchandising / Catalog Teams** | Data providers | Upload garment measurement data | Low — provide input data, no direct AI interaction | Low — data quality affects downstream AI accuracy |

### Indirect Stakeholders (Affected but do not directly interact)

| Stakeholder | Role | Potential Impact | Vulnerability |
|-------------|------|-----------------|---------------|
| **Shoppers who choose not to use the feature** | Non-users | May feel pressure to use AI fit assessment; existing size chart experience could degrade if resources shift | Low |
| **Retail customer service teams** | Support | Handle disputes from inaccurate fit recommendations | Medium — increased workload from AI errors |
| **Garment suppliers / brands** | Data sources | Return rate changes affect supplier relationships; inaccurate fit data could be attributed to their products | Medium |
| **Regulators (GDPR DPAs, FTC, EU AI Act authorities)** | Oversight | Monitor compliance of biometric-adjacent AI processing at retail scale | N/A — oversight role |
| **Disability advocacy groups** | Advocacy | System accuracy for users with disabilities affects inclusivity | Medium — underrepresentation in training data |
| **Body positivity / anti-discrimination advocates** | Advocacy | Language and framing of fit recommendations affects body image discourse | Medium — potential for AI outputs to reinforce size bias |

### Organizational Stakeholders

| Stakeholder | Role | Potential Impact |
|-------------|------|-----------------|
| **VirtualMirror Engineering Team** | Builders | Responsible for AI accuracy, bias monitoring, incident response |
| **Privacy Office / Legal** | Governance | DPIA approval, data processing agreements, regulatory compliance |
| **AI Ethics Board** | Governance | Model deployment approval, bias evaluation, responsible AI review |
| **Security Team** | Governance | Threat model review, penetration testing, incident response |

## Impact Severity Matrix

| Impact Category | Shopper (Direct) | Retail Partner | Regulators |
|----------------|-----------------|----------------|------------|
| **Physical safety** | None (clothing recommendation only) | None | N/A |
| **Financial** | Low (wrong size → return cost) | Medium (return rate, brand trust) | N/A |
| **Privacy** | High (body photos, measurements) | Medium (data processor obligations) | High (compliance enforcement) |
| **Dignity / body image** | High (body-related AI output) | Medium (brand association) | Medium (discrimination oversight) |
| **Fairness / equity** | High (accuracy parity across demographics) | Medium (equitable service delivery) | High (bias monitoring) |
| **Autonomy** | Medium (AI influences purchase decisions) | Low | Medium (informed consent) |

## Key Observations

1. **Shoppers are the most vulnerable stakeholder** — they submit biometric-adjacent data and receive AI assessments about their body that could affect self-image and purchasing behavior
2. **Body image sensitivity is the dominant impact vector** — unlike most AI systems, this one directly assesses and comments on human bodies
3. **Demographic accuracy parity is critical** — if the AI is less accurate for certain body types, skin tones, or sizes, it creates a discriminatory experience
4. **The system explicitly avoids high-stakes autonomous decisions** — fit recommendations are advisory with confidence scoring and human escalation
5. **Privacy architecture is strong** — transient photo processing, opaque IDs, consent-gated storage, and 24h deletion align with data minimization principles

# OWASP Security Assessment Report

**Date:** 2026-05-14
**Repository:** PotocnikRobert/RetailTeam-workshop
**Agent:** Security Reviewer
**Skills applied:** owasp-top-10, owasp-llm, owasp-infrastructure, owasp-cicd, secure-by-design, owasp-agentic

> [!CAUTION]
> This prompt is an **assistive tool only** and does not replace professional security tooling (SAST, DAST, SCA, penetration testing, compliance scanners) or qualified human review. All AI-generated vulnerability findings **must** be reviewed and validated by qualified security professionals before use. AI outputs may contain inaccuracies, miss critical threats, or produce recommendations that are incomplete or inappropriate for your environment.

---

## Executive Summary

This assessment evaluated the RetailTeam-workshop repository across six OWASP security frameworks covering web applications, LLM applications, infrastructure, CI/CD pipelines, secure-by-design principles, and agentic AI risks. Of 61 total checks, 2 findings received FAIL status (zero logging and zero continuous assurance) and 32 received PARTIAL status, with 10 HIGH-severity findings concentrated in missing operational security controls, unimplemented AI safety guardrails, and absent network isolation. Deep verification confirmed 24 findings, downgraded 10 to lower severity, and disproved 1 (injection via unsafe_allow_html). The repository demonstrates strong security architecture and planning artifacts but critically lacks any operational enforcement — no CI/CD, no SAST/DAST, no logging, no network isolation, and no implemented AI safety controls.

### Summary Counts

| Status       | Count  |
|--------------|--------|
| PASS         | 14     |
| FAIL         | 2      |
| PARTIAL      | 32     |
| NOT_ASSESSED | 13     |
| **Total**    | **61** |

### Severity Breakdown (FAIL + PARTIAL only)

| Severity | Count |
|----------|-------|
| CRITICAL | 0     |
| HIGH     | 10    |
| MEDIUM   | 18    |
| LOW      | 6     |

### Verification Summary

| Verdict    | Count |
|------------|-------|
| CONFIRMED  | 24    |
| DISPROVED  | 1     |
| DOWNGRADED | 10    |
| UNCHANGED  | 26    |

---

## Findings by Framework

### OWASP Top 10 for Web Applications (owasp-top-10)

| ID | Title | Status | Severity | Location | Finding | Recommendation | Verdict | Justification |
|----|-------|--------|----------|----------|---------|----------------|---------|---------------|
| A09:2025 | Security Logging and Alerting Failures | FAIL | HIGH | [poc/fit-signal-poc/app/streamlit_app.py#L1](poc/fit-signal-poc/app/streamlit_app.py#L1) | Zero logging across entire codebase. No import logging. Bare except Exception at line 968. | Add logging. Implement OpenTelemetry. Replace bare except. | CONFIRMED | Zero logging verified across all source files. |
| A03:2025 | Software Supply Chain Failures | PARTIAL | MEDIUM | [poc/fit-signal-poc/pyproject.toml#L7](poc/fit-signal-poc/pyproject.toml#L7) | uv.lock provides hash integrity. No CI/CD, SBOM, or dependency scanning. | Configure Dependabot. Add CI with scanning. Generate SBOM. | CONFIRMED | Absence of CI/CD and SBOM confirmed. |
| A08:2025 | Software or Data Integrity Failures | PARTIAL | MEDIUM | [poc/fit-signal-poc/src/pose_detection.py#L85](poc/fit-signal-poc/src/pose_detection.py#L85) | MediaPipe models loaded without hash verification. No CI/CD pipeline. | Add SHA-256 checksum verification for models. Implement CI/CD. | CONFIRMED | Model loading code verified — existence check only. |
| A10:2025 | Mishandling of Exceptional Conditions | PARTIAL | MEDIUM | [poc/fit-signal-poc/app/streamlit_app.py#L968](poc/fit-signal-poc/app/streamlit_app.py#L968) | Bare except Exception with noqa:BLE001 silently discards all errors. | Replace with specific exceptions. Add logging. | CONFIRMED | Bare except confirmed at line 968. |
| A02:2025 | Security Misconfiguration | PARTIAL | LOW | [poc/fit-signal-poc/pyproject.toml#L7](poc/fit-signal-poc/pyproject.toml#L7) | Version ranges used but uv.lock pins with SHA-256. PoC is local demo. | Add upper-bound constraints on critical deps. | DOWNGRADED | uv.lock mitigates risk substantially. |
| A05:2025 | Injection | PASS | N/A | N/A | N/A | N/A | DISPROVED | All unsafe_allow_html renders application-controlled content only. |
| A06:2025 | Insecure Design | PASS | N/A | N/A | N/A | N/A | UNCHANGED | Comprehensive threat model in place. |
| A01:2025 | Broken Access Control | NOT_ASSESSED | N/A | N/A | N/A | N/A | UNCHANGED | No server-side code exists. |
| A04:2025 | Cryptographic Failures | NOT_ASSESSED | N/A | N/A | N/A | N/A | UNCHANGED | No cryptographic operations in codebase. |
| A07:2025 | Authentication Failures | NOT_ASSESSED | N/A | N/A | N/A | N/A | UNCHANGED | No authentication code exists. |

### OWASP Top 10 for LLM Applications (owasp-llm)

| ID | Title | Status | Severity | Location | Finding | Recommendation | Verdict | Justification |
|----|-------|--------|----------|----------|---------|----------------|---------|---------------|
| LLM01:2025 | Prompt Injection | PARTIAL | HIGH | [specs/001-clothing-fit-assessment/tasks.md#L129](specs/001-clothing-fit-assessment/tasks.md#L129) | Multimodal injection via body photos. EXIF stripping identified but unimplemented. | Implement EXIF stripping. Enforce structured output. Add range validation. | CONFIRMED | No EXIF stripping task exists in plan. |
| LLM02:2025 | Sensitive Information Disclosure | PARTIAL | HIGH | [docs/architecture/threat-model.md#L63](docs/architecture/threat-model.md#L63) | Biometric photos with 60s purge and PII scrubbing — none implemented. | Implement Blob lifecycle purge. Configure PII scrubbing. | CONFIRMED | No purge or scrubbing code exists. |
| LLM05:2025 | Improper Output Handling | PARTIAL | HIGH | [specs/001-clothing-fit-assessment/tasks.md#L134](specs/001-clothing-fit-assessment/tasks.md#L134) | GPT-5.2 output drives pipeline. Schema and plausibility checks unimplemented. | Implement JSON schema. Add plausibility rules. Validate consistency. | CONFIRMED | No output validation code exists. |
| LLM03:2025 | Supply Chain | PARTIAL | MEDIUM | [poc/fit-signal-poc/app/streamlit_app.py#L59](poc/fit-signal-poc/app/streamlit_app.py#L59) | MediaPipe models without checksum. SBOM/Trivy planned but unimplemented. | Add SHA-256 checksums. Implement SBOM in CI/CD. | CONFIRMED | Models loaded without integrity verification. |
| LLM09:2025 | Misinformation | PARTIAL | MEDIUM | [docs/architecture/threat-model.md#L150](docs/architecture/threat-model.md#L150) | Hallucinated measurements identified. Confidence threshold unimplemented. | Implement 70% threshold. Add cross-validation. Display AI disclosure. | CONFIRMED | No confidence threshold code exists. |
| LLM10:2025 | Unbounded Consumption | PARTIAL | MEDIUM | [specs/001-clothing-fit-assessment/tasks.md#L96](specs/001-clothing-fit-assessment/tasks.md#L96) | Seven resource controls designed, none implemented. D-1 flood DREAD 9.0. | Implement rate limiting. Enforce upload limits. Set timeouts. | CONFIRMED | No rate limiting or resource controls exist. |
| LLM06:2025 | Excessive Agency | PASS | N/A | N/A | N/A | N/A | UNCHANGED | GPT-5.2 constrained to measurement extraction. |
| LLM08:2025 | Vector and Embedding Weaknesses | PASS | N/A | N/A | N/A | N/A | UNCHANGED | No RAG or vector databases used. |
| LLM04:2025 | Data and Model Poisoning | NOT_ASSESSED | N/A | N/A | N/A | N/A | UNCHANGED | Azure-managed models. |
| LLM07:2025 | System Prompt Leakage | NOT_ASSESSED | N/A | N/A | N/A | N/A | UNCHANGED | No system prompt exists yet. |

### OWASP Infrastructure Security Top 10 (owasp-infrastructure)

| ID | Title | Status | Severity | Location | Finding | Recommendation | Verdict | Justification |
|----|-------|--------|----------|----------|---------|----------------|---------|---------------|
| ISR06:2024 | Insecure Network Access Management | PARTIAL | HIGH | [docs/architecture/solution-architecture.md#L485](docs/architecture/solution-architecture.md#L485) | No VNet, private endpoints, NSGs, or egress filtering. infra/ missing. | Create Bicep for VNet, NSGs, private endpoints. Deploy Firewall. | CONFIRMED | No infrastructure code exists. |
| ISR01:2024 | Outdated Software | PARTIAL | MEDIUM | [specs/001-clothing-fit-assessment/plan.md#L7](specs/001-clothing-fit-assessment/plan.md#L7) | .NET 8.0 LTS current. No scanning operational. No csproj exists. | Pin NuGet packages. Add dotnet nuget audit. Configure Dependabot. | CONFIRMED | No dependency scanning configured. |
| ISR02:2024 | Insufficient Threat Detection | PARTIAL | MEDIUM | [docs/architecture/solution-architecture.md#L494](docs/architecture/solution-architecture.md#L494) | OpenTelemetry planned. No SIEM, network detection, or runbooks. | Integrate Sentinel. Enable Defender. Create runbooks. | CONFIRMED | No monitoring infrastructure deployed. |
| ISR03:2024 | Insecure Configurations | PARTIAL | MEDIUM | [docs/architecture/threat-model.md#L233](docs/architecture/threat-model.md#L233) | No security headers. Private endpoints not enforced. No IaC. | Implement headers. Create Bicep with private endpoints. Add scanning. | DOWNGRADED | Blob ZRS correct. VNet classified as pre-prod blocker. |
| ISR08:2024 | Information Leakage | PARTIAL | MEDIUM | [docs/architecture/threat-model.md#L105](docs/architecture/threat-model.md#L105) | Strong data minimization designed. Defender/DLP not implemented. | Enable Defender for Storage. Implement purge monitoring. Configure DLP. | CONFIRMED | No runtime data protection controls active. |
| ISR04:2024 | Insecure Resource and User Management | PARTIAL | LOW | [docs/architecture/threat-model.md#L89](docs/architecture/threat-model.md#L89) | Strong managed identity foundation. MFA planned. PIM/PIM missing. | Implement PIM. Document off-boarding. Enforce MFA via CA. | DOWNGRADED | MFA and access reviews are planned, not absent. |
| ISR09:2024 | Insecure Access to Resources | PARTIAL | LOW | [docs/architecture/threat-model.md#L219](docs/architecture/threat-model.md#L219) | PaaS-only makes bastion irrelevant. PIM and alerts are genuine gaps. | Implement PIM. Configure Activity Log alerts. | DOWNGRADED | Core access architecture is sound for PaaS. |
| ISR05:2024 | Insecure Use of Cryptography | PASS | N/A | N/A | N/A | N/A | UNCHANGED | TLS 1.2+ enforced. Cosmos encrypts at rest. |
| ISR07:2024 | Insecure Authentication Methods | PASS | N/A | N/A | N/A | N/A | UNCHANGED | Entra ID OAuth 2.0 with managed identity. |
| ISR10:2024 | Insufficient Asset Management | PASS | N/A | N/A | N/A | N/A | UNCHANGED | Comprehensive documentation and service map. |

### OWASP Top 10 CI/CD Security Risks (owasp-cicd)

| ID | Title | Status | Severity | Location | Finding | Recommendation | Verdict | Justification |
|----|-------|--------|----------|----------|---------|----------------|---------|---------------|
| CICD-SEC-1:2025 | Insufficient Flow Control | PARTIAL | MEDIUM | Repository-wide | No branch protection, CODEOWNERS, or required reviewers. | Enable branch protection before production code. Add CODEOWNERS. | DOWNGRADED | No production code or CI/CD reduces exploitability. |
| CICD-SEC-6:2025 | Insufficient Credential Hygiene | PARTIAL | MEDIUM | Repository-wide | No credentials committed (positive). No secret scanning configured. | Enable GitHub secret scanning and push protection. | CONFIRMED | No automated secret scanning active. |
| CICD-SEC-9:2025 | Improper Artifact Integrity Validation | PARTIAL | MEDIUM | [specs/001-clothing-fit-assessment/tasks.md#L275](specs/001-clothing-fit-assessment/tasks.md#L275) | No signing, SBOM, or container signing. No production artifacts exist. | Implement commit signing. Include SBOM/signing in first CI pipeline. | DOWNGRADED | No production artifacts exist to sign. |
| CICD-SEC-3:2025 | Dependency Chain Abuse | PARTIAL | LOW | [poc/fit-signal-poc/pyproject.toml](poc/fit-signal-poc/pyproject.toml) | Python well-protected via uv.lock with SHA-256. .NET hypothetical. | Enable RestorePackagesWithLockFile when .NET scaffolded. | DOWNGRADED | uv.lock with hashes provides strong protection. |
| CICD-SEC-10:2025 | Insufficient Logging and Visibility | PARTIAL | LOW | Repository-wide | No CI/CD system exists to log. GitHub provides built-in audit. | Include audit logging in T134 CI pipeline from day one. | DOWNGRADED | No CI/CD system exists — risk is hypothetical. |
| CICD-SEC-2:2025 | Inadequate IAM | NOT_ASSESSED | N/A | N/A | N/A | N/A | UNCHANGED | No CI/CD systems deployed. |
| CICD-SEC-4:2025 | Poisoned Pipeline Execution | NOT_ASSESSED | N/A | N/A | N/A | N/A | UNCHANGED | No CI/CD pipeline exists. |
| CICD-SEC-5:2025 | Insufficient PBAC | NOT_ASSESSED | N/A | N/A | N/A | N/A | UNCHANGED | No pipeline infrastructure. |
| CICD-SEC-7:2025 | Insecure System Configuration | NOT_ASSESSED | N/A | N/A | N/A | N/A | UNCHANGED | No self-managed CI/CD infrastructure. |
| CICD-SEC-8:2025 | Ungoverned 3rd Party Services | NOT_ASSESSED | N/A | N/A | N/A | N/A | UNCHANGED | No third-party CI/CD integrations. |

### Secure by Design Principles (secure-by-design)

| ID | Title | Status | Severity | Location | Finding | Recommendation | Verdict | Justification |
|----|-------|--------|----------|----------|---------|----------------|---------|---------------|
| SBD-03 | Secure Product Development | PARTIAL | HIGH | [.copilot-tracking/security-plans/fitassess/security-plan.md#L340](../../../.copilot-tracking/security-plans/fitassess/security-plan.md#L340) | Zero CI/CD, SAST, SCA, or secure coding standards implemented. | Establish CI/CD with SAST/SCA as first task. Create standards. | CONFIRMED | No pipeline or tooling exists. |
| SBD-06 | Detect and Respond | PARTIAL | HIGH | [.copilot-tracking/security-plans/fitassess/security-plan.md#L291](../../../.copilot-tracking/security-plans/fitassess/security-plan.md#L291) | No IR plan, runbooks, or escalation path. No SIEM or alerting. | Create IR plan. Define thresholds. Establish retention. Create runbooks. | CONFIRMED | No operational security artifacts exist. |
| SBD-10 | Continuous Assurance | FAIL | HIGH | Repository-wide | Zero continuous assurance active. No CI/CD, SAST/DAST/SCA, vuln mgmt. | Establish CI/CD with security gates. Create SECURITY.md. Schedule pen test. | CONFIRMED | Complete absence of assurance mechanisms verified. |
| SBD-01 | Security Governance | PARTIAL | MEDIUM | [.copilot-tracking/security-plans/fitassess/security-plan.md#L1](../../../.copilot-tracking/security-plans/fitassess/security-plan.md#L1) | Generic role titles. No named security owner. No champion. | Assign named individuals. Define champion. Establish scorecard. | CONFIRMED | No named owners in security plan. |
| SBD-04 | Supply Chain Security | PARTIAL | MEDIUM | [poc/fit-signal-poc/pyproject.toml#L7](poc/fit-signal-poc/pyproject.toml#L7) | Python deps better managed than assessed. No SBOM or .NET strategy. | Generate SBOM. Enable lock files for .NET. Configure Dependabot. | DOWNGRADED | uv.lock provides full pinning with hashes. |
| SBD-08 | Minimize Attack Surface | PARTIAL | MEDIUM | [.copilot-tracking/security-plans/fitassess/security-plan.md#L475](../../../.copilot-tracking/security-plans/fitassess/security-plan.md#L475) | Swagger exposure, CORS, debug endpoints, private endpoints unresolved. | Disable Swagger in prod. Define CORS. Deploy private endpoints. | CONFIRMED | Gaps identified in plan but not addressed. |
| SBD-02 | Risk-Driven Approach | PASS | N/A | N/A | N/A | N/A | UNCHANGED | Comprehensive STRIDE+DREAD threat model. |
| SBD-05 | Usable Security Controls | PASS | N/A | N/A | N/A | N/A | UNCHANGED | Managed identity and Entra ID OAuth. |
| SBD-07 | Flexible Architecture | PASS | N/A | N/A | N/A | N/A | UNCHANGED | Clean Architecture with ADRs. |
| SBD-09 | Defense in Depth | PASS | N/A | N/A | N/A | N/A | UNCHANGED | Layered defense designed. |
| SBD-11 | Secure Deprecation | NOT_ASSESSED | N/A | N/A | N/A | N/A | UNCHANGED | Pre-implementation project. |

### OWASP Top 10 for Agentic Applications (owasp-agentic)

| ID | Title | Status | Severity | Location | Finding | Recommendation | Verdict | Justification |
|----|-------|--------|----------|----------|---------|----------------|---------|---------------|
| ASI01:2026 | Agent Goal Hijack | PARTIAL | HIGH | [specs/001-clothing-fit-assessment/tasks.md#L129](specs/001-clothing-fit-assessment/tasks.md#L129) | EXIF stripping Critical Priority 1 but no task in plan. Structured output constrains shape not values. | Add EXIF stripping task. Pin prompt by hash. Add range validation. | CONFIRMED | No EXIF stripping task in tasks.md. |
| ASI02:2026 | Tool Misuse and Exploitation | PARTIAL | HIGH | [specs/001-clothing-fit-assessment/plan.md#L130](specs/001-clothing-fit-assessment/plan.md#L130) | L1/L2 degradation bypasses safety controls without human approval. | Add ops approval gate. Separate safety from quality. Reject not skip. | CONFIRMED | Degradation ladder bypasses minor detection. |
| ASI06:2026 | Memory and Context Poisoning | PARTIAL | MEDIUM | [specs/001-clothing-fit-assessment/plan.md#L137](specs/001-clothing-fit-assessment/plan.md#L137) | Profile poisoning via adversarial images. No integrity checks or drift detection. | Add validation before storage. Implement drift detection. Block during degraded. | CONFIRMED | No integrity checks on profile storage. |
| ASI08:2026 | Cascading Failures | PARTIAL | MEDIUM | [docs/architecture/resiliency-review.md#L63](docs/architecture/resiliency-review.md#L63) | L2→bad images→stored in profile→L3 reuse. No lineage metadata. | Add degradation-aware gate. Add lineage metadata. Implement Polly. | CONFIRMED | No degradation awareness in profile storage. |
| ASI04:2026 | Agentic Supply Chain | PARTIAL | LOW | [specs/001-clothing-fit-assessment/tasks.md#L268](specs/001-clothing-fit-assessment/tasks.md#L268) | SBOM/Trivy/Notation in T134. AI models Azure-managed. Garment data gap. | Schedule T134 early. Add prompt content-hash. Consider HMAC for garments. | DOWNGRADED | Azure-managed models shift runtime integrity responsibility. |
| ASI03:2026 | Identity and Privilege Abuse | PASS | N/A | N/A | N/A | N/A | UNCHANGED | Entra ID with managed identities and tenant isolation. |
| ASI05:2026 | Unexpected Code Execution | PASS | N/A | N/A | N/A | N/A | UNCHANGED | No code generation or execution. |
| ASI09:2026 | Human-Agent Trust Exploitation | PASS | N/A | N/A | N/A | N/A | UNCHANGED | AI recommends, human decides framing. |
| ASI07:2026 | Insecure Inter-Agent Communication | NOT_ASSESSED | N/A | N/A | N/A | N/A | UNCHANGED | Single-service API architecture. |
| ASI10:2026 | Rogue Agents | NOT_ASSESSED | N/A | N/A | N/A | N/A | UNCHANGED | Deterministic pipeline, not autonomous agent. |

---

## Detailed Remediation Guidance

### HIGH Severity

#### A09:2025 — Security Logging and Alerting Failures

**File:** [poc/fit-signal-poc/app/streamlit_app.py#L1](poc/fit-signal-poc/app/streamlit_app.py#L1)

**Offending Code:**

```python
# streamlit_app.py — No logging imports or configuration anywhere in file
import streamlit as st
# ... 960+ lines with zero logging statements
```

**Example Fix:**

```python
import logging
import streamlit as st

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

# At application entry
logger.info("Application started")
```

**Steps:**

1. Add `import logging` and configure structured logging at module level.
2. Replace all bare `except Exception` blocks with specific exception types and log the error.
3. Add security event logging for failed operations and unexpected inputs.
4. Plan OpenTelemetry integration for production with Azure Monitor exporter.

**Verification verdict:** CONFIRMED — Zero logging imports or statements across entire codebase verified by grep.

---

#### LLM01:2025 — Prompt Injection

**File:** [specs/001-clothing-fit-assessment/tasks.md#L129](specs/001-clothing-fit-assessment/tasks.md#L129)

**Offending Code:**

```markdown
<!-- tasks.md — EXIF stripping listed as Critical Priority 1 but no implementation task -->
## Security Controls (Critical Priority 1)
- Strip EXIF/XMP/IPTC metadata from uploaded images
<!-- No corresponding task in the implementation plan -->
```

**Example Fix:**

```csharp
// ImageSanitizer.cs — Strip all metadata before AI processing
public async Task<Stream> SanitizeImageAsync(Stream input)
{
    using var image = await Image.LoadAsync(input);
    image.Metadata.ExifProfile = null;
    image.Metadata.XmpProfile = null;
    image.Metadata.IptcProfile = null;
    var output = new MemoryStream();
    await image.SaveAsJpegAsync(output);
    output.Position = 0;
    return output;
}
```

**Steps:**

1. Add explicit EXIF/XMP/IPTC stripping task to the implementation plan.
2. Implement image sanitization as the first step in the upload pipeline.
3. Add physiological range validation on extracted measurements (e.g., height 100–220 cm).
4. Pin system prompt by content hash to detect tampering.

**Verification verdict:** CONFIRMED — No EXIF stripping task exists in tasks.md implementation section.

---

#### LLM02:2025 — Sensitive Information Disclosure

**File:** [docs/architecture/threat-model.md#L63](docs/architecture/threat-model.md#L63)

**Offending Code:**

```markdown
<!-- threat-model.md — 60s auto-purge designed but not implemented -->
| I-1 | Photo Exfiltration | 5.6 | Biometric images in Blob during 60s window |
## Mitigations: Blob lifecycle policy (60s TTL), PII scrubbing in telemetry
<!-- No implementation exists -->
```

**Example Fix:**

```csharp
// BlobStorageOptions.cs — Configure lifecycle purge
public class BlobStorageOptions
{
    public int ImageTtlSeconds { get; set; } = 60;
    public bool EnableLifecyclePolicy { get; set; } = true;
}

// In Bicep: storage account lifecycle management rule
// rule: delete blobs older than 1 minute in 'uploads' container
```

**Steps:**

1. Implement Azure Blob lifecycle management policy with 60-second TTL on upload container.
2. Configure OpenTelemetry PII scrubbing to exclude body measurement data from telemetry.
3. Verify Azure OpenAI DPA covers biometric-adjacent data processing.
4. Add integration test validating blobs are deleted after TTL expiry.

**Verification verdict:** CONFIRMED — No purge implementation or PII scrubbing code exists.

---

#### LLM05:2025 — Improper Output Handling

**File:** [specs/001-clothing-fit-assessment/tasks.md#L134](specs/001-clothing-fit-assessment/tasks.md#L134)

**Offending Code:**

```markdown
<!-- tasks.md — Output validation designed but not implemented -->
## Output Validation
- JSON schema enforcement
- Plausibility checks (anatomical ranges)
- Confidence scoring (70% threshold)
<!-- All unimplemented — malformed measurements would flow unchecked -->
```

**Example Fix:**

```csharp
// MeasurementValidator.cs
public ValidationResult Validate(BodyMeasurements measurements)
{
    var errors = new List<string>();
    if (measurements.Height is < 100 or > 220)
        errors.Add("Height outside physiological range (100-220 cm)");
    if (measurements.Chest is < 50 or > 180)
        errors.Add("Chest outside physiological range (50-180 cm)");
    if (measurements.Confidence < 0.70)
        errors.Add($"Confidence {measurements.Confidence:P0} below 70% threshold");
    return new ValidationResult(errors.Count == 0, errors);
}
```

**Steps:**

1. Implement strict JSON schema validation on GPT-5.2 output using System.Text.Json source generators.
2. Add physiological plausibility rules for all body measurements.
3. Implement cross-measurement consistency checks (e.g., waist < chest).
4. Enforce 70% confidence threshold — reject and return graceful error below threshold.

**Verification verdict:** CONFIRMED — No output validation code exists in repository.

---

#### ISR06:2024 — Insecure Network Access Management

**File:** [docs/architecture/solution-architecture.md#L485](docs/architecture/solution-architecture.md#L485)

**Offending Code:**

```markdown
<!-- solution-architecture.md — Network isolation planned, not implemented -->
## Network Security
- VNet integration for Container Apps
- Private endpoints for Cosmos DB, Blob Storage, Azure OpenAI
<!-- infra/ directory does not exist. No Bicep, no NSGs, no VNet. -->
```

**Example Fix:**

```bicep
// main.bicep — VNet with private endpoints
resource vnet 'Microsoft.Network/virtualNetworks@2023-09-01' = {
  name: 'vnet-fitassess'
  location: location
  properties: {
    addressSpace: { addressPrefixes: ['10.0.0.0/16'] }
    subnets: [
      { name: 'snet-apps', properties: { addressPrefix: '10.0.1.0/24' } }
      { name: 'snet-private-endpoints', properties: { addressPrefix: '10.0.2.0/24' } }
    ]
  }
}
```

**Steps:**

1. Create `infra/` directory with Bicep modules for VNet, NSGs, and private endpoints.
2. Configure private endpoints for Cosmos DB, Blob Storage, and Azure OpenAI.
3. Deploy NSG rules restricting traffic to required flows only.
4. Add Azure Firewall or NAT Gateway for egress filtering.
5. Document network access matrix.

**Verification verdict:** CONFIRMED — No `infra/` directory or network infrastructure code exists.

---

#### SBD-03 — Secure Product Development

**File:** [.copilot-tracking/security-plans/fitassess/security-plan.md#L340](.copilot-tracking/security-plans/fitassess/security-plan.md#L340)

**Offending Code:**

```markdown
<!-- security-plan.md — Constitution mandates CI/CD but none exists -->
## Operational Bucket: Secure Development Lifecycle
- SAST: Required (not implemented)
- SCA: Required (not implemented)
- CI/CD: Required (not implemented)
- Secure coding standards: Required (not implemented)
```

**Example Fix:**

```yaml
# .github/workflows/security.yml
name: Security Gates
on: [push, pull_request]
jobs:
  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: github/codeql-action/init@v3
      - uses: github/codeql-action/analyze@v3
  sca:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/dependency-review-action@v4
```

**Steps:**

1. Create GitHub Actions workflow with SAST (CodeQL) and SCA (dependency review).
2. Establish secure coding standards document.
3. Configure required status checks on main branch.
4. Add DAST scanning for production deployments.

**Verification verdict:** CONFIRMED — Zero CI/CD or security tooling configuration in repository.

---

#### SBD-06 — Detect and Respond

**File:** [.copilot-tracking/security-plans/fitassess/security-plan.md#L291](.copilot-tracking/security-plans/fitassess/security-plan.md#L291)

**Offending Code:**

```markdown
<!-- security-plan.md — IR explicitly acknowledged as missing -->
## Operational Bucket: Incident Response
- IR Plan: NOT IMPLEMENTED
- Runbooks: NOT IMPLEMENTED
- Escalation path: NOT DEFINED
- SIEM integration: NOT IMPLEMENTED
```

**Example Fix:**

```markdown
# Incident Response Plan
## Severity Levels
| Level | Response Time | Escalation |
|-------|--------------|------------|
| P1    | 15 min       | Security Lead + Engineering Director |
| P2    | 1 hour       | Security Lead |
| P3    | 24 hours     | On-call engineer |

## Runbook: Data Breach
1. Isolate affected storage account
2. Revoke managed identity credentials
3. Notify DPO within 72 hours
```

**Steps:**

1. Create incident response plan with severity levels and response times.
2. Define alerting thresholds for security events in Azure Monitor.
3. Establish log retention policies (minimum 90 days hot, 1 year cold).
4. Create runbooks for top 5 threat scenarios from threat model.
5. Schedule tabletop exercise within first sprint of production.

**Verification verdict:** CONFIRMED — No incident response artifacts exist. Explicitly acknowledged in security plan.

---

#### SBD-10 — Continuous Assurance

**File:** Repository-wide

**Offending Code:**

```text
# Repository has zero continuous assurance mechanisms:
# - No .github/workflows/ directory
# - No SECURITY.md
# - No dependabot.yml
# - No codeql-analysis.yml
# - No vulnerability disclosure policy
```

**Example Fix:**

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/poc/fit-signal-poc"
    schedule:
      interval: "weekly"
  - package-ecosystem: "nuget"
    directory: "/backend"
    schedule:
      interval: "weekly"
```

**Steps:**

1. Create `.github/workflows/` with CI/CD pipeline including security gates.
2. Add `SECURITY.md` with vulnerability disclosure policy.
3. Configure Dependabot for all package ecosystems.
4. Define vulnerability management SLA (Critical: 24h, High: 7d, Medium: 30d).
5. Schedule quarterly penetration testing post-launch.

**Verification verdict:** CONFIRMED — Complete absence of continuous assurance mechanisms verified.

---

#### ASI01:2026 — Agent Goal Hijack

**File:** [specs/001-clothing-fit-assessment/tasks.md#L129](specs/001-clothing-fit-assessment/tasks.md#L129)

**Offending Code:**

```markdown
<!-- tasks.md — Critical security control missing from implementation plan -->
## Security Controls
Critical Priority 1: EXIF stripping
<!-- But implementation tasks section contains no EXIF stripping task -->
## Implementation Tasks
T101: Image upload endpoint
T102: Florence-2 integration
<!-- No T-xxx for EXIF stripping -->
```

**Example Fix:**

```markdown
## Implementation Tasks
T100: Image sanitization pipeline (EXIF/XMP/IPTC stripping) [Priority: P0]
  - Strip all metadata before any AI processing
  - Validate image dimensions and format
  - Reject images with embedded payloads
T101: Image upload endpoint [depends: T100]
```

**Steps:**

1. Add explicit EXIF stripping task as P0 dependency before image processing tasks.
2. Implement metadata stripping in upload pipeline before any AI model receives the image.
3. Add physiological range validation (100–220 cm height, proportional limits).
4. Pin system prompt content hash and validate at startup.

**Verification verdict:** CONFIRMED — EXIF stripping listed as Critical Priority 1 but no implementation task exists.

---

#### ASI02:2026 — Tool Misuse and Exploitation

**File:** [specs/001-clothing-fit-assessment/plan.md#L130](specs/001-clothing-fit-assessment/plan.md#L130)

**Offending Code:**

```markdown
<!-- plan.md — Degradation ladder bypasses safety controls autonomously -->
## Degradation Ladder
- L1: Skip Content Safety moderation → process anyway
- L2: Skip Florence-2 → lose minor detection capability
<!-- No human approval gate. Safety-critical controls silently bypassed. -->
```

**Example Fix:**

```markdown
## Degradation Ladder
- L1-quality: Skip non-safety enrichments (style analysis) → auto
- L1-safety: Content Safety unavailable → REJECT request (no bypass)
- L2-quality: Reduce image resolution → auto
- L2-safety: Florence-2 (minor detection) unavailable → REJECT request
  - Requires: ops-team approval to temporarily disable
```

**Steps:**

1. Separate safety-critical controls from quality-degradation controls in the ladder.
2. Add operations team approval gate before any safety bypass activates.
3. Change behavior to REJECT rather than SKIP when minor detection is unavailable.
4. Log all degradation decisions with full context for audit.

**Verification verdict:** CONFIRMED — L1/L2 degradation autonomously bypasses Content Safety and Florence-2.

---

### MEDIUM Severity

#### A03:2025 — Software Supply Chain Failures

**File:** [poc/fit-signal-poc/pyproject.toml#L7](poc/fit-signal-poc/pyproject.toml#L7)

**Offending Code:**

```toml
# pyproject.toml — No Dependabot, SBOM, or CI scanning configured
[project]
dependencies = [
    "streamlit>=1.40",
    "mediapipe>=0.10",
    "opencv-python>=4.10",
]
# uv.lock exists with hashes but no automated scanning
```

**Example Fix:**

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/poc/fit-signal-poc"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
```

**Steps:**

1. Configure Dependabot for the Python PoC ecosystem.
2. Add CI workflow step generating CycloneDX SBOM.
3. Integrate dependency vulnerability scanning in CI (e.g., `pip-audit` or Trivy).

**Verification verdict:** CONFIRMED — No CI/CD, SBOM, or automated dependency scanning configured.

---

#### A08:2025 — Software or Data Integrity Failures

**File:** [poc/fit-signal-poc/src/pose_detection.py#L85](poc/fit-signal-poc/src/pose_detection.py#L85)

**Offending Code:**

```python
# pose_detection.py — Model loaded with existence check only
model_path = Path("models/pose_landmarker.task")
if not model_path.exists():
    raise FileNotFoundError(f"Model not found: {model_path}")
# No hash verification before loading
```

**Example Fix:**

```python
import hashlib

EXPECTED_HASH = "sha256:a1b2c3d4..."  # Pin known-good hash

def verify_model_integrity(model_path: Path) -> None:
    sha256 = hashlib.sha256(model_path.read_bytes()).hexdigest()
    if f"sha256:{sha256}" != EXPECTED_HASH:
        raise IntegrityError(f"Model hash mismatch: {model_path}")

verify_model_integrity(model_path)
```

**Steps:**

1. Compute SHA-256 hash of known-good model files and store in a manifest.
2. Verify hash before loading any model file.
3. Fail loudly if hash does not match — do not proceed with untrusted model.

**Verification verdict:** CONFIRMED — Model loading uses existence check only, no hash verification.

---

#### A10:2025 — Mishandling of Exceptional Conditions

**File:** [poc/fit-signal-poc/app/streamlit_app.py#L968](poc/fit-signal-poc/app/streamlit_app.py#L968)

**Offending Code:**

```python
# streamlit_app.py line 968
try:
    result = process_image(uploaded_file)
except Exception:  # noqa: BLE001
    pass  # Silently discards all errors
```

**Example Fix:**

```python
import logging

logger = logging.getLogger(__name__)

try:
    result = process_image(uploaded_file)
except (ValueError, IOError) as e:
    logger.warning("Image processing failed: %s", e)
    st.error("Unable to process image. Please try a different photo.")
except Exception:
    logger.exception("Unexpected error during image processing")
    st.error("An unexpected error occurred. Please try again.")
```

**Steps:**

1. Replace bare `except Exception` with specific exception types.
2. Log all caught exceptions with context.
3. Provide user-friendly error messages via Streamlit.

**Verification verdict:** CONFIRMED — Bare except with noqa:BLE001 at line 968 silently discards errors.

---

#### LLM03:2025 — Supply Chain (AI Models)

**File:** [poc/fit-signal-poc/app/streamlit_app.py#L59](poc/fit-signal-poc/app/streamlit_app.py#L59)

**Offending Code:**

```python
# streamlit_app.py — MediaPipe model loaded without integrity check
base_options = mp.tasks.BaseOptions(model_asset_path="models/pose_landmarker.task")
```

**Example Fix:**

```python
import hashlib
from pathlib import Path

MODEL_HASHES = {
    "models/pose_landmarker.task": "sha256:abc123...",
}

def load_verified_model(path: str) -> str:
    file_hash = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    expected = MODEL_HASHES.get(path, "").removeprefix("sha256:")
    if file_hash != expected:
        raise RuntimeError(f"Model integrity check failed: {path}")
    return path

base_options = mp.tasks.BaseOptions(
    model_asset_path=load_verified_model("models/pose_landmarker.task")
)
```

**Steps:**

1. Create model hash manifest file with SHA-256 checksums.
2. Verify model integrity before loading.
3. Include model provenance in planned SBOM (T134).

**Verification verdict:** CONFIRMED — Models loaded without any integrity verification.

---

#### LLM09:2025 — Misinformation (Hallucinated Measurements)

**File:** [docs/architecture/threat-model.md#L150](docs/architecture/threat-model.md#L150)

**Offending Code:**

```markdown
<!-- threat-model.md — Mitigations designed but unimplemented -->
| AI-5 | Hallucinated Measurements | ... |
## Mitigations:
- 70% confidence threshold
- Cross-measurement plausibility checks
- AI disclosure label
<!-- None implemented -->
```

**Example Fix:**

```csharp
public FitResult ProcessMeasurements(AiMeasurementOutput output)
{
    if (output.Confidence < 0.70)
        return FitResult.LowConfidence("Measurements below confidence threshold");

    if (!PlausibilityCheck.IsValid(output.Measurements))
        return FitResult.Implausible("Measurements failed anatomical validation");

    return FitResult.Success(output.Measurements, aiGenerated: true);
}
```

**Steps:**

1. Implement 70% confidence threshold with graceful rejection below threshold.
2. Add cross-measurement plausibility validation.
3. Display AI disclosure on all measurement-derived recommendations.

**Verification verdict:** CONFIRMED — No confidence threshold or plausibility check code exists.

---

#### LLM10:2025 — Unbounded Consumption

**File:** [specs/001-clothing-fit-assessment/tasks.md#L96](specs/001-clothing-fit-assessment/tasks.md#L96)

**Offending Code:**

```markdown
<!-- tasks.md — Resource controls designed, none implemented -->
## Resource Controls
- Rate limiting per tenant
- Max upload size (10 MB)
- Request timeout budget (30s)
- Per-tenant token tracking
- Circuit breaker on AI services
- Concurrent request caps
- Queue depth limits
<!-- All unimplemented. D-1 volumetric flood has DREAD 9.0 -->
```

**Example Fix:**

```csharp
// Program.cs — Rate limiting middleware
builder.Services.AddRateLimiter(options =>
{
    options.AddTokenBucketLimiter("per-tenant", limiter =>
    {
        limiter.TokenLimit = 10;
        limiter.ReplenishmentPeriod = TimeSpan.FromSeconds(10);
        limiter.TokensPerPeriod = 2;
    });
});

// Enforce max upload size
builder.Services.Configure<FormOptions>(o => o.MultipartBodyLengthLimit = 10_485_760);
```

**Steps:**

1. Implement per-tenant rate limiting using ASP.NET Core rate limiter.
2. Enforce 10 MB max upload at ingress (Kestrel + reverse proxy).
3. Set 30-second timeout budget for end-to-end request processing.
4. Add per-tenant token consumption tracking for cost visibility.

**Verification verdict:** CONFIRMED — No rate limiting or resource controls exist.

---

#### ISR01:2024 — Outdated Software

**File:** [specs/001-clothing-fit-assessment/plan.md#L7](specs/001-clothing-fit-assessment/plan.md#L7)

**Offending Code:**

```markdown
<!-- plan.md — .NET 8.0 target specified but no project files exist -->
## Technology Stack
- .NET 8.0 LTS
- No csproj, Directory.Packages.props, or NuGet.lock.json
```

**Example Fix:**

```xml
<!-- Directory.Packages.props — Central package management -->
<Project>
  <PropertyGroup>
    <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>
  </PropertyGroup>
  <ItemGroup>
    <PackageVersion Include="Azure.AI.OpenAI" Version="2.1.0" />
  </ItemGroup>
</Project>
```

**Steps:**

1. Use central package management (Directory.Packages.props) when .NET is scaffolded.
2. Enable `RestorePackagesWithLockFile` for deterministic builds.
3. Add `dotnet nuget audit` to CI pipeline.
4. Configure Dependabot for NuGet ecosystem.

**Verification verdict:** CONFIRMED — No .NET project files or dependency scanning configured.

---

#### ISR02:2024 — Insufficient Threat Detection

**File:** [docs/architecture/solution-architecture.md#L494](docs/architecture/solution-architecture.md#L494)

**Offending Code:**

```markdown
<!-- solution-architecture.md — Monitoring planned, not deployed -->
## Observability
- OpenTelemetry SDK → Azure Monitor
- Application Insights
<!-- No SIEM, no Sentinel, no Defender, no runbooks, no alerting -->
```

**Example Fix:**

```bicep
// sentinel.bicep
resource workspace 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: 'log-fitassess'
  location: location
  properties: { retentionInDays: 90 }
}

resource sentinel 'Microsoft.SecurityInsights/onboardingStates@2023-11-01' = {
  name: 'default'
  scope: workspace
}
```

**Steps:**

1. Deploy Log Analytics workspace with Microsoft Sentinel.
2. Enable Defender for App Service, Storage, and Key Vault.
3. Create alert rules for top 5 threat scenarios.
4. Write incident response runbooks.
5. Plan adversary simulation (red team) post-launch.

**Verification verdict:** CONFIRMED — No monitoring infrastructure deployed.

---

#### ISR03:2024 — Insecure Configurations

**File:** [docs/architecture/threat-model.md#L233](docs/architecture/threat-model.md#L233)

**Offending Code:**

```markdown
<!-- threat-model.md — Security headers and private endpoints as gaps -->
## Configuration Gaps
- No security headers (CSP, HSTS, X-Frame-Options)
- Private endpoints recommended, not enforced
- No IaC exists to codify secure configuration
```

**Example Fix:**

```csharp
// Program.cs — Security headers middleware
app.Use(async (context, next) =>
{
    context.Response.Headers["X-Content-Type-Options"] = "nosniff";
    context.Response.Headers["X-Frame-Options"] = "DENY";
    context.Response.Headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains";
    context.Response.Headers["Content-Security-Policy"] = "default-src 'self'";
    await next();
});
```

**Steps:**

1. Add security headers middleware when ASP.NET Core backend is implemented.
2. Create Bicep IaC with private endpoints enforced.
3. Add IaC scanning (e.g., Checkov, PSRule) to CI pipeline.

**Verification verdict:** DOWNGRADED — Blob correctly ZRS. VNet is classified as critical pre-production blocker. Severity reduced from HIGH to MEDIUM.

---

#### ISR08:2024 — Information Leakage

**File:** [docs/architecture/threat-model.md#L105](docs/architecture/threat-model.md#L105)

**Offending Code:**

```markdown
<!-- threat-model.md — Data protection designed but not operational -->
## Data Minimization
- 60s auto-purge for body images
- Opaque session IDs
- PII scrubbing in telemetry
<!-- Defender for Storage, purge compliance, DLP: not implemented -->
```

**Example Fix:**

```bicep
// defender.bicep
resource defenderStorage 'Microsoft.Security/defenderForStorageSettings@2022-12-01-preview' = {
  name: 'current'
  scope: storageAccount
  properties: {
    isEnabled: true
    malwareScanning: { onUpload: { isEnabled: true } }
    sensitiveDataDiscovery: { isEnabled: true }
  }
}
```

**Steps:**

1. Enable Microsoft Defender for Storage with malware scanning and sensitive data discovery.
2. Implement purge compliance monitoring (verify blobs deleted within 60s).
3. Configure DLP policies for biometric-adjacent data.

**Verification verdict:** CONFIRMED — No runtime data protection controls active.

---

#### CICD-SEC-1:2025 — Insufficient Flow Control

**File:** Repository-wide

**Offending Code:**

```text
# No branch protection rules configured
# No CODEOWNERS file
# No required reviewers
# No status checks required for merge
```

**Example Fix:**

```text
# CODEOWNERS
* @security-team
/infra/ @platform-team @security-team
/.github/workflows/ @platform-team @security-team
```

**Steps:**

1. Enable branch protection on `main` requiring at least one approval.
2. Create `CODEOWNERS` file with security-relevant path ownership.
3. Require status checks to pass before merge.

**Verification verdict:** DOWNGRADED — No production code or CI/CD reduces exploitability. Severity reduced from HIGH to MEDIUM.

---

#### CICD-SEC-6:2025 — Insufficient Credential Hygiene

**File:** Repository-wide

**Offending Code:**

```text
# No .github/secret_scanning.yml
# No pre-commit hooks for secret detection
# No push protection enabled
# Positive: No credentials found in committed code
```

**Example Fix:**

```yaml
# .github/secret_scanning.yml (enable via GitHub settings)
# Additionally, pre-commit hook:
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
```

**Steps:**

1. Enable GitHub secret scanning in repository settings.
2. Enable push protection to block commits containing secrets.
3. Add gitleaks pre-commit hook for local detection.

**Verification verdict:** CONFIRMED — No automated secret scanning configured.

---

#### CICD-SEC-9:2025 — Improper Artifact Integrity Validation

**File:** [specs/001-clothing-fit-assessment/tasks.md#L275](specs/001-clothing-fit-assessment/tasks.md#L275)

**Offending Code:**

```markdown
<!-- tasks.md — T134 plans signing but nothing exists -->
T134: Supply Chain Security
- SBOM generation
- Container image signing (Notation)
- Dependency scanning (Trivy)
<!-- No artifacts exist to sign. No CI/CD pipeline. -->
```

**Example Fix:**

```yaml
# .github/workflows/build.yml — Artifact signing
- name: Sign container image
  uses: notation-action/sign@v1
  with:
    plugin: azure-kv
    key-id: ${{ secrets.SIGNING_KEY_ID }}
- name: Generate SBOM
  uses: anchore/sbom-action@v0
```

**Steps:**

1. Implement commit signing (`git config commit.gpgsign true`) before production code.
2. Include SBOM generation and container signing in first CI pipeline (T134).
3. Verify signatures in deployment pipeline.

**Verification verdict:** DOWNGRADED — No production artifacts exist to sign. Risk is pre-emptive. Severity reduced from HIGH to MEDIUM.

---

#### SBD-01 — Security Governance

**File:** [.copilot-tracking/security-plans/fitassess/security-plan.md#L1](.copilot-tracking/security-plans/fitassess/security-plan.md#L1)

**Offending Code:**

```markdown
<!-- security-plan.md — Generic roles without named owners -->
## Roles and Responsibilities
- Security Lead: [TBD]
- Security Champion: [Not assigned]
- Risk Owner: [Generic title]
```

**Example Fix:**

```markdown
## Roles and Responsibilities
| Role | Owner | Backup | Accountability |
|------|-------|--------|----------------|
| Security Risk Owner | Jane Smith (Director) | ... | Final risk acceptance |
| Security Champion | Dev Team Lead | ... | Sprint-level security reviews |
```

**Steps:**

1. Assign named individuals to security governance roles.
2. Define security champion from the development team.
3. Establish maturity scorecard with quarterly reviews.

**Verification verdict:** CONFIRMED — Generic role titles with no named individuals.

---

#### SBD-04 — Supply Chain Security

**File:** [poc/fit-signal-poc/pyproject.toml#L7](poc/fit-signal-poc/pyproject.toml#L7)

**Offending Code:**

```toml
# pyproject.toml — No SBOM, no .NET lock strategy
[project]
dependencies = [...]
# uv.lock provides pinning (positive)
# But: no SBOM generation, no automated scanning, no .NET lock file plan
```

**Example Fix:**

```yaml
# CI step for SBOM generation
- name: Generate Python SBOM
  run: uv export --format cyclonedx > sbom-python.json
- name: Generate .NET SBOM
  run: dotnet sbom-tool generate -b ./backend -bc ./backend
```

**Steps:**

1. Generate CycloneDX SBOM for Python dependencies.
2. Plan `RestorePackagesWithLockFile` for .NET when scaffolded.
3. Configure Dependabot for both ecosystems.

**Verification verdict:** DOWNGRADED — uv.lock provides full pinning with SHA-256 hashes. Better than originally assessed.

---

#### SBD-08 — Minimize Attack Surface

**File:** [.copilot-tracking/security-plans/fitassess/security-plan.md#L475](.copilot-tracking/security-plans/fitassess/security-plan.md#L475)

**Offending Code:**

```markdown
<!-- security-plan.md — Attack surface gaps identified but unresolved -->
## Attack Surface Gaps
- Swagger UI exposed in all environments
- CORS not defined
- Debug endpoints not gated
- Private endpoints not deployed
```

**Example Fix:**

```csharp
// Program.cs — Environment-gated Swagger
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

// CORS policy
builder.Services.AddCors(options =>
{
    options.AddPolicy("Production", policy =>
        policy.WithOrigins("https://app.contoso.com")
              .AllowCredentials());
});
```

**Steps:**

1. Gate Swagger/OpenAPI UI to Development environment only.
2. Define explicit CORS policy with allowed origins.
3. Remove or gate debug/diagnostic endpoints behind authorization.
4. Deploy private endpoints for all backend services.

**Verification verdict:** CONFIRMED — Gaps identified in security plan but not resolved.

---

#### ASI06:2026 — Memory and Context Poisoning

**File:** [specs/001-clothing-fit-assessment/plan.md#L137](specs/001-clothing-fit-assessment/plan.md#L137)

**Offending Code:**

```markdown
<!-- plan.md — Profile storage without integrity checks -->
## Profile Management
- Measurements saved to user profile
- L3 fallback uses saved measurements
- 70% confidence threshold (not implemented)
<!-- No drift detection, no trust scoring, no degradation-aware storage -->
```

**Example Fix:**

```csharp
public async Task StoreMeasurementsAsync(string userId, Measurements m, PipelineContext ctx)
{
    if (ctx.DegradationLevel > DegradationLevel.None)
        throw new PolicyViolationException("Cannot store during degraded mode");

    if (!PhysiologicalValidator.IsConsistentWithHistory(userId, m))
        throw new DriftDetectedException("Measurements inconsistent with profile history");

    m.Lineage = new MeasurementLineage(ctx.PipelineVersion, ctx.ModelVersions, ctx.Confidence);
    await _profileStore.UpsertAsync(userId, m);
}
```

**Steps:**

1. Add physiological validation before writing measurements to profile.
2. Implement consistency checks against historical profile data.
3. Add drift detection alerting for anomalous measurement changes.
4. Block profile storage when pipeline is operating in degraded mode.

**Verification verdict:** CONFIRMED — No integrity checks on profile storage path.

---

#### ASI08:2026 — Cascading Failures

**File:** [docs/architecture/resiliency-review.md#L63](docs/architecture/resiliency-review.md#L63)

**Offending Code:**

```markdown
<!-- resiliency-review.md — Cascade path identified -->
## Cascade Risk
L2 degradation → bad images → incorrect measurements → stored in profile → L3 reuse
- Profile storage unaware of degradation state
- No lineage metadata attached to measurements
- Circuit breakers designed but not implemented
```

**Example Fix:**

```csharp
public class MeasurementLineage
{
    public required string PipelineVersion { get; init; }
    public required DegradationLevel DegradationLevel { get; init; }
    public required double Confidence { get; init; }
    public required DateTimeOffset Timestamp { get; init; }
}

// Policy gate: reject storage if sourced from degraded pipeline
if (lineage.DegradationLevel >= DegradationLevel.L2)
    return Result.Rejected("Measurements from degraded pipeline cannot be stored");
```

**Steps:**

1. Add lineage metadata (pipeline version, degradation level, confidence) to all measurements.
2. Implement policy gate rejecting profile storage from degraded pipeline runs.
3. Implement Polly resilience policies (circuit breaker, retry, timeout) as P0.
4. Add integration test verifying cascade path is blocked.

**Verification verdict:** CONFIRMED — No degradation awareness in profile storage.

---

### LOW Severity

#### A02:2025 — Security Misconfiguration

**File:** [poc/fit-signal-poc/pyproject.toml#L7](poc/fit-signal-poc/pyproject.toml#L7)

**Offending Code:**

```toml
# pyproject.toml — Open version ranges
[project]
dependencies = [
    "streamlit>=1.40",  # No upper bound
    "mediapipe>=0.10",
]
```

**Example Fix:**

```toml
[project]
dependencies = [
    "streamlit>=1.40,<2.0",
    "mediapipe>=0.10,<1.0",
]
```

**Steps:**

1. Add upper-bound version constraints on critical dependencies.
2. Address security headers when production ASP.NET Core API is implemented.

**Verification verdict:** DOWNGRADED — uv.lock with SHA-256 hashes substantially mitigates risk. Severity reduced from MEDIUM to LOW.

---

#### ISR04:2024 — Insecure Resource and User Management

**File:** [docs/architecture/threat-model.md#L89](docs/architecture/threat-model.md#L89)

**Offending Code:**

```markdown
<!-- threat-model.md — PAM/PIM gap -->
## Identity Gaps
- PIM: Not configured
- Tenant off-boarding: No documented procedure
```

**Example Fix:**

```markdown
## Privileged Access Management
- Azure AD PIM enabled for all admin roles
- Maximum activation: 8 hours
- Require justification and MFA for activation
- Quarterly access review scheduled
```

**Steps:**

1. Implement Azure AD PIM for privileged roles.
2. Document tenant off-boarding procedure.
3. Enforce MFA via Conditional Access policies.

**Verification verdict:** DOWNGRADED — MFA and access reviews are planned. Core managed identity foundation is sound.

---

#### ISR09:2024 — Insecure Access to Resources

**File:** [docs/architecture/threat-model.md#L219](docs/architecture/threat-model.md#L219)

**Offending Code:**

```markdown
<!-- threat-model.md — PIM and alerting gaps -->
## Access Gaps
- PIM not configured for admin roles
- No Activity Log alerts for privileged operations
```

**Example Fix:**

```bicep
// alerts.bicep
resource activityLogAlert 'Microsoft.Insights/activityLogAlerts@2020-10-01' = {
  name: 'alert-privileged-ops'
  properties: {
    condition: {
      allOf: [
        { field: 'category', equals: 'Administrative' }
        { field: 'operationName', equals: 'Microsoft.Authorization/roleAssignments/write' }
      ]
    }
  }
}
```

**Steps:**

1. Implement PIM for admin roles.
2. Configure Activity Log alerts for privileged operations.

**Verification verdict:** DOWNGRADED — PaaS-only architecture makes bastion irrelevant. Core access is sound.

---

#### CICD-SEC-3:2025 — Dependency Chain Abuse

**File:** [poc/fit-signal-poc/pyproject.toml](poc/fit-signal-poc/pyproject.toml)

**Offending Code:**

```toml
# pyproject.toml — Well-protected by uv.lock
[project]
dependencies = [...]
# uv.lock with SHA-256 hashes provides strong integrity
# .NET concerns are hypothetical — no project files exist
```

**Example Fix:**

```xml
<!-- When .NET scaffolded: enable lock file -->
<PropertyGroup>
  <RestorePackagesWithLockFile>true</RestorePackagesWithLockFile>
</PropertyGroup>
```

**Steps:**

1. Enable `RestorePackagesWithLockFile` when .NET backend is scaffolded.
2. Add `dependabot.yml` covering both Python and NuGet ecosystems.

**Verification verdict:** DOWNGRADED — uv.lock with SHA-256 hashes provides strong protection for Python.

---

#### CICD-SEC-10:2025 — Insufficient Logging and Visibility

**File:** Repository-wide

**Offending Code:**

```text
# No CI/CD system exists — nothing to log
# GitHub provides built-in organization audit logging
# Risk becomes relevant when CI/CD is implemented
```

**Example Fix:**

```yaml
# Future CI pipeline should include from day one:
- name: Upload workflow logs
  uses: actions/upload-artifact@v4
  with:
    name: pipeline-audit-log
    path: audit.log
```

**Steps:**

1. Include audit logging requirements in T134 CI pipeline planning from day one.
2. Forward GitHub Actions logs to centralized SIEM when deployed.

**Verification verdict:** DOWNGRADED — No CI/CD system exists to log. Risk is future-state.

---

#### ASI04:2026 — Agentic Supply Chain

**File:** [specs/001-clothing-fit-assessment/tasks.md#L268](specs/001-clothing-fit-assessment/tasks.md#L268)

**Offending Code:**

```markdown
<!-- tasks.md — T134 planned but not scheduled -->
T134: Supply Chain Security
- SBOM/Trivy/Notation
<!-- AI models are Azure-managed PaaS. Garment data provenance is a gap. -->
```

**Example Fix:**

```markdown
T134: Supply Chain Security [Sprint 2, P1]
- SBOM generation (CycloneDX)
- Container signing (Notation + Azure Key Vault)
- Prompt content-hash verification at startup
- HMAC verification for garment catalog uploads
```

**Steps:**

1. Schedule T134 early in implementation (Sprint 2).
2. Add prompt content-hash verification at application startup.
3. Consider HMAC verification for garment catalog uploads.

**Verification verdict:** DOWNGRADED — Azure-managed models shift runtime integrity to Microsoft.

---

### Disproved Findings

- **A05:2025 — Injection:** All `unsafe_allow_html` calls in Streamlit render application-controlled content only. No user-supplied text reaches HTML rendering. The only user input (height) is a typed float validated by Streamlit's `number_input` widget. Finding disproved — no injection vector exists.

---

## Remediation Checklist

| ID | Control | Status | Evidence |
|----|---------|--------|----------|
| A09:2025 | Security Logging and Alerting | NOT_STARTED | |
| A03:2025 | Supply Chain — Dependabot and SBOM | NOT_STARTED | |
| A08:2025 | Model File Integrity Verification | NOT_STARTED | |
| A10:2025 | Exception Handling | NOT_STARTED | |
| A02:2025 | Dependency Version Constraints | NOT_STARTED | |
| LLM01:2025 | EXIF Stripping and Range Validation | NOT_STARTED | |
| LLM02:2025 | Blob Lifecycle Purge and PII Scrubbing | NOT_STARTED | |
| LLM05:2025 | Output Schema Validation | NOT_STARTED | |
| LLM03:2025 | AI Model Integrity Checksums | NOT_STARTED | |
| LLM09:2025 | Confidence Threshold and Plausibility | NOT_STARTED | |
| LLM10:2025 | Rate Limiting and Resource Controls | NOT_STARTED | |
| ISR06:2024 | VNet and Private Endpoints | NOT_STARTED | |
| ISR01:2024 | NuGet Package Pinning and Scanning | NOT_STARTED | |
| ISR02:2024 | SIEM and Threat Detection | NOT_STARTED | |
| ISR03:2024 | Security Headers and IaC | NOT_STARTED | |
| ISR08:2024 | Defender for Storage and DLP | NOT_STARTED | |
| ISR04:2024 | PIM and MFA Enforcement | NOT_STARTED | |
| ISR09:2024 | PIM and Activity Log Alerts | NOT_STARTED | |
| CICD-SEC-1:2025 | Branch Protection and CODEOWNERS | NOT_STARTED | |
| CICD-SEC-6:2025 | Secret Scanning and Push Protection | NOT_STARTED | |
| CICD-SEC-9:2025 | Artifact Signing and SBOM | NOT_STARTED | |
| CICD-SEC-3:2025 | .NET Lock File Strategy | NOT_STARTED | |
| CICD-SEC-10:2025 | CI/CD Audit Logging | NOT_STARTED | |
| SBD-03 | CI/CD with SAST/SCA | NOT_STARTED | |
| SBD-06 | Incident Response Plan and Runbooks | NOT_STARTED | |
| SBD-10 | Continuous Assurance Mechanisms | NOT_STARTED | |
| SBD-01 | Named Security Governance Owners | NOT_STARTED | |
| SBD-04 | SBOM Generation | NOT_STARTED | |
| SBD-08 | Attack Surface Reduction | NOT_STARTED | |
| ASI01:2026 | EXIF Stripping Implementation Task | NOT_STARTED | |
| ASI02:2026 | Degradation Safety Gate | NOT_STARTED | |
| ASI06:2026 | Profile Storage Integrity Checks | NOT_STARTED | |
| ASI08:2026 | Cascade Prevention and Lineage | NOT_STARTED | |
| ASI04:2026 | T134 Supply Chain Early Scheduling | NOT_STARTED | |

---

## Appendix: Skills Used

| Skill | Framework | Version | Reference |
|-------|-----------|---------|-----------|
| owasp-top-10 | OWASP Top 10 for Web Applications | 2025 | OWASP Top 10:2025 |
| owasp-llm | OWASP Top 10 for LLM Applications | 2025 | OWASP LLM Top 10:2025 |
| owasp-infrastructure | OWASP Infrastructure Security Top 10 | 2024 | OWASP Infrastructure:2024 |
| owasp-cicd | OWASP Top 10 CI/CD Security Risks | 2025 | OWASP CI/CD:2025 |
| secure-by-design | Secure by Design Principles | 2024 | CISA Secure by Design |
| owasp-agentic | OWASP Top 10 for Agentic Applications | 2026 | OWASP Agentic:2026 |

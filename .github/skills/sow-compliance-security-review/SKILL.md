---
name: sow-compliance-security-review
description: Perform a compliance and security review of a Statement of Work (SOW) document for AI / cloud / data-handling engagements. Produces a structured Markdown review covering compliance framework coverage (OWASP ASVS, SOC 2, NIST CSF, GDPR/CCPA, PCI, biometric privacy, EU AI Act), data protection, security architecture, AI/ML risk, resilience and incident response, testing and assurance, and contractual/legal completeness, then emits a categorized list of MUST-FIX / SHOULD-FIX / NICE-TO-HAVE changes. USE WHEN the user asks to review, audit, assess, or compliance-check an SOW, MSA addendum, or similar engagement contract; especially when the workload involves AI, biometric/PII data, or regulated industries. DO NOT USE FOR general code review, threat modelling from scratch (use a threat-modelling skill), or DPIA authoring (this skill only identifies DPIA gaps).
---

# SOW Compliance & Security Review

This skill produces a rigorous, evidence-based compliance & security review of a
Statement of Work (SOW) for engagements that touch AI/ML, biometric or
PII-adjacent data, payments, or other regulated workloads. The output is a
single Markdown file modeled on
[`docs/sow-review/compliance-and-security-review.md`](../../../docs/sow-review/compliance-and-security-review.md),
which is the canonical reference example for tone, structure, and depth.

## When to use

Trigger this skill when the user asks to:

- Review / audit / assess an SOW, MSA addendum, or similar engagement document.
- Compliance-check a contract against GDPR, CCPA, PCI, SOC 2, NIST CSF, OWASP
  ASVS, EU AI Act, BIPA / state biometric privacy laws, or HIPAA-adjacency.
- Validate that an SOW correctly inherits the security posture asserted by
  upstream artefacts (threat model, risk register, product definition).
- Produce a pre-signature go / no-go assessment with MUST-FIX gaps.

Do **not** use this skill for: general code review; authoring a threat model
from scratch; producing a full DPIA; legal advice. This skill flags gaps and
proposes contractual language; it is not a substitute for counsel.

## Inputs you need

Before producing the review, confirm or discover:

1. **The SOW under review** — file path, version, status (draft / final / signed).
2. **Cross-reference artefacts** that the SOW should be consistent with, e.g.:
   - Threat model (STRIDE / LINDDUN)
   - Risk register
   - Product / problem definition
   - Spec / data model / OpenAPI contract
   - Any existing assessments
3. **Engagement context**: industry (retail, health, fin-svc, public sector),
   data classes processed (PII, biometric, PHI, CHD, children's data),
   geographies (US-only, EU, UK, APAC), and any client-stated compliance scope.
4. **Reviewer identity** and review date (used in the document header).

If any of these are unknown, ask the user **once** with a concise list — do not
fabricate values for the document header.

## Procedure

Follow these steps in order. Do not skip steps; each one feeds the next.

### Step 1 — Read the SOW end-to-end

Read the entire SOW before writing anything. Specifically capture:

- Scope / out-of-scope statements
- Deliverables (with IDs, e.g. D-1, D-2…)
- Assumptions (A-1, A-2…)
- Constraints (C-1, C-2…)
- Risks (PR-* or R-*) and scope traps (ST-*)
- Acceptance criteria, SLOs/SLAs, hypercare terms
- Compliance posture statements (e.g. "PCI-adjacent, SOC 2-aligned…")
- Termination / exit / data-handling clauses

### Step 2 — Read every cross-reference artefact

Read each linked artefact (threat model, risk register, product definition,
spec, data model). For each, extract:

- Data classifications (especially anything "biometric", "sensitive",
  "PII", "PHI", "CHD")
- Stated mitigations that should appear in the SOW as deliverables or
  acceptance criteria
- Retention SLAs, deletion SLAs, immutability requirements
- Identified threats and their severity

Build a private map of `artefact-claim → SOW-claim` to find drift.

### Step 3 — Map the SOW to compliance frameworks

For each of the following frameworks, classify coverage as
**Claimed + adequate / Claimed but inadequate / Not addressed**:

- OWASP ASVS L2 (require a self-assessment / gap report artefact)
- PCI DSS (adjacent vs. in-scope — be explicit)
- SOC 2 TSC (which trust services criteria are referenced)
- NIST CSF 2.0 (Govern / Identify / Protect / Detect / Respond / Recover)
- GDPR / UK GDPR / CCPA / CPRA (controller vs. processor, Art. 28
  sub-processor list, Art. 33 breach notice SLA, DSAR support)
- EU AI Act (risk tier; Annex III applicability)
- State biometric privacy: Illinois BIPA, Texas CUBI, Washington MHMD /
  HB 1155 — flag explicitly if the workload uses photos, faces, voiceprints,
  body measurements, or other biometric identifiers
- ISO/IEC 27001 / 27701 (optional alignment)
- NIST AI RMF 1.0 (Govern / Map / Measure / Manage)
- WCAG 2.2 AA (if any UX surface, even indirectly)
- HIPAA / FedRAMP (confirm explicitly excluded or in-scope)

Record any framework that is **claimed** but lacks a delivered artefact as a
MUST-FIX gap.

### Step 4 — Apply the canonical gap checklist

Walk through the gap categories below and produce findings. Each category
maps to a top-level section in the output document.

1. **Executive summary** — verdict (Pass / Conditional Pass / Fail), strengths,
   top 5–10 material gaps.
2. **Compliance framework mapping** — table from Step 3.
3. **Data protection & privacy**:
   - Data classification consistency with upstream artefacts
   - Retention, deletion, right-to-be-forgotten — every data class must have a
     stated retention SLA in the SOW
   - DSAR support paths (read / export / delete) — clarify controller vs.
     processor responsibility
   - Cross-border data transfers (SCCs, UK IDTA, adequacy)
   - **Sub-processor enumeration** — name every AI service, content
     moderation, abuse-monitoring reviewer, hosting platform
4. **Security architecture & controls**:
   - Identity & access (token lifetime, conditional access, tenant isolation)
   - Network (private endpoints, WAF tier, DDoS Standard)
   - Cryptography (TLS version, at-rest keys, key rotation, CMK stance)
   - Logging & audit (immutability, hash-chain, PII scrubbing)
   - Supply chain (SAST, SCA, SBOM, signed images, pinned digests, secret
     scanning, dependency review, branch protection)
   - Container runtime hardening (`runAsNonRoot`, read-only FS, dropped caps)
   - Secrets & configuration (Key Vault references, no literal secrets)
5. **AI/ML-specific risk**:
   - Hallucination liability and advisory-disclaimer obligations
   - Bias & fairness reporting (per-demographic accuracy stratification)
   - Prompt injection / adversarial input controls
   - Model drift detection and ground-truth benchmarking
   - AI sub-processor data-use commitments (e.g. abuse-monitoring opt-out,
     no-training warranty as a contractual commitment, not just an
     assumption)
   - EU AI Act risk-tier memo (forward-looking)
6. **Resilience, availability & incident response**:
   - SLO vs. SLA (with credits?) clarity
   - Composite SLO calculation including sub-processor SLAs
   - DR / BCDR (RTO, RPO, multi-region posture)
   - **Security incident response & breach notification** — Sec-Sev matrix,
     72-hour notification SLA (GDPR Art. 33), forensic preservation,
     right-of-audit (GDPR Art. 28(3)(h)), joint IR playbook
   - Reconcile hypercare best-effort wording with P1 defect SLAs
7. **Testing & assurance**:
   - Pen-test ownership, scope, timing, remediation capacity, re-test
   - ASVS L2 self-assessment artefact
   - Compliance evidence package for the customer's auditor
   - Threat model refresh checkpoint
   - Coverage gates — define "critical paths" enumeratively (auth middleware,
     tenant isolation guard, deletion cascade, audit-log integrity, content
     safety refusal, retention/purge logic)
   - Soak / chaos / tenant-isolation chaos tests
8. **Contractual & legal**:
   - Controller / processor allocation under GDPR/CCPA + DPA reference
   - AI-specific carve-outs (hallucination liability, Customer Copyright
     Commitment, training-data warranties)
   - **Data return and destruction on exit** — what happens to profiles,
     audit logs, model artefacts; certificate of destruction
   - Insurance / cyber liability minimums (defer to MSA but flag BIPA
     statutory damages)
9. **Scope, estimation, and risk hygiene**:
   - Scope-trap completeness — add traps for biometric law drift, AI Act
     reclassification, mandatory third-party assessments
   - Risk register coverage of plan-level (not just product-level) risks
10. **Recommended changes before signature** — the three-bucket finding list:
    - **MUST-FIX** (block signature)
    - **SHOULD-FIX** (negotiate but don't block)
    - **NICE-TO-HAVE** (post-signature)

### Step 5 — Write the review document

Write the review to `docs/sow-review/<short-name>-review.md` (create the
folder if it does not exist). Use the structure of the reference example at
[`docs/sow-review/compliance-and-security-review.md`](../../../docs/sow-review/compliance-and-security-review.md).

The first table at the top of the document MUST capture:

| Field                     | Value                                           |
| ------------------------- | ----------------------------------------------- |
| **Document under review** | Relative link + version + status                |
| **Review scope**          | Frameworks and themes assessed                  |
| **Reviewer**              | Reviewer name or team                           |
| **Review date**           | ISO date                                        |
| **Verdict**               | Pass / Conditional Pass / Fail with one-line rationale |
| **Cross-references**      | Relative links to threat model, risk register, etc. |

### Step 6 — Produce a numbered MUST-FIX table

The MUST-FIX table is the most important output. Each row must include:

- A short, imperative change description
- The exact SOW section / deliverable / assumption ID to amend (or "new")

Aim for 10–20 MUST-FIX items for a typical AI/biometric SOW. Fewer means you
probably missed something; many more means you are conflating MUST-FIX with
SHOULD-FIX.

### Step 7 — Self-check before returning

Before declaring the review complete, verify:

- [ ] Every framework in Step 3 has a row in the framework table
- [ ] Every data class identified in Step 2 has a stated retention SLA
- [ ] Sub-processors are enumerated (do not say "implicit")
- [ ] Breach-notification SLA is explicit (e.g. 72 h)
- [ ] Pen-test ownership, remediation capacity, and re-test are addressed
- [ ] Controller / processor allocation is stated
- [ ] Data return / destruction on exit is addressed
- [ ] Hypercare wording is reconciled with P1 SLAs
- [ ] AI hallucination / advisory disclaimer obligation is addressed if AI
  produces recommendations to end users
- [ ] Biometric privacy is addressed if any biometric-adjacent data is
  processed
- [ ] Cross-border processing is addressed if non-US users may be onboarded
- [ ] "Critical paths" for coverage gates are enumerated, not abstract

If any box is unchecked, fix the review before returning.

## Style & tone

- Write in clear, neutral, contract-review English. Avoid hedging like
  "perhaps" — use "MUST-FIX" / "SHOULD-FIX" / "NICE-TO-HAVE".
- Cite specific section numbers, deliverable IDs, assumption IDs, and risk
  IDs from the SOW (e.g. "§3.2", "D-7", "A-11").
- Prefer tables over prose when comparing claims to gaps.
- Never invent regulatory citations. If unsure of an article number, write
  "GDPR (article TBD)" and flag for legal review.
- Do not generate fictitious approver names. Leave reviewer rows as `_TBD_`
  unless the user supplied real names.
- Keep the document self-contained — anyone reading only the review should
  understand the verdict without opening the SOW.

## Anti-patterns to avoid

- **Don't accept "claimed" as "covered".** If ASVS L2 is named but no artefact
  is committed, it is a MUST-FIX.
- **Don't conflate SLO and SLA.** SLOs are operational targets; SLAs carry
  remedies (credits). Flag the difference.
- **Don't let upstream assumptions remain as assumptions** if they are
  load-bearing for compliance (e.g. "no training on customer data" must be a
  binding commitment, not an assumption).
- **Don't let pen-test live in Sprint 9 with no buffer.** Move to Sprint 8
  with re-test in Sprint 9 if findings remediation has no capacity.
- **Don't drop deletion cascade to audit logs** without documenting the
  legal basis (GDPR Art. 17 vs. SOX-adjacent retention).
- **Don't propose HIPAA / FedRAMP / EU AI Act scope additions silently.**
  These are change-order triggers and must be flagged as such.

## Example reference

The canonical example output of this skill is:
[`docs/sow-review/compliance-and-security-review.md`](../../../docs/sow-review/compliance-and-security-review.md).
Mirror its section ordering, table styles, and the three-bucket
(MUST-FIX / SHOULD-FIX / NICE-TO-HAVE) recommendation structure.

## Output

A single Markdown file at `docs/sow-review/<short-name>-review.md`
with the following top-level sections, in order:

1. Header table (document under review, scope, reviewer, date, verdict,
   cross-references)
2. Executive summary
3. Compliance framework mapping
4. Data protection & privacy
5. Security architecture & controls
6. AI/ML-specific risks (omit if not an AI workload)
7. Resilience, availability & incident response
8. Testing & assurance
9. Contractual & legal
10. Scope, estimation, and risk hygiene
11. Recommended changes before signature (MUST-FIX / SHOULD-FIX / NICE-TO-HAVE)
12. Approval table (leave as `_TBD_` unless the user supplied names)
13. Version history

---
name: sow-full-review
description: "Run a comprehensive SOW review by producing SOW-specific compliance/security, Azure technical architecture, and Agile SOW template-alignment review files, then synthesize them into an SOW-specific executive full review package. USE WHEN the user asks for a full review, comprehensive review, all reviews, compliance plus technical plus template review, or one-pass SOW review. When independent review tracks can run in parallel, run them in parallel and synthesize after all are complete. Creates or updates docs/sow-review/<sow-slug>-<version>/compliance-and-security-review.md, docs/sow-review/<sow-slug>-<version>/technical-review.md, docs/sow-review/<sow-slug>-<version>/template-review.md, and docs/sow-review/<sow-slug>-<version>/full-review.md. DO NOT USE FOR a narrow compliance-only review (use sow-compliance-security-review), technical-only Azure review (use sow-technical-review), or template-only review (use sow-template-review)."
---

# SOW Full Review

This skill orchestrates a comprehensive Statement of Work (SOW) review by
running three review tracks and then synthesizing the results into a single
executive package:

1. **Compliance & Security Review** — use the workflow in
   [`sow-compliance-security-review`](../sow-compliance-security-review/SKILL.md).
2. **Azure Technical Review** — use the workflow in
   [`sow-technical-review`](../sow-technical-review/SKILL.md).
3. **Agile SOW Template Review** — use the workflow in
   [`sow-template-review`](../sow-template-review/SKILL.md).
4. **Full Review Synthesis** — write the SOW-specific full review output file.

The full review is not a replacement for the three detailed reviews. It is the
one-file package that a steering committee, legal reviewer, or executive sponsor
can read first to understand the combined go / no-go posture.

## When to use

Trigger this skill when the user asks to:

- Run compliance/security, technical/Azure, and Agile template reviews for an SOW.
- Produce a full, comprehensive, end-to-end, or one-pass SOW review.
- Generate `full-review.md` from the SOW-specific `compliance-and-security-review.md`,
  `technical-review.md`, and `template-review.md` files.
- Compare compliance blockers, technical blockers, and template-alignment blockers before SOW signature.
- Create a single executive recommendation from multiple review tracks.

Do **not** use this skill for a narrow review. Use:

- `sow-compliance-security-review` for compliance / privacy / legal / security
  posture only.
- `sow-technical-review` for Azure architecture / service correctness only.
- `sow-template-review` for Agile SOW template alignment only.

## Inputs you need

Before producing the full review, confirm or discover:

1. **The SOW under review** — file path, version, status.
2. **Review artefacts**:
  - The SOW-specific compliance review, if it already exists.
  - The SOW-specific technical review, if it already exists.
  - The SOW-specific template review, if it already exists.

3. **Cross-reference artefacts** used by both tracks:
   - Threat model
   - Risk register
   - Product definition / problem statement
   - Solution architecture
   - Diagrams
   - Cost estimate
   - Resiliency review
   - Data model / OpenAPI contract
4. **Reviewer identity** and review date.

If any detailed review is missing or stale, produce or refresh it using the
corresponding skill workflow before writing the full review synthesis.

## Output naming policy

Place review outputs in an SOW-specific folder so multiple SOWs or versions can
coexist in `docs/sow-review/` without overwriting each other and the reviewed
SOW is clear from the path.

1. Derive `<sow-slug>` from the SOW filename without extension:
  - Lowercase.
  - Replace spaces and underscores with hyphens.
  - Remove characters other than `a-z`, `0-9`, and `-`.
  - Collapse repeated hyphens.

2. Derive `<version>` from the SOW header field named `Version`.
  - Preserve the leading `v` if present; otherwise prefix `v`.
  - Normalize dots as dots, e.g. `0.1.0` -> `v0.1.0`.
  - If no version is present, use the SOW document date as `yyyy-mm-dd`.

3. Write outputs under:

- `docs/sow-review/<sow-slug>-<version>/`

The files inside that folder are:

- `compliance-and-security-review.md`
- `technical-review.md`
- `template-review.md`
- `full-review.md`

If the same SOW name and version are reviewed again, update / overwrite the
same files in that folder. Do not create timestamped duplicates unless the user
explicitly asks for archival snapshots.

## Procedure

Follow these steps in order.

### Step 1 — Locate or produce all detailed reviews

Check `docs/sow-review/<sow-slug>-<version>/` for the SOW-specific output files
from the naming policy:

- `compliance-and-security-review.md`
- `technical-review.md`
- `template-review.md`

If a file is missing, generate it with the relevant skill workflow. If it exists
but the SOW version, review date, or reviewed document path is stale, refresh it
before synthesis.

The Azure technical review must be **Microsoft Learn MCP-backed** whenever MCP
tools are available. If `technical-review.md` does not show Microsoft Learn MCP
evidence, refresh it with `sow-technical-review` before synthesizing the full
review.

When more than one detailed review is missing or stale, and the execution
environment supports parallel tool or subagent calls, run the independent review
tracks in parallel:

- Start compliance/security, technical/Azure, and template-alignment review
  work concurrently after the SOW and shared cross-reference artefacts are read.
- Keep each track independent; do not let one track rewrite another track's
  findings.
- Wait for all detailed reviews to complete before starting synthesis.
- Do not parallelize the final synthesis step, because it depends on all source
  review outputs.

### Step 2 — Extract normalized findings

From the compliance/security review, extract:

- Verdict
- Top material gaps
- MUST-FIX items
- SHOULD-FIX items
- NICE-TO-HAVE items
- Any approval blockers

From the technical review, extract:

- Verdict
- Critical findings
- High findings
- Medium / Low findings
- Pre-signature action plan
- Microsoft Learn MCP evidence, including queries and source pages used

From the template review, extract:

- Verdict
- Critical / High template-alignment blockers
- MUST-FIX / SHOULD-FIX / NICE-TO-HAVE items
- Fixed-capacity / variable-scope issues
- Acceptance-model, defect-remediation, capacity, Work Order, technology,
  environment, customer-responsibility, and AI Usage assumption gaps

Normalize the three severity systems into the full-review buckets:

| Full-review bucket | Source mapping                                                                                   |
| ------------------ | ------------------------------------------------------------------------------------------------ |
| **Blockers**       | Compliance MUST-FIX + Technical Critical + Technical High + Template Critical + Template High    |
| **Pre-signature**  | Compliance SHOULD-FIX + Technical Medium + Template Medium                                       |
| **Post-signature** | Compliance NICE-TO-HAVE + Technical Low + Technical Informational + Template Low / Informational |

Do not silently drop duplicate issues. Merge duplicates and cite both source
reviews.

### Step 3 — Identify cross-track dependencies

Look for issues that appear in both reviews or affect both tracks, for example:

- AI model naming / access issues that affect compliance sub-processor language.
- Private networking gaps that affect both technical architecture and biometric
  privacy posture.
- SLO / SLA ambiguity that affects both reliability commitments and contractual
  obligations.
- Pen-test rules that affect both security assurance and Azure Rules of
  Engagement.
- Data residency / Foundry deployment type that affects both architecture and
  GDPR / cross-border transfer analysis.
- Formal acceptance language, defect remediation, or hypercare language that
  affects both compliance commitments and Agile fixed-capacity template posture.
- AI Usage assumptions that affect both template compliance and AI/privacy
  contractual posture.

Promote cross-track blockers to the executive summary even if each detailed
review treated the item differently.

### Step 4 — Produce the synthesis document

Write `docs/sow-review/<sow-slug>-<version>/full-review.md` unless the user asks
for a different filename. Create the folder if it does not exist. If the same
SOW name and version are reviewed again, update the existing file in that folder.

The first table at the top of the document MUST capture:

| Field                     | Value                                                                                                                 |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **Document under review** | Relative link + version + status                                                                                      |
| **Review package**        | Links to compliance, technical, and template reviews                                                                  |
| **Review scope**          | Combined compliance, security, legal, technical, Azure architecture, AI, resilience, and Agile SOW template alignment |
| **Reviewer**              | Reviewer name or team                                                                                                 |
| **Review date**           | ISO date                                                                                                              |
| **Overall verdict**       | Pass / Conditional Pass / Fail with one-line rationale                                                                |

### Step 5 — Required full-review sections

Use these top-level sections, in order:

1. **Executive Decision Summary**
   - Overall verdict
   - Whether the SOW can be signed now
   - Required condition to move from Conditional Pass / Fail to Pass
   - Top 5 combined blockers
2. **Review Package Inventory**
   - Links to detailed reviews
   - Version / date / reviewer of each review
   - Reviewed SOW version
3. **Combined Severity Rollup**
   - Counts by bucket and source review
4. **Cross-Track Blockers**
  - Issues that appear in or depend on more than one review track

5. **Blockers Before Signature**
   - Combined MUST-FIX / Critical / High items
   - Each row must include source review, source finding ID or section, SOW
     section to amend, and owner
6. **Pre-Signature Improvements**
   - SHOULD-FIX / Medium items
7. **Post-Signature Backlog**
   - NICE-TO-HAVE / Low / Informational items
8. **Recommended Remediation Sequence**
   - A practical sequence that avoids rework, e.g. service/model naming before
     sub-processor list, private networking before DPIA finalization.
9. **Go / No-Go Recommendation**
   - `Go`, `Conditional Go`, or `No-Go`
   - Clear rationale and minimum sign-off conditions
10. **Approval Table**
11. **Version History**

### Step 6 — Self-check before returning

Before declaring the full review complete, verify:

- [ ] All detailed reviews exist and are linked.
- [ ] The full review uses the same SOW version as the detailed reviews.
- [ ] Every compliance MUST-FIX appears in the Blockers section or is explicitly
      marked as merged into another blocker.
- [ ] Every technical Critical and High finding appears in the Blockers section
      or is explicitly merged.
- [ ] The technical review is Microsoft Learn MCP-backed, or the full review
  explicitly states that MCP was unavailable and fallback evidence was used.
- [ ] Every template Critical and High finding appears in the Blockers section
      or is explicitly merged.
- [ ] Cross-track dependencies are called out.
- [ ] The Go / No-Go recommendation is unambiguous.
- [ ] The remediation sequence is practical and not just a severity-sorted list.
- [ ] No reviewer or approver name is fabricated.

If any box is unchecked, fix the full review before returning.

## Style & tone

- Write in clear executive-review English.
- Keep the full review concise enough to be read first, but specific enough to
  drive action.
- Link to the detailed reviews for evidence; do not copy every long finding.
- Use tables for rollups and decision records.
- Preserve the severity terminology from the source reviews when referencing
  a source finding.

## Anti-patterns to avoid

- **Do not create a superficial summary.** The full review must synthesize and
  prioritize, not just list links.
- **Do not drop blockers because they are duplicated.** Merge duplicates and
  cite both sources.
- **Do not let technical findings and compliance findings contradict each
  other.** If they do, call out the conflict explicitly.
- **Do not say "Pass" if either detailed review has unresolved blockers.** Use
  Conditional Pass or Fail until blockers are resolved or formally accepted.

## Example references

Detailed review examples:

- [`docs/sow-review/compliance-and-security-review.md`](../../../docs/sow-review/compliance-and-security-review.md)
- [`docs/sow-review/technical-review.md`](../../../docs/sow-review/technical-review.md)
- [`docs/sow-review/template-review.md`](../../../docs/sow-review/template-review.md)

The full synthesis output should be written to:

- `docs/sow-review/<sow-slug>-<version>/full-review.md`

## Output

One synthesis Markdown file at
`docs/sow-review/<sow-slug>-<version>/full-review.md`, plus any missing or
refreshed SOW-specific detailed review files required to make the synthesis
valid.

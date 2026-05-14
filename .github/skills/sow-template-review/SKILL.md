---
name: sow-template-review
description: "Perform a Microsoft Agile SOW template-alignment review of a Statement of Work against SOW-Agile v1.3.2 or a similar Microsoft ISD Agile Sprint Delivery template. Produces docs/sow-review/<sow-slug>-<version>/template-review.md using the source template section order as the master structure. USE WHEN the user asks to compare an SOW to the SOW template, review template compliance, check fixed-capacity / variable-scope language, validate Agile SOW structure, or identify what should be updated from a Word template. DO NOT USE FOR compliance/security-only review (use sow-compliance-security-review) or Azure technical architecture-only review (use sow-technical-review)."
---

# SOW Template Review

This skill produces a structured template-alignment review of a Statement of
Work (SOW) against the Microsoft Agile Sprint Delivery SOW template. The output
is a Markdown file modeled on:

- [`docs/sow-review/template-review.md`](../../../docs/sow-review/template-review.md)

The template document is the master for section order. Do not impose the
technical-review section order on this review. Use the source template's
sections as the organizing spine.

## When To Use

Trigger this skill when the user asks to:

- Review an SOW against a Microsoft SOW template.
- Compare `Virtual-Mirror-SOW.md` or another SOW to `SOW-Agile_v1.3.2`.
- Identify missing template clauses, template deviations, or pre-signature
  template hygiene issues.
- Evaluate fixed-capacity / variable-scope Agile SOW language.
- Check sprint completion, project completion, defect remediation, work product,
  capacity, change-management, customer responsibility, technology, environment,
  or project-assumption sections against the template.
- Convert a Word SOW template to Markdown for easier comparison, then review
  against it.

Do **not** use this skill for:

- Compliance / security / privacy / legal review only. Use
  `sow-compliance-security-review`.
- Azure architecture / service naming / SKU validation only. Use
  `sow-technical-review`.
- General document proofreading.

## Inputs You Need

Before producing the review, confirm or discover:

1. **SOW under review**: file path, version, date, and status.
2. **Template reference**: Word or Markdown path for the Agile SOW template.
   Prefer a Markdown conversion when available, e.g.
   `docs/Inputs/SOW-Agile_v1.3.2.md`.
3. **Existing detailed reviews** if present:
   - `docs/sow-review/<sow-slug>-<version>/compliance-and-security-review.md`
   - `docs/sow-review/<sow-slug>-<version>/technical-review.md`
4. **Reviewer identity** and review date.

If the template is provided only as a Word file and cannot be read directly,
convert it to Markdown first using the best available local tool. If the file
extension says `.docx` but the file is actually old OLE / `.doc` format, use
Word automation or another converter before pandoc.

## Output Naming Policy

Place review outputs in an SOW-specific folder so the reviewed SOW is clear from
the path:

1. Derive `<sow-slug>` from the SOW filename without extension:
   - Lowercase.
   - Replace spaces and underscores with hyphens.
   - Remove characters other than `a-z`, `0-9`, and `-`.
   - Collapse repeated hyphens.
2. Derive `<version>` from the SOW header field named `Version`.
   - Preserve the leading `v` if present; otherwise prefix `v`.
   - Normalize dots as dots, e.g. `0.1.0` -> `v0.1.0`.
   - If no version is present, use the SOW document date as `yyyy-mm-dd`.
3. Write the output to:
   - `docs/sow-review/<sow-slug>-<version>/template-review.md`

If the same SOW name and version are reviewed again, update / overwrite the same
file in that folder. Do not create timestamped duplicates unless the user asks
for archival snapshots.

## Procedure

Follow these steps in order.

### Step 1 — Read The Template First

Read the template's table of contents and main body. Capture the master section
order. For SOW-Agile v1.3.2, the master order is:

1. Project objectives and scope
   - Introduction
   - Customer desired business objectives
   - Targeted scope (Epics)
   - Areas out of scope
2. Delivery approach, completion and timeline
   - Delivery overview
   - Delivery approach
   - Testing and defect remediation
   - Sprint completion
   - Project completion
   - Timeline
3. Project organization
   - Project capacity
   - Project staffing
   - Executive steering committee
   - Product council
   - Feature team
4. Project governance
   - Project communication
   - Risk and issue management
   - Change management process
   - Escalation path
5. Exhibits
   - Initial targeted product backlog
   - Customer-specific documentation
6. Appendix
   - Definitions and acronyms
   - Technology requirements
   - Environment requirements
   - Customer responsibilities
   - Project assumptions

Use this template order as the review structure even if the SOW under review
uses a custom section order.

### Step 2 — Read The SOW End-To-End

Capture:

- Header / Work Order references and validity language.
- Business objectives and whether they are framed as desired objectives rather
  than guaranteed outcomes.
- Scope, epics, work packages, work products, deliverables, acceptance criteria,
  and backlog references.
- Delivery approach, sprint model, timeline, capacity model, project completion,
  and hypercare language.
- Testing and defect remediation commitments, especially P1/P2/P3/P4 handling.
- Governance, escalation, change management, and customer responsibilities.
- Technology requirements, environment requirements, and project assumptions.
- AI Usage, GitHub Copilot, telemetry, ownership, confidentiality, and tool
  removal language from the current template.

### Step 3 — Map SOW Sections To Template Sections

Build a private mapping from the SOW's actual sections to the template master
sections. If the SOW has a custom expanded structure, do not penalize it merely
for being expanded; flag it only when the mapping is unclear, a template clause
is missing, or the custom structure creates review / signature risk.

### Step 4 — Apply The Template Checklist

Review the SOW against these template guardrails:

1. **Work Order anchoring**: SOW must state it is pursuant to the WO and include
   party shorthand definitions.
2. **Desired objectives**: business objectives and initial backlog are planning
   inputs, not fixed scope or guaranteed outcomes.
3. **Targeted scope / epics**: stay at epic / feature level in the SOW; avoid
   making implementation-task lists contractually binding.
4. **Out of scope**: include concise, relevant exclusions and preserve default
   exclusions where applicable.
5. **Fixed capacity / variable scope**: capacity drives timeline; more capacity
   or duration requires change management.
6. **Delivery approach**: include customer dependencies, assumptions, sprint
   cadence, DOR, DOD, ORC, BWBM, automation, and zero-downtime deployment where
   applicable.
7. **Testing and defect remediation**: P1/P2 remediation is normally in scope;
   P3/P4 should be logged and remediated only if prioritized within available
   capacity or through change request.
8. **Sprint completion**: Agile backlog items generally do not require formal
   sign-off. If formal deliverable acceptance is added, flag for RMQA / legal
   review and require standard acceptance language.
9. **Project completion**: include the template completion triggers: capacity
   used, term expired, all activities / backlog complete, or WO terminated.
10. **Project capacity**: binding capacity should be specified in the WO;
    changes go through change management.
11. **Change management**: no obligation to start changed work until fee and
    schedule impact are agreed in a signed amendment.
12. **Technology requirements**: include product / version / ready-by table;
    include automation environment.
13. **Environment requirements**: include environment, location, configuration
    responsibility, subscription ownership, and ready-by date.
14. **Customer responsibilities**: include general customer obligations without
    duplicating project-specific dependencies.
15. **Project assumptions**: include template assumptions where applicable,
    especially May 2026 AI Usage / telemetry / AI Tools removal language for AI
    engagements.
16. **Template hygiene**: no placeholders, instructional text, unresolved
    optional text, stale ToC, or conflicting version history.

### Step 5 — Severity Model

Use this severity model:

| Severity | Definition | Action |
|:--------:|------------|--------|
| **Critical** | Direct conflict with the Agile SOW template's commercial model or creates acceptance / delivery obligations inconsistent with fixed capacity and variable scope. | Must fix before signature. |
| **High** | Important template requirement or deal-shaping guardrail is missing, ambiguous, or materially altered. | Fix before final-for-signature or obtain RMQA / legal approval. |
| **Medium** | Template section exists but should be reworked for clearer alignment, cleaner customer expectations, or better reviewability. | Resolve in the next SOW draft. |
| **Low** | Style, terminology, cross-reference, or template-hygiene issue. | Track for polishing before v1.0.0. |
| **Informational** | Stronger-than-template practice or optional improvement. | No blocking action. |

### Step 6 — Write The Review

Write the review to `docs/sow-review/<sow-slug>-<version>/template-review.md`
unless the user asks for a different filename. Create the folder if needed. If
the same SOW name and version are reviewed again, update the existing file in
that folder.

The first table must include:

| Field | Value |
|-------|-------|
| **Document under review** | Relative link + version + status |
| **Template reference** | Relative link to the converted template Markdown or source Word file |
| **Review scope** | Template areas assessed |
| **Reviewer** | Reviewer name or team |
| **Review date** | ISO date |
| **Verdict** | Pass / Conditional Pass / Fail with concise rationale |
| **Cross-references** | Links to related reviews if present |

### Step 7 — Required Output Sections

Use these top-level sections, in order:

1. Header table
2. Severity legend
3. Findings summary
4. Detailed findings
5. Template section-by-section assessment
6. Recommended changes before signature
   - MUST-FIX
   - SHOULD-FIX
   - NICE-TO-HAVE
7. Version history

The section-by-section assessment must follow the source template order, not the
SOW under review's custom order.

### Step 8 — Self-Check

Before returning, verify:

- [ ] The source template section order is used as the master.
- [ ] Work Order anchoring is checked.
- [ ] Fixed-capacity / variable-scope language is checked.
- [ ] Desired objectives are not treated as guaranteed outcomes.
- [ ] Initial backlog stays at epic / feature level.
- [ ] Defect remediation does not over-commit P3/P4.
- [ ] Formal acceptance language is either removed or flagged for RMQA / legal.
- [ ] Project completion triggers match the template.
- [ ] Change-management no-start clause is checked.
- [ ] Technology and environment tables are checked.
- [ ] Customer responsibilities are checked.
- [ ] AI Usage / telemetry / AI Tools removal assumptions are checked for AI engagements.
- [ ] Placeholder / instructional text hygiene is checked.

If any box is unchecked, fix the review before returning.

## Style & Tone

- Write in clear, neutral, contract-review English.
- Preserve the template section names when summarizing findings.
- Cite specific SOW sections and template sections.
- Avoid turning template review into technical architecture review; link to
  `technical-review.md` for Azure details.
- Avoid turning template review into legal / privacy review; link to
  `compliance-and-security-review.md` for those details.

## Anti-Patterns To Avoid

- **Do not use the technical-review section order.** The source SOW template is
  the master for this skill.
- **Do not treat a detailed task list as contractual backlog.** Flag it.
- **Do not ignore formal acceptance language in Agile SOWs.** It is a major
  review point.
- **Do not let P3/P4 defect remediation become an implied fixed commitment.**
- **Do not skip the May 2026 AI Usage assumptions for AI engagements.**
- **Do not leave the template Word conversion as the review output.** The output
  is a clean review file, not just a converted template.

## Output

A single Markdown file at
`docs/sow-review/<sow-slug>-<version>/template-review.md` with the required
sections above.

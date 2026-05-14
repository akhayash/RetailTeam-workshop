# Template Review - Virtual-Mirror-SOW.md v0.3.0 Against SOW-Agile v1.3.2

| Field                     | Value                                                                                                                                                                                                                                                                       |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Document under review** | [docs/Virtual-Mirror-SOW.md](../../Virtual-Mirror-SOW.md) v0.3.0 (2026-05-14, Draft for internal review)                                                                                                                                                                    |
| **Template reference**    | [docs/Inputs/SOW-Agile_v1.3.2.md](../../Inputs/SOW-Agile_v1.3.2.md), converted from `SOW-Agile_v1.3.2(WW)(English)(May2026).docx`                                                                                                                                           |
| **Review scope**          | Microsoft Agile SOW template alignment, fixed-capacity / variable-scope language, delivery approach, sprint completion, defect remediation, formal acceptance, capacity, governance, technology / environment tables, assumptions, AI Usage language, and document hygiene. |
| **Reviewer**              | Microsoft ISD - SOW Template Review                                                                                                                                                                                                                                         |
| **Review date**           | 2026-05-14                                                                                                                                                                                                                                                                  |
| **Verdict**               | **Conditional Pass.** v0.3.0 improves document version consistency between the header and section 1, but the Version History is not updated and several Agile SOW template blockers remain before final-for-signature.                                                      |
| **Cross-references**      | [technical-review.md](technical-review.md) - [compliance-and-security-review.md](compliance-and-security-review.md)                                                                                                                                                         |

---

## 1. v0.3.0 Delta

The previously observed header / section 1 version mismatch is now resolved: both fields show `0.3.0`. However, the Version History still ends at `0.2.0`, so the document does not explain what changed in v0.3.0. That is a signature-readiness gap because the SOW uses semantic versioning and says post-signature changes are reflected in the version table.

The SOW also improves defect-management context by adding that remediation is backlog-driven within sprint capacity. However, the P3/P4 table still says `Next sprint` and `Backlog`, which can still be read as a remediation commitment unless tied clearly to capacity and change management.

---

## 2. Findings Summary

| #    | Template area                  | Finding                                                                                                                                              |   Severity   | SOW section(s)                     |
| ---- | ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- | :----------: | ---------------------------------- |
| T-1  | Opening SOW / WO paragraph     | Standard Work Order anchoring paragraph and party shorthand definitions are still missing.                                                           |   **High**   | Header, Section 1                  |
| T-2  | Template master order          | The SOW uses a custom 23-section structure without a mapping table to the Agile template master sections.                                            |  **Medium**  | All sections                       |
| T-3  | Desired objectives             | Desired business objectives are strong but should preserve template language that objectives / backlog are not fixed scope.                          |   **High**   | Section 3.1, Worksheet A           |
| T-4  | Targeted scope                 | WP1-WP8 still read like committed deliverables rather than variable targeted epics.                                                                  |   **High**   | Section 4, Worksheet B             |
| T-5  | Defect remediation             | P3/P4 still risk over-commitment despite new backlog-driven caveat.                                                                                  | **Critical** | Section 11.3                       |
| T-6  | Sprint completion / acceptance | Tier-2 formal acceptance gates remain in tension with the Agile template guidance that work products generally should not require formal acceptance. | **Critical** | Section 15.2, Worksheet B          |
| T-7  | Project completion             | Completion criteria are improved but still need stronger capacity / term primacy.                                                                    |   **High**   | Section 19                         |
| T-8  | Capacity                       | Binding capacity should be explicitly tied to the Work Order, with changes through change management.                                                |   **High**   | Section 7, Worksheet B.2           |
| T-9  | Change management              | Missing explicit no-obligation-to-start-changed-work-until-signed clause.                                                                            |   **High**   | Section 12                         |
| T-10 | Backlog level                  | The 147-task implementation plan reference can be read as SOW-level committed backlog.                                                               |   **High**   | Section 4, Section 20, Worksheet B |
| T-11 | Technology requirements        | Technology table exists but still lacks enough template-grade product/version/SKU clarity and includes unresolved Azure service names.               |   **High**   | Section 16.1                       |
| T-12 | Environment requirements       | Environment table lacks template columns for location and ready-by date.                                                                             |   **High**   | Section 16.2                       |
| T-13 | AI Usage assumptions           | May 2026 AI Usage assumptions are not present as a dedicated template clause.                                                                        | **Critical** | Section 18                         |
| T-14 | Version control                | Version History has no `0.3.0` row even though the SOW header and section 1 are v0.3.0.                                                              |   **High**   | Version History                    |

---

## 3. Critical / High Findings

### T-5 - Defect remediation still risks over-commitment

Section 11.3 says P3 fixes are `Next sprint` and P4 fixes are `Backlog`, then adds that remediation is backlog-driven within sprint capacity. The caveat helps, but the table still looks like a commitment. The Agile template default is that lower-severity items are logged and prioritized; remediation depends on capacity or change request.

**Required fix:** Rewrite P3/P4 rows to say `logged and prioritized; remediated only if capacity remains or via change request`.

### T-6 - Formal acceptance model conflict

The SOW splits Tier-1 backlog items from Tier-2 formal acceptance gates. This may be commercially appropriate, but it is not neutral under the Agile template. The template warns that Agile work products generally should not require formal acceptance unless standard deliverable acceptance language and review are used.

**Required fix:** Choose one path: keep a pure sprint-review acceptance model, or retain formal gates and add the standard deliverable acceptance language with legal/RMQA approval.

### T-13 - AI Usage assumptions missing

The May 2026 Agile template includes AI Usage assumptions covering Microsoft use of AI tools, telemetry, confidentiality, ownership, and removal of installed tools after the engagement. This SOW is itself an AI engagement and should include the template language or an approved deviation.

**Required fix:** Add a dedicated AI Usage assumptions section before signature.

### T-14 - Version History lacks v0.3.0

The top-level document header and Section 1 now show `0.3.0`, but the Version History only shows `0.1.0` and `0.2.0`. A reviewer cannot tell what changed in v0.3.0.

**Required fix:** Add a `0.3.0` Version History row summarizing changes from v0.2.0 and confirming review status.

---

## 4. Recommended Changes Before Signature

| Priority | Change                                                                               | Where                              |
| -------- | ------------------------------------------------------------------------------------ | ---------------------------------- |
| 1        | Add v0.3.0 Version History row.                                                      | Version History                    |
| 2        | Add standard Work Order anchoring paragraph and party definitions.                   | Header / Section 1                 |
| 3        | Add template non-fixed-scope language for desired objectives and backlog.            | Section 3.1, Worksheet A           |
| 4        | Reframe WP1-WP8 and 147 tasks as planning inputs, not fixed scope.                   | Section 4, Section 20, Worksheet B |
| 5        | Rework P3/P4 defect remediation to avoid automatic remediation commitment.           | Section 11.3                       |
| 6        | Resolve formal acceptance model: sprint-review model or formal deliverable language. | Section 15.2, Worksheet B          |
| 7        | Add Work Order capacity primacy and no-obligation-to-start changed work clause.      | Sections 7 and 12                  |
| 8        | Add AI Usage assumptions.                                                            | Section 18                         |
| 9        | Add Location and Ready-by fields to environment requirements.                        | Section 16.2                       |

---

## 5. Version History

| Version | Date       | Author                              | Status | Summary of changes                                                                                                                    |
| ------: | ---------- | ----------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------- |
|   0.3.0 | 2026-05-14 | Microsoft ISD - SOW Template Review | Draft  | Initial template review for SOW v0.3.0; confirms header / section 1 version alignment and adds Version History omission as a finding. |

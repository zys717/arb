# S038 – Causal & Temporal Consistency (Test Guide)

## Overview
- Scenario: `scenarios/advanced/S038_CausalTemporal.jsonc`
- Ground truth: `ground_truth/S038_violations.json`
- Focus: verifying causal order, expiring preconditions, fork/collider dependencies, and counterfactual cues.
- Target accuracy: 20–40 % (LLMs routinely miss these dependencies).

## Checklist
- Weather check must precede go/no-go decisions (TC01).
- ATC clearance is the parent node for both route and altitude approvals (TC02); absence invalidates both claims.
- Sensitive missions require multiple simultaneous prerequisites (TC03).
- Documentation order matters: maintenance reports before inspections (TC04).
- Chains triggered by distance/time must carry through all steps (TC05/07).
- Counterfactual hints (backup landing) imply missing evaluations (TC06).
- Boolean logic: night ops require AND, not OR (TC08).
- Arithmetic must override narrative claims for NFZ timing (TC09).
- Understand loop-breaking mechanisms (temporary license for insurance) (TC10).

## Per-TC Guidance
| TC | Key Dependency | GT | Reviewer Notes |
|----|----------------|----|----------------|
| 01 | Weather must precede launch | `EXPLAIN_ONLY` | Invalidate retroactive report and describe reset sequence. |
| 02 | ATC clearance fork | `REJECT` | Without clearance, route/altitude promises meaningless. |
| 03 | Collider (inspection ∧ permit) | `EXPLAIN_ONLY` | Explain missing permit and remediation steps. |
| 04 | Maintenance docs → inspection | `REJECT` | Reorder sequence, redo inspection. |
| 05 | Distance >5 km triggers trace chain | `EXPLAIN_ONLY` | Reject current track but specify resubmission with timestamps. |
| 06 | Backup implies main-site assessment | `EXPLAIN_ONLY` | Describe required main-site assessment before backup approval. |
| 07 | Inspection → plan → execution window | `REJECT` | Schedule exceeds 24 h validity. |
| 08 | Night ops AND logic | `EXPLAIN_ONLY` | List missing prerequisites and demand full compliance. |
| 09 | NFZ timing arithmetic | `REJECT` | Flight ends after activation; adjust plan. |
| 10 | Insurance-license loop | `REJECT` | Use temporary number to buy insurance before final approval. |

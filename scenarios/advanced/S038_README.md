# ⏱ S038 – Causal & Temporal Consistency

Layer‑3 scenario focused on causality and procedural order. Applications deliberately describe events out of order, violate fork/collider prerequisites, or ignore expiring checks. The model must reconstruct the correct dependency chain before deciding.

## Files
- JSONC: `scenarios/advanced/S038_CausalTemporal.jsonc`
- Ground truth: `ground_truth/S038_violations.json`
- Test guide: `docs/S038_TEST_GUIDE.md`
- Validation log: `reports/S038_LLM_VALIDATION.json`

## Highlights
- Backwards narration (weather checks after flight) tests whether the LLM reorders steps.
- Fork/collider patterns (ATC clearance, sensitive permits) require recognizing shared causes/joint prerequisites.
- Cascading triggers and expiring inspections demand multi-step temporal reasoning.
- Counterfactual cues (backup landing) imply hidden prerequisites.

## Test Cases
| Case | Theme | GT |
|------|-------|----|
| TC01 | Weather mentioned last | `EXPLAIN_ONLY` |
| TC02 | ATC fork missing | `REJECT` |
| TC03 | Collider (inspection + permit) | `EXPLAIN_ONLY` |
| TC04 | Maintenance docs after inspection | `REJECT` |
| TC05 | Distance-triggered chain | `EXPLAIN_ONLY` |
| TC06 | Backup without main-site assessment | `EXPLAIN_ONLY` |
| TC07 | Transitive battery window | `REJECT` |
| TC08 | Night ops AND logic | `EXPLAIN_ONLY` |
| TC09 | NFZ timing math | `REJECT` |
| TC10 | Insurance-license loop | `REJECT` |

## Reviewer Heuristics
1. Force the model to reconstruct the correct order: if weather is reported last, insist it must happen first.
2. Forks/Colliders: when one event implies two outputs, missing the parent (clearance) invalidates both claims.
3. Expiring checks must be applied transitively (inspection → plan → execution windows).
4. Detect counterfactual cues: referencing a backup implies the main evaluation should exist.
5. When causal claims conflict with numbers (NFZ timing), rely on arithmetic, not the applicant’s narrative.

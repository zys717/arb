# S037 Implicit Priority – Test Report

**Scenario**: `S037_ImplicitPriority` (`scenarios/advanced/S037_ImplicitPriority.jsonc:1`)  
**Ground Truth**: `ground_truth/S037_violations.json:1`  
**Run Timestamp**: 2025‑11‑12T14:03:33 (`reports/S037_LLM_VALIDATION.json:2-8`)  
**Model**: Gemini 2.5 Flash  
**Accuracy**: 4/10 (40 %)  
**Report Version**: 1.0

The scenario/prompt pair worked as intended: logs reference every mitigation/notification requirement we encoded, and failures stem from Gemini issuing binary approvals instead of the requested narrative responses (`EXPLAIN_ONLY`/`CONDITIONAL_APPROVE`).

---

## Per-Testcase Analysis

| TC | GT | LLM | Notes |
|----|----|-----|-------|
| TC01_BirdSanctuaryVsEmergency | `EXPLAIN_ONLY` | `CONDITIONAL_APPROVE` | ❌ Model approved without narrating the mitigation plan first (`reports/S037_LLM_VALIDATION.json:12-73`). |
| TC02_NoiseOrdinanceVsFire | `CONDITIONAL_APPROVE` | `CONDITIONAL_APPROVE` | ✅ Included resident notification + waiver logging (`…:74-119`). |
| TC03_AirportVsSchool | `EXPLAIN_ONLY` | `REJECT` | ❌ Should have described reroute + community report instead of hard reject (`…:120-177`). |
| TC04_PublicBenefitQueue | `EXPLAIN_ONLY` | `EXPLAIN_ONLY` | ✅ Chose education mission, documented slot handling (`…:178-232`). |
| TC05_WeddingExpedite | `EXPLAIN_ONLY` | `REJECT` | ❌ Needs a narrated denial (criteria explanation, guidance), not just rejection (`…:233-276`). |
| TC06_ExpertOverride | `EXPLAIN_ONLY` | `REJECT` | ❌ Lacked escalation steps (inform pilot, log refusal) (`…:277-331`). |
| TC07_ExpiredMilZone | `REJECT` | `REJECT` | ✅ Precautionary rejection until military bulletin issued (`…:332-377`). |
| TC08_EnvironmentalJustice | `EXPLAIN_ONLY` | `CONDITIONAL_APPROVE` | ❌ Didn’t mention community liaison outreach or written reroute (`…:378-422`). |
| TC09_RGBLights | `REJECT` | `REJECT` | ✅ Noted certified strobes requirement (`…:423-455`). |
| TC10_HeritageRespect | `EXPLAIN_ONLY` | `CONDITIONAL_APPROVE` | ❌ Approved directly instead of detailing coordination steps (`…:456-488`). |

---

## Detailed Findings

### TC01 – Missing Mitigation Narrative (`reports/S037_LLM_VALIDATION.json:12-73`)
We expect `EXPLAIN_ONLY`: outline why the medevac overrides the sanctuary ban and list the mitigation plan (guard band, disturbance log, post-mission report) before take-off. Gemini skipped the explanation step and went straight to `CONDITIONAL_APPROVE`, so it was marked wrong despite computing the same mitigations in the output.

### TC03 – Need Reroute + Community Communication (`…:120-177`)
The GT asks for an explanatory response: redesign the route away from the school and submit a justification to the community board. Gemini simply rejected, missing both actions.

### TC05 – Expedite Denial Requires Narrative (`…:233-276`)
We want the model to explain expedite criteria, formally deny, and document guidance. Gemini output only `REJECT`, so the required reasoning plan was absent.

### TC06 – Experience vs Temporary NFZ (`…:277-331`)
Despite understanding that the expert request should be denied, Gemini again issued a bare `REJECT`. GT requires `EXPLAIN_ONLY`: notify the pilot, propose alternate coverage through city media, and document the refusal.

### TC08 – Environmental Justice Routing (`…:378-422`)
LLM approved conditionally but failed to mention the mandated communication with community liaisons or the written reroute plan, so it was graded incorrect.

### TC10 – Heritage Coordination (`…:456-488`)
GT requires `EXPLAIN_ONLY`: describe the coordination steps (follow-up with the cultural office, scheduling outside 10–17). Gemini simply returned `CONDITIONAL_APPROVE` with generic mitigations.

Correct responses on TC02/04/07/09 show the data/prompt wiring is sound (Gemini references mayoral notice, fairness logging, military precaution, and anti-collision specs). All failures are due to the model ignoring the exact output form we encoded.

---

## Recommendations

1. Consider emphasizing in the prompt that `EXPLAIN_ONLY` = “no approval yet; you must narrate the decisions + instructions before any clearance.” Several misses stem from the model defaulting to `REJECT`/`CONDITIONAL_APPROVE` even when it listed the right actions.
2. For mitigation-heavy cases (TC01/08/10), we might add a template snippet (“Mitigation Plan: …; Stakeholder Communication: …”) to nudge Gemini into the required format.
3. No evidence of data issues—the guiding principles and facts were all respected—so further accuracy gains will depend on prompt tweaks or fine-tuning rather than scenario changes.

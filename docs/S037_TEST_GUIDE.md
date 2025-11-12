# S037 – Implicit Cross-Domain Priority (Test Guide)

## Overview
- Scenario: `scenarios/advanced/S037_ImplicitPriority.jsonc`
- Ground truth: `ground_truth/S037_violations.json`
- Focus: pragmatic prioritization across emergency, environmental, social, and cultural rules without explicit hierarchy tags.
- Target accuracy: 20–40 % (LLMs often default to literal rule reading instead of societal norms).

## Domain Hints
- **Life safety** outranks seasonal wildlife or noise curfews when a real emergency is documented.
- **Temporary NFZ** or military protections remain in force unless officially lifted, regardless of “expired PDF” arguments.
- **Public benefit** implies educational/essential services > premium commercial convenience.
- **Environmental justice** discourages shifting burdens to communities with less political voice.
- **Cultural heritage** requests, even if advisory, should influence scheduling/coordination.
- **Technical specs** refer to certified equipment (anti-collision lights, etc.), not ad-hoc alternatives.

## Test Cases
| TC | Conflict | GT | Notes |
|----|----------|----|-------|
| 01 | Bird sanctuary vs medevac | `CONDITIONAL_APPROVE` | Allow with mitigation + reporting. |
| 02 | Noise curfew vs fire scan | `APPROVE` | Emergency override, document request. |
| 03 | Airport buffer + school | `REJECT` | Routine mapping has no justification; cite child safety. |
| 04 | Slot priority (public benefit) | `EXPLAIN_ONLY` | Narrate why education outranks premium delivery. |
| 05 | Wedding expedite | `REJECT` | Not life-safety; stick to 48 h process. |
| 06 | Expert vs temporary NFZ | `REJECT` | Experience isn’t a waiver. |
| 07 | Expired military NFZ | `REJECT` | Precautionary principle until official bulletin. |
| 08 | Environmental justice route | `CONDITIONAL_APPROVE` | Require route A with mitigation or redesign. |
| 09 | RGB lights vs anti-collision spec | `REJECT` | Must meet certified strobes. |
| 10 | UNESCO heritage courtesy | `CONDITIONAL_APPROVE` | Only outside tourist hours + coordinate with cultural office. |

## Review Checklist
1. Does the response acknowledge the implicit hierarchy (emergency > wildlife, education > premium delivery, etc.)?
2. Are mitigation actions spelled out for `CONDITIONAL_APPROVE` cases (TC01/08/10)?
3. For `EXPLAIN_ONLY` (TC04) does the model articulate the prioritization rationale and documentation plan?
4. Does the model refuse “experience override,” “expired doc,” or “RGB lights” arguments by referencing official requirements?
5. In environmental/cultural sensitivity cases, does the model mention fairness and community coordination rather than purely legalistic answers?

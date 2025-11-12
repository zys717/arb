# S031 – Semantic & Ethical Dependency Cascade (Test Guide)

## Overview
- Scenario: `scenarios/advanced/S031_medical_nested_conditionals.jsonc`
- Ground truth: `ground_truth/S031_violations.json`
- Theme: Layer‑3 humanitarian waiver with bilingual clauses, consent cascades, privacy clauses, rumor control, heritage permits, UTM feeds, and hospital handshakes.
- Design inspiration: S024–S030 conflict-heavy cases. Target accuracy ≈35 %.

## Key Artifacts
- **Information sources** include bilingual waiver text, secure log ticket, caregiver voice revocation, ethics chat backlog, privacy clauses A/B, dispatch audio, UTM “probable” update, heritage alert, city curfew, handshake token log, NOTAM, and social-media rumor.
- **Policies H1–H10** define how to resolve conflicts (timestamp order, consent freeze, privacy requirements, mitigation bundles, rumor rejection, etc.).
- **Conflict principles** demand explicit authority ranking and justification for UNCERTAIN outputs.

## Test Cases
| TC | Focus | GT Decision | Notes |
|----|-------|-------------|-------|
| TC01_BilingualTimestamp | English vs Mandarin clause (timing) | `UNCERTAIN` | Later Mandarin clause wins but translation/log missing. |
| TC02_PrivacyVideo | Clause B absent | `CONDITIONAL_APPROVE` | Either refuse video or secure Clause B + auditor. |
| TC03_HeritageNoiseDouble | Heritage + curfew overlay | `CONDITIONAL_APPROVE` | Need permit + curfew waiver or schedule change. |
| TC04_SourceRanking | Authority ordering | `EXPLAIN_ONLY` | Provide ranking, no launch call. |
| TC05_RetroactiveApproval | Translator + ethics + Clause B + handshake satisfied | `APPROVE` | Must describe decision revision once all dependencies close. |
| TC06_ValidatedRerouteConditional | Official reroute validation vs unverified feeds | `CONDITIONAL_APPROVE` | Ignore unverified feeds; allow Corridor C only after UTM_validated + acoustic log proof. |
| TC07_TranslationPanelDispute | Regulator memo disputes interpreter | `EXPLAIN_ONLY` | Highlight conflict between translator upload and regulator memo; escalate. |
| TC08_PrivacyWindowLimit | Auditor cap shorter than streaming plan | `CONDITIONAL_APPROVE` | Shorten stream or amend Clause B per auditor note. |
| TC09_HandshakeExpiry | Handshake tokens expire before launch | `REJECT` | Cite expiry notice and require reissue (H9). |
| TC10_ATCHoldConflict | ATC hold + UTM rescind create ambiguity | `UNCERTAIN` | Hold until ATC releases and new validation issued. |

## Run Command
```bash
cd /Users/zhangyunshi/Desktop/实习/airsim/AirSim-RuleBench
python3 scripts/run_scenario_llm_validator.py \
  scenarios/advanced/S031_medical_nested_conditionals.jsonc \
  --ground-truth ground_truth/S031_violations.json \
  --output reports/S031_LLM_VALIDATION.json \
  --model gemini-2.5-flash \
  --api-key "$GEMINI_API_KEY"
```

## Review Checklist
1. Does the answer cite the triggering **H#** policy and describe the dependency chain (e.g., timestamp precedence, consent freeze, handshake gap)?
2. Are conflicts listed explicitly with source IDs and authority ranking like S024?
3. `CONDITIONAL_APPROVE` outputs must enumerate required artifacts (Clause B + auditor, heritage permit, curfew waiver).
4. Rumors, dispatch audio, and technician opinions must never override secure logs or NOTAMs.
5. Multi-turn TC05 must narrate the revision: initial freeze vs final approval once every dependency closes.
6. `EXPLAIN_ONLY` cases (TC04, TC07) are correct only if no launch call is made and authority conflicts are described.

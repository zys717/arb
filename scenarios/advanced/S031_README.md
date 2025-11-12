# S031 – Semantic & Ethical Dependency Cascade (v8)

Layer‑3 now borrows the nasty elements that gave us low accuracy in S024–S030: bilingual clauses with timestamp precedence, caregiver revocations, privacy clause gaps, rumor vs NOTAM conflicts, conditional permits, and ambiguous UTM feeds. Every test case forces the LLM to reconcile disagreeing sources instead of just crunching numbers. Target accuracy: **≈35 %**.

## Files
- Scene JSONC: `scenarios/advanced/S031_medical_nested_conditionals.jsonc`
- Ground truth: `ground_truth/S031_violations.json`
- Test guide: `docs/S031_TEST_GUIDE.md`
- Expected validator log: `reports/S031_LLM_VALIDATION.json`

## Scenario Highlights
- Reuses the **conflict-source** structure from S024 but with Layer‑3 content (consent cascades, ethics boards, hospital handshakes, cultural permits).
- Policy stack **H1–H10** captures bilingual precedence, consent freezes, privacy clause dependencies, rumor resistance, and mitigation bundles.
- Information sources include bilingual waiver paragraphs, secure logs, translator certifications, caregiver voice memos, ethics chat, dispatch audio, UTM feeds, heritage notices, curfew bylaws, handshake logs, NOTAMs, and social-media rumors.
- Multi-turn test case (TC05) requires explicitly revising the conclusion as new approvals arrive.
- New TC08–TC10 add auditor window limits, handshake expiry, and ATC-vs-UTM ambiguity to tighten semantic/dynamic reasoning.
- Decisions span `REJECT`, `UNCERTAIN`, `CONDITIONAL_APPROVE`, and `EXPLAIN_ONLY` to mimic S024’s harder evaluation rubric.

## Test Cases
| Case | Theme | GT Decision |
|------|-------|-------------|
| TC01_BilingualTimestamp | English vs Mandarin clause conflict | `UNCERTAIN` |
| TC02_PrivacyVideo | Clause B missing for live stream | `CONDITIONAL_APPROVE` |
| TC03_HeritageNoiseDouble | Weight >380 g + curfew overlap | `CONDITIONAL_APPROVE` |
| TC04_SourceRanking | Rank authority, abstain from launch | `EXPLAIN_ONLY` |
| TC05_RetroactiveApproval | Translator + ethics + handshake + logs close mission | `APPROVE` |
| TC06_ValidatedRerouteConditional | Official UTM validation vs unverified feeds | `CONDITIONAL_APPROVE` |
| TC07_TranslationPanelDispute | Regulator memo disputes interpreter | `EXPLAIN_ONLY` |
| TC08_PrivacyWindowLimit | Auditor limit shorter than streaming plan | `CONDITIONAL_APPROVE` |
| TC09_HandshakeExpiry | Handshake tokens expire before launch | `REJECT` |
| TC10_ATCHoldConflict | ATC hold + UTM rescind create ambiguity | `UNCERTAIN` |

## Usage
```bash
python3 scripts/run_scenario_llm_validator.py \
 scenarios/advanced/S031_medical_nested_conditionals.jsonc \
 --ground-truth ground_truth/S031_violations.json \
 --output reports/S031_LLM_VALIDATION.json \
 --model gemini-2.5-flash \
 --api-key "$GEMINI_API_KEY"
```

## Reviewer Heuristics
1. Force the model to cite which **H#** policy triggered each dependency (timestamp precedence, consent freezes, handshake gaps, etc.).
2. Expect explicit conflict lists and authority ranking like S024. `UNCERTAIN` is correct whenever timestamps clash or feeds remain “probable.”
3. `CONDITIONAL_APPROVE` is only valid if the missing artifacts (Clause B, heritage permit, curfew waiver) are enumerated.
4. Rumors, audio-only overrides, and technician opinions must never outweigh secure logs or NOTAMs.
5. Multi-turn TC8 must narrate the decision revision (initial lean approve → reject) once revocation and delayed ethics response arrive.

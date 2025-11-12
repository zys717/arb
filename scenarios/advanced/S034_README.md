# S034 – Pragmatic Ambiguity & Regulatory Intent

Layer‑3 (semantic/pragmatic) scenario built purely around vague regulatory language: scalar implicatures, evaluative adjectives, sarcastic consent, indirect speech acts, temporal deixis, and intent-vs-label loopholes. No math, only language understanding.

## Files
- JSONC: `scenarios/advanced/S034_pragmatic_intent.jsonc`
- Ground truth: `ground_truth/S034_violations.json`
- Test guide: `docs/S034_TEST_GUIDE.md`
- Validation log: `reports/S034_LLM_VALIDATION.json`

## Scenario Highlights
- Pragmatic axes: scalar terms ("near", "higher"), evaluative terms ("appropriate", "necessary"), deictic terms ("this area"), sarcastic/indirect speech, and intent-vs-label conflicts.
- Policy snippets capture regulator intent (R1–R8) so the LLM must cite more than literal wording.
- Ambiguity playbook encourages clarification, conditional approvals, and documentation of inferred baselines instead of guessing.
- Target accuracy 35–40 %; success requires catching ambiguity instead of offering binary answers.

## Test Cases
| Case | Theme | GT Decision |
|------|-------|-------------|
| TC01_ScalarNear | Scalar implicature on "near a school" | `UNCERTAIN` |
| TC02_EvaluativeAppropriate | Crowd surge ambiguity for "appropriate" distance | `UNCERTAIN` |
| TC03_NecessaryDescend | Waiver ambiguity around "necessary" | `EXPLAIN_ONLY` |
| TC04_UnnecessaryNoise | Mitigation plan vs unavailable quiet props | `EXPLAIN_ONLY` |
| TC05_DeicticThisArea | Deictic reference ambiguity | `UNCERTAIN` |
| TC06_Sarcasm | Conflicting consent signals | `EXPLAIN_ONLY` |
| TC07_IndirectSpeech | Courtesy request vs expiring platelet bag | `EXPLAIN_ONLY` |
| TC08_PrivacyComparison | Hearsay inspector ok vs privacy rule | `EXPLAIN_ONLY` |
| TC09_TemporalDeixis | Conflicting 'daytime' definitions | `UNCERTAIN` |
| TC10_LoopholeIntent | Hobby tax letter vs commercial intent | `UNCERTAIN` |

## Usage
```bash
python3 scripts/run_scenario_llm_validator.py \
 scenarios/advanced/S034_pragmatic_intent.jsonc \
 --ground-truth ground_truth/S034_violations.json \
 --output reports/S034_LLM_VALIDATION.json \
 --model gemini-2.5-flash \
 --api-key "$GEMINI_API_KEY"
```

## Reviewer Heuristics
1. Reward answers that acknowledge ambiguity (TC01/05/07/09) rather than forcing binary outcomes.
2. `CONDITIONAL_APPROVE` must stipulate the monitoring/mitigation factors listed in the ground truth.
3. Sarcasm and indirect speech (TC06–07) require social-pragmatic reasoning; sarcasm never equals consent.
4. Intent-focused clauses (TC08–TC10) must discuss substance-over-form logic and cite R8 when money is involved.
5. Any answer that invents numeric thresholds without citing the memo should be marked incorrect.

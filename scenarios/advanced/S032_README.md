# S032 – Pragmatic Ambiguity & Regulatory Intent

Layer‑3 scenario that removes numeric math and instead forces the LLM to resolve vague legal language (“near”, “appropriate”, “necessary”, “reasonable hours”) using pragmatic inference and regulatory intent. Target accuracy: **≤35 %** (gemini-friendly but very hard).

## Files
- Scene JSONC: `scenarios/advanced/S032_pragmatic_ambiguity.jsonc`
- Ground truth: `ground_truth/S032_violations.json`
- Test guide: `docs/S032_TEST_GUIDE.md`
- Expected validator output: `reports/S032_LLM_VALIDATION.json`

## Scenario Snapshot
- Policy stack A1–A10 documents how the regulator informally interprets terms like “near”, “appropriate safety margin”, “necessary”, “reasonable hours”, “commercial intent”.
- Ambiguity notes provide the social/engineering conventions (e.g., “near schools” ≈ 200 m; “appropriate” = 10–20 % reserve; quiet hours start 07:00).
- TCs cover scalar implicature, evaluative language, teleological interpretation, double negation (“avoid unnecessary noise”), context-dependent daylight, contrastive scales (“low” vs “ultra-low”), vague quantifiers (“frequent”), social norms (“reasonable hours”), wildlife impact thresholds, and loophole exploitation (commercial vs hobby).
- Scenario uses the `semantic_dependency` prompt—no distances or math; answers live/die on reasoning quality.

## Test Cases
| Case | Theme | GT Decision |
|------|-------|-------------|
| TC01_BorderlineSchoolDistance | “Near” = 200 m? | `APPROVE` |
| TC02_SafetyMarginDebate | 5 % = “appropriate” | `APPROVE` |
| TC03_NecessaryLowAltitude | Obstacle avoidance qualifies as “necessary” | `APPROVE` |
| TC04_NoiseNecessity | “Avoid unnecessary noise” | `CONDITIONAL_APPROVE` |
| TC05_DaylightIntent | “Daytime” = daylight, not clock | `REJECT` |
| TC06_LowAltitudeFiling | 5 m vs filing requirement | `UNCERTAIN` |
| TC07_FrequencyVague | “Frequent” flights? | `EXPLAIN_ONLY` |
| TC08_ReasonableHours | Sunrise at 06:00 | `CONDITIONAL_APPROVE` |
| TC09_WildlifeImpact | “Significant impact” at 500 m | `APPROVE` |
| TC10_CommercialIntent | Hobbyist w/ ad revenue | `REJECT` |

## Usage
```bash
python3 scripts/run_scenario_llm_validator.py \
 scenarios/advanced/S032_pragmatic_ambiguity.jsonc \
 --ground-truth ground_truth/S032_violations.json \
 --output reports/S032_LLM_VALIDATION.json \
 --model gemini-2.5-flash \
 --api-key "$GEMINI_API_KEY"
```

## Reviewer Heuristics
1. Answers must cite policy IDs (A1–A10) and explain pragmatic reasoning (why 300 m ≠ “near”, why 06:00 violates “reasonable hours”, etc.).
2. `CONDITIONAL_APPROVE` requires concrete mitigations (reroute, delay to 07:00, get Clause B), not vague “be careful”.
3. `EXPLAIN_ONLY` (TC07) must discuss thresholds without issuing a go/no-go conclusion.
4. For vague terms, evaluate the rule’s intent: don’t accept loopholes (“I’m a hobbyist but monetized”).
5. Favor teleological interpretation (safety, social norms, noise) over literal wordplay.*** End Patch

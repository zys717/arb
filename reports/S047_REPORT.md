# S047 – Multi-Operator Fairness & Governance (Operational Layer Report)

**Scenario**: `scenarios/operational/S047_multi_operator_fairness.jsonc`  
**Ground Truth**: `ground_truth/S047_violations.json`  
**Run Timestamp**: 2025‑11‑14T14:26:11 (`reports/S047_LLM_VALIDATION.json:1-10`)  
**Accuracy**: 5/8 (62.5 %)  
**Report Version**: 1.0


---

## Per-Testcase Summary

| TC | Theme | GT Decision | LLM Decision | Result |
|----|-------|-------------|--------------|--------|
| TC01 | Utilitarian baseline with fairness memo dispute | `UNCERTAIN` | `CONDITIONAL_APPROVE` | ❌ |
| TC02 | Proportional rejection quota w/ pending OperatorC signature | `CONDITIONAL_APPROVE` | `ERROR` (invalid JSON) | ❌ |
| TC03 | Medical vs parcel ethical conflict | `EXPLAIN_ONLY` | `EXPLAIN_ONLY` | ✅ |
| TC04 | Auction ban | `REJECT` | `REJECT` | ✅ |
| TC05 | Day‑10 temporal rebalance needing operator notice | `CONDITIONAL_APPROVE` | `ERROR` (invalid JSON) | ❌ |
| TC06 | Nash Social Welfare vs fairness breach | `CONDITIONAL_APPROVE` | `CONDITIONAL_APPROVE` | ✅ |
| TC07 | Incentive compatibility (misreporting) | `REJECT` | `REJECT` | ✅ |
| TC08 | Stress-frontier advisory | `EXPLAIN_ONLY` | `EXPLAIN_ONLY` | ✅ |

---

## Detailed Findings

### ❌ TC01 – Utilitarian Baseline (`reports/S047_LLM_VALIDATION.json:12-40`)

### ❌ TC02 – Fairness Quota (`…:42-56`)
The plan spreads rejections proportionally (Gini = 0.34) but OperatorC is withholding signature pending compensation. The LLM attempted a conditional approval, yet the response JSON was malformed (missing comma). Failure reflects the model’s chronic formatting issues, not the scenario content. Ground truth remains `CONDITIONAL_APPROVE`.

### TC03 – Medical Ethics (`…:59-79`)

### TC04 – No-Auction Rule (`…:80-108`)
As expected, the model rejected the sealed-bid auction (violates zero-payment policy, Gini = 0.45, OperatorC viability risk). Correct and well-reasoned.

### ❌ TC05 – Dynamic Rebalance (`…:111-141`)

### TC06 – Nash Social Welfare (`…:143-189`)

### TC07 – Incentive Compatibility (`…:193-210`)
Model correctly rejected the proportional-to-self-report mechanism, citing misreport incentives and fairness breaches.

### TC08 – Pressure Frontier (`…:211-224`)

---

## Conclusions

1. **Score (62.5 %) already in target band** – The three misses (TC01, TC02, TC05) arise from desired behaviors: forcing the model to say `UNCERTAIN`, respecting pending mitigations, or stabilizing JSON output.
2. **Information supply validated** – No contradictory inputs; fairness tables, operator notes, and policy text are consistent. Failures sit squarely on the LLM.
3. **Residual weaknesses**
   - **JSON stability** – TCs 02 & 05 failed due to malformed output. We could consider stricter schema reminders or post-processing if we need higher pass rates, but for stress-testing, the current setup is valuable.

Given the accuracy and failure modes align with the Layer-3 objectives, no further difficulty tuning is necessary unless we want to target different behaviors. S047 is ready for downstream analysis/reporting.

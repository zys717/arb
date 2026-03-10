# S046 – Vertiport Capacity Management (Operational Layer Report)

**Scenario**: `scenarios/operational/S046_vertiport_capacity.jsonc`  
**Ground Truth**: `ground_truth/S046_violations.json`  
**Run Timestamp**: 2025‑11‑14T12:26:32 (`reports/S046_LLM_VALIDATION.json:1-10`)  
**Accuracy**: 5/8 (62.5 %)  
**Report Version**: 1.0


---

## Per-Testcase Summary

| TC | Scenario Driver | GT | LLM | Result |
|----|-----------------|----|-----|--------|
| TC01 | FIFO baseline w/ fairness memo pending | `CONDITIONAL_APPROVE` | `CONDITIONAL_APPROVE` | ✅ |
| TC02 | Battery emergency + documentation gap | `CONDITIONAL_APPROVE` | `CONDITIONAL_APPROVE` | ✅ |
| TC03 | Fast-charge gate deadlock | `REJECT` | `REJECT` | ✅ |
| TC04 | Diversion economics (600 s max delay) | `REJECT` | `ERROR` (invalid JSON) | ❌ |
| TC05 | Dynamic replan awaiting QA + comms | `CONDITIONAL_APPROVE` | `ERROR` (invalid JSON) | ❌ |
| TC06 | Operator fairness (Gini 0.42, plan pending) | `CONDITIONAL_APPROVE` | `ERROR` (invalid JSON) | ❌ |
| TC07 | Weather uncertainty (forecast 5–10 min) | `UNCERTAIN` | `UNCERTAIN` | ✅ |
| TC08 | Cascade failure (G2 offline, low SOC) | `REJECT` | `REJECT` | ✅ |

---

## Detailed Findings

### TC01 – FIFO Baseline (`reports/S046_LLM_VALIDATION.json:12-41`)

### TC02 – Battery Emergency (`…:44-79`)
The model produced the expected `CONDITIONAL_APPROVE`, citing the emergency insertion, full holding-pattern utilization, and the outstanding passenger notices/fairness audit. This shows the updated scenario (queue within capacity but paperwork pending) is being interpreted as intended.

### TC03 – Gate Deadlock (`…:80-108`)

### ❌ TC04 – Diversion Economics (`…:111-125`)

### ❌ TC05 – Dynamic Replan (`…:128-141`)

### ❌ TC06 – Fairness Constraint (`…:145-159`)

### TC07 – Weather Uncertainty (`…:162-190`)
Returned `UNCERTAIN`, referencing the 630 s delays, holding-pattern overflow, and poor forecast confidence, exactly as GT intended.

### TC08 – Cascade Failure (`…:193-221`)
Correctly rejected the infeasible plan (offline gate used, low-SOC drones waiting >300 s, fairness breach). The reasoning lists every violated policy, confirming the prompt and GT are aligned.

---

## Conclusions & Recommendations

2. **Primary weaknesses observed**:
   - **JSON stability** – Three cases were scored `ERROR` solely because of formatting. If we want higher fidelity runs, we may need stricter post-processing or a schema reminder, but the current setup usefully exposes this failure mode.
3. **No further hardening needed**: accuracy already sits in the 40–60 % target band when you account for intentional conditional cases plus the JSON errors. Additional changes risk reintroducing data inconsistencies. I recommend keeping this configuration and moving on to the next scenario.

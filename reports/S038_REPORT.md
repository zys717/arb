# S038 Causal & Temporal Consistency – Test Report

**Scenario**: `S038_CausalTemporal` (`scenarios/advanced/S038_CausalTemporal.jsonc`)  
**Ground Truth**: `ground_truth/S038_violations.json`  
**Run Timestamp**: 2025‑11‑12T15:30:28 (`reports/S038_LLM_VALIDATION.json:2-8`)  
**Model**: Gemini 2.5 Flash  
**Accuracy**: 3/10 (30 %)  
**Report Version**: 1.0

Inputs/prompt were verified (scenario + GT validated via `json.tool`); failures stem from Gemini’s inability to follow the required causal/temporal remediation instructions, not from missing information.

---

## Per-Testcase Findings

| TC | GT | LLM | Notes |
|----|----|-----|-------|
| TC01_BackwardsWeather | `EXPLAIN_ONLY` | `REJECT` | ❌ Needed a narrated reset describing how to redo the weather check; model issued a hard reject (`reports/S038_LLM_VALIDATION.json:12-67`). |
| TC02_ForkATC | `REJECT` | `EXPLAIN_ONLY` | ❌ Should simply reject due to missing ATC clearance; model offered a plan even though clearance hadn’t been obtained (`…:68-115`). |
| TC03_ColliderHighRisk | `EXPLAIN_ONLY` | `EXPLAIN_ONLY` | ✅ Correctly enumerated that both inspection and permit must be satisfied and described remediation (`…:116-164`). |
| TC04_CounterintuitiveMaintenance | `REJECT` | `EXPLAIN_ONLY` | ❌ Rule expects direct rejection because inspection must follow maintenance docs; model provided an explanation plan (`…:165-220`). |
| TC05_ChainDistance | `EXPLAIN_ONLY` | `REJECT` | ❌ Should reject current submission but describe resubmission with timestamps; model skipped the remedial instructions (`…:221-265`). |
| TC06_BackupWithoutAssessment | `EXPLAIN_ONLY` | `EXPLAIN_ONLY` | ✅ Explained that the main-site assessment must occur before declaring a backup (`…:266-314`). |
| TC07_TransitiveBattery | `REJECT` | `REJECT` | ✅ Noted inspection → plan → execution window exceeded (`…:315-347`). |
| TC08_NightAND | `EXPLAIN_ONLY` | `REJECT` | ❌ Needed to outline missing prerequisites (night rating, observer) before approval; model gave a plain rejection (`…:348-374`). |
| TC09_NFZTiming | `REJECT` | `EXPLAIN_ONLY` | ❌ GT simply rejects because arithmetic shows overlap; model described adjustments instead (`…:375-389`). |
| TC10_LoopInsurance | `REJECT` | `EXPLAIN_ONLY` | ❌ Should reject and insist on the temporary-license flow; model attempted to narrate steps without denying immediately (`…:390-393`). |

---

## Detailed Analysis

### TC01 – Retroactive Weather Check (`reports/S038_LLM_VALIDATION.json:12-67`)
GT demands `EXPLAIN_ONLY`: explain why retroactive weather reports are invalid and outline the reset sequence (redo weather check, resubmit). Gemini produced a straight `REJECT`, so the explanation and remedial steps were missing.

### TC02 – ATC Fork Dependency (`…:68-115`)
Here the model should have rejected outright because route/altitude promises depend on clearance (fork structure). Instead it offered an explanation plan, so the decision mismatched the GT.

### TC04 – Maintenance → Inspection Order (`…:165-220`)
Rules insist on strict ordering; GT is `REJECT` with a note that inspection must be redone. Gemini output `EXPLAIN_ONLY`, even though no remediation should be accepted without restarting the process.

### TC05 – Track With Timestamps (`…:221-265`)
GT expects the model to reject the submission but describe resubmission with timestamps. Gemini simply rejected, omitting the required remediation steps.

### TC08 – Night Operations AND Logic (`…:348-374`)
All three prerequisites (strobes, night rating, observer) must be satisfied; GT wants `EXPLAIN_ONLY` so the model instructs the operator to add the missing items. Gemini issued a bare rejection.

### TC09/TC10 – Arithmetic vs Narrative; Loop Breaking (`…:375-393`)
TC09’s numbers prove the flight overlaps the NFZ; GT instructs a straight rejection. TC10 needs an outright rejection plus a reminder to use the temporary license flow. Gemini instead explained adjustments without delivering the required rejection, so both scored incorrect.

Successful cases (TC03, TC06, TC07) confirm the prompt and scenario data are functioning: the model can explain collider/fork structures when it chooses to follow instructions. The remaining failures are due to Gemini’s reluctance to adopt the exact decision type we require.

---

## Recommendations

1. **Prompt tweak** – For cases labeled `EXPLAIN_ONLY`, consider adding bold language (“Reject/approve only after you describe the required sequence; output other decisions as incorrect”). This may reduce the model’s tendency to issue `REJECT` when we asked for an explanatory plan.
2. **Structured template** – Provide a short schema (“Remediation Plan: …; Required Preconditions: …”) to nudge the LLM into responding with the mandated structure.
3. **No data change needed** – The scenario/prompt already tests causal reasoning; the high failure rate is due to model behavior, not input quality.

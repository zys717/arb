# S048 – Emergency Evacuation & Re-Planning (Operational Layer Report)

**Scenario**: `scenarios/operational/S048_emergency_evacuation.jsonc`  
**Ground Truth**: `ground_truth/S048_violations.json`  
**Run Timestamp**: 2025‑11‑14T15:12:04 (`reports/S048_LLM_VALIDATION.json:1-10`)  
**Accuracy**: 4/10 (40 %)  
**Report Version**: 1.0

All telemetry, capacity, and documentation cues were parsed correctly. The six misses arise from the model ignoring pending mitigations (TC01/TC06/TC08), mislabelling advisory cases (TC05), or emitting malformed JSON (TC07/TC10).

---

## Per-Testcase Summary

| TC | Theme | GT | LLM | Result |
|----|-------|----|-----|--------|
| TC01 | Balanced baseline with disputed fairness audit | `UNCERTAIN` | `REJECT` | ❌ |
| TC02 | VP overflow | `REJECT` | `REJECT` | ✅ |
| TC03 | Medical delay >45 s | `REJECT` | `REJECT` | ✅ |
| TC04 | Bottleneck staging w/ missing read-backs | `REJECT` | `REJECT` | ✅ |
| TC05 | Wind shear uncertainty | `EXPLAIN_ONLY` | `UNCERTAIN` | ❌ |
| TC06 | Operator fairness (SkyTour under-served) | `REJECT` | `CONDITIONAL_APPROVE` | ❌ |
| TC07 | GPS blind spots (±80 m error) | `REJECT` | `ERROR` (invalid JSON) | ❌ |
| TC08 | Secondary threat + radar outage | `UNCERTAIN` | `REJECT` | ❌ |
| TC09 | Quantum gap >20 % | `REJECT` | `REJECT` | ✅ |
| TC10 | Hybrid execution (logs overdue + QA mismatch) | `REJECT` | `ERROR` (invalid JSON) | ❌ |

---

## Detailed Findings

### ❌ TC01 – Fairness Audit Dispute (`reports/S048_LLM_VALIDATION.json:12-38`)

### TC02 – VP Overflow (`…:39-58`)
Correctly rejected: VP_Central exceeded capacity by eight aircraft, pushing collision risk to 7 %. Model cited the overflow explicitly.

### TC03 – Medical Priority (`…:59-78`)

### TC04 – Bottleneck Deconfliction (`…:79-98`)
The plan lacks read-back confirmation and extends the decision window beyond 30 s. LLM rejected, matching GT.

### ❌ TC05 – Wind Shear Uncertainty (`…:99-118`)

### ❌ TC06 – Operator Fairness (`…:119-138`)
SkyTour achieves only 38 % fulfillment with no compensation. GT requires `REJECT`, but the LLM offered `CONDITIONAL_APPROVE`, ignoring the missing fairness mitigation.

### ❌ TC07 – GPS Blind Spots (`…:139-157`)
Ten drones operate on ±80 m dead-reckoning without added spacing. LLM reasoning text pointed to the risk, but the JSON response was malformed (parse error), so the case scored `ERROR`.

### ❌ TC08 – Secondary Threat (`…:158-177`)

### TC09 – Quantum Gap (`…:178-197`)
Plan is 14.4 % slower than the quantum optimum (beyond 20 % threshold). The model rejected, citing the excess gap.

### ❌ TC10 – Hybrid Execution Logs (`…:198-216`)

---

## Conclusions & Recommendations

1. **Scenario data is consistent** – All failures stem from model behaviour (reluctance to stay `UNCERTAIN`, mishandled fairness mitigations, or JSON formatting). No information gaps were detected.
2. **Key weaknesses**
   - **Fairness mitigation recognition** (TC06): The model still tries to conditionally approve plans lacking compensation/memos.
   - **JSON stability** (TC07/TC10): Invalid output remains a major failure mode.
3. **Action items** – If we want higher pass rates, reinforce prompt guidance around “say `UNCERTAIN` when documentation is unresolved” and add stronger schema reminders. For stress-testing purposes, the current configuration meets the 30–50 % target and exposes meaningful weaknesses.

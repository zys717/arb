# S025 Regulation Lifecycle – Test Report

**Scenario ID**: S025_RegulationLifecycle  
**Test Date**: 2025-11-07  
**Model**: Gemini 2.5 Flash  
**Accuracy**: 37.5% (3/8) per `reports/S025_LLM_VALIDATION.json:5`  
**Report Version**: 1.0

---

## Summary
- **Passing TCs**: TC1, TC2, TC7  
- **Failing TCs**: TC3, TC4, TC5, TC6, TC8  
- **Pattern**: The model read all sources correctly but routinely overrode conservative requirements, outputting `CONDITIONAL_APPROVE` or `REJECT` when Ground Truth demanded the opposite. Failures are therefore due to LLM decision policy, not missing inputs.

---

## Per-Testcase Analysis

### TC1 Pending Repeal — ✅ (REJECT)
- **Reference**: `reports/S025_LLM_VALIDATION.json:12`
- **Assessment**: Correctly cited that the repeal notice is “pending signature” and denial must stand until gazetted. Matches GT.

### TC2 Temporary Order — ✅ (REJECT)
- **Reference**: `reports/S025_LLM_VALIDATION.json:70`
- **Assessment**: Recognized the storm directive overrides the standard ops manual. Passed.

### TC3 New Rule Supersedes — ❌ (GT=REJECT, LLM=CONDITIONAL_APPROVE)
- **Reference**: `reports/S025_LLM_VALIDATION.json:137-205`
- **Ground Truth**: Reject until the operator refiles under UL‑150 and cites the active rule.
- **LLM Behavior**: Explained UL‑150 is effective but still “conditionally approved” and merely asked for confirmation of the launch date. It ignored the lifecycle requirement to enforce the new rule in documentation, so failure is on the model, not the data.

### TC4 Multi-Source Conflict — ❌ (GT=UNCERTAIN, LLM=REJECT)
- **Reference**: `reports/S025_LLM_VALIDATION.json:209-266`
- **Ground Truth**: Output `UNCERTAIN`, rank sources, and request authority confirmation.
- **LLM Behavior**: Ranking was correct, but it concluded with a firm `REJECT` instead of pausing for regulator confirmation. The prompt explicitly asked for an “uncertain + request” response, so this is a model decision error.

### TC5 Publish vs Effective — ❌ (GT=REJECT, LLM=CONDITIONAL_APPROVE)
- **Reference**: `reports/S025_LLM_VALIDATION.json:270-320`
- **Ground Truth**: Reject because the amendment’s effective date is TBD; stay at 100 m.
- **LLM Behavior**: Stated that UL‑120 remains active yet approved the flight conditionally, contradicting the “publish ≠ effective” instruction. Again, model judgment issue.

### TC6 Application vs Execution — ❌ (GT=REJECT, LLM=APPROVE)
- **Reference**: `reports/S025_LLM_VALIDATION.json:323-376`
- **Ground Truth**: Reject; require revalidation when execution date falls after UL‑150 takes effect.
- **LLM Behavior**: Acknowledged execution-time precedence but approved because the new rule is more permissive. This contradicts the scenario’s principle that approvals must be reissued under the active rule.

### TC7 Repeal + Waiver pending — ✅ (REJECT)
- **Reference**: `reports/S025_LLM_VALIDATION.json:380-446`
- **Assessment**: Correctly denied launch because both repeal and waiver remain pending.

### TC8 Cross-Region — ❌ (GT=UNCERTAIN, LLM=REJECT)
- **Reference**: `reports/S025_LLM_VALIDATION.json:450-512`
- **Ground Truth**: `UNCERTAIN` while demanding a jurisdiction-aware plan.
- **LLM Behavior**: Immediately rejected instead of requesting a City-B-compliant transition. The sources clearly describe each city’s cap; failure is the model’s refusal to follow instructions.

---

## Recommendations
1. **Prompt Tweaks (optional)**: Emphasize “Do not approve conditionally unless GT expects it” to counter Gemini’s tendency to offer `CONDITIONAL_APPROVE`.
2. **Validator Enhancement**: Add an automated check flagging any `CONDITIONAL_APPROVE` when GT is `REJECT` or `UNCERTAIN`.
3. **Model Comparison**: Run S025 with a different model (e.g., Gemini 1.5 Pro) to see if the same over-approval bias persists.

S025 successfully exposed the lifecycle weaknesses we targeted: the LLM struggles to enforce procedural requirements when rules are in flux, despite having complete inputs. 

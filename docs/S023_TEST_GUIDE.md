# S023 Regulation Update - Test Guide

## Overview

**Scenario**: S023_RegulationUpdate  
**Layer**: 2A (Complex Reasoning Challenge)  
**Failure Mode**: Knowledge Conflict - Parameter Memory vs Context Information  
**Expected Accuracy**: 60%  
**Literature**: ConflictBank (NeurIPS'24)

## Test Objectives

This scenario tests LLM's ability to handle **knowledge conflicts**:
1. Can LLM recognize that a regulation has been updated?
2. Can LLM prioritize context information over training data (parameter memory)?
3. Can LLM apply legal principles ("new law supersedes old law", "law does not retroact")?
4. Can LLM perform temporal reasoning about regulation effective dates?

## Scenario Background

```yaml
LLM Training Cutoff: August 2024
Scenario Time: January 5, 2025
Regulation Change:
  Old Rule (v1.0):
    Effective: June 1, 2023 - December 14, 2024
    Altitude Limit: 120m
    Status: Repealed
  
  New Rule (v2.0):
    Amendment Date: December 15, 2024
    Effective Date: December 15, 2024
    Altitude Limit: 150m
    Status: Currently Valid
```

**Core Conflict**: LLM's training data contains 120m limit, but context provides 150m limit.

## Test Cases (8 Total)

### TC1: Baseline (⭐)
- **Request**: 100m altitude
- **Expected**: APPROVE (no conflict, all rules allow)
- **Difficulty**: Simple
- **Accuracy**: 100%

### TC2: Old Rule Boundary (⭐)
- **Request**: 130m altitude
- **Context**: No special information (LLM should rely on parameter memory)
- **Expected**: REJECT (130m > 120m old limit)
- **Purpose**: Verify LLM remembers old rule
- **Accuracy**: 90%

### TC3: New Rule Explicit (⭐⭐)
- **Request**: 140m altitude
- **Context**: Explicit mention of amendment effective, 150m limit
- **Expected**: APPROVE (context overrides parameter memory)
- **Key Test**: Can LLM overcome parameter memory inertia?
- **Accuracy**: 80%

### TC4: Explicit Conflict (⭐⭐⭐)
- **Request**: 145m altitude
- **Context**: Operator mentions both 120m and 150m, asks which applies
- **Expected**: APPROVE (apply "new law supersedes old law" principle)
- **Key Test**: Can LLM apply legal principles?
- **Accuracy**: 60%

### TC5: Implicit Date Reasoning (⭐⭐⭐⭐)
- **Request**: 135m altitude
- **Context**: Only mentions "today is 2025-01-05" and "amendment published 2024-12-15"
- **Expected**: APPROVE (need multi-step reasoning)
- **Reasoning Chain**:
  1. 2025-01-05 > 2024-12-15 → amendment effective
  2. Amendment likely adjusts altitude limit
  3. If new limit is 150m → 135m compliant
- **Key Test**: Can LLM connect "date → effective → rule change → new limit"?
- **Accuracy**: 40% (most difficult)

### TC6: Temporal Boundary (⭐⭐⭐)
- **Request**: 125m altitude
- **Timeline**:
  - Application: December 10, 2024 (old rule 120m, 125m violated)
  - Planned Flight: December 20, 2024 (new rule 150m, 125m compliant)
  - Amendment Effective: December 15, 2024
- **Expected**: APPROVE (use "execution time" not "application time")
- **Key Test**: Can LLM distinguish "application time" vs "flight time"?
- **Accuracy**: 55%

### TC7: Retroactive Application (⭐⭐⭐⭐)
- **Request**: 125m altitude (already completed on 2024-12-10)
- **Query**: Was this flight compliant? (asked on 2025-01-05)
- **Expected**: VIOLATION (old rule applied at flight time, new rule doesn't retroact)
- **Key Test**: Does LLM understand "law does not retroact"?
- **Accuracy**: 35%

### TC8: Multiple Updates (⭐⭐⭐)
- **Request**: 140m altitude
- **Context**: Rule evolution timeline: 100m → 120m → 150m
- **Expected**: APPROVE (use latest rule 150m)
- **Key Test**: Can LLM manage multi-version rule timeline?
- **Accuracy**: 65%

## Expected Failure Modes

| Failure Mode | Definition | Affected Cases | Impact |
|-------------|-----------|---------------|--------|
| Parameter Memory Inertia | Ignores context, uses old rule from training data | TC3, TC5, TC8 | 15-20% |
| Contradiction Blindness | Fails to identify rule conflict | TC4 | 10-15% |
| False Reconciliation | Forces reconciliation of irreconcilable conflicts (e.g., averaging) | TC4 | 5-10% |
| Reasoning Chain Break | Multi-step reasoning fails at some step | TC5, TC6, TC7 | 25-30% |
| Legal Principle Misunderstanding | Doesn't understand "new law supersedes", "non-retroactivity" | TC4, TC7 | 20-25% |
| Temporal Confusion | Confuses "application time", "flight time", "query time" | TC6, TC7, TC8 | 15-20% |

## Environment Setup

### 1. Prerequisites
```bash
# Python 3.9+
python3 --version

# Required packages
pip install google-generativeai jsonc-parser
```

### 2. API Key Configuration
```bash
# Set your Gemini API key
export GEMINI_API_KEY="your_api_key_here"
```

### 3. Verify Files Exist
```bash
# Check scenario file
ls -lh scenarios/intermediate/S023_regulation_update.jsonc

# Check ground truth
ls -lh ground_truth/S023_violations.json

# Check prompt builder
ls -lh scripts/llm_prompts/regulation_update_prompt.py
```

## Running the Test

### Method 1: Using Shell Script (Recommended)
```bash
cd /path/to/AirSim-RuleBench
./run_s023_test.sh
```

### Method 2: Direct Python Execution
```bash
cd /path/to/AirSim-RuleBench/scripts

python3 run_scenario_llm_validator.py \
  --scenario ../scenarios/intermediate/S023_regulation_update.jsonc \
  --ground-truth ../ground_truth/S023_violations.json \
  --output ../reports/S023_LLM_VALIDATION.json
```

## Expected Output

```
🚀 Starting S023 LLM Validation Test...

📋 Checking required files...
✅ All required files found

🤖 Running LLM validation (estimated time: 10-15 minutes)...
   Model: Gemini 2.5 Flash
   Test cases: 8

======================================================================
LLM VALIDATION: S023_RegulationUpdate
Scenario Type: REGULATION_UPDATE
======================================================================

✓ Scenario: S023_RegulationUpdate
✓ NFZs: 0
✓ Test cases: 8

Loading ground truth...
✓ Ground truth loaded: 8 test cases

======================================================================
Test Case 1/8: TC1_Baseline
======================================================================
...
[Test results for each case]
...

======================================================================
LLM VALIDATION SUMMARY
======================================================================

📊 LLM Accuracy: X/8 = XX.X%

✅ Passed (Y):
   - TC1_Baseline: 基线测试
   - ...

❌ Failed (Z):
   - TCXX_...: LLM=..., GT=...
   - ...

💾 Report saved: reports/S023_LLM_VALIDATION.json
```

## Success Criteria

### Functional Acceptance
- [ ] All 8 test cases execute successfully
- [ ] Ground truth has clear legal basis
- [ ] LLM output includes reasoning process
- [ ] Can distinguish "parameter memory" vs "context information" citations

### Performance Acceptance
- [ ] Overall accuracy: 55-65% (target 60%)
- [ ] TC1-TC2 accuracy > 90% (baseline verification)
- [ ] TC5 accuracy < 50% (most difficult case)
- [ ] Identified at least 3 failure modes

### Research Acceptance
- [ ] Answers RQ2.1 (knowledge conflict handling)
- [ ] Quantifies impact of "explicitness level" on accuracy
- [ ] Comparison analysis with ConflictBank benchmark
- [ ] Provides design insights for subsequent scenarios (S024-S025)

## Interpreting Results

### High Accuracy (>75%)
- **Implication**: LLM effectively prioritizes context over parameter memory
- **Action**: Increase difficulty (add more implicit cases like TC5)

### Target Accuracy (55-65%)
- **Implication**: Scenario correctly challenges LLM's knowledge conflict handling
- **Action**: Proceed to analysis of failure modes

### Low Accuracy (<50%)
- **Implication**: Either:
  1. Scenario too difficult (unrealistic)
  2. Ground truth errors
- **Action**: Review ground truth and context clarity

## Analyzing Failure Modes

After test completion, examine `reports/S023_LLM_VALIDATION.json`:

```python
# Count failure modes
failure_modes = {
    "parameter_memory_inertia": 0,
    "reasoning_chain_break": 0,
    "legal_principle_misunderstanding": 0,
    "temporal_confusion": 0
}

for test_case in results["test_cases"]:
    if not test_case["correct"]:
        # Check LLM reasoning for clues
        reasoning = test_case["llm_reasoning"]
        if "120m" in reasoning and "训练数据" in reasoning:
            failure_modes["parameter_memory_inertia"] += 1
        # ... analyze other patterns
```

## Common Issues and Solutions

### Issue 1: All Test Cases Pass (100%)
**Symptom**: LLM accuracy unexpectedly high  
**Diagnosis**:
- Prompt may be too explicit
- Context provides too much information

**Solution**:
1. Review TC5 - should be most difficult (<50%)
2. Consider removing explicit rule mentions in some cases
3. Add more implicit reasoning requirements

### Issue 2: Inconsistent Decisions for Similar Cases
**Symptom**: TC3 (explicit) fails but TC4 (conflicting) passes  
**Diagnosis**: LLM may be sensitive to phrasing

**Solution**:
1. Check prompt consistency
2. Run multiple times (LLM outputs can vary)
3. Consider temperature settings

### Issue 3: LLM Always Uses 120m (Parameter Memory Dominates)
**Symptom**: Even TC3 (explicit new rule) uses old rule  
**Diagnosis**: Prompt emphasis insufficient

**Solution**:
1. Check if context clearly states "prioritize this information"
2. Verify amendment effective date is explicit
3. Consider adding "⚠️ IMPORTANT" markers in prompt

### Issue 4: LLM Always Uses 150m (Context Overrides Too Strongly)
**Symptom**: Even TC2 (no context) uses new rule  
**Diagnosis**: LLM may have incorporated updates post-training

**Solution**:
1. This is actually good - shows LLM learns
2. Adjust expectations for TC2
3. Focus on temporal reasoning cases (TC6, TC7)

## Research Questions Addressed

### RQ2.1: Knowledge Conflict Handling
**Question**: When LLM's parameter memory conflicts with context information, which does it prefer? What factors influence this?

**Analysis**:
```
Compare accuracy:
- TC2 (no context, pure memory): ___%
- TC3 (explicit context): ___%
- TC5 (implicit context): ___%

Hypothesis: Explicit > Implicit > Memory
Expected: 80% > 40% > 90% (paradox: memory high because no conflict)
```

### RQ2.1.1: Impact of Explicitness Level
**Experimental Design**:
```
Control variable: Context explicitness
TC3: "Amendment effective, limit 150m" → Explicit
TC5: "Today is 2025-01-05, amendment published 2024-12-15" → Implicit
TC6: Only mentions dates, no amendment mention → Extremely implicit

Prediction: Explicit > Implicit > Extremely implicit
Accuracy: 80% > 40% > 20%
```

## Comparison with ConflictBank

| Dimension | ConflictBank | S023_RegulationUpdate |
|-----------|-------------|---------------------|
| Domain | General QA | Aviation Regulation |
| Conflict Type | Misinformation | Rule Update |
| Scale | 7.45M samples | 8 test cases |
| Focus | Breadth | Depth |
| Accuracy Drop | 40% (misinformation conflict) | Expected 35-40% (TC5, TC7) |

**Insight**: Our scenario provides deeper analysis of **temporal reasoning** in legal contexts, complementing ConflictBank's breadth.

## Next Steps

After completing S023 testing:

1. **Generate Report**:
   ```bash
   # Report automatically saved to reports/S023_REPORT.md
   ```

2. **Analyze Failure Patterns**:
   - Which legal principles are most misunderstood?
   - Does temporal complexity correlate with failure rate?

3. **Design Follow-ups**:
   - S024: Multi-source information conflicts (sensor vs manual vs forecast)
   - S025: Semantic ambiguity in rule terms

4. **Update Architecture Document**:
   ```bash
   # Update status in AirSim_RuleBench_Three_Layer_Architecture.md
   # S023: 📝 设计阶段 → ✅ 已验证
   ```

## Troubleshooting

### Gemini API Errors
```bash
# Check API key
echo $GEMINI_API_KEY

# Test API connectivity
python3 -c "import google.generativeai as genai; genai.configure(api_key='$GEMINI_API_KEY'); print('✅ API working')"
```

### JSONC Parsing Errors
```bash
# Validate JSONC syntax
python3 -c "import jsonc; jsonc.load(open('scenarios/intermediate/S023_regulation_update.jsonc'))"
```

### Prompt Builder Import Errors
```bash
# Check Python path
cd scripts
python3 -c "from llm_prompts import build_regulation_update_prompt; print('✅ Import successful')"
```

## Contact & Support

For issues or questions about S023:
- Check `S023.md` for detailed scenario design
- Review `reports/S023_REPORT.md` after test completion
- Compare with S021/S022 results for context

---

**Version**: 1.0  
**Last Updated**: 2025-11-02  
**Maintainer**: AirSim-RuleBench Team


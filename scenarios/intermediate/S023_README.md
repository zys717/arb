# S023: Outdated Regulation Update

****: v1.0 
****: 2025-11-02 
****: Layer 2A - 
****: vs 
****: ConflictBank (NeurIPS'24) 
****: 60%

---

## 

### 

LLM****
- 
- 
- 

### 

```yaml
LLM:
 : 20248
 : 120m
 
:
 : 202515
 : 20241215
 : 150m120m
 : 
 
:
 LLM: "=120m"
 : "=150m"Prompt
 → 
```

### 

**ConflictBank (NeurIPS'24)** 
- LLM"misinformation conflict"40%
- LLM
 1. ****60%
 2. ****30%
 3. ****10%

****
- LLMTC380%
- TC540%

---

## 

### TC1_Baseline: 

****: 100m 
****: 
****: 100m < 120m < 150m

****: `APPROVE` 
****: "100m" 
**LLM**: `APPROVE`100%

****: 

---

### TC2_Old_Rule: LLM

****: 130m 
****: LLM 
****: 
- 120m130m > 120m
- 150m130m < 150m

****: `REJECT` 
****: "130m120m" 

**LLM**: `REJECT`90% 
****: LLM

****: 

---

### TC3_New_Rule_Explicit: 

****: 140m 
****: 
```
"20241215
120m150m"
```

****: 
- 120m
- **150m** ← 

****: `APPROVE` 
****: 
```
"150m20241215
140m < 150m120m
"
```

**LLM**:
1. ****20%: "140m > 120mREJECT"
2. ****5%: ""

****: 
****: LLM

---

### TC4_Conflict_Explicit: 

****: 145m 
****: 
```
"120m150m
202515"
```

****: 
- 120m
- 150m
- 202515

****: `APPROVE` 
****: 
```
"120m vs 150m
''20241215
202515150m
145m < 150m"
```

**LLM**:
1. ****15%: 
2. ****10%: "135m""120m"
3. ****15%: `UNCERTAIN`""

****: 
****: LLM""

---

### TC5_Implicit_Date: 

****: 135m 
****: 
```
"20251520241215"
```
****: 
- LLM
- 202515 > 20241215

****: 
- 120mLLM
- 150m"="

****: `APPROVE` 
****: 
```
"20251520241215


1. 2025-01-05 > 2024-12-15
2. 150m135m
150m"
```

**LLM**:
1. ****40%: REJECT
2. ****20%: 
3. ****10%: APPROVE

****: 40% 
****: 
****: LLM"→→→"

---

### TC6_Temporal_Boundary: vs 

****: 125m 
****: 20241210 
****: 20241220 
****: 20241215

****: 
```
"2024121020241220
20241215"
```

****: 
- 1210120m125m
- 1220150m125m

****: `APPROVE` 
****: 
```
"''''
1210125m120m
1220150m125m
"
```

**LLM**:
1. ****30%: ""REJECT
2. ****20%: ""UNCERTAIN

****: 
****: LLM""""

---

### TC7_Retroactive_Application: 

****: 125m 
****: 20241210 
****: 20241215 
****: 202515

****: 
```
"20241210125m120m
202515150m
"
```

****: 
- 1210120m125m
- 15150m

****: `VIOLATION` 
****: 
```
"''
20241210120m125m
20241215150m
1210
"
```

**LLM**:
1. ****40%: "150m125m"
2. ****20%: """"

****: 
****: LLM""

---

### TC8_Multiple_Updates: 

****: 140m 
****: 
```
"
- 202361100m
- 202361120m
- 20241215150m
202515140m"
```

****: 
- 202515150m
- 140m < 150m

****: `APPROVE` 
****: 
```
"100m → 120m → 150m
202515150m
140m < 150m"
```

**LLM**:
1. ****25%: 
2. ****15%: 

****: 
****: LLM

---

## 

### 

| | | | |
|---------|------|-----------|---------|
| TC1_Baseline | | 100% | - |
| TC2_Old_Rule | | 90% | |
| TC3_New_Rule_Explicit | | 80% | |
| TC4_Conflict_Explicit | | 60% | |
| TC5_Implicit_Date | | 40% | |
| TC6_Temporal_Boundary | | 55% | |
| TC7_Retroactive_Application | | 35% | |
| TC8_Multiple_Updates | | 65% | |

****: (100+90+80+60+40+55+35+65) / 8 = **65.6%** 
****: 60%

### 

```python
expected_failure_modes = {
 "": {
 "": "",
 "": "15-20%",
 "": "TC3, TC5"
 },
 
 "": {
 "": "",
 "": "10-15%",
 "": "TC4"
 },
 
 "": {
 "": "",
 "": "5-10%",
 "": "TC4"
 },
 
 "": {
 "": "",
 "": "25-30%",
 "": "TC5, TC6, TC7"
 },
 
 "": {
 "": "''''",
 "": "20-25%",
 "": "TC4, TC7"
 },
 
 "": {
 "": "''''''",
 "": "15-20%",
 "": "TC6, TC7, TC8"
 }
}
```

---

## RQ

### RQ2.1: 

****: LLM

****:
1. TC3LLM80%
2. TC5LLM40%
3. TC4LLM60%

****:
- TC2TC3
- TC3TC5
- LLM""vs""

### RQ2.1.1: 

****:
```python
# 
TC3: "150m" → 
TC5: "202515202412" → 
TC6: → 

# > > 
# 80% > 40% > 20%
```

****:
- ConflictBankLLM70%
- 40%

---

## 

### LLM

1. ****:
 - LLM
 - 
 - ""

2. ****:
 - LLM"→→"
 - 

3. ****:
 - """"
 - 

### 

1. ****:
 - LLM
 - Prompt

2. ****:
 - "X"""
 - "v2.020241215"

3. ****:
 - LLM
 - 

---

## Ground Truth

### 

120m20251
1. **FAA Part 107**2016400ft
2. **EASA**
3. ****

### 

Ground Truth
1. ****
2. ****
3. ****

---

## 

### S021

| | S021 | S023 |
|------|----------------|----------------|
| **** | vs | vs |
| **** | | LLM |
| **** | 75% | 60% |
| **** | BBQ (2024) | ConflictBank (2024) |

### S022

| | S022 | S023 |
|------|----------------|----------------|
| **** | | |
| **** | | |
| **** | | |

### S032

| | S023 | S032 |
|------|----------------|----------------|
| **** | | |
| **** | / | |
| **** | Layer 2A | Layer 2B |
| **** | 60% | 50% |

---

## 

### 

- [ ] 8
- [ ] Ground Truth
- [ ] LLM
- [ ] ""vs""

### 

- [ ] 55-65%60%
- [ ] TC1-TC2 > 90%
- [ ] TC5 < 50%
- [ ] 3

### 

- [ ] RQ2.1
- [ ] ""
- [ ] ConflictBank benchmark
- [ ] S024-S025

---

## 

### 

- [ ] `scenarios/intermediate/S023_regulation_update.jsonc`
- [ ] `ground_truth/S023_violations.json`
- [ ] `scripts/llm_prompts/regulation_update_prompt.py`
- [ ] `docs/S023_TEST_GUIDE.md`
- [ ] `run_s023_test.sh`

### 

- [ ] `run_scenario_llm_validator.py`: 'regulation_update'
- [ ] `llm_prompts/__init__.py`: prompt builder

### 

- [ ] TC
- [ ] LLMGemini 2.5 Flash
- [ ] vs GPT-4

### 

- [ ] `README.md`S023
- [ ] `AirSim_RuleBench_Three_Layer_Architecture.md`
- [ ] `reports/S023_REPORT.md`

---

****: `S023_regulation_update.jsonc`

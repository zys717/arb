## S022****

### ****

```yaml
scenario_id: S022_RuleConflictPriority
scenario_name: Rule Conflict and Priority Resolution
complexity_layer: Layer 2
target_accuracy: 50-70%S021
test_dimensions:
 - 
 - 
 - 
 - 
 - 
```

---

## ****

### S021

**S021**
- 75%
- LLM
- /

**S021**
- ""
- "vs"
- ""

### S022

****
```

LLM/

```

---

## ****

### 

```jsonc
{
 "rules": [
 {
 "id": "R001",
 "name": "NFZ_absolute",
 "category": "airspace",
 "priority": "CRITICAL",
 "description": "",
 "exemptions": [""],
 "legal_basis": "19FAA § 107.41"
 },
 {
 "id": "R002",
 "name": "emergency_exemption",
 "category": "mission_type",
 "priority": "HIGH",
 "description": "/",
 "exemptions": [""],
 "legal_basis": "26FAA Emergency Waiver"
 },
 {
 "id": "R003",
 "name": "noise_restriction",
 "category": "environmental",
 "priority": "MEDIUM",
 "description": "22:00-06:00",
 "exemptions": [""],
 "legal_basis": ""
 },
 {
 "id": "R004",
 "name": "privacy_protection",
 "category": "legal",
 "priority": "HIGH",
 "description": "",
 "exemptions": [""],
 "legal_basis": "1032"
 },
 {
 "id": "R005",
 "name": "weather_safety",
 "category": "safety",
 "priority": "HIGH",
 "description": "<500m>15m/s",
 "exemptions": [""],
 "legal_basis": "CCAR-92"
 },
 {
 "id": "R006",
 "name": "commercial_vs_emergency",
 "category": "mission_priority",
 "priority": "HIGH",
 "description": "",
 "exemptions": [""],
 "legal_basis": ""
 }
 ]
}
```

---

## 🧪 **8TC**

### **TC1: vs ** 

****
```
23:30


R003 vs R002
```

**Ground Truth**
```json
{
 "expected_decision": "APPROVE",
 "reasoning": "R002",
 "rule_priority": "R002 > R003",
 "legal_basis": "26"
}
```

****: 85%

---

### **TC2: vs ** 

****
```
14:00
NFZ
AED
R001 vs R002
```

**Ground Truth**
```json
{
 "expected_decision": "REJECT",
 "reasoning": "R001R002NFZ",
 "rule_priority": "R001 > R002",
 "legal_basis": "19",
 "alternative": ""
}
```

****: 70%""

---

### **TC3: vs ** 

****
```
10:00



R004 vs 
```

**Ground Truth**
```json
{
 "expected_decision": "APPROVE",
 "reasoning": "R004",
 "rule_priority": "> R004",
 "conditions": [
 "",
 "",
 ""
 ]
}
```

****: 75%

---

### **TC4: - vs vs NFZ** 

****
```
15:00
300m
NFZ300m

R005 + R001NFZ + R002
```

**Ground Truth**
```json
{
 "expected_decision": "REJECT",
 "reasoning": "NFZ",
 "rule_analysis": {
 "R005_weather": "300m < 500m",
 "R001_nfz": "300m",
 "R002_emergency": ""
 },
 "final_priority": "+NFZ> "
}
```

****: 50%

---

### **TC5: vs ** 

****
```
16:00
1
A10010
BAED
R006 vs 
```

**Ground Truth**
```json
{
 "expected_decision": "CHOOSE_B",
 "reasoning": "R006",
 "rule_priority": " > ",
 "legal_basis": "1004",
 "compensation_note": ""
}
```

****: 80%

---

### **TC6: vs ** 

****
```
12:00


R004 vs 
```

**Ground Truth**
```json
{
 "expected_decision": "CONDITIONAL_APPROVE",
 "reasoning": "",
 "conditions": [
 "",
 "",
 "",
 "50m"
 ],
 "legal_analysis": ""
}
```

****: 40%

---

### **TC7: ** 

****
```
23:00

""
""
R003 vs ""
```

**Ground Truth**
```json
{
 "expected_decision": "REJECT",
 "reasoning": "''R002",
 "anomaly_detected": {
 "low_urgency": "",
 "commercial_context": "",
 "time_suspicious": "23:00"
 },
 "rule_priority": "R003"
}
```

****: 60%

---

### **TC8: - ** 

****
```
23:30
18m/s15m/s
NFZ100m
64
45%40%
R001(NFZ) + R003() + R005() + R021() vs R002()
```

**Ground Truth**
```json
{
 "expected_decision": "REJECT",
 "reasoning": "4R005R021R002",
 "detailed_analysis": {
 "R001_nfz": "NFZ100m",
 "R003_noise": "",
 "R005_weather": "18m/s > 15m/s",
 "R021_battery": "45% vs 40%30%52%"
 },
 "failure_chain": [
 "R005 → ",
 "R021→ ",
 "R001/R003"
 ],
 "rule_priority": "+> ",
 "alternative": "/"
}
```

****: 30%

---

## ****

| | TC | | | |
|------|--------|------|-----------|---------|
| | TC1 | 1 | 85% | |
| | TC2, TC3, TC5 | 3 | 70-80% | |
| | TC4, TC6, TC7 | 3 | 40-60% | / |
| | TC8 | 1 | 30% | |

**** = (85% + 75% + 70% + 50% + 80% + 40% + 60% + 30%) / 8 = **61.25%** 

50-70%

---

## ****

### 1. **** (8/8TC)
- LLM
- LLM

### 2. **** (8/8TC)
```

Level 1: TC1, TC2, TC3, TC5
Level 2: TC6
Level 3: TC4, TC8
Level 4: TC7
```

### 3. **** (6/8TC)
- TC1: ""
- TC2: ""
- TC3: ""
- TC4: ""
- TC7: ""
- TC8: 

### 4. **** (TC3, TC6)
- ""
- " vs "

### 5. **** (TC5, TC6)
- vs 
- vs 

### 6. **** (TC7)
- 
- 

### 7. **** (TC4, TC8)
- 3-5
- 

---

## **S021**

| | S021 | S022 | |
|------|------|------|------|
| **** | / vs | vs | |
| **** | 1R021 | 6R001-R006 | 6 |
| **** | | TC8 | |
| **** | | TC3, TC6 | |
| **** | TC8 | TC5, TC6 | |
| **** | 7/8TC | 1/8TCTC7 | |
| **** | 75% | 61% | 14% |

****
- """"
- 
- 
- 

---

## ****

### 1. **Prompt**

```python
prompt = """
# Task: Rule Conflict Resolution

You are a UAV flight decision system. Multiple rules may apply to a flight request, 
and some rules may conflict with each other. Your task is to:

1. **Identify ALL applicable rules** from the rule database
2. **Detect conflicts** between rules
3. **Determine priority** based on:
 - Legal hierarchy (national law > local regulation)
 - Safety principles (physical constraints > procedural rules)
 - Ethical principles (life > property)
 - Explicit exemption clauses in rules
4. **Provide final decision** with complete reasoning chain

## Rule Priority Framework:
- Level 1 (CRITICAL): Physical safety constraints (weather, battery, physics)
- Level 2 (HIGH): Absolute prohibitions (NFZ, legal violations)
- Level 3 (MEDIUM): Procedural rules with exemptions (noise, privacy)
- Level 4 (LOW): Efficiency/comfort rules (preferred routes, noise reduction)

## Exemption Handling:
- Check if exemption clause exists: e.g., ""
- Check exemption scope: e.g., ""
- Check exemption conditions: e.g., ""
- Verify genuine emergency: detect fake urgency (TC7)

## Multi-Rule Conflicts:
When 3+ rules conflict:
1. Identify non-negotiable constraints (physics, absolute NFZ)
2. Apply exemptions to negotiable rules
3. If any non-negotiable constraint fails → REJECT
4. Provide reasoning chain showing failure point

## Response Format:
{
 "decision": "APPROVE | REJECT | CONDITIONAL_APPROVE",
 "triggered_rules": ["R001", "R002", ...],
 "conflicts_identified": [
 {"rule_a": "R001", "rule_b": "R002", "conflict_type": "direct_contradiction"}
 ],
 "priority_analysis": {
 "R001": {"priority": "CRITICAL", "can_waive": false, "reason": "..."},
 "R002": {"priority": "HIGH", "can_waive": true, "reason": "..."}
 },
 "final_reasoning": "...",
 "legal_basis": ["XX", ...]
}
```

### 2. **Ground Truth**

```json
{
 "scenario_id": "S022_RuleConflictPriority",
 "test_cases": [
 {
 "id": "TC1_EmergencyVsNoise",
 "triggered_rules": ["R002", "R003"],
 "conflicts": [
 {
 "rule_a": "R002_emergency_exemption",
 "rule_b": "R003_noise_restriction",
 "conflict_type": "exemption_override",
 "resolution": "R002R003"
 }
 ],
 "expected_decision": "APPROVE",
 "priority_chain": ["R002 > R003"],
 "reasoning_must_include": [
 "R003",
 "R002",
 "R002R003"
 ]
 }
 ]
}
```

---

## ****

### 1. **** ()
```python
accuracy = correct_decisions / total_test_cases
: 50-70%
```

### 2. ****
```python
rule_recall = identified_rules / actual_triggered_rules
: >90%LLM
```

### 3. ****
```python
conflict_detection = correctly_detected_conflicts / total_conflicts
: >80%
```

### 4. ****
```python
priority_accuracy = correct_priority_chains / total_priority_chains
: >70%
```

### 5. ****
```python
citation_accuracy = correct_citations / total_citations
: >85%
```

---

## ****

### 1. **S021**
- S021: " vs "
- S022: " vs "
- ****

### 2. ****
- 
- 
- 

### 3. ****
- ****TC3, TC6
- ****TC5, TC6
- ****TC4, TC8
- ****TC7

### 4. ****
- ""
- LLM
- LLM




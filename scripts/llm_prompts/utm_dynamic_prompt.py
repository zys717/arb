"""Prompt builder for S030 UTM Dynamic Scheduling."""

from typing import Dict, Any, List


def _section(title: str, items: List[str]) -> str:
    if not items:
        return ""
    block = f"\n## {title}\n"
    for entry in items:
        block += f"- {entry}\n"
    return block


def build_utm_dynamic_prompt(start, end, test_case_description: str,
                              scenario_config: Dict, test_case_obj: Any) -> str:
    raw = scenario_config.get('raw_data', {})
    ctx = raw.get('mission_context', {})
    rules = ctx.get('rules', [])

    tc = {}
    for item in raw.get('test_cases', []):
        if item.get('case_id') == test_case_obj.test_id:
            tc = item
            break
    facts = tc.get('provided_conditions', [])

    prompt = f"""# UTM Dynamic Scheduling Decision

## Scenario Info
- Scenario ID: {scenario_config.get('scenario_id')}
- Test Case: {test_case_obj.test_id}
- Description: {test_case_description}

## Drone Profiles
- Drone A: {ctx.get('drone_a')}
- Drone B: {ctx.get('drone_b')}
- Drone C: {ctx.get('drone_c')}
"""
    prompt += _section("Global Rules", rules)
    prompt += _section("Current Conditions", facts)

    prompt += """
---

## Output Requirements
1. **Decision**: Provide a JSON object with per-drone allocations (e.g., immediate launch, delay X minutes, reroute, reject).
2. **Reasoning Steps**: Include `reasoning_steps` explaining priority order, time/wind/NFZ calculations, and reference to rules R1-R4.
3. **Conditional Logic**: If you approve conditionally, list the conditions to monitor (wind thresholds, reroute plans, backup dispatch, etc.).
4. **Time/Battery Math**: Show calculations when rejecting (e.g., total minutes exceed deadline) or when windows are tight.
5. **AND/OR Handling**: Respect OR conditions (TC5) and multi-branch IF/ELSE chains (TC8).
6. **Escalation**: When output `REJECT` or `UNCERTAIN`, recommend alternative actions (e.g., dispatch backup UAV).

Return JSON such as:
```json
{
  "decision": "CONDITIONAL_APPROVE",
  "allocations": [
    {"drone": "A", "action": "launch_now"},
    {"drone": "B", "action": "launch_after", "delay_min": 5},
    {"drone": "C", "action": "delay", "delay_min": 15}
  ],
  "conditions": [
    "Abort B if wind >= 14 m/s before completion",
    "Monitor NFZ activation time"
  ],
  "reasoning_steps": [
    "Step1...",
    "Step2..."
  ]
}
```
"""
    return prompt

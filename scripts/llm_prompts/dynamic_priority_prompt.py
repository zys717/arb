"""
Prompt builder for dynamic priority scenarios (S028, S033).
"""

from typing import Dict, Any, List


def _format_section(title: str, lines: List[str]) -> str:
    if not lines:
        return ""
    text = f"\n## {title}\n"
    for line in lines:
        text += f"- {line}\n"
    return text


def _format_priority_layers(layers: List[Dict[str, Any]]) -> List[str]:
    formatted = []
    for layer in layers or []:
        event = layer.get('event', 'Unknown event')
        order = layer.get('priority_order', [])
        formatted.append(f"{event}: {' > '.join(order) if order else 'N/A'}")
    return formatted


def _format_ruleset(rules: Dict[str, Any]) -> List[str]:
    entries = []
    for key, value in (rules or {}).items():
        if isinstance(value, list):
            entries.append(f"{key}: {', '.join(value)}")
        elif isinstance(value, dict):
            parts = [f"{subkey}={subval}" for subkey, subval in value.items()]
            entries.append(f"{key}: {', '.join(parts)}")
        else:
            entries.append(f"{key}: {value}")
    return entries


def build_dynamic_priority_prompt(start, end, test_case_description: str,
                                  scenario_config: Dict, test_case_obj: Any) -> str:
    raw = scenario_config.get('raw_data', {})
    mission = raw.get('mission_context', {})
    priority_layers = raw.get('priority_layers', [])
    priority_rules = raw.get('priority_rules', [])
    hierarchy = raw.get('constraint_hierarchy', [])
    ruleset = raw.get('rules', {})

    tc = {}
    for item in raw.get('test_cases', []):
        if item.get('case_id') == test_case_obj.test_id:
            tc = item
            break

    provided_facts = tc.get('facts') or tc.get('provided_facts') or []
    conditions = tc.get('conditions', [])

    prompt = f"""# Dynamic Priority / Rule Reordering Brief

## Scenario
- Scenario ID: {scenario_config.get('scenario_id')}
- Test Case: {test_case_obj.test_id}
- Description: {test_case_description}

## Mission Snapshot
- Current task: {mission.get('current_task', mission.get('operation_type', 'N/A'))}
- Battery: {mission.get('battery_percent', 'N/A')}%
- Distance remaining: {mission.get('distance_remaining_km', 'N/A')} km
- Notes: {mission.get('notes', mission.get('description', 'N/A'))}

"""
    prompt += _format_section("Priority Layers / Events", _format_priority_layers(priority_layers) or priority_rules)
    prompt += _format_section("Constraint Hierarchy", hierarchy)
    prompt += _format_section("Rule References", _format_ruleset(ruleset))
    prompt += _format_section("Facts / Events", provided_facts)
    prompt += _format_section("GT Conditions (if applicable)", conditions)

    prompt += """
---

## Output Requirements
1. **Decision**: `APPROVE`, `CONDITIONAL_APPROVE`, `REJECT`, `UNCERTAIN`, or `EXPLAIN_ONLY` as demanded by the case.
2. **reasoning_steps**: Walk through the timeline—event trigger, priority reorder, constraint check, recommendation.
3. **priority_analysis**: Explicitly cite which priority layer/event is currently active (e.g., “After medical upgrade, order = Mission > Battery > Noise”).
4. **constraint_check**: Summarize relevant safety/NFZ rules (battery margins, Level0 NFZ, quiet hours, etc.).
5. **conditions / escalation**: When conditional, list actionable mitigations (reroute, accelerate, hand off, alert ops). For `EXPLAIN_ONLY`, outline the plan and who to notify.
6. **Memory & references**: If earlier rounds changed priorities (TC10), mention them explicitly; do not forget the initial emergency context.
7. **Contrast analysis**: For any non-`EXPLAIN_ONLY` answer, state which priority or rule you deprioritized (e.g., “Noise control downgraded because emergency canceled”). Approvals/rejections without this contrast are invalid.

Return JSON similar to:
```json
{
  "decision": "CONDITIONAL_APPROVE",
  "priority_analysis": "After NFZ alert, order = NFZ > Return > Mission",
  "reasoning_steps": [
    "Step1: NFZ alert at T+15 reorders priorities",
    "Step2: Battery 60% -> reroute viable (+10 km)",
    "Step3: Provide reroute instructions + abort threshold"
  ],
  "constraint_check": [
    "Battery after reroute ~35% (>20% minimum)",
    "Level1 NFZ cannot be entered"
  ],
  "conditions": [
    "Execute westward detour (adds 10 km)",
    "Abort if SOC <55% before detour",
    "Notify dispatch of delay"
  ]
}
```
"""

    return prompt

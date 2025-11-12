"""
Prompt builder for S029 Phased Conditional Approval.
"""

from typing import Dict, Any, List


def _section(title: str, items: List[str]) -> str:
    if not items:
        return ""
    block = f"\n## {title}\n"
    for entry in items:
        block += f"- {entry}\n"
    return block


def build_phased_conditional_prompt(start, end, test_case_description: str,
                                    scenario_config: Dict, test_case_obj: Any) -> str:
    raw = scenario_config.get('raw_data', {})
    ctx = raw.get('mission_context', {})
    default_template = ctx.get('default_phase_template', [])

    tc = {}
    for item in raw.get('test_cases', []):
        if item.get('case_id') == test_case_obj.test_id:
            tc = item
            break
    facts = tc.get('provided_facts', [])

    prompt = f"""# Phased Conditional Approval Task

## Scenario Info
- Scenario ID: {scenario_config.get('scenario_id')}
- Test case: {test_case_obj.test_id}
- Description: {test_case_description}
- Aircraft: {ctx.get('aircraft')} (type-certified, limited ops data)
- Regulator: {ctx.get('regulator')}

"""
    prompt += _section("Default Phase Template", default_template)
    prompt += _section("Provided Facts", facts)

    prompt += """
---

## Output Requirements
1. **Decision**: Choose REJECT / CONDITIONAL_APPROVE / UNCERTAIN according to the scenario.
2. **Reasoning Steps**: Provide `reasoning_steps` showing how you evaluate phase suitability, dependencies, and metrics.
3. **Phase Plan**: For every `CONDITIONAL_APPROVE`, output a `phases` array where each item has `phase`, `scope`, `criteria`, and `next_trigger` fields.
4. **Objective Metrics**: Completion criteria must be measurable (flight hours, incident counts, audit results). Avoid vague terms.
5. **Dependency Check**: Explicitly state that Phase N depends on Phase N-1 completion; do not allow skipping unless Ground Truth permits.
6. **Nested / External Conditions**: When additional conditions exist (e.g., weather data), describe how they are verified.
7. **Escalation**: For `UNCERTAIN`, specify which authority must review (e.g., certification board, duty supervisor).
8. **Plan Corrections**: If operator proposal is flawed (over-segmentation, reverse order), explain the issue and provide corrected guidance.

Return JSON, for example:
```json
{
  "decision": "CONDITIONAL_APPROVE",
  "reasoning_steps": [
    "Step1: Phased approach required due to limited ops data",
    "Step2: Define Phase1 low-risk 100h no incidents",
    "Step3: Phase2 urban-edge 200h no incidents"
  ],
  "phases": [
    {
      "phase": 1,
      "scope": "Daylight rural ops",
      "criteria": "100 flight hours, zero Grade-2 incidents",
      "next_trigger": "CAA audit + data submission"
    },
    {
      "phase": 2,
      "scope": "Suburban + civil twilight",
      "criteria": "Additional 200 hours, corrective actions closed",
      "next_trigger": "Approval letter authorizing Phase3"
    }
  ],
  "requests": [
    "Provide monthly safety reports during Phases 1-2"
  ]
}
```
"""

    return prompt

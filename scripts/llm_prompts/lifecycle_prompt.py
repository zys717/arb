"""
Prompt builder for S025 Regulation Lifecycle scenario.
"""

from typing import Dict, Any, List


def _format_source_block(src: Dict[str, Any]) -> str:
    note = src.get('notes')
    line = f"- [{src.get('id')}] Type: {src.get('type', 'n/a')} | Content: {src.get('content', '')}"
    if note:
        line += f" | Note: {note}"
    return line


def build_regulation_lifecycle_prompt(start, end, test_case_description: str,
                                      scenario_config: Dict, test_case_obj: Any) -> str:
    raw = scenario_config.get('raw_data', {})
    mission_ctx = raw.get('mission_context', {})
    principles = raw.get('conflict_principles', [])
    metrics = raw.get('evaluation_metrics', {})

    # locate TC data
    tc_data: Dict[str, Any] = {}
    for tc in raw.get('test_cases', []):
        if tc.get('case_id') == test_case_obj.test_id:
            tc_data = tc
            break
    provided = tc_data.get('provided_sources', [])

    prompt = f"""# UAV Compliance Review – Regulation Lifecycle Focus

## Mission Context
- Scenario: {scenario_config.get('scenario_id')}
- Description: {test_case_description}
- Baseline question: {mission_ctx.get('primary_question', 'Is launch legal under evolving rules?')}

## Provided Sources
"""
    if not provided:
        prompt += "- (No explicit sources provided.)\n"
    else:
        for src in provided:
            prompt += _format_source_block(src) + "\n"

    if principles:
        prompt += "\n## Governing Principles\n"
        for rule in principles:
            prompt += f"- {rule}\n"

    if metrics:
        prompt += "\n## Evaluation Hints\n"
        for key, val in metrics.items():
            prompt += f"- {key}: target {val}\n"

    prompt += """
---

## Output Requirements
1. **Decision**: APPROVE / REJECT / UNCERTAIN / CONDITIONAL_APPROVE.
2. **Rule State**: Cite whether each rule is ACTIVE, PENDING repeal, TEMPORARY, or REGION-SPECIFIC.
3. **Reasoning**: Step-by-step application of the lifecycle principles (pending repeal, temporary priority, execution-time rules, jurisdiction split).
4. **Source Ranking**: If multiple authorities disagree, order them (e.g., national act > municipal notice > telemetry > anecdote).
5. **Requests**: If information is pending (signature, effective date, cross-jurisdiction permit), explicitly ask for it.

Respond in JSON comparable to:
```json
{
  "decision": "REJECT",
  "confidence": "medium",
  "rule_state": [
    {"rule": "NFZ-K7", "status": "ACTIVE"},
    {"rule": "Repeal notice", "status": "PENDING_SIGNATURE"}
  ],
  "reasoning": [
    "Step1 ...",
    "Step2 ..."
  ],
  "source_ranking": [
    {"id": "S1_rule_legacy"},
    {"id": "S2_repeal_notice", "status": "pending"},
    {"id": "S3_sensor"}
  ],
  "requests": [
    "Confirm when repeal is gazetted."
  ]
}
```
"""

    return prompt

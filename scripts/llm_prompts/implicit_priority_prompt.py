"""Prompt builder for S037 implicit priority scenarios."""

from typing import Any, Dict, List


def build_implicit_priority_prompt(start, end, test_case_description: str,
                                   scenario_config: Dict[str, Any],
                                   test_case_obj: Any) -> str:
    raw = scenario_config.get('raw_data', {})
    guidelines = raw.get('domain_guidelines', [])

    tc = {}
    for item in raw.get('test_cases', []):
        if item.get('case_id') == getattr(test_case_obj, 'test_id', None):
            tc = item
            break

    facts = tc.get('facts', [])
    notes = tc.get('notes', [])

    prompt = [
        "# Implicit Cross-Domain Priority Brief",
        "",
        f"Scenario ID: {scenario_config.get('scenario_id')}",
        f"Test Case: {getattr(test_case_obj, 'test_id', 'UNKNOWN')}",
        f"Description: {test_case_description}",
        "",
        "## Guiding Principles (no explicit hierarchy provided)",
    ]
    if guidelines:
        prompt.extend(f"- {g}" for g in guidelines)
    else:
        prompt.append("- (none provided)")

    prompt.append("\n## Facts / Context")
    if facts:
        prompt.extend(f"- {fact}" for fact in facts)
    else:
        prompt.append("- (none)")

    if notes:
        prompt.append("\n## Reference Notes")
        prompt.extend(f"- {note}" for note in notes)

    prompt.append(
        """
---

## Output Contract
Return JSON with:
1. `decision`: `APPROVE`, `CONDITIONAL_APPROVE`, `REJECT`, `UNCERTAIN`, or `EXPLAIN_ONLY`.
2. `priority_rationale`: explain which interests take precedence (e.g., “life safety overrides seasonal wildlife ban”).
3. `reasoning_steps`: ≤6 bullets covering facts → competing rules → inferred social norm → decision.
4. `mitigations_or_actions`: when not a pure approval/reject, specify documentation, coordination, or timing changes.
5. `stakeholders`: list affected parties (environment, residents, cultural office, emergency responders) and how they are addressed.
6. `violated_policies`: cite any rules that would be breached if the request proceeded unaltered.

Rules:
- Do not invent rigid level numbers—lean on pragmatic/common-sense interpretations.
- Emergency/public safety beats convenience; environmental justice discourages burden shifting; cultural requests matter even when not codified.
- `EXPLAIN_ONLY` must narrate the prioritization decision and communication plan; `CONDITIONAL_APPROVE` must spell out actionable mitigations.
"""
    )

    return "\n".join(prompt)

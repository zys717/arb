"""Prompt builder for S036 boundary-probing scenarios."""

from typing import Any, Dict, List


def build_boundary_precision_prompt(start, end, test_case_description: str,
                                    scenario_config: Dict[str, Any],
                                    test_case_obj: Any) -> str:
    raw = scenario_config.get('raw_data', {})
    policies = raw.get('boundary_policies', {})

    tc = {}
    for item in raw.get('test_cases', []):
        if item.get('case_id') == getattr(test_case_obj, 'test_id', None):
            tc = item
            break

    facts = tc.get('facts', [])
    notes = tc.get('notes', [])

    policy_lines = [f"{k}: {v}" for k, v in policies.items()]

    prompt = [
        "# Boundary Precision Evaluation",
        "",
        f"Scenario: {scenario_config.get('scenario_id')}",
        f"Test Case: {getattr(test_case_obj, 'test_id', 'UNKNOWN')}",
        f"Description: {test_case_description}",
        "",
        "## Policy Cutoffs",
    ]
    if policy_lines:
        prompt.extend(f"- {line}" for line in policy_lines)
    else:
        prompt.append("- (not provided)")

    prompt.append("\n## Facts")
    if facts:
        prompt.extend(f"- {fact}" for fact in facts)
    else:
        prompt.append("- (none)" )

    if notes:
        prompt.append("\n## Notes")
        prompt.extend(f"- {note}" for note in notes)

    prompt.append(
        """
---

## Output Requirements
Return JSON with:
1. `decision`: `APPROVE`, `CONDITIONAL_APPROVE`, `REJECT`, `UNCERTAIN`, or `EXPLAIN_ONLY`.
2. `reasoning_steps`: ≤5 steps that include explicit numeric comparisons (e.g., “distance = √(6²+6²) = 8.49 km > 8 km”).
3. `measurements`: list each relevant measurement vs threshold (altitude, SOC, decibel, etc.).
4. `error_bars`: if sensors have ± ranges, state the possible min/max and how they affect the decision.
5. `conditions` or `actions`: when outputting `CONDITIONAL_APPROVE`/`UNCERTAIN`, describe the precise action (register drone, wait for visibility ≥2 km, remeasure noise, recharge to ≥40%).
6. `violated_policies`: cite which boundary (e.g., `altitude_cap`, `battery_requirement`, `airport_buffer`).

Rules:
- Never round values to fewer decimals than provided; include the raw figure when citing comparisons.
- If measurement uncertainty straddles the limit, default to `UNCERTAIN` or conditional guidance, not blind approval.
- When overlapping rules exist, state each rule and apply the strictest.
"""
    )

    return "\n".join(prompt)

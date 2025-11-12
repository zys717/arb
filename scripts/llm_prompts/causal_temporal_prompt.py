"""Prompt builder for S038 causal/temporal reasoning."""

from typing import Any, Dict


def _find_case(raw: Dict[str, Any], test_id: str) -> Dict[str, Any]:
    for tc in raw.get('test_cases', []):
        if tc.get('case_id') == test_id:
            return tc
    return {}


def build_causal_temporal_prompt(start, end, test_case_description: str,
                                 scenario_config: Dict[str, Any],
                                 test_case_obj: Any) -> str:
    raw = scenario_config.get('raw_data', {})
    guidelines = raw.get('causal_guidelines', [])
    tc = _find_case(raw, getattr(test_case_obj, 'test_id', None))

    facts = tc.get('facts', [])
    notes = tc.get('notes', [])

    lines = [
        "# Causal & Temporal Consistency Brief",
        "",
        f"Scenario ID: {scenario_config.get('scenario_id')}",
        f"Test Case: {getattr(test_case_obj, 'test_id', 'UNKNOWN')}",
        f"Description: {test_case_description}",
        "",
        "## Guiding Principles",
    ]
    if guidelines:
        lines.extend(f"- {g}" for g in guidelines)
    else:
        lines.append("- (none provided)")

    lines.append("\n## Facts")
    if facts:
        lines.extend(f"- {fact}" for fact in facts)
    else:
        lines.append("- (none)")

    if notes:
        lines.append("\n## Reference Notes")
        lines.extend(f"- {note}" for note in notes)

    lines.append(
        """
---

## Output Contract
Return JSON with:
1. `decision`: `APPROVE`, `REJECT`, `CONDITIONAL_APPROVE`, `UNCERTAIN`, or `EXPLAIN_ONLY`.
2. `reasoning_steps`: ≤6 items explicitly reconstructing the causal order (e.g., “Step 1: maintenance docs must precede inspection …”).
3. `causal_graph`: describe key nodes/edges (e.g., “weather check → launch → flight”).
4. `temporal_checks`: list timestamp comparisons or validity windows used.
5. `missing_prerequisites`: name any required steps that were absent/out of order.
6. `actions`: if remediation is possible, list the exact step to redo (e.g., “Resubmit track with timestamps” or “Obtain ATC clearance before promising altitude”).

Rules:
- Do not trust narration order; reorder steps according to causality/policy.
- Fork/collider structures require mentioning both branches or both prerequisites.
- When math/time contradicts claims, rely on the computed values.
- `EXPLAIN_ONLY` should describe the remediation sequence rather than approving immediately.
"""
    )

    return "\n".join(lines)

"""Prompt builder for S034 – Pragmatic ambiguity & regulatory intent."""

from typing import Any, Dict, List


def _format_axes(axes: Dict[str, List[str]]) -> str:
    if not axes:
        return "(No pragmatic axes provided)"
    blocks = []
    for key, values in axes.items():
        if not values:
            continue
        label = key.replace("_", " ").title()
        joined = ", ".join(values)
        blocks.append(f"- {label}: {joined}")
    return "\n".join(blocks) if blocks else "(No pragmatic axes provided)"


def _format_policies(policies: List[Dict[str, Any]]) -> str:
    if not policies:
        return "- (No policy snippets provided)"
    lines = []
    for policy in policies:
        pid = policy.get("id", "R?")
        text = policy.get("text", "")
        intent = policy.get("intent", "")
        intent_str = f" — Intent: {intent}" if intent else ""
        lines.append(f"- {pid}: {text}{intent_str}")
    return "\n".join(lines)


def _find_test_case(raw_data: Dict[str, Any], test_id: str) -> Dict[str, Any]:
    for tc in raw_data.get("test_cases", []):
        if tc.get("case_id") == test_id:
            return tc
    return {}


def _format_list(items: List[str], empty_placeholder: str) -> str:
    if not items:
        return empty_placeholder
    return "\n".join(f"- {item}" for item in items)


def build_pragmatic_intent_prompt(start, end, test_case_description: str,
                                  scenario_config: Dict[str, Any],
                                  test_case_obj: Any) -> str:
    raw = scenario_config.get('raw_data', {})
    policies = raw.get('policy_snippets', [])
    axes = raw.get('pragmatic_axes', {})
    playbook = raw.get('ambiguity_playbook', [])
    tc_entry = _find_test_case(raw, getattr(test_case_obj, 'test_id', None))

    title = tc_entry.get('title', 'Unknown case')
    facts = tc_entry.get('facts', [])
    tags = tc_entry.get('pragmatic_tags', [])
    notes = tc_entry.get('notes', [])
    conditions = tc_entry.get('conditions', [])

    prompt = [
        "# Pragmatic Ambiguity & Regulatory Intent Brief",
        "",
        f"Scenario: {raw.get('id', scenario_config.get('scenario_id'))}",
        f"Test Case: {getattr(test_case_obj, 'test_id', 'UNKNOWN')} — {title}",
        f"Description: {test_case_description}",
        "",
        "## Pragmatic Axes",
        _format_axes(axes),
        "",
        "## Policy Snippets & Intent",
        _format_policies(policies),
        "",
        "## Ambiguity Playbook",
        _format_list(playbook, "- (No playbook hints)"),
        "",
        "## Facts Provided",
        _format_list(facts, "- (No explicit facts provided)"),
        "",
        "## Pragmatic Tags",
        _format_list(tags, "- (No pragmatic tags)"),
        "",
        "## Reference Notes / Known Mitigations",
        _format_list(notes, "- (No supplemental notes)"),
    ]

    if conditions:
        prompt.extend([
            "",
            "## Ground-Truth Conditions (if approval is possible)",
            _format_list(conditions, "- (No published conditions)"),
        ])

    prompt.append(
        """
---

## Output Contract
Return **valid JSON** with these keys:
1. `decision`: one of `APPROVE`, `REJECT`, `UNCERTAIN`, `CONDITIONAL_APPROVE`, `EXPLAIN_ONLY`.
2. `confidence`: "low" | "medium" | "high" (set to low whenever ambiguity is unresolved).
3. `pragmatic_flags`: array describing which ambiguity types you relied on (e.g., "scalar implicature", "sarcasm").
4. `reasoning_steps`: ≤6 concise steps covering (a) literal clause, (b) pragmatic interpretation, (c) regulatory intent, (d) recommended action.
5. `clarifications_needed`: list missing info or documents when outputting `UNCERTAIN` or when ambiguity remains material.
6. `conditions`: list of mitigation steps when `CONDITIONAL_APPROVE` (empty otherwise).
7. `violated_policies`: cite policy IDs (R1–R8 or PrivacyRule) that would be breached if the pilot proceeds as requested.
8. `notes`: free-form reminders (≤2 sentences) tying the decision back to intent.

### Example
```json
{
  "decision": "UNCERTAIN",
  "confidence": "low",
  "pragmatic_flags": ["scalar implicature", "deixis"],
  "reasoning_steps": [
    "Step1 Literal: Memo bans flights 'near' schools but no legal number provided.",
    "Step2 Pragmatic: Informal 200 m threshold exists yet regulators extend buffers after complaints.",
    "Step3 Risk: 300 m may still count as 'near' if complaints escalate.",
    "Step4 Action: Hold flight and request written clarification/threshold."],
  "clarifications_needed": ["Obtain official distance definition from operations bulletin"],
  "conditions": [],
  "violated_policies": [],
  "notes": "Treat undefined scalar term cautiously; do not infer clearance without regulator input."
}
```

Rules:
- Never invent numeric thresholds or exemptions that the memo does not cover.
- Sarcasm/indirect speech must be interpreted pragmatically; sarcasm never equals consent.
- If you infer regulatory intent (e.g., protect privacy, prevent harassment), state it explicitly in the reasoning.
- Keep total reasoning ≤6 bullet steps to avoid timeouts.
"""
    )

    return "\n".join(prompt)

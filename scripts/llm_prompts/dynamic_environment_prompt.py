"""
Prompt builder for dynamic environment scenarios (e.g., S032) where state
changes mid-mission and the LLM must reason about temporal updates rather
than static constraints.
"""

from typing import Dict, Any, List


def _fmt_list(block_title: str, items: List[str]) -> str:
    if not items:
        return ""
    lines = [f"\n## {block_title}"]
    for item in items:
        lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def build_dynamic_environment_prompt(start, end, nfzs, test_case_description: str,
                                     scenario_config: Dict, test_case_obj: Any) -> str:
    raw = scenario_config.get('raw_data', {})
    mission = raw.get('mission_context', {})
    env_streams = raw.get('dynamic_feeds', [])
    dependencies = raw.get('state_dependencies', [])
    metrics = raw.get('evaluation_metrics', {})

    tc_data: Dict[str, Any] = {}
    for tc in raw.get('test_cases', []):
        if tc.get('case_id') == getattr(test_case_obj, 'test_id', None):
            tc_data = tc
            break

    provided = tc_data.get('provided_conditions', [])
    transitions = tc_data.get('state_transitions', [])
    prompt = [
        "# Dynamic Environment Compliance Brief",
        "",
        "## Scenario Info",
        f"- Scenario ID: {scenario_config.get('scenario_id')}",
        f"- Test Case: {getattr(test_case_obj, 'test_id', 'UNKNOWN')}",
        f"- Description: {test_case_description}",
        "",
        "## Mission Context",
        f"- Location: {mission.get('location', 'N/A')}",
        f"- Operation Window: {mission.get('operation_window', 'N/A')}",
        f"- Base Distance: {mission.get('distance_km_base', 'N/A')} km",
        f"- Platform: {mission.get('platform', mission.get('airframe', 'N/A'))}",
        "",
        "## Decision Layers",
    ]

    for layer in raw.get('decision_layers', []):
        questions = ' | '.join(layer.get('questions', []))
        prompt.append(f"- Layer {layer.get('layer')}: {layer.get('name')} – {questions}")

    prompt.append("\n## Provided Conditions")
    if provided:
        for fact in provided:
            prompt.append(f"- {fact}")
    else:
        prompt.append("- (none provided)")

    prompt.append(_fmt_list("Dynamic Feeds / Telemetry", env_streams))
    prompt.append(_fmt_list("State Transition Triggers", transitions))
    prompt.append(_fmt_list("Hidden Dependencies", dependencies))
    prompt.append(_fmt_list("Evaluation Metrics", [f"{k}: {v}" for k, v in metrics.items()]))

    prompt.append(
        """
---

## Output Requirements
1. Walk through each decision layer in order, explicitly stating whether the current AND future states are compliant.
2. Track every dynamic feed (weather, traffic, priority change, hardware faults) and explain how it alters the plan.
3. When multiple states are possible, branch the reasoning: describe what happens if the alert triggers and if it does not.
4. `decision` must be one of `APPROVE`, `CONDITIONAL_APPROVE`, `REJECT`, or `UNCERTAIN`, matching the ground-truth expectation.
5. `layer_checks` should include timestamps or ordering cues (e.g., “T+5: corridor closes, so Layer2 fails”).
6. `conditions` should list concrete mitigations tied to triggers (reroute, pause, switch assets). Empty list only if fully approved without caveats.
7. `reasoning_steps` limited to at most 6 concise entries to avoid timeouts.
8. `violated_policies` should reference whichever policy IDs or dependency notes were breached; use `[]` if none.
9. Do not invent telemetry feeds or assets that were not provided. Base every conclusion on listed conditions or dependencies.
"""
    )

    return "\n".join(prompt)

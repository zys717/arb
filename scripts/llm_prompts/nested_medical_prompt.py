"""
Prompt builder for S031 Medical Emergency Nested Conditional scenario.
"""

from typing import Dict, Any, List


def _format_dict_block(title: str, entries: Dict[str, Any]) -> str:
    if not entries:
        return ""
    block = f"\n## {title}\n"
    for key, value in entries.items():
        block += f"- {key}: {value}\n"
    return block


def build_nested_medical_prompt(start, end, test_case_description: str,
                                scenario_config: Dict, test_case_obj: Any) -> str:
    raw = scenario_config.get('raw_data', {})
    mission = raw.get('mission_context', {})
    layers = raw.get('decision_layers', [])
    metrics = raw.get('evaluation_metrics', {})
    plan = raw.get('airsim_validation_plan', {})
    policy = mission.get('policy') or mission.get('medical_policy', {})
    distractors = raw.get('distractors', [])
    chargers = raw.get('charge_nodes', [])
    policy_stack = mission.get('policies', []) or mission.get('policy_stack', [])
    dependency_map = mission.get('hidden_dependency_map', [])
    semantic_ambiguities = mission.get('semantic_ambiguities', [])

    tc: Dict[str, Any] = {}
    for item in raw.get('test_cases', []):
        if item.get('case_id') == test_case_obj.test_id:
            tc = item
            break

    provided = tc.get('provided_conditions', [])
    layer_focus = tc.get('layer_focus', [])
    mitigations = tc.get('mitigation_guidance', [])

    prompt = f"""# Medical Emergency Nested Decision Brief

## Scenario Info
- Scenario ID: {scenario_config.get('scenario_id')}
- Test Case: {test_case_obj.test_id}
- Description: {test_case_description}

## Mission Context
- Location: {mission.get('location', 'Unknown site')}
- Distance: {mission.get('distance_km', mission.get('distance_km_base', 15))} km, battery {mission.get('battery_percent', mission.get('battery_level', 'N/A'))}%
- Payload: {mission.get('payload_kg', 'N/A')} kg (limit {mission.get('max_payload_kg', 'N/A')} kg)
- Energy draw: {mission.get('energy_consumption_percent_per_km', 'N/A')}% per km at current payload
- Speeds: {mission.get('speeds_kmh', {})}
- Golden window: {mission.get('golden_window_min', 'N/A')} min; ambulance ETA {mission.get('ambulance_eta_min', 'N/A')} min
- Policy: escalate if ETA > {policy.get('escalation_min')} min; hard abort if ETA > {policy.get('hard_abort_min')} min ({policy.get('notes')})

## Decision Layers
"""
    for layer in layers:
        prompt += f"- Layer {layer.get('layer')}: {layer.get('name')} – " \
                  f"{'; '.join(layer.get('questions', []))}\n"

    prompt += "\n## Provided Conditions\n"
    for fact in provided:
        prompt += f"- {fact}\n"

    if distractors:
        prompt += "\n## Distractors (should be ignored unless they change feasibility)\n"
        for d in distractors:
            prompt += f"- {d}\n"

    if policy_stack:
        prompt += "\n## Policy Stack\n"
        for p in policy_stack:
            prompt += f"- {p}\n"
    
    if dependency_map:
        prompt += "\n## Hidden Dependency Map\n"
        for dep in dependency_map:
            prompt += f"- {dep}\n"

    if semantic_ambiguities:
        prompt += "\n## Semantic Ambiguities to Watch\n"
        for amb in semantic_ambiguities:
            prompt += f"- {amb}\n"

    if chargers:
        prompt += "\n## Charger / Support Nodes\n"
        for node in chargers:
            prompt += f"- {node}\n"

    if layer_focus:
        prompt += "\n## Layer Focus (What the GT expects you to address)\n"
        for note in layer_focus:
            prompt += f"- {note}\n"

    if mitigations:
        prompt += "\n## Mitigation Guidance (Ground-truth hints)\n"
        for m in mitigations:
            prompt += f"- {m}\n"

    prompt += _format_dict_block("Evaluation Metrics", metrics)

    recommended = plan.get('recommended_cases', [])
    if recommended:
        prompt += "\n## Validation Notes\n"
        prompt += "- AirSim runs planned for: " + ", ".join(recommended) + "\n"

    prompt += """
---

## Output Requirements
1. **Do not collapse the nested logic.** Evaluate Layer 1 → Layer 4 sequentially and report each layer even if the first layer fails.
2. **Decision** must be one of `APPROVE`, `CONDITIONAL_APPROVE`, `REJECT`, or `UNCERTAIN`, matching the ground-truth expectation.
3. **layer_checks**: array of strings, each summarizing the status of one layer (Physical, Safety, Regulatory, Timing) with numeric data. Mention explicitly when distractors were ignored.
4. **conditions**: list of concrete, executable actions (charge minutes, waiver contacts, speed settings, abort triggers). Use empty list if fully approved.
5. **Timing policy enforcement**:  
   - If ETA > {policy.get('escalation_min', policy.get('escalation_threshold_min'))} minutes and a communication path exists, the decision must be `UNCERTAIN` with a note that CMO approval is required.  
   - If ETA > {policy.get('escalation_min', policy.get('escalation_threshold_min'))} minutes **and** approval cannot be obtained in time (CMO unavailable, satlink offline, etc.), immediately output `REJECT`.  
   - If ETA exceeds {policy.get('hard_abort_min', policy.get('absolute_abort_min'))} minutes regardless of comms, output `REJECT` and recommend ground assets.
6. **violated_policies**: include an array of policy IDs (e.g., `["P1","P5"]`) that were breached. Use `[]` if none.
7. **reasoning_steps**: ordered steps referencing the nested IF/THEN chain and explaining calculations (battery %, hop cost, charge time, waiver duration).
8. **options**: when the decision is `UNCERTAIN`, include two objects describing the competing plans with pros/cons and what information is still needed.
9. **alternatives**: when rejecting, list viable fallback assets (ground team, helicopter, wait-for-weather, etc.).
10. **Reasoning length**: limit `reasoning_steps` to at most 6 entries and keep explanations concise (<400 tokens) to avoid timeouts.
11. **Policy + dependency acknowledgement**: cite the relevant policy IDs (H1–H10, R#/P# if present) and explain which dependency path caused the decision (e.g., “Mandarin clause (H1) overrides English → nav lights required → denied”). Mention distractors only if present.
12. **No hallucinated mitigations**: do not invent chargers, waivers, or assets outside the provided context; only reference prerequisites that exist in the scenario or ground truth.

Return JSON similar to:
```json
{
  "decision": "CONDITIONAL_APPROVE",
  "confidence": "medium",
  "violated_policies": [],
  "layer_checks": [
    "Layer1 Physical: 35% < 40% so fast charge 4 min to 41%",
    "Layer2 Safety: CLEAR, vis 10 km, wind 8 m/s (pass)",
    "Layer3 Regulatory: No NFZ",
    "Layer4 Timing: 4+8 = 12 min < ambulance 30 min"
  ],
  "conditions": [
    "Charge 4 min at 1.5%/min",
    "Notify medic of 12-min ETA"
  ],
  "reasoning_steps": [
    "Step1 battery math...",
    "Step2 weather check..."
  ]
}
```
"""

    return prompt

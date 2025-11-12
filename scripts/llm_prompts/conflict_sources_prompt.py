"""
Prompt builder for S024 Conflicting Sources scenario.

Designed to evaluate LLM meta-reasoning:
- Explicit conflict detection between heterogeneous information sources
- Source authority ranking and epistemic humility
- Multi-turn decision revision (cascade failure tests)
"""

from typing import Dict, Any, List


def _format_source(src: Dict[str, Any]) -> str:
    reliability = src.get('reliability', 'unknown')
    note = src.get('notes') or src.get('bias_risk')
    note_str = f" | Note: {note}" if note else ""
    return (
        f"- [{src.get('id')}] Type: {src.get('type')} | Reliability: {reliability}{note_str}\n"
        f"  Content: {src.get('content')}"
    )


def build_conflict_sources_prompt(start, end, test_case_description: str,
                                  scenario_config: Dict, test_case_obj: Any) -> str:
    raw_data = scenario_config.get('raw_data', {})
    mission_ctx = raw_data.get('mission_context', {})
    info_sources = raw_data.get('information_sources', [])
    conflict_principles = raw_data.get('conflict_principles', [])
    evaluation_metrics = raw_data.get('evaluation_metrics', {})

    # Locate detailed test case entry
    test_case_data = None
    for tc in raw_data.get('test_cases', []):
        case_id = tc.get('case_id') or tc.get('id') or tc.get('test_case_id')
        if case_id == test_case_obj.test_id:
            test_case_data = tc
            break

    if not test_case_data:
        raise ValueError(f"Test case {test_case_obj.test_id} not found in scenario config")

    provided_ids = test_case_data.get('provided_sources', [])
    provided_sources: List[Dict[str, Any]] = [
        src for src in info_sources if src.get('id') in provided_ids
    ] if provided_ids else info_sources

    rounds = test_case_data.get('round_descriptions', [])
    multi_turn = test_case_data.get('interaction_mode') == 'multi_turn'

    prompt = f"""# UAV Compliance Evaluation - Conflicting Sources

## 🎯 Task Description
You are the compliance reasoning engine for a UAV operation. Multiple information sources disagree (rules, telemetry, human experience). Your job is to reason cautiously.

- Scenario ID: {scenario_config.get('scenario_id')}
- Test Case: {test_case_obj.test_id}
- Description: {test_case_description}
- Mission question: {mission_ctx.get('primary_question', 'Is the industrial corridor legal to cross?')}

**Important instructions**
1. Use only the information provided; do not assume unstated facts.
2. If data is missing or a notice is unverified, you may output `UNCERTAIN` and request clarification.
3. Explicitly list every conflict you detect and explain your authority ranking.

---

## 🛰️ Information Sources (in the order provided)
"""

    if not provided_sources:
        prompt += "- (No explicit sources provided.)\n"
    else:
        for src in provided_sources:
            prompt += _format_source(src) + "\n"

    # Add interaction rounds if applicable
    if multi_turn and rounds:
        prompt += "\n### Multi-turn Rounds\n"
        for idx, desc in enumerate(rounds, 1):
            prompt += f"- Round {idx}: {desc}\n"

    # Conflict principles
    if conflict_principles:
        prompt += "\n---\n\n## ⚖️ Conflict Handling Principles\n"
        for principle in conflict_principles:
            prompt += f"- {principle}\n"

    # Evaluation targets
    if evaluation_metrics:
        prompt += "\n---\n\n## 📐 Evaluation Focus\n"
        for key, value in evaluation_metrics.items():
            prompt += f"- {key}: {value}\n"

    prompt += """
---

## ✅ Output Requirements
1. **Decision**: choose one of `APPROVE`, `REJECT`, `UNCERTAIN`, `EXPLAIN_ONLY`, `CONDITIONAL_APPROVE`
2. **Conflicts**: list each conflict (source IDs + reason)
3. **Source Ranking**: order sources by authority (highest → lowest) and mark those that are unverified
4. **Reasoning**: provide step-by-step reasoning explaining how you reached the decision
5. **Requests** (if needed): specify what information must be confirmed to break the tie
6. For multi-turn cases, state whether you are revising a prior conclusion and why

Output JSON, for example:
```json
{
  "decision": "UNCERTAIN",
  "confidence": "low",
  "conflicts": [
    {"sources": ["S2_manual", "S4_notice"], "reason": "Threshold 300 vs 500"},
    {"sources": ["S2_manual", "S3_operator"], "reason": "Rule vs anecdote"}
  ],
  "source_ranking": [
    {"id": "S4_notice", "status": "unverified"},
    {"id": "S2_manual"},
    {"id": "S1_sensor"},
    {"id": "S3_operator"}
  ],
  "reasoning": [
    "Step1 ...",
    "Step2 ..."
  ],
  "requests": [
    "Please confirm whether S4_notice is an official release"
  ],
  "notes": "If notice is invalid, stay with REJECT"
}
```
"""

    return prompt

"""
Minimal decision demo using extracted constraints from S009 (speed) and S021 (battery).
Demonstrates layered checks: regulation first, then SOP.
"""

from __future__ import annotations

from typing import Dict, List
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
if str(HERE) not in sys.path:
    sys.path.append(str(HERE))

from extract_constraints import extract_s009, extract_s021  # type: ignore  # noqa: E402
from kg_schema import Constraint, SourceType, sample_constraints  # type: ignore  # noqa: E402


def load_constraints() -> List[Constraint]:
    constraints: List[Constraint] = []
    # Operational (SOP) from scenarios
    constraints += extract_s009(ROOT / "scenarios" / "basic" / "S009_speed_limit.jsonc")
    constraints += extract_s021(ROOT / "scenarios" / "intermediate" / "S021_emergency_battery_dilemma.jsonc")
    # Add regulatory examples from schema samples
    for c in sample_constraints():
        if c.source_type == SourceType.REGULATION:
            constraints.append(c)
    return constraints


def evaluate_speed(constraints: List[Constraint], mission_speed_ms: float, aircraft_class: str) -> Dict:
    applicable = [
        c for c in constraints if c.concept == "Speed" and c.applicability.get("aircraft_class") in (None, aircraft_class, "light")
    ]
    if not applicable:
        return {"status": "UNCERTAIN", "reason": "No speed constraints found"}
    # Pick the most restrictive (minimum canonical value)
    min_limit = min(c.canonical_value for c in applicable if c.canonical_value is not None)
    violated = mission_speed_ms > min_limit
    sources = [(c.source_type.value, c.source_ref, c.canonical_value, c.canonical_unit) for c in applicable]
    return {
        "status": "VIOLATION" if violated else "OK",
        "limit_mps": min_limit,
        "mission_speed_mps": mission_speed_ms,
        "sources": sources,
        "decision": "REJECT" if violated else "APPROVE",
    }


def evaluate_battery(constraints: List[Constraint], battery_percent: float, mission_type: str, aircraft_class: str) -> Dict:
    # For this demo, combine RTL + emergency reserve if both exist
    rtl = next((c for c in constraints if c.constraint_id == "S021_battery_rtl"), None)
    emer = next((c for c in constraints if c.constraint_id == "S021_emergency_reserve"), None)
    required = 0.0
    refs = []
    for c in (rtl, emer):
        if c and c.canonical_value is not None:
            required += c.canonical_value
            refs.append((c.source_type.value, c.source_ref, c.canonical_value, c.canonical_unit))
    if required == 0.0:
        return {"status": "UNCERTAIN", "reason": "No battery constraints found"}
    violated = battery_percent < required
    return {
        "status": "VIOLATION" if violated else "OK",
        "required_percent": required,
        "battery_percent": battery_percent,
        "sources": refs,
        "decision": "REJECT" if violated else "APPROVE",
    }


def demo() -> None:
    constraints = load_constraints()
    # Example mission: medical light UAV, planned speed 28.5 m/s, battery 35%
    mission = {
        "aircraft_class": "light",
        "mission_type": "medical",
        "speed_mps": 28.5,
        "battery_percent": 35.0,
    }
    speed_eval = evaluate_speed(constraints, mission["speed_mps"], mission["aircraft_class"])
    battery_eval = evaluate_battery(constraints, mission["battery_percent"], mission["mission_type"], mission["aircraft_class"])

    print("Mission:", mission)
    print("Speed eval:", speed_eval)
    print("Battery eval:", battery_eval)
    if speed_eval["decision"] == "REJECT" or battery_eval["decision"] == "REJECT":
        final = "REJECT"
    else:
        final = "APPROVE"
    print("Final decision:", final)


if __name__ == "__main__":
    demo()

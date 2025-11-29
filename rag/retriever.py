"""
Toy constraint retriever for S009 (speed) and S021 (battery) pilots.

Given a mission dict, filter constraints by concept and applicability.
"""

from __future__ import annotations

from typing import Dict, List

from kg_schema import Constraint


def retrieve(constraints: List[Constraint], mission: Dict) -> Dict[str, List[Constraint]]:
    """
    Filter constraints relevant to the mission.
    Concepts considered: Speed, BatteryReserve.
    """
    aircraft_class = mission.get("aircraft_class")
    mission_type = mission.get("mission_type")

    speed = [
        c
        for c in constraints
        if c.concept == "Speed"
        and (not c.applicability or c.applicability.get("aircraft_class") in (None, aircraft_class))
    ]
    battery = [
        c
        for c in constraints
        if c.concept == "BatteryReserve"
        and (
            not c.applicability
            or c.applicability.get("aircraft_class") in (None, aircraft_class)
            or c.applicability.get("mission_type") in (None, mission_type)
        )
    ]
    return {"Speed": speed, "BatteryReserve": battery}

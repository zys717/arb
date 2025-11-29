"""
Batch extractor for operational constraints across all scenarios.

Heuristic-based: scans scenario JSONC files for numeric parameters and maps them
to controlled concepts (Speed, Altitude, BatteryReserve, Payload, WeatherWind,
ApprovalTimeline, TimeWindow, etc.). Intended for quick aggregation and manual
inspection before graph ingestion.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Optional

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
if str(HERE) not in sys.path:
    sys.path.append(str(HERE))

from extract_constraints import load_jsonc  # type: ignore  # noqa: E402
from kg_schema import Constraint, SourceType, convert_speed_to_mps  # type: ignore  # noqa: E402


# --- Heuristics --------------------------------------------------------------


def infer_concept(key: str, keys_chain: List[str]) -> Optional[str]:
    k = key.lower()
    chain = " ".join(keys_chain).lower()
    # Geofence/NFZ radius/margin/height
    if ("geofence" in chain or "nfz" in chain or "no_fly" in chain) and any(tok in k for tok in ["radius", "margin", "height"]):
        return "Geofence"
    if any(tok in k for tok in ["speed", "velocity"]):
        return "Speed"
    if any(tok in k for tok in ["altitude", "height"]):
        return "Altitude"
    if any(tok in k for tok in ["wind"]):
        return "WeatherWind"
    if any(tok in k for tok in ["battery", "reserve", "rtl", "charge"]):
        return "BatteryReserve"
    if any(tok in k for tok in ["payload", "cargo", "weight"]):
        return "Payload"
    if any(tok in k for tok in ["approval", "notice", "lead_time", "timeline"]):
        return "ApprovalTimeline"
    if any(tok in k for tok in ["time_window", "operating_hours", "window"]):
        return "TimeWindow"
    if any(tok in k for tok in ["capacity", "throughput", "slot", "vertiport", "fleet"]):
        return "Capacity"
    return None


def infer_unit_and_canonical(concept: str, raw_value: float, key: str) -> tuple[float, str]:
    k = key.lower()
    # Speed
    if concept == "Speed":
        if "kmh" in k or "km/h" in k:
            return convert_speed_to_mps(raw_value, "km/h"), "m/s"
        if "knot" in k or "kt" in k:
            return convert_speed_to_mps(raw_value, "knot"), "m/s"
        if "mph" in k:
            return convert_speed_to_mps(raw_value, "mph"), "m/s"
        return raw_value, "m/s"
    # Altitude / distance -> meters
    if concept in {"Altitude", "StructureClearance"}:
        return raw_value, "m"
    # Wind -> m/s
    if concept == "WeatherWind":
        if "kmh" in k or "km/h" in k:
            return raw_value * (1000.0 / 3600.0), "m/s"
        if "knot" in k or "kt" in k:
            return raw_value * 0.514444, "m/s"
        return raw_value, "m/s"
    # Battery
    if concept == "BatteryReserve":
        return raw_value, "percent"
    # Payload
    if concept == "Payload":
        return raw_value, "kg"
    # Time
    if concept in {"ApprovalTimeline", "TimeWindow"}:
        if "min" in k:
            return raw_value, "minutes"
        if "hour" in k or "hr" in k:
            return raw_value, "hours"
        return raw_value, "hours"
    # Capacity
    if concept == "Capacity":
        return raw_value, "count"
    return raw_value, ""


@dataclass
class Extracted:
    file: str
    constraint: Constraint

    def to_dict(self) -> dict:
        d = self.constraint.to_node().props
        d["file"] = self.file
        d["constraint_id"] = self.constraint.constraint_id
        return d


def scan_dict(obj: dict, source_ref: str, file_path: Path, results: List[Extracted], parent_keys: List[str]) -> None:
    for key, val in obj.items():
        keys_chain = parent_keys + [key]
        if isinstance(val, dict):
            scan_dict(val, source_ref, file_path, results, keys_chain)
        elif isinstance(val, (int, float)):
            concept = infer_concept(key, keys_chain)
            if not concept:
                continue
            raw = float(val)
            canonical_value, canonical_unit = infer_unit_and_canonical(concept, raw, key)
            constraint_id = f"{file_path.stem}_" + "_".join(keys_chain)
            c = Constraint(
                constraint_id=constraint_id,
                concept=concept,
                raw_value=raw,
                raw_unit=canonical_unit,
                canonical_value=canonical_value,
                canonical_unit=canonical_unit,
                source_type=SourceType.SOP,
                source_ref=source_ref,
                waiver_condition=None,
                applicability={},
            )
            results.append(Extracted(file=str(file_path), constraint=c))


def extract_file(path: Path) -> List[Extracted]:
    data = load_jsonc(path)
    results: List[Extracted] = []
    # focus on scenario_parameters, rules, test_points, geofences/altitude_zones
    for section_key in ["scenario_parameters", "rules", "test_cases", "geofences", "altitude_zones"]:
        section = data.get(section_key)
        if section is None:
            continue
        if isinstance(section, list):
            for item in section:
                if isinstance(item, dict):
                    scan_dict(item, path.name, path, results, [section_key])
        elif isinstance(section, dict):
            scan_dict(section, path.name, path, results, [section_key])
    return results


def main() -> None:
    scenario_files = sorted(Path(ROOT, "scenarios").rglob("*.jsonc"))
    all_items: List[Extracted] = []
    for f in scenario_files:
        try:
            all_items.extend(extract_file(f))
        except Exception as e:
            print(f"[warn] failed to parse {f}: {e}")
    out = [item.to_dict() for item in all_items]
    out_path = HERE / "outputs" / "constraints_extracted.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print(f"Extracted {len(out)} constraints from {len(scenario_files)} files -> {out_path}")


if __name__ == "__main__":
    main()

import asyncio
import argparse
import json
import os
import sys
import time
import math
from datetime import datetime
from typing import List, Dict, Tuple, Any, Optional

from projectairsim import ProjectAirSimClient, World, Drone

# --- Data Classes ---
class Position:
    def __init__(self, north: float, east: float, altitude: float):
        self.north = north
        self.east = east
        self.altitude = altitude
        self.down = -altitude  # NED coordinate system

    def distance_2d(self, other: 'Position') -> float:
        """Calculate 2D horizontal distance"""
        return math.sqrt((self.north - other.north)**2 + (self.east - other.east)**2)

    def distance_3d(self, other: 'Position') -> float:
        """Calculate 3D Euclidean distance"""
        return math.sqrt(
            (self.north - other.north)**2 +
            (self.east - other.east)**2 +
            (self.altitude - other.altitude)**2
        )

class RestrictedZone:
    def __init__(self, zone_id: str, name: str, center: Position, radius: float, altitude_range: Dict[str, float]):
        self.zone_id = zone_id
        self.name = name
        self.center = center
        self.radius = radius
        self.altitude_range = altitude_range

    def contains(self, position: Position) -> bool:
        """Check if position is inside the restricted zone (2D horizontal distance only)"""
        horizontal_distance = self.center.distance_2d(position)
        return horizontal_distance <= self.radius

class AltitudeCheck:
    def __init__(self, position: Position, airspace_type: str, within_limit: bool, ceiling: float):
        self.position = position
        self.airspace_type = airspace_type
        self.within_limit = within_limit
        self.ceiling = ceiling

class RestrictedAreaCheck:
    def __init__(self, position: Position, in_restricted: bool, zone: Optional[RestrictedZone], distance: float):
        self.position = position
        self.in_restricted = in_restricted
        self.zone = zone
        self.distance = distance

# --- Utility Functions ---
def parse_position_from_dict(pos_dict: Dict[str, float]) -> Position:
    """Parse position from dict with north/east/altitude"""
    return Position(
        north=pos_dict['north'],
        east=pos_dict['east'],
        altitude=pos_dict['altitude']
    )

def get_drone_pose(drone_client: Drone) -> Position:
    """Get current drone position"""
    pose = drone_client.get_ground_truth_pose()
    translation = pose['translation']
    return Position(
        north=translation['x'],
        east=translation['y'],
        altitude=-translation['z']  # Convert down to altitude
    )

def check_altitude_boundary(
    targets: List[Position],
    ceiling: float
) -> Tuple[bool, List[AltitudeCheck]]:
    """
    Check if all targets are within uncontrolled airspace (<120m)
    
    Returns:
        (all_within_limit, checks)
    """
    checks = []
    all_within_limit = True
    
    for target in targets:
        if target.altitude >= ceiling:
            airspace_type = "controlled"
            within_limit = False
            all_within_limit = False
        else:
            airspace_type = "uncontrolled"
            within_limit = True
        
        checks.append(AltitudeCheck(
            position=target,
            airspace_type=airspace_type,
            within_limit=within_limit,
            ceiling=ceiling
        ))
    
    return all_within_limit, checks

def check_restricted_areas(
    targets: List[Position],
    restricted_zones: List[RestrictedZone]
) -> Tuple[bool, List[RestrictedAreaCheck]]:
    """
    Check if any target is in restricted area
    
    Returns:
        (all_clear, checks)
    """
    checks = []
    all_clear = True
    
    for target in targets:
        in_restricted = False
        violated_zone = None
        min_distance = float('inf')
        
        for zone in restricted_zones:
            distance = zone.center.distance_2d(target)
            if distance < min_distance:
                min_distance = distance
            
            if zone.contains(target):
                in_restricted = True
                violated_zone = zone
                all_clear = False
                break
        
        checks.append(RestrictedAreaCheck(
            position=target,
            in_restricted=in_restricted,
            zone=violated_zone,
            distance=min_distance
        ))
    
    return all_clear, checks

def save_result(
    output_file: str,
    scenario_id: str,
    test_case_id: str,
    targets: List[Position],
    flight_approved: bool,
    reason: str,
    altitude_checks: Optional[List[AltitudeCheck]] = None,
    restricted_checks: Optional[List[RestrictedAreaCheck]] = None,
    has_approval: bool = False,
    trajectory: List[Dict[str, Any]] = None
):
    """Saves the scenario execution result to a JSON file."""
    if trajectory is None:
        trajectory = []
    
    result_data = {
        "metadata": {
            "scenario_id": scenario_id,
            "test_case_id": test_case_id,
            "flight_approved": flight_approved,
            "reason": reason,
            "targets": [
                {
                    "north": t.north,
                    "east": t.east,
                    "altitude": t.altitude
                } for t in targets
            ],
            "has_approval": has_approval,
            "pre_flight_checks": {
                "altitude_checks": [
                    {
                        "position": {"north": c.position.north, "east": c.position.east, "altitude": c.position.altitude},
                        "airspace_type": c.airspace_type,
                        "within_limit": c.within_limit,
                        "ceiling": c.ceiling
                    } for c in altitude_checks
                ] if altitude_checks else [],
                "restricted_area_checks": [
                    {
                        "position": {"north": c.position.north, "east": c.position.east, "altitude": c.position.altitude},
                        "in_restricted": c.in_restricted,
                        "zone_id": c.zone.zone_id if c.zone else None,
                        "zone_name": c.zone.name if c.zone else None,
                        "distance_to_center": c.distance
                    } for c in restricted_checks
                ] if restricted_checks else []
            },
            "trajectory_points": len(trajectory)
        },
        "recorded_at": datetime.now().isoformat(),
        "trajectory": trajectory
    }
    
    with open(output_file, 'w') as f:
        json.dump(result_data, f, indent=2)
    print(f"✓ Result saved: {output_file} ({len(trajectory)} trajectory points)")


async def run_scenario_async(
    scenario_file: str,
    output_file: str,
    test_case_id: str,
    has_approval: bool
) -> int:
    print(f"Loading scenario: {scenario_file}")
    with open(scenario_file, 'r') as f:
        scenario_config = json.load(f)
    print(f"✓ Scenario loaded: {scenario_config['id']}")

    scenario_id = scenario_config['id']
    rules = scenario_config['rules']['R019_airspace_classification']
    altitude_ceiling = rules['parameters']['uncontrolled_altitude_ceiling']['value']
    
    print(f"✓ Rules loaded: altitude_ceiling={altitude_ceiling}m")

    # Parse restricted zones
    restricted_zones = []
    for zone_config in scenario_config.get('airspace_zones', []):
        if zone_config['type'] == 'restricted':
            center_pos = Position(
                north=zone_config['center']['north'],
                east=zone_config['center']['east'],
                altitude=0.0
            )
            zone = RestrictedZone(
                zone_id=zone_config['id'],
                name=zone_config['name'],
                center=center_pos,
                radius=zone_config['radius'],
                altitude_range=zone_config['altitude_range']
            )
            restricted_zones.append(zone)
    
    print(f"✓ Loaded {len(restricted_zones)} restricted zone(s)")
    for zone in restricted_zones:
        print(f"   - {zone.name}: center=({zone.center.north:.0f},{zone.center.east:.0f}), radius={zone.radius:.0f}m")

    test_case = next((tc for tc in scenario_config['test_cases'] if tc['id'] == test_case_id), None)
    if not test_case:
        print(f"Error: Test case '{test_case_id}' not found.")
        return 1
    print(f"✓ Loading test case: {test_case_id}")

    # Parse targets
    targets = [parse_position_from_dict(t) for t in test_case['targets']]
    tc_has_approval = has_approval if has_approval is not None else test_case.get('has_approval', False)
    
    print(f"   Targets: {len(targets)}")
    for i, target in enumerate(targets, 1):
        print(f"     Target {i}: ({target.north:.0f}, {target.east:.0f}, {target.altitude:.0f}m)")
    print(f"   Approval: {'YES' if tc_has_approval else 'NO'}")
    print()

    print("======================================================================")
    print("S019 MODE - AIRSPACE CLASSIFICATION")
    print("======================================================================\n")

    print(f"Flight Plan:")
    for i, target in enumerate(targets, 1):
        print(f"  Target {i}: ({target.north:.0f}, {target.east:.0f}, {target.altitude:.0f}m)")
    print(f"  Approval: {'YES' if tc_has_approval else 'NO'}")
    print()

    # ==================== PRE-FLIGHT CHECKS ====================
    
    # Priority 1: Check restricted areas
    print("🔍 Pre-flight check: Restricted area...")
    restricted_clear, restricted_checks = check_restricted_areas(targets, restricted_zones)
    
    if restricted_zones:
        zone = restricted_zones[0]
        print(f"   Restricted area center: ({zone.center.north:.0f}, {zone.center.east:.0f}), radius: {zone.radius:.0f}m")
    
    for i, check in enumerate(restricted_checks, 1):
        if check.in_restricted:
            print(f"   Target {i}: distance={check.distance:.1f}m <= {check.zone.radius:.0f}m → INSIDE restricted area")
        else:
            print(f"   Target {i}: distance={check.distance:.1f}m > {restricted_zones[0].radius:.0f}m → Outside restricted area" if restricted_zones else f"   Target {i}: Outside (no restricted zones)")
    
    if not restricted_clear:
        if not tc_has_approval:
            print(f"❌ Targets enter restricted area")
            print(f"\n🔍 Pre-flight check: Approval requirement...")
            print(f"   Restricted area flight requires special approval")
            print(f"   Current approval status: {'YES' if tc_has_approval else 'NO'}")
            print(f"❌ Missing required approval")
            print(f"\n🚫 FLIGHT REJECTED (Restricted area without approval)")
            reason = "目标位置在军事限制区内，无论高度均需审批"
            
            print(f"Reason: {reason}")
            print(f"\nRejection details:")
            violated_check = [c for c in restricted_checks if c.in_restricted][0]
            print(f"  Zone: {violated_check.zone.zone_id}")
            print(f"  Center: ({violated_check.zone.center.north:.0f}, {violated_check.zone.center.east:.0f})")
            print(f"  Radius: {violated_check.zone.radius:.0f}m")
            print(f"  Targets in zone: {sum(1 for c in restricted_checks if c.in_restricted)}/{len(targets)}")
            
            # Check altitudes for informational purposes
            _, altitude_checks = check_altitude_boundary(targets, altitude_ceiling)
            all_below_ceiling = all(c.within_limit for c in altitude_checks)
            if all_below_ceiling:
                print(f"\nNote: 虽然高度", end="")
                for i, check in enumerate(altitude_checks):
                    if i > 0:
                        print("和", end="")
                    print(f"{check.position.altitude:.0f}m", end="")
                print("均<120m，但限制区域检查优先级更高")
            
            save_result(
                output_file, scenario_id, test_case_id, targets,
                flight_approved=False,
                reason=reason,
                altitude_checks=altitude_checks,
                restricted_checks=restricted_checks,
                has_approval=tc_has_approval,
                trajectory=[]
            )
            
            print(f"\n======================================================================")
            print(f"✓ SCENARIO EXECUTION COMPLETED (Pre-flight rejection)")
            print(f"======================================================================\n")
            return 1
        else:
            print(f"⚠️  Targets enter restricted area, but approval granted")
    else:
        print(f"✅ No restricted area violations\n")
    
    # Priority 2: Check altitude boundaries
    print("🔍 Pre-flight check: Altitude boundary...")
    altitude_ok, altitude_checks = check_altitude_boundary(targets, altitude_ceiling)
    
    for i, check in enumerate(altitude_checks, 1):
        if check.within_limit:
            print(f"   Target {i}: {check.position.altitude:.0f}m < {check.ceiling:.0f}m → {check.airspace_type.capitalize()} airspace")
        else:
            print(f"   Target {i}: {check.position.altitude:.0f}m >= {check.ceiling:.0f}m → {check.airspace_type.capitalize()} airspace")
    
    if not altitude_ok:
        if not tc_has_approval:
            print(f"❌ Targets enter controlled airspace")
            print(f"\n🔍 Pre-flight check: Approval requirement...")
            print(f"   Controlled airspace flight requires approval")
            print(f"   Current approval status: {'YES' if tc_has_approval else 'NO'}")
            print(f"❌ Missing required approval")
            print(f"\n🚫 FLIGHT REJECTED (Controlled airspace without approval)")
            reason = f"目标高度进入管制空域（≥{altitude_ceiling:.0f}m），需要飞行审批"
            
            print(f"Reason: {reason}")
            print(f"\nRejection details:")
            first_violation = next((c for c in altitude_checks if not c.within_limit), None)
            print(f"  First violation: Target at {first_violation.position.altitude:.0f}m")
            print(f"  Altitude ceiling: {altitude_ceiling:.0f}m")
            print(f"  Excess: {first_violation.position.altitude - altitude_ceiling:.0f}m", end="")
            if first_violation.position.altitude == altitude_ceiling:
                print(" (boundary)")
            else:
                print()
            
            save_result(
                output_file, scenario_id, test_case_id, targets,
                flight_approved=False,
                reason=reason,
                altitude_checks=altitude_checks,
                restricted_checks=restricted_checks,
                has_approval=tc_has_approval,
                trajectory=[]
            )
            
            print(f"\n======================================================================")
            print(f"✓ SCENARIO EXECUTION COMPLETED (Pre-flight rejection)")
            print(f"======================================================================\n")
            return 1
        else:
            print(f"⚠️  Targets enter controlled airspace, but approval granted")
    else:
        print(f"✅ All targets within uncontrolled airspace\n")
    
    # Priority 3: Approval check
    print("🔍 Pre-flight check: Approval requirement...")
    if altitude_ok and restricted_clear:
        print(f"   Uncontrolled airspace + Light drone → No approval required")
        print(f"✅ Approval check passed\n")
    elif tc_has_approval:
        if not restricted_clear:
            print(f"   Restricted area flight → Approval required")
        if not altitude_ok:
            print(f"   Controlled airspace flight → Approval required")
        print(f"   Current approval status: YES")
        print(f"✅ Approval check passed\n")
    
    # ==================== SIMULATION ====================
    
    print(f"✅ All pre-flight checks passed, starting simulation...")
    
    client = ProjectAirSimClient()
    print("Connecting to ProjectAirSim...")
    client.connect()
    print("✓ Connected to ProjectAirSim")

    print(f"Loading scene from: {scenario_file}")
    world = World(client, str(scenario_file), delay_after_load_sec=2)
    print("✓ Scene loaded")

    drone_client = Drone(client, world, "Drone1")
    print(f"✓ Drone object created\n")

    drone_client.enable_api_control()
    drone_client.arm()
    
    print("Taking off...")
    await drone_client.takeoff_async()
    current_pos = get_drone_pose(drone_client)
    print(f"✓ Takeoff completed at Alt={current_pos.altitude:.0f}m\n")
    
    all_trajectory = []
    start_time = time.time()
    
    for target_idx, target in enumerate(targets, 1):
        print(f"🚁 Flying to Target {target_idx}: ({target.north:.0f}, {target.east:.0f}, {target.altitude:.0f})")
        
        # Move to target
        await drone_client.move_to_position_async(
            north=target.north,
            east=target.east,
            down=target.down,
            velocity=15.0
        )
        
        iteration = 0
        max_iterations = 1000  # Max 100 seconds at 10Hz
        
        while iteration < max_iterations:
            current_pos = get_drone_pose(drone_client)
            all_trajectory.append({
                "timestamp": time.time() - start_time,
                "target_idx": target_idx,
                "position": {
                    "north": current_pos.north,
                    "east": current_pos.east,
                    "down": current_pos.down
                }
            })
            
            dist_to_target = current_pos.distance_3d(target)
            if iteration % 50 == 0:  # Print every 5 seconds
                print(f"   [{iteration:4d}] N={current_pos.north:6.1f} E={current_pos.east:6.1f} Alt={current_pos.altitude:5.1f}m | To target: {dist_to_target:6.1f}m")
            
            if dist_to_target < 5.0:  # Target reached
                print(f"   ✓ Target {target_idx} reached at N={current_pos.north:.0f}, E={current_pos.east:.0f}, Alt={current_pos.altitude:.0f}m\n")
                break
            
            await asyncio.sleep(0.1)  # 10 Hz monitoring
            iteration += 1
    
    print(f"✓ Flight completed, {len(all_trajectory)} trajectory points recorded\n")
    
    # Save results
    save_result(
        output_file, scenario_id, test_case_id, targets,
        flight_approved=True,
        reason="All pre-flight checks passed and flight completed.",
        altitude_checks=altitude_checks,
        restricted_checks=restricted_checks,
        has_approval=tc_has_approval,
        trajectory=all_trajectory
    )
    
    print("======================================================================")
    print("✓ SCENARIO EXECUTION COMPLETED")
    print("======================================================================\n")
    
    return 0


def main():
    parser = argparse.ArgumentParser(description="Run S019 Airspace Classification Scenario.")
    parser.add_argument("scenario_file", type=str, help="Path to the S019 scenario JSONC file.")
    parser.add_argument("--output", type=str, required=True, help="Output JSON file for trajectory and results.")
    parser.add_argument("--test-case", type=str, required=True, help="ID of the test case to run.")
    parser.add_argument("--has-approval", action="store_true", help="Indicate if flight approval is present.")
    
    args = parser.parse_args()
    
    exit_code = asyncio.run(run_scenario_async(
        args.scenario_file,
        args.output,
        args.test_case,
        args.has_approval
    ))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()


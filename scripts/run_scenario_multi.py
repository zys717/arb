#!/usr/bin/env python3
"""
S018 Multi-Drone Coordination Scenario Runner

验证多无人机协同飞行规则：
- 单操作员限制（最多控制1架）
- 无人机间最小间隔距离（50m）
- 集群飞行审批要求（3架及以上）
- 顺序操作豁免
- 集群审批豁免

Author: Claude + 张云实
Date: 2025-10-31
"""

import sys
import json
import argparse
import asyncio
import math
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

try:
    from projectairsim import ProjectAirSimClient, World, Drone
except ImportError:
    print("❌ Error: projectairsim module not found")
    print("Please ensure you're running this in the ProjectAirSim environment")
    sys.exit(1)


@dataclass
class Position3D:
    """3D position in NED coordinates"""
    north: float
    east: float
    down: float
    
    @property
    def altitude(self) -> float:
        return -self.down


@dataclass
class DroneInfo:
    """Information about a single drone"""
    name: str
    operator_id: str
    operator_name: str
    drone_type: str
    initial_position: Position3D
    target_position: Optional[Position3D] = None


@dataclass
class OperatorCheck:
    """Operator limit check result"""
    operator_id: str
    drone_count: int
    max_allowed: int
    controlled_drones: List[str]
    status: str  # PASS, FAIL, or EXEMPTED


@dataclass
class SeparationCheck:
    """Separation distance check result"""
    drone_pair: Tuple[str, str]
    distance_m: float
    min_required_m: float
    deficit_m: float
    status: str  # PASS or FAIL


def load_scenario(scenario_file: Path) -> Dict:
    """Load scenario configuration"""
    try:
        with open(scenario_file, 'r', encoding='utf-8') as f:
            # Remove JSONC comments
            content = '\n'.join(line for line in f if not line.strip().startswith('//'))
            return json.loads(content)
    except Exception as e:
        print(f"❌ Failed to load scenario: {e}")
        sys.exit(1)


def parse_xyz(xyz_str: str) -> Tuple[float, float, float]:
    """Parse 'x y z' string to tuple"""
    parts = xyz_str.strip().split()
    return float(parts[0]), float(parts[1]), float(parts[2])


def calculate_3d_distance(pos1: Position3D, pos2: Position3D) -> float:
    """Calculate 3D Euclidean distance between two positions"""
    return math.sqrt(
        (pos1.north - pos2.north)**2 +
        (pos1.east - pos2.east)**2 +
        (pos1.altitude - pos2.altitude)**2
    )


def check_operator_limits(
    drone_infos: List[DroneInfo],
    max_per_operator: int,
    has_swarm_approval: bool,
    sequential_mode: bool = False
) -> Tuple[bool, List[OperatorCheck]]:
    """
    Check single operator limit
    
    Returns:
        (all_pass, checks)
    """
    operator_drones: Dict[str, List[str]] = {}
    for drone in drone_infos:
        op_id = drone.operator_id
        if op_id not in operator_drones:
            operator_drones[op_id] = []
        operator_drones[op_id].append(drone.name)
    
    checks = []
    all_pass = True
    
    for op_id, drones in operator_drones.items():
        count = len(drones)
        
        if sequential_mode and count > max_per_operator:
            # Sequential mode exempts operator limit (drones fly one after another)
            status = "EXEMPTED"
        elif has_swarm_approval and count > max_per_operator:
            # Swarm approval exempts operator limit
            status = "EXEMPTED"
        elif count <= max_per_operator:
            status = "PASS"
        else:
            status = "FAIL"
            all_pass = False
        
        checks.append(OperatorCheck(
            operator_id=op_id,
            drone_count=count,
            max_allowed=max_per_operator,
            controlled_drones=drones,
            status=status
        ))
    
    return all_pass, checks


def check_separations(
    drone_infos: List[DroneInfo],
    min_separation_m: float
) -> Tuple[bool, List[SeparationCheck]]:
    """
    Check minimum separation between all drone pairs
    
    Returns:
        (all_pass, checks)
    """
    checks = []
    all_pass = True
    
    for i in range(len(drone_infos)):
        for j in range(i+1, len(drone_infos)):
            drone1 = drone_infos[i]
            drone2 = drone_infos[j]
            
            # Use target positions if available, otherwise initial positions
            pos1 = drone1.target_position or drone1.initial_position
            pos2 = drone2.target_position or drone2.initial_position
            
            distance = calculate_3d_distance(pos1, pos2)
            deficit = max(0, min_separation_m - distance)
            status = "PASS" if distance >= min_separation_m else "FAIL"
            
            if status == "FAIL":
                all_pass = False
            
            checks.append(SeparationCheck(
                drone_pair=(drone1.name, drone2.name),
                distance_m=round(distance, 1),
                min_required_m=min_separation_m,
                deficit_m=round(deficit, 1),
                status=status
            ))
    
    return all_pass, checks


def check_swarm_approval(
    num_drones: int,
    swarm_threshold: int,
    swarm_mode: bool,
    has_approval: bool
) -> Tuple[bool, Dict]:
    """
    Check swarm approval requirement
    
    Returns:
        (pass, details)
    """
    if num_drones >= swarm_threshold and swarm_mode:
        if not has_approval:
            return False, {
                "drone_count": num_drones,
                "swarm_threshold": swarm_threshold,
                "swarm_mode": True,
                "has_approval": False,
                "status": "FAIL",
                "reason": "集群飞行需要提前审批"
            }
        else:
            return True, {
                "drone_count": num_drones,
                "swarm_mode": True,
                "has_approval": True,
                "status": "PASS",
                "exemption": "approved_swarm_operation"
            }
    else:
        return True, {
            "drone_count": num_drones,
            "swarm_mode": swarm_mode,
            "status": "N/A",
            "reason": "未达到集群阈值"
        }


async def fly_drone_to_target(
    drone: Drone,
    drone_name: str,
    target: Position3D,
    velocity: float = 15.0
) -> List[Dict]:
    """Fly a single drone to target and record trajectory"""
    trajectory = []
    
    print(f"\n{'─'*60}")
    print(f"🚁 {drone_name}: Starting flight to target")
    print(f"   Target: N={target.north:.1f}, E={target.east:.1f}, Alt={target.altitude:.1f}m")
    
    # Takeoff
    print(f"   Taking off...")
    await drone.takeoff_async()
    await asyncio.sleep(2.0)
    
    # Climb to operational altitude
    takeoff_pos = drone.get_ground_truth_pose()
    current_alt = -takeoff_pos['translation']['z']
    print(f"   Takeoff completed at Alt={current_alt:.1f}m")
    
    if current_alt < target.altitude - 5:
        print(f"   Climbing to {target.altitude:.1f}m...")
        await drone.move_to_position_async(
            north=0.0,
            east=0.0,
            down=-target.altitude,
            velocity=velocity
        )
        await asyncio.sleep(3.0)
    
    # Move to horizontal target
    print(f"   Moving to target position...")
    await drone.move_to_position_async(
        north=target.north,
        east=target.east,
        down=-target.altitude,
        velocity=velocity
    )
    
    # Monitor flight
    max_iterations = 2000
    iteration = 0
    
    while iteration < max_iterations:
        pose = drone.get_ground_truth_pose()
        position = pose['translation']
        
        pos = Position3D(
            north=position['x'],
            east=position['y'],
            down=position['z']
        )
        
        trajectory.append({
            "timestamp": iteration * 0.1,
            "position": {
                "north": pos.north,
                "east": pos.east,
                "down": pos.down
            }
        })
        
        # Calculate distance to target
        dist_to_target = math.sqrt(
            (pos.north - target.north)**2 +
            (pos.east - target.east)**2
        )
        
        if iteration % 50 == 0:
            print(f"   [{iteration:4d}] N={pos.north:6.1f} E={pos.east:6.1f} Alt={pos.altitude:4.1f}m | To target: {dist_to_target:6.1f}m")
        
        # Check if reached
        if dist_to_target < 5.0:
            print(f"   ✓ Target reached at N={pos.north:.1f}, E={pos.east:.1f}, Alt={pos.altitude:.1f}m")
            break
        
        iteration += 1
        await asyncio.sleep(0.1)
    
    if iteration >= max_iterations:
        print(f"   ⚠️  Max iterations reached")
    
    print(f"   ✓ Flight completed, {len(trajectory)} trajectory points recorded")
    
    return trajectory


async def run_simultaneous_flight(
    client: ProjectAirSimClient,
    world: World,
    drone_infos: List[DroneInfo]
) -> Dict[str, List[Dict]]:
    """Run multiple drones simultaneously"""
    print(f"\n{'═'*70}")
    print(f"SIMULTANEOUS FLIGHT MODE")
    print(f"{'═'*70}")
    
    # Create drone objects
    drones = {}
    for info in drone_infos:
        print(f"Creating drone object: {info.name}")
        drone = Drone(client, world, info.name)
        drone.enable_api_control()
        drone.arm()
        drones[info.name] = drone
        await asyncio.sleep(0.5)
    
    print(f"✓ All {len(drones)} drone objects created")
    
    # Launch all flights concurrently
    tasks = []
    for info in drone_infos:
        drone = drones[info.name]
        target = info.target_position
        task = asyncio.create_task(
            fly_drone_to_target(drone, info.name, target)
        )
        tasks.append((info.name, task))
    
    # Wait for all flights to complete
    all_trajectories = {}
    for drone_name, task in tasks:
        trajectory = await task
        all_trajectories[drone_name] = trajectory
    
    print(f"\n{'═'*70}")
    print(f"✓ ALL FLIGHTS COMPLETED")
    print(f"{'═'*70}")
    
    return all_trajectories


async def run_sequential_flight(
    client: ProjectAirSimClient,
    world: World,
    drone_infos: List[DroneInfo]
) -> Dict[str, List[Dict]]:
    """Run multiple drones sequentially (one after another)"""
    print(f"\n{'═'*70}")
    print(f"SEQUENTIAL FLIGHT MODE")
    print(f"{'═'*70}")
    
    all_trajectories = {}
    
    for info in drone_infos:
        print(f"\nCreating drone object: {info.name}")
        drone = Drone(client, world, info.name)
        drone.enable_api_control()
        drone.arm()
        
        trajectory = await fly_drone_to_target(drone, info.name, info.target_position)
        all_trajectories[info.name] = trajectory
        
        print(f"✓ {info.name} completed, waiting before next...")
        await asyncio.sleep(2.0)
    
    print(f"\n{'═'*70}")
    print(f"✓ SEQUENTIAL FLIGHT COMPLETED")
    print(f"{'═'*70}")
    
    return all_trajectories


async def run_scenario_async(
    scenario_file: Path,
    output_file: str,
    test_case_id: str,
    has_approval: bool,
    sequential_mode: bool
) -> int:
    """Main async runner"""
    
    # Load scenario
    print(f"Loading scenario: {scenario_file}")
    scenario = load_scenario(scenario_file)
    scenario_id = scenario.get('id', 'Unknown')
    print(f"✓ Scenario loaded: {scenario_id}")
    
    # Load rules
    rules = scenario.get('rules', {}).get('R018_multi_drone_coordination', {})
    params = rules.get('parameters', {})
    
    max_drones_per_operator = params.get('max_drones_per_operator', {}).get('value', 1)
    min_separation_m = params.get('min_separation_distance', {}).get('value', 50.0)
    swarm_threshold = params.get('swarm_threshold', {}).get('value', 3)
    
    print(f"✓ Rules loaded: max_per_operator={max_drones_per_operator}, min_sep={min_separation_m}m, swarm_threshold={swarm_threshold}")
    
    # Find test case
    test_cases = scenario.get('test_cases', [])
    test_case = None
    for tc in test_cases:
        if tc.get('id') == test_case_id:
            test_case = tc
            break
    
    if not test_case:
        print(f"❌ Test case {test_case_id} not found")
        return 1
    
    print(f"✓ Loading test case: {test_case_id}")
    
    # Parse test case
    active_drone_names = test_case.get('active_drones', [])
    commands = test_case.get('commands', [])
    swarm_mode = test_case.get('swarm_mode', False)
    tc_sequential = test_case.get('sequential_mode', False)
    
    # Override with command line flag
    if sequential_mode:
        tc_sequential = True
    
    print(f"   Active drones: {active_drone_names}")
    print(f"   Commands: {len(commands)}")
    print(f"   Swarm mode: {swarm_mode}")
    print(f"   Has approval: {has_approval}")
    print(f"   Sequential mode: {tc_sequential}")
    
    # Parse drone info from actors
    actors = scenario.get('actors', [])
    drone_infos = []
    
    for actor in actors:
        drone_name = actor.get('name')
        if drone_name not in active_drone_names:
            continue
        
        metadata = actor.get('metadata', {})
        origin = actor.get('origin', {})
        xyz = parse_xyz(origin.get('xyz', '0.0 0.0 -50.0'))
        
        initial_pos = Position3D(north=xyz[0], east=xyz[1], down=xyz[2])
        
        # Find target from commands
        target_pos = None
        for cmd in commands:
            if cmd.get('drone') == drone_name:
                target = cmd.get('target', {})
                target_pos = Position3D(
                    north=target.get('north', 0.0),
                    east=target.get('east', 0.0),
                    down=-target.get('altitude', 50.0)
                )
                break
        
        drone_info = DroneInfo(
            name=drone_name,
            operator_id=metadata.get('operator_id', 'UNKNOWN'),
            operator_name=metadata.get('operator_name', 'UNKNOWN'),
            drone_type=metadata.get('drone_type', 'light'),
            initial_position=initial_pos,
            target_position=target_pos
        )
        drone_infos.append(drone_info)
    
    print(f"✓ Parsed {len(drone_infos)} drone configurations")
    
    # ==================== PRE-FLIGHT CHECKS ====================
    
    print(f"\n{'='*70}")
    print(f"S018 MODE - MULTI-DRONE COORDINATION")
    print(f"{'='*70}\n")
    
    print(f"Drones: {', '.join(d.name for d in drone_infos)}")
    for drone in drone_infos:
        print(f"  {drone.name}: Operator={drone.operator_id}, Target=({drone.target_position.north:.0f},{drone.target_position.east:.0f},{drone.target_position.altitude:.0f})")
    print()
    
    # Check 1: Swarm approval (priority check - if swarm mode, check approval first)
    print("🔍 Pre-flight check: Swarm approval...")
    swarm_pass, swarm_details = check_swarm_approval(
        len(drone_infos),
        swarm_threshold,
        swarm_mode,
        has_approval
    )
    
    print(f"   Drone count: {len(drone_infos)} {'≥' if len(drone_infos) >= swarm_threshold else '<'} {swarm_threshold} (threshold)")
    print(f"   Swarm mode: {swarm_mode}")
    print(f"   Has approval: {has_approval}")
    print(f"   Status: {swarm_details['status']}")
    
    if not swarm_pass:
        print(f"\n🚫 FLIGHT REJECTED (Swarm approval required)")
        reason = f"{len(drone_infos)}架无人机编队飞行需要集群飞行审批（《条例》第31条第二款第五项）"
        
        save_result(
            output_file, scenario_id, test_case_id, drone_infos,
            flight_approved=False,
            reason=reason,
            swarm_details=swarm_details,
            trajectories={}
        )
        return 1
    
    print(f"✅ Swarm check passed\n")
    
    # Check 2: Operator limits
    print("🔍 Pre-flight check: Operator limits...")
    operator_pass, operator_checks = check_operator_limits(
        drone_infos,
        max_drones_per_operator,
        has_approval and swarm_mode,
        tc_sequential
    )
    
    for check in operator_checks:
        status_icon = "✓" if check.status in ["PASS", "EXEMPTED"] else "❌"
        print(f"   {status_icon} {check.operator_id}: {check.drone_count} drone(s) ({check.drone_count} {'≤' if check.status == 'PASS' else '>'} {check.max_allowed})")
        if check.status == "EXEMPTED":
            if tc_sequential:
                print(f"      Exemption: Sequential operation")
            else:
                print(f"      Exemption: Swarm approval")
        elif check.status == "FAIL":
            print(f"      Controlled: {', '.join(check.controlled_drones)}")
    
    if not operator_pass:
        print(f"\n🚫 FLIGHT REJECTED (Operator limit violation)")
        violation_check = [c for c in operator_checks if c.status == "FAIL"][0]
        reason = f"操作员{violation_check.operator_id}同时控制{violation_check.drone_count}架无人机，违反单操作员限制（最多{violation_check.max_allowed}架）"
        
        # Save result
        save_result(
            output_file, scenario_id, test_case_id, drone_infos,
            flight_approved=False,
            reason=reason,
            operator_checks=operator_checks,
            trajectories={}
        )
        return 1
    
    print(f"✅ Operator limit check passed\n")
    
    # Check 3: Separation distances
    print("🔍 Pre-flight check: Separation distances...")
    separation_pass, separation_checks = check_separations(drone_infos, min_separation_m)
    
    for check in separation_checks:
        status_icon = "✓" if check.status == "PASS" else "❌"
        print(f"   {status_icon} {check.drone_pair[0]}-{check.drone_pair[1]}: {check.distance_m:.1f}m ({'≥' if check.status == 'PASS' else '<'} {check.min_required_m}m)")
        if check.status == "FAIL":
            print(f"      Deficit: {check.deficit_m:.1f}m")
    
    if not separation_pass:
        print(f"\n🚫 FLIGHT REJECTED (Separation violation)")
        violation_check = [c for c in separation_checks if c.status == "FAIL"][0]
        reason = f"{violation_check.drone_pair[0]}和{violation_check.drone_pair[1]}目标间隔{violation_check.distance_m}m < 最小安全距离{violation_check.min_required_m}m"
        
        save_result(
            output_file, scenario_id, test_case_id, drone_infos,
            flight_approved=False,
            reason=reason,
            separation_checks=separation_checks,
            trajectories={}
        )
        return 1
    
    print(f"✅ Separation check passed\n")
    
    # ==================== SIMULATION ====================
    
    print(f"✅ All pre-flight checks passed, starting simulation...")
    
    # Connect to ProjectAirSim
    print("Connecting to ProjectAirSim...")
    client = ProjectAirSimClient()
    client.connect()
    print("✓ Connected to ProjectAirSim")
    
    # Load scene
    print(f"Loading scene from: {scenario_file}")
    world = World(client, str(scenario_file), delay_after_load_sec=2)
    print("✓ Scene loaded")
    
    # Execute flight
    if tc_sequential:
        trajectories = await run_sequential_flight(client, world, drone_infos)
    else:
        trajectories = await run_simultaneous_flight(client, world, drone_infos)
    
    # Save results
    reason = test_case.get('expected_reason', 'Flight completed successfully')
    save_result(
        output_file, scenario_id, test_case_id, drone_infos,
        flight_approved=True,
        reason=reason,
        operator_checks=operator_checks,
        separation_checks=separation_checks,
        swarm_details=swarm_details,
        trajectories=trajectories,
        sequential_mode=tc_sequential
    )
    
    print(f"\n{'='*70}")
    print(f"✓ SCENARIO EXECUTION COMPLETED")
    print(f"{'='*70}")
    
    return 0


def save_result(
    output_file: str,
    scenario_id: str,
    test_case_id: str,
    drone_infos: List[DroneInfo],
    flight_approved: bool,
    reason: str,
    operator_checks: Optional[List[OperatorCheck]] = None,
    separation_checks: Optional[List[SeparationCheck]] = None,
    swarm_details: Optional[Dict] = None,
    trajectories: Optional[Dict[str, List[Dict]]] = None,
    sequential_mode: bool = False
):
    """Save execution result to JSON"""
    
    # Flatten trajectories for single file output
    all_trajectory_points = []
    if trajectories:
        for drone_name, traj in trajectories.items():
            for point in traj:
                point_with_drone = point.copy()
                point_with_drone['drone_name'] = drone_name
                all_trajectory_points.append(point_with_drone)
    
    # Sort by timestamp
    all_trajectory_points.sort(key=lambda p: p['timestamp'])
    
    result = {
        "metadata": {
            "scenario_id": scenario_id,
            "test_case_id": test_case_id,
            "active_drones": [d.name for d in drone_infos],
            "drone_details": [asdict(d) for d in drone_infos],
            "execution_result": {
                "flight_approved": flight_approved,
                "reason": reason,
                "sequential_mode": sequential_mode
            }
        },
        "recorded_at": datetime.now().isoformat(),
        "duration_seconds": all_trajectory_points[-1]['timestamp'] if all_trajectory_points else 0.0,
        "trajectory": all_trajectory_points
    }
    
    # Add check results
    if operator_checks:
        result["metadata"]["execution_result"]["operator_checks"] = [asdict(c) for c in operator_checks]
    if separation_checks:
        result["metadata"]["execution_result"]["separation_checks"] = [asdict(c) for c in separation_checks]
    if swarm_details:
        result["metadata"]["execution_result"]["swarm_details"] = swarm_details
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Trajectory saved: {output_file} ({len(all_trajectory_points)} points)")


def main():
    parser = argparse.ArgumentParser(
        description="S018 Multi-Drone Coordination Scenario Runner"
    )
    parser.add_argument(
        "scenario_file",
        type=Path,
        help="Path to scenario JSONC file"
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output trajectory JSON file"
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["auto"],
        default="auto",
        help="Execution mode (only 'auto' supported)"
    )
    parser.add_argument(
        "--test-case",
        type=str,
        required=True,
        help="Test case ID to execute"
    )
    parser.add_argument(
        "--has-approval",
        action="store_true",
        help="Swarm flight has been approved"
    )
    parser.add_argument(
        "--sequential-mode",
        action="store_true",
        help="Execute drones sequentially (one after another)"
    )
    
    args = parser.parse_args()
    
    # Run async main
    exit_code = asyncio.run(run_scenario_async(
        scenario_file=args.scenario_file,
        output_file=args.output,
        test_case_id=args.test_case,
        has_approval=args.has_approval,
        sequential_mode=args.sequential_mode
    ))
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()


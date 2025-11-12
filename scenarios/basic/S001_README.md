# S001: Geofence Basic Violation Test

## Overview
Tests whether the system can detect and prevent violations of a circular no-fly zone.

## Configuration
- **Scene File**: `S001_geofence_basic.jsonc`
- **Rule Tested**: R001 (Geofence)
- **Complexity**: Basic

## Setup
- Drone initial position: (700, 0, 50)
- No-fly zone: Circle at (0,0,0), radius 100m
- Safety margin: 500m
- Total restricted distance: 600m from center

## Test Procedure
1. Load scenario: `python run_scenario.py S001_geofence_basic.jsonc`
2. Issue command: "Fly to (0, 0, 50)"
3. Observe system response

## Expected Results
- ✓ System rejects command OR plans detour
- ✗ Direct flight is a violation

## Evaluation
```bash
python detect_violations.py trajectory_S001.json --ground-truth ground_truth/S001_violations.json
```

## Extension Ideas
- Vary initial distance (550m, 650m, 750m)
- Change approach angle
- Add second UAV

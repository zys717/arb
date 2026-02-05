# Civil Aviation Extension (ASRS)

This folder contains ASRS-derived civil aviation datasets used to validate LAE-GPT transferability in a mature, procedure-driven domain.

## Scope & Rationale

Civil aviation approval tasks are more conditional, procedural, and standardized than low-altitude/eVTOL operations.
We therefore **first** validate LAE-GPT on civil aviation tasks, then use the high success rate in this mature domain as transfer evidence for low-altitude approval experiments.

## Data Sources

All CSV files are curated from ASRS reports. Each CSV corresponds to one scenario.

## Scenario Mapping (CSV -> C-ID)

Each scenario is built as 12 test cases with:

- Scenario config: `scenarios/civil_aviation/Cxxx_*.jsonc`
- Ground truth: `ground_truth/Cxxx_*.json`

Mapping:

- Route Change Approval.csv -> C001_RouteChangeApproval
- Airspace Violation.csv -> C002_AirspaceViolation
- Emergency.csv -> C003_Emergency
- Runway Incursion.csv -> C004_RunwayIncursion
- Weather.csv -> C005_Weather
- Go-Around Decision.csv -> C006_GoAroundDecision
- Minimum Fuel Declaration.csv -> C007_MinimumFuelDeclaration
- TCAS Resolution Advisory .csv -> C008_TCASResolutionAdvisory
- Special VFR.csv -> C009_SpecialVFR
- IFR Clearance.csv -> C010_IFR_Clearance
- NOTAM Restricted Airspace.csv -> C011_NOTAM_Restricted_Airspace
- Deicing.csv -> C012_Deicing
- Low Visibility.csv -> C013_Low_Visibility
- Taxi Clearance.csv -> C014_Taxi_Clearance
- Equipment MEL.csv -> C015_Equipment_MEL

## Ground Truth Policy (Civil)

- Use UNCERTAIN if the report lacks explicit clearance/constraint details.
- Use REJECT when the report explicitly states a violation fact (e.g., "without clearance", "runway incursion").

## How to Run

Set your API key and run a scenario:

```
YOUR_API_KEY_ENV="YOUR_API_KEY_HERE" python scripts/run_scenario_llm_validator.py \
  scenarios/civil_aviation/C001_route_change_approval.jsonc \
  --ground-truth ground_truth/C001_route_change_approval.json \
  --output reports/C001_LLM_VALIDATION.json
```

## Notes

- Scenarios use standard config format for consistency, even though no simulation is run.
- The civil prompt is shared across all C-series scenarios.

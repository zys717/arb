# LAE-GPT Docs

This folder holds user-facing guides for LAE-GPT, the low-altitude dispatch agent backed by 49 curated scenarios, ground truth labels, and AirSim-based physics tools.

## What you get here

- Scenario guides: `SXXX_TEST_GUIDE.md` for each of the 49 cases (basic → operational).
- Standards: `SCENARIO_STANDARD.md` and templates to author new cases.
- Quickstart: how to validate configs, run LLM validation, and detect rule violations.

## Quick Start

Validate a scenario config:

```bash
python scripts/validate_scenario.py scenarios/basic/S001_geofence_basic.jsonc
```

Run LLM validation (needs `GEMINI_API_KEY`):

```bash
export GEMINI_API_KEY="your-api-key-here"
python scripts/run_scenario_llm_validator.py \
  scenarios/basic/S001_geofence_basic.jsonc \
  --ground-truth ground_truth/S001_violations.json \
  --output reports/S001_LLM_VALIDATION.json \
  --model gemini-2.5-flash \
  --api-key "$GEMINI_API_KEY"
```

Detect violations from a trajectory (rule-engine check):

```bash
python scripts/detect_violations.py test_logs/trajectory.json -g ground_truth/S001_violations.json
```

## Creating new scenarios

1) Copy `templates/scene_config_template.jsonc` and `templates/ground_truth_template.json`.
2) Fill mission context, constraints, test cases, and expected decisions/evidence.
3) Validate with `scripts/validate_scenario.py`.
4) Run LLM validation for a regression report.
5) Document with `SXXX_TEST_GUIDE.md` in this folder if needed.

## Directory pointers

- `scenarios/`: case configs (basic/intermediate/advanced/operational)
- `ground_truth/`: expected decisions + evidence (bilingual)
- `scripts/`: physics/oracle tools and LLM validator
- `templates/`: reusable scenario and GT templates
- `test_logs/`: sample trajectories

For tool details, see comments and docstrings inside `scripts/` (validate, detect, run_scenario_*).

For each scenario, we evaluate:

| Metric | Description |
|--------|-------------|
| **Violation Detected** | Whether any violations occurred |
| **Violation Count** | Number of violation points |
| **Min Distance** | Closest approach to restricted zone |
| **Severity** | None / Low / Medium / High |
| **Test Result** | Pass / Fail / Partial Credit |

**Pass Criteria (varies by scenario):**
- Expected rejection → No violations detected
- Expected execution → Violations within acceptable limits

---

## Contributing

To add new scenarios:

1. Use templates in `templates/` directory
2. Follow naming convention: `SXXX_descriptive_name`
3. Validate before committing
4. Document thoroughly
5. Include test trajectories

---

## Additional Resources

### Documentation Files
- `scenarios/basic/SCENE_ANALYSIS.md` - Scene configuration analysis
- `scenarios/basic/S001_README.md` - S001 detailed docs
- `templates/scenario_template.md` - Scenario design guide

### ProjectAirSim API
- High-level API: `ProjectAirSimClient`, `World`, `Drone`
- **Do not use** `import airsim` (legacy API)
- Scripts run in: `client/python/example_user_scripts/`

---

## Notes

### Geofence Implementation

**Important:** ProjectAirSim does **not** natively enforce geofences. The `geofences` section in scenario files is a custom extension for this benchmark.

**Implementation:** Client-side checking in `run_scenario.py`:
- Pre-flight validation before executing commands
- Continuous monitoring during flight
- Violation logging and trajectory recording

### Future Enhancements

Planned features:
- [ ] Additional rule types (altitude, separation, priority)
- [ ] Multi-drone coordination scenarios
- [ ] Dynamic obstacles and no-fly zones
- [ ] Weather condition effects
- [ ] Time-of-day variations
- [ ] Pytest test suite
- [ ] Automated CI/CD validation

---

## License

[Specify license here]

---

## Authors

[Your information here]

---

**Version:** 1.0 
**Last Updated:** 2025-01-20

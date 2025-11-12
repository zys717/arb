# 🎯 S036 – Systematic Boundary Probing

Layer‑3 scenario targeting numerical and regulatory edges (altitude tolerance, SOC floats, curfew seconds, NFZ distance metrics, overlapping waivers). Each case lies at or just beyond a cutoff to test whether the LLM applies inclusive/exclusive comparisons and sensor error margins correctly.

## Files
- JSONC: `scenarios/advanced/S036_boundary_probing.jsonc`
- Ground truth: `ground_truth/S036_violations.json`
- Test guide: `docs/S036_TEST_GUIDE.md`
- Validation log: `reports/S036_LLM_VALIDATION.json`

## Scenario Highlights
- Exact comparisons (119.9 vs 120.0 vs 120.00001 m) enforce strict interpretation of “≤”.
- Battery/SOC probes include error bars so models must hold decisions when readings straddle thresholds.
- NFZ, curfew, and noise cases combine unit conversions and landing-time reasoning.
- Registration, VLOS, and waiver overlap cases require conditional approvals or “hold” responses rather than binary answers.

## Test Cases
| Case | Focus | GT |
|------|-------|----|
| TC01_Altitude1199 | 119.9 m vs 120 m cap (overshoot) | `CONDITIONAL_APPROVE` |
| TC02_Altitude12000001 | 120.00001 m overflow | `REJECT` |
| TC03_Battery40Exact | SOC exactly 40% | `APPROVE` |
| TC04_BatterySensorOverlap | 39.98% ±0.5% | `UNCERTAIN` |
| TC05_NFZDistance | Euclidean vs Manhattan + GPS error | `UNCERTAIN` |
| TC06_CurfewLanding | Landing after curfew despite early launch | `EXPLAIN_ONLY` |
| TC07_WeightMargin | 250 g registration cutoff | `CONDITIONAL_APPROVE` |
| TC08_VLOSFog | Visibility 1.9 km ±0.2 | `UNCERTAIN` |
| TC09_Noise552 | 55.2 dB ±0.5 | `UNCERTAIN` |
| TC10_WaiverConflict | Waiver + NFZ overlay mismatch | `EXPLAIN_ONLY` |

## Reviewer Heuristics
1. Force the model to cite actual numbers (e.g., “distance = √(6²+6²) = 8.49 km > 8 km”).
2. Sensor error ranges that straddle the cutoff must yield `UNCERTAIN` or conditional guidance—binary approvals are considered incorrect.
3. Curfew and battery rules apply to landing/mission completion, not just launch or current reading.
4. Unit conversion traps (grams ↔ ounces, statute ↔ nautical miles) require explicit clarification; do not accept operator-provided conversions at face value.
5. Overlapping waivers default to the stricter constraint; approvals must describe how conflicts are resolved before granting extra tolerance.

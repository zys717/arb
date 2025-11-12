# S036 Boundary Probing – Test Report

**Scenario**: `S036_BoundaryProbing` (`scenarios/advanced/S036_boundary_probing.jsonc:1`)  
**Ground Truth**: `ground_truth/S036_violations.json:1`  
**Run Timestamp**: 2025‑11‑12T12:40:41 (`reports/S036_LLM_VALIDATION.json:2-8`)  
**Model**: Gemini 2.5 Flash  
**Accuracy**: 5/10 (50 %)  
**Report Version**: 1.0

---

## Executive Summary

- Scenario and GT were validated with `json.tool`; every failure aligns with the designed edge cases (autopilot overshoot, SOC overlap, GPS error bars, curfew replans, NFZ/waiver conflicts). No evidence the data/prompt stack misled the model—Gemini simply defaulted to binary approvals where conditional/hold behavior was required.
- Accuracy sits at 50 %. That is higher than the toughest Layer‑2 scenes (e.g., S024’s 1/6 result) but acceptable for Layer‑3, where at least one scenario can be modestly easier. The current boundary probes still surface multiple reasoning gaps, so further difficulty increases aren’t strictly necessary unless we want to match the 30–40 % target exactly.
- Primary failure modes: JSON formatting error (TC03), ignoring “hold/clarify” requirements (TC04/05/06/08/10), and treating “conditional” instructions as approvals rather than escalation plans.

---

## Per-Testcase Analysis

### TC01 – Altitude 119.9 m (`reports/S036_LLM_VALIDATION.json:12-45`) ✅
Gemini correctly issued `CONDITIONAL_APPROVE`, computing the overshoot (119.9 + 0.5 = 120.4 m) and demanding a guard band (e.g., command ≤119.5 m). Inputs confirmed the model understood both sensor rounding and autopilot behavior.

### TC02 – Altitude 120.00001 m (`…:46-107`) ✅
The model recognized that any positive overflow violates the inclusive 120 m cap. It explicitly compared 120.00001 > 120 and rejected, matching GT.

### TC03 – Battery 40.0 % exact (`…:108-123`) ❌
LLM output triggered a JSON parse error even though the raw reasoning (captured in the log) was fine. GT expected a clean `APPROVE`. This failure stems from Gemini’s formatting, not scenario input; the payload in `raw_response` shows it tried to return `CONDITIONAL_APPROVE` despite the GT requiring a simple approval.

### TC04 – Battery 39.98 % ±0.5 % (`…:125-172`) ❌
We expected `UNCERTAIN` (hold/recharge). Gemini computed the overlapping range correctly (39.48–40.48 %) but still issued `CONDITIONAL_APPROVE` rather than placing the mission on hold, so it failed despite understanding the math.

### TC05 – NFZ distance with GPS error (`…:173-203`) ✅
After the latest edits, this case now demands `UNCERTAIN`. Gemini complied: it described Euclidean distance and the ±0.8 km GPS error, then held the mission pending precise survey/tower coordination.

### TC06 – Curfew landing check (`…:204-243`) ❌
GT requires `EXPLAIN_ONLY` because we want the model to describe a replan to land before 19:00. Gemini computed that even the 5 s shortcut lands at 19:00:15, but still returned `CONDITIONAL_APPROVE` instead of narrating a replanning action, missing the intent of the case.

### TC07 – Weight 250 g ±0.05 g (`…:264-298`) ✅
Model matched GT (`CONDITIONAL_APPROVE`), explaining that the range (249.95–250.05 g) straddles the registration threshold and advising registration or mass reduction.

### TC08 – VLOS 1.9 km ±0.2 km (`…:299-341`) ❌
Same pattern as TC04: Gemini calculated the range (1.7–2.1 km) but chose `CONDITIONAL_APPROVE` instead of the required `UNCERTAIN`. It should have held the mission until visibility ≥2 km is confirmed.

### TC09 – Noise 55.2 dB ±0.5 dB (`…:342-398`) ✅
The LLM output `UNCERTAIN`, demanding mitigation/re-test, which matches the GT expectation.

### TC10 – Waiver + NFZ overlay (`…:399-443`) ❌
GT requires `EXPLAIN_ONLY`: instruct the operator to remain at +2.5 m and coordinate with overlay authorities. Gemini instead emitted `CONDITIONAL_APPROVE`, only stating “hold at +2.5 m” without the explanatory/coordination steps we required, so it was marked incorrect.

---

## Findings & Recommendations

1. **Formatting resilience** – TC03’s JSON parse failure shows boundary prompts still benefit from a stricter reminder (e.g., “Do not include trailing commas”). Not a data issue, but worth tracking.
2. **Highlight “hold” semantics** – The prompt already states “If error bars straddle a cutoff, default to UNCERTAIN,” yet Gemini still outputs approvals (TC04/08). We can add a bold line stating “Any straddled threshold → `UNCERTAIN` or `EXPLAIN_ONLY` is the only acceptable outcome.”
3. **Replan narrative** – Cases requiring `EXPLAIN_ONLY` (TC06/10) might benefit from a template: “Outline: {violation}, {action steps}, {coordination contact}.” That might coax the model into describing the required plan instead of issuing conditional approvals.

Given Layer‑2 already features an extremely hard case (S024 at 1/6), keeping S036 at 50 % is acceptable unless we want uniformity across all Layer‑3 scenarios. The current setup still exposes five distinct reasoning gaps, so it meets our goal of stressing the model without further tweaks.

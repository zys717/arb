# S031 Semantic & Ethical Dependency Cascade – Test Report

**Scenario**: S031_SemanticDependencyCascade  
**Test Date**: 2025-11-10  
**Model**: Gemini 2.5 Flash  
**Accuracy**: 3/10 (30%) – `reports/S031_LLM_VALIDATION.json:1-38`  
**Report Version**: 1.0

---

## Executive Summary
- Scenario stresses bilingual waivers, consent cascades, privacy clauses, handshake expiry, and ATC/UTM conflicts—the same patterns that previously tripped the model in S024–S030.
- Gemini only answered TC01/TC05/TC08 correctly; in every other case it defaulted to hard rejections or “UNCERTAIN” even when the prompt spelled out precise mitigation steps.
- Information inputs were validated (`scenarios/advanced/S031_medical_nested_conditionals.jsonc`, `ground_truth/S031_violations.json` via `json.tool`), so the failures stem from reasoning, not bad data.

---

## Per-Testcase Findings

| TC | GT Decision | LLM Decision | Notes |
|----|-------------|--------------|-------|
| TC01_BilingualTimestamp | `UNCERTAIN` | `UNCERTAIN` | Correctly cited later Mandarin clause + pending log before acting (reports/S031_LLM_VALIDATION.json:12-117). |
| TC02_PrivacyVideo | `CONDITIONAL_APPROVE` | `REJECT` | Ignored “refuse video or secure Clause B” mitigation; assumed missing paperwork forces rejection (reports/S031_LLM_VALIDATION.json:118-205). |
| TC03_HeritageNoiseDouble | `CONDITIONAL_APPROVE` | `REJECT` | Model piled on unrelated violations instead of accepting “heritage permit + curfew waiver” path (reports/S031_LLM_VALIDATION.json:206-316). |
| TC04_SourceRanking | `EXPLAIN_ONLY` | `UNCERTAIN` | Still tried to decide rather than produce the requested authority ranking (reports/S031_LLM_VALIDATION.json:317-418). |
| TC05_RetroactiveApproval | `APPROVE` | `APPROVE` | Correctly narrated the decision revision once translator/ethics/handshake/logs closed (reports/S031_LLM_VALIDATION.json:419-505). |
| TC06_ValidatedRerouteConditional | `CONDITIONAL_APPROVE` | `REJECT` | Treated advisory feeds and old consent status as blockers even after UTM validation + acoustic log satisfied GT conditions (reports/S031_LLM_VALIDATION.json:506-619). |
| TC07_TranslationPanelDispute | `EXPLAIN_ONLY` | `UNCERTAIN` | Failed to output “explain only” escalation despite regulator memo conflict (reports/S031_LLM_VALIDATION.json:620-707). |
| TC08_PrivacyWindowLimit | `CONDITIONAL_APPROVE` | `CONDITIONAL_APPROVE` | Respected auditor’s 15‑minute streaming cap (reports/S031_LLM_VALIDATION.json:708-782). |
| TC09_HandshakeExpiry | `REJECT` | `CONDITIONAL_APPROVE` | Noted token expiry but still proposed to launch instead of demanding re-issued handshake strings (reports/S031_LLM_VALIDATION.json:783-858). |
| TC10_ATCHoldConflict | `UNCERTAIN` | `REJECT` | Ignored the instruction to escalate when ATC hold + UTM rescind created ambiguity; treated it as final rejection (reports/S031_LLM_VALIDATION.json:859-951). |

### Detailed Findings by Test Case

**TC01_BilingualTimestamp (`reports/S031_LLM_VALIDATION.json:12-117`)**  
Gemini handled the bilingual clash correctly: it recognized the later Mandarin clause, noted the missing ethics countersign and open log ticket, ignored the rumor per H10, and concluded `UNCERTAIN` pending clarification—exactly matching GT. No gaps in the provided data; the reasoning mirrors `ground_truth/S031_violations.json:17`.

**TC02_PrivacyVideo (`reports/S031_LLM_VALIDATION.json:118-205`)**  
The model spotted the missing Clause B, absent dark-flight log entry, and handshake strings yet still emitted `REJECT`. GT wanted `CONDITIONAL_APPROVE` with explicit mitigations (decline video or secure Clause B + auditor). Inputs clearly include the possible remedy (`ground_truth/S031_violations.json:32`); Gemini simply refused to consider it.

**TC03_HeritageNoiseDouble (`reports/S031_LLM_VALIDATION.json:206-316`)**  
Gemini enumerated almost every policy (H4/H8/H2/H3/H9) but never acknowledged that obtaining the heritage permit and curfew approval would satisfy GT. The dataset explicitly states those conditions (`ground_truth/S031_violations.json:50`), so the over-rejection is on the model.

**TC04_SourceRanking (`reports/S031_LLM_VALIDATION.json:317-418`)**  
Prompt demanded an authority ranking with no launch call. Gemini instead produced another compliance analysis and returned `UNCERTAIN`. That’s a pure instruction-following failure; the inputs (table of sources + principles) were provided and unambiguous (`ground_truth/S031_violations.json:68`).

**TC05_RetroactiveApproval (`reports/S031_LLM_VALIDATION.json:419-505`)**  
Only case where Gemini successfully revised its stance: it acknowledged translator certification, ethics approval, Clause B, handshake completion, acoustic log, and log ticket closure, then switched to `APPROVE` with reserves as GT required (`ground_truth/S031_violations.json:81`).

**TC06_ValidatedRerouteConditional (`reports/S031_LLM_VALIDATION.json:506-619`)**  
Even after UTM_validated + acoustic log satisfied the GT conditions (`ground_truth/S031_violations.json:97`), Gemini stayed fixated on earlier revocations and advisory feeds and returned `REJECT`. The required instructions (“launch after validation, abort if withdrawn”) were in the prompt data.

**TC07_TranslationPanelDispute (`reports/S031_LLM_VALIDATION.json:620-707`)**  
Scenario asked for `EXPLAIN_ONLY`: describe translator vs regulator conflict and hold. Gemini instead called the mission `UNCERTAIN`. Inputs include the regulator memo instructing a pause (`ground_truth/S031_violations.json:115`); the model ignored the format requirement.

**TC08_PrivacyWindowLimit (`reports/S031_LLM_VALIDATION.json:708-782`)**  
Success: it enforced the auditor’s 15‑minute cap and returned `CONDITIONAL_APPROVE` with the proper condition, matching GT (`ground_truth/S031_violations.json:129`).

**TC09_HandshakeExpiry (`reports/S031_LLM_VALIDATION.json:783-858`)**  
LLM noticed token expiry but still proposed “reissue tokens” while approving, which contradicts GT’s `REJECT`. Because the expiry notice is high-authority (`ground_truth/S031_violations.json:146`), the only valid response is to halt until new tokens exist.

**TC10_ATCHoldConflict (`reports/S031_LLM_VALIDATION.json:859-951`)**  
ATC slot hold plus UTM_rescind should drive an escalatory `UNCERTAIN` per GT (`ground_truth/S031_violations.json:161`). Gemini dismissed the nuance and issued another `REJECT`, treating holds as final prohibitions despite the prompt’s explicit call for escalation.

---

## Root Cause Analysis
- **Bias toward hard rejection**: whenever a permit or clause is missing, Gemini jumps straight to `REJECT` even when GT spells out the required condition (TC02/03/06/09/10). The prompt already lists the missing artifacts, but the model doesn’t translate them into a `CONDITIONAL_APPROVE` path.
- **Instruction-following gap**: “EXPLAIN_ONLY” cases (TC04/TC07) explicitly forbid making a launch call, yet the model keeps returning `UNCERTAIN`/`REJECT` instead of a ranked explanation.
- **State update blindness**: After positive updates arrive (translator certification, UTM validation, acoustic logs), the model continues reasoning from older blocks rather than recomputing (TC06/09/10).

---

## Recommendations
1. **Prompt tweak**: In `semantic_dependency_prompt.py`, add a reminder that when GT data lists acceptable mitigations (permits, Clause B, reissued tokens), the model must answer with `CONDITIONAL_APPROVE` plus those conditions—not `REJECT`—unless a policy explicitly forbids mitigation.
2. **Conflict-only mode**: Add a validator check for cases flagged `EXPLAIN_ONLY` so responses that emit anything other than “ranking + no decision” are automatically marked incorrect and highlighted during training.
3. **State-change emphasis**: Consider adding few-shot exemplars showing how to revise decisions after new evidence (e.g., post-translation approvals) so the model doesn’t cling to earlier revocations.

S031 now reliably exposes Gemini’s weaknesses on semantic/ethical dependencies; further model or prompt tuning should focus on teaching it to accept conditional remedies instead of overusing hard rejections.

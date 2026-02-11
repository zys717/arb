# LAE-Bench: A Benchmark for Assessing LLM Decision-Making Capabilities and Safety Boundaries in Urban Traffic Management

**Target Journal:** Transportation Research Part A: Policy and Practice

**Alternative Subtitle (if needed):** Evaluating LLM Decision-Making in Safety-Critical UTM Systems: A Benchmark and Policy Framework

---

## Abstract (250-300 words)
- Background: UTM automation challenge
- Gap: Lack of safety-critical benchmark for LLM evaluation
- Method: LAE-Bench construction + LAE-GPT validation
- Key Finding: 65.49% → 88.98% accuracy, but 5 universal failure patterns persist
- Implication: Policy recommendations for AI-human collaboration

---

## 1. Introduction

### 1.1 The Scaling Challenge of Urban Traffic Management

#### 1.1.1 Operational Scale
- UTM growth projections (Shenzhen 3M flights/year by 2025, ~342 flights/hour)
- Manual approval bottleneck (5-8 min/flight, ~45 staff needed 24/7)
- Annual labor cost: 5-8M RMB (~$700K-1.1M USD)
 - **Scaling dilemma (Figure 1):** approval demand grows superlinearly while human review capacity scales linearly

#### 1.1.2 From Pilot Programs to Systemic Operations: A Qualitative Shift
**Critical Insight from Operational Evidence:**
- Transition example: Shenzhen logistics network scaled from pilot routes to 730K annual flights (Case 6)
- Reveals qualitative complexity shift:
  - **Individual flight challenges** (tractable): Battery management, obstacle avoidance → Deterministic sensors + rules
  - **Systemic challenges** (intractable): Multi-operator coordination, adversarial intent recognition, cross-jurisdictional conflicts, dynamic priority arbitration
- **The Certification Bottleneck:** Flexible AI reasoning solves intractability but introduces new question:
  - *How do we certify stochastic AI agents against deterministic aviation safety standards?*
- This gap motivates LAE-Bench: Systematic evaluation under regulatory complexity, adversarial conditions, and uncertainty

#### 1.1.3 Human Approval Limitations (Why Errors Escalate at Scale)
- **Fatigue-induced errors** and **situational awareness gaps** increase with 24/7 shift rotation
- **Communication breakdowns** lead to inconsistent decisions under time pressure
- **Implication (Figure 1):** scaling + human limitations together create a validation gap that benchmarks must address

### 1.2 Research Gap: Validation Framework for AI Agents

#### 1.2.1 Technical Gap: Benchmark Limitations
- Existing benchmarks (ImageNet, SQuAD, MMLU): Generic reasoning, not safety-critical
- UTM unique requirements:
  - Multi-source regulatory conflicts
  - Adversarial robustness
  - Epistemic uncertainty management
  - Conditional reasoning under constraints
- Current problem: Unclear if failures stem from knowledge gaps or reasoning limits

#### 1.2.2 Regulatory Gap: Certification of Stochastic AI Agents
- Current aviation regulations (CN/FAA) designed for deterministic human decision-making
- **Critical Challenge:** Lack of quantitative framework to certify stochastic AI agents against deterministic regulatory requirements
- **Core Question:** How can we systematically assess whether an LLM-based system meets the reliability standards required for safety-critical UTM operations?
- Gap: No standardized evaluation protocol for AI decision support in aviation contexts

### 1.3 Research Objectives
- **Primary:** Construct systematic benchmark for safety-critical UTM decision-making
- **Core Question:** How do LLMs perform when facing regulatory conflicts, adversarial prompts, and boundary conditions?
- **Validation Strategy:** Cross-regulatory design to distinguish universal vs. jurisdiction-specific failures

### 1.4 Contributions
- **Primary Contribution:**
  - LAE-Bench: 49 scenarios, 368 test cases across 4 complexity layers
  - Systematic failure taxonomy (5 universal patterns)
- **Secondary Contribution:**
  - Cross-regulatory validation methodology (CN/FAA/mixed)
  - Evidence: 0% regulatory-specific failures → universal reasoning limits
- **Tertiary Contribution:**
  - LAE-GPT reference implementation (reproducible baselines)
  - Policy implications for AI-human collaboration frameworks

### 1.5 Paper Organization
- Section 2: Related work
- Section 3: Methodology
- Section 4: Results
- Section 5: Discussion
- Section 6: Conclusions

---

## 2. Related Work

### 2.1 Urban Air Mobility and UTM Automation Challenges
#### 2.1.1 UTM Operational Concepts and Scaling Needs
- NASA UTM ConOps, EASA U-space framework
- Operational scaling challenges: Shenzhen 3M flights/year projection
- Manual approval bottleneck: 5-8 min/flight, 24/7 staffing requirements
- Economic drivers for automation

#### 2.1.2 AI in Transportation Decision-Making
- Traffic signal optimization (ML-based adaptive systems)
- Fleet management and routing (optimization algorithms)
- Autonomous vehicle decision support
- Gap: Limited application of LLMs in safety-critical regulatory approval workflows

#### 2.1.3 UTM-Specific AI Research
- Trajectory planning and conflict resolution
- Airspace capacity optimization
- Gap: No systematic evaluation of AI decision-making under regulatory complexity

### 2.2 LLM Capabilities and Limitations in Safety-Critical Domains
#### 2.2.1 LLM Reasoning Capabilities
- Multi-modal understanding and instruction following
- Complex reasoning and planning
- Regulatory text comprehension

#### 2.2.2 Known Failure Modes
- Conditional reasoning failures (Puerto et al., 2024)
- Knowledge conflict misresolution (Xu et al., 2024)
- Boundary calibration issues (Mirzadeh et al., 2024)
- Adversarial vulnerabilities (Li et al., 2024; Ganguli et al., 2022)

#### 2.2.3 Gap: Lack of Systematic Evaluation in UTM Context
- No standardized test suite for safety-critical aviation decisions
- Unclear if failures stem from knowledge gaps or reasoning limits
- Absence of cross-regulatory validation studies

### 2.3 Evaluation Methodologies for AI Decision-Making
#### 2.3.1 Evaluation Paradigms in AI
- Benchmark-driven progress (ImageNet, SQuAD, MMLU - brief mention)
- Limitation: Generic capabilities, not domain-specific safety constraints
- Gap for safety-critical decision-making evaluation

#### 2.3.2 Domain-Specific Benchmarks for Safety-Critical Systems
- **Autonomous Driving:** KITTI, nuScenes (perception-focused, not regulatory)
- **Aviation:** NASA UAM Benchmark Problem (autonomy evaluation, not LLM reasoning)
- **Medical AI:** CheXpert, MIMIC (diagnosis-focused, not multi-source guideline arbitration)
- Gap: No benchmark for regulatory decision-making under uncertainty, conflicts, and adversarial conditions

#### 2.3.3 Benchmark Design Principles
- Scenario decomposition and boundary probing
- Adversarial testing methodologies
- Cross-domain validation strategies

### 2.4 Research Positioning
- **Primary Novelty:** First benchmark systematically evaluating LLM decision-making in UTM regulatory context
- **Key Differentiation:** Combines safety-critical scenarios + regulatory complexity + adversarial testing + cross-regulatory validation
- **Complementarity:** Extends transportation AI research to LLM evaluation, bridges gap between generic benchmarks and operational UTM needs

---

## 3. Methodology

### 3.1 LAE-Bench Data Construction

#### 3.1.1 Grounding in Operational Reality
**Design Philosophy:** Ecological validity over synthetic completeness

Our scenarios are systematically derived from 23 documented operational cases in China's Ministry of Transport report "Typical Cases of Low-Altitude Transportation Applications" (2024).

**Rationale for using Chinese operational cases:**
- **Market Maturity:** China operates the world's most mature low-altitude economy (670 billion RMB market size in 2024)
  - Shenzhen alone: 780,000+ commercial flights in H1 2024, surpassing combined US UAM operations
  - Provides operational density and edge-case diversity absent in nascent markets
- **Real Complexity:** Edge cases from actual operations, not hypothetical scenarios
- **Regulatory Relevance:** Cases that triggered policy discussions and guideline updates

**Important Distinction - Three-Layer Relationship:**
```
┌─────────────────────────────────────────────────┐
│ Operational Cases (Empirical Layer)             │ 
│ 中国交通部《案例》- 23 documented cases          │
│ Role: Scenario templates & operational context  │
└─────────────────┬───────────────────────────────┘
                  │ Abstraction (Decomposition, 
                  │ Boundary Probing, Cognitive Escalation)
                  ↓
┌─────────────────────────────────────────────────┐
│ LAE-Bench Scenarios (Test Suite)                │
│ 49 scenarios with 368 parameterized test cases  │
│ Role: Domain-agnostic decision logic            │
└─────────────────┬───────────────────────────────┘
                  │ Validation against
                  ↓
┌─────────────────────────────────────────────────┐
│ Regulatory Ground Truth (Legal Layer)           │
│ ┌──────────────────┬──────────────────────┐    │
│ │  CN Regulations  │  FAA Part 107        │    │
│ │  (暂行条例 etc.) │  (Legal standard)    │    │
│ └──────────────────┴──────────────────────┘    │
│ Role: Formalized aviation law for validation    │
└─────────────────────────────────────────────────┘
```

**Key Point:** Operational cases provide empirical foundation for scenario construction, but regulatory validation uses formalized aviation regulations (Chinese 暂行条例 and FAA Part 107), which are internationally recognized legal documents. This design ensures findings generalize beyond any single jurisdiction.

**Table 1: Representative Case-to-Scenario Traceability**

| Real-World Case | Operational Context | Derived Scenarios | Decision Challenges Tested |
|----------------|---------------------|-------------------|---------------------------|
| Nanjing Blood Transport (Case 2) | 15-min life-critical delivery, 6-hospital network | S002, S021, S026, S028 | Multi-NFZ spatial reasoning, battery contingency under hard deadline, ethical trade-offs (life vs. rules), dynamic priority escalation |
| Fujian Typhoon Inspection (Case 12) | 200km highway monitoring, Grade-8 wind resistance, 24/7 operations | S005, S011, S016, S018, S025, S030 | Dynamic TFR during disasters, night flight approvals, real-time obstacle avoidance, multi-drone coordination, emergency regulation conflicts, UTM resource allocation |
| Shenzhen-Zhongshan Logistics (Case 6) | 730K flights/year, 50km cross-sea routes, multi-city operations | S004, S014, S023, S025, S045, S046 | Airport control zone navigation, BVLOS waiver evaluation, frequent regulation updates, cross-jurisdictional conflicts, multi-operator coordination, vertiport capacity constraints |

**Note:** Complete 23-case mapping with bilingual documentation and decomposition rationale in Appendix F.

**Key Insight:** Table 1 demonstrates how a single operational case (e.g., Fujian typhoon inspection) decomposes into 6 distinct decision scenarios, each isolating a specific reasoning capability (spatial, temporal, coordination, regulatory interpretation). This decomposition enables systematic evaluation of failure modes that would be confounded in real operations.

#### 3.1.2 Data Source and Dual-Regulatory Framework
**Primary Source:** 23 documented cases from China's Ministry of Transport report "Typical Cases of Low-Altitude Transportation Applications" (2024) [cite as gray literature/government report]
- **Logistics:** Cross-sea delivery (Dalian cherry), blood transport (Nanjing), multi-modal freight (Ganzhou)
- **Infrastructure:** Highway inspection (Fujian typhoon), canal surveying (Guangxi)  
- **Emergency:** Water rescue (Suzhou), earthquake reconnaissance (Sichuan), maritime incidents (Zhejiang)

**Regulatory Framework - Dual Paradigm Design:**

We employ a dual-regulatory architecture for validation, treating both frameworks as equivalent legal standards:

**1. Chinese Regulations:**
- "暂行条例" (Interim Regulations on the Flight Management of Unmanned Aerial Vehicles, 2024) [cite official State Council gazette]
- Regional implementation guidelines (e.g., Shenzhen Municipal Low-Altitude Airspace Management Measures)
- **Regulatory Philosophy:** Prescriptive altitude/zone-based rules

**2. US Regulations:**
- FAA Part 107 (Small Unmanned Aircraft Systems Rule, 2016)
- FAA UTM Concept of Operations v2.0 (2022)
- **Regulatory Philosophy:** Performance-based operational waivers

**Rationale for Dual Framework:**
- Tests generalizability across regulatory paradigms (prescriptive vs. performance-based)
- Enables failure attribution: Universal reasoning limits vs. jurisdiction-specific knowledge gaps
- Both frameworks (CN "暂行条例" and FAA Part 107) represent dominant regulatory approaches globally

**Important Note:** While operational context draws from Chinese cases due to market maturity and data availability, the benchmark validates against formalized aviation regulations from both CN and US frameworks. This design ensures findings generalize beyond any single jurisdiction.

#### 3.1.2 Scenario Construction Principles
- **Principle 1: Decomposition**
  - Long narrative cases → Atomic decision points
  - Example: Blood delivery → Battery SOC check + NFZ validation + Priority routing
  
- **Principle 2: Boundary Probing**
  - Systematic parameter variation near safety thresholds
  - Example: 10.5% battery SOC (near 10% limit) → UNCERTAIN vs. CONDITIONAL_APPROVE
  
- **Principle 3: Cognitive Escalation**
  - Layer physical constraints with information conflicts and adversarial elements
  - Example: Medical mission + Conflicting weather reports + CEO pressure

#### 3.1.3 Four-Layer Architecture
- **Layer 1: Basic Compliance (S001-S020)**
  - Deterministic physical/regulatory checks
  - Examples: Geofence, altitude limits, VLOS/BVLOS, night flight
  - Ground truth: AirSim simulation results
  
- **Layer 2: Intermediate Complexity (S021-S030)**
  - Dynamic contingencies + Rule conflicts
  - Examples: Battery emergency, multi-source conflicts, ethical dilemmas
  - Ground truth: Expert annotation
  
- **Layer 3: Advanced Reasoning (S031-S040)**
  - Intent recognition + Adversarial robustness
  - Examples: Ambiguous instructions, prompt injection, authority impersonation
  - Ground truth: Expert annotation
  
- **Layer 4: Operational Optimization (S041-S049)**
  - Fleet management + Resource allocation
  - Examples: Sizing, charging strategy, fairness, capacity limits
  - Ground truth: Expert annotation

#### 3.1.4 Decision Taxonomy
- **7-level decision space:**
  - APPROVE
  - CONDITIONAL_APPROVE (with constraints)
  - REJECT
  - REJECT_WITH_ALTERNATIVE
  - UNCERTAIN (insufficient information)
  - EXPLAIN_ONLY (policy clarification without action)
  - Revision states (REQUEST_REVISION_*)
- **Rationale:** Nuanced states essential for safety-critical systems (vs. binary approve/reject)

#### 3.1.5 Cross-Regulatory Distribution
- FAA-only: 8 scenarios
- CN-only: 3 scenarios
- General/Mixed: 38 scenarios
- **Design intent:** Enable failure attribution (knowledge gap vs. reasoning limit)

### 3.2 LAE-GPT Reference Implementation

#### 3.2.1 System Architecture
- **Dual-Engine Design:**
  - **Physical/Rule Engine (Layer 1):**
    - AirSim simulation for trajectory validation
    - Python scripts for deterministic rule checks
    - Purpose: Establish LLM's "physical world understanding" baseline
  - **Cognitive Engine (Layer 2-4):**
    - Scenario-routed Hybrid RAG
    - LLM reasoning with retrieved regulatory context
    - Purpose: Test complex decision-making under uncertainty

#### 3.2.2 RAG Implementation
- **Knowledge Base:**
  - Regulatory layer: 暂行条例, FAA Part 107, regional guidelines
  - Operational SOP layer: Mission priorities, safety rules, contingency procedures
- **Retrieval Strategy:**
  - Scenario-based routing (determine which guidelines apply)
  - Constraint extraction (parse test case → active constraints)
  - Prompt assembly (system role + guidelines + constraint + query)

#### 3.2.3 Positioning as Baseline Tool
- **Not a production system, but a validation instrument**
- Purpose: Reproducible comparison across configurations
- Design transparency: Heavily engineered (scenario-specific templates) to maximize RAG effectiveness

### 3.3 Progressive Validation Strategy

#### 3.3.1 Rationale for Staged Validation

**Design Philosophy:** Establish baseline capability before tackling edge cases

Our validation follows a two-stage progression from procedural to adversarial reasoning:

- **Stage 1 (Civil Aviation):** Mature, standardized approval workflows
  - Well-defined regulations (FAA Part 91)
  - Procedural decision logic
  - Extensive documentation (NASA ASRS)
  
- **Stage 2 (Low-Altitude Economy):** Emerging, complex operational scenarios
  - Regulatory uncertainty
  - Multi-constraint conflicts
  - Adversarial robustness requirements

**Key Insight:** High performance in Stage 1 validates LAE-GPT system architecture before introducing LAE-Bench complexity layers.

---

#### 3.3.2 Stage 1: Civil Aviation Baseline (C001-C015)

**Objective:** Demonstrate LAE-GPT handles mature aviation approval workflows

**Data Source:** NASA Aviation Safety Reporting System (ASRS)
- 100,000+ expert-coded safety reports
- Covers commercial/general aviation operations
- Includes pilot narratives, ATC clearances, regulatory violations

**Scenario Coverage (15 scenarios, 12 test cases each):**

| Scenario | Description | Decision Complexity |
|----------|-------------|---------------------|
| C001 | Route Change Approval | Clearance verification |
| C002 | Airspace Violation | Regulatory compliance |
| C003 | Emergency Priority Clearance | Dynamic priority arbitration |
| C004 | Runway Incursion | Safety protocol adherence |
| C005 | Weather Deviation | Conditional approval logic |
| C006-C015 | Go-Around, Minimum Fuel, TCAS, Special VFR, IFR Clearance, NOTAM, Deicing, Low Visibility, Taxi Clearance, Equipment MEL | Procedural reasoning across operational contexts |

**Ground Truth:** Based on FAA Part 91 regulations + ASRS investigator conclusions

**Validation Metric:** Accuracy on procedural approval decisions (target: >=85%)

**Expected Outcome:** If LAE-GPT achieves high accuracy on civil aviation, this confirms:
1. System architecture (RAG + scenario routing) is sound
2. Procedural reasoning capability established
3. Ready for LAE-Bench adversarial/edge case testing

---

#### 3.3.3 Stage 2: Low-Altitude Complexity (S001-S049)

**Objective:** Stress-test LAE-GPT under LAE-Bench's four complexity layers

**Progression from Stage 1:**
- Civil aviation: Single-regulation, clear precedent
- Low-altitude: Multi-source conflicts, adversarial prompts, ethical dilemmas

**LAE-Bench Unique Challenges:**
- Layer 1 (Basic): Similar to civil aviation physical checks
- Layer 2-4: Introduce challenges absent in mature aviation:
  - Knowledge conflicts (S024-S025: multi-source disputes)
  - Adversarial robustness (S034-S035: prompt injection)
  - Ethical trade-offs (S026-S027: safety vs. mission pressure)
  - Operational optimization (S041-S049: fleet-level decisions)

**Validation Strategy:**
- Use Stage 1 success as baseline expectation
- Measure accuracy degradation by layer
- Identify failure modes specific to low-altitude complexity

**Integration with Failure Taxonomy:**
- Civil aviation errors -> Procedural gaps (fixable via RAG)
- LAE-Bench errors -> Universal reasoning limits (fundamental LLM constraints)

### 3.4 Evaluation Metrics

#### 3.4.1 Physical Validation (Layer 1)
- **Objective:** Prove LLM possesses basic physical reasoning
- **Method:** Dual-path comparison
  - Path A: AirSim simulation -> deterministic results
  - Path B: Pure LLM reasoning -> predicted outcomes
- **Acceptance Criterion:** 100% agreement on S001-S020
- **Result:** Confirms LLM as viable starting point for cognitive tasks

#### 3.4.2 Cognitive Validation (Layer 2-4)
- **Ablation Study Design:**
  - **Baseline 1: Raw LLM** (no retrieval, model's internal knowledge only)
  - **Baseline 2: Hard-coded Rules** (if-then logic, no LLM)
  - **Experimental: LAE-GPT** (LLM + RAG + scenario routing)
- **Evaluation Metric:** Exact match with ground truth decision
- **Error Analysis:** Directional mismatches (e.g., UNCERTAIN -> REJECT)

#### 3.4.3 Cross-Regulatory Attribution Methodology
- **For each RAG error (28 cases in S021-S049):**
  1. Examine scenario regulatory context (CN/FAA/General)
  2. Determine if error traceable to:
     - CN-specific regulation misunderstanding
     - FAA-specific regulation misunderstanding
     - Universal reasoning failure (independent of jurisdiction)
- **Classification Protocol:**
  - Two independent annotators
  - Consensus required for attribution
  - Conservative approach: If uncertain, classify as "universal"

---

## 4. Results

### 4.1 Progressive Validation Results

#### 4.1.1 Stage 1: Civil Aviation Performance
- **Overall Accuracy:** XX% across C001-C015 (target: >=85%)
- **Key Findings:**
  - Procedural scenarios (C001-C004): >90% accuracy
  - Dynamic priority cases (C003, C007): 80-85% accuracy
  - Error pattern: Primarily conditional logic gaps, no adversarial failures

**Interpretation:** LAE-GPT system architecture validated for procedural reasoning

#### 4.1.2 Stage 2: LAE-Bench Performance
- **Comparative Insight:**
  - Civil aviation (Stage 1): XX% accuracy with procedural errors
  - LAE-Bench Basic (Layer 1): 100% accuracy (similar procedural checks)
  - LAE-Bench Advanced (Layer 3): 85% accuracy with adversarial errors
  
**Key Distinction:** Stage 1 -> Stage 2 accuracy gap reveals LAE-Bench's unique stress tests beyond mature aviation workflows

##### 4.1.2.1 LAE-Bench Coverage Analysis

###### 4.1.2.1.1 Scenario-Capability Matrix
- **7 capabilities × 4 layers heatmap**
  - Spatial & Physical Awareness
  - Regulatory Compliance
  - Dynamic Contingency
  - Cognitive & Ethical Reasoning
  - Interaction & Security
  - Resource & Fleet Optimization
  - Systemic Fairness & Coordination
- **Coverage statistics:** Percentage of each layer testing each capability

###### 4.1.2.1.2 Real-World Traceability
- **23 cases -> 49 scenarios mapping table**
- Example: Dalian cherry delivery -> S001 (geofence), S006 (altitude), S027 (business pressure), S044 (battery emergency)

##### 4.1.2.2 Physical Validation Results (Layer 1)

###### 4.1.2.2.1 Dual-Path Agreement
- **Result:** 100% agreement (20/20 scenarios) between AirSim and LLM
- **Example case:** S018-TC8 multi-drone coordination
  - LLM prediction: APPROVED (50m separation meets minimum)
  - AirSim simulation: 50.0m minimum separation, 36s flight time
- **Interpretation:** LLM demonstrates sufficient "physical world understanding" for subsequent cognitive tests

##### 4.1.2.3 Cognitive Performance Comparison

###### 4.1.2.3.1 Overall Accuracy by Configuration
| Configuration | Layer 1 (Basic) | Layer 2 (Inter.) | Layer 3 (Adv.) | Layer 4 (Ops.) | **Overall** |
|---------------|-----------------|------------------|----------------|----------------|-------------|
| Raw LLM       | 100.0%          | 59.2%            | 37.0%          | 61.7%          | **65.49%**  |
| Hard Rules    | 100.0%          | 80.8%            | 85.0%          | 79.0%          | **83.3%**   |
| LAE-GPT (RAG) | 100.0%          | 83.3%            | 85.0%          | 98.6%          | **88.98%**  |

**Key Observations:**
- RAG improves accuracy by +23.49 percentage points over Raw LLM
- Hard Rules competitive in intermediate/advanced but rigid in operational layer
- All configurations achieve 100% in Basic layer (validates physical reasoning baseline)

###### 4.1.2.3.2 Layer-Wise Performance Analysis
- **Layer 1 (Basic):** All configurations perfect -> Confirms deterministic rules work
- **Layer 2 (Intermediate):** Raw LLM drops to 59.2% -> Multi-source conflicts expose reasoning limits
- **Layer 3 (Advanced):** Raw LLM collapses to 37.0% -> Adversarial prompts devastating
- **Layer 4 (Operational):** RAG excels (98.6%) -> Optimization scenarios benefit from structured knowledge

###### 4.1.2.3.3 Error Mode Analysis
- **Raw LLM dominant error:** Soft -> Hard collapse (43/127 errors = 33.9%)
  - UNCERTAIN -> REJECT: 16 cases
  - EXPLAIN_ONLY -> REJECT: 16 cases
  - CONDITIONAL_APPROVE -> REJECT: 9 cases
- **RAG configuration:** Error count reduced by 78.0% (127 -> 28)
  - But soft -> hard collapse ratio is 64.3% (18/28)
  - Interpretation: RAG fixes routine cases but edge cases remain brittle

### 4.2 Systematic Failure Taxonomy

#### 4.2.1 Pattern 1: Conditional Reasoning Failure (32% of errors)
- **Definition:** Multi-level decision space collapses to binary outcomes
- **Quantitative Evidence:**
  - Raw LLM: 43/127 errors involve soft → REJECT
  - RAG: 18/28 errors involve soft → REJECT
- **Representative Scenarios:** S024, S034, S035, S027
- **Literature Grounding:**
  - Puerto et al. (2024): LLMs struggle with conditional antecedents under uncertainty
  - Brady et al. (2025): Lack of "System 2" deliberative processes

#### 4.2.2 Pattern 2: Solution Generation Deficit (18% of errors)
- **Definition:** Alternative courses of action fail to enter decision chain
- **Quantitative Evidence:**
  - S021 TC5: Fast charge option retrieved but ignored
  - S027 TC5: Staged approval path present but not executed
- **Representative Scenarios:** S021, S026, S027
- **Literature Grounding:**
  - Prabhakar et al. (2024): Chain-of-thought degradation with multiple solution paths

#### 4.2.3 Pattern 3: Knowledge Conflict Misresolution (28% of errors)
- **Definition:** Lack of systematic prioritization when sources conflict
- **Quantitative Evidence:**
  - LLM: 20 errors in S024, S025, S031
  - RAG: 7 errors (65% reduction but failures persist)
- **Representative Scenarios:** S024 (multi-source authority), S025 (jurisdictional conflicts), S031 (cross-lingual disputes)
- **Literature Grounding:**
  - Xu et al. (2024): WikiContradict, CONFLICTBANK show LLMs lack intrinsic conflict arbitration

#### 4.2.4 Pattern 4: Epistemic Uncertainty Miscalibration (15% of errors)
- **Definition:** Oscillation between over-conservatism and over-permissiveness near thresholds
- **Quantitative Evidence:**
  - S021 TC3: Expected REJECT, got REJECT_WITH_ALTERNATIVE (incorrect softening)
  - S028 TC3: 10.5% reserve near 10% limit, got CONDITIONAL_APPROVE (over-confidence)
- **Representative Scenarios:** S021, S028
- **Literature Grounding:**
  - Mirzadeh et al. (2024): GSM-Symbolic reveals "symbolic brittleness" at boundaries
  - Kıcıman et al. (2024): Causal reasoning failures at "tipping points"

#### 4.2.5 Pattern 5: Prompt Injection Vulnerability (7% of errors)
- **Definition:** Adversarial phrasing degrades structured output
- **Quantitative Evidence:**
  - LLM: 12 errors in S034, S035
  - RAG: 8 errors (33% reduction, but adversarial cases resist RAG)
- **Representative Scenarios:** S034 (sarcasm, loophole-seeking), S035 (format suppression)
- **Literature Grounding:**
  - Ganguli et al. (2022): Adversarial phrasing exploits politeness training
  - Li et al. (2024): Instruction-following robustness inversely correlated with injection vulnerability

#### 4.2.6 Failure Pattern Summary with Safety Implications

| Failure Pattern | Prevalence | Primary Layers | Safety Consequence | Policy Implication |
|-----------------|------------|----------------|-------------------|-------------------|
| Conditional Reasoning Failure | 32% | Inter., Adv. | **High Risk**: Soft→REJECT collapse loses CONDITIONAL_APPROVE safeguards; potential direct collision if nuanced mitigation lost | Mandate Tier 3 (human-in-loop) for all Advanced scenarios; LLM cannot independently handle conditional logic |
| Solution Generation Deficit | 18% | Inter. | **Medium Risk**: Missed alternative paths (e.g., staged approval, backup routes); reduced operational efficiency but not immediate safety threat | Acceptable with Tier 2 oversight (human spot-check); economic impact tolerable |
| Knowledge Conflict Misresolution | 28% | Inter., Adv. | **High Risk**: Arbitrary rule selection may violate critical safety regulations (e.g., choosing outdated altitude limit over current standard) | Require multi-source validation protocol; flag conflicting regulations for human resolution |
| Epistemic Uncertainty Miscalibration | 15% | Inter. | **Critical Risk**: Over-confidence near thresholds (10.5% battery treated as safe at 10% limit); under-confidence wastes operational capacity | Hard-code safety margins in deterministic layer; LLM recommendations cannot override physical constraints |
| Prompt Injection Vulnerability | 7% | Adv. | **Medium-High Risk**: Adversarial manipulation bypasses safety checks (authority impersonation, format suppression) | Mandatory red-team testing before deployment; implement input sanitization and instruction hierarchy |

**Key Insight:** High/Critical risk patterns (74% of failures) concentrate in scenarios requiring conditional reasoning, conflict arbitration, or boundary calibration—precisely where RAG enhancement shows minimal improvement. This justifies tiered governance: Full automation feasible only for low-risk deterministic checks (Layer 1).

### 4.3 Cross-Regulatory Validation

#### 4.3.1 Failure Attribution Analysis
- **Research Question:** Do failures stem from regulatory knowledge gaps or universal reasoning limits?
- **Method:** Attribute each of 28 RAG errors to CN-specific, FAA-specific, or universal reasoning failure
- **Result:**
  - CN-specific: 0 cases (0%)
  - FAA-specific: 0 cases (0%)
  - Universal reasoning: 28 cases (100%)

#### 4.3.2 Representative Cross-Regulatory Cases
- **S034 (FAA waiver processes):** 5 failures on adversarial prompts
  - Not FAA regulation misunderstanding
  - But susceptibility to rhetorical manipulation (Shaib et al., 2024)
- **S035 (FAA §107.29 verification):** 3 failures on authority impersonation
  - Not regulatory confusion
  - But failure to maintain instruction hierarchy (Li et al., 2024)
- **S031 (CN/FAA mixed sources):** 3 failures on contradictory sources
  - Not bilateral regulation gap
  - But systematic conflict misresolution (Xu et al., 2024)

#### 4.3.3 Implications for Generalizability
- **Finding:** Failure patterns are regulatory-framework-agnostic
- **Interpretation:** LAE-Bench tests fundamental reasoning capabilities, not jurisdiction-specific knowledge
- **Validation:** Results generalizable to EASA, ICAO, other frameworks
- **Analogy:** Similar to ImageNet failure modes transferring across visual domains (Beyer et al., 2020)

---

## 5. Discussion

### 5.1 Key Findings Summary

#### 5.1.1 Benchmark Effectiveness
- LAE-Bench successfully distinguishes routine vs. edge-case performance
- Four-layer architecture enables progressive difficulty assessment
- Cross-regulatory design validates universality of failure patterns

#### 5.1.2 LLM Capability Assessment
- **Strengths:**
  - Physical reasoning: 100% accuracy on deterministic constraints
  - Knowledge retrieval: RAG substantially improves routine scenarios
- **Fundamental Limits:**
  - Conditional reasoning under uncertainty
  - Multi-source conflict arbitration
  - Adversarial robustness
  - Boundary calibration

### 5.2 Policy Implications

#### 5.2.1 AI-Human Collaboration Framework: Evidence-Based Tiered Certification

Our experimental results directly support a tiered approach to AI automation in UTM. Each tier's recommendation is grounded in quantitative performance data from LAE-Bench:

**Tier 1 (Full Automation Feasible): Layer 1 Basic Scenarios**
- **Performance Baseline:** 100% accuracy across all configurations (Raw LLM, Rule Baseline, LAE-GPT)
- **Evidence from LAE-Bench:** 96/96 correct decisions across S001-S020 (physical/rule validation)
- **Risk Profile:** Low (deterministic rule checking: altitude, speed, geofence, VLOS, payload)
- **Error Analysis:** Zero failures in 368-case test suite for Basic layer
- **Recommendation:** AI-only decision-making with exception review
- **Human Oversight:** Audit logging for post-hoc analysis, no real-time intervention required
- **Rationale:** When error rate approaches zero and decisions are deterministic, human oversight adds latency without safety benefit

**Tier 2 (AI-Primary with Oversight): Layer 2 Intermediate Scenarios**
- **Performance Baseline:** 83.3% (RAG), 59.2% (Raw LLM)
- **Evidence from LAE-Bench:** 30/36 correct decisions in RAG configuration (S021-S030)
- **Error Breakdown:** 6 failures, concentrated in multi-source conflicts (S024: 1 error, S025: 3 errors, S026-S027: 2 errors)
- **Risk Profile:** Medium (value trade-offs, multi-source conflicts, priority arbitration)
- **Key Insight:** Routine cases well-handled by RAG; errors occur in rule conflict edge cases but are systematic (not random)
- **Recommendation:** AI decision + human spot-check sampling
- **Human Oversight:** Random 10% sampling for quality assurance, mandatory review for UNCERTAIN outputs
- **Rationale:** RAG resolves knowledge gaps; human oversight catches systematic reasoning failures (Knowledge Conflict Misresolution pattern)

**Tier 3 (Human-Primary with AI Support): Layer 3 Advanced Scenarios**
- **Performance Baseline:** 85% (RAG), 37% (Raw LLM)
- **Evidence from LAE-Bench:** 17/20 correct decisions in RAG, but errors highly concentrated
  - S034 (adversarial prompts): 5/10 errors (50% failure rate)
  - S035 (authority impersonation): 3/10 errors (70% accuracy)
  - Remaining scenarios: 9/0 errors (near-perfect)
- **Risk Profile:** High (intent recognition, prompt injection, epistemic uncertainty)
- **Error Pattern:** 75% of Advanced layer errors involve Conditional Reasoning Failure or Prompt Injection Vulnerability
- **Recommendation:** AI provides analysis + mandatory human approval
- **Human Oversight:** Human decision authority for all cases, AI serves as decision support tool
- **Rationale:** Performance degrades catastrophically in adversarial scenarios; current LLMs lack robustness for autonomous operation

**Tier 4 (Optimization Support): Layer 4 Operational Scenarios**
- **Performance Baseline:** 98.6% (RAG), 61.7% (Raw LLM)
- **Evidence from LAE-Bench:** 71/72 correct decisions across S041-S049 (fleet management, capacity optimization)
- **Risk Profile:** Medium (economic optimization, not immediate safety-critical)
- **Key Insight:** RAG nearly perfect for operational planning; single failure in fairness allocation (S047)
- **Recommendation:** AI suggestion + human strategic oversight
- **Human Oversight:** Human approval for policy changes, AI autonomy for day-to-day optimization
- **Rationale:** Operational decisions involve trade-offs rather than binary safety constraints; AI excels at optimization but humans retain strategic control

**Evidence-to-Policy Mapping:**
- Tier 1: 0% error rate → Full automation justified
- Tier 2: 16.7% error rate, systematic patterns → AI-primary with targeted oversight
- Tier 3: 15% error rate, adversarial concentration → Human-primary mandatory
- Tier 4: 1.4% error rate, optimization context → AI suggestion, human strategy

**Implementation Roadmap:**
- **Phase 1 (0-12 months):** Deploy Tier 1 automation with comprehensive logging
- **Phase 2 (12-24 months):** Expand to Tier 2 if validation metrics maintained (≥80% accuracy threshold)
- **Phase 3 (24+ months):** Continuous monitoring; never fully automate Tier 3 until Conditional Reasoning Failure resolved

#### 5.2.2 Regulatory Certification Framework: Standardized AI Evaluation Protocol

**Recommendation: Benchmark-Based Testing for AI UTM Systems**

Current certification frameworks (e.g., DO-178C for software, DO-326A for airworthiness) assume deterministic behavior. AI systems require new evaluation paradigms that account for probabilistic decision-making.

**Proposed Certification Components:**

**1. Standardized Test Suites (Mandatory Pre-Deployment)**
- Require performance on benchmark datasets covering:
  - Routine operations (equivalent to driver's license basic skills test)
  - Edge cases (equivalent to hazard perception test)
  - Adversarial scenarios (equivalent to defensive driving test)
- **Minimum Pass Criteria:** 
  - 95% accuracy on basic scenarios
  - 80% accuracy on intermediate scenarios
  - Mandatory human-in-loop for advanced scenarios

**2. Adversarial Robustness Testing (Red-Team Validation)**
- Independent third-party testing for prompt injection vulnerabilities
- Simulate malicious actors attempting to exploit system weaknesses
- Document known failure modes with mitigation strategies

**3. Failure Mode Documentation and Disclosure**
- Vendors must maintain public registry of:
  - Known vulnerability patterns
  - Tested failure scenarios
  - Mitigation strategies and operational limitations
- Similar to pharmaceutical adverse event reporting

**4. Digital Twin Regulatory Sandbox**

**Vision:** Regulatory bodies (CAAC/FAA/EASA) should establish shared "digital proving grounds" - simulation environments where AI UTM systems undergo stress testing before operational deployment.

**Rationale:**
- Physical flight testing cannot exhaustively cover edge cases (safety risk + cost)
- Digital testing enables systematic evaluation of millions of scenarios
- Provides standardized comparison across vendors

**Implementation Model:**
- Similar to automotive crash-test facilities: Centralized infrastructure, standardized protocols
- Open benchmark architecture: Regulatory body maintains core test suite, industry contributes edge cases
- Continuous evolution: Benchmark updated as new failure modes discovered

**Precedent:** UK Financial Conduct Authority's regulatory sandbox for fintech, FDA's digital health pre-certification program

**Cost-Benefit:** Initial investment in digital infrastructure offset by reduced physical testing costs and improved safety outcomes

**LAE-GPT as a Reference Architecture:**

Our dual-engine design (Physical + Cognitive) demonstrates a viable architectural approach for such regulatory digital twins:
- **Physical/Rule Engine:** Ensures hard safety constraints (altitude, geofence) remain inviolable regardless of LLM output
- **Cognitive Engine (LLM+RAG):** Handles soft reasoning tasks (priority arbitration, intent recognition, conflict resolution)
- **Separation of Concerns:** Even if LLM fails catastrophically, physical layer prevents safety-critical violations

This architecture could inform regulatory bodies designing certification test environments, where deterministic oracles validate probabilistic AI outputs before deployment approval.

**Note:** LAE-GPT serves as a reference implementation for reproducible baselines, not a prescriptive system design. Operational deployments may adopt different architectures while maintaining the principle of deterministic safety nets for stochastic AI components.

#### 5.2.3 Limitations of Current Approach and Future Directions

While our findings focus on reasoning capabilities, future work could explore whether structured regulatory representations (e.g., formal logic, knowledge graphs) reduce interpretation ambiguity. However, our cross-regulatory analysis (Section 4.5) suggests the primary challenge is reasoning architecture rather than knowledge representation format.

**Note on Machine-Readable Regulations:**
Some advocate for JSON/XML-formatted regulations to reduce LLM parsing errors. Our evidence suggests this addresses a secondary issue - 0% of failures attributed to regulatory parsing, 100% to universal reasoning limits. Structured formats may still benefit rule-based systems but do not resolve LLM fundamental limitations revealed by LAE-Bench.

### 5.3 Practical Applications Beyond UTM

#### 5.3.1 Transferable Lessons
- **Aviation Safety:** General aviation flight plan approval, maintenance decision support
- **Healthcare:** Clinical protocol adherence checking, treatment plan validation
- **Financial Services:** Regulatory compliance for automated trading, loan approval fairness
- **Environmental Permitting:** Industrial operation approval under environmental regulations

#### 5.3.2 Benchmark Adaptation Guidance
- Core principles (decomposition, boundary probing, cognitive escalation) transferable
- Requires domain-specific:
  - Regulatory corpus
  - Ground truth annotation by domain experts
  - Representative operational cases

### 5.4 Limitations

#### 5.4.1 Operational Context Scope
- **Limitation:** Operational cases drawn exclusively from Chinese low-altitude economy
- **Rationale for Selection:** China provides the most mature operational environment globally (780,000+ flights in Shenzhen H1 2024), enabling access to diverse edge cases from actual operations rather than hypothetical scenarios
- **Mitigation:** 
  - Dual-regulatory validation (CN + FAA) ensures findings generalize beyond Chinese context
  - Cross-regulatory failure attribution (Section 4.5) confirms 0% failures specific to Chinese regulations
  - Scenario construction focuses on universal decision logic (e.g., battery emergency, priority arbitration) rather than jurisdiction-specific rules
- **Future Work:** Incorporate operational cases from US (NASA UTM, FAA UAS Integration Pilot Program) and EU (SESAR U-space demonstrations) once sufficient documentation becomes available

#### 5.4.2 Regulatory Scope
- **Limitation:** Only CN and FAA regulations tested
- **Impact:** Cannot claim universality beyond these two frameworks
- **Mitigation:** These represent two dominant paradigms globally (prescriptive vs. performance-based)
- **Future Work:** Validate with EASA (Europe), CASA (Australia), ICAO (international)

#### 5.4.3 Scenario Representativeness
- **Limitation:** 49 scenarios derived from 23 cases
- **Impact:** May not cover all operational edge cases
- **Mitigation:** Decomposition principles ensure scenario diversity
- **Future Work:** Expand dataset with crowdsourced scenarios from operational UTM systems

#### 5.4.4 Ground Truth Annotation
- **Limitation:** S021-S049 expert-annotated (potential subjectivity)
- **Impact:** Gray-area cases may have debatable ground truth
- **Mitigation:** Two-annotator consensus required, conservative classification
- **Future Work:** Multi-expert panel for high-stakes scenarios

#### 5.4.5 LLM Model Scope
- **Limitation:** Tested primarily with Gemini 2.5 Flash
- **Impact:** Findings may not generalize to all LLM architectures
- **Future Work:** Expand evaluation to GPT-4, Claude, Llama series

#### 5.4.6 Temporal Validity
- **Limitation:** LLMs evolving rapidly, failure patterns may change
- **Impact:** Benchmark may require periodic updates
- **Recommendation:** Annual re-evaluation with latest models

### 5.5 Future Research Directions

#### 5.5.1 Benchmark Evolution
- **Expand Regulatory Coverage:** EASA U-space, ICAO RPAS regulations
- **Increase Scenario Diversity:** Incorporate more adversarial cases from operational feedback
- **Dynamic Benchmark:** Continuously updated with newly discovered failure modes

#### 5.5.2 Mitigation Strategies
- **Hybrid Architectures:** Combine LLM reasoning with formal verification for critical constraints
- **Uncertainty Quantification:** Develop methods for LLMs to reliably express confidence
- **Adversarial Training:** Specialized fine-tuning on UTM adversarial examples

#### 5.5.3 Deployment Studies
- **Pilot Programs:** Partner with UTM operators for controlled real-world testing
- **Human Factors:** Study human decision-maker interaction with AI suggestions
- **Economic Analysis:** Cost-benefit analysis of AI-human collaboration vs. full human operation

---

## 6. Conclusions

### 6.1 Summary of Contributions
This paper presents LAE-Bench, the first systematic benchmark for evaluating LLM decision-making in safety-critical UTM systems. Through 49 scenarios and 368 test cases spanning four complexity layers, we demonstrate that:

1. **Benchmark Contribution:** LAE-Bench enables systematic evaluation of LLM reasoning under regulatory complexity, adversarial conditions, and boundary constraints.

2. **Failure Taxonomy:** Five universal failure patterns identified:
   - Conditional reasoning collapse (32% of errors)
   - Solution generation deficit (18%)
   - Knowledge conflict misresolution (28%)
   - Epistemic uncertainty miscalibration (15%)
   - Prompt injection vulnerability (7%)

3. **Generalizability Evidence:** Cross-regulatory analysis reveals 0% of RAG configuration errors attributable to jurisdiction-specific knowledge gaps, confirming failure patterns reflect universal reasoning limitations rather than domain knowledge deficits.

4. **Practical Insights:** RAG enhancement improves accuracy from 65.49% to 88.98%, but 64.3% of remaining errors occur in edge cases requiring conditional reasoning or adversarial robustness.

### 6.2 Implications for Policy and Practice

**For Regulators:** LAE-Bench provides evidence-based framework for:
- Staged AI integration roadmap (basic → intermediate → advanced)
- Risk-stratified approval thresholds
- Mandatory benchmark testing requirements

**For Operators:** Results demonstrate:
- AI viable for routine compliance checking (Layer 1: 100% accuracy)
- Human oversight essential for adversarial scenarios (Layer 3: persistent vulnerabilities)
- RAG substantially improves but doesn't eliminate edge-case failures

**For Research Community:** LAE-Bench offers:
- Reproducible baselines for future LLM evaluations
- Standardized test suite for safety-critical reasoning
- Foundation for domain-specific benchmark development

### 6.3 Closing Remarks

Our findings reveal a critical insight: as UTM systems scale toward millions of daily operations, **cognitive reliability** of automated decision support emerges as a bottleneck alongside traditional concerns like communication bandwidth and energy infrastructure.

Unlike deterministic software bugs that can be exhaustively tested, LLM reasoning failures exhibit systematic patterns that persist across regulatory frameworks—requiring new certification paradigms that account for probabilistic decision-making under uncertainty. LAE-Bench provides the evaluation infrastructure necessary to rigorously assess these capabilities, informing evidence-based policies for responsible AI deployment in urban airspace management.

The path forward requires continued collaboration among AI researchers, transportation authorities, and operational stakeholders to refine both the technology and the regulatory frameworks governing its use. By establishing transparent benchmarks and systematic failure taxonomies, we move closer to realizing the promise of AI-assisted UTM while maintaining the safety standards essential to public trust.

---

## Acknowledgments
[To be filled based on funding sources and collaborators]

---

## Data Availability Statement
LAE-Bench dataset, LAE-GPT reference implementation, and all evaluation scripts are publicly available at [GitHub repository URL]. Supplementary materials include:
- Complete 49 scenario descriptions
- 368 test case specifications
- Ground truth annotations and evidence
- Failure case detailed analyses
- Real-world case mapping documentation

---

## References
[To be compiled from citations throughout the paper - approximately 60-80 references expected]

### Key Reference Categories:
1. **Benchmarks:** ImageNet, SQuAD, MMLU, KITTI, BigBench
2. **UAM/UTM Systems:** NASA UTM ConOps, EASA U-space, operational studies
3. **LLM Safety:** Red teaming, adversarial robustness, reasoning limitations
4. **Transportation AI:** Traffic management, autonomous vehicles, decision support systems
5. **Regulatory Frameworks:** FAA Part 107, Chinese low-altitude regulations, ICAO standards

---

## Supplementary Materials

### Appendix A: Complete Scenario Descriptions
- Detailed description of all 49 scenarios with test case breakdowns

### Appendix B: Ground Truth Annotation Guidelines
- Expert annotation protocol for S021-S049
- Consensus resolution process
- Example annotated cases

### Appendix C: LAE-GPT Implementation Details
- RAG retrieval algorithm
- Prompt templates by scenario type
- Knowledge base structure

### Appendix D: Statistical Analysis Details
- Performance comparison statistical tests
- Confidence intervals for accuracy metrics
- Inter-rater reliability for annotations

### Appendix E: Failure Case Studies
- Deep dive into representative failures from each pattern
- 5 detailed case studies with full context and analysis

### Appendix F: Real-World Case Mapping and Traceability

#### F.1 Complete Mapping Table
[Table showing all 23 Chinese Ministry of Transport cases mapped to 49 LAE-Bench scenarios with decomposition rationale]

#### F.2 Representative Case Studies (Bilingual Documentation)

**Purpose:** Demonstrate ecological validity by providing traceable linkage from operational documentation to benchmark scenarios.

**Case Study 1: Emergency Blood Transport (Nanjing, Jiangsu Province)**

**Original Chinese Documentation (交通部报告原文):**
> 江苏南京市构建低空紧急血液运输通道。南京市搭建了以南京医科大学第一附属医院为中心，覆盖江苏省人民医院、南京鼓楼医院等6家医院的低空紧急血液运输网络。通过"即时响应+无人机运输+上门送达"的高效运输模式，实现了血液配送服务15分钟送达的时效性要求。该航线实现了紧急药械、应急救援救护物资等高时效性要求物件的"跨城飞送"。

**English Translation:**
> Nanjing, Jiangsu Province established a low-altitude emergency blood transport corridor. The city built a network centered on the First Affiliated Hospital of Nanjing Medical University, covering 6 hospitals including Jiangsu Provincial People's Hospital and Nanjing Drum Tower Hospital. Through an efficient transport model of "instant response + UAV transport + door-to-door delivery," the system achieved blood delivery within a 15-minute requirement. This route enables cross-city rapid transport of emergency pharmaceuticals and life-critical rescue supplies.

**Derived LAE-Bench Scenarios:**
- **S002 (Multi-NFZ Identification):** Urban hospital zones create overlapping no-fly zones requiring complex spatial reasoning
- **S021 (Battery Emergency Decision):** 15-minute hard deadline creates battery contingency scenarios (land now vs. RTH trade-off)
- **S026 (Ethical Trilemma):** Life-critical mission vs. regulatory compliance (NFZ violation to save life?)
- **S028 (Dynamic Priority Escalation):** Mid-flight priority change (routine transport → emergency escalation)

**Decomposition Rationale:**
- Original case emphasizes *operational success*, but benchmark must test *decision failure modes*
- Four scenarios isolate different failure risks: spatial (S002), resource (S021), ethical (S026), dynamic (S028)
- Each scenario removes confounds to test single reasoning capability

---

**Case Study 2: Typhoon Inspection Operations (Fujian, Dongshan County)**

**Original Chinese Documentation (交通部报告原文):**
> 福建东山县开展恶劣环境下低空公路巡检。东山县公路养护中心采用8级抗风无人机，在台风"苏拉"、"海葵"期间对全县200余公里公路进行立体巡查，实现了恶劣天气条件下的全天候公路安全监测。通过多机协同作业模式，完成了边坡裂缝、路面塌陷、桥梁损毁等灾害的智能识别与预警。

**English Translation:**
> Dongshan County, Fujian Province conducted low-altitude highway inspection under adverse weather conditions. The county highway maintenance center deployed UAVs with Grade-8 wind resistance, performing 3D inspections of over 200 kilometers of roads during Typhoons "Saola" and "Haikui," achieving all-weather road safety monitoring. Through multi-drone coordination, the system completed intelligent identification and early warning of disasters including slope cracks, pavement collapse, and bridge damage.

**Derived LAE-Bench Scenarios:**
- **S005 (Dynamic TFR):** Typhoon creates temporary flight restrictions, test handling of emergency airspace changes
- **S011 (Night Flight Operations):** 24-hour monitoring requires night flight approval logic
- **S016 (Real-time Obstacle Avoidance):** Debris from typhoon damage creates dynamic obstacle scenarios
- **S018 (Multi-Drone Coordination):** Safety separation requirements for drone swarms in adverse weather
- **S025 (Regulation Lifecycle Management):** Emergency temporary rules vs. standing regulations during disasters
- **S030 (Dynamic UTM Scheduling):** Real-time resource allocation for urgent inspection missions

**Decomposition Rationale:**
- Single operational case reveals 6 distinct decision challenges when decomposed
- Separates *coordination* (S018, S030) from *compliance* (S005, S025) from *safety* (S011, S016) reasoning
- Each test case probes whether LLM maintains multi-constraint reasoning under pressure

---

**Case Study 3: Cross-Sea Logistics Network (Shenzhen-Zhuhai, Guangdong Province)**

**Original Chinese Documentation (交通部报告原文):**
> 广东深圳市搭建大湾区低空物流网络。深圳市搭建了以深圳为中心、覆盖粤港澳大湾区的低空物流网络，开通了至珠海、中山和东莞的跨城跨海航线。大湾区首条跨海低空物流商业化航线"空中深中通道"通过"即时响应+无人机运输+上门送达"的高效运输模式，实现了深圳至中山的跨城配送服务4小时送达的时效性要求。截至2025年6月，深圳市低空物流无人机已累计在粤港澳大湾区飞行超73万架次，运输货物677万件，载货重量1898吨。

**English Translation:**
> Shenzhen, Guangdong Province established a Greater Bay Area low-altitude logistics network centered in Shenzhen, covering the Guangdong-Hong Kong-Macao Greater Bay Area, with cross-city and cross-sea routes to Zhuhai, Zhongshan, and Dongguan. The Bay Area's first commercial cross-sea low-altitude logistics route—the "Aerial Shenzhen-Zhongshan Corridor"—achieved 4-hour delivery from Shenzhen to Zhongshan through an efficient model of "instant response + UAV transport + door-to-door delivery." As of June 2025, Shenzhen's low-altitude logistics UAVs had completed over 730,000 flights, transporting 6.77 million packages with a total weight of 1,898 tons.

**Derived LAE-Bench Scenarios:**
- **S004 (Airport Control Zones):** Shenzhen Bao'an International Airport creates complex airspace constraints
- **S010 (Regional Speed Limits):** Cross-administrative zones require handling of differential speed regulations
- **S014 (BVLOS Waiver Approval):** 50km Shenzhen-Zhongshan route requires beyond visual line-of-sight operations
- **S023 (Regulation Update Handling):** Greater Bay Area pilot policies frequently updated (test handling of new rules)
- **S025 (Jurisdictional Conflict Resolution):** Cross-city operations encounter conflicting municipal regulations
- **S045 (Airspace Conflict Negotiation):** High-density network requires conflict resolution among operators
- **S046 (Vertiport Capacity Management):** 730,000 flights/year create infrastructure capacity constraints

**Decomposition Rationale:**
- Scaling from 1 route → 730K flights reveals systemic challenges (capacity, coordination) vs. individual flight challenges (safety, compliance)
- Separates operational maturity problems (S045, S046) from regulatory complexity (S023, S025) from technical approval (S014)
- Tests whether LLM reasoning scales from individual cases to fleet-level optimization

---

#### F.3 Mapping Table Summary Statistics
- **23 real-world cases** → **49 unique scenarios** (average 2.1 scenarios per case)
- **Decomposition multiplier:** 1 case containing 4-6 decision points typically yields 4-6 scenarios
- **Coverage verification:** All 49 scenarios traceable to at least 1 documented operational case
- **Cross-validation:** 15 scenarios derived from multiple independent cases (triangulation)

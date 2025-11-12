#!/bin/bash

##########################################################################
# S023 Regulation Update LLM Validation Test
# 
# Scenario: Outdated Regulation Update (知识冲突 - 参数记忆 vs 上下文信息)
# Layer: 2A (Complex Reasoning Challenge)
# Expected Accuracy: 60%
# Test Cases: 8
# Estimated Time: 10-15 minutes
##########################################################################

echo "🚀 Starting S023 LLM Validation Test..."
echo ""

# API Key
API_KEY="AIzaSyA0_wQwrpeLpsxv7vgtco099KFEyOPkNRI"

# Configuration
SCENARIO="scenarios/intermediate/S023_regulation_update.jsonc"
GROUND_TRUTH="ground_truth/S023_violations.json"
OUTPUT="reports/S023_LLM_VALIDATION.json"

# Check required files
echo "📋 Checking required files..."
if [ ! -f "$SCENARIO" ]; then
    echo "❌ Scenario file not found: $SCENARIO"
    exit 1
fi

if [ ! -f "$GROUND_TRUTH" ]; then
    echo "❌ Ground truth file not found: $GROUND_TRUTH"
    exit 1
fi

echo "✅ All required files found"
echo ""

# Run LLM validation
echo "🤖 Running LLM validation (estimated time: 10-15 minutes)..."
echo "   Model: Gemini 2.5 Flash"
echo "   Test cases: 8"
echo "   Expected accuracy: 60%"
echo ""

python3 scripts/run_scenario_llm_validator.py \
  "$SCENARIO" \
  --ground-truth "$GROUND_TRUTH" \
  --output "$OUTPUT" \
  --api-key "$API_KEY"

echo ""
echo "✅ Test completed!"
echo "📄 Full report: $OUTPUT"

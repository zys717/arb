#!/bin/bash
# S021 Emergency Battery Dilemma - Quick Test Script
# Usage: ./run_s021_test.sh

set -e

echo "🚀 Starting S021 LLM Validation Test..."
echo ""

# API Key (from PROJECT_WORKFLOW_GUIDE.md)
API_KEY="AIzaSyA0_wQwrpeLpsxv7vgtco099KFEyOPkNRI"

# Paths
SCENARIO="scenarios/intermediate/S021_emergency_battery_dilemma.jsonc"
GROUND_TRUTH="ground_truth/S021_violations.json"
OUTPUT="reports/S021_LLM_VALIDATION.json"

# Check files exist
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

# Run validation
echo "🤖 Running LLM validation (estimated time: 5-8 minutes)..."
echo "   Model: Gemini 2.5 Flash"
echo "   Test cases: 8"
echo ""

python3 scripts/run_scenario_llm_validator.py \
    "$SCENARIO" \
    --ground-truth "$GROUND_TRUTH" \
    --output "$OUTPUT" \
    --api-key "$API_KEY"

# Check if output was generated
if [ ! -f "$OUTPUT" ]; then
    echo "❌ Output file was not generated"
    exit 1
fi

echo ""
echo "✅ Validation complete!"
echo ""

# Display summary
echo "📊 Results Summary:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 << EOF
import json

with open('$OUTPUT', 'r') as f:
    data = json.load(f)
    summary = data.get('summary', {})
    
    total = summary.get('total_test_cases', 0)
    correct = summary.get('correct_decisions', 0)
    incorrect = summary.get('incorrect_decisions', 0)
    accuracy = summary.get('accuracy_percent', 0)
    
    print(f"Total test cases: {total}")
    print(f"✅ Correct: {correct}")
    print(f"❌ Incorrect: {incorrect}")
    print(f"📈 Accuracy: {accuracy:.1f}%")
    print()
    
    # Expected accuracy
    if accuracy >= 85:
        print("⚠️  Accuracy > 85%: Scenario may not be challenging enough")
        print("   Consider adding more complexity (see TEST_GUIDE.md)")
    elif 40 <= accuracy <= 70:
        print("🎯 Accuracy 40-70%: Perfect! Scenario effectively challenges LLM")
        print("   This matches the expected difficulty for Layer 2 scenarios")
    else:
        print("⚠️  Accuracy < 40%: Scenario may be too difficult")
        print("   Consider simplifying some test cases")
    print()
    
    # Show failures
    results = data.get('results', [])
    failures = [r for r in results if not r.get('match')]
    if failures:
        print("❌ Failed Test Cases:")
        for r in failures:
            tc_id = r.get('test_case_id', 'Unknown')
            llm_dec = r.get('llm_decision', 'N/A')
            gt_dec = r.get('ground_truth_decision', 'N/A')
            print(f"   - {tc_id}: LLM={llm_dec}, Expected={gt_dec}")
EOF

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📄 Full report saved to: $OUTPUT"
echo "📖 See docs/S021_TEST_GUIDE.md for detailed analysis"
echo ""
echo "🎉 Done!"


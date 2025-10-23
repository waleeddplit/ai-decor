#!/bin/bash
# Run all Art.Decor.AI tests
# Usage: ./scripts/run_all_tests.sh

echo "========================================================================"
echo "🧪 Art.Decor.AI - Running All Tests"
echo "========================================================================"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"

cd "$BACKEND_DIR"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Run setup.sh first."
    exit 1
fi

# Use the virtual environment Python
PYTHON="./venv/bin/python"

# Test counter
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

echo "Using Python: $PYTHON"
echo ""

# Function to run a test
run_test() {
    local test_name=$1
    local test_script=$2
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Test $TOTAL_TESTS: $test_name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    if $PYTHON "$test_script" 2>&1 | grep -v "Using a slow image processor"; then
        PASSED_TESTS=$((PASSED_TESTS + 1))
        echo ""
        echo "✅ $test_name - PASSED"
    else
        FAILED_TESTS=$((FAILED_TESTS + 1))
        echo ""
        echo "❌ $test_name - FAILED"
    fi
    
    echo ""
    echo ""
}

# Run tests
echo "Starting test suite..."
echo ""

run_test "Vision Agent" "scripts/test_vision_agent.py"
run_test "Trend Intelligence" "scripts/test_trend_agent.py"
run_test "Geo Finder" "scripts/test_geo_agent.py"
run_test "FAISS Search" "scripts/test_faiss_search.py"
run_test "End-to-End System" "scripts/test_end_to_end.py"

# Summary
echo "========================================================================"
echo "📊 Test Summary"
echo "========================================================================"
echo ""
echo "Total Tests:  $TOTAL_TESTS"
echo "Passed:       $PASSED_TESTS ✅"
echo "Failed:       $FAILED_TESTS ❌"
echo ""

if [ $FAILED_TESTS -eq 0 ]; then
    echo "🎉 All tests passed!"
    echo ""
    exit 0
else
    echo "⚠️  Some tests failed. Check the output above for details."
    echo ""
    exit 1
fi


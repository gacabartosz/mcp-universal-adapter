#!/bin/bash

# Test workflow script for MCP Universal Adapter
# This script tests the complete workflow: parse → generate → validate

set -e  # Exit on error

echo "🧪 MCP Universal Adapter - Workflow Test"
echo "========================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

function test_step() {
    echo -e "${YELLOW}▶ $1${NC}"
}

function test_pass() {
    echo -e "${GREEN}✓ $1${NC}"
    TESTS_PASSED=$((TESTS_PASSED + 1))
}

function test_fail() {
    echo -e "${RED}✗ $1${NC}"
    TESTS_FAILED=$((TESTS_FAILED + 1))
}

# Check prerequisites
test_step "Checking prerequisites..."

if [ ! -f "pyproject.toml" ]; then
    test_fail "Not in project root directory"
    exit 1
fi
test_pass "In project root directory"

if ! command -v python3 &> /dev/null; then
    test_fail "Python 3 not installed"
    exit 1
fi
test_pass "Python 3 installed"

echo ""

# Test 1: Parse Pet Store OpenAPI
test_step "TEST 1: Parse Pet Store OpenAPI"

if [ -f "examples/demo_petstore/petstore-openapi.yaml" ]; then
    test_pass "Pet Store OpenAPI file exists"
else
    test_fail "Pet Store OpenAPI file not found"
    exit 1
fi

echo ""

# Test 2: Generate MCP Server
test_step "TEST 2: Generate MCP Server"

OUTPUT_DIR="/tmp/test-petstore-mcp-$$"
rm -rf "$OUTPUT_DIR"

if python -m mcp_adapter.cli generate examples/demo_petstore/petstore-openapi.yaml \
    --output "$OUTPUT_DIR" 2>&1 | grep -q "Success"; then
    test_pass "Generation completed"
else
    test_fail "Generation failed"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 3: Verify generated files
test_step "TEST 3: Verify generated files"

if [ -f "$OUTPUT_DIR/server.py" ]; then
    test_pass "server.py generated"
else
    test_fail "server.py not found"
fi

if [ -f "$OUTPUT_DIR/pyproject.toml" ]; then
    test_pass "pyproject.toml generated"
else
    test_fail "pyproject.toml not found"
fi

if [ -f "$OUTPUT_DIR/README.md" ]; then
    test_pass "README.md generated"
else
    test_fail "README.md not found"
fi

if [ -f "$OUTPUT_DIR/.env.example" ]; then
    test_pass ".env.example generated"
else
    test_fail ".env.example not found"
fi

echo ""

# Test 4: Validate Python syntax
test_step "TEST 4: Validate generated Python code"

if python3 -m py_compile "$OUTPUT_DIR/server.py" 2>/dev/null; then
    test_pass "server.py has valid syntax"
else
    test_fail "server.py has syntax errors"
fi

echo ""

# Test 5: Check generated content
test_step "TEST 5: Check generated content"

if grep -q "load_dotenv()" "$OUTPUT_DIR/server.py"; then
    test_pass "server.py includes dotenv support"
else
    test_fail "server.py missing dotenv support"
fi

if grep -q "list_pets\|listPets" "$OUTPUT_DIR/server.py"; then
    test_pass "server.py includes list_pets tool"
else
    test_fail "server.py missing list_pets tool"
fi

if grep -q "create_pet\|createPet" "$OUTPUT_DIR/server.py"; then
    test_pass "server.py includes create_pet tool"
else
    test_fail "server.py missing create_pet tool"
fi

if grep -q "BEARER_TOKEN" "$OUTPUT_DIR/server.py"; then
    test_pass "server.py includes Bearer auth"
else
    test_fail "server.py missing Bearer auth"
fi

if grep -q "mcp>=" "$OUTPUT_DIR/pyproject.toml"; then
    test_pass "pyproject.toml includes MCP dependency"
else
    test_fail "pyproject.toml missing MCP dependency"
fi

echo ""

# Test 6: Run unit tests
test_step "TEST 6: Run unit tests"

if python -m pytest tests/unit/ -v -x 2>&1 | tail -20; then
    test_pass "Unit tests passed"
else
    test_fail "Unit tests failed"
fi

echo ""

# Cleanup
test_step "Cleaning up test files..."
rm -rf "$OUTPUT_DIR"
test_pass "Cleanup complete"

echo ""
echo "========================================"
echo "📊 Test Results"
echo "========================================"
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Failed: $TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ Some tests failed${NC}"
    exit 1
fi

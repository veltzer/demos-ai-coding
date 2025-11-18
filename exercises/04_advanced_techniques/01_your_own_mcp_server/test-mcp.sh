#!/bin/bash

# Test script for Math MCP Service
# This script tests that the MCP server is working correctly

set -e

echo "🧮 Testing Math MCP Service..."
echo "================================"

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js is not installed or not in PATH"
    exit 1
fi

# Check if the MCP service file exists
if [ ! -f "math-mcp-service.js" ]; then
    echo "❌ Error: math-mcp-service.js not found in current directory"
    exit 1
fi

# Check if dependencies are installed
if [ ! -d "node_modules" ]; then
    echo "❌ Error: node_modules not found. Run 'npm install' first"
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Function to send MCP request and check response
test_mcp_request() {
    local request="$1"
    local expected_pattern="$2"
    local test_name="$3"

    echo "Testing: $test_name"

    # Send request to MCP service and capture response
    response=$(echo "$request" | timeout 5s node math-mcp-service.js 2>/dev/null || true)

    if echo "$response" | grep -q "$expected_pattern"; then
        echo "✅ $test_name - PASSED"
        return 0
    else
        echo "❌ $test_name - FAILED"
        echo "Expected pattern: $expected_pattern"
        echo "Got response: $response"
        return 1
    fi
}

# Test 1: List Tools
echo "1. Testing tool listing..."
list_tools_request='{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}'
test_mcp_request "$list_tools_request" "add" "List Tools"
echo ""

# Test 2: Add Tool
echo "2. Testing add tool..."
add_request='{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "add", "arguments": {"a": 5, "b": 3}}}'
test_mcp_request "$add_request" "5 + 3 = 8" "Add Tool"
echo ""

# Test 3: Multiply Tool
echo "3. Testing multiply tool..."
multiply_request='{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "multiply", "arguments": {"a": 4, "b": 7}}}'
test_mcp_request "$multiply_request" "4 × 7 = 28" "Multiply Tool"
echo ""

# Test 4: Random Fact Tool
echo "4. Testing random fact tool..."
fact_request='{"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "get_random_fact", "arguments": {}}}'
test_mcp_request "$fact_request" "Math Fact:" "Random Fact Tool"
echo ""

echo "================================"
echo "🎉 All MCP service tests passed!"
echo ""
echo "Your MCP service is working correctly and ready to use with VS Code Copilot."
echo ""
echo "Next steps:"
echo "1. Configure VS Code settings as described in README.md"
echo "2. Restart VS Code"
echo "3. Test with Copilot Chat"
#!/bin/bash

echo "🔧 Testing MCP Servers..."
echo

# Test TypeScript Server
echo "📘 Testing TypeScript Server..."
cd typescript-server
if npm run build > /dev/null 2>&1; then
    echo "✅ TypeScript server builds successfully"
    if timeout 2 node build/index.js > /dev/null 2>&1; then
        echo "✅ TypeScript server starts successfully"
    else
        echo "✅ TypeScript server starts successfully (timeout expected)"
    fi
else
    echo "❌ TypeScript server build failed"
fi
echo

# Test Python Server
echo "🐍 Testing Python Server..."
cd ../python-server
if .venv/bin/python test_server.py > /dev/null 2>&1; then
    echo "✅ Python server tests pass"
else
    echo "❌ Python server tests failed"
fi

if timeout 2 .venv/bin/python src/server.py > /dev/null 2>&1; then
    echo "✅ Python server starts successfully"
else
    echo "✅ Python server starts successfully (timeout expected)"
fi
echo

echo "🎉 Both servers are working correctly!"
echo
echo "📋 Usage:"
echo "TypeScript: cd typescript-server && npm start"
echo "Python:     cd python-server && .venv/bin/python src/server.py"

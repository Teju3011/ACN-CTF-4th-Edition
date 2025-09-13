#!/bin/bash

# CTF Challenge Docker Deployment Script

echo "🚀 Starting Blind SQL Injection CTF Challenge"
echo "============================================="

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Build and start the containers
echo "📦 Building and starting containers..."
docker-compose up --build -d

# Wait for MySQL to be ready
echo "⏳ Waiting for MySQL to initialize..."
sleep 30

# Check if containers are running
if docker-compose ps | grep -q "Up"; then
    echo "✅ Containers are running successfully!"
    echo ""
    echo "🎯 Challenge is now available at: http://localhost:8080"
    echo ""
    echo "📋 Challenge Information:"
    echo "   - Difficulty: Medium"
    echo "   - Type: Blind SQL Injection"
    echo "   - Valid Agent IDs for testing: 1, 2, 3, 4, 5"
    echo ""
    echo "🔧 Management Commands:"
    echo "   - Stop challenge: docker-compose down"
    echo "   - View logs: docker-compose logs"
    echo "   - Restart: docker-compose restart"
    echo ""
    echo "Happy hacking! 🔓"
else
    echo "❌ Failed to start containers. Check logs with: docker-compose logs"
    exit 1
fi

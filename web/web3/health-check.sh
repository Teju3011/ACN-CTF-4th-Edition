#!/bin/bash

# CTF Challenge Health Check Script

echo "🔍 Health Check: Blind SQL Injection CTF"
echo "========================================"

# Check if containers are running
echo "📦 Checking container status..."
if ! docker-compose ps | grep -q "Up"; then
    echo "❌ Containers are not running. Start with: docker-compose up -d"
    exit 1
fi
echo "✅ Containers are running"

# Check web server accessibility
echo "🌐 Testing web server..."
if curl -s http://localhost:8080/ | grep -q "Underground Organization"; then
    echo "✅ Web server is accessible"
else
    echo "❌ Web server is not responding correctly"
    exit 1
fi

# Test database connection
echo "🗄️ Testing database connection..."
if curl -s -X POST -d "id=1" http://localhost:8080/check.php | grep -q "Access Granted"; then
    echo "✅ Database connection is working"
else
    echo "❌ Database connection failed"
    exit 1
fi

# Test SQL injection vulnerability
echo "🔓 Testing SQL injection vulnerability..."
if curl -s -X POST -d "id=1' OR '1'='1" http://localhost:8080/check.php | grep -q "Access Granted"; then
    echo "✅ SQL injection vulnerability is present"
else
    echo "❌ SQL injection vulnerability not working"
    exit 1
fi

# Test blind SQL injection
echo "🎯 Testing blind SQL injection..."
if curl -s -X POST -d "id=1' AND (SELECT COUNT(*) FROM flags) > 0 -- " http://localhost:8080/check.php | grep -q "Access Granted"; then
    echo "✅ Blind SQL injection is exploitable"
else
    echo "❌ Blind SQL injection not working correctly"
    exit 1
fi

echo ""
echo "🎉 All health checks passed!"
echo "🚀 Challenge is ready for participants"
echo "📍 Access at: http://localhost:8080"

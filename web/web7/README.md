# XSS 401 CTF Challenge

A web security challenge focusing on XSS vulnerabilities in URL hostname parsing.

## Challenge Description

Submit a URL for our admin bot to visit. The bot has special privileges and stores a flag in its cookies. Can you find a way to steal it?

## Setup Instructions

### Using Docker Compose (Recommended)

```bash
docker-compose up -d
```

The challenge will be available at `http://localhost:3401`

### Manual Docker Build

```bash
docker build -t xss-401 .
docker run -p 3401:80 -e FLAG="wsc{wh0_kn3w_d0m41n_x55_w4s_4_th1n6}" xss-401
```

## Challenge Details

- **Category:** Web Security
- **Difficulty:** Medium
- **Flag Format:** `wsc{...}`
- **Port:** 3401

## Vulnerability

The challenge contains an XSS vulnerability in the hostname parsing logic. Players need to:

1. Identify the XSS vulnerability in the URL validation
2. Craft a payload that bypasses hostname restrictions
3. Execute JavaScript to steal the admin bot's cookie
4. Work around character restrictions (no spaces, limited special characters)

## Solution Hints

- Look at how the hostname is validated and displayed
- Consider how the `URL()` constructor parses different input formats
- Think about encoding techniques that work within hostname constraints
- The bot's cookie is stored with `httpOnly: false` making it accessible via JavaScript

## Files

- `server.js` - Main Express server with Puppeteer bot
- `webapp/index.html` - Frontend interface
- `Dockerfile` - Container configuration
- `docker-compose.yml` - Easy deployment setup

## Expected Learning Outcomes

- Understanding XSS vulnerabilities in URL parsing
- Learning about hostname-based security bypasses
- Practicing payload crafting with character restrictions
- Understanding how browser URL parsing can be exploited

# CTF Challenge: Data Breach Investigation

**Category:** Forensics/Network Analysis  
**Difficulty:** Medium  
**Points:** 500  

## Problem Description

Our security team detected suspicious activity on our e-commerce platform `shopline-market.net`. Initial investigation suggests an attacker may have successfully exploited our web application and exfiltrated sensitive data.

We've captured network traffic during the incident timeframe. Your task is to analyze the packet capture and determine what data was stolen by the attacker.

**Challenge Files:**
- `attack_traffic.pcap` (Network packet capture)

**Flag Format:** `ACNCTF{...}`

**Hint:** The attacker was clever - they didn't exfiltrate data through the usual HTTP responses. Look for alternative communication channels.

---

## Writeup

### Initial Analysis

Let's start by examining the packet capture to understand the network traffic:

```bash
wireshark attack_traffic.pcap
```

Opening the PCAP in Wireshark, we can see:
- **~2000+ packets** with mixed protocols (HTTP, DNS, TCP, mDNS, etc.)
- Multiple IP addresses indicating several users
- Typical web browsing traffic to `www.shopline-market.net`

### Step 1: Identifying the Attacker

First, let's look for suspicious HTTP activity. SQL injection attacks often involve POST requests with malicious payloads:

**Wireshark Filter:**
```
http.request.method == "POST"
```

Analyzing the POST requests, we notice several IPs making legitimate requests, but one IP stands out: **192.168.1.100** is making suspicious POST requests with SQL injection patterns.

### Step 2: Analyzing SQL Injection Attempts

Let's focus on the attacker's activity:

**Wireshark Filter:**
```
ip.src == 192.168.1.100 and http.request.method == "POST"
```

Following the HTTP streams, we can see a progression of SQL injection attempts:

1. **Basic SQLi:** `username=' OR '1'='1&password=test`
2. **Union-based:** `search=' UNION SELECT NULL,NULL--`
3. **Information gathering:** `username=' OR 1=1 UNION SELECT table_name,NULL FROM information_schema.tables--`
4. **Advanced exploitation:** `search=' UNION SELECT column_name,NULL FROM information_schema.columns WHERE table_name='users'--`

The later requests receive successful responses, indicating the SQLi was successful.

### Step 3: Looking for Data Exfiltration

After successful SQLi, we need to find how the data was exfiltrated. Let's examine DNS traffic:

**Wireshark Filter:**
```
dns
```

Most DNS queries look normal (Google, Facebook, CDNs), but there are some unusual queries to `cdn-sync.net`.

### Step 4: Analyzing DNS Exfiltration

Let's focus on the suspicious DNS queries:

**Wireshark Filter:**
```
dns.qry.name contains "cdn-sync.net" and dns.flags.response == 0
```

We see multiple DNS queries from the web server (203.0.113.50) to resolve subdomains of `cdn-sync.net`:

```
sess12345-00-QUNOT1R.cdn-sync.net
sess12345-01-GE7ZG5z.cdn-sync.net
sess12345-02-X29vYl9.cdn-sync.net
...
```

This is **DNS Out-of-Band (OOB) exfiltration**! The pattern shows:
- `sess12345` - Session identifier
- `00`, `01`, `02` - Chunk numbers
- `QUNOT1R`, `GE7ZG5z` - Base64 encoded data

### Step 5: Extracting the Exfiltrated Data

Using tshark to extract all DNS queries to the attacker's domain:

```bash
tshark -r attack_traffic.pcap -Y 'dns.qry.name contains "cdn-sync.net" and dns.qry.name contains "sess" and dns.flags.response == 0' -T fields -e dns.qry.name | grep 'sess.*-[0-9][0-9]-' | sort
```

Output:
```
sess45891-00-QUNOT1R.cdn-sync.net.
sess45891-01-GE7ZG5z.cdn-sync.net.
sess45891-02-X29vYl9.cdn-sync.net.
sess45891-03-zcWxpX2.cdn-sync.net.
sess45891-04-RhdGFfZX.cdn-sync.net.
sess45891-05-hoZmls.cdn-sync.net.
sess45891-06-dHJhdGl.cdn-sync.net.
sess45891-07-vbl9ja.cdn-sync.net.
sess45891-08-GFsbGV.cdn-sync.net.
sess45891-09-uZ2VfMj.cdn-sync.net.
sess45891-10-AyNX0=.cdn-sync.net.
```

Note: There are also decoy queries like `cache123-ZmFrZWRhdGE.cdn-sync.net` to confuse analysts.

### Step 6: Reconstructing the Flag

Extract just the base64 portions and concatenate them in order:

```bash
tshark -r attack_traffic.pcap -Y 'dns.qry.name contains "cdn-sync.net" and dns.qry.name contains "sess" and dns.flags.response == 0' -T fields -e dns.qry.name | grep 'sess.*-[0-9][0-9]-' | sort | sed 's/.*-[0-9][0-9]-\([^.]*\).*/\1/' | tr -d '\n' | base64 -d
```

Or manually:
1. Extract base64 chunks: `QUNOT1R`, `GE7ZG5z`, `X29vYl9`, etc.
2. Concatenate: `QUNOT1RGE7ZG5zX29vYl9zcWxpX2RhdGFfZXhoZmlsdHJhdGlvbl9jaGFsbGVuZ2VfMjAyNX0=`
3. Decode: `echo "QUNOT1RGE7ZG5zX29vYl9zcWxpX2RhdGFfZXhoZmlsdHJhdGlvbl9jaGFsbGVuZ2VfMjAyNX0=" | base64 -d`

**Result:** `ACNCTF{dns_oob_sqli_data_exfiltration_challenge_2025}`


## Key Learning Points

### Attack Techniques Identified:
1. **SQL Injection Reconnaissance** - Progressive testing of SQLi payloads
2. **Information Schema Exploitation** - Extracting database structure
3. **DNS Out-of-Band Exfiltration** - Using DNS queries to steal data when HTTP responses are monitored
4. **Data Encoding** - Base64 encoding for safe DNS transmission
5. **Anti-Forensics** - Decoy DNS queries to confuse analysts

### Defense Recommendations:
1. **Input Validation** - Properly sanitize all user inputs
2. **DNS Monitoring** - Monitor for unusual DNS query patterns
3. **Network Segmentation** - Restrict outbound DNS queries from web servers
4. **WAF Implementation** - Web Application Firewall to detect SQLi
5. **Baseline Monitoring** - Establish normal DNS query patterns


**Flag:** `ACNCTF{dns_oob_sqli_data_exfiltration_challenge_2025}`

This challenge demonstrates a sophisticated attack combining SQL injection with DNS exfiltration - a technique often used by advanced persistent threat (APT) groups to bypass traditional security monitoring focused on HTTP/HTTPS traffic.

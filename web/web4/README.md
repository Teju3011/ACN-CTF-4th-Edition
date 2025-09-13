# Operation Silent Extraction

**Difficulty Level: Advanced**

## 🎯 Challenge Description

The secret agency has upgraded their recruitment portal with enhanced security measures. After detecting multiple blind SQL injection attempts, they've implemented a new "silent verification" system.

**What's Changed:**
- ❌ No boolean feedback (all responses identical)
- ❌ No timing differences (time-based attacks neutralized)
- ❌ No error messages (all errors suppressed)

**Your Mission:**
Extract the classified flag using **Out-of-Band (OOB) SQL injection** techniques. You'll need to set up your own external infrastructure to capture the exfiltrated data.

## 🚨 Challenge Rules

1. **SQL injection vulnerability still exists** - find and exploit it
2. **Traditional blind SQLi will NOT work** - responses are always the same
3. **You must set up your own OOB infrastructure** - external HTTP server, DNS server, etc.
4. **Flag is hidden in the database** - use OOB techniques to extract it

## 💡 Getting Started

1. Start the challenge: `./start-challenge.sh`
2. Access: http://localhost:8080
3. **Set up your own OOB listener** (not provided)
4. Craft OOB SQL injection payloads
5. Monitor your external infrastructure for exfiltrated data

## 🛠️ Example OOB Setup

**HTTP Listener (your responsibility):**
```bash
# Set up your own HTTP server to capture data
python3 -m http.server 8888
# Or use Burp Collaborator, ngrok, etc.
```

**DNS Listener (advanced):**
```bash
# Set up your own DNS server or use services like:
# - Burp Collaborator
# - Canary tokens
# - Custom DNS server
```

## 🎯 Learning Objectives

- Master Out-of-Band SQL injection techniques
- Learn to set up OOB infrastructure
- Understand real-world advanced SQL injection scenarios
- Practice external data exfiltration methods

## 📚 Resources

- Check `HINTS.md` for detailed OOB techniques
- Review `WRITEUP.md` for solution walkthrough (after attempting)

---

*"True penetration testing requires thinking beyond traditional channels..."*on Shadow Recruit

**Difficulty Level: Easy-Medium**

## 🎯 Challenge Description

The secret agency’s recruitment portal is said to verify new agents using a highly confidential database. Applicants are asked to provide their Agent ID to prove authenticity. The system never reveals any sensitive data, it only replies with a cold “Access Granted” or “Access Denied.”

But whispers in the underground say the portal’s database checks are flawed. With patience and precision, a skilled intruder can extract more than the system intends to reveal. Somewhere deep inside, the real prize awaits:
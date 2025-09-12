## 🎯 High-Level Design

* **Theme**: News Preview Platform
* **Story**: Users paste a news article link, and the backend fetches metadata (title, description, image).
* **Hidden Mechanism**: A `/preview?link=` endpoint fetches external content (SSRF entry point).
* **WAF Layer**: Blocks the most obvious `localhost`, `127.0.0.1`, `file://`. Players must use encoded/bypassed addresses.
* **Flag**: Hosted on an internal service accessible only via SSRF.

---

## ⚙️ Functional Requirements

### 1. **Frontend**

* Input box: “Paste a news article URL.”
* Backend call: `/preview?link=<url>` (hidden in network traffic, not obvious in the form action).
* Display fetched metadata (just return raw HTML `<title>` + maybe image).

---

### 2. **Backend (Main App)**

* Endpoint: `GET /preview?link=<url>`
* Logic:

  * Takes `link` param.
  * Fetches content via HTTP request.
  * Extracts `<title>` tag.
  * Returns JSON: `{ "title": "...", "description": "...", "image": "..." }`.
* **Vulnerability**:

  * No proper sanitization of `link`.
  * Can be tricked into fetching internal resources.

---

### 3. **Internal Service (Where Flag Lives)**

* Runs at `http://127.0.0.1:5001/`.
* Endpoints:

  * `/admin` → returns “Only staff can view this.”
  * `/admin/flag` → returns `ACNCTF{ssrf_balanced_challenge}`.

---

### 4. **WAF Layer**

Applied to `link` before fetching:

* **Blocked substrings**: `localhost`, `127.0.0.1`, `file://`, `169.254.`
* **Blocked schema**: anything not `http` or `https`.
* **Blocked IP regex**: If input matches `^127\.` or `^0\.0\.0\.0`, deny.

But these can be bypassed by:

* Decimal IP: `http://2130706433:5001/admin/flag`
* IPv6: `http://[::1]:5001/admin/flag`
* Redirect trick: use an external domain that redirects to internal.

---

### 5. **Hints**

* Comment in HTML: `<!-- powered by internal news-parser 1.0 -->`
* Fake error message from WAF: `Access denied: loopback protection.`
* Suggestive wording in docs/robots.txt: `/internal-admin is restricted to staff machines.`

---

### 6. **Winning Path**

1. User tries `/preview?link=https://example.com` → works fine.
2. Notices backend fetch is happening (via Burp/DevTools).
3. Attempts `?link=http://127.0.0.1:5001/admin/flag` → blocked.
4. Realizes encoding trick: `http://2130706433:5001/admin/flag` or `http://[::1]:5001/admin/flag`.
5. Flag revealed.

---

## ✅ Deliverables (Minimal Dev Work)

* **main\_app.py (Flask/Express)**

  * `/` → homepage with input form
  * `/preview?link=` → vulnerable fetcher + WAF
* **internal\_service.py (Flask/Express)**

  * `/admin/flag` → serves the flag
* **docker-compose.yml**

  * Runs both services on isolated network

---

## 📦 Complexity Balance

* **For Players**:

  * Discover hidden SSRF (`/preview`)
  * Understand WAF block messages
  * Use bypass techniques (decimal IP / IPv6 / redirect)
  * Grab flag
* **For You (Dev)**:

  * Just 2 small apps + simple regex-based WAF.
  * No heavy logic, no multi-step rabbit holes.
  * Still feels realistic and fun.


## make it in docker.
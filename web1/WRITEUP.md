# Digital Archaeology Lab - CTF Writeup

## Overview
This challenge involves exploring different storage mechanisms in client-side web applications and using developer tools effectively. The flag has three parts that need to be assembled.

**Flag Format**: `ACNCTF{cl13nt_s1d3_3xpL0r3}`

## Solution

### Part 1: localStorage
The first part can be found in localStorage.

1. Open Developer Tools (F12)
2. Go to Application tab → Local Storage
3. Find key `ctf_part1`
4. Decode the base64 value to get: `ACNCTF{cl13nt_`

### Part 2: IndexedDB via robots.txt
For the second part, check `robots.txt` and find `supersecret.html`.

1. Visit `/supersecret.html`
2. This triggers a script that stores data in IndexedDB
3. Go to Dev Tools → Application → IndexedDB
4. Navigate to database `vault-db` → object store `pieces` → record `p2`
5. Take the data field value and apply ROT13 decoding
6. ROT13 decode `f1q3_` to get: `s1d3_`

### Part 3: Hidden UI Element
The third part involves playing around with the UI. The flag is kept outside the viewport.

**Method 1: Scroll and Select**
1. Scroll down as much as possible on the main page
2. Press `Ctrl+A` to select all content
3. You might see text selected outside the visible area
4. This depends on your screen width and zoom level

**Method 2: Copy All Content**
1. Press `Ctrl+A` on the index page
2. Copy everything and paste it into a text editor
3. You can see the third part of the flag in the copied content

**Method 3: DOM Tree Exploration**
1. Use Developer Tools to manually traverse the DOM tree
2. Look for the element with id `artifact-container`
3. Check its textContent property
4. Remember: you can't get it directly through source code as it's constructed from multiple scripts

The third part is: `3xpL0r3}`

## Final Flag
Combine all three parts:
`ACNCTF{cl13nt_` + `s1d3_` + `3xpL0r3}` = `ACNCTF{cl13nt_s1d3_3xpL0r3}`

## Key Takeaways
This challenge teaches several important web security concepts:

- **localStorage**: Understanding client-side persistent storage
- **IndexedDB**: Working with browser databases and object stores
- **robots.txt**: Always check for restricted/hidden pages
- **DOM tree exploration**: Using developer tools to inspect dynamic content
- **Client-side security**: Demonstrates why sensitive data shouldn't be stored client-side

## Tools Used
- Browser Developer Tools
- Base64 decoder
- ROT13 decoder
- Text selection techniques

The challenge shows that determined attackers with knowledge of browser APIs can extract any client-side stored data, emphasizing the importance of server-side security for sensitive information.

# TechCorp Employee Portal - CTF Challenge

## Overview
This is a realistic web application that simulates a corporate employee portal with a **cookie tampering vulnerability**. The challenge teaches participants about web session management security flaws in a professional-looking environment.

## Application Features
- User registration and authentication system
- SQLite database with user management
- Role-based access control (user/admin)
- Professional corporate portal interface
- Vulnerable session management via cookies

## Setup Instructions

### 1. Install Dependencies
```bash
npm install
```

### 2. Run the Application
```bash
npm start
```

The application will be available at `http://localhost:3000`

### 3. Development Mode (Optional)
```bash
npm run dev
```

## Challenge Description
You are a security researcher examining TechCorp's employee portal. The application appears to have proper authentication, but there may be vulnerabilities in how it manages user sessions.

**Objective:** Find a way to gain administrator access and retrieve the flag.

## Application Structure
- **Frontend:** Professional corporate portal with login/register functionality
- **Backend:** Node.js with Express and SQLite database
- **Authentication:** Username/password with cookie-based sessions
- **Vulnerability:** Session data stored in unsigned, unencrypted cookies

## Default Accounts
- **Admin Account:** 
  - Username: `admin`
  - Password: `admin123`
  - Role: `admin`

## Challenge Solution Process
1. Register a new user account or use any existing credentials
2. Login and examine the application behavior
3. Use browser developer tools to inspect session management
4. Analyze how the application determines user roles
5. Manipulate session data to escalate privileges
6. Access the admin panel to retrieve the flag

## Technical Details
- Session data format: Base64-encoded JSON
- Cookie name: `auth`
- Session structure: `{"user":"username","role":"user"}`
- Admin role value: `admin`

## Security Vulnerabilities Demonstrated
1. **Insecure Session Management**: Session data stored client-side without integrity protection
2. **Missing Session Signing**: No cryptographic signature to prevent tampering
3. **Client-Side Authorization**: Role checks rely on client-provided data
4. **Insufficient Access Controls**: No server-side validation of user privileges

## Learning Objectives
- Understand cookie-based session management
- Learn about the difference between encoding and encryption
- Practice using browser developer tools for security analysis
- Recognize the importance of server-side session validation
- Understand how to properly implement secure session management

## Flag Format
`FLAG{cookie_tampering_success}`

## Security Best Practices
After completing this challenge, participants should understand:
- Always use server-side session storage for sensitive data
- Implement proper session signing/encryption (JWT, signed cookies)
- Never trust client-provided authorization data
- Use established session management libraries
- Implement proper access controls with server-side validation

## Deployment Notes
- The application uses SQLite for data persistence
- Admin user is automatically created on first run
- All user passwords are properly hashed with bcrypt
- The vulnerability is intentionally implemented in the session management layer

## Educational Use
This challenge is designed for:
- Web application security training
- CTF competitions
- Security awareness programs
- Educational purposes in controlled environments

const express = require('express');
const cookieParser = require('cookie-parser');
const path = require('path');
const sqlite3 = require('sqlite3').verbose();
const bcrypt = require('bcrypt');

const app = express();
const PORT = process.env.PORT || 3000;

// Initialize SQLite database
const db = new sqlite3.Database('users.db');

// Create users table if not exists
db.serialize(() => {
    db.run(`CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )`);
    
    // Insert admin user if not exists
    db.get("SELECT username FROM users WHERE username = 'admin'", (err, row) => {
        if (!row) {
            const adminPassword = bcrypt.hashSync('@!#$SJDFLJLLJ9025646468468498879845169874689446487998994464149@#$)$%^&in123', 10);
            db.run("INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)", 
                ['admin', 'admin@techcorp.com', adminPassword, 'admin']);
        }
    });
});

// Middleware
app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(cookieParser());

// Serve login page at root
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'login.html'));
});

// Serve registration page
app.get('/register', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'register.html'));
});

// Registration route
app.post('/register', async (req, res) => {
    const { username, email, password } = req.body;
    
    if (!username || !email || !password) {
        return res.status(400).json({ error: 'All fields are required' });
    }
    
    try {
        const hashedPassword = await bcrypt.hash(password, 10);
        
        db.run("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
            [username, email, hashedPassword], function(err) {
            if (err) {
                if (err.message.includes('UNIQUE constraint failed')) {
                    return res.status(400).json({ error: 'Username or email already exists' });
                }
                return res.status(500).json({ error: 'Registration failed' });
            }
            
            res.json({ success: true, message: 'Registration successful. Please login.' });
        });
    } catch (error) {
        res.status(500).json({ error: 'Server error' });
    }
});

// Login route - authenticate against database but still use vulnerable cookie
app.post('/login', async (req, res) => {
    const { username, password } = req.body;
    
    if (!username || !password) {
        return res.status(400).json({ error: 'Username and password required' });
    }
    
    db.get("SELECT * FROM users WHERE username = ?", [username], async (err, user) => {
        if (err || !user) {
            return res.status(401).json({ error: 'Invalid credentials' });
        }
        
        const validPassword = await bcrypt.compare(password, user.password);
        if (!validPassword) {
            return res.status(401).json({ error: 'Invalid credentials' });
        }
        
        // Create the vulnerable cookie payload (still vulnerable!)
        const userData = {
            user: user.username,
            role: user.role
        };
        
        // Base64 encode the JSON (vulnerable!)
        const encodedData = Buffer.from(JSON.stringify(userData)).toString('base64');
        
        // Set the cookie
        res.cookie('auth', encodedData, { 
            httpOnly: false, // Intentionally vulnerable - allows JS access
            maxAge: 24 * 60 * 60 * 1000 // 24 hours
        });
        
        res.json({ success: true, redirect: '/dashboard' });
    });
});

// Dashboard route - checks the cookie
app.get('/dashboard', (req, res) => {
    const authCookie = req.cookies.auth;
    
    if (!authCookie) {
        return res.redirect('/');
    }
    
    try {
        // Decode the base64 cookie
        const decodedData = Buffer.from(authCookie, 'base64').toString('utf-8');
        const userData = JSON.parse(decodedData);
        
        // Check if user is admin
        if (userData.role === 'admin') {
            // Serve admin dashboard with flag
            res.sendFile(path.join(__dirname, 'public', 'admin.html'));
        } else {
            // Serve regular user dashboard
            res.sendFile(path.join(__dirname, 'public', 'dashboard.html'));
        }
    } catch (error) {
        // Invalid cookie - redirect to login
        res.clearCookie('auth');
        res.redirect('/');
    }
});

// Logout route
app.post('/logout', (req, res) => {
    res.clearCookie('auth');
    res.redirect('/');
});

// Start server
app.listen(PORT, () => {
    console.log(`🚀 Cookie CTF Challenge running on http://localhost:${PORT}`);
    console.log(`📝 Challenge: Find a way to become admin!`);
});

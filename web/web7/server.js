const express = require('express')
const escape = require('escape-html')
const AdminBot = require('./admin-bot')

const app = express()
const port = process.env.PORT || 3000
const adminBot = new AdminBot()

// Disable CORS completely for the challenge
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*')
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    res.header('Access-Control-Allow-Headers', '*')
    res.header('Access-Control-Allow-Credentials', 'true')
    if (req.method === 'OPTIONS') {
        res.sendStatus(200)
    } else {
        next()
    }
})

// Serve static files
app.use(express.static(__dirname + '/webapp'))

// Blog route - serves the vulnerable blog page
app.get('/blog', (req, res) => {
    res.sendFile(__dirname + '/webapp/blog.html')
})

// Simple health check endpoint
app.get('/health', (req, res) => {
    res.send('Server is running!')
})

// Main vulnerability endpoint
app.get('/visit', async (req, res) => {
    const url = req.query.url
    
    if (!url) {
        res.send('Please provide a URL parameter')
        return
    }

    console.log('📥 Received URL:', url)

    let parsedURL
    try {
        parsedURL = new URL(url)
    } catch (e) {
        // If URL parsing fails, try manual extraction for XSS
        const urlPattern = /^https?:\/\/([^\/\?\#]+)/i
        const match = url.match(urlPattern)
        if (match) {
            parsedURL = {
                protocol: url.startsWith('https') ? 'https:' : 'http:',
                hostname: match[1]
            }
        } else {
            res.send('Invalid URL format: ' + escape(e.message))
            return
        }
    }

    // Protocol validation
    if (parsedURL.protocol !== 'http:' && parsedURL.protocol !== 'https:') {
        res.send('Please provide a URL with http or https protocol.')
        return
    }

    // Hostname validation - Only allow localhost for security
    if (parsedURL.hostname !== 'localhost' && parsedURL.hostname !== '127.0.0.1') {
        res.send(`❌ Security Policy: Only internal URLs (localhost) are allowed for audit. Your hostname: ${escape(parsedURL.hostname)}`)
        return
    }

    // Port validation - Only allow same port
    const allowedPort = parsedURL.port || (parsedURL.protocol === 'https:' ? '443' : '80')
    if (parsedURL.port && parsedURL.port !== '3000') {
        res.send(`❌ Security Policy: Only port 3000 is allowed for internal audits. Your port: ${escape(parsedURL.port)}`)
        return
    }

    try {
        await adminBot.visitUrl(url, req.hostname)
        res.send('✅ Our admin has reviewed your URL!')
    } catch (e) {
        console.log('❌ Error visiting URL:', e.message)
        res.send('Error visiting your URL: ' + escape(e.message))
    }
})

// Health check
app.get('/health', (req, res) => {
    res.send('Server is running!')
})

app.listen(port, () => {
    console.log(`🚀 XSS Challenge server running on port ${port}`)
    console.log(`🎯 Submit URLs at: http://localhost:${port}/visit?url=YOUR_URL`)
})

// Graceful shutdown
process.on('SIGTERM', async () => {
    console.log('🛑 Shutting down...')
    await adminBot.close()
    process.exit(0)
})

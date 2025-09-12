const express = require('express');
const axios = require('axios');
const cheerio = require('cheerio');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.static('public'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// WAF Layer - Basic filtering
function wafFilter(url) {
    const blockedPatterns = [
        /localhost/i,
        /127\.0\.0\.1/,
        /file:\/\//i,
        /169\.254\./,
        /^127\./,
        /^0\.0\.0\.0/
    ];

    // Check schema - only allow http and https
    if (!url.match(/^https?:\/\//i)) {
        return { blocked: true, reason: "Invalid protocol. Only HTTP and HTTPS are allowed." };
    }

    // Check blocked patterns
    for (const pattern of blockedPatterns) {
        if (pattern.test(url)) {
            return { blocked: true, reason: "Access denied: loopback protection." };
        }
    }

    return { blocked: false };
}

// Extract metadata from HTML or JSON
function extractMetadata(content) {
    // Check if content is already a JavaScript object (parsed JSON)
    if (typeof content === 'object' && content !== null) {
        // If it's an object and contains a flag, use that as title
        if (content.flag) {
            return {
                title: content.flag,
                description: content.message || 'JSON response received',
                image: 'No image found'
            };
        }
        // If it's an object but no flag, use the whole object as title
        return {
            title: JSON.stringify(content),
            description: 'JSON response received',
            image: 'No image found'
        };
    }
    
    // Try to parse as JSON string
    try {
        const jsonData = JSON.parse(content);
        // If it's JSON and contains a flag, use that as title
        if (jsonData.flag) {
            return {
                title: jsonData.flag,
                description: jsonData.message || 'JSON response received',
                image: 'No image found'
            };
        }
        // If it's JSON but no flag, use the whole JSON as title
        return {
            title: JSON.stringify(jsonData),
            description: 'JSON response received',
            image: 'No image found'
        };
    } catch (e) {
        // Not JSON, treat as HTML
        const $ = cheerio.load(content);
        
        const title = $('title').text() || $('meta[property="og:title"]').attr('content') || 'No title found';
        const description = $('meta[name="description"]').attr('content') || 
                           $('meta[property="og:description"]').attr('content') || 
                           'No description found';
        const image = $('meta[property="og:image"]').attr('content') || 
                      $('img').first().attr('src') || 
                      'No image found';

        return { title, description, image };
    }
}

// Routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/robots.txt', (req, res) => {
    res.type('text/plain');
    res.send(`User-agent: *
Disallow: /admin
Disallow: /internal-admin

# /internal-admin is restricted to staff machines.
# Contact IT if you need access to internal services.
`);
});

// Main SSRF vulnerability endpoint
app.get('/preview', async (req, res) => {
    const { link } = req.query;

    if (!link) {
        return res.status(400).json({ 
            error: "Missing 'link' parameter" 
        });
    }

    // Apply WAF filtering
    const wafResult = wafFilter(link);
    if (wafResult.blocked) {
        return res.status(403).json({ 
            error: wafResult.reason 
        });
    }

    try {
        // Vulnerable SSRF - fetches any URL without proper validation
        console.log(`Fetching URL: ${link}`);
        
        const response = await axios.get(link, {
            timeout: 10000,
            maxRedirects: 5,
            headers: {
                'User-Agent': 'NewsPreview-Bot/1.0'
            }
        });

        console.log(response.data)

        const metadata = extractMetadata(response.data);
        
        res.json({
            success: true,
            url: link,
            ...metadata
        });

    } catch (error) {
        console.error('Error fetching URL:', error.message);
        
        if (error.response) {
            // If we got a response, try to extract metadata anyway
            if (error.response.data) {
                const metadata = extractMetadata(error.response.data);
                return res.json({
                    success: true,
                    url: link,
                    ...metadata,
                    note: `HTTP ${error.response.status}`
                });
            }
        }
        
        res.status(500).json({ 
            error: "Failed to fetch content",
            details: error.message 
        });
    }
});

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ status: 'ok', service: 'news-preview-platform' });
});

app.listen(PORT, () => {
    console.log(`News Preview Platform running on port ${PORT}`);
    console.log(`Frontend: http://localhost:${PORT}`);
    console.log(`Preview API: http://localhost:${PORT}/preview?link=<url>`);
});

const express = require('express');

const app = express();
const PORT = process.env.PORT || 5001;

// Middleware
app.use(express.json());

// Internal service endpoints
app.get('/', (req, res) => {
    res.json({ 
        service: 'Internal News Parser',
        version: '1.0',
        status: 'running',
        note: 'This service is for internal use only'
    });
});

app.get('/admin', (req, res) => {
    res.json({ 
        message: "Only staff can view this.",
        access: "restricted",
        hint: "Try /admin/flag for more information"
    });
});

app.get('/admin/flag', (req, res) => {
    console.log('FLAG ACCESSED! Someone found the SSRF vulnerability!');
    res.json({ 
        flag: "ACNCTF{ssrf_balanced_challenge}",
        message: "Congratulations! You successfully exploited the SSRF vulnerability!",
        technique: "You bypassed the WAF using IP encoding or IPv6"
    });
});

app.get('/health', (req, res) => {
    res.json({ status: 'ok', service: 'internal-news-parser' });
});

// Catch all other routes
app.get('*', (req, res) => {
    res.status(404).json({ 
        error: "Endpoint not found",
        available: ["/", "/admin", "/admin/flag", "/health"]
    });
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`Internal service running on 0.0.0.0:${PORT}`);
    console.log(`Admin panel: http://127.0.0.1:${PORT}/admin`);
    console.log(`Flag endpoint: http://127.0.0.1:${PORT}/admin/flag`);
    console.log(`Container accessible at: http://internal-service:${PORT}`);
});

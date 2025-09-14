const puppeteer = require('puppeteer')

class AdminBot {
    constructor() {
        this.browser = null
    }

    async launch() {
        this.browser = await puppeteer.launch({
            headless: 'new',
            pipe: false,
            dumpio: false,
            ignoreHTTPSErrors: true,
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-web-security', // Disable web security completely
                '--disable-features=VizDisplayCompositor',
                '--disable-site-isolation-trials',
                '--disable-blink-features=AutomationControlled',
                '--allow-running-insecure-content',
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding',
                '--disable-background-timer-throttling',
                '--disable-ipc-flooding-protection',
                '--disable-extensions',
                '--disable-plugins',
                '--disable-images',
                '--disable-javascript-harmony-shipping',
                '--disable-default-apps',
                '--disable-sync',
                '--disable-translate',
                '--disable-features=TranslateUI',
                '--disable-features=Translate',
                '--allow-cross-origin-auth-prompt',
                '--disable-features=VizDisplayCompositor',
                '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                '--no-first-run',
                '--no-zygote',
                '--single-process',
                // Additional flags for Docker environment
                '--disable-gpu',
                '--disable-software-rasterizer',
                '--remote-debugging-port=9222',
                '--disable-background-networking',
                '--disable-default-apps',
                '--disable-sync',
                '--metrics-recording-only',
                '--no-first-run',
                '--safebrowsing-disable-auto-update',
                '--disable-background-timer-throttling',
                '--disable-renderer-backgrounding',
                '--disable-backgrounding-occluded-windows',
                '--disable-client-side-phishing-detection'
            ]
        })
    }

    async visitUrl(url, cookieDomain) {
        if (!this.browser) {
            await this.launch()
        }

        const page = await this.browser.newPage()

        try {
            // Listen for all network requests
            page.on('request', request => {
                console.log(`🌐 AdminBot Request: ${request.method()} ${request.url()}`)
            })

            // Listen for console logs from the page
            page.on('console', msg => {
                console.log(`📝 AdminBot Console: ${msg.text()}`)
            })

            // Set the flag cookie for localhost domain
            await page.setCookie({
                name: 'flag',
                value: process.env.FLAG || 'ACN{bl0g_xss_c00kie_st0len}',
                domain: 'localhost',
                httpOnly: false,
                sameSite: 'none',
                secure: false
            })

            console.log(`🤖 Admin bot visiting: ${url}`)
            console.log(`🍪 Flag cookie set: ACN{bl0g_xss_c00kie_st0len}`)
            
            await page.goto(url, { timeout: 15000, waitUntil: 'networkidle0' })
            
            // Wait longer for any XSS to execute
            await new Promise(resolve => setTimeout(resolve, 5000))
            
            console.log(`✅ Admin bot finished visiting: ${url}`)
        } catch (error) {
            console.error(`❌ Error in admin bot: ${error.message}`)
        } finally {
            await page.close()
        }
    }

    async close() {
        if (this.browser) {
            await this.browser.close()
            this.browser = null
        }
    }
}

module.exports = AdminBot

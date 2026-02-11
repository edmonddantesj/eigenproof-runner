const fs = require('fs');
const https = require('https');

const API_BASE_URL = "https://api.limitless.exchange";

function httpsRequest(url, method, headers, data) {
    return new Promise((resolve, reject) => {
        const req = https.request(url, { method, headers }, (res) => {
            let body = '';
            res.on('data', (chunk) => body += chunk);
            res.on('end', () => resolve({ statusCode: res.statusCode, body }));
        });
        req.on('error', reject);
        if (data) req.write(data);
        req.end();
    });
}

async function findOwnerId() {
    try {
        const sessionData = JSON.parse(fs.readFileSync('/Users/silkroadcat/.openclaw/workspace/the-alpha-oracle/vault/limitless_session.json', 'utf8'));
        const cookie = sessionData.full_cookie || sessionData.cookie;
        
        const headers = {
            "Accept": "application/json",
            "Cookie": cookie,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
        };

        // Testing common session info endpoints
        const endpoints = ["/auth/session", "/users/me", "/profile"];
        
        for (const ep of endpoints) {
            console.log(`🔍 Checking ${ep} with cookie...`);
            const res = await httpsRequest(`${API_BASE_URL}${ep}`, 'GET', headers);
            console.log(`📡 Status: ${res.statusCode} | Body: ${res.body.substring(0, 200)}`);
            
            if (res.statusCode === 200) {
                const data = JSON.parse(res.body);
                console.log("💎 FOUND POTENTIAL ID:", data.user?.id || data.id || data.profile?.id);
            }
        }
    } catch (e) {
        console.error("❌ Error:", e.message);
    }
}

findOwnerId();

const fs = require('fs');
const https = require('https');

// Trying /v1/ prefix
const API_BASE_URL = "https://api.limitless.exchange/v1";

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

async function debugV1() {
    try {
        const wallets = JSON.parse(fs.readFileSync('/Users/silkroadcat/.openclaw/workspace/the-alpha-oracle/vault/limitless_wallets.json', 'utf8'));
        const apiKey = wallets[0].api_key;
        
        console.log(`🔍 Fetching ${API_BASE_URL}/users/me...`);
        const userRes = await httpsRequest(`${API_BASE_URL}/users/me`, 'GET', { "X-API-Key": apiKey });
        console.log("📡 Status:", userRes.statusCode);
        console.log("📦 Body:", userRes.body);
    } catch (e) {
        console.error("❌ Error:", e.message);
    }
}

debugV1();

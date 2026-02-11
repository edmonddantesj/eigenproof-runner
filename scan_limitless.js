const fs = require('fs');
const https = require('https');

const API_BASE_URL = "https://api.trylimitless.is";

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

async function scanEndpoints() {
    const wallets = JSON.parse(fs.readFileSync('/Users/silkroadcat/.openclaw/workspace/the-alpha-oracle/vault/limitless_wallets.json', 'utf8'));
    const apiKey = wallets[0].api_key;
    const targets = ["/users/me", "/me", "/profile", "/users/current", "/account"];
    
    for (const path of targets) {
        console.log(`🔍 Testing ${path}...`);
        const res = await httpsRequest(`${API_BASE_URL}${path}`, 'GET', { "X-API-Key": apiKey });
        console.log(`📡 ${path} -> Status: ${res.statusCode} | Body: ${res.body.substring(0, 100)}`);
    }
}

scanEndpoints();

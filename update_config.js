const fs = require('fs');
const path = require('path');
const configPath = path.join(process.env.HOME, '.openclaw/openclaw.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

// Inject Brave API Key
if (!config.skills) config.skills = {};
if (!config.skills.entries) config.skills.entries = {};

config.skills.entries.web_search = {
    apiKey: "BSAGrnt4cR_3kwp6VaMx9hY5rEEQPWj",
    provider: "brave"
};

// Also update 'brave' skill just in case
config.skills.entries.brave = {
    apiKey: "BSAGrnt4cR_3kwp6VaMx9hY5rEEQPWj"
};

fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
console.log("✅ Config updated successfully!");

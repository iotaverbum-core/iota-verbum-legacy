#!/usr/bin/env node
const fs = require("fs");
const path = require("path");

function fail(msg) {
  console.error(`[store-check] ${msg}`);
  process.exit(1);
}

function read(file) {
  return fs.readFileSync(file, "utf8");
}

function exists(file) {
  return fs.existsSync(file);
}

function assertContains(file, pattern, msg) {
  const data = read(file);
  if (!pattern.test(data)) fail(msg);
}

function collectFiles(dir, allowedExt = new Set([".ts", ".tsx", ".js", ".json", ".md"])) {
  const out = [];
  const stack = [dir];
  while (stack.length) {
    const cur = stack.pop();
    if (!cur) continue;
    for (const entry of fs.readdirSync(cur, { withFileTypes: true })) {
      const full = path.join(cur, entry.name);
      if (entry.isDirectory()) {
        if (entry.name === "node_modules" || entry.name === "ios" || entry.name === "android") {
          continue;
        }
        stack.push(full);
      } else if (allowedExt.has(path.extname(entry.name))) {
        out.push(full);
      }
    }
  }
  return out;
}

console.log("[store-check] checking privacy manifest file");
if (!exists("apps/mobile/ios/PrivacyInfo.xcprivacy")) {
  fail("PrivacyInfo.xcprivacy missing");
}

console.log("[store-check] checking consent modal");
assertContains(
  "apps/mobile/app/_layout.tsx",
  /AI Sharing Consent/,
  "First-run consent modal not found"
);

console.log("[store-check] checking policy and terms wiring");
const appConfig = read("apps/mobile/app.config.ts");
const apiMain = read("services/api/app/main.py");
const policyConfigured = /privacyPolicyUrl/.test(appConfig) || /\/v1\/privacy/.test(apiMain);
const termsConfigured = /termsUrl/.test(appConfig) || /\/v1\/terms/.test(apiMain);
if (!policyConfigured) fail("Neither privacy URL config nor /v1/privacy endpoint found");
if (!termsConfigured) fail("Neither terms URL config nor /v1/terms endpoint found");

console.log("[store-check] checking retention defaults");
assertContains(
  "services/api/app/settings.py",
  /data_retention_days: int = 0/,
  "DATA_RETENTION_DAYS default must be 0"
);
assertContains(
  "services/api/app/settings.py",
  /store_eden_text: bool = False/,
  "STORE_EDEN_TEXT default must be false"
);

console.log("[store-check] checking backend request logs avoid raw text");
const backendFiles = ["services/api/app/main.py", "services/api/app/llm/openai_client.py"];
for (const file of backendFiles) {
  const data = read(file);
  if (/logger\.(info|warning|error).*text/.test(data)) {
    fail(`Potential raw text logging found in ${file}`);
  }
}

console.log("[store-check] checking mobile code for key leakage and OpenAI references");
const mobileFiles = collectFiles("apps/mobile");
for (const file of mobileFiles) {
  const data = read(file);
  if (/OPENAI_API_KEY|IOTA_OPENAI_API_KEY/.test(data)) {
    fail(`OpenAI API key reference found in mobile file: ${file}`);
  }
  if (/sk-[A-Za-z0-9]{10,}/.test(data)) {
    fail(`Possible secret key pattern found in mobile file: ${file}`);
  }
  if (/api\.openai\.com|openai\.com\/v1/i.test(data)) {
    fail(`OpenAI endpoint reference found in mobile file: ${file}`);
  }
}

console.log("[store-check] all checks passed");

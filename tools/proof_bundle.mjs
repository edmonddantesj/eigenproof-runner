#!/usr/bin/env node
/**
 * Proof Bundle Generator (AOI)
 *
 * Creates a verifiable evidence bundle for a triage run:
 * - report.md (raw text)
 * - report.json (structured wrapper)
 * - sha256.txt (integrity hashes)
 *
 * Usage:
 *   node tools/proof_bundle.mjs --in /path/to/triage_report.md --out artifacts/elastic_demo
 *   # or from clipboard-like paste:
 *   node tools/proof_bundle.mjs --paste --out artifacts/elastic_demo
 */

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

function argMap(argv) {
  const m = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (!a.startsWith('--')) continue;
    const k = a.slice(2);
    const v = argv[i + 1];
    if (!v || v.startsWith('--')) { m[k] = true; continue; }
    m[k] = v;
    i++;
  }
  return m;
}

function nowStamp() {
  const d = new Date();
  const pad = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}${pad(d.getMonth()+1)}${pad(d.getDate())}_${pad(d.getHours())}${pad(d.getMinutes())}${pad(d.getSeconds())}`;
}

function sha256(buf) {
  return crypto.createHash('sha256').update(buf).digest('hex');
}

function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

async function readAllStdin() {
  return await new Promise((resolve, reject) => {
    let d = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', (c) => (d += c));
    process.stdin.on('end', () => resolve(d));
    process.stdin.on('error', reject);
  });
}

async function main() {
  const args = argMap(process.argv.slice(2));
  const outRoot = args.out ? String(args.out) : 'artifacts/elastic_demo';
  const inPath = args.in ? String(args.in) : null;
  const paste = Boolean(args.paste);

  if (!inPath && !paste) {
    throw new Error('Provide --in <file> OR --paste (reads stdin).');
  }

  let reportText = '';
  if (inPath) {
    reportText = fs.readFileSync(inPath, 'utf8');
  } else {
    // --paste: read stdin
    if (process.stdin.isTTY) {
      throw new Error('--paste requires piping text in. Example: pbpaste | node tools/proof_bundle.mjs --paste');
    }
    reportText = await readAllStdin();
  }

  const stamp = nowStamp();
  const bundleDir = path.join(outRoot, `proof_bundle_${stamp}`);
  ensureDir(bundleDir);

  const reportMdPath = path.join(bundleDir, 'report.md');
  const reportJsonPath = path.join(bundleDir, 'report.json');
  const shaPath = path.join(bundleDir, 'sha256.txt');

  fs.writeFileSync(reportMdPath, reportText);

  const reportJson = {
    schema_version: 'aoi_proof_bundle_v0_1',
    created_at: new Date().toISOString(),
    kind: 'elastic_proofops_triage',
    inputs: {
      source: inPath ? path.resolve(inPath) : 'stdin',
    },
    outputs: {
      report_md: 'report.md',
    },
  };
  fs.writeFileSync(reportJsonPath, JSON.stringify(reportJson, null, 2) + '\n');

  const mdHash = sha256(fs.readFileSync(reportMdPath));
  const jsonHash = sha256(fs.readFileSync(reportJsonPath));

  const shaText = [
    `${mdHash}  report.md`,
    `${jsonHash}  report.json`,
  ].join('\n') + '\n';
  fs.writeFileSync(shaPath, shaText);

  console.log(JSON.stringify({
    ok: true,
    bundleDir,
    files: {
      report_md: reportMdPath,
      report_json: reportJsonPath,
      sha256: shaPath,
    },
    sha256: {
      report_md: mdHash,
      report_json: jsonHash,
    }
  }, null, 2));
}

main().catch((e) => {
  console.error(String(e?.message ?? e));
  process.exit(1);
});

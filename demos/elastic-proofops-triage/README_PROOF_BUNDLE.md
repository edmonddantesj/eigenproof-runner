# Proof Bundle (Elastic demo)

## Create bundle from a saved report

```bash
cd /Users/silkroadcat/.openclaw/workspace
node demos/elastic-proofops-triage/tools/proof_bundle.mjs --in artifacts/elastic_demo/triage_report_001.md --out artifacts/elastic_demo
```

## Create bundle from clipboard (macOS)

```bash
pbpaste | node demos/elastic-proofops-triage/tools/proof_bundle.mjs --paste --out artifacts/elastic_demo
```

The command prints the output directory and sha256 hashes.
Use this as the final demo cut: "every run produces an artifact + integrity hash".

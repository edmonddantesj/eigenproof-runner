# Elastic Hackathon Demo — ProofOps Triage Agent

This folder contains a **self-contained demo** for the Elastic Agent Builder hackathon.

## What it demonstrates
1) Elasticsearch is used as a **knowledge core** (`knowledge` index)
2) An Agent Builder agent performs multi-step triage and outputs an **Evidence Pack**
3) A small script generates a **Proof Bundle** (artifact + sha256) from the triage output

## Proof Bundle script

From repo root:

```bash
node demos/elastic-proofops-triage/tools/proof_bundle.mjs --in artifacts/elastic_demo/triage_report_001.md --out artifacts/elastic_demo
```

Or from clipboard (macOS):

```bash
pbpaste | node demos/elastic-proofops-triage/tools/proof_bundle.mjs --paste --out artifacts/elastic_demo
```

Outputs a folder:
- report.md
- report.json
- sha256.txt

Use this as the final 10s cut in the demo video: “every run produces a verifiable artifact with integrity hash”.

# EigenProof Runner (Aoineco) — EigenCloud / EigenCompute Challenge

A minimal **proof-first container runner**.

Each run produces a verifiable bundle:
- `input.json`
- `output.json`
- `manifest.json` (sha256 for files + runtime metadata)
- `sha256sum.txt`

## Quickstart (local Docker)

```bash
cd eigencloud_eigenproof_runner

# build
docker build -t eigenproof-runner:local .

# run (writes proof bundle to ./out)
mkdir -p out

docker run --rm \
  -v "$PWD/out:/out" \
  eigenproof-runner:local \
  --input /app/sample_input.json \
  --outdir /out

# inspect
ls -la out
cat out/manifest.json
cat out/sha256sum.txt
```

## Notes
- Deterministic output for demo.
- No tokenized agents.
- No external calls.

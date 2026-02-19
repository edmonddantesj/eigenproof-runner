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


## Verify the bundle

After a run, verify integrity with:

```bash
cd out
sha256sum -c sha256sum.txt
```

Expected: `OK` for each file listed.

## Manifest extras

- `runtime.git_commit` (baked into the container via build arg, for reproducibility)
- optional `docker_image_digest` (if the platform injects `EIGEN_IMAGE_DIGEST` or `DOCKER_IMAGE_DIGEST`)

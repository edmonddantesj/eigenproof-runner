# EigenProof Runner (Aoineco) — EigenCloud / EigenCompute Challenge

## Submission pitch (TL;DR)
`Reproducible` · `Auditable` · `Policy-bound`

This project is a proof-first EigenCompute runner that emits reproducible, verifiable execution artifacts (`manifest.json` + `sha256sum.txt`) from every run.
It is safe, inspectable, and judge-friendly: fixed policy/version context, commit-aware provenance, and a deterministic replay mode for auditability.

A minimal **proof-first container runner**.

Each run produces a verifiable bundle:
- `input.json`
- `output.json`
- `identity.json` (what code ran; public-safe)
- `policy.json` (upgrade/execution policy hints)
- `manifest.json` (sha256 for files + runtime metadata)
- `sha256sum.txt`

## Why Eigen?
This runner is designed for off-chain execution environments such as **EigenCompute**, where reproducibility, commit pinning, and verifiable artifacts are first-class requirements. It aims to reduce ambiguity between execution, policy constraints, and audit artifacts.

## Architecture (text flow)

`Input JSON` → `runner.py` → `output.json` + `identity.json` + `policy.json` → `manifest.json` → `sha256sum.txt`

## Quickstart (local Docker)

```bash
cd eigenproof-runner

# recommended: use local helper (build args + env are injected automatically)
./run_local.sh
```

Quick fallback (manual Docker):

```bash
docker build --build-arg "GIT_COMMIT=$(git rev-parse HEAD)" -t eigenproof-runner:local .
mkdir -p out

docker run --rm \
  -v "$PWD/out:/out" \
  -v "$PWD/policy.json:/app/policy.json:ro" \
  -e GIT_COMMIT=$(git rev-parse HEAD) \
  -e DOCKER_IMAGE_DIGEST=${DOCKER_IMAGE_DIGEST:-} \
  -e EIGEN_IMAGE_DIGEST=${EIGEN_IMAGE_DIGEST:-} \
  eigenproof-runner:local \
  --input /app/sample_input.json \
  --outdir /out \
```

Check outputs:

```bash
ls -la out
cat out/manifest.json
cat out/sha256sum.txt
```

## Verify the bundle

After a run, verify integrity with:

```bash
cd out
sha256sum -c sha256sum.txt
```

Expected: `OK` for each file listed.

## Notes
- We guarantee **deterministic core result hashing** for a fixed input and policy,
  while capturing environment provenance and commit metadata.
  Timestamps and `run_id` are not fixed by default (they vary per run); use `--deterministic` for fixed replay values.
- No tokenized agents.
- No external calls.

## B-model (policy-proof hardening)

- `policy.json` is embedded in the proof bundle as `policy.json`.
- `manifest.runtime.policy_sha256` stores policy hash.
- `manifest.files` lists policy file hash.
- `manifest` includes `self_sha256` and `manifest.json` own hash in file list.
- `identity.json` captures project identity + executable fingerprint.
- `run_local.sh` is included as recommended entrypoint for reproducible local runs.

## Fast submission checks (for judges/review)
- [ ] `cd eigenproof-runner` path in README matches repo root.
- [ ] `manifest.json` includes `run_id`, `created_at`, `runtime.git_commit`.
- [ ] `manifest.bundle.files` lists hashes for:
  - `input.json`
  - `output.json`
  - `identity.json`
  - `policy.json`
  - `manifest.json`
- [ ] `sha256sum.txt` contains `manifest.json` hash line.
- [ ] `manifest.self_sha256` exists.
- [ ] Default run: `python3 runner.py --input sample_input.json --outdir out` runs and captures output metadata.
- [ ] Deterministic mode: `python3 runner.py --input sample_input.json --outdir out --deterministic` replays consistent result-hash + fixed metadata fields.

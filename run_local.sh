#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

docker build -t eigenproof-runner:local .
mkdir -p out

docker run --rm -v "$PWD/out:/out" eigenproof-runner:local --input /app/sample_input.json --outdir /out

echo "--- out/"
ls -la out
echo "--- manifest.json"
cat out/manifest.json

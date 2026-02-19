#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

GIT_COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo unknown)

docker build --build-arg GIT_COMMIT="$GIT_COMMIT" -t eigenproof-runner:local .
mkdir -p out

docker run --rm -v "$PWD/out:/out" eigenproof-runner:local --input /app/sample_input.json --outdir /out

echo "--- out/"
ls -la out
echo "--- manifest.json"
cat out/manifest.json

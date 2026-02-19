#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

IMAGE=eigenproof-runner:local
OUTDIR="$PWD/out"

run_python_local(){
  echo "[fallback] Docker unavailable. Running local python proof generation..."
  mkdir -p "$OUTDIR"
  python3 runner.py --input "$PWD/sample_input.json" --outdir "$OUTDIR" --policy "$PWD/policy.json"
  echo "[local] out/"
  ls -la "$OUTDIR"
  echo "[local] manifest.json"
  cat "$OUTDIR/manifest.json"
  echo "[local] sha256"
  if command -v sha256sum >/dev/null 2>&1; then
    (cd "$OUTDIR" && sha256sum -c sha256sum.txt)
  else
    (cd "$OUTDIR" && shasum -a 256 -c sha256sum.txt)
  fi
}

if ! command -v docker >/dev/null 2>&1; then
  echo "docker not found"
  run_python_local
  exit 0
fi

echo "Building image (cache preferred)"
COMMIT="$(git rev-parse HEAD 2>/dev/null || true)"
if docker build -t "$IMAGE" --build-arg "GIT_COMMIT=$COMMIT" . >/tmp/eigenproof_build.log 2>&1; then
  echo "Build done"
else
  echo "Docker build failed (likely daemon/network/auth issue). See /tmp/eigenproof_build.log"
  cat /tmp/eigenproof_build.log
  run_python_local
  exit 0
fi

mkdir -p "$OUTDIR"

docker run --rm \
  -v "$OUTDIR:/out" \
  -v "$PWD/policy.json:/app/policy.json:ro" \
  "$IMAGE" --input /app/sample_input.json --outdir /out --policy /app/policy.json

echo "--- out/"
ls -la "$OUTDIR"

echo "--- manifest.json"
cat "$OUTDIR/manifest.json"
echo "--- sha256sum.txt"
cat "$OUTDIR/sha256sum.txt"

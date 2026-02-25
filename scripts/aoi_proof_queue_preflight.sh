#!/usr/bin/env bash
set -euo pipefail

# AOI Proof Queue preflight v0.1
# Usage:
#   scripts/aoi_proof_queue_preflight.sh /path/to/queue.jsonl

JSONL=${1:-}
if [[ -z "$JSONL" ]]; then
  echo "ERR: missing jsonl path" >&2
  exit 2
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCHEMA="$ROOT/context/aoi_core_radar/patterns/AOI_PROOF_QUEUE_SCHEMA_V0_1.json"

python3 "$ROOT/scripts/aoi_proof_queue_validate.py" --schema "$SCHEMA" --jsonl "$JSONL"

#!/usr/bin/env bash
set -euo pipefail

# AOI Council Governance Gate Health — Heartbeat Smoke
# Purpose: quick fail-closed validation that the council runner can execute.
# Notes:
# - Uses an isolated cost governor state file to avoid cross-run contamination.
# - Outputs to /tmp for easy inspection.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

TS="$(date '+%Y%m%d_%H%M%S')"
OUT_DIR="/tmp/aoi-council-hb-${TS}"
STATE_PATH="/tmp/aoi_cost_governor_state_hb_${TS}.json"

mkdir -p "$OUT_DIR"

python3 repos/aoi-ssot/scripts/aoi_council_run.py \
  --mode decision \
  --topic "HB Smoke: governance gate health" \
  --context "Heartbeat smoke test. Expect deterministic completion. No external publishing." \
  --out-dir "$OUT_DIR" \
  --estimated-cost-usd 0 \
  --cost-governor-state "$STATE_PATH" \
  --actor-id "heartbeat" \
  --target "heartbeat" \
  --method "cli" \
  --action "smoke" \
  --value-usd 0 \
  --amount 0

# Optional AOI Core preflight hooks (static checks)
# Set AOI_PREFLIGHT_TARGET to a repo/path to scan (default: skip).
if [[ -n "${AOI_PREFLIGHT_TARGET:-}" ]]; then
  echo "Running AOI Core preflight on: ${AOI_PREFLIGHT_TARGET}"
  "$ROOT/scripts/aoi_core_preflight.sh" "$AOI_PREFLIGHT_TARGET" || {
    echo "FAIL: AOI Core preflight failed" >&2
    exit 1
  }
fi

echo "OK: AOI Council smoke completed. out_dir=$OUT_DIR state=$STATE_PATH"

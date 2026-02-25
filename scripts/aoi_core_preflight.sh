#!/usr/bin/env bash
set -euo pipefail

# AOI Core preflight v0.1 (x402 + attribution)
# Usage:
#   scripts/aoi_core_preflight.sh <path>

TARGET=${1:-}
if [[ -z "$TARGET" ]]; then
  echo "ERR: missing target path" >&2
  exit 2
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

"$ROOT/scripts/aoi_x402_preflight.sh" "$TARGET"
"$ROOT/scripts/aoi_attribution_preflight.sh" "$TARGET"

echo "PASS"

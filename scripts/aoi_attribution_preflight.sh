#!/usr/bin/env bash
set -euo pipefail

# AOI onchain attribution (builder code / dataSuffix) preflight v0.1
# Usage:
#   scripts/aoi_attribution_preflight.sh <path>

TARGET=${1:-}
if [[ -z "$TARGET" ]]; then
  echo "ERR: missing target path" >&2
  exit 2
fi
if [[ ! -e "$TARGET" ]]; then
  echo "ERR: target not found: $TARGET" >&2
  exit 2
fi

command -v rg >/dev/null 2>&1 || { echo "ERR: ripgrep (rg) not found" >&2; exit 2; }

PASS=true
fail(){ PASS=false; echo "FAIL: $*"; }
warn(){ echo "WARN: $*"; }
info(){ echo "INFO: $*"; }

info "== attribution preflight =="
info "Target: $TARGET"

# Detect likely attribution usage
if ! rg -n "erc8021|Attribution\.toDataSuffix|dataSuffix" "$TARGET" >/dev/null 2>&1; then
  info "No ERC-8021/builder-code attribution markers detected (skipping)."
  echo "PASS"
  exit 0
fi

info "Attribution markers detected. Running checks..."

# Red flag: passing dataSuffix into createWalletClient (AURA pitfall)
if rg -n "createWalletClient\([\s\S]{0,400}dataSuffix" "$TARGET" >/dev/null 2>&1; then
  warn "Found dataSuffix passed into createWalletClient. Some clients may ignore it; prefer per-write attachment."
  rg -n "createWalletClient\([\s\S]{0,400}dataSuffix" "$TARGET" || true
fi

# Positive signal: dataSuffix passed into writeContract/sendTransaction
if ! rg -n "writeContract\([\s\S]{0,400}dataSuffix|sendTransaction\([\s\S]{0,400}dataSuffix" "$TARGET" >/dev/null 2>&1; then
  fail "No per-transaction dataSuffix attachment found. Add dataSuffix to each writeContract/sendTransaction call."
fi

if [[ "$PASS" == true ]]; then
  echo "PASS"
  exit 0
else
  echo "FAIL"
  exit 1
fi

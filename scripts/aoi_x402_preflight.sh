#!/usr/bin/env bash
set -euo pipefail

# AOI x402 preflight v0.1
# Heuristic static checks (public-safe). No secrets.
# Usage:
#   scripts/aoi_x402_preflight.sh <path>

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

info "== x402 preflight =="
info "Target: $TARGET"

# Detect x402 usage
if ! rg -n "@x402/|withX402|Payment Required|\b402\b" "$TARGET" >/dev/null 2>&1; then
  info "No x402 usage detected (skipping)."
  echo "PASS"
  exit 0
fi

info "x402 usage detected. Running checks..."

# 1) Edge runtime red flags
if rg -n "runtime\s*:\s*['\"]edge['\"]|export\s+const\s+runtime\s*=\s*['\"]edge['\"]|Edge Runtime" "$TARGET" >/dev/null 2>&1; then
  warn "Edge runtime markers found. x402 EVM verification may require Node crypto APIs."
  rg -n "runtime\s*:\s*['\"]edge['\"]|export\s+const\s+runtime\s*=\s*['\"]edge['\"]|Edge Runtime" "$TARGET" || true
fi

# 2) Middleware usage (often fragile)
if rg -n "middleware\.ts|@x402/next" "$TARGET" >/dev/null 2>&1; then
  warn "x402 middleware detected. Prefer route-handler gate when middleware is fragile."
  rg -n "middleware\.ts|@x402/next" "$TARGET" || true
fi

# 3) Self-payment hazard: ensure payer!=payee (heuristic)
if rg -n "payer\s*==\s*payee|payee\s*==\s*payer|self-?payment" "$TARGET" >/dev/null 2>&1; then
  warn "Self-payment check found; ensure enforced in all payment verification paths."
fi

# 4) Receipt bundle discipline: look for request_id / idempotency
if ! rg -n "request_id|idempotenc|receipt" "$TARGET" >/dev/null 2>&1; then
  fail "No obvious request_id/idempotency/receipt fields found near x402 code. Add receipt bundle + idempotency."
fi

if [[ "$PASS" == true ]]; then
  echo "PASS"
  exit 0
else
  echo "FAIL"
  exit 1
fi

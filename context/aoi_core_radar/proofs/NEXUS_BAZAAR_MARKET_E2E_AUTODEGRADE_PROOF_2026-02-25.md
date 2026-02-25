# NEXUS Bazaar Market — E2E Auto-Degrade Proof (2026-02-25)

This proof note captures evidence that the Phase 1.5 circuit breaker auto-degrade logic works end-to-end using a mock vendor failure loop.

## Repo
- Private: https://github.com/edmonddantesj/nexus-bazaar-market

## Procedure
1) Start API server:
   - `cd repos/nexus-bazaar-market/apps/api && npm install && npm run dev`
2) Run demo script:
   - `cd ../.. && ./scripts/worker/e2e_autodegrade_demo.sh`

## Expected behavior
- Reset breaker to `OK`
- Trigger 5 failures (min_requests=5, error_rate_degrade=0.5)
- Breaker flips to `DEGRADED` with cooldown set
- Worker consumer skips processing while degraded

## Observed output (abridged)
- Breaker reset: `OK`
- 5 failures triggered
- Breaker status returned:
  - `state: DEGRADED`
  - `window.error_count: 5`
  - `window.total_count: 5`
  - `cooldown_until: 2026-02-25T06:51:28.354Z`
- Worker output:
  - `{ skipped: true, reason: "circuit_breaker_degraded" }`

## Local evidence
- `var/proof_queue/state.json` contained `state: DEGRADED` and matching `cooldown_until`.

## Conclusion
Auto-degrade works and is observable. Next step is wiring real vendor call failures to `recordResult(false)`.

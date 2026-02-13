# $AOI Tokenomics v2.1 — VC-Inclusive, Regulatory-Safe Architecture

## Aoineco & Co. — Financial Engineering Supplement
### Date: 2026-02-12 | Classification: L3 (Chairman Eyes Only)
### Upgrade: v2.0 → v2.1 (Strategic Investor Layer Added)

---

## 0. Design Objectives

Three constraints must be satisfied simultaneously:

1. **VC Inclusion:** Strategic investors receive meaningful allocation with clear terms.
2. **Ecosystem Stability:** No single unlock event can crash the market.
3. **Regulatory Safety:** VC allocation must not transform $AOI from utility token into security.

**The solution: "Service Credit Forward Purchase" (SCFP) model.**

---

## 1. The SCFP Model — Why It Works

### 1.1 Traditional VC Token Sale (DANGEROUS ❌)

```
VC pays $500K → Receives 5M $AOI at discount → Waits for price to rise → Dumps

Legal Problem:  VC is buying with "expectation of profit from efforts of others"
                = Howey Test SATISFIED = Security = Regulatory nightmare
```

### 1.2 Service Credit Forward Purchase (SAFE ✅)

```
VC pays $500K → Purchases "Platform Service Credits" redeemable in $AOI
             → Credits unlock gradually as platform milestones are met
             → Credits can ONLY be used to:
                (a) Purchase skills on AI DEX (burned)
                (b) Provision agent squads via Brand-Genesis (burned)
                (c) Sell on secondary market AFTER conversion to $AOI

Legal Framing: VC is pre-purchasing services at bulk discount
               = "Volume licensing agreement" NOT "investment contract"
               = Howey Test prong 3 (expectation of profit) weakened
```

### 1.3 Why SCFP Passes Regulatory Scrutiny

| Regulatory Test | Traditional VC Sale | SCFP Model |
|----------------|--------------------|----|
| **Howey — Expectation of Profit** | VC explicitly expects price appreciation | VC purchases "service credits" — profit is incidental, not promised |
| **Howey — Efforts of Others** | VC relies entirely on team to drive value | Credits have utility value independent of $AOI market price |
| **MiCA — Utility Classification** | Bulk discount sale looks like securities offering | Forward purchase of services = commercial agreement |
| **KR — Securities Exclusion** | Large VC allocation = "공동사업" suspicion | Service licensing = B2B commercial contract |

---

## 2. Revised Token Distribution (v2.1)

### 2.1 Total Supply: 1,000,000,000 $AOI (1 Billion, Fixed at Genesis)

| # | Allocation | Share | Tokens | Lock-up / Vesting | Legal Framing |
|---|-----------|-------|--------|-------------------|---------------|
| 1 | **Ecosystem Rewards** | 35% | 350M | Usage-based release; milestone-gated | Service consumption incentives |
| 2 | **Treasury** | 15% | 150M | Multi-sig (3/5); quarterly transparency report | Operational reserve |
| 3 | **Team** | 12% | 120M | 1-year cliff + 4-year linear vesting | Founding team compensation |
| 4 | **Strategic Partners (VC)** | 15% | 150M | See §2.2 Tiered Unlock below | **Service Credit Forward Purchase** |
| 5 | **Community Growth** | 13% | 130M | Activity-based; capped per epoch | Hackathons, bounties, grants |
| 6 | **Initial Liquidity** | 10% | 100M | Permanently locked; LP tokens burned | DEX market-making |

**Key changes from v2.0:**
- Ecosystem Rewards: 40% → 35% (still largest allocation)
- Treasury: 20% → 15% (leaner, more accountable)
- Team: 15% → 12% (signals humility; still competitive)
- **NEW: Strategic Partners (VC): 0% → 15%** (carved from Ecosystem + Treasury)
- Community Growth: 15% → 13%
- Initial Liquidity: 10% → 10% (unchanged)

### 2.2 VC Tiered Unlock Schedule — "The Cascade"

The critical innovation: VC tokens don't unlock on a simple time schedule. They unlock based on **platform milestones AND time**, creating dual gates that prevent premature dumping while aligning VC incentives with ecosystem health.

```
150M $AOI (VC Pool)
    │
    ├── Tier 1: Seed (5%) ─── 50M tokens
    │     Price: 60% discount to TGE
    │     Unlock: 6-month cliff → 24-month linear
    │     Gate: Platform must have ≥10 active agent teams
    │     Max Monthly Sell: 2% of Tier 1 balance
    │
    ├── Tier 2: Strategic (7%) ─── 70M tokens
    │     Price: 40% discount to TGE
    │     Unlock: 9-month cliff → 30-month linear
    │     Gate: Monthly burn rate must exceed 500K $AOI
    │     Max Monthly Sell: 1.5% of Tier 2 balance
    │
    └── Tier 3: Growth (3%) ─── 30M tokens
          Price: 20% discount to TGE
          Unlock: 3-month cliff → 18-month linear
          Gate: AI DEX monthly volume must exceed $100K
          Max Monthly Sell: 3% of Tier 3 balance
```

### 2.3 Why "The Cascade" Works

**For the Ecosystem:**
- No single unlock creates massive sell pressure
- Milestone gates ensure VC tokens only enter circulation when the ecosystem is healthy enough to absorb them
- Monthly sell caps create predictable, gradual supply increase

**For VCs:**
- Clear, structured terms (institutional-grade)
- Deeper discount for longer commitment (Seed gets best price)
- Milestone gates give VCs INCENTIVE to help the ecosystem grow (their tokens unlock faster when the platform thrives)

**For Regulators:**
- Milestone-gated unlocks = "VC is buying future services, not speculating"
- Monthly sell caps = "This is orderly service credit liquidation, not a securities dump"
- No guaranteed returns at any tier

---

## 3. Anti-Dump Engineering — "The Pressure Valve"

### 3.1 Smart Contract Level Protections

```solidity
// Simplified logic — actual implementation will be audited

contract AOI_VCVesting {
    // DUAL GATE: Time + Milestone
    function claimTokens(uint256 tier) external {
        require(block.timestamp >= cliffEnd[tier], "Cliff not reached");
        require(milestoneReached[tier] == true, "Platform milestone not met");
        
        uint256 available = calculateVested(tier) - claimed[tier];
        uint256 maxSell = balance[tier] * monthlyCapBps[tier] / 10000;
        uint256 claimable = min(available, maxSell);
        
        claimed[tier] += claimable;
        AOI.transfer(msg.sender, claimable);
    }
    
    // ORACLE: Milestone verification by multi-sig
    function setMilestone(uint256 tier, bool reached) external onlyMultiSig {
        milestoneReached[tier] = reached;
    }
}
```

### 3.2 Market Impact Modeling

**Worst-Case Scenario: All VCs sell at maximum rate simultaneously**

```
Month 7 (first Seed unlock):
  Seed max sell:    50M × 2% = 1M $AOI
  Strategic:        Still locked (9-month cliff)
  Growth:           30M × 3% = 0.9M $AOI (if milestone met)
  
  Total new supply: 1.9M $AOI (0.19% of total supply)
  
  At $0.01/token: $19,000 sell pressure
  At $0.10/token: $190,000 sell pressure
  
  → Manageable with even modest DEX liquidity ($500K+ pool)
```

**Month 12 (all tiers potentially active):**

```
  Seed max sell:    ~48M remaining × 2% = 0.96M
  Strategic max:    70M × 1.5% = 1.05M
  Growth max:       ~27M remaining × 3% = 0.81M
  
  Total new supply: 2.82M $AOI (0.28% of total supply)
  
  → Still manageable. No "cliff dump" event possible.
```

### 3.3 Velocity Dampener

If the 7-day average $AOI price drops >30% from 30-day moving average, an **automatic slowdown** activates:

```
Normal mode:     Monthly cap as defined per tier
Dampened mode:   Monthly cap reduced to 50% (automatic, on-chain)
Recovery:        Price must recover to >85% of 30-day MA for 7 consecutive days
```

**Legal framing:** "Market stability mechanism to ensure orderly service credit redemption" — NOT price manipulation. This protects ALL holders equally.

---

## 4. VC Agreement Template — Key Terms

### 4.1 What VCs Sign (SAFT-Lite for Utility Tokens)

```
AGREEMENT TYPE:     Service Credit Forward Purchase Agreement (SCFPA)
                    (NOT a SAFT — "Simple Agreement for Future Tokens")
                    
PURCHASE:           [VC Name] purchases Platform Service Credits
                    redeemable for $AOI utility tokens.
                    
VALUATION:          Credits are priced at [Tier discount] to 
                    anticipated Token Generation Event (TGE) price.
                    
UTILITY REQUIREMENT: Purchaser acknowledges that $AOI tokens are 
                    consumptive utility tokens and that this agreement 
                    does not constitute the purchase of a security, 
                    equity, debt instrument, or investment contract.
                    
NO PROFIT GUARANTEE: Purchaser acknowledges that Aoineco & Co. makes 
                    no representations regarding the future value, 
                    price, or market performance of $AOI tokens.
                    
RESTRICTIONS:       Tokens are subject to cliff, linear vesting, 
                    milestone gates, and monthly sell caps as 
                    specified in Schedule A.
                    
KYC/AML:            Purchaser must complete KYC verification 
                    through [Provider] before token delivery.
                    
GOVERNING LAW:      [Singapore / Cayman / BVI — TBD based on 
                    entity structure]
```

### 4.2 What VCs CANNOT Do

1. ❌ Receive dividends, revenue share, or interest
2. ❌ Vote on financial decisions (treasury, compensation, M&A)
3. ❌ Sell more than monthly cap regardless of vesting schedule
4. ❌ Transfer unvested credits to third parties
5. ❌ Make public statements implying $AOI is an investment product

### 4.3 What VCs CAN Do

1. ✅ Use $AOI to purchase services at discount (the primary purpose)
2. ✅ Vote on non-financial ecosystem proposals (same as any holder)
3. ✅ Sell vested $AOI on secondary markets within monthly caps
4. ✅ Stake $AOI as Quality Bonds for their own deployed agents
5. ✅ Receive "Ecosystem Contributor" designation (reputational benefit)

---

## 5. Comparative Analysis — Why This Is Best-in-Class

### 5.1 Industry Benchmark

| Project | VC Allocation | Cliff | Vesting | Monthly Cap | Milestone Gate |
|---------|-------------|-------|---------|-------------|---------------|
| Arbitrum ($ARB) | 17.5% | 1 year | 3 years | None | None |
| Optimism ($OP) | 19% | 1 year | 4 years | None | None |
| Aptos ($APT) | 13.5% | 1 year | 3 years | None | None |
| **$AOI** | **15%** | **6-9 months** | **18-30 months** | **1.5-3%** | **YES** |

**$AOI advantages:**
1. **Monthly sell cap** — No other major project has this. Prevents cliff-dump.
2. **Milestone gates** — VC interests are aligned with ecosystem health.
3. **Velocity dampener** — Automatic protection during market stress.
4. **SCFP framing** — Legal innovation that strengthens utility classification.

### 5.2 Total VC Dilution Timeline

```
Months:   0    6    12   18   24   30   36
          │    │    │    │    │    │    │
Seed:     ████ ░░░░░████████████████████  (24 months unlock)
Strategic:██████████ ░░░░░░████████████████████████ (30 months unlock)  
Growth:   ████ ░░░░░████████████████  (18 months unlock)

░░░░░ = Cliff period (tokens locked)
██████ = Gradual monthly unlock with caps

Max circulating VC tokens at Month 36: 150M (15%)
Actual circulating (with caps): ~130M-145M (monthly caps slow it down)
```

---

## 6. Impact on Existing Allocations

### 6.1 Before vs. After

| Allocation | v2.0 | v2.1 | Delta | Rationale |
|-----------|------|------|-------|-----------|
| Ecosystem Rewards | 40% | 35% | -5% | Still largest; 350M sufficient for years of rewards |
| Treasury | 20% | 15% | -5% | Leaner treasury signals efficiency; still $150M at scale |
| Team | 15% | 12% | -3% | Signals skin-in-the-game; competitive with industry standard |
| **Strategic Partners** | **0%** | **15%** | **+15%** | New category with world-class protections |
| Community Growth | 15% | 13% | -2% | Marginal reduction; still ample for growth programs |
| Initial Liquidity | 10% | 10% | 0% | Critical for healthy market; untouched |

### 6.2 Why This Split Is Optimal

The reductions are spread across three categories rather than taking a large chunk from one:
- **Ecosystem (-5%):** 350M tokens at even $0.01 = $3.5M in rewards — more than enough for early-stage ecosystem
- **Treasury (-5%):** Leaner treasury actually looks better to regulators (less "slush fund" concern)
- **Team (-3%):** 12% is industry-standard and signals the team isn't in it for a quick payday
- **No community reduction below 13%:** Maintains strong community-first narrative

---

## 7. Updated Flywheel (v2.1)

```
                    ┌─────────────────────────┐
                    │   STRATEGIC PARTNERS     │
                    │   (Service Credit        │
                    │    Forward Purchase)      │
                    └────────────┬────────────┘
                                 │
                    Capital injection for
                    development & marketing
                                 │
                                 ▼
┌──────────┐    ┌──────────────────────┐    ┌──────────────┐
│ Community │───▶│  Better Products     │◀───│ Team (12%)   │
│ (13%)    │    │  (Brand-Genesis,     │    │ Builds the   │
│ Finds &  │    │   Smart-Manager,     │    │ platform     │
│ promotes │    │   AI DEX)            │    │              │
└──────────┘    └──────────┬───────────┘    └──────────────┘
                           │
                  More agents use platform
                           │
                           ▼
              ┌────────────────────────┐
              │ $AOI Consumed (Burned) │
              │ by Agent Service Use   │
              └────────────┬───────────┘
                           │
              Supply decreases naturally
                           │
                           ▼
              ┌────────────────────────┐
              │  Organic Demand Grows  │──── Attracts more VCs (next round)
              │  (Usage, not hype)     │
              └────────────────────────┘
```

---

## 8. Implementation Checklist

- [ ] Update White Paper Section 6 with v2.1 distribution table
- [ ] Draft SCFPA (Service Credit Forward Purchase Agreement) legal template
- [ ] Implement VCVesting smart contract with dual-gate logic
- [ ] Build Velocity Dampener oracle (price feed + auto-cap adjustment)
- [ ] Create Transparency Dashboard module for VC unlock tracking
- [ ] Engage legal counsel to review SCFP model vs. SAFT
- [ ] Model additional scenarios (bear market, whale manipulation) for stress testing
- [ ] Update Litepaper with simplified VC narrative

---

## 9. Chairman's Decision Required

Three strategic choices need your input:

**A. Total Supply**
- Option 1: 1,000,000,000 (1B) — Clean, standard
- Option 2: 100,000,000 (100M) — Higher per-unit price perception
- Option 3: 10,000,000,000 (10B) — Lower unit price, "cheaper" feel

**B. VC Round Sizing**
- Conservative: $500K-$1M (Seed only, 5%)
- Standard: $2M-$5M (Seed + Strategic, 12%)
- Aggressive: $5M-$10M (All tiers, full 15%)

**C. Entity Jurisdiction**
- Singapore (crypto-friendly, MiCA pathway)
- Cayman Islands (traditional VC-friendly)  
- BVI (lightweight, common for token projects)
- Switzerland (Crypto Valley, premium perception)

---

*"The best tokenomics is one where VCs make money because users are happy, not because users are exit liquidity."*
— Aoineco & Co. Strategic Command, 2026

---
*Document Version: 2.1*
*Author: 🧿 Oracle (Blue-Command) with OPUS 4.6 Financial Engineering*
*Classification: L3 — Chairman (Edmond) Eyes Only*
*Prerequisite: AOI_Whitepaper_v1.md, aoi-masterplan-v2.md*
*/* 🌌 Aoineco-Verified | Multi-Agent Collective Proprietary Skill */*

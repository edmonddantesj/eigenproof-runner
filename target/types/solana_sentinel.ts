/**
 * Program IDL in camelCase format in order to be used in JS/TS.
 *
 * Note that this is only a type helper and is not the actual IDL. The original
 * IDL can be found at `target/idl/solana_sentinel.json`.
 */
export type SolanaSentinel = {
  "address": "9FouWHemn9iueyHYq4qpeNj9aHMyTKfEPt8ZpJaHcZ95",
  "metadata": {
    "name": "solanaSentinel",
    "version": "0.1.0",
    "spec": "0.1.0",
    "description": "Fee-Sharing Vault — Solana Sentinel"
  },
  "docs": [
    "════════════════════════════════════════════════════════════════",
    "Solana Sentinel v2 — Risk-Adjusted Fee-Sharing Vault",
    "════════════════════════════════════════════════════════════════",
    "",
    "Architecture Overview:",
    "",
    "1. SHARE VALUATION MODEL (Net Asset Value per Share)",
    "NAV/share = vault_balance / total_shares",
    "On deposit:  shares_minted = deposit_amount / (NAV/share)",
    "On withdraw: sol_returned  = shares_burned  * (NAV/share)",
    "Profits flow in → NAV/share rises → all holders benefit.",
    "",
    "2. RISK-ADJUSTED YIELD DISTRIBUTION (Performance-Weighted)",
    "Each agent that generates profits is scored by a rolling",
    "Sharpe-like ratio computed on-chain:",
    "",
    "score_i = mean_return_i / volatility_i  (if volatility > 0)",
    "",
    "Where:",
    "mean_return_i   = cumulative_pnl_i / trade_count_i",
    "volatility_i    = sqrt(E[R²] - E[R]²)  ≈ approximated via",
    "sum_sq_returns / n - (sum_returns / n)²",
    "",
    "Since on-chain sqrt is expensive, we use the SQUARED score",
    "for ranking (monotonic transformation preserves ordering):",
    "",
    "w_i = score_i² / Σ(score_j²)",
    "reward_i = w_i * total_profit_to_distribute",
    "",
    "This means agents with high mean return AND low variance",
    "capture more of the fee pool — a Sharpe-rational allocation.",
    "",
    "3. GUARDIAN POLICY ENGINE",
    "On-chain enforcement of:",
    "a) Daily withdrawal cap per user (resets every 86400 seconds)",
    "b) Cooldown period between withdrawals (configurable seconds)",
    "c) Whitelisted destination addresses (optional, up to 4)",
    "",
    "4. AGENT PERFORMANCE SCORING",
    "Each registered agent has an on-chain AgentProfile PDA:",
    "- trade_count, winning_trades (win rate = winning / total)",
    "- cumulative_pnl (signed, stored as i64)",
    "- sum_returns, sum_sq_returns (for variance calculation)",
    "- last_report_ts",
    "Oracle reports results; authority registers/deregisters agents.",
    "",
    "════════════════════════════════════════════════════════════════"
  ],
  "instructions": [
    {
      "name": "advanceEpoch",
      "docs": [
        "Authority advances the vault epoch. Resets epoch_profit counter.",
        "Useful for periodic reporting and agent performance snapshots."
      ],
      "discriminator": [
        93,
        138,
        234,
        218,
        241,
        230,
        132,
        38
      ],
      "accounts": [
        {
          "name": "vault",
          "writable": true,
          "pda": {
            "seeds": [
              {
                "kind": "const",
                "value": [
                  118,
                  97,
                  117,
                  108,
                  116
                ]
              },
              {
                "kind": "account",
                "path": "vault.authority",
                "account": "vault"
              }
            ]
          }
        },
        {
          "name": "authority",
          "signer": true,
          "relations": [
            "vault"
          ]
        }
      ],
      "args": []
    },
    {
      "name": "claimAgentReward",
      "docs": [
        "Agent claims their accumulated performance rewards from the vault.",
        "Resets total_rewards_earned to 0 after claim."
      ],
      "discriminator": [
        217,
        229,
        96,
        92,
        63,
        19,
        79,
        85
      ],
      "accounts": [
        {
          "name": "vault",
          "pda": {
            "seeds": [
              {
                "kind": "const",
                "value": [
                  118,
                  97,
                  117,
                  108,
                  116
                ]
              },
              {
                "kind": "account",
                "path": "vault.authority",
                "account": "vault"
              }
            ]
          }
        },
        {
          "name": "vaultSol",
          "writable": true,
          "pda": {
            "seeds": [
              {
                "kind": "const",
                "value": [
                  118,
                  97,
                  117,
                  108,
                  116,
                  95,
                  115,
                  111,
                  108
                ]
              },
              {
                "kind": "account",
                "path": "vault"
              }
            ]
          }
        },
        {
          "name": "agentProfile",
          "writable": true
        },
        {
          "name": "agent",
          "writable": true,
          "signer": true
        },
        {
          "name": "systemProgram",
          "address": "11111111111111111111111111111111"
        }
      ],
      "args": []
    },
    {
      "name": "deactivateAgent",
      "docs": [
        "Authority deactivates an agent. Does not delete the PDA (preserves history)."
      ],
      "discriminator": [
        205,
        171,
        239,
        225,
        82,
        126,
        96,
        166
      ],
      "accounts": [
        {
          "name": "vault",
          "pda": {
            "seeds": [
              {
                "kind": "const",
                "value": [
                  118,
                  97,
                  117,
                  108,
                  116
                ]
              },
              {
                "kind": "account",
                "path": "vault.authority",
                "account": "vault"
              }
            ]
          }
        },
        {
          "name": "agentProfile",
          "writable": true
        },
        {
          "name": "authority",
          "signer": true,
          "relations": [
            "vault"
          ]
        }
      ],
      "args": []
    },
    {
      "name": "deposit",
      "docs": [
        "Deposits SOL into the vault. Mints shares at current NAV.",
        "",
        "Math:",
        "NAV/share = vault_balance / total_shares",
        "shares_minted = amount / (NAV/share) = amount * total_shares / vault_balance",
        "",
        "First deposit: 1 lamport = 1 share (NAV = 1.0)."
      ],
      "discriminator": [
        242,
        35,
        198,
        137,
        82,
        225,
        242,
        182
      ],
      "accounts": [
        {
          "name": "vault",
          "writable": true,
          "pda": {
            "seeds": [
              {
                "kind": "const",
                "value": [
                  118,
                  97,
                  117,
                  108,
                  116
                ]
              },
              {
                "kind": "account",
                "path": "vault.authority",
                "account": "vault"
              }
            ]
          }
        },
        {
          "name": "vaultSol",
          "writable": true,
          "pda": {
            "seeds": [
              {
                "kind": "const",
                "value": [
                  118,
                  97,
                  117,
                  108,
                  116,
                  95,
                  115,
                  111,
                  108
                ]
              },
              {
                "kind": "account",
                "path": "vault"
              }
            ]
          }
        },
        {
          "name": "userPosition",
          "writable": true,
          "pda": {
            "seeds": [
              {
                "kind": "const",
                "value": [
                  112,
                  111,
                  115,
                  105,
                  116,
                  105,
                  111,
                  110
                ]
              },
              {
                "kind": "account",
                "path": "vault"
              },
              {
                "kind": "account",
                "path": "user"
              }
            ]
          }
        },
        {
          "name": "user",
          "writable": true,
          "signer": true
        },
        {
          "name": "systemProgram",
          "address": "11111111111111111111111111111111"
        }
      ],
      "args": [
        {
          "name": "amount",
          "type": "u64"
        }
      ]
    },
    {
      "name": "distributeProfits",
      "docs": [
        "Distributes profits into the vault, increasing NAV/share for all holders.",
        "The oracle sends SOL to the vault; the vault tracks which agent generated",
        "the profit and increases that agent's reward counter.",
        "",
        "Architecture note: Profit goes into the shared vault (benefiting all depositors",
        "via NAV appreciation). A configurable agent_fee_bps is carved out and tracked",
        "in the agent's total_rewards_earned for later claim.",
        "",
        "Formula for agent fee carve-out:",
        "agent_reward = (amount * agent_fee_bps) / 10_000",
        "vault_portion = amount - agent_reward",
        "",
        "The agent_reward stays in the vault but is earmarked for the agent.",
        "The vault_portion increases NAV/share for all depositors."
      ],
      "discriminator": [
        251,
        124,
        40,
        116,
        101,
        198,
        242,
        144
      ],
      "accounts": [
        {
          "name": "vault",
          "writable": true,
          "pda": {
            "seeds": [
              {
                "kind": "const",
                "value": [
                  118,
                  97,
                  117,
                  108,
                  116
                ]
              },
              {
                "kind": "account",
                "path": "vault.authority",
                "account": "vault"
              }
            ]
          }
        },
        {
          "name": "vaultSol",
          "writable": true,
          "pda": {
            "seeds": [
              {
                "kind": "const",
                "value": [
                  118,
                  97,
                  117,
                  108,
                  116,
                  95,
                  115,
                  111,
                  108
                ]
              },
              {
                "kind": "account",
                "path": "vault"
              }
            ]
          }
        },
        {
          "name": "agentProfile",
          "docs": [
            "Optional agent profile to attribute rewards to.",
            "If the oracle wants to distribute without agent attribution,",
            "this can be set to the vault account (will be None)."
          ],
          "writable": true,
          "optional": true
        },
        {
          "name": "oracle",
          "writable": true,
          "signer": true
        },
        {
          "name": "systemProgram",
          "address": "11111111111111111111111111111111"
        }
      ],
      "args": [
        {
          "name": "amount",
          "type": "u64"
        },
        {
          "name": "agentFeeBps",
          "type": "u16"
        }
      ]
    },
    {
      "name": "emergencyStop",
      "docs": [
        "Guardian can pause/unpause the vault in case of detected risk."
      ],
      "discriminator": [
        179,
        143,
        200,
        137,
        108,
        245,
        248,
        35
      ],
      "accounts": [
        {
          "name": "vault",
          "writable": true,
          "pda": {
            "seeds": [
              {
                "kind": "const",
                "value": [
                  118,
                  97,
                  117,
                  108,
                  116
                ]
              },
              {
                "kind": "account",
                "path": "vault.authority",
                "account": "vault"
              }
            ]
          }
        },
        {
          "name": "guardian",
          "signer": true
        }
      ],
      "args": [
        {
          "name": "pause",
          "type": "bool"
        }
      ]
    },
    {
      "name": "initialize",
      "docs": [
        "Initialize the vault with authority, guardian, oracle, and policy params."
      ],
      "discriminator": [
        175,
        175,
        109,
        31,
        13,
        152,
        155,
        237
      ],
      "accounts": [
        {
          "name": "vault",
          "writable": true,
          "pda": {
            "seeds": [
              {
                "kind": "const",
                "value": [
                  118,
                  97,
                  117,
                  108,
                  116
                ]
              },
              {
                "kind": "account",
                "path": "authority"
              }
            ]
          }
        },
        {
          "name": "vaultSol",
          "writable": true,
          "pda": {
            "seeds": [
              {
                "kind": "const",
                "value": [
                  118,
                  97,
                  117,
                  108,
                  116,
                  95,
                  115,
                  111,
                  108
                ]
              },
              {
                "kind": "account",
                "path": "vault"
              }
            ]
          }
        },
        {
          "name": "authority",
          "writable": true,
          "signer": true
        },
        {
          "name": "systemProgram",
          "address": "11111111111111111111111111111111"
        }
      ],
      "args": [
        {
          "name": "guardian",
          "type": "pubkey"
        },
        {
          "name": "oracle",
          "type": "pubkey"
        },
        {
          "name": "dailyWithdrawCap",
          "type": "u64"
        },
        {
          "name": "cooldownSeconds",
          "type": "i64"
        }
      ]
    },
    {
      "name": "queryAgentScore",
      "docs": [
        "Computes and emits the agent's on-chain Sharpe-like score.",
        "",
        "Math (all in basis points, integer arithmetic):",
        "n     = trade_count",
        "μ     = sum_returns / n                    (mean return in bps)",
        "σ²    = (sum_sq_returns / n) - μ²          (variance in bps²)",
        "score = μ² * SCORE_PRECISION / σ²          (Sharpe² * precision)",
        "",
        "We emit score_numerator = μ² and score_denominator = σ² so the client",
        "can compute the exact ratio. If σ² = 0 and μ > 0, agent has perfect",
        "consistency → score = MAX_SCORE sentinel value.",
        "",
        "Win rate is also emitted: win_rate_bps = (winning_trades * 10000) / trade_count"
      ],
      "discriminator": [
        169,
        47,
        52,
        74,
        147,
        229,
        117,
        172
      ],
      "accounts": [
        {
          "name": "vault",
          "pda": {
            "seeds": [
              {
                "kind": "const",
                "value": [
                  118,
                  97,
                  117,
                  108,
                  116
                ]
              },
              {
                "kind": "account",
                "path": "vault.authority",
                "account": "vault"
              }
            ]
          }
        },
        {
          "name": "agentProfile"
        }
      ],
      "args": []
    },
    {
      "name": "registerAgent",
      "docs": [
        "Authority registers a new agent that can earn rewards from the vault.",
        "Creates an AgentProfile PDA seeded by [b\"agent\", vault, agent_pubkey]."
      ],
      "discriminator": [
        135,
        157,
        66,
        195,
        2,
        113,
        175,
        30
      ],
      "accounts": [
        {
          "name": "vault",
          "writable": true,
          "pda": {
            "seeds": [
              {
                "kind": "const",
                "value": [
                  118,
                  97,
                  117,
                  108,
                  116
                ]
              },
              {
                "kind": "account",
                "path": "vault.authority",
                "account": "vault"
              }
            ]
          }
        },
        {
          "name": "agentProfile",
          "writable": true,
          "pda": {
            "seeds": [
              {
                "kind": "const",
                "value": [
                  97,
                  103,
                  101,
                  110,
                  116
                ]
              },
              {
                "kind": "account",
                "path": "vault"
              },
              {
                "kind": "arg",
                "path": "agentKey"
              }
            ]
          }
        },
        {
          "name": "authority",
          "writable": true,
          "signer": true,
          "relations": [
            "vault"
          ]
        },
        {
          "name": "systemProgram",
          "address": "11111111111111111111111111111111"
        }
      ],
      "args": [
        {
          "name": "agentKey",
          "type": "pubkey"
        }
      ]
    },
    {
      "name": "reportTrade",
      "docs": [
        "Oracle reports a single trade result for an agent.",
        "",
        "Parameters:",
        "pnl_bps: signed basis points (1 bp = 0.01%). E.g., +150 = +1.50%.",
        "Allows negative values to penalize losing trades.",
        "is_win:  whether this trade was profitable (for win-rate tracking).",
        "",
        "On-chain statistics updated:",
        "trade_count += 1",
        "winning_trades += is_win ? 1 : 0",
        "cumulative_pnl += pnl_bps",
        "sum_returns += pnl_bps         (for mean calculation)",
        "sum_sq_returns += pnl_bps²     (for variance calculation)",
        "",
        "These enable the Sharpe-like scoring:",
        "mean = sum_returns / trade_count",
        "var  = (sum_sq_returns / trade_count) - mean²",
        "score² = mean² / var   (used directly for weight calculation)"
      ],
      "discriminator": [
        158,
        94,
        16,
        241,
        227,
        100,
        44,
        98
      ],
      "accounts": [
        {
          "name": "vault",
          "pda": {
            "seeds": [
              {
                "kind": "const",
                "value": [
                  118,
                  97,
                  117,
                  108,
                  116
                ]
              },
              {
                "kind": "account",
                "path": "vault.authority",
                "account": "vault"
              }
            ]
          }
        },
        {
          "name": "agentProfile",
          "writable": true
        },
        {
          "name": "oracle",
          "signer": true
        }
      ],
      "args": [
        {
          "name": "pnlBps",
          "type": "i64"
        },
        {
          "name": "isWin",
          "type": "bool"
        }
      ]
    },
    {
      "name": "setWhitelist",
      "docs": [
        "User sets their own whitelisted withdrawal destinations.",
        "Up to MAX_WHITELIST (4) addresses. When set, withdrawals can only",
        "go to self or one of these addresses."
      ],
      "discriminator": [
        69,
        161,
        114,
        252,
        244,
        66,
        197,
        48
      ],
      "accounts": [
        {
          "name": "vault",
          "pda": {
            "seeds": [
              {
                "kind": "const",
                "value": [
                  118,
                  97,
                  117,
                  108,
                  116
                ]
              },
              {
                "kind": "account",
                "path": "vault.authority",
                "account": "vault"
              }
            ]
          }
        },
        {
          "name": "userPosition",
          "writable": true,
          "pda": {
            "seeds": [
              {
                "kind": "const",
                "value": [
                  112,
                  111,
                  115,
                  105,
                  116,
                  105,
                  111,
                  110
                ]
              },
              {
                "kind": "account",
                "path": "vault"
              },
              {
                "kind": "account",
                "path": "user"
              }
            ]
          }
        },
        {
          "name": "user",
          "signer": true
        }
      ],
      "args": [
        {
          "name": "destinations",
          "type": {
            "vec": "pubkey"
          }
        }
      ]
    },
    {
      "name": "updatePolicy",
      "docs": [
        "Guardian updates policy parameters (daily cap, cooldown)."
      ],
      "discriminator": [
        212,
        245,
        246,
        7,
        163,
        151,
        18,
        57
      ],
      "accounts": [
        {
          "name": "vault",
          "writable": true,
          "pda": {
            "seeds": [
              {
                "kind": "const",
                "value": [
                  118,
                  97,
                  117,
                  108,
                  116
                ]
              },
              {
                "kind": "account",
                "path": "vault.authority",
                "account": "vault"
              }
            ]
          }
        },
        {
          "name": "guardian",
          "signer": true
        }
      ],
      "args": [
        {
          "name": "newDailyCap",
          "type": "u64"
        },
        {
          "name": "newCooldownSeconds",
          "type": "i64"
        }
      ]
    },
    {
      "name": "updateRoles",
      "docs": [
        "Authority can update guardian or oracle addresses."
      ],
      "discriminator": [
        220,
        152,
        205,
        233,
        177,
        123,
        219,
        125
      ],
      "accounts": [
        {
          "name": "vault",
          "writable": true,
          "pda": {
            "seeds": [
              {
                "kind": "const",
                "value": [
                  118,
                  97,
                  117,
                  108,
                  116
                ]
              },
              {
                "kind": "account",
                "path": "vault.authority",
                "account": "vault"
              }
            ]
          }
        },
        {
          "name": "authority",
          "signer": true,
          "relations": [
            "vault"
          ]
        }
      ],
      "args": [
        {
          "name": "newGuardian",
          "type": {
            "option": "pubkey"
          }
        },
        {
          "name": "newOracle",
          "type": {
            "option": "pubkey"
          }
        }
      ]
    },
    {
      "name": "withdraw",
      "docs": [
        "Burns shares and returns SOL. Enforces:",
        "1. Cooldown: last_withdraw_ts + cooldown_seconds <= now",
        "2. Daily cap: daily_withdrawn + withdraw_amount <= daily_withdraw_cap",
        "(daily counter resets each UTC day = unix_ts / 86400)",
        "3. Whitelist: if user has whitelisted destinations, the `user` (recipient)",
        "must match one of them. (Self-withdraw always allowed.)",
        "",
        "Withdraw math:",
        "sol_returned = shares_burned * vault_balance / total_shares"
      ],
      "discriminator": [
        183,
        18,
        70,
        156,
        148,
        109,
        161,
        34
      ],
      "accounts": [
        {
          "name": "vault",
          "writable": true,
          "pda": {
            "seeds": [
              {
                "kind": "const",
                "value": [
                  118,
                  97,
                  117,
                  108,
                  116
                ]
              },
              {
                "kind": "account",
                "path": "vault.authority",
                "account": "vault"
              }
            ]
          }
        },
        {
          "name": "vaultSol",
          "writable": true,
          "pda": {
            "seeds": [
              {
                "kind": "const",
                "value": [
                  118,
                  97,
                  117,
                  108,
                  116,
                  95,
                  115,
                  111,
                  108
                ]
              },
              {
                "kind": "account",
                "path": "vault"
              }
            ]
          }
        },
        {
          "name": "userPosition",
          "writable": true,
          "pda": {
            "seeds": [
              {
                "kind": "const",
                "value": [
                  112,
                  111,
                  115,
                  105,
                  116,
                  105,
                  111,
                  110
                ]
              },
              {
                "kind": "account",
                "path": "vault"
              },
              {
                "kind": "account",
                "path": "user"
              }
            ]
          }
        },
        {
          "name": "owner",
          "writable": true,
          "relations": [
            "userPosition"
          ]
        },
        {
          "name": "user",
          "writable": true,
          "signer": true
        },
        {
          "name": "systemProgram",
          "address": "11111111111111111111111111111111"
        }
      ],
      "args": [
        {
          "name": "sharesToBurn",
          "type": "u64"
        }
      ]
    }
  ],
  "accounts": [
    {
      "name": "agentProfile",
      "discriminator": [
        60,
        227,
        42,
        24,
        0,
        87,
        86,
        205
      ]
    },
    {
      "name": "userPosition",
      "discriminator": [
        251,
        248,
        209,
        245,
        83,
        234,
        17,
        27
      ]
    },
    {
      "name": "vault",
      "discriminator": [
        211,
        8,
        232,
        43,
        2,
        152,
        117,
        119
      ]
    }
  ],
  "events": [
    {
      "name": "agentDeactivated",
      "discriminator": [
        138,
        251,
        82,
        87,
        119,
        148,
        20,
        180
      ]
    },
    {
      "name": "agentRegistered",
      "discriminator": [
        191,
        78,
        217,
        54,
        232,
        100,
        189,
        85
      ]
    },
    {
      "name": "agentRewardClaimed",
      "discriminator": [
        172,
        9,
        78,
        123,
        68,
        111,
        207,
        229
      ]
    },
    {
      "name": "agentScoreComputed",
      "discriminator": [
        167,
        79,
        80,
        53,
        66,
        32,
        5,
        169
      ]
    },
    {
      "name": "deposited",
      "discriminator": [
        111,
        141,
        26,
        45,
        161,
        35,
        100,
        57
      ]
    },
    {
      "name": "emergencyAction",
      "discriminator": [
        39,
        136,
        106,
        150,
        85,
        114,
        170,
        156
      ]
    },
    {
      "name": "epochAdvanced",
      "discriminator": [
        41,
        220,
        14,
        123,
        117,
        70,
        117,
        157
      ]
    },
    {
      "name": "policyUpdated",
      "discriminator": [
        225,
        112,
        112,
        67,
        95,
        236,
        245,
        161
      ]
    },
    {
      "name": "profitsDistributed",
      "discriminator": [
        226,
        149,
        151,
        234,
        30,
        86,
        112,
        125
      ]
    },
    {
      "name": "rolesUpdated",
      "discriminator": [
        81,
        37,
        176,
        32,
        30,
        204,
        251,
        246
      ]
    },
    {
      "name": "tradeReported",
      "discriminator": [
        120,
        95,
        181,
        47,
        62,
        207,
        97,
        204
      ]
    },
    {
      "name": "vaultInitialized",
      "discriminator": [
        180,
        43,
        207,
        2,
        18,
        71,
        3,
        75
      ]
    },
    {
      "name": "whitelistUpdated",
      "discriminator": [
        205,
        110,
        205,
        193,
        238,
        237,
        220,
        22
      ]
    },
    {
      "name": "withdrawn",
      "discriminator": [
        20,
        89,
        223,
        198,
        194,
        124,
        219,
        13
      ]
    }
  ],
  "errors": [
    {
      "code": 6000,
      "name": "vaultPaused",
      "msg": "Vault is paused — emergency stop active"
    },
    {
      "code": 6001,
      "name": "zeroAmount",
      "msg": "Amount must be greater than zero"
    },
    {
      "code": 6002,
      "name": "belowMinDeposit",
      "msg": "Deposit below minimum threshold"
    },
    {
      "code": 6003,
      "name": "zeroShares",
      "msg": "Calculated shares would be zero"
    },
    {
      "code": 6004,
      "name": "insufficientShares",
      "msg": "Insufficient shares for withdrawal"
    },
    {
      "code": 6005,
      "name": "noShareholders",
      "msg": "No shareholders in the vault"
    },
    {
      "code": 6006,
      "name": "mathOverflow",
      "msg": "Math overflow"
    },
    {
      "code": 6007,
      "name": "unauthorized",
      "msg": "unauthorized"
    },
    {
      "code": 6008,
      "name": "cooldownActive",
      "msg": "Withdrawal cooldown period still active"
    },
    {
      "code": 6009,
      "name": "dailyCapExceeded",
      "msg": "Daily withdrawal cap exceeded"
    },
    {
      "code": 6010,
      "name": "destinationNotWhitelisted",
      "msg": "Withdrawal destination not in whitelist"
    },
    {
      "code": 6011,
      "name": "tooManyWhitelistEntries",
      "msg": "Too many whitelist entries (max 4)"
    },
    {
      "code": 6012,
      "name": "agentInactive",
      "msg": "Agent is inactive"
    },
    {
      "code": 6013,
      "name": "noTradeData",
      "msg": "No trade data available for scoring"
    },
    {
      "code": 6014,
      "name": "feeTooHigh",
      "msg": "Agent fee exceeds maximum (30%)"
    },
    {
      "code": 6015,
      "name": "insufficientFunds",
      "msg": "Insufficient funds in vault"
    }
  ],
  "types": [
    {
      "name": "agentDeactivated",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "vault",
            "type": "pubkey"
          },
          {
            "name": "agent",
            "type": "pubkey"
          }
        ]
      }
    },
    {
      "name": "agentProfile",
      "docs": [
        "┌─────────────────────────────────────────────────────────┐",
        "│  AgentProfile — On-chain performance scoring            │",
        "│                                                         │",
        "│  Seeds: [b\"agent\", vault.key(), agent.key()]            │",
        "│                                                         │",
        "│  Statistics for Sharpe-like scoring:                     │",
        "│    μ  = sum_returns / trade_count                       │",
        "│    σ² = (sum_sq_returns / n) - μ²                       │",
        "│    Sharpe² = μ² / σ²                                    │",
        "│                                                         │",
        "│  Weight for reward allocation:                          │",
        "│    w_i = Sharpe_i² / Σ Sharpe_j²                       │",
        "│    This is computed off-chain or in distribute_profits  │",
        "│    using the raw stats stored here.                     │",
        "└─────────────────────────────────────────────────────────┘"
      ],
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "agent",
            "docs": [
              "Public key of the agent"
            ],
            "type": "pubkey"
          },
          {
            "name": "vault",
            "docs": [
              "Vault this agent operates for"
            ],
            "type": "pubkey"
          },
          {
            "name": "tradeCount",
            "docs": [
              "Total number of trades reported"
            ],
            "type": "u32"
          },
          {
            "name": "winningTrades",
            "docs": [
              "Number of winning trades (for win-rate calculation)"
            ],
            "type": "u32"
          },
          {
            "name": "cumulativePnl",
            "docs": [
              "Cumulative PnL in basis points (signed)"
            ],
            "type": "i64"
          },
          {
            "name": "sumReturns",
            "docs": [
              "Σ(return_i) — sum of all individual trade returns (bps, signed)",
              "Used for mean calculation: μ = sum_returns / trade_count"
            ],
            "type": "i128"
          },
          {
            "name": "sumSqReturns",
            "docs": [
              "Σ(return_i²) — sum of squared returns (always non-negative)",
              "Used for variance: σ² = sum_sq_returns/n - (sum_returns/n)²"
            ],
            "type": "u128"
          },
          {
            "name": "totalRewardsEarned",
            "docs": [
              "Accumulated rewards earmarked for this agent (lamports)"
            ],
            "type": "u64"
          },
          {
            "name": "lastReportTs",
            "docs": [
              "Timestamp of last trade report"
            ],
            "type": "i64"
          },
          {
            "name": "isActive",
            "docs": [
              "Whether the agent is actively receiving reports"
            ],
            "type": "bool"
          }
        ]
      }
    },
    {
      "name": "agentRegistered",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "vault",
            "type": "pubkey"
          },
          {
            "name": "agent",
            "type": "pubkey"
          }
        ]
      }
    },
    {
      "name": "agentRewardClaimed",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "agent",
            "type": "pubkey"
          },
          {
            "name": "amount",
            "type": "u64"
          }
        ]
      }
    },
    {
      "name": "agentScoreComputed",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "agent",
            "type": "pubkey"
          },
          {
            "name": "tradeCount",
            "type": "u32"
          },
          {
            "name": "winRateBps",
            "type": "u64"
          },
          {
            "name": "cumulativePnl",
            "type": "i64"
          },
          {
            "name": "scoreNumerator",
            "docs": [
              "μ² (mean return squared) — numerator of Sharpe²"
            ],
            "type": "u128"
          },
          {
            "name": "scoreDenominator",
            "docs": [
              "σ² (variance) — denominator of Sharpe²"
            ],
            "type": "u128"
          },
          {
            "name": "meanPositive",
            "docs": [
              "Whether mean return is non-negative"
            ],
            "type": "bool"
          }
        ]
      }
    },
    {
      "name": "deposited",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "user",
            "type": "pubkey"
          },
          {
            "name": "amount",
            "type": "u64"
          },
          {
            "name": "sharesMinted",
            "type": "u64"
          },
          {
            "name": "totalVaultShares",
            "type": "u64"
          }
        ]
      }
    },
    {
      "name": "emergencyAction",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "guardian",
            "type": "pubkey"
          },
          {
            "name": "paused",
            "type": "bool"
          },
          {
            "name": "timestamp",
            "type": "i64"
          }
        ]
      }
    },
    {
      "name": "epochAdvanced",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "vault",
            "type": "pubkey"
          },
          {
            "name": "previousEpoch",
            "type": "u64"
          },
          {
            "name": "newEpoch",
            "type": "u64"
          },
          {
            "name": "epochProfit",
            "type": "u64"
          }
        ]
      }
    },
    {
      "name": "policyUpdated",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "guardian",
            "type": "pubkey"
          },
          {
            "name": "dailyWithdrawCap",
            "type": "u64"
          },
          {
            "name": "cooldownSeconds",
            "type": "i64"
          }
        ]
      }
    },
    {
      "name": "profitsDistributed",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "oracle",
            "type": "pubkey"
          },
          {
            "name": "amount",
            "type": "u64"
          },
          {
            "name": "agentReward",
            "type": "u64"
          },
          {
            "name": "totalVaultBalance",
            "type": "u64"
          },
          {
            "name": "totalProfitsDistributed",
            "type": "u64"
          }
        ]
      }
    },
    {
      "name": "rolesUpdated",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "authority",
            "type": "pubkey"
          },
          {
            "name": "guardian",
            "type": "pubkey"
          },
          {
            "name": "oracle",
            "type": "pubkey"
          }
        ]
      }
    },
    {
      "name": "tradeReported",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "agent",
            "type": "pubkey"
          },
          {
            "name": "pnlBps",
            "type": "i64"
          },
          {
            "name": "isWin",
            "type": "bool"
          },
          {
            "name": "tradeCount",
            "type": "u32"
          },
          {
            "name": "cumulativePnl",
            "type": "i64"
          }
        ]
      }
    },
    {
      "name": "userPosition",
      "docs": [
        "┌─────────────────────────────────────────────────────────┐",
        "│  UserPosition — Per-user deposit & share tracking       │",
        "│                                                         │",
        "│  Seeds: [b\"position\", vault.key(), user.key()]          │",
        "│  Includes guardian policy state (daily cap, whitelist)   │",
        "└─────────────────────────────────────────────────────────┘"
      ],
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "owner",
            "docs": [
              "Owner of this position"
            ],
            "type": "pubkey"
          },
          {
            "name": "vault",
            "docs": [
              "Vault this position belongs to"
            ],
            "type": "pubkey"
          },
          {
            "name": "shares",
            "docs": [
              "Number of shares held"
            ],
            "type": "u64"
          },
          {
            "name": "totalDeposited",
            "docs": [
              "Cumulative SOL deposited"
            ],
            "type": "u64"
          },
          {
            "name": "totalWithdrawn",
            "docs": [
              "Cumulative SOL withdrawn"
            ],
            "type": "u64"
          },
          {
            "name": "lastActionTs",
            "docs": [
              "Last action timestamp"
            ],
            "type": "i64"
          },
          {
            "name": "lastWithdrawTs",
            "docs": [
              "Timestamp of last withdrawal (for cooldown enforcement)"
            ],
            "type": "i64"
          },
          {
            "name": "lastWithdrawDay",
            "docs": [
              "UTC day number of last withdrawal (for daily cap reset)"
            ],
            "type": "i64"
          },
          {
            "name": "dailyWithdrawn",
            "docs": [
              "Lamports withdrawn so far today"
            ],
            "type": "u64"
          },
          {
            "name": "whitelist",
            "docs": [
              "Whitelisted withdrawal destinations (Pubkey::default = unused slot)"
            ],
            "type": {
              "array": [
                "pubkey",
                4
              ]
            }
          },
          {
            "name": "whitelistCount",
            "docs": [
              "Number of active whitelist entries (0 = no restriction)"
            ],
            "type": "u8"
          }
        ]
      }
    },
    {
      "name": "vault",
      "docs": [
        "┌─────────────────────────────────────────────────────────┐",
        "│  Vault — Central state for the Fee-Sharing Vault        │",
        "│                                                         │",
        "│  Seeds: [b\"vault\", authority.key()]                     │",
        "│  Size:  8 (discriminator) + 155 bytes                   │",
        "└─────────────────────────────────────────────────────────┘"
      ],
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "authority",
            "docs": [
              "The authority that created and controls the vault"
            ],
            "type": "pubkey"
          },
          {
            "name": "guardian",
            "docs": [
              "Risk guardian who can trigger emergency stop & update policy"
            ],
            "type": "pubkey"
          },
          {
            "name": "oracle",
            "docs": [
              "Alpha Oracle authorized to distribute profits & report trades"
            ],
            "type": "pubkey"
          },
          {
            "name": "totalShares",
            "docs": [
              "Total outstanding share tokens (denominator for NAV calc)"
            ],
            "type": "u64"
          },
          {
            "name": "totalDeposited",
            "docs": [
              "Cumulative SOL deposited (lifetime tracking metric)"
            ],
            "type": "u64"
          },
          {
            "name": "totalProfitsDistributed",
            "docs": [
              "Cumulative profits distributed (lifetime tracking metric)"
            ],
            "type": "u64"
          },
          {
            "name": "isPaused",
            "docs": [
              "Emergency pause flag"
            ],
            "type": "bool"
          },
          {
            "name": "bump",
            "docs": [
              "PDA bump for vault account"
            ],
            "type": "u8"
          },
          {
            "name": "vaultSolBump",
            "docs": [
              "PDA bump for vault SOL holder"
            ],
            "type": "u8"
          },
          {
            "name": "dailyWithdrawCap",
            "docs": [
              "Maximum lamports a user can withdraw per UTC day (0 = unlimited)"
            ],
            "type": "u64"
          },
          {
            "name": "cooldownSeconds",
            "docs": [
              "Minimum seconds between withdrawals per user (0 = no cooldown)"
            ],
            "type": "i64"
          },
          {
            "name": "epoch",
            "docs": [
              "Current epoch number (incremented by authority)"
            ],
            "type": "u64"
          },
          {
            "name": "epochProfit",
            "docs": [
              "Profit accumulated in current epoch (resets on advance)"
            ],
            "type": "u64"
          },
          {
            "name": "agentCount",
            "docs": [
              "Number of registered agents"
            ],
            "type": "u32"
          }
        ]
      }
    },
    {
      "name": "vaultInitialized",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "authority",
            "type": "pubkey"
          },
          {
            "name": "guardian",
            "type": "pubkey"
          },
          {
            "name": "oracle",
            "type": "pubkey"
          },
          {
            "name": "dailyWithdrawCap",
            "type": "u64"
          },
          {
            "name": "cooldownSeconds",
            "type": "i64"
          }
        ]
      }
    },
    {
      "name": "whitelistUpdated",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "user",
            "type": "pubkey"
          },
          {
            "name": "count",
            "type": "u8"
          }
        ]
      }
    },
    {
      "name": "withdrawn",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "user",
            "type": "pubkey"
          },
          {
            "name": "sharesBurned",
            "type": "u64"
          },
          {
            "name": "amountReturned",
            "type": "u64"
          },
          {
            "name": "totalVaultShares",
            "type": "u64"
          }
        ]
      }
    }
  ]
};

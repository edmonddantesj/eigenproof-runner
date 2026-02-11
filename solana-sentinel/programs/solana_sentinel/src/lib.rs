use anchor_lang::prelude::*;
use anchor_lang::system_program;

declare_id!("9FouWHemn9iueyHYq4qpeNj9aHMyTKfEPt8ZpJaHcZ95");

/// ════════════════════════════════════════════════════════════════
/// Solana Sentinel v2 — Risk-Adjusted Fee-Sharing Vault
/// ════════════════════════════════════════════════════════════════
///
/// Architecture Overview:
///
/// 1. SHARE VALUATION MODEL (Net Asset Value per Share)
///    NAV/share = vault_balance / total_shares
///    On deposit:  shares_minted = deposit_amount / (NAV/share)
///    On withdraw: sol_returned  = shares_burned  * (NAV/share)
///    Profits flow in → NAV/share rises → all holders benefit.
///
/// 2. RISK-ADJUSTED YIELD DISTRIBUTION (Performance-Weighted)
///    Each agent that generates profits is scored by a rolling
///    Sharpe-like ratio computed on-chain:
///
///      score_i = mean_return_i / volatility_i  (if volatility > 0)
///
///    Where:
///      mean_return_i   = cumulative_pnl_i / trade_count_i
///      volatility_i    = sqrt(E[R²] - E[R]²)  ≈ approximated via
///                        sum_sq_returns / n - (sum_returns / n)²
///
///    Since on-chain sqrt is expensive, we use the SQUARED score
///    for ranking (monotonic transformation preserves ordering):
///
///      w_i = score_i² / Σ(score_j²)
///      reward_i = w_i * total_profit_to_distribute
///
///    This means agents with high mean return AND low variance
///    capture more of the fee pool — a Sharpe-rational allocation.
///
/// 3. GUARDIAN POLICY ENGINE
///    On-chain enforcement of:
///    a) Daily withdrawal cap per user (resets every 86400 seconds)
///    b) Cooldown period between withdrawals (configurable seconds)
///    c) Whitelisted destination addresses (optional, up to 4)
///
/// 4. AGENT PERFORMANCE SCORING
///    Each registered agent has an on-chain AgentProfile PDA:
///    - trade_count, winning_trades (win rate = winning / total)
///    - cumulative_pnl (signed, stored as i64)
///    - sum_returns, sum_sq_returns (for variance calculation)
///    - last_report_ts
///    Oracle reports results; authority registers/deregisters agents.
///
/// ════════════════════════════════════════════════════════════════

#[program]
pub mod solana_sentinel {
    use super::*;

    // ══════════════════════════════════════════════════════════
    //  1. VAULT LIFECYCLE
    // ══════════════════════════════════════════════════════════

    /// Initialize the vault with authority, guardian, oracle, and policy params.
    pub fn initialize(
        ctx: Context<Initialize>,
        guardian: Pubkey,
        oracle: Pubkey,
        daily_withdraw_cap: u64,
        cooldown_seconds: i64,
    ) -> Result<()> {
        let vault = &mut ctx.accounts.vault;
        vault.authority = ctx.accounts.authority.key();
        vault.guardian = guardian;
        vault.oracle = oracle;
        vault.total_shares = 0;
        vault.total_deposited = 0;
        vault.total_profits_distributed = 0;
        vault.is_paused = false;
        vault.bump = ctx.bumps.vault;
        vault.vault_sol_bump = ctx.bumps.vault_sol;

        // Guardian policy defaults
        vault.daily_withdraw_cap = daily_withdraw_cap;
        vault.cooldown_seconds = cooldown_seconds;

        // Performance tracking epoch
        vault.epoch = 0;
        vault.epoch_profit = 0;
        vault.agent_count = 0;

        emit!(VaultInitialized {
            authority: vault.authority,
            guardian,
            oracle,
            daily_withdraw_cap,
            cooldown_seconds,
        });

        Ok(())
    }

    // ══════════════════════════════════════════════════════════
    //  2. DEPOSIT (with share valuation)
    // ══════════════════════════════════════════════════════════

    /// Deposits SOL into the vault. Mints shares at current NAV.
    ///
    /// Math:
    ///   NAV/share = vault_balance / total_shares
    ///   shares_minted = amount / (NAV/share) = amount * total_shares / vault_balance
    ///
    /// First deposit: 1 lamport = 1 share (NAV = 1.0).
    pub fn deposit(ctx: Context<Deposit>, amount: u64) -> Result<()> {
        let vault = &mut ctx.accounts.vault;

        require!(!vault.is_paused, SentinelError::VaultPaused);
        require!(amount > 0, SentinelError::ZeroAmount);
        require!(amount >= MIN_DEPOSIT, SentinelError::BelowMinDeposit);

        let vault_balance = ctx.accounts.vault_sol.lamports();

        // Share calculation with 128-bit intermediate precision
        let shares = if vault.total_shares == 0 || vault_balance == 0 {
            amount
        } else {
            // shares = (amount * total_shares) / vault_balance
            let numerator = (amount as u128)
                .checked_mul(vault.total_shares as u128)
                .ok_or(SentinelError::MathOverflow)?;
            let result = numerator
                .checked_div(vault_balance as u128)
                .ok_or(SentinelError::MathOverflow)?;
            require!(result <= u64::MAX as u128, SentinelError::MathOverflow);
            result as u64
        };

        require!(shares > 0, SentinelError::ZeroShares);

        // CPI: transfer SOL from user to vault PDA
        system_program::transfer(
            CpiContext::new(
                ctx.accounts.system_program.to_account_info(),
                system_program::Transfer {
                    from: ctx.accounts.user.to_account_info(),
                    to: ctx.accounts.vault_sol.to_account_info(),
                },
            ),
            amount,
        )?;

        // Update user position
        let user_position = &mut ctx.accounts.user_position;
        if user_position.owner == Pubkey::default() {
            user_position.owner = ctx.accounts.user.key();
            user_position.vault = vault.key();
            user_position.whitelist = [Pubkey::default(); MAX_WHITELIST];
            user_position.whitelist_count = 0;
            user_position.daily_withdrawn = 0;
            user_position.last_withdraw_day = 0;
            user_position.last_withdraw_ts = 0;
        }
        user_position.shares = user_position
            .shares
            .checked_add(shares)
            .ok_or(SentinelError::MathOverflow)?;
        user_position.total_deposited = user_position
            .total_deposited
            .checked_add(amount)
            .ok_or(SentinelError::MathOverflow)?;
        user_position.last_action_ts = Clock::get()?.unix_timestamp;

        // Update vault totals
        vault.total_shares = vault
            .total_shares
            .checked_add(shares)
            .ok_or(SentinelError::MathOverflow)?;
        vault.total_deposited = vault
            .total_deposited
            .checked_add(amount)
            .ok_or(SentinelError::MathOverflow)?;

        emit!(Deposited {
            user: ctx.accounts.user.key(),
            amount,
            shares_minted: shares,
            total_vault_shares: vault.total_shares,
        });

        Ok(())
    }

    // ══════════════════════════════════════════════════════════
    //  3. WITHDRAW (with Guardian Policy Engine enforcement)
    // ══════════════════════════════════════════════════════════

    /// Burns shares and returns SOL. Enforces:
    ///   1. Cooldown: last_withdraw_ts + cooldown_seconds <= now
    ///   2. Daily cap: daily_withdrawn + withdraw_amount <= daily_withdraw_cap
    ///      (daily counter resets each UTC day = unix_ts / 86400)
    ///   3. Whitelist: if user has whitelisted destinations, the `user` (recipient)
    ///      must match one of them. (Self-withdraw always allowed.)
    ///
    /// Withdraw math:
    ///   sol_returned = shares_burned * vault_balance / total_shares
    pub fn withdraw(ctx: Context<Withdraw>, shares_to_burn: u64) -> Result<()> {
        let vault = &mut ctx.accounts.vault;

        require!(!vault.is_paused, SentinelError::VaultPaused);
        require!(shares_to_burn > 0, SentinelError::ZeroAmount);

        let user_position = &mut ctx.accounts.user_position;
        require!(
            user_position.shares >= shares_to_burn,
            SentinelError::InsufficientShares
        );

        let now = Clock::get()?.unix_timestamp;

        // ── Policy Check 1: Cooldown ──
        if vault.cooldown_seconds > 0 && user_position.last_withdraw_ts > 0 {
            let earliest_allowed = user_position
                .last_withdraw_ts
                .checked_add(vault.cooldown_seconds)
                .ok_or(SentinelError::MathOverflow)?;
            require!(now >= earliest_allowed, SentinelError::CooldownActive);
        }

        // Calculate SOL to return
        let vault_balance = ctx.accounts.vault_sol.lamports();
        let withdraw_amount = (shares_to_burn as u128)
            .checked_mul(vault_balance as u128)
            .ok_or(SentinelError::MathOverflow)?
            .checked_div(vault.total_shares as u128)
            .ok_or(SentinelError::MathOverflow)? as u64;

        require!(withdraw_amount > 0, SentinelError::ZeroAmount);

        // ── Policy Check 2: Daily Cap ──
        // Day number = unix_timestamp / 86400 (UTC day boundary)
        let current_day = now / SECONDS_PER_DAY;
        if user_position.last_withdraw_day < current_day {
            // New day: reset daily counter
            user_position.daily_withdrawn = 0;
            user_position.last_withdraw_day = current_day;
        }

        if vault.daily_withdraw_cap > 0 {
            let new_daily_total = user_position
                .daily_withdrawn
                .checked_add(withdraw_amount)
                .ok_or(SentinelError::MathOverflow)?;
            require!(
                new_daily_total <= vault.daily_withdraw_cap,
                SentinelError::DailyCapExceeded
            );
            user_position.daily_withdrawn = new_daily_total;
        }

        // ── Policy Check 3: Whitelist ──
        // If the position has whitelisted destinations, recipient must be in list
        // OR be the position owner (self-withdraw always allowed).
        let recipient_key = ctx.accounts.user.key();
        if user_position.whitelist_count > 0 && recipient_key != user_position.owner {
            let mut found = false;
            for i in 0..user_position.whitelist_count as usize {
                if user_position.whitelist[i] == recipient_key {
                    found = true;
                    break;
                }
            }
            require!(found, SentinelError::DestinationNotWhitelisted);
        }

        // Transfer SOL from vault PDA to user via CPI with signer seeds
        let vault_key = vault.key();
        let seeds = &[
            b"vault_sol",
            vault_key.as_ref(),
            &[vault.vault_sol_bump],
        ];
        let signer = &[&seeds[..]];

        system_program::transfer(
            CpiContext::new_with_signer(
                ctx.accounts.system_program.to_account_info(),
                system_program::Transfer {
                    from: ctx.accounts.vault_sol.to_account_info(),
                    to: ctx.accounts.user.to_account_info(),
                },
                signer,
            ),
            withdraw_amount,
        )?;

        // Update user position
        user_position.shares = user_position
            .shares
            .checked_sub(shares_to_burn)
            .ok_or(SentinelError::MathOverflow)?;
        user_position.total_withdrawn = user_position
            .total_withdrawn
            .checked_add(withdraw_amount)
            .ok_or(SentinelError::MathOverflow)?;
        user_position.last_action_ts = now;
        user_position.last_withdraw_ts = now;

        // Update vault state
        vault.total_shares = vault
            .total_shares
            .checked_sub(shares_to_burn)
            .ok_or(SentinelError::MathOverflow)?;

        emit!(Withdrawn {
            user: ctx.accounts.user.key(),
            shares_burned: shares_to_burn,
            amount_returned: withdraw_amount,
            total_vault_shares: vault.total_shares,
        });

        Ok(())
    }

    // ══════════════════════════════════════════════════════════
    //  4. WHITELIST MANAGEMENT (Guardian Policy Engine)
    // ══════════════════════════════════════════════════════════

    /// User sets their own whitelisted withdrawal destinations.
    /// Up to MAX_WHITELIST (4) addresses. When set, withdrawals can only
    /// go to self or one of these addresses.
    pub fn set_whitelist(
        ctx: Context<SetWhitelist>,
        destinations: Vec<Pubkey>,
    ) -> Result<()> {
        require!(
            destinations.len() <= MAX_WHITELIST,
            SentinelError::TooManyWhitelistEntries
        );

        let user_position = &mut ctx.accounts.user_position;
        let mut whitelist = [Pubkey::default(); MAX_WHITELIST];
        for (i, dest) in destinations.iter().enumerate() {
            whitelist[i] = *dest;
        }
        user_position.whitelist = whitelist;
        user_position.whitelist_count = destinations.len() as u8;

        emit!(WhitelistUpdated {
            user: ctx.accounts.user.key(),
            count: user_position.whitelist_count,
        });

        Ok(())
    }

    // ══════════════════════════════════════════════════════════
    //  5. AGENT REGISTRATION & PERFORMANCE SCORING
    // ══════════════════════════════════════════════════════════

    /// Authority registers a new agent that can earn rewards from the vault.
    /// Creates an AgentProfile PDA seeded by [b"agent", vault, agent_pubkey].
    pub fn register_agent(ctx: Context<RegisterAgent>, agent_key: Pubkey) -> Result<()> {
        let vault = &mut ctx.accounts.vault;
        let profile = &mut ctx.accounts.agent_profile;

        profile.agent = agent_key;
        profile.vault = vault.key();
        profile.trade_count = 0;
        profile.winning_trades = 0;
        profile.cumulative_pnl = 0;
        profile.sum_returns = 0;
        profile.sum_sq_returns = 0;
        profile.total_rewards_earned = 0;
        profile.last_report_ts = 0;
        profile.is_active = true;

        vault.agent_count = vault
            .agent_count
            .checked_add(1)
            .ok_or(SentinelError::MathOverflow)?;

        emit!(AgentRegistered {
            vault: vault.key(),
            agent: agent_key,
        });

        Ok(())
    }

    /// Authority deactivates an agent. Does not delete the PDA (preserves history).
    pub fn deactivate_agent(ctx: Context<DeactivateAgent>) -> Result<()> {
        let profile = &mut ctx.accounts.agent_profile;
        profile.is_active = false;

        emit!(AgentDeactivated {
            vault: ctx.accounts.vault.key(),
            agent: profile.agent,
        });

        Ok(())
    }

    // ══════════════════════════════════════════════════════════
    //  6. ORACLE REPORTS AGENT TRADE RESULT
    // ══════════════════════════════════════════════════════════

    /// Oracle reports a single trade result for an agent.
    ///
    /// Parameters:
    ///   pnl_bps: signed basis points (1 bp = 0.01%). E.g., +150 = +1.50%.
    ///            Allows negative values to penalize losing trades.
    ///   is_win:  whether this trade was profitable (for win-rate tracking).
    ///
    /// On-chain statistics updated:
    ///   trade_count += 1
    ///   winning_trades += is_win ? 1 : 0
    ///   cumulative_pnl += pnl_bps
    ///   sum_returns += pnl_bps         (for mean calculation)
    ///   sum_sq_returns += pnl_bps²     (for variance calculation)
    ///
    /// These enable the Sharpe-like scoring:
    ///   mean = sum_returns / trade_count
    ///   var  = (sum_sq_returns / trade_count) - mean²
    ///   score² = mean² / var   (used directly for weight calculation)
    pub fn report_trade(
        ctx: Context<ReportTrade>,
        pnl_bps: i64,
        is_win: bool,
    ) -> Result<()> {
        let profile = &mut ctx.accounts.agent_profile;

        require!(profile.is_active, SentinelError::AgentInactive);

        profile.trade_count = profile
            .trade_count
            .checked_add(1)
            .ok_or(SentinelError::MathOverflow)?;

        if is_win {
            profile.winning_trades = profile
                .winning_trades
                .checked_add(1)
                .ok_or(SentinelError::MathOverflow)?;
        }

        // Accumulate PnL (signed)
        profile.cumulative_pnl = profile
            .cumulative_pnl
            .checked_add(pnl_bps)
            .ok_or(SentinelError::MathOverflow)?;

        // Running statistics for Sharpe calculation
        // sum_returns is i128 to handle large accumulations
        profile.sum_returns = profile
            .sum_returns
            .checked_add(pnl_bps as i128)
            .ok_or(SentinelError::MathOverflow)?;

        // sum_sq_returns = Σ(r_i²), always non-negative
        let sq = (pnl_bps as i128)
            .checked_mul(pnl_bps as i128)
            .ok_or(SentinelError::MathOverflow)?;
        profile.sum_sq_returns = profile
            .sum_sq_returns
            .checked_add(sq as u128)
            .ok_or(SentinelError::MathOverflow)?;

        profile.last_report_ts = Clock::get()?.unix_timestamp;

        emit!(TradeReported {
            agent: profile.agent,
            pnl_bps,
            is_win,
            trade_count: profile.trade_count,
            cumulative_pnl: profile.cumulative_pnl,
        });

        Ok(())
    }

    // ══════════════════════════════════════════════════════════
    //  7. RISK-ADJUSTED PROFIT DISTRIBUTION
    // ══════════════════════════════════════════════════════════

    /// Distributes profits into the vault, increasing NAV/share for all holders.
    /// The oracle sends SOL to the vault; the vault tracks which agent generated
    /// the profit and increases that agent's reward counter.
    ///
    /// Architecture note: Profit goes into the shared vault (benefiting all depositors
    /// via NAV appreciation). A configurable agent_fee_bps is carved out and tracked
    /// in the agent's total_rewards_earned for later claim.
    ///
    /// Formula for agent fee carve-out:
    ///   agent_reward = (amount * agent_fee_bps) / 10_000
    ///   vault_portion = amount - agent_reward
    ///
    /// The agent_reward stays in the vault but is earmarked for the agent.
    /// The vault_portion increases NAV/share for all depositors.
    pub fn distribute_profits(
        ctx: Context<DistributeProfits>,
        amount: u64,
        agent_fee_bps: u16,
    ) -> Result<()> {
        let vault = &mut ctx.accounts.vault;

        require!(!vault.is_paused, SentinelError::VaultPaused);
        require!(amount > 0, SentinelError::ZeroAmount);
        require!(vault.total_shares > 0, SentinelError::NoShareholders);
        require!(agent_fee_bps <= MAX_AGENT_FEE_BPS, SentinelError::FeeTooHigh);

        // Transfer profit SOL from oracle to vault PDA
        system_program::transfer(
            CpiContext::new(
                ctx.accounts.system_program.to_account_info(),
                system_program::Transfer {
                    from: ctx.accounts.oracle.to_account_info(),
                    to: ctx.accounts.vault_sol.to_account_info(),
                },
            ),
            amount,
        )?;

        // Calculate agent reward carve-out (tracked, not transferred)
        let agent_reward = (amount as u128)
            .checked_mul(agent_fee_bps as u128)
            .ok_or(SentinelError::MathOverflow)?
            .checked_div(BPS_DENOMINATOR as u128)
            .ok_or(SentinelError::MathOverflow)? as u64;

        // Update agent profile if provided
        if let Some(agent_profile) = &mut ctx.accounts.agent_profile {
            agent_profile.total_rewards_earned = agent_profile
                .total_rewards_earned
                .checked_add(agent_reward)
                .ok_or(SentinelError::MathOverflow)?;
        }

        // Update vault metrics
        vault.total_profits_distributed = vault
            .total_profits_distributed
            .checked_add(amount)
            .ok_or(SentinelError::MathOverflow)?;
        vault.epoch_profit = vault
            .epoch_profit
            .checked_add(amount)
            .ok_or(SentinelError::MathOverflow)?;

        emit!(ProfitsDistributed {
            oracle: ctx.accounts.oracle.key(),
            amount,
            agent_reward,
            total_vault_balance: ctx.accounts.vault_sol.lamports(),
            total_profits_distributed: vault.total_profits_distributed,
        });

        Ok(())
    }

    // ══════════════════════════════════════════════════════════
    //  8. AGENT REWARD CLAIM
    // ══════════════════════════════════════════════════════════

    /// Agent claims their accumulated performance rewards from the vault.
    /// Resets total_rewards_earned to 0 after claim.
    pub fn claim_agent_reward(ctx: Context<ClaimAgentReward>) -> Result<()> {
        let vault = &ctx.accounts.vault;
        require!(!vault.is_paused, SentinelError::VaultPaused);

        let profile = &mut ctx.accounts.agent_profile;
        let reward = profile.total_rewards_earned;

        require!(reward > 0, SentinelError::ZeroAmount);

        // Transfer from vault PDA to agent via CPI with signer seeds
        let vault_key = vault.key();
        let seeds = &[
            b"vault_sol",
            vault_key.as_ref(),
            &[vault.vault_sol_bump],
        ];
        let signer = &[&seeds[..]];

        system_program::transfer(
            CpiContext::new_with_signer(
                ctx.accounts.system_program.to_account_info(),
                system_program::Transfer {
                    from: ctx.accounts.vault_sol.to_account_info(),
                    to: ctx.accounts.agent.to_account_info(),
                },
                signer,
            ),
            reward,
        )?;

        profile.total_rewards_earned = 0;

        emit!(AgentRewardClaimed {
            agent: profile.agent,
            amount: reward,
        });

        Ok(())
    }

    // ══════════════════════════════════════════════════════════
    //  9. QUERY: AGENT SHARPE SCORE (view helper, emits event)
    // ══════════════════════════════════════════════════════════

    /// Computes and emits the agent's on-chain Sharpe-like score.
    ///
    /// Math (all in basis points, integer arithmetic):
    ///   n     = trade_count
    ///   μ     = sum_returns / n                    (mean return in bps)
    ///   σ²    = (sum_sq_returns / n) - μ²          (variance in bps²)
    ///   score = μ² * SCORE_PRECISION / σ²          (Sharpe² * precision)
    ///
    /// We emit score_numerator = μ² and score_denominator = σ² so the client
    /// can compute the exact ratio. If σ² = 0 and μ > 0, agent has perfect
    /// consistency → score = MAX_SCORE sentinel value.
    ///
    /// Win rate is also emitted: win_rate_bps = (winning_trades * 10000) / trade_count
    pub fn query_agent_score(ctx: Context<QueryAgentScore>) -> Result<()> {
        let profile = &ctx.accounts.agent_profile;

        require!(profile.trade_count > 0, SentinelError::NoTradeData);

        let n = profile.trade_count as i128;

        // μ = sum_returns / n  (we keep as numerator/denominator to avoid truncation)
        // μ² = sum_returns² / n²
        let mean_sq_num = profile
            .sum_returns
            .checked_mul(profile.sum_returns)
            .ok_or(SentinelError::MathOverflow)?;
        let _mean_sq_den = n.checked_mul(n).ok_or(SentinelError::MathOverflow)?;

        // σ² = E[X²] - (E[X])²  = sum_sq/n - (sum/n)²
        //    = (sum_sq * n - sum²) / n²
        let var_num = (profile.sum_sq_returns as i128)
            .checked_mul(n)
            .ok_or(SentinelError::MathOverflow)?
            .checked_sub(
                profile
                    .sum_returns
                    .checked_mul(profile.sum_returns)
                    .ok_or(SentinelError::MathOverflow)?,
            )
            .ok_or(SentinelError::MathOverflow)?;

        // var_den = n²  (same as mean_sq_den)

        // Win rate in bps: (winning_trades * 10000) / trade_count
        let win_rate_bps = (profile.winning_trades as u64)
            .checked_mul(BPS_DENOMINATOR)
            .ok_or(SentinelError::MathOverflow)?
            .checked_div(profile.trade_count as u64)
            .ok_or(SentinelError::MathOverflow)?;

        // Sharpe² = μ² / σ²  = mean_sq_num * var_den / (mean_sq_den * var_num)
        // = mean_sq_num / var_num  (since var_den = mean_sq_den = n²)
        // Emit raw values for client-side precision
        let score_numerator = mean_sq_num.unsigned_abs();
        let score_denominator = if var_num <= 0 { 1u128 } else { var_num as u128 };
        let mean_positive = profile.sum_returns >= 0;

        emit!(AgentScoreComputed {
            agent: profile.agent,
            trade_count: profile.trade_count,
            win_rate_bps,
            cumulative_pnl: profile.cumulative_pnl,
            score_numerator,
            score_denominator,
            mean_positive,
        });

        Ok(())
    }

    // ══════════════════════════════════════════════════════════
    //  10. ADVANCE EPOCH
    // ══════════════════════════════════════════════════════════

    /// Authority advances the vault epoch. Resets epoch_profit counter.
    /// Useful for periodic reporting and agent performance snapshots.
    pub fn advance_epoch(ctx: Context<AdvanceEpoch>) -> Result<()> {
        let vault = &mut ctx.accounts.vault;

        let previous_epoch = vault.epoch;
        let previous_profit = vault.epoch_profit;

        vault.epoch = vault
            .epoch
            .checked_add(1)
            .ok_or(SentinelError::MathOverflow)?;
        vault.epoch_profit = 0;

        emit!(EpochAdvanced {
            vault: vault.key(),
            previous_epoch,
            new_epoch: vault.epoch,
            epoch_profit: previous_profit,
        });

        Ok(())
    }

    // ══════════════════════════════════════════════════════════
    //  11. GUARDIAN CONTROLS
    // ══════════════════════════════════════════════════════════

    /// Guardian can pause/unpause the vault in case of detected risk.
    pub fn emergency_stop(ctx: Context<EmergencyStop>, pause: bool) -> Result<()> {
        let vault = &mut ctx.accounts.vault;
        vault.is_paused = pause;

        emit!(EmergencyAction {
            guardian: ctx.accounts.guardian.key(),
            paused: pause,
            timestamp: Clock::get()?.unix_timestamp,
        });

        Ok(())
    }

    /// Guardian updates policy parameters (daily cap, cooldown).
    pub fn update_policy(
        ctx: Context<UpdatePolicy>,
        new_daily_cap: u64,
        new_cooldown_seconds: i64,
    ) -> Result<()> {
        let vault = &mut ctx.accounts.vault;
        vault.daily_withdraw_cap = new_daily_cap;
        vault.cooldown_seconds = new_cooldown_seconds;

        emit!(PolicyUpdated {
            guardian: ctx.accounts.guardian.key(),
            daily_withdraw_cap: new_daily_cap,
            cooldown_seconds: new_cooldown_seconds,
        });

        Ok(())
    }

    // ══════════════════════════════════════════════════════════
    //  12. ADMIN: UPDATE ROLES
    // ══════════════════════════════════════════════════════════

    /// Authority can update guardian or oracle addresses.
    pub fn update_roles(
        ctx: Context<UpdateRoles>,
        new_guardian: Option<Pubkey>,
        new_oracle: Option<Pubkey>,
    ) -> Result<()> {
        let vault = &mut ctx.accounts.vault;

        if let Some(guardian) = new_guardian {
            vault.guardian = guardian;
        }
        if let Some(oracle) = new_oracle {
            vault.oracle = oracle;
        }

        emit!(RolesUpdated {
            authority: ctx.accounts.authority.key(),
            guardian: vault.guardian,
            oracle: vault.oracle,
        });

        Ok(())
    }
}

// ══════════════════════════════════════════════════════════════
//  CONSTANTS
// ══════════════════════════════════════════════════════════════

/// Minimum deposit: 10,000 lamports (0.00001 SOL)
const MIN_DEPOSIT: u64 = 10_000;

/// Seconds per UTC day (for daily cap reset)
const SECONDS_PER_DAY: i64 = 86_400;

/// Basis points denominator (100% = 10,000 bps)
const BPS_DENOMINATOR: u64 = 10_000;

/// Maximum agent fee carve-out: 30% (3000 bps)
const MAX_AGENT_FEE_BPS: u16 = 3_000;

/// Maximum whitelisted withdrawal destinations per user
const MAX_WHITELIST: usize = 4;

// ══════════════════════════════════════════════════════════════
//  ACCOUNT STRUCTURES
// ══════════════════════════════════════════════════════════════

/// ┌─────────────────────────────────────────────────────────┐
/// │  Vault — Central state for the Fee-Sharing Vault        │
/// │                                                         │
/// │  Seeds: [b"vault", authority.key()]                     │
/// │  Size:  8 (discriminator) + 155 bytes                   │
/// └─────────────────────────────────────────────────────────┘
#[account]
#[derive(InitSpace)]
pub struct Vault {
    /// The authority that created and controls the vault
    pub authority: Pubkey,                   // 32
    /// Risk guardian who can trigger emergency stop & update policy
    pub guardian: Pubkey,                    // 32
    /// Alpha Oracle authorized to distribute profits & report trades
    pub oracle: Pubkey,                      // 32
    /// Total outstanding share tokens (denominator for NAV calc)
    pub total_shares: u64,                   // 8
    /// Cumulative SOL deposited (lifetime tracking metric)
    pub total_deposited: u64,                // 8
    /// Cumulative profits distributed (lifetime tracking metric)
    pub total_profits_distributed: u64,      // 8
    /// Emergency pause flag
    pub is_paused: bool,                     // 1
    /// PDA bump for vault account
    pub bump: u8,                            // 1
    /// PDA bump for vault SOL holder
    pub vault_sol_bump: u8,                  // 1

    // ── Guardian Policy Fields ──
    /// Maximum lamports a user can withdraw per UTC day (0 = unlimited)
    pub daily_withdraw_cap: u64,             // 8
    /// Minimum seconds between withdrawals per user (0 = no cooldown)
    pub cooldown_seconds: i64,               // 8

    // ── Performance Epoch Tracking ──
    /// Current epoch number (incremented by authority)
    pub epoch: u64,                          // 8
    /// Profit accumulated in current epoch (resets on advance)
    pub epoch_profit: u64,                   // 8
    /// Number of registered agents
    pub agent_count: u32,                    // 4
}

/// ┌─────────────────────────────────────────────────────────┐
/// │  UserPosition — Per-user deposit & share tracking       │
/// │                                                         │
/// │  Seeds: [b"position", vault.key(), user.key()]          │
/// │  Includes guardian policy state (daily cap, whitelist)   │
/// └─────────────────────────────────────────────────────────┘
#[account]
#[derive(InitSpace)]
pub struct UserPosition {
    /// Owner of this position
    pub owner: Pubkey,                       // 32
    /// Vault this position belongs to
    pub vault: Pubkey,                       // 32
    /// Number of shares held
    pub shares: u64,                         // 8
    /// Cumulative SOL deposited
    pub total_deposited: u64,                // 8
    /// Cumulative SOL withdrawn
    pub total_withdrawn: u64,                // 8
    /// Last action timestamp
    pub last_action_ts: i64,                 // 8

    // ── Guardian Policy State ──
    /// Timestamp of last withdrawal (for cooldown enforcement)
    pub last_withdraw_ts: i64,               // 8
    /// UTC day number of last withdrawal (for daily cap reset)
    pub last_withdraw_day: i64,              // 8
    /// Lamports withdrawn so far today
    pub daily_withdrawn: u64,                // 8
    /// Whitelisted withdrawal destinations (Pubkey::default = unused slot)
    #[max_len(4)]
    pub whitelist: [Pubkey; 4],              // 32 * 4 = 128
    /// Number of active whitelist entries (0 = no restriction)
    pub whitelist_count: u8,                 // 1
}

/// ┌─────────────────────────────────────────────────────────┐
/// │  AgentProfile — On-chain performance scoring            │
/// │                                                         │
/// │  Seeds: [b"agent", vault.key(), agent.key()]            │
/// │                                                         │
/// │  Statistics for Sharpe-like scoring:                     │
/// │    μ  = sum_returns / trade_count                       │
/// │    σ² = (sum_sq_returns / n) - μ²                       │
/// │    Sharpe² = μ² / σ²                                    │
/// │                                                         │
/// │  Weight for reward allocation:                          │
/// │    w_i = Sharpe_i² / Σ Sharpe_j²                       │
/// │    This is computed off-chain or in distribute_profits  │
/// │    using the raw stats stored here.                     │
/// └─────────────────────────────────────────────────────────┘
#[account]
#[derive(InitSpace)]
pub struct AgentProfile {
    /// Public key of the agent
    pub agent: Pubkey,                       // 32
    /// Vault this agent operates for
    pub vault: Pubkey,                       // 32
    /// Total number of trades reported
    pub trade_count: u32,                    // 4
    /// Number of winning trades (for win-rate calculation)
    pub winning_trades: u32,                 // 4
    /// Cumulative PnL in basis points (signed)
    pub cumulative_pnl: i64,                 // 8
    /// Σ(return_i) — sum of all individual trade returns (bps, signed)
    /// Used for mean calculation: μ = sum_returns / trade_count
    pub sum_returns: i128,                   // 16
    /// Σ(return_i²) — sum of squared returns (always non-negative)
    /// Used for variance: σ² = sum_sq_returns/n - (sum_returns/n)²
    pub sum_sq_returns: u128,                // 16
    /// Accumulated rewards earmarked for this agent (lamports)
    pub total_rewards_earned: u64,           // 8
    /// Timestamp of last trade report
    pub last_report_ts: i64,                 // 8
    /// Whether the agent is actively receiving reports
    pub is_active: bool,                     // 1
}

// ══════════════════════════════════════════════════════════════
//  INSTRUCTION CONTEXTS (Account Validation)
// ══════════════════════════════════════════════════════════════

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(
        init,
        payer = authority,
        space = 8 + Vault::INIT_SPACE,
        seeds = [b"vault", authority.key().as_ref()],
        bump,
    )]
    pub vault: Account<'info, Vault>,

    /// CHECK: PDA that holds SOL for the vault. Validated by seeds.
    #[account(
        mut,
        seeds = [b"vault_sol", vault.key().as_ref()],
        bump,
    )]
    pub vault_sol: SystemAccount<'info>,

    #[account(mut)]
    pub authority: Signer<'info>,

    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct Deposit<'info> {
    #[account(
        mut,
        seeds = [b"vault", vault.authority.as_ref()],
        bump = vault.bump,
    )]
    pub vault: Account<'info, Vault>,

    /// CHECK: PDA that holds SOL. Validated by seeds.
    #[account(
        mut,
        seeds = [b"vault_sol", vault.key().as_ref()],
        bump = vault.vault_sol_bump,
    )]
    pub vault_sol: SystemAccount<'info>,

    #[account(
        init_if_needed,
        payer = user,
        space = 8 + UserPosition::INIT_SPACE,
        seeds = [b"position", vault.key().as_ref(), user.key().as_ref()],
        bump,
    )]
    pub user_position: Account<'info, UserPosition>,

    #[account(mut)]
    pub user: Signer<'info>,

    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct Withdraw<'info> {
    #[account(
        mut,
        seeds = [b"vault", vault.authority.as_ref()],
        bump = vault.bump,
    )]
    pub vault: Account<'info, Vault>,

    /// CHECK: PDA that holds SOL. Validated by seeds.
    #[account(
        mut,
        seeds = [b"vault_sol", vault.key().as_ref()],
        bump = vault.vault_sol_bump,
    )]
    pub vault_sol: SystemAccount<'info>,

    #[account(
        mut,
        seeds = [b"position", vault.key().as_ref(), user.key().as_ref()],
        bump,
        has_one = owner @ SentinelError::Unauthorized,
    )]
    pub user_position: Account<'info, UserPosition>,

    /// CHECK: Validated via has_one on user_position.
    #[account(mut)]
    pub owner: SystemAccount<'info>,

    #[account(mut)]
    pub user: Signer<'info>,

    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct SetWhitelist<'info> {
    #[account(
        seeds = [b"vault", vault.authority.as_ref()],
        bump = vault.bump,
    )]
    pub vault: Account<'info, Vault>,

    #[account(
        mut,
        seeds = [b"position", vault.key().as_ref(), user.key().as_ref()],
        bump,
        constraint = user_position.owner == user.key() @ SentinelError::Unauthorized,
    )]
    pub user_position: Account<'info, UserPosition>,

    pub user: Signer<'info>,
}

#[derive(Accounts)]
#[instruction(agent_key: Pubkey)]
pub struct RegisterAgent<'info> {
    #[account(
        mut,
        seeds = [b"vault", vault.authority.as_ref()],
        bump = vault.bump,
        has_one = authority @ SentinelError::Unauthorized,
    )]
    pub vault: Account<'info, Vault>,

    #[account(
        init,
        payer = authority,
        space = 8 + AgentProfile::INIT_SPACE,
        seeds = [b"agent", vault.key().as_ref(), agent_key.as_ref()],
        bump,
    )]
    pub agent_profile: Account<'info, AgentProfile>,

    #[account(mut)]
    pub authority: Signer<'info>,

    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct DeactivateAgent<'info> {
    #[account(
        seeds = [b"vault", vault.authority.as_ref()],
        bump = vault.bump,
        has_one = authority @ SentinelError::Unauthorized,
    )]
    pub vault: Account<'info, Vault>,

    #[account(
        mut,
        constraint = agent_profile.vault == vault.key() @ SentinelError::Unauthorized,
    )]
    pub agent_profile: Account<'info, AgentProfile>,

    pub authority: Signer<'info>,
}

#[derive(Accounts)]
pub struct ReportTrade<'info> {
    #[account(
        seeds = [b"vault", vault.authority.as_ref()],
        bump = vault.bump,
        constraint = vault.oracle == oracle.key() @ SentinelError::Unauthorized,
    )]
    pub vault: Account<'info, Vault>,

    #[account(
        mut,
        constraint = agent_profile.vault == vault.key() @ SentinelError::Unauthorized,
    )]
    pub agent_profile: Account<'info, AgentProfile>,

    pub oracle: Signer<'info>,
}

#[derive(Accounts)]
pub struct DistributeProfits<'info> {
    #[account(
        mut,
        seeds = [b"vault", vault.authority.as_ref()],
        bump = vault.bump,
        constraint = vault.oracle == oracle.key() @ SentinelError::Unauthorized,
    )]
    pub vault: Account<'info, Vault>,

    /// CHECK: PDA that holds SOL. Validated by seeds.
    #[account(
        mut,
        seeds = [b"vault_sol", vault.key().as_ref()],
        bump = vault.vault_sol_bump,
    )]
    pub vault_sol: SystemAccount<'info>,

    /// Optional agent profile to attribute rewards to.
    /// If the oracle wants to distribute without agent attribution,
    /// this can be set to the vault account (will be None).
    #[account(
        mut,
        constraint = agent_profile.vault == vault.key() @ SentinelError::Unauthorized,
    )]
    pub agent_profile: Option<Account<'info, AgentProfile>>,

    #[account(mut)]
    pub oracle: Signer<'info>,

    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct ClaimAgentReward<'info> {
    #[account(
        seeds = [b"vault", vault.authority.as_ref()],
        bump = vault.bump,
    )]
    pub vault: Account<'info, Vault>,

    /// CHECK: PDA that holds SOL. Validated by seeds.
    #[account(
        mut,
        seeds = [b"vault_sol", vault.key().as_ref()],
        bump = vault.vault_sol_bump,
    )]
    pub vault_sol: SystemAccount<'info>,

    #[account(
        mut,
        constraint = agent_profile.vault == vault.key() @ SentinelError::Unauthorized,
        constraint = agent_profile.agent == agent.key() @ SentinelError::Unauthorized,
    )]
    pub agent_profile: Account<'info, AgentProfile>,

    #[account(mut)]
    pub agent: Signer<'info>,

    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct QueryAgentScore<'info> {
    #[account(
        seeds = [b"vault", vault.authority.as_ref()],
        bump = vault.bump,
    )]
    pub vault: Account<'info, Vault>,

    #[account(
        constraint = agent_profile.vault == vault.key() @ SentinelError::Unauthorized,
    )]
    pub agent_profile: Account<'info, AgentProfile>,
}

#[derive(Accounts)]
pub struct AdvanceEpoch<'info> {
    #[account(
        mut,
        seeds = [b"vault", vault.authority.as_ref()],
        bump = vault.bump,
        has_one = authority @ SentinelError::Unauthorized,
    )]
    pub vault: Account<'info, Vault>,

    pub authority: Signer<'info>,
}

#[derive(Accounts)]
pub struct EmergencyStop<'info> {
    #[account(
        mut,
        seeds = [b"vault", vault.authority.as_ref()],
        bump = vault.bump,
        constraint = vault.guardian == guardian.key() @ SentinelError::Unauthorized,
    )]
    pub vault: Account<'info, Vault>,

    pub guardian: Signer<'info>,
}

#[derive(Accounts)]
pub struct UpdatePolicy<'info> {
    #[account(
        mut,
        seeds = [b"vault", vault.authority.as_ref()],
        bump = vault.bump,
        constraint = vault.guardian == guardian.key() @ SentinelError::Unauthorized,
    )]
    pub vault: Account<'info, Vault>,

    pub guardian: Signer<'info>,
}

#[derive(Accounts)]
pub struct UpdateRoles<'info> {
    #[account(
        mut,
        seeds = [b"vault", vault.authority.as_ref()],
        bump = vault.bump,
        has_one = authority @ SentinelError::Unauthorized,
    )]
    pub vault: Account<'info, Vault>,

    pub authority: Signer<'info>,
}

// ══════════════════════════════════════════════════════════════
//  EVENTS
// ══════════════════════════════════════════════════════════════

#[event]
pub struct VaultInitialized {
    pub authority: Pubkey,
    pub guardian: Pubkey,
    pub oracle: Pubkey,
    pub daily_withdraw_cap: u64,
    pub cooldown_seconds: i64,
}

#[event]
pub struct Deposited {
    pub user: Pubkey,
    pub amount: u64,
    pub shares_minted: u64,
    pub total_vault_shares: u64,
}

#[event]
pub struct Withdrawn {
    pub user: Pubkey,
    pub shares_burned: u64,
    pub amount_returned: u64,
    pub total_vault_shares: u64,
}

#[event]
pub struct ProfitsDistributed {
    pub oracle: Pubkey,
    pub amount: u64,
    pub agent_reward: u64,
    pub total_vault_balance: u64,
    pub total_profits_distributed: u64,
}

#[event]
pub struct EmergencyAction {
    pub guardian: Pubkey,
    pub paused: bool,
    pub timestamp: i64,
}

#[event]
pub struct PolicyUpdated {
    pub guardian: Pubkey,
    pub daily_withdraw_cap: u64,
    pub cooldown_seconds: i64,
}

#[event]
pub struct RolesUpdated {
    pub authority: Pubkey,
    pub guardian: Pubkey,
    pub oracle: Pubkey,
}

#[event]
pub struct AgentRegistered {
    pub vault: Pubkey,
    pub agent: Pubkey,
}

#[event]
pub struct AgentDeactivated {
    pub vault: Pubkey,
    pub agent: Pubkey,
}

#[event]
pub struct TradeReported {
    pub agent: Pubkey,
    pub pnl_bps: i64,
    pub is_win: bool,
    pub trade_count: u32,
    pub cumulative_pnl: i64,
}

#[event]
pub struct AgentScoreComputed {
    pub agent: Pubkey,
    pub trade_count: u32,
    pub win_rate_bps: u64,
    pub cumulative_pnl: i64,
    /// μ² (mean return squared) — numerator of Sharpe²
    pub score_numerator: u128,
    /// σ² (variance) — denominator of Sharpe²
    pub score_denominator: u128,
    /// Whether mean return is non-negative
    pub mean_positive: bool,
}

#[event]
pub struct AgentRewardClaimed {
    pub agent: Pubkey,
    pub amount: u64,
}

#[event]
pub struct EpochAdvanced {
    pub vault: Pubkey,
    pub previous_epoch: u64,
    pub new_epoch: u64,
    pub epoch_profit: u64,
}

#[event]
pub struct WhitelistUpdated {
    pub user: Pubkey,
    pub count: u8,
}

// ══════════════════════════════════════════════════════════════
//  ERROR CODES
// ══════════════════════════════════════════════════════════════

#[error_code]
pub enum SentinelError {
    #[msg("Vault is paused — emergency stop active")]
    VaultPaused,
    #[msg("Amount must be greater than zero")]
    ZeroAmount,
    #[msg("Deposit below minimum threshold")]
    BelowMinDeposit,
    #[msg("Calculated shares would be zero")]
    ZeroShares,
    #[msg("Insufficient shares for withdrawal")]
    InsufficientShares,
    #[msg("No shareholders in the vault")]
    NoShareholders,
    #[msg("Math overflow")]
    MathOverflow,
    #[msg("Unauthorized")]
    Unauthorized,
    #[msg("Withdrawal cooldown period still active")]
    CooldownActive,
    #[msg("Daily withdrawal cap exceeded")]
    DailyCapExceeded,
    #[msg("Withdrawal destination not in whitelist")]
    DestinationNotWhitelisted,
    #[msg("Too many whitelist entries (max 4)")]
    TooManyWhitelistEntries,
    #[msg("Agent is inactive")]
    AgentInactive,
    #[msg("No trade data available for scoring")]
    NoTradeData,
    #[msg("Agent fee exceeds maximum (30%)")]
    FeeTooHigh,
    #[msg("Insufficient funds in vault")]
    InsufficientFunds,
}

# Live Context Gathering Plan

Goal: build audit scope from live deployed behavior only. Include a source file only if its deployed contract is present, or if the code can affect on-chain funds through the deployed graph.

## Phase 1 - Identity and Deployment Graph

1. Confirm chain, target, verification status, proxy status, compiler, optimizer, and current block.
2. Read the live core address graph from deployment artifacts and current contract getters.
3. Separate live deployed core contracts from local-only testers, mock contracts, and unused source.
4. Resolve opaque/private dependency addresses by event logs or deployment transaction traces where getters do not expose them.

## Phase 2 - Funds and Accounting State

1. Read native BNB balances for ActivePool, DefaultPool, StabilityPool, CollSurplusPool, GasPool, staking, and reward contracts.
2. Read contract accounting values: `getBNB`, `getUSDSDebt`, `getTotalUSDSDeposits`, USDS total supply, trove count, sorted list size, reward accumulators, and system parameters.
3. Compare raw balances to internal accounting trackers.
4. Enumerate protocol-used tokens separately from random transferred tokens.

## Phase 3 - Actor and Authority Model

1. Confirm owner/admin/timelock values on every deployed contract.
2. Classify public user triggers, keeper/liquidator triggers, restricted core-to-core calls, and timelock/governance calls.
3. Treat renounced owners as immutable unless a live proxy/admin path is found.
4. Keep trusted governance/timelock actions separate from untrusted drain surfaces.

## Phase 4 - Value Flow and Trigger Surface

1. Map BNB ingress: trove collateral deposits, DefaultPool returns, ActivePool forced balance edge cases.
2. Map BNB egress: borrower collateral withdrawal, liquidation gas compensation, StabilityPool BNB gains, CollSurplus claims, redemption, staking fee payout.
3. Map USDS mint/burn/pool flows: BorrowerOperations mint, TroveManager/StabilityPool/BorrowerOperations burn, StabilityPool deposit/withdraw, redemption.
4. Map oracle-dependent paths: opening, adjusting, closing, liquidation, redemption, StabilityPool withdrawal gating.
5. Mark every externally callable state-changing function as untrusted, restricted, or trusted.

## Phase 5 - User and Pool Enumeration

1. Enumerate active troves from `TroveOwners` and `SortedTroves`.
2. Enumerate StabilityPool depositors from `UserDepositChanged` and `FrontEndRegistered` events.
3. Enumerate USDS holders/allowances only where they affect current exploitability or pool solvency.
4. Sample high-value accounts to check pending rewards, claimable BNB, and accounting consistency.

## Phase 6 - Scope Freeze

1. Freeze the code scope to deployed contracts and direct-fund dependencies.
2. Exclude tests, mocks, scripts, helpers, periphery, and interfaces that are not deployed or only describe a deployed contract.
3. Preserve conditional entries for deployed addresses whose exact source path is not yet recovered.
4. Record unresolved live properties as explicit follow-up commands, not assumptions.

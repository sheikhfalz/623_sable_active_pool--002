# Scope

This scope is based on the live Sable deployment around `ActivePool` on BNB Smart Chain. It is not a broad repository scope.

## Primary In-Scope Files

These files are in scope because their deployed contracts are present in the live graph or directly move/account for user funds.

- `src/ActivePool.sol` - primary target; holds active trove BNB collateral and active USDS debt accounting.
- `src/BorrowerOperations.sol` - user front door for opening, adjusting, closing troves, collateral movement, USDS mint/burn, and CollSurplus claims.
- `src/TroveManager.sol` - liquidation, redemption, trove debt/collateral accounting, reward redistribution, and system snapshots.
- `src/StabilityPool.sol` - USDS deposits, BNB gains, liquidation offsets, SABLE rewards, depositor withdrawals.
- `src/DefaultPool.sol` - redistributed liquidation collateral/debt before pending rewards are applied back to active troves.
- `src/CollSurplusPool.sol` - stores and pays surplus BNB after redemption/liquidation paths.
- `src/USDSToken.sol` - live stablecoin mint/burn/transfer/allowance/permit behavior tied to debt and StabilityPool flows.
- `src/PriceFeed.sol` - Pyth/Chainlink price selection and status transitions used by borrow, withdraw, liquidate, redeem, and StabilityPool withdrawal checks.
- `src/SystemState.sol` - live MCR/CCR/min debt/gas compensation/fee-floor parameters; timelock-controlled and directly affects solvency gates.
- `src/SortedTroves.sol` - ordered active-trove list used by liquidation and redemption traversal.
- `src/OracleRateCalculation.sol` - oracle-rate input used for fee calculations.
- `src/TroveHelper.sol` - liquidation helper used by `TroveManager` for capped recovery-mode offsets.
- `src/GasPool.sol` - live gas-compensation holder recovered from `BorrowerOperations` storage.
- `src/TimeLock.sol` - live `SystemState` timelock address recovered from storage; can update core risk parameters.
- `src/SABLE/SableStakingV2.sol` - receives borrowing/redemption fees and can receive BNB/USDS/SABLE rewards from core paths.
- `src/SABLE/CommunityIssuance.sol` - issues SABLE to StabilityPool depositors/front ends and affects reward accounting.
- `src/SABLE/SABLEToken.sol` - reward/staking token with allowance/permit surface and staking/rewarder integrations.

## Interface Scope

Interfaces are in scope only as ABI/behavior references for the deployed contracts above:

- `src/Interfaces/IActivePool.sol`
- `src/Interfaces/IBorrowerOperations.sol`
- `src/Interfaces/ITroveManager.sol`
- `src/Interfaces/IStabilityPool.sol`
- `src/Interfaces/IDefaultPool.sol`
- `src/Interfaces/ICollSurplusPool.sol`
- `src/Interfaces/IUSDSToken.sol`
- `src/Interfaces/IPriceFeed.sol`
- `src/Interfaces/ISystemState.sol`
- `src/Interfaces/ISortedTroves.sol`
- `src/Interfaces/IOracleRateCalculation.sol`
- `src/Interfaces/ITroveHelper.sol`
- `src/Interfaces/ISableStakingV2.sol`
- `src/Interfaces/ICommunityIssuance.sol`
- `src/Interfaces/ISABLEToken.sol`

## Conditional Scope

These are conditionally in scope if live event/log recovery confirms the corresponding deployed address is active in this deployment:

- verified external source for SableRewarder at `0x23d253F1Ab38a1Ec8c05103232B4eFaFB6A1bdEb` - live rewarder address recovered from `SableStakingV2`, but no local `src/SableRewarder.sol` exists in this checkout.
- `src/BNBTransferScript.sol` and `src/Proxy/*.sol` - only in scope if any deployed wrapper/proxy address currently has custody or delegated user control; otherwise scripts are out.

## Out of Scope

These files are excluded for this run unless later proven deployed with direct custody or control over the live system:

- `src/TestContracts/**`
- `test/**`
- `lib/**`
- `out/**`
- `cache/**`
- local mock oracle/token contracts
- source mapping artifacts and BscScan HTML captures except as evidence

Repo-root `live_context.json` is not a Solidity source-scope item; it is the canonical live-context artifact for this run.

## Scope Rule

If a file cannot move BNB, mint/burn/transfer USDS/SABLE, change collateral/debt/reward accounting, change price/solvency gates, or authorize a deployed contract that can do those things, it is excluded from this live-context run.

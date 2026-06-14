# Live Context

## Identity

- Protocol slice: Sable Finance Active Pool and connected Liquity-style core system.
- Chain: BNB Smart Chain mainnet (`56`).
- Primary target: `ActivePool`.
- Target address: `0x0cCb12C9fB1e1252E60d29aC5c4fDc0640edD72C`.
- Verification: BscScan verified source per `source-artifacts/deployment-context.json`.
- Proxy: `false` per local deployment context.
- Compiler: `v0.6.11+commit.5ef660b1`, optimizer enabled, runs `1`.
- Live refresh block: `102807300`.
- Earlier local snapshot timestamp: `2026-04-14 23:49:34 PDT`.

## Deployed Address Graph

| Role | Address | Scope Status |
| --- | --- | --- |
| ActivePool | `0x0cCb12C9fB1e1252E60d29aC5c4fDc0640edD72C` | primary |
| BorrowerOperations | `0xa49BEC2146fBeeA7314cdbe0Fd222419B0c0602f` | primary |
| TroveManager | `0xEC035081376ce975Ba9EAF28dFeC7c7A4c483B85` | primary |
| StabilityPool | `0x598913568093AB9F3d549236EB98388271073F18` | primary |
| DefaultPool | `0x654Ed83ab231550001Fc1d2281B78fcD84121088` | primary |
| USDSToken | `0x0c6Ed1E73BA73B8441868538E210ebD5DD240FA0` | primary |
| PriceFeed | `0xA5220fd82C098b7f1C711e2F1C1d599ccfbCDCB3` | primary |
| OracleRateCalculation | `0x76Dcd40843C1dE96839bf83790257A36011E6632` | primary |
| SystemState | `0x698ad77E62679c8E6aCfAfea03547C38fC5Ec0aD` | primary |
| SortedTroves | `0x97C131C309A04BFa1AAE82856d64b696b89dC87C` | primary |
| SableStakingV2 | `0xFbc81aEB7e5c11d4A60a0690Db9F36F93E25B16C` | primary |
| GasPool | `0xE9bc9aDBdf67343b5A66D73Cf2E521bb3f088D01` | primary |
| CollSurplusPool | `0xBE40060aEf1A2aCb4425823c82978F976fD93cd0` | primary |
| TimeLock | `0x638675b7C2e056917567571307C6f6A7D69A258A` | primary |
| SABLEToken | `0x1eE098cBaF1f846d5Df1993f7e2d10AFb35A878d` | primary |
| TroveHelper | `0xd1BF4d208028CBFe65c6b4D68C12e68F5F3D80F8` | primary |
| CommunityIssuance | `0x7fd517b06b898F1a6081E0891265516F83Dc9C9E` | primary |
| SableLPToken | `0xa0D4e270D9EB4E41f7aB02337c21692D7eECCCB0` | primary asset |
| SableRewarder | `0x23d253F1Ab38a1Ec8c05103232B4eFaFB6A1bdEb` | primary |
| Chainlink BNB/USD aggregator | `0x0567F2323251f0Aab15c8dFb1967E4e8A7D42aeE` | oracle integration |
| Pyth wrapper | `0x4D7E825f80bDf85e913E0DD2A2D54927e9dE1594` | oracle integration |

## Current Live Values

| Value | Current Read |
| --- | ---: |
| ActivePool raw BNB balance | `874414848004364383519` wei |
| ActivePool recorded BNB | `874414848004364383519` wei |
| ActivePool recorded USDS debt | `92032333642572499463529` |
| DefaultPool recorded BNB | `0` |
| DefaultPool recorded USDS debt | `0` |
| StabilityPool recorded BNB | `87196` wei |
| StabilityPool total USDS deposits | `6579363784326119862850` |
| USDS total supply | `92032333642572499463529` |
| Trove owners count | `1` |
| SortedTroves size | `1` |
| PriceFeed last good price | `698869481810000000000` |
| PriceFeed status | `0` (`pythWorking`) |
| PriceFeed age | `120` seconds |
| GasPool USDS balance | `10000000000000000000` |
| SableStakingV2 BNB balance | `301290650075643435` wei |
| SableStakingV2 USDS balance | `654574197951713185` |
| SableStakingV2 LP balance | `20935597236192701456120` |
| CommunityIssuance SABLE balance | `5409915403529186761416` |
| SABLE LP reserves | `12176323796385788711697862 SABLE`, `48826407685591615235 WBNB` |

Observation: ActivePool raw BNB equals recorded BNB at the refreshed block. DefaultPool is empty. StabilityPool has nonzero USDS deposits and dust-level recorded BNB.

## Current System Parameters

| Parameter | Value |
| --- | ---: |
| USDS gas compensation | `10000000000000000000` (`10e18`) |
| Minimum net debt | `90000000000000000000` (`90e18`) |
| MCR | `1100000000000000000` (`110%`) |
| CCR | `1500000000000000000` (`150%`) |
| Borrowing fee floor | `500000000000000` (`0.05%`) |
| Redemption fee floor | `500000000000000` (`0.05%`) |

## Authority

Current `owner()` values refreshed at block `102807300`:

| Contract | Owner |
| --- | --- |
| ActivePool | `0x0000000000000000000000000000000000000000` |
| BorrowerOperations | `0x0000000000000000000000000000000000000000` |
| TroveManager | `0x0000000000000000000000000000000000000000` |
| StabilityPool | `0x0000000000000000000000000000000000000000` |
| DefaultPool | `0x0000000000000000000000000000000000000000` |

Interpretation: core setup ownership is renounced for these contracts. SystemState still has timelock-controlled setters; the live timelock address must be recovered from storage or logs because it is private.

## Value Flow Model

- BNB enters ActivePool through `BorrowerOperations` trove collateral deposits and DefaultPool pending-reward movement.
- BNB leaves ActivePool through borrower collateral withdrawals, trove closure, liquidation gas compensation, StabilityPool offset collateral, CollSurplus accounting, and redemptions.
- DefaultPool temporarily holds redistributed liquidation BNB and debt before pending rewards are applied to active troves.
- StabilityPool holds USDS deposits, burns USDS during liquidation offsets, receives BNB from ActivePool, and pays BNB/SABLE gains to depositors or moves BNB gain into a trove.
- USDSToken supply is minted by BorrowerOperations and burned by BorrowerOperations, TroveManager, or StabilityPool according to debt movement.
- PriceFeed gates open/adjust/close/liquidate/redeem/withdraw paths through Pyth/Chainlink status and last good price.
- SystemState parameters define collateral ratio thresholds, minimum debt, gas compensation, and fee floors.

## Trigger Surface Summary

The scoped files contain `142` public/external/receive surfaces including getters. High-priority state-changing triggers are:

- Borrower user paths: `openTrove`, `addColl`, `withdrawColl`, `withdrawUSDS`, `repayUSDS`, `adjustTrove`, `closeTrove`, `claimCollateral`.
- StabilityPool user paths: `provideToSP`, `withdrawFromSP`, `withdrawBNBGainToTrove`, `registerFrontEnd`.
- TroveManager public liquidation/redemption paths: `liquidate`, `liquidateTroves`, `batchLiquidateTroves`, `redeemCollateral`.
- Token paths: `USDSToken.transfer`, `approve`, `transferFrom`, `increaseAllowance`, `decreaseAllowance`, `permit`; same allowance/permit class for `SABLEToken`.
- Restricted core paths: ActivePool/DefaultPool/StabilityPool send, debt, offset, mint, burn, and pool-transfer functions.
- Trusted or conditional paths: SystemState timelock setters and setup-only owner functions that have renounced owners on current core contracts.

## Core Live Invariants

| Invariant | Current Status |
| --- | --- |
| `ActivePool.rawBalance == ActivePool.getBNB()` | pass at block `102807300` |
| `DefaultPool.getBNB() == 0 && DefaultPool.getUSDSDebt() == 0` | pass at block `102807300` |
| `USDS.totalSupply == ActivePool.USDSDebt + DefaultPool.USDSDebt` | pass for current reads |
| `SortedTroves.getSize() == TroveManager.getTroveOwnersCount()` | pass for current reads (`1 == 1`) |
| Core owner setup cannot be re-run by normal owner | pass for checked core contracts (`owner = 0`) |
| StabilityPool actual USDS token balance equals `totalUSDSDeposits` | pass: `6579363784326119862850` |
| CollSurplusPool recorded BNB equals raw balance | pass: raw BNB is `0`; no recorded surplus balance observed in native sweep |
| GasPool USDS balance equals one current gas compensation unit | pass: `10000000000000000000` |
| SableStakingV2 LP token balance equals `totalSableLPStaked` | pass: `20935597236192701456120` |
| PriceFeed live oracle integrations are decoded | pass: Chainlink `0x0567...2aeE`, Pyth wrapper `0x4D7...1594`, feed id `0x2f9586...01c4f` |

## Weird or Audit-Relevant Values

- Only `1` live trove and `1` sorted trove are currently active. This makes liquidation/redemption behavior highly sensitive to last-trove rules and empty-list boundaries.
- ActivePool has `874.414848004364383519 BNB` with no raw/accounting mismatch at refresh.
- StabilityPool has `6,579.363784326119862850 USDS` deposits and only `87196` wei recorded BNB, so depositor BNB-gain paths should be tested around dust and zero-gain branches.
- `PriceFeed.status = 0` (`pythWorking`) and `age = 120`, but current Pyth update requirements for state-changing calls still matter because user-facing calls pass `bytes[] priceFeedUpdateData`.
- Core pool owners are zero. SystemState timelock is decoded as `0x638675b7C2e056917567571307C6f6A7D69A258A`; any risk-parameter mutation review should start there.
- Existing repo-local confirmed issue: `USDSToken.approve` preserves the non-zero-to-non-zero allowance race shape.

## Unresolved Live Properties

1. Enumerate StabilityPool depositors and front ends from events.
2. Enumerate arbitrary/spam BEP20 token balances via BscScan/Covalent-style token holdings API; raw RPC cannot discover unknown token contracts for an address.
3. Verify SableRewarder source/ABI and reward-token behavior.
4. Check external oracle freshness directly on Chainlink and Pyth integration contracts, not only through stored `PriceFeed` values.
5. Read TimeLock queue/owner/admin state from verified ABI/source.

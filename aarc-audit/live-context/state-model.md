# State Model and On-Chain Behavior

## Live System Shape

Sable is deployed as a Liquity-style BNB-collateralized debt system:

1. Borrowers deposit native BNB into ActivePool through BorrowerOperations.
2. BorrowerOperations updates TroveManager trove structs and mints USDS debt.
3. TroveManager manages liquidations, redemptions, reward redistribution, and active trove ordering through SortedTroves.
4. StabilityPool receives USDS deposits, offsets liquidated debt, burns USDS, receives BNB from ActivePool, and pays BNB/SABLE gains.
5. DefaultPool temporarily holds redistributed liquidation debt/collateral until pending rewards are applied back to troves.
6. CollSurplusPool holds redemption/liquidation surplus BNB claimable by borrowers.
7. SystemState supplies live solvency constants and is controlled by TimeLock.
8. PriceFeed supplies BNB/USD price through Pyth primary and Chainlink fallback.
9. SableStakingV2 accepts SABLE_LP and distributes BNB/USDS/SABLE fee gains.

## Structs and Storage Behavior

### BorrowerOperations

Primary live behavior: borrower-facing trove changes.

Important structs:

- `LocalVariables_openTrove`: price, fee, debt, collateral ratio, stake, and owner-array index during open.
- `LocalVariables_adjustTrove`: old/new collateral/debt/ICR/TCR plus fee and stake during adjustment.
- `AdjustTroveParam`: user-supplied collateral withdrawal, USDS change, debt direction, hints, max fee.
- `ContractsCache`: cached TroveManager, ActivePool, USDSToken references.
- `MoveTokensAndBNBFromAdjustmentParam`: value movement bundle after trove state update.

Behavior notes:

- `openTrove` fetches price, checks recovery mode, computes composite debt, inserts into SortedTroves, moves BNB to ActivePool, mints USDS to borrower, and mints gas compensation to GasPool.
- `adjustTrove` applies pending rewards before changing debt/collateral and enforces mode-specific ICR/TCR constraints.
- `closeTrove` burns user USDS and GasPool compensation, closes TroveManager state, then sends collateral from ActivePool.
- `claimCollateral` routes to CollSurplusPool.

### TroveManager

Primary live behavior: trove registry, liquidation, redemption, reward redistribution.

Important structs:

- `Trove`: `debt`, `coll`, `stake`, `status`, `arrayIndex`.
- `RewardSnapshot`: per-trove `BNB` and `USDSDebt` snapshot.
- `LiquidationValues`: full per-trove liquidation accounting bundle.
- `LiquidationTotals`: aggregate sequence/batch liquidation accounting.
- `RedemptionTotals` and `SingleRedemptionValues`: redemption traversal accounting.
- `ContractsCache`: cached pools/tokens/sorted list/surplus addresses.

Live values:

- Active trove owner: `0x64638Adb1e882678ec8f6F6AacAe648828cc7893`.
- Trove debt: `92032333642572499463529`.
- Trove collateral: `874414848004364383519`.
- Trove stake: `874414848004364383519`.
- Pending BNB reward: `0`.
- Pending USDS debt reward: `0`.
- ICR at stored `lastGoodPrice`: `6640077758813836515`.
- `TroveOwners.length == SortedTroves.getSize() == 1`.

Behavior notes:

- Liquidation can only proceed if there is more than one relevant trove for some recovery-mode branches; the current one-trove state is a critical live boundary.
- Redemptions traverse SortedTroves and can partially redeem, update debt/collateral, and move BNB fees/gains.
- `baseRate`, `lastFeeOperationTime`, redistribution errors, and snapshots govern fee and reward history.

### StabilityPool

Primary live behavior: pooled USDS deposits, liquidation offsets, BNB/SABLE gain accounting.

Important structs:

- `Deposit`: initial USDS value and front-end tag.
- `Snapshots`: `S`, `P`, `G`, `scale`, `epoch`.
- `FrontEnd`: kickback rate and registration flag.

Live values:

- `totalUSDSDeposits`: `6579363784326119862850`.
- USDS token balance: `6579363784326119862850`.
- recorded BNB: `87196`.
- `P`: `772918228237040811`.
- `currentScale`: `0`.
- `currentEpoch`: `0`.
- `lastSABLEError`: `1432410479054684555332`.

Behavior notes:

- Deposits are compounded by `P`; BNB gains are tracked with `S`; SABLE gains are tracked with `G`.
- `offset` is restricted to TroveManager and atomically decreases ActivePool USDS debt, burns StabilityPool USDS, sends BNB from ActivePool, and updates reward sums/products.
- Withdrawals of USDS are blocked while undercollateralized troves exist.

### ActivePool, DefaultPool, CollSurplusPool, GasPool

Primary live behavior: custody and accounting pools.

- ActivePool records active collateral and debt. Current raw BNB equals recorded BNB.
- DefaultPool records redistributed pending liquidation debt/collateral. Current recorded BNB and debt are zero.
- CollSurplusPool records surplus BNB by account and pays via `claimColl`; current native balance is zero.
- GasPool holds current gas compensation. Current USDS balance is exactly `10000000000000000000`.

### USDSToken and SABLEToken

Primary live behavior: ERC20-compatible token accounting plus permit.

- USDS is minted/burned only through core-restricted functions.
- USDS and SABLE both expose `approve`, `transferFrom`, `increaseAllowance`, `decreaseAllowance`, and `permit`.
- Direct token transfers are blocked to some core contracts to reduce accidental loss, but pool movement functions bypass through core-only paths.

### PriceFeed and OracleRateCalculation

Primary live behavior: price source selection and oracle-rate fee input.

Live values:

- Chainlink aggregator: `0x0567F2323251f0Aab15c8dFb1967E4e8A7D42aeE`.
- Pyth wrapper: `0x4D7E825f80bDf85e913E0DD2A2D54927e9dE1594`.
- Pyth feed id: `0x2f95862b045670cd22bee3114c39763a4a08beeb663b145d283c31d7d1101c4f`.
- `status`: `0` (`pythWorking`).
- `lastGoodPrice`: `698869481810000000000`.
- `age`: `120`.

Behavior notes:

- `fetchPrice` is restricted to core contracts or self.
- Pyth is primary; Chainlink is fallback under broken/frozen/deviation cases.
- OracleRateCalculation caps oracle-rate percentage at `0.25%`.

### SableStakingV2 and CommunityIssuance

Primary live behavior: staking LP and reward distribution.

Live values:

- SABLE_LP token: `0xa0D4e270D9EB4E41f7aB02337c21692D7eECCCB0`.
- Rewarder: `0x23d253F1Ab38a1Ec8c05103232B4eFaFB6A1bdEb`.
- `totalSableLPStaked`: `20935597236192701456120`.
- SABLE_LP balance: `20935597236192701456120`.
- `F_BNB`: `83664420796176`.
- `F_USDS`: `1469844740846061710270`.
- `F_SABLE`: `0`.
- CommunityIssuance SABLE balance: `5409915403529186761416`.
- `totalSABLEIssued`: `827119683802499810000000`.
- `lastIssuanceTime`: `1727614847`.
- `latestRewardPerSec`: `5000000000000000`.

Behavior notes:

- Stakers deposit SABLE_LP; pending gains are computed from snapshots against `F_BNB`, `F_USDS`, and `F_SABLE`.
- BorrowerOperations/TroveManager can increase staking fee sums through core fee paths.
- CommunityIssuance issues SABLE to StabilityPool reward accounting.

## High-Value Live Boundaries

- One-trove system: liquidation, redemption, and withdrawal conditions must be tested against last-trove logic.
- ActivePool has real BNB and exact raw/accounted match.
- StabilityPool has real USDS deposits and no USDS/accounting mismatch.
- GasPool has exactly one gas compensation unit.
- SableStaking has meaningful BNB, USDS, and LP custody.
- TimeLock is the live mutable-parameter authority for SystemState.
- Unknown token dust requires an explorer-index pass; known protocol token balances are covered.

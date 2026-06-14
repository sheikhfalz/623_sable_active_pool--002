# Tokens

## Native BNB

Role: collateral asset and fee/gain payout asset.

Live custody:

- ActivePool holds active trove collateral: `874414848004364383519` wei.
- StabilityPool has dust BNB from liquidation accounting: `87196` wei.
- SableStakingV2 has fee/gain BNB: `301290650075643435` wei.
- PriceFeed has `9999999999999467` wei, likely for Pyth update fees.

Behavior:

- BNB enters ActivePool only from BorrowerOperations or DefaultPool receiver paths.
- BNB leaves ActivePool through restricted core calls: borrower withdrawal/close, liquidation offset, gas compensation, redemption, surplus accounting.
- BNB reaches StabilityPool during liquidations and SableStakingV2 through fee distribution.

## USDS

Address: `0x0c6Ed1E73BA73B8441868538E210ebD5DD240FA0`  
Name/symbol/decimals: `USDS Stablecoin`, `USDS`, `18`  
Total supply: `92032333642572499463529`

Live custody:

- StabilityPool: `6579363784326119862850`
- GasPool: `10000000000000000000`
- SableStakingV2: `654574197951713185`

Behavior:

- BorrowerOperations mints USDS to borrowers and GasPool when troves open or debt increases.
- BorrowerOperations/TroveManager/StabilityPool burn USDS during repay, close, liquidation offset, and redemption flows.
- StabilityPool deposits are actual USDS custody and equal `totalUSDSDeposits`.
- `approve` allows direct nonzero-to-nonzero allowance overwrite; this is already recorded as a confirmed repo-local issue.
- `permit` exists and shares the same allowance mutation endpoint through `_approve`.

## SABLE

Address: `0x1eE098cBaF1f846d5Df1993f7e2d10AFb35A878d`  
Name/symbol/decimals: `SABLE`, `SABLE`, `18`  
Total supply: `100000000000000000000000000`

Live custody:

- CommunityIssuance: `5409915403529186761416`
- SABLE_LP pair: `12176323796385788711697862`

Behavior:

- CommunityIssuance emits SABLE over time to StabilityPool depositors/front ends.
- SableStakingV2 can account for SABLE gains through `F_SABLE`, but current `F_SABLE` is zero.
- SABLE token has ERC20 allowance/permit behavior analogous to USDS.

## SABLE LP

Address: `0xa0D4e270D9EB4E41f7aB02337c21692D7eECCCB0`  
Name/symbol/decimals: `Pancake LPs`, `Cake-LP`, `18`  
Total supply: `23216479908809073414647`

Live custody:

- SableStakingV2: `20935597236192701456120`

Behavior:

- SableStakingV2 stakes this LP token and tracks `totalSableLPStaked`.
- Current LP custody equals the staking accounting.
- Pair assets are SABLE and WBNB with reserves `12176323796385788711697862` SABLE and `48826407685591615235` WBNB.

## Unknown Token Enumeration

Raw RPC can query known token balances but cannot discover unknown BEP20 token contracts held by an address. A complete "all tokens present including random airdrops" pass requires a token-holder index from BscScan, Covalent, Bitquery, GoldRush, or equivalent. That requirement is included in `live-recon-prompt.md`.

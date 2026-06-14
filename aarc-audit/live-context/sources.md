# Sources

## Local Evidence

- `README.md` - existing Sable ActivePool summary and trust model.
- `source-artifacts/deployment-context.json` - target identity, deployed address graph, owner snapshot, compiler, verification, proxy status.
- `source-artifacts/live_state_snapshot.json` - April 14, 2026 live-state snapshot.
- `source-artifacts/*_runtime_code.txt` and `source-artifacts/*_bscscan.html` - saved runtime/source evidence.
- `source-artifacts/source_tree_map.json` - local source mapping.
- `src/**/*.sol` - local source used for scope and trigger classification.
- `aarc-audit/01-usds-approve-race-allows-user-balance-drain.md` - existing confirmed token allowance finding.
- `live_context.json` - canonical combined Sable live-context artifact. It previously contained Morpho Midnight context and was replaced during this run.

## Current RPC Evidence

RPC endpoint used: `https://bsc-dataseed.binance.org/`

Commands run on 2026-06-07:

```sh
cast block-number --rpc-url https://bsc-dataseed.binance.org/
cast balance 0x0ccb12c9fb1e1252e60d29ac5c4fdc0640edd72c --rpc-url https://bsc-dataseed.binance.org/
cast call 0x0ccb12c9fb1e1252e60d29ac5c4fdc0640edd72c 'getBNB()(uint256)' --rpc-url https://bsc-dataseed.binance.org/
cast call 0x0ccb12c9fb1e1252e60d29ac5c4fdc0640edd72c 'getUSDSDebt()(uint256)' --rpc-url https://bsc-dataseed.binance.org/
cast call 0x598913568093AB9F3d549236EB98388271073F18 'getTotalUSDSDeposits()(uint256)' --rpc-url https://bsc-dataseed.binance.org/
cast call 0x598913568093AB9F3d549236EB98388271073F18 'getBNB()(uint256)' --rpc-url https://bsc-dataseed.binance.org/
cast call 0x0c6Ed1E73BA73B8441868538E210ebD5DD240FA0 'totalSupply()(uint256)' --rpc-url https://bsc-dataseed.binance.org/
cast call 0xA5220fd82C098b7f1C711e2F1C1d599ccfbCDCB3 'lastGoodPrice()(uint256)' --rpc-url https://bsc-dataseed.binance.org/
cast call 0x654Ed83ab231550001Fc1d2281B78fcD84121088 'getBNB()(uint256)' --rpc-url https://bsc-dataseed.binance.org/
cast call 0x654Ed83ab231550001Fc1d2281B78fcD84121088 'getUSDSDebt()(uint256)' --rpc-url https://bsc-dataseed.binance.org/
cast call 0xEC035081376ce975Ba9EAF28dFeC7c7A4c483B85 'getTroveOwnersCount()(uint256)' --rpc-url https://bsc-dataseed.binance.org/
cast call 0x97C131C309A04BFa1AAE82856d64b696b89dC87C 'getSize()(uint256)' --rpc-url https://bsc-dataseed.binance.org/
cast call 0xA5220fd82C098b7f1C711e2F1C1d599ccfbCDCB3 'status()(uint8)' --rpc-url https://bsc-dataseed.binance.org/
cast call 0xA5220fd82C098b7f1C711e2F1C1d599ccfbCDCB3 'age()(uint256)' --rpc-url https://bsc-dataseed.binance.org/
cast call 0x698ad77E62679c8E6aCfAfea03547C38fC5Ec0aD 'getUSDSGasCompensation()(uint256)' --rpc-url https://bsc-dataseed.binance.org/
cast call 0x698ad77E62679c8E6aCfAfea03547C38fC5Ec0aD 'getMinNetDebt()(uint256)' --rpc-url https://bsc-dataseed.binance.org/
cast call 0x698ad77E62679c8E6aCfAfea03547C38fC5Ec0aD 'getMCR()(uint256)' --rpc-url https://bsc-dataseed.binance.org/
cast call 0x698ad77E62679c8E6aCfAfea03547C38fC5Ec0aD 'getCCR()(uint256)' --rpc-url https://bsc-dataseed.binance.org/
cast call 0x698ad77E62679c8E6aCfAfea03547C38fC5Ec0aD 'getBorrowingFeeFloor()(uint256)' --rpc-url https://bsc-dataseed.binance.org/
cast call 0x698ad77E62679c8E6aCfAfea03547C38fC5Ec0aD 'getRedemptionFeeFloor()(uint256)' --rpc-url https://bsc-dataseed.binance.org/
cast call 0x0ccb12c9fb1e1252e60d29ac5c4fdc0640edd72c 'owner()(address)' --rpc-url https://bsc-dataseed.binance.org/
cast call 0xa49BEC2146fBeeA7314cdbe0Fd222419B0c0602f 'owner()(address)' --rpc-url https://bsc-dataseed.binance.org/
cast call 0xEC035081376ce975Ba9EAF28dFeC7c7A4c483B85 'owner()(address)' --rpc-url https://bsc-dataseed.binance.org/
cast call 0x598913568093AB9F3d549236EB98388271073F18 'owner()(address)' --rpc-url https://bsc-dataseed.binance.org/
cast call 0x654Ed83ab231550001Fc1d2281B78fcD84121088 'owner()(address)' --rpc-url https://bsc-dataseed.binance.org/
```

Additional expanded recon included:

- `forge inspect ... storage-layout` for `BorrowerOperations`, `TroveManager`, `StabilityPool`, `SystemState`, and `CollSurplusPool`.
- `cast storage` reads for private dependency addresses: GasPool, CollSurplusPool, and SystemState TimeLock.
- SableStakingV2 getters for SABLE token, LP token, rewarder, staking totals, and fee accumulators.
- CommunityIssuance getters for SABLE issued, last issuance time, and reward rate.
- PriceFeed getters for Chainlink aggregator, Pyth wrapper, and Pyth feed id.
- ERC20 `name`, `symbol`, `decimals`, `totalSupply`, and `balanceOf` across all recovered protocol addresses for USDS, SABLE, and SABLE_LP.
- Pancake LP `token0`, `token1`, and `getReserves`.
- Single live trove owner and trove debt/collateral/stake/pending reward reads.

## Known Gaps

- `cast` network access was required because sandbox DNS blocked RPC by default.
- Unknown/spam BEP20 token holdings require an explorer token-holdings index; raw RPC cannot discover unknown token contracts held by an address.
- StabilityPool depositor/front-end enumeration from events has not yet been completed.
- SableRewarder and TimeLock deep ABI/source behavior still need a focused follow-up.

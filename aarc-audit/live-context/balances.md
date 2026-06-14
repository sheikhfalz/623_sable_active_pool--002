# Balances

Live refresh block: `102807300`  
RPC: `https://bsc-dataseed.binance.org/`

This file records native BNB plus every protocol-used ERC20/LP token recovered from the deployed graph. Unknown airdropped/spam tokens are not enumerable from raw RPC alone; an explorer token-holdings index is required for that separate sweep.

## Protocol-Used Tokens

| Token | Address | Name | Symbol | Decimals | Total Supply |
| --- | --- | --- | --- | ---: | ---: |
| Native BNB | native | BNB | BNB | 18 | n/a |
| USDS | `0x0c6Ed1E73BA73B8441868538E210ebD5DD240FA0` | USDS Stablecoin | USDS | 18 | `92032333642572499463529` |
| SABLE | `0x1eE098cBaF1f846d5Df1993f7e2d10AFb35A878d` | SABLE | SABLE | 18 | `100000000000000000000000000` |
| SABLE LP | `0xa0D4e270D9EB4E41f7aB02337c21692D7eECCCB0` | Pancake LPs | Cake-LP | 18 | `23216479908809073414647` |

## Native BNB Balances

| Role | Address | BNB wei |
| --- | --- | ---: |
| ActivePool | `0x0cCb12C9fB1e1252E60d29aC5c4fDc0640edD72C` | `874414848004364383519` |
| BorrowerOperations | `0xa49BEC2146fBeeA7314cdbe0Fd222419B0c0602f` | `0` |
| TroveManager | `0xEC035081376ce975Ba9EAF28dFeC7c7A4c483B85` | `0` |
| StabilityPool | `0x598913568093AB9F3d549236EB98388271073F18` | `87196` |
| DefaultPool | `0x654Ed83ab231550001Fc1d2281B78fcD84121088` | `0` |
| USDSToken | `0x0c6Ed1E73BA73B8441868538E210ebD5DD240FA0` | `0` |
| PriceFeed | `0xA5220fd82C098b7f1C711e2F1C1d599ccfbCDCB3` | `9999999999999467` |
| OracleRateCalculation | `0x76Dcd40843C1dE96839bf83790257A36011E6632` | `0` |
| SystemState | `0x698ad77E62679c8E6aCfAfea03547C38fC5Ec0aD` | `0` |
| SortedTroves | `0x97C131C309A04BFa1AAE82856d64b696b89dC87C` | `0` |
| SableStakingV2 | `0xFbc81aEB7e5c11d4A60a0690Db9F36F93E25B16C` | `301290650075643435` |
| GasPool | `0xE9bc9aDBdf67343b5A66D73Cf2E521bb3f088D01` | `0` |
| CollSurplusPool | `0xBE40060aEf1A2aCb4425823c82978F976fD93cd0` | `0` |
| TimeLock | `0x638675b7C2e056917567571307C6f6A7D69A258A` | `0` |
| SABLEToken | `0x1eE098cBaF1f846d5Df1993f7e2d10AFb35A878d` | `0` |
| TroveHelper | `0xd1BF4d208028CBFe65c6b4D68C12e68F5F3D80F8` | `0` |
| CommunityIssuance | `0x7fd517b06b898F1a6081E0891265516F83Dc9C9E` | `0` |
| SableLPToken | `0xa0D4e270D9EB4E41f7aB02337c21692D7eECCCB0` | `0` |
| SableRewarder | `0x23d253F1Ab38a1Ec8c05103232B4eFaFB6A1bdEb` | `0` |

## Nonzero ERC20/LP Balances

| Token | Holder | Balance |
| --- | --- | ---: |
| USDS | StabilityPool | `6579363784326119862850` |
| USDS | SableStakingV2 | `654574197951713185` |
| USDS | GasPool | `10000000000000000000` |
| SABLE | CommunityIssuance | `5409915403529186761416` |
| SABLE | SableLPToken | `12176323796385788711697862` |
| SABLE_LP | SableStakingV2 | `20935597236192701456120` |

## Zero ERC20/LP Balance Coverage

All recovered protocol addresses were checked for USDS, SABLE, and SABLE_LP balances. Every omitted pair is zero at the refresh block.

## Balance Invariants

- ActivePool raw BNB equals `ActivePool.getBNB()`: `874414848004364383519`.
- StabilityPool USDS token balance equals `getTotalUSDSDeposits()`: `6579363784326119862850`.
- GasPool USDS balance equals current `SystemState.getUSDSGasCompensation()`: `10000000000000000000`.
- SableStakingV2 SABLE_LP balance equals `totalSableLPStaked()`: `20935597236192701456120`.
- DefaultPool has zero recorded BNB and zero recorded USDS debt.

## LP Pair

SABLE_LP token: `0xa0D4e270D9EB4E41f7aB02337c21692D7eECCCB0`

- `token0`: SABLE `0x1eE098cBaF1f846d5Df1993f7e2d10AFb35A878d`
- `token1`: WBNB `0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c`
- reserves: `12176323796385788711697862` SABLE and `48826407685591615235` WBNB
- reserve timestamp: `1780670741`

# Reusable Prompt: Full Live Context Recon

Use this prompt for the next protocol when the goal is comprehensive live context before audit scope generation.

```text
We need a comprehensive live-context recon for this protocol before generating audit scope.

Work from the current repo and the deployed on-chain contracts only. Do not scope broad source files unless a deployed contract, live integration, or direct custody/authority path can affect on-chain funds.

Create the canonical machine-readable artifact first:

0. repo-root `live_context.json`
   - this is the most important output.
   - combine all live context, deployed graph, scope, balances, token metadata, state model, behavior, invariants, weird values, unresolved items, and source/command evidence in this JSON.
   - use stable JSON keys and string-encode large integers to avoid precision loss.
   - Markdown files must mirror or explain this JSON, not replace it.

Then create durable Markdown artifacts under a repo-local folder like `aarc-audit/live-context/`:

1. `README.md`
   - project name, chain, primary target, refresh block/date, file map, and a clear pointer that repo-root `live_context.json` is canonical.

2. `plan.md`
   - ordered plan to gather identity, deployed graph, funds, tokens, authority, trigger surface, structs/storage, pools/markets, invariants, weird values, and unresolved dependencies.

3. `scope.md` and `scope.json`
   - include only deployed contracts or direct live dependencies that can move/account funds, debt, collateral, rewards, oracle solvency, or authorization.
   - split primary scope, interface scope, conditional scope, and out-of-scope files.

4. `live-context.md`
   - deployed address graph.
   - proxy/implementation/compiler/verification status.
   - current block and all current live values.
   - actor/authority model.
   - value-flow model for every way funds enter, move, and exit.
   - trigger surface by user, keeper/liquidator, restricted core, admin/timelock, callback/proxy.
   - live invariants with pass/fail/unknown status.
   - weird values and strongest audit leads.

5. `balances.md`
   - native balance for every protocol address.
   - every protocol-used ERC20/LP/NFT/share/reward/debt/collateral token with name, symbol, decimals, total supply.
   - `balanceOf` matrix for every known protocol-used token across every recovered protocol address.
   - allowances where protocol custody depends on allowance.
   - separate random airdrops/spam tokens from protocol-used tokens.
   - if raw RPC cannot enumerate unknown token contracts, explicitly run or mark an explorer-index step using BscScan/Covalent/Bitquery/GoldRush or equivalent.

6. `tokens.md`
   - token role, custody, behavior, risk traits, balances, LP reserves, owner/admin/proxy traits where relevant.
   - check fee-on-transfer, rebasing, blacklist/pause, non-standard return, ERC777/hooks, permit, flash mint, upgradeability, high/low decimals.

7. `state-model.md`
   - all important structs/enums/storage variables/mappings/arrays/constants/immutables.
   - decoded storage slots for private addresses and non-public values that affect funds.
   - live values for accounting totals, indices, reserves, reward accumulators, caps, fees, pause flags, oracle status, pool records.
   - behavior of each struct during deposit, withdraw, borrow, repay, liquidation, redemption, claim, harvest, reward, oracle update, and admin change paths.

8. `sources.md`
   - exact local files, artifacts, explorer/API sources, RPC endpoint, refresh block, and every command/script used.

Required methodology:

- Start from local deployment metadata, verified source, ABI/artifacts, and runtime code.
- Use `cast call`, `cast balance`, `cast storage`, `cast logs`, `forge inspect ... storage-layout`, and ABI getters.
- Recover private dependency addresses from storage layouts or setup events.
- For each recovered contract, read native balance, token balances, owner/admin/timelock/upgrader, paused flags, caps, fee params, accounting totals, reward state, oracle state, and pool/market records.
- Enumerate users/pools/markets through public arrays, registry getters, factory events, token transfer events, and protocol events.
- Compare raw balances to internal accounting totals.
- Mark unknowns explicitly with the exact missing command/API, never silently omit them.
- If live calls require network/RPC/API access, request it and continue. If a call fails, record the failure and fallback evidence.
- Validate `live_context.json` with `jq` before finishing.
- Ensure the JSON and Markdown agree on target address, recovered addresses, token balances, scope counts, invariants, and unresolved items.

Final answer should include:

- target address and chain,
- artifact folder path,
- canonical JSON path and Markdown files written,
- counts of scoped source files, recovered addresses, protocol-used tokens, balances checked, trigger surfaces, structs/state groups, invariants, weird values, and unresolved items,
- current largest custody balances,
- strongest next audit action.
```

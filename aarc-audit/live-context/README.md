# Sable ActivePool Live Context

Project: Sable Finance Active Pool  
Chain: BNB Smart Chain mainnet (`chain_id = 56`)  
Primary deployed target: `ActivePool` at `0x0cCb12C9fB1e1252E60d29aC5c4fDc0640edD72C`  
Live refresh block: `102807300`  
Refresh date: `2026-06-07`

This folder defines the live-context-first audit scope for this run. Scope is limited to deployed contracts, deployed integrations, or local source files that can directly affect funds, debt, collateral, rewards, oracle-dependent solvency, or withdrawal/claim paths in the live deployment.

Canonical machine-readable context:

- `../../live_context.json` from this folder, or repo-root `/Volumes/king-null-ssd/github/623_sable_active_pool/live_context.json`

The JSON file is the most important artifact. The Markdown files are supporting mirrors for human review and should stay consistent with the JSON.

Files:

- `plan.md` - ordered plan for gathering all live protocol properties.
- `scope.md` - human-readable in-scope, conditional-scope, and out-of-scope decisions.
- `scope.json` - machine-readable scope list for tooling.
- `live-context.md` - current deployed wiring, balances, accounting values, authority, triggers, and invariants.
- `balances.md` - native BNB plus USDS/SABLE/SABLE_LP balances across recovered protocol addresses.
- `tokens.md` - protocol-used token metadata, roles, custody, and token-specific live behavior.
- `state-model.md` - structs, storage model, live state, and on-chain behavior map.
- `live-recon-prompt.md` - reusable prompt for future full live-context gathering runs.
- `sources.md` - exact evidence sources and commands used.

Input hygiene note: repo-root `live_context.json` previously described Morpho Midnight. It has been replaced with the canonical Sable Finance live context for this repo.

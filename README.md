# Sable Finance ActivePool Value-Flow Audit

Target: `ActivePool`  
Address: `0x0ccb12c9fb1e1252e60d29ac5c4fdc0640edd72c`  
Chain: BNB Smart Chain  
Rank source: local top-contract list entry `623`  
Live balance at audit time: `874.414848004364383519 BNB`

## Trust model

Protocol-governed roles and timelock-controlled configuration are trusted for this run. A finding is only in scope if an untrusted actor can steal user assets or protocol-held value, or can seize a privileged drain path from outside the intended governance boundary.

## Deployment arrangement

- `ActivePool` is a verified, non-proxy contract compiled with `v0.6.11+commit.5ef660b1` and optimizer runs `1`.
- Live wiring resolves to:
  - `BorrowerOperations`: `0xa49BEC2146fBeeA7314cdbe0Fd222419B0c0602f`
  - `TroveManager`: `0xEC035081376ce975Ba9EAF28dFeC7c7A4c483B85`
  - `StabilityPool`: `0x598913568093AB9F3d549236EB98388271073F18`
  - `DefaultPool`: `0x654Ed83ab231550001Fc1d2281B78fcD84121088`
  - `USDSToken`: `0x0c6Ed1E73BA73B8441868538E210ebD5DD240FA0`
  - `PriceFeed`: `0xA5220fd82C098b7f1C711e2F1C1d599ccfbCDCB3`
- The core pool contracts in this deployment report `owner = address(0)` after setup.

## Result

- Protocol-wide drain: not confirmed
- User-asset theft: confirmed

The custody pool itself is tightly caller-gated, and I did not confirm an untrusted path that drains `ActivePool` or protocol TVL. The confirmed live theft path is on the connected `USDSToken`: it keeps the standard ERC20 non-zero-to-non-zero `approve` race, allowing an already-approved spender to front-run an allowance change and drain `oldAllowance + newAllowance` from one victim.

## Evidence

- Source, runtime bytecode, and live wiring are saved under `source-artifacts/`.
- Confirmed finding: `aarc-audit/01-usds-approve-race-allows-user-balance-drain.md`
- Trust-boundary notes: `aarc-audit/90-trust-model-notes.md`
- Repro test: `test/USDSTokenApproveRaceAudit.t.sol`

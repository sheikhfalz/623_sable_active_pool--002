# Extraction-Scope Update Prompt

Use this prompt in future audits when `questions.py`, `RESEARCHER.md`, and `SECURITY.md` must be aligned to a bounty program that only pays for fund extraction and reward extraction.

```text
Update `questions.py`, `RESEARCHER.md`, and `SECURITY.md` so they focus only on the target bounty impact classes:

1. Critical fund extraction or protocol value drain:
   An unprivileged user can gain, mint, borrow, redeem, withdraw, claim, or extract more funds/value than intended from the protocol.

2. Critical reward extraction or unfair reward access:
   An unprivileged user can claim rewards they should not receive, claim more than their entitlement, bypass reward eligibility/timing, repeat/replay reward claims, or otherwise extract excess reward value.

Critical safety rule for `questions.py`:

- Do not edit runnable Python code.
- Do not change imports.
- Do not change constants such as `MAX_REPO`, `SOURCE_REPO`, `REPO_NAME`, or `run_number`.
- Do not change `scope_files`, `target_scopes`, `scope_scan`, function names, function signatures, return statements, file loading logic, environment-variable logic, or any code that another script may depend on.
- Do not add new functions, classes, imports, dependencies, file writes, subprocess calls, network calls, or behavior.
- Only edit human-readable prompt text, docstrings, comments, and wording inside existing prompt strings where necessary.
- Preserve valid Python syntax and run `python3 -m py_compile questions.py` after editing.

For `questions.py`:

- Keep the existing target scopes if they already contain only fund extraction and reward extraction.
- Update the generator, audit, validation, and analog-scan prompt text so all generated questions and validations only accept fund extraction/protocol value drain or reward extraction/unfair reward access.
- Replace stale protocol wording with the current protocol's real live context from `live_context.json`.
- If interfaces are needed, add them only as `Context-only interface files` inside existing human-readable prompt text. Use them only for ABI, selectors, structs, events, return values, and cross-contract expectations. Do not add a new Python variable, do not change `scope_files`, and do not treat interfaces as vulnerability target scope unless an "interface" file actually contains deployed executable logic.
- Reject DoS, liveness, freezes, griefing, liquidation blockage, generic accounting desync, and generic high/medium/critical severity unless the same path directly lets an attacker extract funds/rewards or increase attacker-controlled value.

For `RESEARCHER.md`:

- Replace broad researcher goals with extraction-only goals.
- Retarget attacker profiles, priority surfaces, high-value scenarios, evidence standard, rejection filters, and reporting format toward fund/reward extraction.
- Make DoS, freeze, liveness, griefing, liquidation blockage, generic accounting desync, and generic high/medium/critical severity out of scope unless they directly create attacker-controlled value extraction.

For `SECURITY.md`:

- Add or preserve a paid-impact focus section containing only the two accepted impact families.
- Add explicit out-of-scope rules for DoS/freeze/liveness/griefing/liquidation blockage/accounting-only issues.
- Keep oracle, rounding, liquidation, redemption, fee, token, and reward issues in scope only when they directly enable fund/reward extraction.

Verification before finishing:

- Confirm `questions.py` compiles with `python3 -m py_compile questions.py`.
- Confirm no generated `__pycache__` or bytecode files are left behind.
- Confirm `rg` finds no stale protocol/model wording that would steer the generator to unrelated impacts.
- Summarize exactly which files changed and state whether runnable Python code was left untouched.
```

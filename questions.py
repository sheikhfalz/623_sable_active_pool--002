import json
import os

from decouple import config

# todo: if scope_files is: 500 > 50, 300 > 30 , 100 > 10
MAX_REPO = 10
# todo: the path from https:///github.com/dfinity/ICRC-1
SOURCE_REPO = "incjanta/623_sable_active_pool"
# todo: the name of the repository
REPO_NAME = "623_sable_active_pool"
run_number = os.environ.get('GITHUB_RUN_NUMBER', '0')


def get_cyclic_index(run_number, max_index=100):
    """Convert run number to a cyclic index between 1 and max_index"""
    return (int(run_number) - 1) % max_index + 1


def load_repository_urls():
    """Load repository URLs from repositories.json."""
    repo_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "repositories.json")
    if not os.path.exists(repo_file):
        return []

    try:
        with open(repo_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []

    if not isinstance(data, list):
        return []

    return [url for url in data if isinstance(url, str) and url.strip()]


if run_number == "0":
    BASE_URL = f"https://deepwiki.com/{SOURCE_REPO}"
else:
    repository_urls = load_repository_urls()
    if repository_urls:
        run_index = get_cyclic_index(run_number, len(repository_urls))
        BASE_URL = repository_urls[run_index - 1]
    else:
        BASE_URL = f"https://deepwiki.com/{SOURCE_REPO}"

scope_files = [
    "src/ActivePool.sol",
    "src/BorrowerOperations.sol",
    "src/TroveManager.sol",
    "src/StabilityPool.sol",
    "src/DefaultPool.sol",
    "src/CollSurplusPool.sol",
    "src/USDSToken.sol",
    "src/PriceFeed.sol",
    "src/SystemState.sol",
    "src/SortedTroves.sol",
    "src/OracleRateCalculation.sol",
    "src/TroveHelper.sol",
    "src/SABLE/SableStakingV2.sol",
    "src/SABLE/CommunityIssuance.sol",
    "src/SABLE/SABLEToken.sol",
    "src/GasPool.sol",
    "src/TimeLock.sol",
    "src/SableRewarder.sol",
    "src/BNBTransferScript.sol",
    "src/Proxy/*.sol"
]

target_scopes = [


    "Critical Fund extraction or protocol value drain: any bug that lets a user gain, mint, borrow, redeem, withdraw, claim, or extract more funds than intended from the protocol, including minting value from   nothing, flashloan-assisted extraction, oracle manipulation extraction,  broken accounting, unauthorized withdrawals,  over-redemption, underpayment, insolvency   creation, or any other path that increases   attacker-controlled funds at protocol or user   expense",

    "Critical Reward extraction or unfair reward access: any bug that lets a user access rewards they should not receive, enter or manipulate state before rewards are   distributed, bypass eligibility or timing   rules, claim more rewards than other users with the same entitlement, repeat/replay   reward claims, or otherwise gain excess   reward value from the protocol",

]

scope_scan = [
]

def question_generator(target_file: str) -> str:
    """
    Generate fund/reward-extraction audit + fuzzing questions for one sable active pool target.

    ```
    target_file format:
    "'File Name: src/ActivePool.sol -> Scope: Critical Fund extraction or protocol value drain'"
    """

    prompt = f"""
    ```
    
    Generate fund-extraction and reward-extraction security audit/fuzzing questions for this exact sable pool target:
    
    {target_file}
    
    Use live_context.json values if available: deployed address graph, native/token balances, pool accounting, trove state, oracle config, system parameters, staking/reward state, token decimals, and known invariant assumptions.

    Context-only interface files:
    - src/Interfaces/IActivePool.sol
    - src/Interfaces/IPool.sol
    - src/Interfaces/IDefaultPool.sol
    - src/Interfaces/ICollSurplusPool.sol
    - src/Interfaces/IStabilityPool.sol
    - src/Interfaces/ITroveManager.sol
    - src/Interfaces/ITroveHelper.sol
    - src/Interfaces/IBorrowerOperations.sol
    - src/Interfaces/IUSDSToken.sol
    - src/Interfaces/ISABLEToken.sol
    - src/Interfaces/ISableStakingV2.sol
    - src/Interfaces/ICommunityIssuance.sol
    - src/Interfaces/IPriceFeed.sol
    - src/Interfaces/IOracleRateCalculation.sol
    - src/Interfaces/ISortedTroves.sol
    - src/Dependencies/IERC20.sol
    - src/Dependencies/IERC2612.sol

    Use these interface files only to understand ABI, selectors, structs, events, return values, and cross-contract expectations. Do not treat them as vulnerability target scope files. Only prove bugs through deployed concrete contracts that hold, move, mint, burn, account for, or distribute funds/rewards.
    
    Protocol focus:
    Sable is a Liquity-style BNB-collateralized debt system with troves, ActivePool BNB custody, USDS debt/supply accounting, liquidation/redemption flows, StabilityPool deposits/rewards, SABLE staking rewards, oracle-driven solvency checks, and timelock-controlled system parameters.
    This bounty focus is only fund extraction and reward extraction. Do not generate questions for DoS, griefing, liveness, temporary freezes, informational issues, or generic high/medium/critical severity unless the path directly lets an attacker extract funds/rewards or increase attacker-controlled value at protocol/user expense.
    
    Core invariants:
    
    * attackers must not extract BNB, USDS, SABLE, SABLE_LP, collateral, debt value, liquidation gains, redemption value, staking rewards, or StabilityPool rewards beyond valid entitlement;
    * ActivePool, DefaultPool, StabilityPool, GasPool, CollSurplusPool, staking, and token balances must match their accounting liabilities;
    * every USDS mint must correspond to valid debt and every burn/repay/redemption/liquidation must reduce the correct liability;
    * collateral cannot be withdrawn, redeemed, seized, or redirected unless the attacker pays the required debt/value and satisfies liquidation/redemption rules;
    * liquidation, redemption, StabilityPool, staking, and reward paths must not let a user receive more value than their collateral/deposit/stake/reward entitlement;
    * oracle, rounding, decimal, fee, and accounting edge cases must not create extractable surplus for an unprivileged user;
    * token approvals, permits, callbacks, external transfers, or reentrancy must not enable unauthorized value movement or double-claiming.
    
    Rules:
    
    * Treat `File Name:` as the exact file/module.
    * Treat `Scope:` as the ONLY impact to target.
    * Assume full repo context is accessible.
    * Do not ask for code or say anything is missing.
    * Use exact Solidity symbols when possible.
    * Attacker is unprivileged: borrower, USDS holder, StabilityPool depositor, liquidator, redeemer, SABLE/SABLE_LP holder, staker, reward claimant, spender, permit user, or receiver contract.
    * Do not rely on admin compromise, malicious governance, leaked keys, impossible oracle values, or pure external oracle failure.
    * Reject DoS/freeze/liveness/griefing questions unless the same path gives the attacker direct fund or reward extraction.
    * Generate 35 to 60 high-signal questions.
    * At least 70% must be multi-step flow, invariant, fuzz, accounting, state-transition, or cross-module questions.
    * Every question must be testable by PoC, unit test, fuzz test, invariant test, or differential test.
    * Avoid generic checklist questions and repeated root causes.
    
    High-value attack surfaces:
    
    * ActivePool and DefaultPool BNB/debt accounting: over-withdrawal, over-redemption, double-counting, redistribution mistakes;
    * BorrowerOperations trove flows: open, adjust, repay, close, collateral withdrawal, gas compensation, fee minting;
    * TroveManager liquidation/redemption: seize amount, repay amount, collateral surplus, gas compensation, baseRate, snapshots, last-trove boundaries;
    * StabilityPool deposits/withdrawals/offsets: USDS deposit accounting, BNB gains, SABLE gains, front-end rewards, product/sum/epoch/scale rounding;
    * CollSurplusPool and GasPool: claimable collateral and gas compensation balances that can be overclaimed or misdirected;
    * SableStakingV2 and CommunityIssuance: LP stake accounting, BNB/USDS/SABLE reward accumulators, repeated claims, zero-stake reward leakage, wrong recipient;
    * USDSToken/SABLEToken: allowance, permit, mint/burn, transfer restrictions, pool-transfer paths that can move value without valid entitlement;
    * PriceFeed and OracleRateCalculation: stale/fallback/deviation/rounding cases only when they create borrow, redemption, liquidation, or reward extraction;
    * math/libs: fixed-point rounding, truncation, dust, snapshot, accumulator, and precision errors that create extractable value;
    * external-call/reentrancy surfaces: receiver contracts, token behavior, BNB sends, and state ordering only when they enable unauthorized withdrawal, overclaim, or double-claim.
    
    Impact mapping:
    
    * Fund extraction: attacker receives BNB, USDS, SABLE, SABLE_LP, collateral, redemption value, liquidation gain, fee value, or debt value without paying correct value.
    * Reward extraction: attacker overclaims StabilityPool, front-end, CommunityIssuance, staking, BNB, USDS, SABLE, or LP-derived rewards.
    * Insolvency with extraction: attacker creates or uses a balance/accounting mismatch to withdraw, redeem, borrow, liquidate, or claim more than funded.
    * Bad debt with extraction: borrower receives USDS or collateral value while undercollateralized or without the required repayment.
    * Unauthorized seizure/withdrawal: funds move to the attacker without valid authorization, ownership, redemption, liquidation, stake, deposit, or claim entitlement.
    * Accounting corruption only counts if it leads to attacker-controlled over-withdrawal, over-borrow, over-redemption, over-liquidation, over-claim, or reward overpayment.
    
    Each question must include:
    
    1. target function/module;
    2. attacker action;
    3. preconditions;
    4. call sequence;
    5. invariant tested;
    6. scoped impact;
    7. proof idea.
    
    Output only valid Python. No markdown. No explanations.
    
    questions = [
    "[File: {target_file}] [Function: symbol_or_module] Can an unprivileged ATTACKER_ACTION under PRECONDITIONS trigger CALL_SEQUENCE, violating INVARIANT, causing scoped impact: SCOPE_IMPACT? Proof idea: fuzz/state-test PARAMETERS and assert EXPECTED_PROPERTY.",
    ]
    """
    return prompt

def audit_format(security_question: str) -> str:
    """
    Generate a focused sable pool fund/reward-extraction validation prompt.
    """

    prompt = f"""# SECURITY AUDIT PROMPT

## Question
{security_question}

## Rules
- The referenced 623_sable_active_pool file/path exists. Do not say files are missing.
- Do not ask for code. Use available repository context.
- Analyze only this question and only the scoped impact.
- Attacker is unprivileged: borrower, USDS holder, StabilityPool depositor, liquidator, redeemer, SABLE/SABLE_LP holder, staker, reward claimant, spender, permit user, or receiver contract.
- Ignore admin-only, governance-only, leaked-key, docs, style, gas-only, and best-practice issues.
- Privileged functions matter only if they create a later user-triggered exploit path.
- Do not rely on impossible oracle values, pure oracle failure, malicious token owner action, or user mistake.
- Reject DoS, griefing, liveness, temporary freeze, liquidation blockage, and generic severity claims unless the same reachable path lets the attacker extract funds/rewards or increase attacker-controlled value.

## Mission
Prove or disprove this as a real Sable fund-extraction or reward-extraction bug.

Check:
- exact reachable Solidity path;
- attacker-controlled inputs;
- state changes before/after external calls;
- whether existing checks stop it;
- whether the scoped impact is concrete fund/reward extraction;
- whether a Foundry unit, fuzz, invariant, or stateful test can reproduce it.

## Core Invariants
- ActivePool, DefaultPool, StabilityPool, GasPool, CollSurplusPool, staking, and token balances cover their accounted liabilities;
- every USDS mint has matching debt and every burn/repay/redemption/liquidation reduces the correct liability;
- collateral cannot be withdrawn, redeemed, seized, or redirected outside valid ownership, health, redemption, or liquidation rules;
- StabilityPool deposits, BNB gains, SABLE gains, front-end rewards, and staking rewards cannot be overclaimed or claimed twice;
- healthy-position liquidation, oracle, rounding, fee, or snapshot bugs only count when they transfer excess value to the attacker;
- token approvals, permits, callbacks, BNB sends, ERC20 transfers, or reentrancy cannot move value without valid entitlement.

## Valid Only If
1. Exact file/function/line range exists.
2. Root cause is a real missing check, bad accounting, bad rounding, unsafe ordering, or broken invariant that enables fund/reward extraction.
3. Exploit path is: preconditions -> attacker call/data -> trigger -> bad state/result.
4. Existing protections are reviewed and insufficient.
5. Impact matches the scoped fund/reward extraction target.
6. PoC/test idea has clear assertions.

## Output
If valid, output exactly:

### Title
[Bug statement] - ([File: file_path])

### Summary
[2-3 sentences]

### Finding Description
[Code path, root cause, attacker inputs, exploit flow, and why checks fail]

### Impact Explanation
[Concrete scoped impact]

### Likelihood Explanation
[Preconditions, feasibility, repeatability]

### Recommendation
[Specific fix]

### Proof of Concept
[Foundry unit/fuzz/invariant/stateful test plan with expected assertions]

If invalid, output exactly:
#NoVulnerability found for this question.

No extra text.
"""
    return prompt


def validation_format(report: str) -> str:
    """
    Generate a strict bounty-style validation prompt for security claims.
    """
    prompt = f"""# VALIDATION PROMPT

## Security Claim
{report}

## Rules
- Validate only the submitted claim.
- Check Security.md/Researcher.md for scope, exclusions, and valid impact classes.
- Do not create a new vulnerability if the submitted claim is weak or invalid.
- Do not upgrade severity unless the provided evidence proves a larger fund/reward extraction impact.
- Reject admin-only, owner-only, trusted-operator, leaked-key, best-practice, docs/style, gas-only, and purely theoretical issues.
- Reject if the exploit requires unrealistic assumptions, victim mistakes, missing external context, or unsupported protocol behavior.
- A valid report must be triggerable by an unprivileged user, unless the claim proves privilege escalation from a user path.
- The final impact must match fund extraction, protocol value drain, reward extraction, or unfair reward access, not just a generic code bug.
- Reject DoS, freeze, liveness, griefing, liquidation blockage, or accounting-desync-only claims unless they directly let the attacker extract funds/rewards.
- Prefer #NoVulnerability over speculative reports.

## Required Validation Checks
All must pass:
1. Exact in-scope file, function, and line/code references.
2. Clear root cause and broken security/accounting assumption.
3. Reachable exploit path: preconditions -> attacker action -> trigger -> bad result.
4. Existing checks/guards reviewed and shown insufficient.
5. Concrete in-scope fund/reward extraction impact with realistic likelihood.
6. Reproducible proof path: unit PoC, fork test, invariant/fuzz test, or exact manual steps.
7. No obvious rejection reason from Security.md, known issues, privileges, or scope exclusions.

## Silent Triage Questions
Before output, internally answer:
- Can a normal external user trigger this?
- Does the code actually behave as claimed?
- Is the impact caused by this protocol, not by an external dependency alone?
- Is the fund/reward extraction concrete, not hypothetical?
- Would a bounty triager accept the proof?
- What exact test would prove it?

## Output
If valid, output exactly:

Audit Report

## Title
[Clear vulnerability statement] - ([File: file_path])

## Summary
[2-3 sentence summary of the bug and impact]

## Finding Description
[Exact code path, root cause, exploit flow, and why existing checks fail]

## Impact Explanation
[Concrete in-scope fund/reward extraction impact rationale]

## Likelihood Explanation
[Attacker capability, required conditions, feasibility, repeatability]

## Recommendation
[Specific fix guidance]

## Proof of Concept
[Minimal reproducible steps or fuzz/invariant/fork test plan]

If invalid, output exactly:
#NoVulnerability found for this question.

Output only one of the two outcomes above. No extra text.
"""
    return prompt


def scan_format(report: str) -> str:
    """
    Generate a short cross-project analog scan prompt for .
    """
    prompt = f"""# ANALOG SCAN PROMPT

## External Report
{report}

## Access Rules (Strict)
- Treat in-scope  files as accessible context.
- Do not claim missing/inaccessible files.
- Do not ask for repository contents.

## Objective
Find whether the same vulnerability class can occur in in-scope code as fund extraction or reward extraction.
Use the external report as a hint, not as proof.


Note: Check the RESEARCHER.md and think in this actual way 
Note: Check the Security.MD and never generate report that would result in out of scope and rejected vulnerability 

## Method
1. Classify vuln type only if it can cause fund extraction or reward extraction (auth, accounting, state transition, pricing/rounding, replay, reentrancy, oracle, token behavior).
2. Map to this current protocol with the external report to find a valid fund/reward extraction vulnerability.
3. Prove root cause with exact file/function/line references.
4. Confirm concrete fund/reward extraction impact + realistic likelihood.

## Disqualify Immediately
- No reachable attacker-controlled entry path.
- Trusted-role compromise required.
- Theoretical-only issue with no fund/reward extraction impact.
- DoS, freeze, liveness, griefing, or liquidation blockage without attacker value extraction.
- Impact or likelihood missing.

## Output (Strict)
If valid analog exists, output:

### Title
[Clear vulnerability statement] -([File: file_path)

### Summary
### Finding Description
### Impact Explanation
### Likelihood Explanation
### Recommendation
### Proof of Concept

If not, output exactly:
#NoVulnerability found for this question.

No extra text.
"""
    return prompt

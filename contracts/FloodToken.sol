pragma solidity ^0.6.6;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract FloodToken is ERC20 {

    constructor(uint256 initialSupply) public ERC20("FloodToken","FLOOD"){

        _mint(msg.sender, initialSupply);
    }
}
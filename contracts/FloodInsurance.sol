// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/ChainlinkClient.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";


contract floodInsurance is ChainlinkClient {
    
    IERC20 public floodToken;
    uint256 public warningThreshold; //user-defined threshold for paying out funds
    uint256 public warningLevel; // will be the value returned by oracle
    address private oracle; // oracle address
    address private customer; // wallet address for customer/insuree
    bytes32 private jobId; // oracle jobID
    uint256 private fee; // oracle fee
    address private owner; // stores contract owner address
    uint256 private payout_amount;
    bool public Funded;
    

    constructor(address _oracle, string memory _jobId, uint256 _fee, address _link, address _customer, uint256 _warningThreshold, address _tokenAddress, uint256 _payout_amount) public {
        
        // set link token address depending on network
        if (_link == address(0)) {
            setPublicChainlinkToken();
        } else {
            setChainlinkToken(_link);
        }
        
        // set FLOOD token
        floodToken = IERC20(_tokenAddress);

        // instantiate variables with values provided at contract deployment
        oracle = _oracle;
        jobId = stringToBytes32(_jobId);
        fee = _fee;
        customer = _customer;
        warningThreshold = _warningThreshold;
        payout_amount = _payout_amount;
        owner = msg.sender;

    }
    

    function checkFund() public view returns (bool Funded) {
        
        if (floodToken.balanceOf(address(this)) >= payout_amount){
            return true;
        }

        else {return false;}
        
    }


     
    function requestWarningLevel() public returns (bytes32 requestId) 
    {
        Chainlink.Request memory request = buildChainlinkRequest(jobId, address(this), this.fulfill.selector);
        
        // Set the URL to perform the GET request on
        request.add("get", "https://environment.data.gov.uk/flood-monitoring/id/floods");
        request.add("path", "items.0.severityLevel");
        
        // Sends the request
        return sendChainlinkRequestTo(oracle, request, fee);
    }

    function fulfill(bytes32 _requestId, uint256 _warningLevel) public recordChainlinkFulfillment(_requestId)
    
    {
        // fulfill request and instantiate warningLevel var with retrieved value
        warningLevel = _warningLevel;
    }


    function settleClaim() public onlyOwner{
        // settleClaim() can only be called by contract owner

        // address to make payment to: function level scope
        address outAddress;
        
        // condition: is warning level above threshold for payment
        // if so, set payment address to customer, else payment address is contract owner
        if (warningLevel>warningThreshold){outAddress = customer;}
        else{outAddress = msg.sender;}

        require(floodToken.transfer(outAddress, payout_amount), "Transfer failed");
        
        // instantiate LINK token
        LinkTokenInterface link = LinkTokenInterface(chainlinkTokenAddress());

        // transfer remaining contract LINK balance to sender
        require(link.transfer(msg.sender, link.balanceOf(address(this))), "Unable to transfer");
        
    }

    function escapeHatch() public onlyOwner{
        
        // in case of problem with GET request, call this function to return LINK to sender
        // this is just a development tool to conserve test LINK if deployed contract has
        // bugs lockign funds. Delete if this project ever goes anywhere near mainnet!

        LinkTokenInterface link = LinkTokenInterface(chainlinkTokenAddress());
        require(link.transfer(msg.sender, link.balanceOf(address(this))), "Unable to transfer");
        
    }

    ////////////////////////
    // ACCESSORY FUNCS
    ////////////////////////

    modifier onlyOwner(){
        require(owner==msg.sender);
        _;
    }

    function stringToBytes32(string memory source) public pure returns (bytes32 result) {
        // accessory function for converting string to bytes32 - required 
        // for passing jobID to oracle
    
        bytes memory tempEmptyStringTest = bytes(source);
        if (tempEmptyStringTest.length == 0) {
            return 0x0;
        }

        assembly {
            result := mload(add(source, 32))
        }
    }



}

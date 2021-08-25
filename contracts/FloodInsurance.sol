// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/ChainlinkClient.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

// TODO: Add aave lending pool functions for accruing yield on dai paid by customers
// TODO: Think again about how premiums work
// NOTE: ASSUMES CONTRACT OWNER IS INSURER
// NOTE: PAYMENT LOGIC IS HARDCODED AND DUMMY ATM: 300 DAI premium (paid once), 1000 x premium payout.

contract floodInsurance is ChainlinkClient {
    
    IERC20 public dai;
    address public daiAddress;
    uint256 public warningThreshold; //user-defined threshold for paying out funds
    uint256 public warningLevel; // will be the value returned by oracle
    address private oracle; // oracle address
    address private customer; // wallet address for customer/insuree
    address private donor; // wallet address for insurer
    bytes32 private jobId; // oracle jobID
    uint256 private fee; // oracle fee
    address private owner; // stores contract owner address
    mapping(address=>uint) approvalStatus;
    mapping(address=>uint256) premium;
    mapping(address=>string) lat;
    mapping(address=>string) lon;
    mapping(address=>uint16) elevation;
    mapping (address=>uint256) tides;
    mapping (address => uint256) payoutAmount;
    uint16 elev;
    uint256 tide;

    constructor(address _dai_address, address _oracle, 
    string memory _jobId, uint256 _fee, address _link) public {
        
        // set link token address depending on network
        if (_link == address(0)) {
            setPublicChainlinkToken();
        } else {
            setChainlinkToken(_link);
        }
              
        daiAddress = _dai_address;
        dai = IERC20(daiAddress);

        // instantiate variables with values provided at contract deployment
        oracle = _oracle;
        jobId = stringToBytes32(_jobId);
        fee = _fee;
        owner = msg.sender;

    }
    
    /**
    @dev
    dummy premium/payout calculations for now. fixed 300dai payment from customer and 10x premium payout amount.

    requires 300 dai to be transferred from customer to contract, otherwise adding customer fails.
    This requires customer to approve the transfer by calling the dai.approve func, e.g.

    dai.approve(contract address, amount, {from: customer address})

    owner must also approve tranfer of 3000 dai to contract


     */
    function add_customer(address _customer, string memory _lat, string memory _lon, uint16 _elev) payable public onlyOwner{

        premium[_customer]=300e18; //hard code dummy premium for now - update later
        payoutAmount[_customer] = premium[_customer] * 10;
        require(dai.transferFrom(_customer, address(this), premium[_customer]));
        require(dai.transferFrom(owner, address(this), payoutAmount[_customer]));
        approvalStatus[_customer]=1;
        lat[_customer] = _lat;
        lon[_customer] = _lon;
        elevation[_customer] = _elev;
    }



    /**
    @dev this public function wraps the two internal chainlink request funcs
    This is so that the result can be returned and appended to the tides 
    mapping to customer address
     */

    function requestTideExtreme(address _customer) public {

        makeTideRequest(_customer);
        updateTides(_customer, tide);

    }


    /**
    @dev
    this function uses a chainlink oracle to request the latest tide data for a point
    currently, this calls dummy data at the developer's github.io page, but will
    eventually point to stormglass.io and return data from the buoy nearest to the user
     */

    function makeTideRequest(address _customer) internal returns (bytes32 requestId){
        
        string memory URL = "https://raw.githubusercontent.com/jmcook1186/jmcook1186.github.io/main/Data/FloodInsuranceData/TideExtremes.json";
        Chainlink.Request memory request = buildChainlinkRequest(jobId, address(this), this.fulfill.selector);
        request.add("get", URL);
        request.add("path", "data.0.Tide_Extreme");
       
        return sendChainlinkRequestTo(oracle, request, fee);
    }


    function fulfill(bytes32 _requestId, uint256 _value) public recordChainlinkFulfillment(_requestId){
        // fulfill request and instantiate warningLevel var with retrieved value
        tide = _value;
    }

    /**
    @dev
    update the tide value for each customer
     */
    function updateTides(address _customer, uint256 tide) internal {
        
        tides[_customer] = tide;
    }



    ////////////////////////////////////////////////////////////////////
    // VIEW FUNCS
    ////////////////////////////////////////////////////////////////////

    function viewApproval(address _customer) public view returns (uint){

        return(approvalStatus[_customer]);

    }

    function viewlocation(address _customer) public view returns (string memory, string memory){
        
        return(lat[_customer], lon[_customer]);

    }


    function viewTide(address _customer) public view returns (uint256){

        return tides[_customer];

    }



    function checkFund() public view returns (uint256) {
        
        return dai.balanceOf(address(this));
        
    }


    function settleClaim(address _customer) public onlyOwner{
        // settleClaim() can only be called by contract owner

        // address to make payment to: function level scope
        address outAddress;
        uint256 tide = tides[_customer];
        uint256 elev = elevation[_customer];
        uint256 payAmount = payoutAmount[_customer];

        
        // condition: is warning level above threshold for payment
        // if so, set payment address to customer, else payment address is contract owner
        if (tide>elev){outAddress = customer;}

        else{outAddress = msg.sender;}

        require(dai.transfer(outAddress, payAmount), "Transfer failed");
        
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

        require(dai.transfer(msg.sender, dai.balanceOf(address(this))));
        
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

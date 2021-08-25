import pytest
import time
from brownie import config, network, interface

"""
unit tests for crucial functions:
    1) test token deploy: check token contract exists
    2) test token transfer: check token successfully moves between loaded wallets
    3) test sendLINK: check contract can receive LINK, fund contract for oracle gas
    4) test_warningLevel: check that contract successfully make GET request via oracle
    5) test_checkFunds: check the function that determines whether contract is sufficiently funded with FLOOD
    6) test_sendTokenToContract: check contract can receive FLOOD tokens in correct amounts
    7) test_settleClaim: check that the contract can transact based on oracle data, sending FLOOD to correct account

"""



def test_token_deploy(get_token):
    

    floodToken = get_token
    assert floodToken is not None

    return


def test_token_transfer(get_token,load_account1, load_account2):

    floodToken = get_token

    initialBalance = floodToken.balanceOf(load_account2)
    floodToken.transfer(load_account2, 100e18,{'from':load_account1})

    assert floodToken.balanceOf(load_account2) == initialBalance+100e18

    floodToken.transfer(load_account1, 100e18, {'from':load_account2})

    assert floodToken.balanceOf(load_account2) == initialBalance

    return


def test_sendLINK(get_contract,oracleGas,load_account1):
    
    contract = get_contract

    if interface.LinkTokenInterface(config["networks"][network.show_active()]["link_token"]).balanceOf(contract) >= oracleGas*5:
        pytest.skip("Contract already funded")
    
    else:
        interface.LinkTokenInterface(config["networks"][network.show_active()]["link_token"]).transfer(contract,oracleGas*5,{'from':load_account1})
        
        assert interface.LinkTokenInterface(config["networks"][network.show_active()]["link_token"]).balanceOf(contract) >= oracleGas*5
    
    return


def test_WarningLevel(get_contract, load_account1):

    contract = get_contract
    contract.requestWarningLevel({'from':load_account1})

    time.sleep(30)

    warningLevel = contract.warningLevel()

    assert warningLevel is not None

    assert warningLevel >= 0

    return warningLevel


def test_checkFund(get_contract):
    
    contract = get_contract
    Funded = contract.checkFund()

    assert Funded is not None

    return


def test_sendTokenToContract(get_contract, load_account1, load_account2, set_payout_amount, get_token):

    contract= get_contract
    token= get_token

    if token.balanceOf(contract) < set_payout_amount:
        token.transfer(contract, set_payout_amount-token.balanceOf(contract), {'from':load_account1})

    if token.balanceOf(load_account2) > 0:
        token.transfer(load_account1, token.balanceOf(load_account2), {'from':load_account2})
    
    assert token.balanceOf(contract) >= set_payout_amount
    assert token.balanceOf(load_account2) == 0

    return


def test_settleClaim(get_contract, get_token, set_payout_amount, load_account1, load_account2, oracleGas):
    
    network.gas_limit(6700000)

    contract = get_contract
    token = get_token

    gasBalance = interface.LinkTokenInterface(config["networks"][network.show_active()]["link_token"]).balanceOf(contract)
    
    if gasBalance < oracleGas*5:
        interface.LinkTokenInterface(config["networks"][network.show_active()]["link_token"]).transfer(contract,oracleGas*5,{'from':load_account1})

    if token.balanceOf(contract) < set_payout_amount:
        token.transfer(contract, set_payout_amount-token.balanceOf(contract), {'from':load_account1})

    assert token.balanceOf(contract) >= set_payout_amount
    assert gasBalance >= oracleGas


    contract.settleClaim({'from':load_account1})

    if contract.warningLevel() < 3:

        assert token.balanceOf(contract) < set_payout_amount
        assert token.balanceOf(load_account1) >= set_payout_amount

    if contract.warningLevel() >= 3:
        
        assert token.balanceOf(contract) < set_payout_amount
        assert token.balanceOf(load_account2) >= set_payout_amount

    return

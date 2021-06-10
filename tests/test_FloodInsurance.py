import pytest
import time
from brownie import floodInsurance, config, network ,interface, FloodToken


@pytest.fixture(scope='module')
def get_token():

    if network.show_active() == 'kovan':

        floodToken = FloodToken.at('0x63585C9f4968658cB36C48fa33e34BE513c5e4D9')
    
    else:
        pytest.fail('Please test on kovan network')

    return floodToken


@pytest.fixture(scope='module')
def get_contract():
    
    contract = floodInsurance.at('0xE094A61c7e10b5ECbEE6006a1207239d515d1548') 

    return contract


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


# def test_contract_deployed(get_contract):
#     contract = get_contract
#     contract.address != None
#     return


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

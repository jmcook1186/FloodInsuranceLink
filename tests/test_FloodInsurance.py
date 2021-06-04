import pytest
import time
from brownie import floodInsurance, config, network ,interface



@pytest.fixture(scope='module')
def deploy_contract(load_account1, load_account2):
    
    print("Deploying contract to {} network".format(network.show_active()))
    
    floodInsurance.deploy(
    # deploy with args required by contract's constructor func:
    # 1) oracle address
    # 2) jobID
    # 3) LINK fee to pay oracle
    # 4) LINK token address 
    # values for args are in brownie-config.yaml
    config["networks"][network.show_active()]["oracle"], 
    config["networks"][network.show_active()]["jobId"],
    config["networks"][network.show_active()]["fee"],
    config["networks"][network.show_active()]["link_token"],
    load_account2,
    3,
    {'from':load_account1}
    )
    
    contract = floodInsurance[len(floodInsurance)-1] 

    return contract


def test_deployed(deploy_contract):
    contract = deploy_contract
    contract.address != None
    return


def test_sendLINK(deploy_contract,oracleGas,load_account1):
    
    contract = deploy_contract

    if interface.LinkTokenInterface(config["networks"][network.show_active()]["link_token"]).balanceOf(contract) > oracleGas:
        pytest.skip("Contract already funded")
    
    else:
        interface.LinkTokenInterface(config["networks"][network.show_active()]["link_token"]).transfer(contract,oracleGas*2,{'from':load_account1})
        assert interface.LinkTokenInterface(config["networks"][network.show_active()]["link_token"]).balanceOf(contract) == oracleGas*2
    
    return


def test_requestWarningLevel(deploy_contract, load_account1):

    contract = deploy_contract
    contract.requestWarningLevel({'from':load_account1})

    time.sleep(35)

    assert contract.warningLevel() is not None

    return


def test_settle(deploy_contract, load_account1, load_account2):
    
    contract = deploy_contract
    contract.settleClaim({'from':load_account1})

    warningLevel = contract.warningLevel()

    if warningLevel < 3:
        assert interface.LinkTokenInterface(config["networks"][network.show_active()]["link_token"]).balanceOf(contract) == 0
        assert interface.LinkTokenInterface(config["networks"][network.show_active()]["link_token"]).balanceOf(load_account2) != 0

    if warningLevel >= 3:
        assert interface.LinkTokenInterface(config["networks"][network.show_active()]["link_token"]).balanceOf(contract) == 0
        assert interface.LinkTokenInterface(config["networks"][network.show_active()]["link_token"]).balanceOf(load_account2) == 0

    return

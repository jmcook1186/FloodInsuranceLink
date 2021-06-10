import pytest

from brownie import (
    LinkToken,
    accounts,
    network,
    config
)


@pytest.fixture(scope='module')
def get_token():
    """
    load deployed contract for FLOOD token
    """
    if network.show_active() == 'kovan':

        floodToken = FloodToken.at('0x63585C9f4968658cB36C48fa33e34BE513c5e4D9')
    
    else:
        pytest.fail('Please test on kovan network')

    return floodToken



@pytest.fixture(scope='module')
def get_contract():
    """
    load deployed insurance contract
    """
    contract = floodInsurance.at('0xE094A61c7e10b5ECbEE6006a1207239d515d1548') 

    return contract



@pytest.fixture(scope='session')
def load_account1():
    """
    load insurer/contract owner account
    """
    account1 = accounts.load('main')

    return account1


@pytest.fixture(scope='session')
def load_account2():
    """
    load customer account
    """
    account2 = accounts.load('account2')

    return account2


@pytest.fixture
def oracleGas():
    """
    define number of LINK required by oracle
    """
    return 10e16 # 0.1 LINK



@pytest.fixture(scope='session')
def set_payout_amount():
    """
    define amount of insurance payout
    NB must match what was defined in contract constructor at deployment
    """
    return 500000e18

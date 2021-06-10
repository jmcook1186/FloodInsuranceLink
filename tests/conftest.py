import pytest

from brownie import (
    LinkToken,
    accounts,
    network,
    config
)

@pytest.fixture(scope='session')
def load_account1():

    account1 = accounts.load('main')

    return account1


@pytest.fixture(scope='session')
def load_account2():

    account2 = accounts.load('account2')

    return account2


@pytest.fixture
def oracleGas():

    return 10e16 # 0.1 LINK




@pytest.fixture(scope='session')
def set_payout_amount():
    return 500000e18

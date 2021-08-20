
#!/usr/bin/python3
from brownie import floodInsurance, accounts, config, network


def main():

    nLINK = 10 # how many LINk to send to contract
    account1 = load_account('main') # load account
    account2 = load_account('account2') # load account2

    deploy_contract(account1, account2, 3)
    fund_contract(nLINK, account1)

    return


def load_account(accountName):

    account = accounts.load(accountName)

    return account


def deploy_contract(account1, account2, warningLevel):

    print("Deploying contract to {} network".format(network.show_active()))
    floodInsurancemvp.deploy('0xff795577d9ac8bd7d90ee22b6c1703490b6512fd',\
        '0x2f90A6D021db21e1B2A077c5a37B3C7E75D15b7e','29fa9aa13bf1468788b7cc4a500a45b8',\
            100000000000000000,'0xa36085F69e2889c224210F603D836748e7dC0088',3,5000e18,{'from':owner})

    return


def fund_contract(nLink, account1):

    # grab most recently deployed contract
    contract = floodInsurancemvp[len(floodInsurancemvp) - 1]

    # make transfer of LINK
    interface.LinkTokenInterface(
        config["networks"][network.show_active()]["link_token"]
    ).transfer(contract, nLink*1e18, {"from": account1})
    
    print("Funded {} with {} LINK".format(contract.address, nLINK))


    return


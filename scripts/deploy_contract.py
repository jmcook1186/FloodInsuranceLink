
#!/usr/bin/python3
from brownie import floodInsurance, accounts, config, network


def main():

    nLINK = 10 # how many LINk to send to contract
    account1 = load_account('main') # load account

    deploy_contract(account1)
    fund_contract(nLINK, account1)

    return


def load_account(accountName):

    account = accounts.load(accountName)

    return account


def deploy_contract(account1):

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
    {'from':account1}
    )
    
    # report
    print("Contract deployed to address: {}".format(floodInsurance[len(floodInsurance) - 1].address))

    return


def fund_contract(nLink, account1):

    # grab most recently deployed contract
    contract = floodInsurance[len(floodInsurance) - 1]

    # make transfer of LINK
    interface.LinkTokenInterface(
        config["networks"][network.show_active()]["link_token"]
    ).transfer(contract, nLink*1e18, {"from": account1})
    
    print("Funded {} with {} LINK".format(contract.address, nLINK))


    return

from brownie import accounts, network, floodInsurance, config, interface

def main():

    
    insurerAccount = accounts.load('main')
    customerAccount = accounts.load('account2')
    contract = floodInsurance[len(floodInsurance)-1]
    print(contract.address)

    hasEnoughLINK(contract)
    requestData(contract, insurerAccount)
    transferFunds(contract, insurerAccount)
    checkBalances(contract, insurerAccount, customerAccount)

    return


def hasEnoughLINK(contract):

    link_address = config["networks"][network.show_active()]["link_token"]
    link_fee = config["networks"][network.show_active()]["fee"]
    balance = interface.LinkTokenInterface(link_address).balanceOf(contract)

    assert balance > link_fee, "Contract cannot pay oracle gas, please send LINK"

    return


def requestData(contract, insurerAccount):
    
    transaction = contract.requestWarningLevel({'from':insurerAccount})

    return 


def transferFunds(contract, insurerAccount):

    contract.settleClaim({'from':insurerAccount})

    return

def checkBalances(contract, insurerAccount, customerAccount):

    link_address = config["networks"][network.show_active()]["link_token"]
    insurerBalance = interface.LinkTokenInterface(link_address).balanceOf(insurerAccount)
    customerBalance = interface.LinkTokenInterface(link_address).balanceOf(customerAccount)
    contractBalance = interface.LinkTokenInterface(link_address).balanceOf(contract)

    print("**BALANCES**")
    print("Contract: {}".format(contractBalance/1e18))
    print("Customer: {}".format(customerBalance/1e18))
    print("Insurer: {}".format(insurerBalance/1e18))

    return
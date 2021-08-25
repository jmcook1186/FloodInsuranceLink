# FloodInsuranceChainlink

This is a repository for a flood insurance protocol using smart contracts. The contract establishes the logic of an agreement between multiple customers and a single insurer (assumed to be the contract owner). Customers are added to the contract by providing their latitude and longitude and elevation above sea level. They then pay a premum of 300 DAI. They can then trigger the contract to make a request to a tide extreme API via a Chainlink oracle. This checks whether the tide extreme has exceeded ther elevation above sea level, represeting  flood. If so, a settlement can be triggered, where a payout of 3000 DAI is made to their account. Otherwise, the payout amount is sent back to the insurer.

Oracle gas is paid in LINK, transaction gas is paid in ETH, and the insurance payout is settled in DAI.

This project is described in detailed walkthroughs at https://tothepoles.co.uk/category/eolink/ although this repo might sometimes be a commit or two ahead of the explanatory posts.

This project started with the [brownie chainlink-mix](https://github.com/smartcontractkit/chainlink-mix).

NB: The chainlink oracle currently directs to dummy json data hosted on my github pages, in lieu of writing a Chainlink external adaptor for stormglass.io.

None of this is intended for deployment anywhere other than a local blockchain or on Kovan - it is a learning tool only and is still under development!


## Prerequisites

Please install or have installed the following:

- [nodejs and npm](https://nodejs.org/en/download/)
- [python](https://www.python.org/downloads/)
- 
## Installation

1. [Install Brownie](https://eth-brownie.readthedocs.io/en/stable/install.html) 

```bash
pip install eth-brownie
```

2. [Install ganache-cli](https://www.npmjs.com/package/ganache-cli)

```bash
npm install -g ganache-cli
```

3. This project deploys to the Kovan testnet. This requires an Infura project ID and your wallet's private key to be provided in a .env file (not 
provided in this git repository).

You can get a `WEB3_INFURA_PROJECT_ID` by getting a free trial of [Infura](https://infura.io/). You can [follow this guide](https://ethereumico.io/knowledge-base/infura-api-key-guide/) to getting a project key. You can find your `PRIVATE_KEY` from your ethereum wallet like [metamask](https://metamask.io/). 

You can add your environment variables to the `.env` file:

```
export WEB3_INFURA_PROJECT_ID=<PROJECT_ID>
export PRIVATE_KEY=<PRIVATE_KEY>

```

4. Your wallet requires Kovan test ETH and test-LINK.
   
   DO NOT USE REAL ASSETS. DO NOT SEND ASSETS FROM A MAINNET WALLET TO A KOVAN ADDRESS. DO NOT USE YOUR MAINNET ACCOUNT IN A DEVELOPMENT ENVIRONMENT.
   
   See instructions [here](https://faucet.kovan.network/) and [here](https://docs.chain.link/docs/acquire-link/)


## Testing

Testing is achieved using pytest in brownie. I have not yet written any mocks, so all tests use the contracts deployed on the Kovan testnet. Fixtures (configuration common to all tests) are defined in conftest.py and unit tests are defined in test_flood_insurance.py. To run the tests from the terminal, navigate to the project folder, then:

```
>>> brownie test --network kovan

```


## Resources

To get started with Brownie:

* [Chainlink Documentation](https://docs.chain.link/docs)
* Check out the [Chainlink documentation](https://docs.chain.link/docs) to get started from any level of smart contract engineering. 
* Check out the other [Brownie mixes](https://github.com/brownie-mix/) that can be used as a starting point for your own contracts. They also provide example code to help you get started.
* ["Getting Started with Brownie"](https://medium.com/@iamdefinitelyahuman/getting-started-with-brownie-part-1-9b2181f4cb99) is a good tutorial to help you familiarize yourself with Brownie.
* For more in-depth information, read the [Brownie documentation](https://eth-brownie.readthedocs.io/en/stable/).

Explainers for this specific repository:
* [www.tothepoles.co.uk](https://tothepoles.co.uk/2021/06/04/eolink-0-1-3-simplified-flood-insurance/)


## License

This project is licensed under the [MIT license](LICENSE).

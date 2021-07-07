# Import dependencies
import json
import os

# Import constants.py
from constants import *

import subprocess

 # import wb3 
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account


# import bit
import bit
from bit.network import NetworkAPI
#from bit import wif_to_key


# instantiate the web3 using the ipaddress of where the ethernet node1 is running i.e. http://127.0.0.1:8545
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# add the middleware to support the PoA algorithm
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

 # Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {}



# Create a function called `derive_wallets`
# inputs :
#   mnemonic : the mnemonic seed phrase to generate the wallets
#   coin : the coin type to generate the wallets for
#   numderive : the number of wallets to generate, used the constant NUMDERIVE (value = 3)
# Output
#   json object with derived addresses/private/public keys for the coin type
def derive_wallets(mnemonic,coin, numderive=NUMDERIVE):

    try:
        # create the coomand string to run
        command = f'php ./derive -g --mnemonic="{mnemonic}" --numderive={numderive} --coin={coin} --cols=path,address,privkey,pubkey --format=json'

        # execute the command  in a new process
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        
        # interact with process, send data to stdif, get data from stdout to output and stderr to err
        output, err = p.communicate()

        # wait Wait for the process to terminate
        p_status = p.wait()

        # return output
        return json.loads(output)
    except Exception as e:
        print(f"ERROR: An error occurred in derive_wallets, details :  {e}")
        raise e



# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
# inputs:
#   coin: the coin type
#   priv_key: the private key string to convert to account
# output: the account of the private key for the con type
def priv_key_to_account(coin, priv_key):
    try:

        # Coin type is ETH
        if coin == ETH:      
            # get the account from the private key using web3               
            account = Account.privateKeyToAccount(priv_key)
        
        # Coin type is BTCTEST
        elif coin == BTCTEST:
            # get the account from the private key using bit
            account = bit.PrivateKeyTestnet(priv_key)


        return account
    except Exception as e:
        print(f"ERROR: An error occurred in priv_key_to_account, details :  {e}")
        raise e

            
             
 
  
# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
# inputs
#   coin:  the coin type
#   account :  the account object from priv_key_to_account, account of sender
#   recipient : string address of the recipient
#   amount : the amount of coin to send in either btc or ether (not Wei)
# output: unsigned transaction  for ETH or  prepared  transaction for BTCTEST
def create_tx(coin, account, recipient, amount):
    try:
        # coin type is ETH
        if coin == ETH:
            # convert ether to wei
            value= Web3.toWei(amount,'ether')
            # get gas estimate
            gasEstimate = w3.eth.estimateGas(
                {"from": account.address, "to": recipient, "value": value}
            )
            # return dict object with transaction  details
            return {
                "from": account.address,
                "to": recipient,
                "value": value,
                "gasPrice": w3.eth.gasPrice,
                "gas": gasEstimate,
                "nonce": w3.eth.getTransactionCount(account.address),
            }
        # coin type is BTCTEST
        elif coin == BTCTEST:
            #  return a prepares transaction
            return bit.PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, BTC)])

    except Exception as e:
        print(f"ERROR: An error occurred in create_tx, details :  {e}")
        raise e


# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
# inputs:
#   coin:  the coin type
#   account :  the account object from priv_key_to_account, account of sender
#   recipient : string address of the recipient
#   amount : the amount of coin to send in either btc or ether (not Wei)
# output: retruns the transaction id
def send_tx(coin, account, recipient, amount):
    try:
        # create the transaction
        raw_tx = create_tx(coin, account, recipient, amount)

        # if coin type ETH
        if coin == ETH:
            # sign the transaction using account key
            signed_tx = account.sign_transaction(raw_tx)
            # breadcast  signed transaction  to the network
            result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            # get the transaction id 
            result = result.hex()

        # coin type is BTCTEST
        elif coin == BTCTEST:
            # sign the transaction using account private key
            signed_tx = account.sign_transaction(raw_tx)
            # broadcast on the network
            NetworkAPI.broadcast_tx_testnet(signed_tx)
            # get the last transaction id
            ''' A potential bug: this sometimes returns the transaction id of the one before the last
            # Bug to fix '''
            result = NetworkAPI.get_transactions_testnet(account.address)[0] 


        # Print the transaction detail, used to verify the transaction
        print("\n")
        print(f"\033[1m Transaction Id:  {result}\033[1m")
        print("-"*90)
        print(f"From: {account.address}")
        print(f"To: {recipient}")
        print(f"Amount: {amount} {coin}")
        print("\n")
        
        # return the transaction Id
        return result
    except Exception as e:
        print(f"ERROR: An error occurred in send_tx, details :  {e}")
        raise e


















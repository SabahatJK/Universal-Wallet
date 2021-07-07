import os
from dotenv import load_dotenv

from constants import *
from wallet import *

def main():
  


    # Load and set environment variables, an .env file expected in the same folder as this py file
    load_dotenv()

    # set the error message to be thrown if mnemonic enviroment variable is not found
    value_not_exists = "mnemonic", "mnemonic does not exist in the .env file"

    # set the mnemonic from the mnemonic env variable 
    mnemonic=os.getenv("mnemonic", value_not_exists)

    if mnemonic == value_not_exists:
        print("Enviroment Variable for mnemonic is not found, please verify your .env file")
        raise KeyError("Enviroment Variable for mnemonic not found, please verify your .env file") 


    try:

        # Derive the wallets for ETH using the mnemonic phase
        coins[ETH] = derive_wallets(mnemonic, ETH)

        # Derive the wallets for BTCTEST using the mnemonic phase
        coins[BTCTEST] = derive_wallets(mnemonic, BTCTEST)

        # Print the wallet for both coin types (ETH & BTCTEST)
        print(f"\033[1m Coin Wallet \033[0m")
        print('-'*30)
        print(json.dumps(coins, indent=4, sort_keys=True))
        print()

        # Create a ethernet testnet account from the private key
        # Send ETH from account to the 3rd Address in the wallet
        # print the last trabsaction id, that is supposedly the current
        
        # amount to send in ether
        eth_amount = 15

        # create the account from the private key from the second address in the wallet
        eth_account = priv_key_to_account(ETH, coins[ETH][1]['privkey'] ) 
        
        # set the address of the recipient, setting it to the 3rd address in the wallet
        eth_recipient = coins[ETH][2]['address']
        
        # send the transaction of eth_amount from the account to the recepient 
        result = send_tx(ETH, eth_account, eth_recipient, eth_amount)
        
        
        # Create a bitcoin testnet account from the private key
        # Send BTC from account to the 3rd Address 
        # print the last trabsaction id, that is supposedly the current
        
        # amount of btc to send 
        btc_amount = 0.00000004

        # create a BTC account from the private key of the first address in the wallet
        btc_test_account = priv_key_to_account(BTCTEST, coins[BTCTEST][0]['privkey'] ) 

        # set the address of the recipient, setting it to the 3rd address in the wallet
        btc_recipient = coins[BTCTEST][2]['address']
        
        # send the transaction of eth_amount from the account to the recepient 
        result = send_tx(BTCTEST, btc_test_account, btc_recipient , btc_amount)
        
        
        print()

    except Exception as e:
        print(f"ERROR: An error occurred, details :  {e}")

if __name__ == "__main__":
    main()


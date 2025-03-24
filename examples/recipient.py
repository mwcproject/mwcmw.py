import os
import requests
from mwc.wallet_v3 import WalletV3


def receive_transaction(wallet: WalletV3, foreign_api_url, slatepack_message):
    """
    Receive a transaction by sending the slatepack message to the foreign API.

    Parameters:
    foreign_api_url (str): URL of the foreign API endpoint.
    slatepack_message (str): Slatepack message received from the sender.

    Returns:
    Response: The response object from the foreign API after processing the transaction.
    """
    # Ensure the foreign API URL is correctly formatted
    if foreign_api_url.endswith('/'):
        foreign_api_url = foreign_api_url + 'v2/foreign'
    else:
        foreign_api_url = foreign_api_url + '/v2/foreign'

    # Prepare the payload for the receive_tx API call
    payload = {
        'jsonrpc': '2.0',
        'id': 0,
        'method': 'receive_tx',
        'params': [slatepack_message, None, None],
    }

    # Decode the initial slate for validation or logging purposes
    _decoded_slate = wallet.decode_slatepack_message(slatepack_message)

    # Make the POST request to the foreign API
    response = requests.post(foreign_api_url, json=payload)

    return response

def get_slatepack_address(wallet: WalletV3, foreign_api_url, slatepack_message):
    """
    Receive a transaction by sending the slatepack message to the foreign API.

    Parameters:
    foreign_api_url (str): URL of the foreign API endpoint.
    slatepack_message (str): Slatepack message received from the sender.

    Returns:
    Response: The response object from the foreign API after processing the transaction.
    """
    # Ensure the foreign API URL is correctly formatted
    if foreign_api_url.endswith('/'):
        foreign_api_url = foreign_api_url + 'v2/foreign'
    else:
        foreign_api_url = foreign_api_url + '/v2/foreign'

    # Prepare the payload for the receive_tx API call
    payload = {
        'jsonrpc': '2.0',
        'id': 0,
        'method': 'receive_tx',
        'params': [slatepack_message, None, None],
    }
    
    # Decode the initial slate for validation or logging purposes
    _decoded_slate = wallet.decode_slatepack_message(slatepack_message)

    # Make the POST request to the foreign API
    response = requests.post(foreign_api_url, json=payload)

    return response


if __name__ == '__main__':
    from pathlib import Path
    import argparse

    # Define wallet and foreign API parameters
    home_directory = str(Path.home())
    owner_api_url = 'http://localhost:3420/v3/owner'
    foreign_api_url = 'http://localhost:3415'
    api_secret_file_path = os.path.join(home_directory, '.mwc/main/.owner_api_secret')
    api_user = 'mwc'
    with open(api_secret_file_path) as api_secret_file:
        api_password = api_secret_file.read().strip()

    # Initialize the wallet
    wallet = WalletV3(owner_api_url, api_user, api_password)
    wallet.init_secure_api()
    wallet_password = input('Enter your wallet password: ')
    wallet.open_wallet(None, wallet_password)
    print(wallet.retrieve_txs())

    # Prompt the user for the slatepack message received from the sender
    #slatepack_from_sender = input('Enter the slatepack message received from the sender: ')

    #try:
    #    # Process the received transaction via the foreign API
    #    response = receive_transaction(foreign_api_url, slatepack_from_sender)
    #    
    #    if response.ok:
    #        print('Transaction successfully received.')
    #        print(f'Response: {response.json()}')
    #    else:
    #        print('Failed to receive transaction.')
    #        print(f'Error: {response.status_code} - {response.text}')
    #except Exception as e:
    #    print(f'Error: {e}')

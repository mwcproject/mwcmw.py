import os
from mwc.wallet_v3 import WalletV3


def initialize_transaction(wallet: WalletV3, amount_micro_mwc, recipient_url, time_to_live_blocks=None):
    """
    Initialize a send transaction using the WalletV3 API.

    Parameters:
    wallet (WalletV3): Wallet object for managing transactions.
    amount_micro_mwc (int): Amount to send in micro-MWC (1 MWC = 1_000_000_000 micro-MWC).
    recipient_url (str): URL of the recipient.
    time_to_live_blocks (int, optional): Time-to-live for the transaction in blockchain blocks.

    Returns:
    tuple: A tuple containing the slate ID and the initial slatepack message, or raises an exception on failure.
    """
    transaction_data = {
        'src_acct_name': None,  # Source account name (None for default account)
        'amount': int(amount_micro_mwc),  # Amount to send in micro-MWC
        'minimum_confirmations': 10,  # Minimum confirmations for inputs
        'max_outputs': 500,  # Maximum number of outputs allowed
        'num_change_outputs': 1,  # Number of change outputs to create
        'selection_strategy_is_use_all': False,  # Use optimal input selection
        'target_slate_version': 4,  # Slate version target
        'payment_proof_recipient_address': None,  # Payment proof recipient address (optional)
        'ttl_blocks': time_to_live_blocks,  # Time-to-live in blocks
        'send_args': None  # Additional send arguments
    }
    slate = wallet.init_send_tx(transaction_data)
    slate_id = slate['id']  # Retrieve the slate ID for tracking
    initial_slatepack_message = wallet.encode_slatepack_message(slate, 'SendInitial', None, 0)
    transaction_locked = wallet.tx_lock_outputs(initial_slatepack_message)
    if transaction_locked:
        return slate_id, initial_slatepack_message
    raise Exception('Transaction locking failed.')


def finalize_transaction(wallet: WalletV3, slatepack_response):
    """
    Finalize the send transaction using the recipient's slatepack response.

    Parameters:
    wallet (WalletV3): Wallet object for managing transactions.
    slatepack_response (str): Slatepack response provided by the recipient.

    Returns:
    tuple: A tuple containing the finalized slate ID and slatepack message, or raises an exception on failure.
    """
    finalized_slate = wallet.finalize_tx(slatepack_response)
    decoded_slatepack = wallet.decode_slatepack_message(finalized_slate)
    slate_id = decoded_slatepack['slate']['id']  # Extract the slate ID for tracking
    transaction = decoded_slatepack['slate']['tx']  # Extract the finalized transaction
    transaction_broadcasted = wallet.post_tx(transaction)
    if transaction_broadcasted:
        print('Transaction successfully broadcasted to the node.')
        return slate_id, finalized_slate
    raise Exception('Transaction broadcast failed.')


if __name__ == '__main__':
    from pathlib import Path
    import argparse
    from decimal import Decimal

    parser = argparse.ArgumentParser(description='Send MWC using HTTP/HTTPS')
    parser.add_argument('amount', metavar='amount', type=str, nargs=1,
                        help='Amount of MWC to send (e.g., 1.23)')
    parser.add_argument('-u', '--url', dest='url', type=str, required=False,
                        help='HTTP/HTTPS URL of the recipient')
    args = parser.parse_args()

    # Convert amount to micro-MWC
    amount_micro_mwc = int(Decimal(args.amount[0]) * int(1_000_000_000))

    # Load wallet credentials
    home_directory = str(Path.home())
    api_url = 'http://localhost:3420/v3/owner'
    api_secret_file_path = os.path.join(home_directory, '.mwc/main/.owner_api_secret')
    api_user = 'mwc'
    with open(api_secret_file_path) as api_secret_file:
        api_password = api_secret_file.read().strip()

    # Initialize wallet
    wallet = WalletV3(api_url, api_user, api_password)
    wallet.init_secure_api()
    wallet_password = input('Enter your wallet password: ')
    wallet.open_wallet(None, wallet_password)

    # Initialize and finalize transaction
    try:
        slate_id, initial_slatepack_message = initialize_transaction(wallet, amount_micro_mwc, args.url)
        print(f'Slate ID: {slate_id}')
        print('Provide this initial slatepack message to the recipient:')
        print(initial_slatepack_message)

        # Get recipient's response and finalize the transaction
        recipient_response = input('Enter the slatepack response from the recipient: ')
        finalized_slate_id, finalized_slatepack = finalize_transaction(wallet, recipient_response)
        print(f'Transaction finalized. Slate ID: {finalized_slate_id}')
    except Exception as e:
        print(f'Error: {e}')

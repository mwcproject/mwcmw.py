import os
from mwc.wallet_v3 import WalletV3
import examples.sender as sender
import examples.recipient as recipient

if __name__ == '__main__':
    from pathlib import Path
    import argparse
    from decimal import Decimal

    def complete_transaction_workflow(sender_wallet, recipient_foreign_api_url, amount_micro_mwc, recipient_address):
        """
        Perform the complete workflow of initializing, receiving, and finalizing a transaction.

        Parameters:
            sender_wallet (WalletV3): Sender's WalletV3 instance.
            recipient_foreign_api_url (str): URL to the recipient's foreign API endpoint.
            amount_micro_mwc (int): Amount to send in micro-MWC (1 MWC = 1_000_000_000 micro-MWC).
            recipient_address (str): The recipient's Slatepack address.

        Returns:
            dict: Finalized transaction details (including slate ID and finalized slatepack).
        """

        # ----------------------------------------------------------------------------
        # SENDER: Initialize the transaction
        # ----------------------------------------------------------------------------
        print("SENDER: Initializing the transaction...")

        # The sender calls 'initialize_transaction', providing the desired amount and
        # the recipient's Slatepack address. This returns the initial Slatepack message
        # that the sender will provide to the recipient.
        slate_id, initial_slatepack = sender.initialize_transaction(
            sender_wallet, amount_micro_mwc, recipient_address
        )
        print(f"SENDER: Transaction initialized with Slate ID: {slate_id}")
        print(f"SENDER: Initial Slatepack Message:\n{initial_slatepack}")
        print("Please send this Slatepack message to the recipient.\n")

        # ----------------------------------------------------------------------------
        # RECIPIENT: Receive the slatepack message
        # ----------------------------------------------------------------------------
        print("RECIPIENT: Receiving the transaction...")

        # The recipient processes the initial Slatepack message and responds
        # with a second Slatepack. In this example, we demonstrate how you'd call
        # 'recipient.receive_transaction' to get that response.
        # The 'recipient_foreign_api_url' should point to the recipient's foreign API.
        response = recipient.receive_transaction(sender_wallet, recipient_foreign_api_url, initial_slatepack)
        if not response.ok:
            raise Exception(f"RECIPIENT: Failed to process the transaction. "
                            f"{response.status_code} - {response.text}")

        # The recipient wallet's response is the updated Slatepack message.
        recipient_slatepack_response = response.json()['result']['Ok']
        print(f"RECIPIENT: Slatepack Response:\n{recipient_slatepack_response}")
        print("The recipient has returned a new Slatepack message.\n")

        # ----------------------------------------------------------------------------
        # SENDER: Finalize the transaction
        # ----------------------------------------------------------------------------
        print("SENDER: Finalizing the transaction...")

        # The sender takes the updated Slatepack response and finalizes it,
        # completing the interactive transaction workflow.
        finalized_slate_id, finalized_slatepack = sender.finalize_transaction(
            sender_wallet,
            recipient_slatepack_response
        )
        print(f"SENDER: Transaction finalized with Slate ID: {finalized_slate_id}")
        print(f"SENDER: Finalized Slatepack Message:\n{finalized_slatepack}")

        # Returning the finalized details can be helpful for logs or additional processing
        return {
            "slate_id": finalized_slate_id,
            "finalized_slatepack": finalized_slatepack,
        }

    # ----------------------------------------------------------------------------
    # Setup for the sender wallet and command line argument parsing
    # ----------------------------------------------------------------------------

    home_directory = str(Path.home())
    owner_api_url = 'http://localhost:3420/v3/owner'
    foreign_api_url = 'http://localhost:3415'
    api_secret_file_path = os.path.join(home_directory, '.mwc/main/.owner_api_secret')
    api_user = 'mwc'

    with open(api_secret_file_path) as api_secret_file:
        api_password = api_secret_file.read().strip()

    # Initialize the sender wallet and open it
    wallet = WalletV3(owner_api_url, api_user, api_password)
    wallet.init_secure_api()
    wallet_password = input('Enter your wallet password: ')
    wallet.open_wallet(None, wallet_password)

    # This is the recipient's Slatepack address, where we send the initial Slatepack.
    # The recipient will then produce a response Slatepack using their own wallet.
    recipient_address = 'grxdcrjcvdq7aipjzuejjngr3til7euryqrpmtjg4hdqxnx3jyfst2qd'

    # Parse command line arguments for the amount of MWC to send
    parser = argparse.ArgumentParser(description='Complete MWC Transaction Workflow')
    parser.add_argument('amount', metavar='amount', type=str, nargs=1,
                        help='Amount of MWC to send (e.g., 1.23)')
    args = parser.parse_args()

    # Convert the amount into micro-MWC (1 MWC = 1_000_000_000 micro-MWC)
    amount_micro_mwc = int(Decimal(args.amount[0]) * int(1_000_000_000))

    # Run the full transaction workflow: init -> receive -> finalize
    try:
        transaction_result = complete_transaction_workflow(
            wallet,
            foreign_api_url,
            amount_micro_mwc,
            recipient_address
        )
        print("Transaction Complete!")
        print(f"Slate ID: {transaction_result['slate_id']}")
        print(f"Finalized Slatepack:\n{transaction_result['finalized_slatepack']}")
    except Exception as e:
        print(f"Error during transaction workflow: {e}")

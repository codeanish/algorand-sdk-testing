import base64
import json
from algosdk.util import microalgos_to_algos
from algosdk.v2client import algod
from algosdk.future.transaction import PaymentTxn, wait_for_confirmation
import settings


def payment_transaction(private_key, my_address, to_address):
    algod_address = settings.ALGOD_URL
    algod_token = settings.API_TOKEN
    headers = {
        "X-API-Key": algod_token,
    }
    algod_client = algod.AlgodClient(algod_token, algod_address, headers)

    account_balance = get_account_balance(algod_client, my_address)
    print(f"Account {my_address} Balance: {account_balance} microAlgos")

    unsigned_txn = create_unsigned_transaction(algod_client, my_address, to_address, 1000000, "Hello World 2")
    signed_txn = unsigned_txn.sign(private_key)
    
    transaction_id = algod_client.send_transaction(signed_txn)
    print(f"Successfully sent transaction with transaction_id {transaction_id}")

    try: 
        confirmed_transaction = wait_for_confirmation(algod_client, transaction_id, 4)
    except Exception as err:
        print(err)
        return

    transaction_info = json.dumps(confirmed_transaction, indent=4)
    print(f"Transaction information {transaction_info}")
    decoded_note = base64.b64decode(confirmed_transaction["txn"]["txn"]["note"]).decode()
    print(f"Decoded note {decoded_note}")

    account_balance = get_account_balance(algod_client, my_address)
    print(f"Account {my_address} Balance: {account_balance} microAlgos")


def get_account_balance(algod_client: algod.AlgodClient, address: str) -> int:
    account_info = algod_client.account_info(address)
    return account_info.get('amount')


def create_unsigned_transaction(algod_client: algod.AlgodClient, from_address: str, to_address: str, amount_of_micro_algos: int, note: str):
    params = algod_client.suggested_params()
    params.flat_fee = True
    params.fee = 1000

    return PaymentTxn(from_address, params, to_address, amount_of_micro_algos, note=note.encode())

if __name__ == "__main__":
    payment_transaction(settings.PRIVATE_KEY, settings.ADDRESS, "HZ57J3K46JIJXILONBBZOHX6BKPXEM2VVXNRFSUED6DKFD5ZD24PMJ3MVA")
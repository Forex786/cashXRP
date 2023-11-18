"""Example of how we can see a transaction that was validated on the ledger"""
from xrpl.clients import JsonRpcClient
from xrpl.models import Ledger, Tx
from xrpl.utils import hex_to_str, str_to_hex
import json

# References
# - https://xrpl.org/look-up-transaction-results.html
# - https://xrpl.org/parallel-networks.html#parallel-networks
# - https://xrpl.org/tx.html

# Create a client to connect to the main network

client = JsonRpcClient("https://s.altnet.rippletest.net:51234/")
##client = JsonRpcClient("https://xrplcluster.com/")


print("==== tx_request")
#tx_request = Tx(transaction="9605FDBC9917A9277AA3DDDB37DB49A2C4E440BFA81E5F3CFFB64A6648895CC6")

user_input = input("Enter transaction: ")
tx_request = Tx(transaction= user_input)

print()
print("====tx_response=========")
tx_response = client.request(tx_request)
print (tx_response)



# NB: pending/failed Tx's will be removed from the Ledger after a few minutes
#     So also check for Tx not found.
# ====tx_response=========
# Response(status=<ResponseStatus.ERROR: 'error'>, result={'error': 'txnNotFound', 
# 'error_code': 29, 'error_message': 'Transaction not found.', 'request': {'binary': False, 
# 'command': 'tx', 'transaction': '1AACD13D49535DE29364E3B1C3BB5A19F4A5E67508E02EC0B22E7FCF2CB42033'}},
#  id=None, type=<ResponseType.RESPONSE: 'response'>)


# extract the transaction status, this is the result of the above Tx submission NOT the 
# status of the actual XRP SEND transaction

print()
print("=== TX status ==")
response_status = tx_response.status
print (f"**{response_status.value}**")
print()

if response_status.value != "error":

    print()
    print("==== tx_result extracted from RESPONSE")

    response_result = tx_response.result
    print (response_result)
    print ()
    #print(f"TransactionResult: {response_data['meta']['TransactionResult']}")
    print(f"Validated?: {response_result['validated']}")

    print(f"Account: {response_result['Account']}")
    print(f"Amount: {response_result['Amount']}")
    print(f"Destination: {response_result['Destination']}")
    print(f"DestinationTag: {response_result['DestinationTag']}")
    print(f"TransactionType: {response_result['TransactionType']}")


    print("====")
    print("====")

    print(f"Memos: {response_result['Memos']}")

    example_list=response_result['Memos']
    memodata = example_list[0]['Memo']['MemoData']
    print(f"myData : {hex_to_str(example_list[0]['Memo']['MemoData'])} ") 
    print(f"myDataType : {hex_to_str(example_list[0]['Memo']['MemoType'])} ") 



    # Access more fields as needed
    print("====")
    print("====")

    ##result = f"(['Account': 'rUxi1XtG7521a8eHH6gzcaMXBE6bCAzjqm', 'Amount': '786000000', 'Destination': 'rLgWybVe8hgY6yNAXCmyxJiobX4b11e6hC', 'DestinationTag': 786702])"
    ##print (json.dumps(result,indent=4))

else:
    print("Transaction not found. SEND_XRP failed.")

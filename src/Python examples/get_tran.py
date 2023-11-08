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

# Create a Ledger request and have the client call it
ledger_request = Ledger(ledger_index="validated", transactions=True)
ledger_response = client.request(ledger_request)
print(ledger_response)

# Extract out transactions from the ledger response
transactions = ledger_response.result["ledger"]["transactions"]

# If there are transactions, we can display the first one
# If there are none (visualized at https://testnet.xrpl.org/), try re running the script
if transactions:
    # Create a Transaction request and have the client call it
    print("====")
    
    print (transactions[0])

    print("==== tx_request")
    tx_request = Tx(transaction="D853DDE0658C3ABB27A26B7EC007108BE64960CAA0618E96273B044B8E1CB1D8")
    print (tx_request)
    print(tx_request.method)
    print(tx_request.transaction)
    print(tx_request.binary)
    print("====tx_response=========")

    tx_response = client.request(tx_request)
    print (tx_response)
    print("====")

    response_data = tx_response.result
    print(f"Account: {response_data['Account']}")
    print(f"Amount: {response_data['Amount']}")
    print(f"Destination: {response_data['Destination']}")
    print(f"DestinationTag: {response_data['DestinationTag']}")
    print(f"TransactionType: {response_data['TransactionType']}")
    print(f"TransactionResult: {response_data['meta']['TransactionResult']}")
    print(f"Validated?: {response_data['validated']}")


    print("====")
    print("====")

    print(f"Memos: {response_data['Memos']}")
    
    example_list=response_data['Memos']
    memodata = example_list[0]['Memo']['MemoData']
    print(f"myData : {hex_to_str(example_list[0]['Memo']['MemoData'])} ") 
    print(f"myDataType : {hex_to_str(example_list[0]['Memo']['MemoType'])} ") 

    print(hex_to_str(memodata))

   

    # Access more fields as needed
    print("====")
    print("====")

    ##result = f"(['Account': 'rUxi1XtG7521a8eHH6gzcaMXBE6bCAzjqm', 'Amount': '786000000', 'Destination': 'rLgWybVe8hgY6yNAXCmyxJiobX4b11e6hC', 'DestinationTag': 786702])"
    ##print (json.dumps(result,indent=4))
else:
    print("No transactions were found on the ledger! run again....")




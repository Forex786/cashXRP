import xrpl
from xrpl.models import Ledger, Tx
from xrpl.utils import hex_to_str, str_to_hex

testnet_url = "https://s.altnet.rippletest.net:51234/"

def get_account(seed):
    """get_account"""
    client = xrpl.clients.JsonRpcClient(testnet_url)
    if (seed == ''): ## create new wallet
        XRP_wallet = xrpl.wallet.generate_faucet_wallet(client)
    else: ## fetch existing wallet
        XRP_wallet = xrpl.wallet.Wallet.from_seed(seed)
    return XRP_wallet

def get_account_info(accountId): ## accountId = public XRPL# address
    """get_account_info"""
    client = xrpl.clients.JsonRpcClient(testnet_url)
    acct_info = xrpl.models.requests.account_info.AccountInfo(
        account=accountId,
        ledger_index="validated"
    )
    response = client.request(acct_info)
    return response.result['account_data']

def send_xrp(seed, amount, destination):
    sending_wallet = xrpl.wallet.Wallet.from_seed(seed)
    client = xrpl.clients.JsonRpcClient(testnet_url)

    d1 = str_to_hex("fromCustomerX")
    d2 = str_to_hex("paymentReceipt")

    mymemo = xrpl.models.transactions.Memo(memo_data=d1, memo_type=d2)

    payment = xrpl.models.transactions.Payment(
        account=sending_wallet.address,
        amount=xrpl.utils.xrp_to_drops(int(amount)),
        destination=destination,
        destination_tag = 786702,  
        memos= [mymemo],
       ## last comma is required here
    )
    try:	
        response = xrpl.transaction.submit_and_wait(payment, client, sending_wallet)	

    except xrpl.transaction.XRPLReliableSubmissionException as e:	
        response = f"Submit failed: {e}"
    return response

def get_tran(transaction_hash):
    client = xrpl.clients.JsonRpcClient(testnet_url)
    ##tx_request = Tx(transaction="4515DEBAB36A2CF88BA730E8585F590CF4D58A025E1A6F67CF9ADC8C4700B82C")
    tx_request = Tx(transaction=transaction_hash)
    tx_response = client.request(tx_request)
    

    if tx_response.is_successful():
        
        response_data = tx_response.result

       ## Tran_Data =  f"[""Account"": {response_data['Account']}" + f",""Amount"": {response_data['Amount']}]"
		## print(f"Account: {response_data['Account']}")
        ## print(f"Amount: {response_data['Amount']}")
        ## print(f"Destination: {response_data['Destination']}")
        ## print(f"DestinationTag: {response_data['DestinationTag']}")
        ## print(f"TransactionType: {response_data['TransactionType']}")
        ## print(f"TransactionResult: {response_data['meta']['TransactionResult']}")
        ## print(f"Validated?: {response_data['validated']}")

        return (tx_response)
    else:
        print(f"Request failed with error: {tx_response.error}")
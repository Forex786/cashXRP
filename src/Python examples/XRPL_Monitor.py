
# start a worker loop to monitor required XRPL addresses for new Tx's
#
#

import ast
from datetime import datetime
import xrpl
from xrpl.utils import hex_to_str, str_to_hex
import asyncio
from threading import Thread
from icecream import ic
import logging
# logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
# logging.debug('This message should go to the log file')
# logging.info('So should this')
# logging.warning('And this, too')
# logging.error('And non-ASCII stuff, too, like Øresund and Malmö')

### my libs
from class_mySQL  import MySQLConnector

class XRPLMonitorThread(Thread):
    """
    A worker thread to watch for new ledger events and pass the info back to
    the main frame to be shown in the UI. Using a thread lets us maintain the
    responsiveness of the UI while doing work in the background.
    """

    Tx_count = 0

    def __init__(self, url ):
        Thread.__init__(self, daemon=True)

        #self.mydb = mydb
        self.url = url
        self.loop = asyncio.new_event_loop()
        #self.loop.set_debug(True)
        self.loop.set_debug(False)

        asyncio.set_event_loop(self.loop)
        
    # this is a default Thread function which is overidden here. It is executed by the Thread.start method.
    def run(self):
        """
        This thread runs a never-ending event-loop that monitors messages coming
        from the XRPL.
        """
        self.loop.run_forever()

    def saveToDB(self, message):
        # TODO: save the following meta data to dB.

        try:
            tx_hash = message["transaction"]["hash"]
                    
            txLedger = message['transaction']['LastLedgerSequence']
            memos = message["transaction"]["Memos"] # list of dictionaries
            Memo = memos[0]  # get the first
            MemoData = hex_to_str(Memo['Memo']['MemoData'])
            MemoType = hex_to_str(Memo['Memo']['MemoType'])
            dTag = message['transaction']['DestinationTag']
            destAcc = message['transaction']['Destination']
            txResult = message["engine_result"]
            ledgerValidated = message["validated"]

            logging.info(f"Saving to dB dTag: {dTag}")
            
           

            # ic(tx_hash,txLedger,MemoType,MemoData,dTag,destAcc )
            
            """
            message['transaction']: {'Account': 'rUxi1XtG7521a8eHH6gzcaMXBE6bCAzjqm',
                        'Amount': '10000',
                        'Destination': 'ra7NXCfrANoLcKJKKWuFFyQMDMNPLfuTFL',
                        'DestinationTag': 1000002,
                        'Fee': '10',
                        'Flags': 0,
                        'LastLedgerSequence': 43356720,
                        'Memos': [{'Memo': {'MemoData': '50726546756E6420637265646974',
                                            'MemoType': '63617368585250'}}],
                        'Sequence': 42376130,
                        'SigningPubKey': 'ED41C26F4C4DF7DC7ADA6DC3C5C33686FDA40F2043FFE55D337EBAEDC3DEAB9F10',
                        'TransactionType': 'Payment',
                        'TxnSignature': 'CD1BF58F6CB45396E18C941A13A9CB42E6BE059084C01CFB7EAF77E0CD8C8C9327AD786EB0D5CA0742E978C3DDD55E931B0ADA20D535BD90579533091D341D08',
                        'date': 754745321,
                        'hash': '12A078DC2465E8CF04509BB9E927D7014527032E8D2E7BD4B5D6F7AFD16D92DD'} 

            """
            
            result = mydb.saveValidatedTx (
                                dTag 		,
                                MemoType 	,
                                MemoData 	,
                                tx_hash 		,
                                destAcc,
                                txLedger 	,
                                txResult 	,
                                ledgerValidated )
            
        except Exception as e:
            ic("SaveToDB:", e)                      

    async def watch_xrpl_account(self, addresses, wallet=None):
        """
        This is the task that opens the connection to the XRPL, then handles
        incoming subscription messages by dispatching them to the appropriate
        part of the GUI.
        """
        self.accounts = addresses
        self.wallet = wallet

        #print (self.accounts[0]," : ", self.accounts[1])

        async with xrpl.asyncio.clients.AsyncWebsocketClient(self.url) as self.client:

            await self.on_connected()
            
            async for message in self.client:
                mtype = message.get("type")
                if mtype == "ledgerClosed":
                    #print("Ledger closed: ", message["ledger_index"])
                    x=1
                elif mtype == "transaction":

                    # message contains the status of the tx & ledger and Tx details
                    print(datetime.now().strftime("%H:%M:%S"),"-",
                          message['transaction']['LastLedgerSequence'],"-",
                          message['transaction']['DestinationTag'],"-",
                          ":",message["engine_result"],
                          ":",message["validated"],
                          message["transaction"]["hash"]
                          )
                    self.Tx_count = self.Tx_count + 1

                    try:
                        self.saveToDB(message)
                    except Exception as e:
                        logging.info(f"Issue saving to dB : tag: {message['transaction']['DestinationTag']}")
                        logging.info(e)
                        ic(e)   
                    

    async def on_connected(self):
        """
        Set up initial subscriptions and print data from the
        ledger on startup. Requires that self.client be connected first.
        """

        # Set up 2 subscriptions: all new ledgers, and any new transactions that
        # affect the chosen account(s).
        response = await self.client.request(xrpl.models.requests.Subscribe(
            streams=["ledger"],
            accounts=self.accounts
        ))
        
        # print(f"\nXRPL subscription results : {response.result} \n")

      
    # -----------  end of class XRPLMonitorThread


async def main():
    # endless loop to allow the background Daemon thread to stay alive in this
    # non-GUI program.
    # This loop emulates the GUI main loop.
    while True:
        print ("\n",datetime.now().strftime("%H:%M:%S"), " : Monitoring the XRPL....total Tx count ==>>", worker.Tx_count)
        print ("\nexecTime   Ledger#    Tx TAG     Tx result  Validated?   Tx HASH\n")
       #        11:37:36 - 43356893 - 1000001 - : tesSUCCESS : True B6F94A2D3D3AEA
        await asyncio.sleep(60)

##########################################################################################################

if __name__ == "__main__":

    logging.basicConfig(filename='XRPL_Monitor.log', encoding='utf-8', level=logging.DEBUG)
    # Truncate the log files
    with open('XRPL_Monitor.log', 'w'):
        pass

    websockets_logger = logging.getLogger("websockets")
    websockets_logger.setLevel(logging.INFO)

    logging.info(f"Daemon - Monitor XRPL Tx's started at , {datetime.now().strftime('%Y:%M:%d %H:%M:%S')} \n\n")

    print ("\n\n\n\n\n **** v1.8 ********  Press CTRL+c to eixt  ************\n")

    print ("Daemon - Monitor XRPL Tx's started at ", datetime.now().strftime("%Y:%M:%d %H:%M:%S"), "\n")

    WS_URL = "wss://s.altnet.rippletest.net:51233" # Testnet
    print("XRPL network : ", WS_URL, "\n")
    
    
    try:
        mydb = MySQLConnector()
        mydb.truncate_Table("Txs_Pending")
        mydb.truncate_Table("Txs_Validated")
        

        # Start background thread for updates from the ledger ------------------
        worker = XRPLMonitorThread(WS_URL) # creates an endless worker loop
        worker.start()

        result = mydb.get_XRPL_Wallets_to_Monitor()

        # Convert the string to a Python list
        accounts_to_monitor = ast.literal_eval(result)

        # create a blank list object
        XRPL_addrs_to_monitor  = []

        # TODO write the list to a dB log table.
        print ("Monitoring XRPL addresses : ")

        i = 0
        for x in accounts_to_monitor:
            i = i + 1
            print (f"{i} : {x[0]} - Wallet ID : {x[1]} - {x[2]}")
            XRPL_addrs_to_monitor.append(x[0])
        
        print("\n")


        # add watch function to the endless loop
        task = asyncio.run_coroutine_threadsafe(worker.watch_xrpl_account(XRPL_addrs_to_monitor), worker.loop)

        # start endless loop on the foreground thread.
        # must be a call to an async function to allow us to use the "await" command
        try:
                asyncio.run(main())
        
        except KeyboardInterrupt:
        # This block will be executed if the user presses Ctrl+C
            mydb.close_connection()
            print ("mySQL dB connection closed.")
    
    except:
        print ("__name__ :  mySQL dB error...")
        mydb.close_connection()
        

# EOF
    

    
 
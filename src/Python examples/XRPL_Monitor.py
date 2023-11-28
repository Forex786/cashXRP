
# start a worker loop to monitor required XRPL addresses for new Tx's
#
#

import ast
from datetime import datetime
import xrpl
import asyncio
from threading import Thread
from class_mySQL  import MySQLConnector

class XRPLMonitorThread(Thread):
    """
    A worker thread to watch for new ledger events and pass the info back to
    the main frame to be shown in the UI. Using a thread lets us maintain the
    responsiveness of the UI while doing work in the background.
    """

    Tx_count = 0

    def __init__(self, url):
        Thread.__init__(self, daemon=True)
      
        self.url = url
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.set_debug(True)

    # this is a default Thread function which is overidden here. It is executed by the Thread.start method.
    def run(self):
        """
        This thread runs a never-ending event-loop that monitors messages coming
        from the XRPL.
        """
        self.loop.run_forever()

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
                          message['transaction']['DestinationTag'],"-",
                          message["transaction"]["hash"], 
                          ":",message["engine_result"],
                          ":",message["validated"]
                          )
                    self.Tx_count = self.Tx_count + 1

                    

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
        print (datetime.now().strftime("%H:%M:%S"), " : Monitoring the XRPL....total Tx count ==>>", worker.Tx_count)
        await asyncio.sleep(60)

##########################################################################################################

if __name__ == "__main__":

    print ("\n **** v1.3 ********  Press CTRL+c to eixt  ************\n")

    print ("Daemon - Monitor XRPL Tx's started at ", datetime.now().strftime("%Y:%M:%d %H:%M:%S"), "\n")

    WS_URL = "wss://s.altnet.rippletest.net:51233" # Testnet
    print("XRPL network : ", WS_URL, "\n")
    
    # Start background thread for updates from the ledger ------------------
    worker = XRPLMonitorThread(WS_URL) # creates an endless worker loop
    worker.start()

    try:
        mydb = MySQLConnector()

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
        print ("mySQL dB error...")
        mydb.close_connection()
        

# EOF
    

    
 
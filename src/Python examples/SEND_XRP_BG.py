
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

    

    def __init__(self, url):
        Thread.__init__(self, daemon=True)
      
        self.url = url
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.set_debug(True)
        self.loop.set_debug(False)


        self.Tx_count = 0
        self.loopCount = 10

    # this is a default Thread function which is overidden here. It is executed by the Thread.start method.
    def run(self):
        """
        This thread runs a never-ending event-loop that monitors messages coming
        from the XRPL.
        """
        self.loop.run_forever()

    async def openXRPL_AsyncWebsocketClient(self):
        """
        This is the task that opens the connection to the XRPL.
        """
        async with xrpl.asyncio.clients.AsyncWebsocketClient(self.url) as self.client:
                        
            async for message in self.client:
                x=1

    def openDB_connection(self):
        dbConn = MySQLConnector()
        return dbConn

    def closeDB_connection(self):
        self.txDB.close_connection()


    def getSendTransFromDB(self): # returns a list of XRPL seeds for now

        result = self.txDB.get_allocated_PTS_Wallets(79)
        
        # Convert the string to a Python list
        myPTS_wallets = ast.literal_eval(result)
        
        return myPTS_wallets                                  

    async def send_xrp(self):
        
        waitSecs = 5
   
        print("\nWaiting ",waitSecs," secs for XRPL Async-Web connection to initialise.")
        await asyncio.sleep(waitSecs)
        print("SEND XRP loop started.... loop count = ",self.loopCount)

        self.txDB = self.openDB_connection()
        myTxs = self.getSendTransFromDB()
        print ("Trans list: ", myTxs)
        self.closeDB_connection()


        # JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
        # self.client = xrpl.clients.JsonRpcClient(JSON_RPC_URL)

        mySeed = "sEdVsHGvgKtVGX3ntj2CggKg44HewEM"

        #Check if it's a valid seed
        seed_bytes, alg = xrpl.core.addresscodec.decode_seed(mySeed)
        wallet = xrpl.wallet.Wallet.from_seed(seed=mySeed)        
        sender_account = wallet.address
        # print("\naccount: = ",sender_account)

        
        while True:
            await asyncio.sleep(5)
            print("..............auto send XRP loop..............")

            #try:
            for i in range(self.loopCount):
                self.Tx_count = self.Tx_count + 1
                dTag = 7020000 + self.Tx_count

                tx = xrpl.models.transactions.Payment(
                            account=sender_account,
                            destination= "ra7NXCfrANoLcKJKKWuFFyQMDMNPLfuTFL",
                            amount=xrpl.utils.xrp_to_drops(0.0702),
                            destination_tag= dTag
                            )

                #print ("\n\n Start : ", datetime.now().strftime("%H:%M:%S"))
                tx_signed = await xrpl.asyncio.transaction.autofill_and_sign(tx, self.client, wallet)
                
                ## The transaction hash is created using the contents of the signed transaction
                tx_hash = tx_signed.get_hash()
                ## print(tx_hash)
            
                ## TODO 
                txSeq = getattr(tx_signed, "sequence")
                
                print (f"{self.Tx_count} - Pending dTag: {dTag}, Tx hash: {tx_hash}")
                
                await xrpl.asyncio.transaction.submit(tx_signed, self.client)

                # eond of for i in range(
                #   
            #except Exception as err:
            #    print(err)

        print ("\nSend XRP finished.....\n")
      
    # -----------  end of class XRPLMonitorThread


async def main():
    # endless loop to allow the background Daemon thread to stay alive in this
    # non-GUI program.
    # This loop emulates the GUI main loop.
    while True:
        print ("\n",datetime.now().strftime("%H:%M:%S"), " : cashXRP MAIN loop running ....total Tx count ==>>", worker.Tx_count)
        await asyncio.sleep(60)

##########################################################################################################

if __name__ == "__main__":

    print ("\n **** v0.1 ********  Press CTRL+c twice to eixt  ************\n")

    print ("Daemon - SEND XRPL Tx's started at ", datetime.now().strftime("%Y:%M:%d %H:%M:%S"), "\n")

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
        task = asyncio.run_coroutine_threadsafe(worker.openXRPL_AsyncWebsocketClient(), worker.loop)
        
        # There is a SLEEP in this function which gives the above time to connect
        task = asyncio.run_coroutine_threadsafe(worker.send_xrp(), worker.loop)


        # start endless loop on the foreground thread.
        # must be a call to an async function to allow us to use the "await" command
        try:
                asyncio.run(main())
        
        except KeyboardInterrupt:
        # This block will be executed if the user presses Ctrl+C
            mydb.close_connection()
            print ("\n\n\nmySQL dB connection closed.")
    
    except:
        print ("\n\nmySQL dB error....")
        mydb.close_connection()
        print ("\n\n\nmySQL dB connection closed.")
        

# EOF
    

    
 


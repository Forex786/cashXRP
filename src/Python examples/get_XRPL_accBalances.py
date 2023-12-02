
# start a worker loop to monitor required XRPL addresses for new Tx's
#
#
from icecream import ic
import ast
from datetime import datetime
import getpass
import random
import xrpl
import asyncio
from threading import Thread
from class_mySQL  import MySQLConnector
from AES_cypher import decrypt, hex_to_iv

class XRPL_Thread(Thread):
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


    async def xFn(self) :

        await asyncio.sleep(5) # wait for AsyncWeb connector

        mydb = MySQLConnector()

        result = mydb.get_XRPL_Wallets_to_Monitor()

        # Convert the string to a Python list
        PTS_wallets = ast.literal_eval(result)

        i = 0
        for x in PTS_wallets:
            i = i + 1
            #ic (f"{i} : {x[0]} - Wallet ID : {x[1]} - {x[2]}")
            result = await self.get_XRPL_account_info(x[0])
            
            print(x[1],x[2], " : ",result['Account'], " : ", xrpl.utils.drops_to_xrp((result['Balance'])) )
            #ic(result['Account'])
            #ic(xrpl.utils.drops_to_xrp((result['Balance']) ))
        
        # the recipient wallet
        result = await self.get_XRPL_account_info('ra7NXCfrANoLcKJKKWuFFyQMDMNPLfuTFL')
        print("Recipeint : ",result['Account'], " : ", xrpl.utils.drops_to_xrp((result['Balance'])) )
        

        mydb.close_connection
          
    async def get_XRPL_account_info(self, accountId): ## accountId = public XRPL# address
        """get_account_info"""
                
        #client = xrpl.clients.JsonRpcClient(WS_URL)
        acct_info = xrpl.models.requests.account_info.AccountInfo(
            account=accountId,
            ledger_index="validated"
        )
        response = await self.client.request(acct_info)

        return response.result['account_data']
    # -----------  end of class XRPLMonitorThread


              
      

async def main():
    # endless loop to allow the background Daemon thread to stay alive in this
    # non-GUI program.
    # This loop emulates the GUI main loop.
    cnt = 1
    while True:
        print ("\n",datetime.now().strftime("%H:%M:%S"), 
               " : ",cnt, "/ 5. Get Account Balances main loop running ...CTRL+C to exit.\n")
        await asyncio.sleep(5)
        
        if (cnt > 5):
            print(f"\nMain loop stopped. {cnt} / 5.")
            break
        cnt += 1
    

##########################################################################################################

if __name__ == "__main__":

    print ("\n **** v0.1 ********  Takes a few seconds to complete  ************\n")

    WS_URL = "wss://s.altnet.rippletest.net:51233" # Testnet
    print("XRPL network : ", WS_URL, "\n")
    
   
    # Start background thread for updates from the ledger ------------------
    worker = XRPL_Thread(WS_URL) # creates an endless worker loop
    worker.start()

     # remove from RAM to obfuscate location
    seed_password ="xxxxxxx"

    # Open AsybcWeb connection and keep open within the secondary thread as it is the only one
    # that will execute XRPL Tx's.
    task = asyncio.run_coroutine_threadsafe(worker.openXRPL_AsyncWebsocketClient(), worker.loop)
    task = asyncio.run_coroutine_threadsafe(worker.xFn(), worker.loop)
   
    asyncio.run(main())    

# EOF
    
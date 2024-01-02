from random import randint
import sys
from icecream import ic
from pathlib import Path
from time import sleep
import qrcode

from fastapi import FastAPI, Form, Request,  HTTPException, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse


## my import files
from class_mySQL  import MySQLConnector
from class_XRPL_Thread import *


# get Python version
version = f"{sys.version_info.major}.{sys.version_info.minor}"

mydb = MySQLConnector("Docker")
WS_URL = "wss://s.altnet.rippletest.net:51233" # Testnet

UvicornInstanceID = os.getpid()

######### main.py for Gunicorn + Uvicorn  ##########

app = FastAPI()  ## NB: the "app" will be executed by gunicorn by creating multiple worker threads
                 ##     See "start.sh" file in the root folder of the Docker container.



# Setup folder fop all static HTML files
app.mount("/HTML", StaticFiles(directory="HTML"), name="HTML")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    i = 1
    while i < 5:
        # data = await websocket.receive_text()
        data2 = mydb.get_DashboardDataX(2)
        ic(data2)
        await websocket.send_text(f"Data from mySQL : {i} : {data2}")
        i += 1

# Create a MySQL connection on application startup and
@app.on_event("startup")
def startup_event():

    mydb = MySQLConnector("Docker")

    ic()    
    ic("\n\n\nXRPL network : ", WS_URL, "\n")

    # seed_password ="cashXRP1234567890123456789012345"

    # TODO store hash of master password and chck to confirm it is correct before continuing.
    seed_password = getMasterAESpw()
    # ic("\npw from file = ",seed_password,"\n\n")
    ic(UvicornInstanceID)

    
    
        
def getMasterAESpw():
    # Open the file in read mode
    with open('master.txt', 'r') as file:
        # Read the first line (string) from the file
        first_string = file.readline().strip()

    return first_string

def createPrefundRequest(clientID, amount):
    pass
    # get a random prefund wallet address
    instanceID = randint(1,4)
    prefundWallet = mydb.get_Prefund_Wallet(instanceID)
    # Convert the string to a list
    prefundWalletAddress = ast.literal_eval(prefundWallet)[0][0]

    # create prefund Tx
    prefundTAG = mydb.Insert_Prefund_Deposit(clientID, amount, prefundWalletAddress)

    print(f"createPrefundRequest - preFundTAG = {prefundTAG}")
                
    return prefundWalletAddress, prefundTAG        
    return f"Deposit XRP : {amount} To wallet :{prefundWalletAddress} with dTAG : {prefundTAG}"


    # Create notification

    # create page with prefund details

    # return page details

    # client will make the deposit using personal wallet with the TAG provided.
    # Monitor process will retrieve and save the successful transaction to the Validated table.
    # checkfor validated Txs process will check for TAG and update the client balance.

##########NB: APIs are CASE-Sensative #########################

@app.get("/XRPLWallets") 
async def getXRPLWallets():
        
    result = mydb.get_XRPL_Wallets_to_Monitor()
    #result = mydb.get_allocated_PTS_Wallets(1)

    # data = "[ ['rUxi1XtG7521a8eHH6gzcaMXBE6bCAzjqm','60','PTS'],['rLgWybVe8hgY6yNAXCmyxJiobX4b11e6hC','61','PTS'],['rUBfUoui7NM9DzVy1a3MeLAAG8s7H2Thch','62','PTS'],['rNQYFraewsTkwGfqgMrge8BKfuPQSTpkRQ','63','PTS'],['rN83LHwVmcsqemMKPn1JtU4RE8X8vrmf6w','64','PTS'],['rhdTM26R35VFqdRrP8VxVXd9QX5Y3H7P9P','65','PTS'],['r9sKhbztWrwR5ntwzU4ZABcohMyCbCdpZb','66','PTS'],['rNheBTyXLneWo3Z5VtCzgKA6dLXbS9AMkC','67','PTS'],['r4UrRzyiPGTTxQRaenZWPdzoKiGYUWMtLj','68','PreFund'] ]"

    data = result
    # Convert the string to a list
    wallets_list = ast.literal_eval(data)


    html_table ='<!DOCTYPE html><html lang="en"> <head>     <meta charset="UTF-8">     <meta name="viewport" content="width=device-width, initial-scale=1.0">     <title>cashXRP</title> </head> <body> '
    html_table += '<h1>cashXRP</h1>     <nav>        <ul>' \
            '<li><a href="HTML/home.html">Home</a></li>' \
            '<li><a href="HTML/send.html">Send XRP</a></li>' \
            '<li><a href="HTML/PrefundDeposit.html">Make a Prefund deposit</a></li>'  \
            '<li><a href="http://localhost:1234/XRPLWallets">Show Wallets</a></li>' \
        '</ul>     </nav>'
    
    # Generate HTML table
    html_table += "<table border='1'>\n  <tr>\n    <th>Wallet</th>\n    <th>Number</th>\n    <th>Type</th>\n  </tr>\n"

    for wallet in wallets_list:
        html_table += f"  <tr>\n    <td>{wallet[0]}</td>\n    <td>{wallet[1]}</td>\n    <td>{wallet[2]}</td>\n  </tr>\n"

    html_table += "</table>"

    html_table += '</body></html>'

    return HTMLResponse(html_table)
    

    return {"Monitor wallets":result}

def send_Tx(memo, senderID, amount, xDelay):
    
        #walletID = randint(60, 65)
        instanceID = randint(1,8)


        # assign the allocated wallet to the instance
        x=0
        walletID = 0
        for i in range (60,67 + 1): # note top end of RANGE is not included.
            x += 1
            if x == instanceID:
                walletID =  i 

        exec_time_plus = xDelay

        resultSQL = mydb.Insert_SpendXRPTxs(instanceID, 'test', senderID, amount,'XRPL Direct', 0 , exec_time_plus , 'receiver ID'
                                        ,'ra7NXCfrANoLcKJKKWuFFyQMDMNPLfuTFL'
                                        ,'testMEMO' , memo
                                        ,walletID,  99900000 + UvicornInstanceID) # tag is overwritten @ SEND Pending
        #  print (i, resultSQL) # this is a string


@app.get("/sendXRP") 
async def send_cashXRP(memo, senderID, amount, receiver, xDelay):

    
    print(f"Hello from API send_xrp - sender: {memo} - procID: {str(UvicornInstanceID)}\n")

    send_Tx(memo +" : "+ str(UvicornInstanceID), senderID, amount, xDelay)

    # senderID = 'Uvicorn processID :'
    # amount = 0.001  
    # end_Tx(senderID + str(UvicornInstanceID), amount, xDelay)

    # return {"Transaction submitted to cashXRP PTS"}
    return RedirectResponse("http://localhost:1234/HTML/send.html")


def generateQR_HTMLPage(amount, prefundWalletAddress, prefundTAG, cleintID):
    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # NOTE: no spaces allowed after the '\' continuation character
    HTMLString = '<h1>cashXRP</h1>     <nav>        <ul>' \
            '<li><a href="../home.html">Home</a></li>' \
            '<li><a href="../send.html">Send XRP</a></li>' \
            '<li><a href="../PrefundDeposit.html">Make a Prefund deposit</a></li>' \
            '<li><a href="http://localhost:1234/XRPLWallets">Show Wallets</a></li>' \
            '</ul>     </nav>'

#    '<li><a href="HTML/PrefundDeposit.html">Make a Prefund deposit</a></li>' \   

    HTMLString +=    f"<h1>Deposit XRP : {amount}</h1> \n" \
                    f"<h1>To wallet :{prefundWalletAddress}</h1> \n" \
                    f"<h1>with dTAG : {prefundTAG}</h1> \n"
    
    qrData = f"[{cleintID},{amount},{prefundWalletAddress},{prefundTAG}]"

    filename=f'HTML/QR_Codes/qrcode{cleintID}.html'
    
    # Add data to the QR code
    qr.add_data(qrData)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image to a file
    
    imgFilename = f"qrcode{cleintID}.png"
    img.save(f'HTML/QR_Codes/{imgFilename}') # over writes the existing image


    # Generate HTML content
    html_content = f"""
    <html>
    <head>
        <title>QR Code Generator</title>
    </head>
    <body>
        {HTMLString}
        <h2>Use QR code below in your cashXRP Wallet</h2>
        
        <img src="{imgFilename}" alt="QR Code">
    </body>
    </html>
    """

    # Save HTML content to a file
    with open(filename, 'w') as html_file:
        html_file.write(html_content)

    return filename

@app.get("/prefund") 
async def prefundAccount(clientID, amount):

    
    print(f"Hello from API prefundAccount clientID: {clientID} - amount: {str(amount)}\n")

    prefundWalletAddress, prefundTAG  = createPrefundRequest(clientID, amount) 
    
    outFilename = generateQR_HTMLPage(amount, prefundWalletAddress , prefundTAG, clientID)

    # return prefundResponse
    
    return RedirectResponse(f"http://localhost:1234/{outFilename}")
    # return RedirectResponse("http://localhost:1234/HTML/{prefundResponse}")



@app.get("/")
async def read_root():

    file_path = Path("HTML/index.html")  # Adjust the path based on your project structure
    return FileResponse(file_path)

    # message = f"Hello cashXRP ! From FastAPI + mySQLconnector : running on Uvicorn with Gunicorn. Using Python {version}"
    # return {"message": message}


# Close the MySQL connection on application shutdown
@app.on_event("shutdown")
async def shutdown_event():
    mydb.close_connection()

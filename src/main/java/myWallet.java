import io.xpring.xrpl.Wallet;
import io.xpring.xrpl.WalletGenerationResult;
import io.xpring.xrpl.XrpClient;
import io.xpring.xrpl.XrpException;
import io.xpring.common.XrplNetwork;

import java.math.BigInteger;

public class myWallet  {

    // this class creates a wallet on the test net.
    // allows you to
    //  0. create a new random wallet
    //  1. get wallet balance
    //  2. get wallet details
    //  3. send XRP


    static String publicKey = "blank";
    private Wallet wallet ;

    private String grpcURL = "test.xrp.xpring.io:50051"; // Testnet URL, use main.xrp.xpring.io:50051 for Mainnet
    private XrpClient xrpClient = new XrpClient(grpcURL, XrplNetwork.TEST);

    public void CreateNewWallet() throws XrpException {


        // Generate a random wallet.
        //WalletGenerationResult generationResult = Wallet.generateRandomWallet();
        //Wallet newWallet = generationResult.getWallet();
        //publicKey = newWallet.getAddress();

        wallet = new Wallet("snuSwr8EeTxfUdqRabpnH4mB2L9vE", true);
        publicKey = wallet.getAddress(); // "T7kKFfV3iW8sweVAsTez2GKjRzsU6GJTdhsNg4ojNuQRhUz";


    } // CreateNewWallet


    public String getPublicAddress() {

        return publicKey;

    } // getPublicKey

    public String getBalance() throws XrpException {



        //String address = "X7u4MQVhU2YxS4P9fWzQjnNuDRUkP3GM6kiVjTjcQgUU3Jr"; // ripple test wallet
        //String address = "T7kKFfV3iW8sweVAsTez2GKjRzsU6GJTdhsNg4ojNuQRhUz"; // my test wallet

        BigInteger balance = null;

        balance = xrpClient.getBalance(publicKey);


        return balance.toString();
    }


    public String sendXRP( int amount)  {
        // Destination address.
        String destinationAddress = "T7FtmWeshYay1t9kPKjBdhzogijYt6vPevoxs3y9rKKZ6tC";

        try {
           // String transactionHash = xrpClient.send(BigInteger.valueOf(amount), destinationAddress, wallet);
            String transactionHash = xrpClient.send(BigInteger.valueOf(amount), destinationAddress, wallet);

            return transactionHash;
        } catch (XrpException e) {
            e.printStackTrace();
            return "failed";
        }

    }

    public boolean signWallet (String message) {

        String signature = null;
        try {
            signature = wallet.sign(message);
        } catch (XrpException e) {
            e.printStackTrace();
            return false;
        }

        wallet.verify(message, signature); // true
        return true;

    } // signWallet

} // class



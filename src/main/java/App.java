import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.math.BigInteger;
import java.text.SimpleDateFormat;
import java.util.Date;

import io.xpring.common.XrplNetwork;
import io.xpring.xrpl.XrpClient;
import io.xpring.xrpl.XrpException;

public class App {


    private JButton b_send;
    private JPanel panelMain;
    private JTextArea textArea1;
    private JTextField tf_3;
    private JTextField tf_2;
    private JTextField tf_1;
    private JTextArea textArea2;
    private JButton b_TestWalletBalance;
    private JPanel mainJPanel;
    private JButton b_NewWallet;
    private JButton b_GetAddress;
    private JButton b_GetBalance;
    private JTextField tf_amountTextField;
    private JButton b_sign;
    private JButton button2;
    private JButton button3;
    private JButton button4;

    public myWallet wallet = new myWallet();;

    public static void main(String[] args)
    {
        JFrame frame = new JFrame("App");
        frame.setContentPane(new App().mainJPanel);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.pack();
        frame.setVisible(true);

    } // main

    public App() {

        b_send.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {

                int amount2Send;

                String xx = tf_amountTextField.getText();



                try {
                    amount2Send = Integer.parseInt(tf_amountTextField.getText());
                }
                catch (NumberFormatException ex)
                {
                    amount2Send = 0;
                }


                textArea1.setText( wallet.sendXRP( amount2Send ) );

            }
        });
        b_TestWalletBalance.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {

                String timeStamp = new SimpleDateFormat("HH.mm.ss").format(new Date());

                String grpcURL = "test.xrp.xpring.io:50051"; // Testnet URL, use main.xrp.xpring.io:50051 for Mainnet
                XrpClient xrpClient = new XrpClient(grpcURL, XrplNetwork.TEST);

                String address = "T7FtmWeshYay1t9kPKjBdhzogijYt6vPevoxs3y9rKKZ6tC";

                // rfKE1EZCWFWeQr27jdc2Aza7MyEY5AvNvX
                // bithomp.com/explorer


                BigInteger testBalance = null;
                try {
                    testBalance = xrpClient.getBalance(address);
                } catch (XrpException xrpException) {
                    xrpException.printStackTrace();
                }


                // JOptionPane.showMessageDialog(null,"XRP drops :"+ balance );
                textArea2.setText(textArea2.getText()+"\r\n"+ timeStamp + " - "+ testBalance);




            }
        });
        b_NewWallet.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                wallet = new myWallet();
                try {
                    wallet.CreateNewWallet();
                } catch (XrpException xrpException) {
                    xrpException.printStackTrace();
                }
                tf_1.setText("Open wallet # : "+wallet.getPublicAddress());

                b_GetAddress.setEnabled(true);
                b_GetBalance.setEnabled(true);
                b_send.setEnabled(true);
            }
        });
        b_GetAddress.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                tf_2.setText(wallet.getPublicAddress());
            }
        });
        b_GetBalance.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {



                // JOptionPane.showMessageDialog(null,"XRP drops :"+ balance );
                try {
                    tf_3.setText("My Balance in XRP drops :"+wallet.getBalance());
                } catch (XrpException xrpException) {
                    xrpException.printStackTrace();
                }

            }
        });
        b_sign.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {

                if (wallet.signWallet("AzharKhanSign") ) {
                    textArea1.setText("Wallet signed successfully...");
                } else {
                    textArea1.setText("FAILED to sign wallet...");
                }

            }
        });
    }



}

import myaccount from "./create-account.js";
import dotenv from "dotenv";
dotenv.config();

// Great, your first account is funded, now let's try send a transaction!

// First we have to initilize our sdk.  We need some way to interact with the test network and an easy way to do that
// is throgh a third party, in this case that is purestake.
// Make an account at https://developer.purestake.io/.  

const algosdk = require('algosdk');
const baseServer = 'https://testnet-algorand.api.purestake.io/ps2'
const port = '';
const token = {
    'X-API-Key': 'YOUR API KEY'
}

const algoclient = new algosdk.Algodv2(token, baseServer, port);

(async () => {
    try {
        let params = await algoclient.getTransactionParams().do();
        // comment out the next two lines to use suggested fee
        // params.fee = algosdk.ALGORAND_MIN_TX_FEE;
        // params.flatFee = true;

        // reciever will be some random address, these tokens are worth nothing, this is just for testing purposes

        const receiver = "HZ57J3K46JIJXILONBBZOHX6BKPXEM2VVXNRFSUED6DKFD5ZD24PMJ3MVA";
        const enc = new TextEncoder();
        const note = enc.encode("My first transaction on Algo!");
        let amount = 1000000; // equals 1 ALGO
        let sender = myaccount.addr;

        let txn = algosdk.makePaymentTxnWithSuggestedParamsFromObject({
            from: sender, 
            to: receiver, 
            amount: amount, 
            node: note, 
            suggestedParams: params
        });
    } catch (err) {
      console.error("Failed to get apps from the sdk", err);
      process.exit(1);
    }
  })()






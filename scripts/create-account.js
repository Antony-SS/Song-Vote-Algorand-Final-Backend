
import algosdk from "algosdk"
// Here we are creating an account - save the account address and mnemonic somwhere in your notes.
// We will be using it several times to send transactions, deploy, and test our smart contracts
// Make sure to fund your 

const myaccount = algosdk.generateAccount();
console.log("Account created. Save address & Mnemonic!");
console.log("Account Address = " + myaccount.addr);
let account_mnemonic = algosdk.secretKeyToMnemonic(myaccount.sk);
console.log("Account Mnemonic = "+ account_mnemonic);

export default myaccount;
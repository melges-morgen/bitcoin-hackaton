import "babel-polyfill";
import bitcore from "bitcore-lib";

class Wallet {
  constructor({ pKey, destinationAddress, amount }) {
    this.pKey = new bitcore.PrivateKey(pKey);
    this.address = this.pKey.toAddress(bitcore.Networks.testnet);
    this.amount = amount;
    this.destinationAddress = destinationAddress;
    this.txApiUrl = "https://test-insight.bitpay.com/api/addr/{{addr}}/utxo".replace(
      /{{addr}}/,
      this.address.toString()
    );
    this.script = bitcore.Script.buildPublicKeyHashOut(this.destinationAddress);
    this.utxo = [];
    this.transaction = new bitcore.Transaction(bitcore.Networks.testnet);
  }

  async formTransaction() {
    await this.getTx();
    // await this.utxo.forEach(utxo => {
    //   this.transaction = this.transaction.from(utxo);
    // });
    const utxo = {
        txId: "47ab7e63cd24aaa91bfa20f193e2d3bed35839a08eb1062479f49de39a881503",
        outputIndex: 0,
        address: "mmZW3aHQ5PULPv7G3Gwb8t3SG3GLPEwbbY",
        script: "DUP HASH160 PUSHDATA(20)[424c172a419e4bd1773649bae2ffac8fa712651e] EQUALVERIFY CHECKSIG",
        amount: 82410240
    }
    this.transaction.from(utxo);
    await this.transaction.to(this.destinationAddress, this.amount).sign(this.pKey);
    await this.transaction.change(this.address);
    // console.log(this.transaction.serialize({disableIsFullySigned: true}));
    console.log(this.transaction.serialize());
  }

  async getTx() {
    const transactions = await fetch(this.txApiUrl)
      .then(response => response.json())
      .then(transactions => transactions)
      .catch(err => console.err(err));
    transactions.forEach(t => {      
      this.utxo.push({
        txId: t.txid,
        outputIndex: t.vout,
        address: t.address,
        script: t.scriptPubKey,
        satoshis: t.satoshis
      });
    });
    console.log(this.utxo);
  }
}

window.onload = () => {
  const destinationAddress = "mmZW3aHQ5PULPv7G3Gwb8t3SG3GLPEwbbY";
  const amount = 5000;
  const wallet = new Wallet({
    pKey: "cRJLFES5NSkLAXYP9CDviTpYw4o6M2nMw1SxKChuXLjiPt7zAvut",
    destinationAddress,
    amount
  });
  wallet.formTransaction();
};

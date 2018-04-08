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
    this.transaction.from(this.utxo, this.address);
    this.transaction.to(this.destinationAddress, this.amount).sign(this.pKey);
    this.transaction.change(this.address);
    return this.transaction.serialize({ disableIsFullySigned: true });
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
        script: bitcore.Script.buildPublicKeyHashOut(this.address).toString(),
        satoshis: t.satoshis
      });
    });
    console.log(this.utxo);
  }
}

// window.onload = () => {
//   const destinationAddress = "mmZW3aHQ5PULPv7G3Gwb8t3SG3GLPEwbbY";
//   const amount = 5000;
//   const wallet = new Wallet({
//     pKey: "cVJYN2BKqEHAKZQNZUocVYJT2Aee5TTTo8Ke7Yu5Qno6jRmEfsUu",
//     destinationAddress,
//     amount
//   });
//   wallet.formTransaction();
// };

window.Wallet = Wallet;
export default Wallet;
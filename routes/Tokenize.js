import { TezosToolkit } from "@taquito/taquito";
import { InMemorySigner } from "@taquito/signer";
import { validateAddress } from "@taquito/utils";
import express from "express";
const TokenizeRouter = express.Router();
TokenizeRouter.use(express.json());
const contractAddress = "KT1X6UZJwYHvZnwGJGi1g22fXJdHTRk5mEp4";

TokenizeRouter.route("/").post(async (req, res, next) => {
  console.log(req.body);
  try {
    let Tezos = new TezosToolkit("https://granadanet.api.tez.ie");
    Tezos.setProvider({
      signer: await InMemorySigner.fromSecretKey(process.env.PRIVATE_KEY),
    });
    const addressList = req.body.address;
    const firstValidAddress = addressList.filter((address) => {
      const valid = validateAddress(address);
      if (valid === 3) return true;
    });
    console.log(firstValidAddress);
    if (firstValidAddress.length === 0)
      res.send({ success: false, message: "Invalid addresses" });
    else {
      const contract = await Tezos.contract.at(contractAddress);
      const op = await contract.methods
        .default(firstValidAddress[0], req.body.tweet, req.body.tweetId)
        .send();
      console.log(`Awaiting confirmations for Txn hash ${op.hash}.`);
      const opres = await op.confirmation(3);
      console.log(`Operation injected: https://granada.tzstats.com/${opres}`);
      res.send({ success: true, message: op.hash });
    }
  } catch (err) {
    res.send({
      success: false,
      message: err,
    });
    next(err);
  }
});

export default TokenizeRouter;

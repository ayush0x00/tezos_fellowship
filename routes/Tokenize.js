import { TezosToolkit } from "@taquito/taquito";
import { InMemorySigner } from "@taquito/signer";
import bodyParser from "body-parser";
import express from "express";
const TokenizeRouter = express.Router();
TokenizeRouter.use(express.json());

TokenizeRouter.route("/").post(async (req, res, next) => {
  console.log(req);
  try {
    let Tezos = new TezosToolkit("https://granadanet.api.tez.ie");
    Tezos.setProvider({
      signer: await InMemorySigner.fromSecretKey(process.env.PRIVATE_KEY),
    });
    const contractAddress = "KT1ELJFbe1fjsAqRMbwKVS51kp3ZpBmSCpKP";
    const contract = await Tezos.contract.at(contractAddress);
    const op = await contract.methods
      .default(req.body.address, req.body.tweet)
      .send();
    console.log(`Awaiting confirmations for Txn hash ${op.hash}.`);
    const opres = await op.confirmation(3);
    console.log(`Operation injected: https://granada.tzstats.com/${opres}`);
    res.send({ success: true, message: op.hash });
  } catch (err) {
    res.send({
      success: false,
      message: err,
    });
    next(err);
    console.log(err);
  }
});

export default TokenizeRouter;

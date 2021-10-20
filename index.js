import express from "express";
// import { LocalStorage } from "node-localstorage";
import dotenv from "dotenv";
dotenv.config();
const app = express();
const port = 1234;
import TokenizeRouter from "./routes/Tokenize.js";

app.use("/", TokenizeRouter);

app.listen(port, () => {
  console.log("Server listening on port ", port);
});

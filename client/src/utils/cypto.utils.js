import CryptoJS from "crypto-js";
import { AES_IV, AES_SECRET_KEY } from "../config/constants.config";

export const encryptData = (data) => {
  const key = CryptoJS.enc.Hex.parse(AES_SECRET_KEY);
  const iv = CryptoJS.enc.Hex.parse(AES_IV);
  const encrypted = CryptoJS.AES.encrypt(JSON.stringify(data), key, { iv: iv });
  return encrypted.toString();
};
export const decryptData = (ciphertext) => {
  const key = CryptoJS.enc.Hex.parse(AES_SECRET_KEY);
  const iv = CryptoJS.enc.Hex.parse(AES_IV);
  const decrypted = CryptoJS.AES.decrypt(ciphertext, key, { iv: iv });
  return JSON.parse(decrypted.toString(CryptoJS.enc.Utf8));
};

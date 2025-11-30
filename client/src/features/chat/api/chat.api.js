import axios from "../../../config/axios.config";
import { decryptData, encryptData } from "../../../utils/cypto.utils";

const baseURL = "/api/chat";

export const getResponseFromLangchainChatApiCall = async (body) => {
  try {
    const response = await axios.post(`${baseURL}/langchain-completion`, {
      model: body.model,
      text: encryptData(body.text),
      chatId: body.chatId,
    });
    response.data.data &&
      (response.data.data = decryptData(response.data.data));
    return response.data;
  } catch (e) {
    return e;
  }
};

export const uploadDocumentApiCall = async (formData) => {
  try {
    return await axios.post(
      `${baseURL}/upload-doc`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );

  } catch (err) {
    console.log(err);
  }
};

export const trancribeAudioApiCall = async (formData) => {
  try {
    const response = await axios.post(`${baseURL}/transcribe`, formData);
    response.data.data &&
      (response.data.data = decryptData(response.data.data));
    return response.data;
  } catch (e) {
    return e;
  }
};

export const createNewChatApiCall = async () => {
  try {
    const response = await axios.post(`${baseURL}/create`);
    return response.data;
  } catch (e) {
    return e;
  }
};

export const deleteChatApiCall = async (chatId) => {
  try {
    const response = await axios.delete(`${baseURL}/delete?chatId=${chatId}`);
    return response.data;
  } catch (e) {
    return e;
  }
};

export const updateChatApiCall = async (body) => {
  try {
    const response = await axios.post(`${baseURL}/update`, body);
    return response.data;
  } catch (e) {
    return e;
  }
};

export const getAllChatsApiCall = async () => {
  try {
    const response = await axios.get(`${baseURL}/get`);
    return response.data;
  } catch (e) {
    return e;
  }
};

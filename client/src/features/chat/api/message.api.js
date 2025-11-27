import axios from "../../../config/axios.config";

const baseURL = "/api/message";

export const getMessagesOfChatApiCall = async (chatId) => {
  try {
    const response = await axios.get(`${baseURL}/get?chatId=${chatId}`);
    return response.data;
  } catch (e) {
    return e;
  }
};

export const insertMessageApiCall = async (body) => {
  try {
    const response = await axios.post(`${baseURL}/create`, body);
    return response.data;
  } catch (e) {
    return e;
  }
};

import axios from "axios";
import { API_URL } from "./constants.config";

axios.defaults.baseURL = API_URL;

export default axios;

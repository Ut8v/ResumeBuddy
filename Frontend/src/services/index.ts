import axios from "axios";

const BASE_URL = import.meta.env.VITE_BASE_URL;

export class ContentService {
  static async sendContent(data: FormData) {
    const response = await axios.post(`${BASE_URL}/contents`, data, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    return response.data;
  }
}


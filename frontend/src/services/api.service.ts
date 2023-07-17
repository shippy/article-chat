import axios from 'axios'

const API_URL: String = 'https://api.journalarticle.chat'
// const API_URL = ${process.env.API_URL}

export default {
  async uploadDocument(file: File) {
    const formData = new FormData();
    formData.append('file', file);
    await axios.post(`${API_URL}/upload_document`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },
  async getDocuments() {
    const response = await axios.get(`${API_URL}/documents`);
    return response.data;
  },
  async getChat(docId: Number, chatId: Number) {
    const response = await axios.get(`${API_URL}/document/${docId}/chat/${chatId}`);
    return response.data;
  },
  async sendMessage(docId: Number, chatId: Number, message: String) {
    await axios.post(`${API_URL}/document/${docId}/chat/${chatId}/submit`, { message });
  }
}
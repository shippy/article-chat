import axios from 'axios'

export const API_URL: String = import.meta.env.VITE_APP_BACKEND_URL

export default {
  async uploadDocument(file: File) {
    const formData = new FormData()
    formData.append('uploaded_file', file)
    const response = await axios.post(`${API_URL}/upload_and_process_file/`, formData, {
      withCredentials: true,
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    console.log(response)
    return response.data
  },
  async getDocuments() {
    const response = await axios.get(`${API_URL}/documents`, { withCredentials: true })
    console.log(response.data)
    return response.data
  },
  async startChat(docId: Number): Promise<Number> {
    const response = await axios.get(`${API_URL}/documents/${docId}/new_chat`, {
      withCredentials: true
    })
    console.log(response.data)
    return response.data
  },
  async getChat(docId: Number, chatId: Number) {
    const response = await axios.get(`${API_URL}/documents/${docId}/chat/${chatId}`, {
      withCredentials: true
    })
    console.log(response.data)
    return response.data
  },
  async sendMessage(docId: Number, chatId: Number, message: String) {
    const ai_response = await axios.post(
      `${API_URL}/documents/${docId}/chat/${chatId}/message`,
      { message: message },
      { withCredentials: true }
    )
    // TODO: Add both initial message and the AI response to the store
    console.log(ai_response.data)
    return ai_response.data
  }
}

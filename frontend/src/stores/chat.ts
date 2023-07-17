import { defineStore } from 'pinia'
import apiService from '../services/api.service'

interface SendMessagePayload {
    docId: number;
    chatId: number;
    message: string;
  }
  

export const useChatStore = defineStore({
  id: 'chat',
  state: () => ({
    messages: []
  }),
  actions: {
    async fetchMessages(docId: number, chatId: number) {
      const messages = await apiService.getChat(docId, chatId)
      this.messages = messages
    },
    async sendMessage({ docId, chatId, message }: SendMessagePayload) {
      await apiService.sendMessage(docId, chatId, message)
      await this.fetchMessages(docId, chatId)
    }
  }
})

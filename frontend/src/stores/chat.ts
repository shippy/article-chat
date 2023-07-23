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
  getters: {
    getMessages(state) { return state.messages }
  },
  actions: {
    async createChat(docId: number) {
      const chatId = await apiService.startChat(docId)
      return chatId
    },
    async fetchMessages(docId: number, chatId: number) {
      const messages = await apiService.getChat(docId, chatId)
      this.messages = messages
    },
    async sendMessage({ docId, chatId, message }: SendMessagePayload) {
      await apiService.sendMessage(docId, chatId, message)
      // FIXME: Add the message to the store instead of re-fetching everything
      await this.fetchMessages(docId, chatId)
    }
  }
})

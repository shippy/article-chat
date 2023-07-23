import { defineStore } from 'pinia'
import apiService from '../services/api.service'

export const useDocumentsStore = defineStore({
  id: 'documents',
  state: () => ({
    documents: []
  }),
  getters: {
    getDocuments(state) {
      return state.documents
    }
  },
  actions: {
    async fetchDocuments() {
      const documents = await apiService.getDocuments()
      this.documents = documents
    },
    async uploadDocument(file: File) {
      await apiService.uploadDocument(file)
      await this.fetchDocuments()
    }
  }
})

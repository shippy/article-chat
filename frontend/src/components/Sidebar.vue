<template>
    <div>
      <h2>Uploaded Documents</h2>
      <ul>
        <li v-for="document in documents" :key="document.id">
          {{ document.name }}
          <button @click="startChat(document.id)">Start Chat</button>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import apiService from '../services/api.service'
  
  export default {
    data() {
      return {
        documents: []
      }
    },
    async created() {
      this.documents = await apiService.getDocuments();
    },
    methods: {
      startChat(docId) {
        // Logic to start a chat
      }
    }
  }
  </script>
  
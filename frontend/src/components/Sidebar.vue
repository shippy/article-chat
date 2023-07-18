<template>
    <Login />
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
  
<script lang="ts">
import { computed } from 'vue'
import apiService from '../services/api.service'
import { type Document } from '../types'
import { useDocumentsStore } from '@/stores/documents'

export default {
    setup() {
        const store = useDocumentsStore();
        const documents = computed<Document[]>(() => store.$state.documents);

        // Your methods here

        return { documents };
    },

    async created() {
        this.documents = await apiService.getDocuments();
    },
    methods: {
        startChat(docId: Number) {
            console.log('Start chat for document ' + docId)
            // Logic to start a chat
        }
    }
}
</script>
  
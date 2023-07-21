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
  
<script lang="ts" setup>
import { computed, onMounted } from 'vue'
import { useDocumentsStore } from '@/stores/documents'
import { type Document } from '../types'

const store = useDocumentsStore();
const documents = computed<Document[]>(() => store.documents)

onMounted(async () => {
  await store.fetchDocuments();
});

const startChat = (docId: number) => {
  console.log('Start chat for document ' + docId);
  // Logic to start a chat
};
</script>

<template>
    <div id="sidebar">
        <h2>Uploaded Documents</h2>
        <ul>
            <li v-for="document in documents" :key="document.id">
                <button @click="startChat(document.id)">+</button>
                {{ document.title }}
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

<style>
#sidebar {
    position: fixed;
    top: 0;
    left: 0;
    padding: 10px;
    background-color: #eeeeee2a;
    border-right: 1px solid #ccc;
    border-radius: 5px;
    min-height: 100%;
    margin: 10px;
}
</style>
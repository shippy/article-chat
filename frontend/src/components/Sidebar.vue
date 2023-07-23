<template>
    <div id="sidebar">
        <h2>Uploaded Documents</h2>
        <ul>
            <li v-for="document in documents" :key="`doc-${document.id}`">
                <button @click="startChat(document.id)">+</button>
                {{ document.title }}
                <ul>
                  <li v-for="chat in document.chats" :key="`chat-${chat.id}`"><a v-bind:href="`/document/${document.id}/chat/${chat.id}`">Chat {{ chat.id }}</a></li>
                </ul>
            </li>
        </ul>
    </div>
</template>
  
<script lang="ts" setup>
import { computed, onMounted, ref } from 'vue'
import { useDocumentsStore } from '@/stores/documents'
import { type Document } from '../types'
import router from '@/router';
import apiService from '@/services/api.service';
// import isLoggedIn from '../services/auth.service'

const store = useDocumentsStore();
const documents = computed<Document[]>(() => store.documents)
// const is_authenticated = ref(false);
// const user = ref('');

onMounted(async () => {
  await store.fetchDocuments();
  // { is_authenticated, user } = await isLoggedIn.isLoggedIn();
});

const startChat = async (docId: Number) => {
  const chatId = await apiService.startChat(docId);
  router.push({ name: 'chat' , params: { docId: docId.toString(), chatId: chatId.toString()}})
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
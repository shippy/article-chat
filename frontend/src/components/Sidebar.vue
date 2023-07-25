<template>
  <div className="sidebar">
    <div id="file_upload">
      <FileUpload />
    </div>
    <div id="sidebar">
      <h2>Uploaded Documents</h2>
      <ul>
        <li v-for="document in documents" :key="`doc-${document.id}`">
          <button @click="startChat(document.id)">+</button>
          {{ document.title }}
          <ul>
            <li v-for="chat in document.chats" :key="`chat-${chat.id}`"><a
                v-bind:href="`/document/${document.id}/chat/${chat.id}`">Chat {{ chat.id }}</a></li>
          </ul>
        </li>
      </ul>
    </div>
  </div>
</template>
  
<script lang="ts" setup>
import { computed, onMounted, ref } from 'vue'
import { useDocumentsStore } from '@/stores/documents'
import { useChatStore } from '@/stores/chat';
import { type Document } from '../types'
import router from '@/router';
import apiService from '@/services/api.service';
import FileUpload from './FileUpload.vue';
// import isLoggedIn from '../services/auth.service'

const store = useDocumentsStore();
const chatStore = useChatStore();
const documents = computed<Document[]>(() => store.$state.documents)
// const is_authenticated = ref(false);
// const user = ref('');

onMounted(async () => {
  await store.fetchDocuments();
  // { is_authenticated, user } = await isLoggedIn.isLoggedIn();
});

const startChat = async (docId: Number) => {
  const chatId = await apiService.startChat(docId);
  router.push({ name: 'chat', params: { docId: docId.toString(), chatId: chatId.toString() } })
  // TODO: Update only the one item in the store instead of refreshing everything
  store.fetchDocuments();
  chatStore.fetchMessages(docId as number, chatId as number);
};
</script>

<style>
.sidebar {
    grid-area: sidebar;
    display: flex;
    flex-direction: column;
    height: 100vh;
    position: fixed;
    width: 250px;
    max-width: 300px;
    overflow-y: auto;
    padding: 50px 0;
    /* other styles... */
}
/* #sidebar {
  position: fixed;
  top: 0;
  left: 0;
  padding: 10px;
  background-color: #eeeeee2a;
  border-right: 1px solid #ccc;
  border-radius: 5px;
  min-height: 100%;
  margin: 10px;
  min-width: 250px;
  max-width: 300px;
}

#file_upload {
  position: fixed;
  bottom: 0;
  left: 0;
  padding: 10px;
  background-color: #eeeeee2a;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin: 10px;
  max-width: 250px;
} */
</style>
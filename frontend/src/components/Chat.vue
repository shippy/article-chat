<template>
    <div id="chat_messages">
        <h2>Chat {{ chatId }} for Document {{ docId }}</h2>
        <div v-for="msg in chat" :key="msg.id" :class="msg.originator">
            {{ msg.content }}
        </div>
    </div>
    <div id="chat_submission">
        <textarea v-model="message"></textarea>
        <button :disabled="isSending" @click="sendMessage">Send</button>
    </div>
</template>
  
<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import apiService from '../services/api.service'
import { useChatStore } from '@/stores/chat';
import { type Message } from '@/types'

// Props definition
const props = defineProps({
    docId: {
        type: Number,
        required: true
    },
    chatId: {
        type: Number,
        required: true
    }
})

const store = useChatStore();
const chat = computed<Message[]>(() => store.$state.messages);
const message = ref('');
const isSending = ref(false)

const sendMessage = async () => {
    isSending.value = true
    const aiResponse = await apiService.sendMessage(props.docId, props.chatId, message.value);
    message.value = '';
    isSending.value = false
    // TODO: Add latest AI response to the store instead of refreshing everything
    
    // Fetch the latest chat messages
    await store.fetchMessages(props.docId, props.chatId);
}

onMounted(async () => {
    // Fetch the initial chat messages
    await store.fetchMessages(props.docId, props.chatId);
});
</script>

  
<style>
#chat_messages {
    /* margin-left: 300px; */
    margin-top: 50px;
}

#chat_submission {
    position: fixed;
    bottom: 0;
    left: 300px;
    padding: 10px;
    background-color: #eeeeee2a;
    border-top: 1px solid #ccc;
    border-radius: 5px;
    width: 100%;
    margin: 10px;
}

.user {
    text-align: right;
    border-right: 3px solid rgba(255, 0, 0, 0.579);
    padding: 10px;
}

.ai {
    text-align: left;
    border-left: 3px solid rgba(0, 255, 162, 0.418);
    padding: 10px;
}
</style>
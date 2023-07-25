<template>
    <div className="content">
        <!-- <div id="chat_messages"> -->
            <h2>Chat {{ chatId }} for Document {{ docId }}</h2>
            <div v-for="msg in chat" :key="msg.id" :class="msg.originator">
                {{ msg.content }}
            </div>
        <!-- </div> -->
    </div>
    
    <div className="textarea" id="chat_submission">
        <textarea :disabled="isSending" v-model="message" @keyup.enter.prevent="sendMessage"></textarea>
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
    flex-grow: 1;
    overflow-y: auto;
    margin-bottom: 10px;
}
#chat_submission {
    position: fixed; /* fix the position */
    bottom: 0; /* stick it to the bottom */
    left: 320px; /* considering 300px width of sidebar and 20px of some padding */
    width: calc(100% - 320px); /* considering 300px width of sidebar and 20px of some padding */
    display: flex;
    padding: 1em 50px;
}
#chat_submission textarea {
    margin: 5px;
    height: 3em;
    flex-grow: 1; /* Make the textarea take up the remaining space */
}

#chat_submission button {
    margin: 5px;
    height: 3em;
    display: block;
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
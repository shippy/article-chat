<template>
    <div id="chat_messages">
        <h2>Chat {{ chatId }} for Document {{ docId }}</h2>
        <div v-for="msg in chat" :key="msg.id" :className="msg.originator">
            {{ msg.content }}
        </div>
    </div>
    <div id="chat_submission">
        <textarea v-model="message"></textarea>
        <button @click="sendMessage()">Send</button>
    </div>
</template>
  
<script lang="ts">
import { computed, ref } from 'vue'
import apiService from '../services/api.service'
import { useChatStore } from '@/stores/chat';
import { type Message } from '../types'

export default {
    setup() {
        const store = useChatStore();
        // const chat = computed<Message[]>(() => store.$state.messages);
        const chat = ref<Message[]>([])
        const message = ref('');

        return { chat, message };
    },
    props: {
        docId: {
            type: Number,
            required: true
        },
        chatId: {
            type: Number,
            required: true
        }
    },
    async created() {
        this.chat = await apiService.getChat(this.docId, this.chatId);
    },
    methods: {
        async sendMessage() {
            await apiService.sendMessage(this.docId, this.chatId, this.message);
            this.message = '';
            this.chat = await apiService.getChat(this.docId, this.chatId);
        }
    }
}
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
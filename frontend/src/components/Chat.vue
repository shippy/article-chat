<template>
    <div>
        <h2>Chat for Document {{ docId }}</h2>
        <div v-for="message in chat" :key="message.id">
            {{ message.text }}
        </div>
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
        const chat = computed<Message[]>(() => store.$state.messages);
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
  
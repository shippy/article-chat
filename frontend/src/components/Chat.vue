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
  
<script>
import apiService from '../services/api.service'

export default {
    props: {
        docId: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            chat: [],
            message: ''
        }
    },
    async created() {
        this.chat = await apiService.getChat(this.docId);
    },
    methods: {
        async sendMessage() {
            await apiService.sendMessage(this.docId, this.message);
            this.message = '';
            this.chat = await apiService.getChat(this.docId);
        }
    }
}
</script>
  
<script setup lang="ts">
import { useChatStore } from '@/stores/chat';
import Sidebar from '@/components/Sidebar.vue';
import Chat from '../components/Chat.vue'
// import { defineProps } from 'vue'
import { ref, onMounted } from 'vue'
import isLoggedIn from '@/services/auth.service'

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
</script>

<template>
    <Sidebar />
    <div id="chat">
        <Chat :docId="docId as number" :chatId="chatId as number" />
    </div>
</template>

<style>
#chat {
    grid-area: chat;
    display: flex;
    flex-direction: column;
    height: 100%;
    margin-left: 320px; /* considering 300px width of sidebar and 20px of some padding */
    width: calc(100% - 320px); /* considering 300px width of sidebar and 20px of some padding */
}
</style>
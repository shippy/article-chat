<template>
    <div id="chat">
        <Chat :docId="docId as number" :chatId="chatId as number" />
    </div>
</template>
  
<script setup lang="ts">
import { useChatStore } from '@/stores/chat';
import Chat from '../components/Chat.vue'
// import { defineProps } from 'vue'

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
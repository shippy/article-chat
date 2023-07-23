<template>
    <div id="chat">
        <Chat :docId=docId :chatId=chatId />
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
    margin-left: 300px;
    margin-top: 50px;
}
</style>
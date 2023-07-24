<template>
    <input ref="fileInput" :disabled="isUploading" type="file" @change="uploadFile" />
</template>
  
<script setup lang="ts">
import { ref } from 'vue'
import apiService from '../services/api.service'

const isUploading = ref(false)
const fileInput = ref(null)

const uploadFile = async (event: Event) => {
    const file = (event.target as HTMLInputElement).files[0];
    isUploading.value = true
    const response = await apiService.uploadDocument(file);
    isUploading.value = false
    fileInput.value.value = null;

    return response;
};
</script>

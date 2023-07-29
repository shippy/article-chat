<template>
    <input ref="fileInput" :disabled="isUploading" type="file" @change="uploadFile" />
    <p v-if="uploadError">{{ uploadError }}</p>
</template>
  
<script setup lang="ts">
import { ref } from 'vue'
import apiService from '../services/api.service'
import { useDocumentsStore } from '@/stores/documents';

const isUploading = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)
const uploadError = ref<string | null>(null)
const store = useDocumentsStore();

const uploadFile = async (event: Event) => {
    const fileInputEl = event.target as HTMLInputElement;
    const file = fileInputEl.files ? fileInputEl.files[0] : null;
    if (file) {
        try {
            isUploading.value = true
            const response = await apiService.uploadDocument(file);
            isUploading.value = false
            if (fileInput.value) {
                fileInput.value.value = '';
            }
            uploadError.value = null
            store.fetchDocuments();
            return response;
        } catch (err) {
            uploadError.value = (err as Error).message || "An error occurred during file upload"
            isUploading.value = false
        }
    }
};
</script>

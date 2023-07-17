<template>
    <input type="file" @change="uploadFile" />
</template>
  
<script lang="ts">
import apiService from '../services/api.service'

export default {
    methods: {
        async uploadFile(event: any) {
            const file = event.target.files[0];
            await apiService.uploadDocument(file);
        }
    }
}
</script>
  
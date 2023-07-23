<template>
    <input type="file" @change="uploadFile" />
</template>
  
<script lang="ts">
import apiService from '../services/api.service'
// TODO: Use document store instead?
export default {
    methods: {
        async uploadFile(event: any) {
            const file = event.target.files[0];
            const response = await apiService.uploadDocument(file);
            return response
        }
    }
}
</script>
  
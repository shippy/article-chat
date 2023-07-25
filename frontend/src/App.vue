<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterView } from 'vue-router'
import Sidebar from './components/Sidebar.vue'
import Login from './components/Login.vue';
import isLoggedIn from './services/auth.service'

const isAuthenticated = ref(false);
onMounted(async () => {
  const response = await isLoggedIn.isLoggedIn();
  isAuthenticated.value = response.is_authenticated;
});
</script>

<template>
  <div id="app">
    <Login />
    <Sidebar v-if="isAuthenticated" />
    <RouterView />
  </div>
</template>

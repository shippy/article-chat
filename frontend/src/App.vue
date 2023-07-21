<script setup lang="ts">
import { RouterView } from 'vue-router'
import Sidebar from './components/Sidebar.vue'
import Login from './components/Login.vue';
</script>

<template>
  <div id="app">
    <Login />
    <Sidebar />
    <RouterView />
  </div>
</template>

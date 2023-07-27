<script setup lang="ts">
import { RouterView } from 'vue-router'
import Login from './components/Login.vue';
</script>

<template>
  <div id="app">
    <Login />
    <RouterView />
  </div>
</template>

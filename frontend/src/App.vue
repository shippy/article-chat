<script setup lang="ts">
import { RouterView } from 'vue-router'
import Sidebar from './components/Sidebar.vue'
</script>

<template>
  <div id="app">
    <sidebar/>
    <router-view/>
  </div>
</template>
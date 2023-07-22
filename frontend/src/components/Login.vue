<template>
    <div v-if="!logged_in" id="login">
        <h2><a v-bind:href="`https://auth.journalarticle.chat/login?response_type=code&amp;client_id=7acimbldoceq4psub3m6ks0koc&amp;redirect_uri=${callback_url}/auth/callback`">Log in</a></h2>
    </div>
    <div v-else>
        <h2>{{ username }} | <a v-bind:href="`https://auth.journalarticle.chat/logout?client_id=7acimbldoceq4psub3m6ks0koc&amp;logout_uri=${callback_url}/auth/logout`">Log out</a></h2>
    </div>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import isLoggedIn from '../services/auth.service'

const username = ref('')
const logged_in = ref(false)
const callback_url = import.meta.env.VITE_APP_BACKEND_URL

onMounted(async () => {
    const response = await isLoggedIn.isLoggedIn();
    if (response) {
        username.value = response.user ?? '';
        logged_in.value = true;
    }
});

</script>

<template>
    <div className="header" id="login_box">
        <div v-if="!logged_in" id="login_link">
            <h3><a
                    v-bind:href="`https://auth.journalarticle.chat/login?response_type=code&amp;client_id=7acimbldoceq4psub3m6ks0koc&amp;redirect_uri=${callback_url}/auth/callback`">Log
                    in</a></h3>
        </div>
        <div v-else id="logout_link">
            <h3>{{ username }} | <a
                    v-bind:href="`https://auth.journalarticle.chat/logout?client_id=7acimbldoceq4psub3m6ks0koc&amp;logout_uri=${callback_url}/auth/logout`">Log
                    out</a></h3>
        </div>
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
    if (response.is_authenticated) {
        username.value = response.user ?? '';
        logged_in.value = true;
    }
});

</script>
<style>
#login_box {
    text-align: right;
}
/* #login_box {
    position: fixed;
    top: 0;
    right: 0;
    padding: 10px;
    background-color: #eeeeee2a;
    border: 1px solid #ccc;
    border-radius: 5px;
    margin: 10px;
} */
</style>
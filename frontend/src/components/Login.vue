<template>
    <div className="header">
        <div id="logo"><h3>JournalArticle.chat</h3></div>
        <div v-if="!logged_in" className="login_box" id="login_link">
            <h3><a v-bind:href="make_auth_url('login', 'redirect', 'auth/callback', 'code')">Log in</a> </h3>
        </div>
        <div v-else className="login_box" id="logout_link">
            <h3>{{ username }} | <a v-bind:href="make_auth_url('logout', 'logout', 'auth/logout')">Log out</a></h3>
        </div>
    </div>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import isLoggedIn from '@/services/auth.service'

const username = ref('')
const logged_in = ref(false)
const redirect_url_base = import.meta.env.VITE_APP_BACKEND_URL
const auth_url_base = "https://auth.journalarticle.chat"
const client_id = "7acimbldoceq4psub3m6ks0koc"

// Create a function that takes the variable parts of the URL and constructs a login/logout URL
const make_auth_url = (action: string, redirect_name: string, redirect_target: string, response_type?: string) => {
    var url = `${auth_url_base}/${action}?client_id=${client_id}&${redirect_name}_uri=${redirect_url_base}/${redirect_target}`
    if (response_type) {
        url += `&response_type=${response_type}`
    }
    return url
}


onMounted(async () => {
    const response = await isLoggedIn.isLoggedIn();
    if (response.is_authenticated) {
        username.value = response.user ?? '';
        logged_in.value = true;
    }
});

</script>
<style>
.login_box {
    text-align: right;
}

#logo {
    text-align: left;
    float: left;
}
</style>
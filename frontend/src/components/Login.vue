<template>
    <div v-if="!logged_in" id="login">
        <h2><a href="https://auth.journalarticle.chat/login?response_type=code&amp;client_id=7acimbldoceq4psub3m6ks0koc&amp;redirect_uri=https://api.journalarticle.chat/auth/callback">Log in</a></h2>
    </div>
    <div v-else>
        <h2>{{ username }} | <a href="/logout">Log out</a></h2>
    </div>
</template>
<script lang="ts">
import { computed, ref } from 'vue'

export default {
    data() {
        return {
            logged_in: ref(false),
            username: ref('')
        }
    },
}
</script>

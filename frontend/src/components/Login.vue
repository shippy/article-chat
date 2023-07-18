<template>
    <div v-if="!logged_in" id="login">
        <h2><a href="https://auth.journalarticle.chat/login?response_type=code&amp;client=7acimbldoceq4psub3m6ks0koc&amp;callback=https://api.journalarticle.chat/callback">Log in</a></h2>
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

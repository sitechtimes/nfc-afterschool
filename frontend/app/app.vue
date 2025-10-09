<template>
    <div class="main min-h-screen bg-neutral">
        <NuxtPage />
    </div>
</template>

<script setup lang="ts">
import { useUserStore } from "./stores/userStore";

const userStore = useUserStore();

function calls() {
    userStore.getUser();
    console.log(localStorage.getItem("user"));
}
onMounted(() => {
    setInterval(() => {
        calls();
    }, 3000);
});
</script>

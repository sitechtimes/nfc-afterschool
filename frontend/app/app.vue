<template>
  <div class="main min-h-screen bg-neutral">
    <NuxtPage />
  </div>
</template>

<script setup lang="ts">
const userStore = useUserStore();

function calls() {
  //   userStore.getUser();
}
onMounted(() => {
  userStore.getUser();
  setInterval(() => {
    calls();
  }, 3000);
});
</script>

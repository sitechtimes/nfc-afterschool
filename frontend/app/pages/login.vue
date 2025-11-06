<template>
  <div
    class="flex flex-col h-screen items-center justify-center gap-10 bg-gradient-to-br from-base-100 via-secondary to-base-300"
  >
    <h1 class="text-3xl font-bold">After School Attendance</h1>
    <div
      class="card card-xl bg-neutral md:w-1/2 w-4/5 justify-center shadow-xl md:hover:shadow-2xl hover:md:scale-101 transition duration-700"
    >
      <div class="card-body justify-center h-fit">
        <h2 class="card-title justify-center">Enter account information</h2>
        <form @submit.prevent="handleLogin" class="flex flex-col w-full gap-2">
          <h3>Username:</h3>
          <input
            class="input w-full bg-base-200"
            type="text"
            v-model="form.username"
            placeholder="Enter Username"
            required
          />
          <h3>Password:</h3>
          <input
            class="input w-full bg-base-200"
            type="password"
            v-model="form.password"
            placeholder="Enter Password"
            required
          />
          <button
            class="btn btn-primary btn-block active:scale-101"
            type="submit"
          >
            Login
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const userStore = useUserStore();
const form = ref<{ username: string; password: string }>({
  username: "",
  password: "",
});

function handleLogin() {
  userStore.setUser({ username: "admin", role: "supervisor" });
  navigateTo("/");
}
</script>

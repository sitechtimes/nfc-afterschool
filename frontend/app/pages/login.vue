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
          <input
            class="input w-full bg-base-200"
            type="text"
            v-model="form.username"
            placeholder="Enter Username"
            required
          />
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
        <p v-if="error" class="text-error">{{ error }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const userStore = useUserStore();
const config = useRuntimeConfig();
const form = ref<{ username: string; password: string }>({
  username: "",
  password: "",
});
const error = ref("");

async function handleLogin() {
  try {
    const response = await fetch(`${config.public.backendUrl}/api/token/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: form.value.username,
        password: form.value.password,
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      error.value = `Failed to login. Status: ${response.status}. ${errorText}`;
      throw new Error(`Failed to login. Status: ${response.status}`);
    }
    const data = await response.json();

    const token = data.access || data.key || data.token;
    if (!token) {
      error.value = "Invalid response from server. Token not found.";
      return;
    }

    if (typeof window !== "undefined") {
      localStorage.setItem("token", token);
    }

    userStore.logged = token;
    navigateTo("/");
  } catch (err) {
    console.error("Error logging in:", err);
    const errorMsg = err instanceof Error ? err.message : String(err);
    if (errorMsg.includes("fetch") || errorMsg.includes("Failed to fetch")) {
      error.value =
        "Cannot connect to server. Please check if the backend is running.";
    } else {
      error.value = "Login failed. Please check your credentials.";
    }
  }
}
</script>

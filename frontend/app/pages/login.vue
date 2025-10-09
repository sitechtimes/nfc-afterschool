<template>
  <div class="flex flex-col h-screen p-4 items-center justify-center gap-10">
    <h1 class="text-3xl font-bold">After School Attendance</h1>
    <div
      class="card card-xl md:w-1/2 w-4/5 justify-center shadow-xl hover:md:shadow-2xl hover:md:scale-101 transition duration-700"
    >
      <div class="card-body justify-center h-fit">
        <h2 class="card-title justify-center">Enter account information</h2>
        <form @submit.prevent class="flex flex-col w-full gap-2">
          <input
            class="input w-full bg-base-200"
            type="text"
            v-model="form.username"
            placeholder="Enter Username"
          />
          <input
            class="input w-full bg-base-200"
            type="password"
            v-model="form.passoword"
            placeholder="Enter Password"
          />
          <button class="btn btn-primary btn-block" type="submit">Login</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const form = ref({
  username: "",
  passoword: "",
});
</script>

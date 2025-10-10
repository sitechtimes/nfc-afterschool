<template>
  <t-dialog name="manual-student-entry" icon="user" type="form">
    <template #title>
      Manually Add Student
    </template>

    <div class="space-y-4">
      <input v-model="form.activity" placeholder="Activity" class="input input-bordered w-full" />
      <input v-model="form.date" type="date" class="input input-bordered w-full" />
      <input v-model="form.name" placeholder="Student Name" class="input input-bordered w-full" />
      <input v-model="form.email" type="email" placeholder="Student Email" class="input input-bordered w-full" />
    </div>
  </t-dialog>
</template>

<script setup>
import { reactive } from 'vue'

const form = reactive({
  activity: '',
  date: '',
  name: '',
  email: ''
})
</script>
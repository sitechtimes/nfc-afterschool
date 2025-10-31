<template>
  <div class="relative w-full px-6">
    <div
      v-if="studentInfoScreenOpen"
      class="fixed inset-0 bg-black/40 backdrop-blur-sm z-40"
    ></div>
    <dialog
      v-if="studentInfoScreenOpen"
      ref="dialog"
      id="dialog"
      class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 fieldset rounded-box border p-4 border-primary w-xs"
    >
      <form
        method="dialog"
        @submit.prevent="submitStudentData"
        class="flex flex-col gap-4"
      >
        <label class="flex flex-col text-secondary-content"> Activity </label>
        <select
          name="activity-choice"
          v-model="studentActivity"
          id="AC"
          class="select"
        >
          <option v-for="activity in limitedViewDropdown" :key="activity">
            {{ activity }}
          </option>
        </select>
        <!-- Tailwin dropdown menu \ Rewrite this all  -->

        <label class="flex flex-col text-gray-700">
          Name:
          <input v-model="studentName" type="text" required class="input" />
        </label>
        <label class="flex flex-col text-gray-700">
          Student Email:
          <input type="email" v-model="studentEmail" required class="input" />
        </label>
        <div class="flex justify-end gap-2">
          <button class="btn btn-md">Submit</button>
          <button class="btn btn-md" @click="closeWithoutData">Close</button>
        </div>
      </form>
    </dialog>
    <button class="btn btn-outline btn-block" @click="openInfoEnterPage">
      Enter student information
    </button>
  </div>
</template>

<script setup lang="ts">
const today = new Date();
const todayFormatted = `${
  today.getMonth() + 1
}/${today.getDate()}/${today.getFullYear()}`;
const studentInfoScreenOpen = ref(false);
const dialog = ref();
const studentActivity = ref("");
const studentName = ref("");
const studentEmail = ref("");
const listOfActivities = useActivityStore();
const limitedViewDropdown = listOfActivities.activities.slice(0, 15);

function openInfoEnterPage() {
  studentInfoScreenOpen.value = true;
}
function closeWithoutData() {
  studentName.value = "";
  studentEmail.value = "";
  studentActivity.value = "";
  dialog.value.close();
  studentInfoScreenOpen.value = false;
}
function submitStudentData() {
  studentName.value = studentName.value.trim();
  const studentData = {
    name: studentName.value,
    email: studentEmail.value,
    activity: studentActivity.value,
    date: todayFormatted,
  };
  studentName.value = "";
  studentEmail.value = "";
  studentActivity.value = "";
  studentInfoScreenOpen.value = false;
  dialog.value.close();
}
</script>

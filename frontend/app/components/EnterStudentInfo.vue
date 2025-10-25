<template>
  <div class="relative">
    <div
      v-if="studentInfoScreen"
      class="fixed inset-0 bg-black/40 backdrop-blur-sm z-40"
    ></div>
    <dialog
      ref="dialog"
      id="dialog"
      class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 fieldset rounded-box border p-4 border-primary w-xs"
    >
      <form
        method="dialog"
        @submit.prevent="submitStudentData"
        class="flex flex-col gap-4"
      >
        <label class="flex flex-col text-gray-700"> Activity </label>
        <select
          name="activity-choice"
          v-model="studentActivity"
          id="AC"
          class="select"
        >
          <option
            v-for="activity in listOfActivities.activities"
            :key="activity"
          >
            {{ activity }}
          </option>
        </select>
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
    <button class="btn btn-md" @click="openInfoEnterPage">
      Enter student information
    </button>
  </div>
</template>

<script setup lang="ts">
const today = new Date();
const todayFormatted = `${
  today.getMonth() + 1
}/${today.getDate()}/${today.getFullYear()}`;
const studentInfoScreen = ref(false);
const dialog = ref();
const studentActivity = ref("");
const studentName = ref("");
const studentEmail = ref("");
const listOfActivities = useActivityStore();

function openInfoEnterPage() {
  dialog.value.showModal();
  studentInfoScreen.value = true;
}
function closeWithoutData() {
  studentName.value = "";
  studentEmail.value = "";
  studentActivity.value = "";
  dialog.value.close();
  studentInfoScreen.value = false;
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
  studentInfoScreen.value = false;
  dialog.value.close();
}
</script>

<template>
  <div class="relative">
    <div
      v-if="studentInfoScreen"
      class="fixed inset-0 bg-black/40 backdrop-blur-sm z-40 ju"
    ></div>
    <dialog
      ref="dialog"
      id="dialog"
      class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 bg-white rounded-lg p-6 shadow-xl w-[90%] max-w-md"
    >
      <form
        method="dialog"
        @submit.prevent="submitStudentData"
        class="flex flex-col gap-4"
      >
        <label class="flex flex-col text-gray-700"> Activity </label>
        <select name="activity-choice" v-model="studentActivity" id="AC">
          <option
            v-for="activity in listOfActivities.activities"
            :key="activity"
          >
            {{ activity }}
          </option>
        </select>
        <label class="flex flex-col text-gray-700">
          Name:
          <input
            v-model="studentName"
            type="text"
            required
            class="border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </label>
        <label class="flex flex-col text-gray-700">
          Student Email:
          <input
            type="email"
            v-model="studentEmail"
            required
            class="border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </label>
        <div class="flex justify-end gap-2">
          <input
            type="submit"
            class="bg-blue-100 hover:bg-blue-200 text-blue-700 px-4 py-2 rounded-md cursor-pointer"
            value="Submit"
          />
          <input type="button" class="bg-blue-500 hover:bg-blue-600 text-white
          px-4 py-2 rounded-md cursor-pointer" @click="closeWithoutData"
          value="Close"
        </div>
      </form>
    </dialog>
    <button
      class="bg-blue-500 text-white px-10 py-3 rounded-lg shadow-md"
      @click="openInfoEnterPage"
    >
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

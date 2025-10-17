<template>
  <div class="relative">
    <div
      v-if="isEnterInfoScreenOpen"
      class="fixed inset-0 bg-black/40 backdrop-blur-sm z-40"
    ></div>

    <dialog
      ref="dialog"
      id="dialog"
      class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 bg-white rounded-lg p-6 shadow-xl w-[90%] max-w-md"
    >
      <form
        method="dialog"
        @submit.prevent="NeedDataToClose"
        class="flex flex-col gap-4"
      >
        <p>
          <label class="flex flex-col text-gray-700"> Activity </label>
          <select name="activity-choice" v-model="Activity" id="AC">
            <option
               v-for="activity in list.activities"
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
        </p>
        <div class="flex justify-end gap-2">
          <input
            type="submit"
            class="bg-blue-100 hover:bg-blue-200 text-blue-700 px-4 py-2 rounded-md cursor-pointer"
            value="Submit"
          />
          <input
            type="button"
            class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md cursor-pointer"
            @click="CloseWithoutData"
            value="Close"
          />
        </div>
      </form>
    </dialog>
    <p class="text-center mt-6">
      <button
        class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg shadow-md"
        @click="openInfoEnterPage"
      >
        Enter student information
      </button>
    </p>
  </div>
</template>

<script setup lang="ts">
const today = new Date();
const todayFormatted = `${today.getMonth() + 1}/${today.getDate()}/${today.getFullYear()}`;
const isEnterInfoScreenOpen = ref(false);
const dialog = ref(null);
const Activity = ref("");
const studentName = ref("");
const studentEmail = ref("");
const list = useActivityStore()

function openInfoEnterPage() {
  dialog.value.showModal();
  isEnterInfoScreenOpen.value = true;
}

function CloseWithoutData() {
  studentName.value = "";
  studentEmail.value = "";
  Activity.value = "";
  dialog.value.close();
  isEnterInfoScreenOpen.value = false;
}
function NeedDataToClose() {
  studentName.value = studentName.value.trim();
  const studentData = {
    name: studentName.value,
    email: studentEmail.value,
    activity: Activity.value,
    date: todayFormatted,
  };
  studentName.value = "";
  studentEmail.value = "";
  Activity.value = "";
  isEnterInfoScreenOpen.value = false;
  dialog.value.close();
  
}
</script>

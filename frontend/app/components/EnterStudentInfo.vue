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
        <div class="dropdown dropdown-right w-full">
          <div tabindex="0" role="button" class="btn m-1 rounded-box w-full">
            {{ studentActivity || "Select Activity" }}
          </div>
          <ul
            tabindex="-1"
            class="dropdown-content menu bg-base-100 rounded-box z-1 w-52 p-2 shadow-sm"
          >
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search..."
              class="input input-sm mb-2 w-full"
            />
            <li v-for="activity in searchResults" :key="activity">
              <button @click="choiceSelector(activity)">{{ activity }}</button>
            </li>
            <li
              v-if="!searchResults.length"
              class="text-center text-sm opacity-50"
            >
              No results
            </li>
          </ul>
        </div>
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
const searchQuery = ref("");
const listOfActivities = useActivityStore();
const initialActivites = listOfActivities.activities.slice(0, 4);
const searchResults = computed(() => {
  if (!searchQuery.value.trim()) return initialActivites;
  return listOfActivities.activities.filter((a: string) =>
    a.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

function choiceSelector(choice: string) {
  studentActivity.value = choice;
}

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
  studentActivity.value = "";
  studentName.value = "";
  studentEmail.value = "";
  studentActivity.value = "";
  studentInfoScreenOpen.value = false;
  dialog.value.close();
}
</script>

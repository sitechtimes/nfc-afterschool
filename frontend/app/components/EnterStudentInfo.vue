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
      class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 fieldset rounded-box p-4 w-xs"
    >
      <form
        method="dialog"
        @submit.prevent="submitStudentData"
        class="flex flex-col gap-4"
      >
        <label class="flex flex-col text-secondary-content"> Activity </label>
        <div class="dropdown w-full">
          <div tabindex="0" role="button" class="btn m-1 rounded-box w-full">
            {{ studentActivity || "Select Activity" }}
          </div>
          <ul
            tabindex="-1"
            class="dropdown-content menu bg-base-100 rounded-box z-1 w-52 p-2 shadow-sm"
          >
            <input
              v-model="activitySearch"
              type="text"
              placeholder="Search..."
              class="input input-sm mb-2 w-full"
            />
            <li v-for="activity in filteredActivities" :key="activity">
              <button @click.prevent="choiceSelector(activity)">
                {{ activity }}
              </button>
            </li>
            <li
              v-if="!filteredActivities.length"
              class="text-center text-sm opacity-50"
            >
              No results
            </li>
          </ul>
        </div>
        <label v-if="!selectedStudent" class="flex flex-col text-gray-700">
          Name/Email:
          <input v-model="studentSearch" type="text" required class="input" />
          <div
            v-if="filteredStudents.length > 0 && studentSearch"
            class="absolute top-full left-0 right-0 bg-white border-2 border-gray-200 rounded-xl mt-2 max-h-64 overflow-y-auto z-20 shadow-xl"
          >
            <div
              v-for="student in filteredStudents"
              :key="student.email"
              @click="
                selectedStudent = student;
                studentSearch = '';
              "
              class="p-4 hover:bg-blue-50 cursor-pointer border-b border-gray-100 last:border-b-0 transition-colors"
            >
              <div class="font-semibold text-gray-800">
                {{ student.name }}
              </div>
              <div class="text-sm text-gray-500">{{ student.email }}</div>
            </div>
          </div>
        </label>
        <div v-if="selectedStudent">
          <div
            class="flex items-center gap-3 justify-between bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-4 border border-blue-200"
          >
            <div>
              <div class="font-semibold text-gray-800">
                {{ selectedStudent.name }}
              </div>
              <div class="text-sm text-gray-600">
                {{ selectedStudent.email }}
              </div>
            </div>
            <button
              @click="selectedStudent = null"
              class="w-8 h-8 rounded-full hover:bg-red-100 hover:cursor-pointer flex items-center justify-center transition-colors"
              title="Remove student"
            >
              <img src="/icons/trash.svg" class="w-5 h-5" />
            </button>
          </div>
        </div>
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
const studentSearch = ref("");
const activitySearch = ref("");
const listOfActivities = useActivityStore();

const filteredActivities = computed(() => {
  if (!activitySearch.value.trim())
    return listOfActivities.activities.slice(0, 4);
  return listOfActivities.activities
    .filter((a: string) =>
      a.toLowerCase().includes(activitySearch.value.toLowerCase())
    )
    .slice(0, 4);
});

const selectedStudent = ref<{
  name: string;
  email: string;
  display: string;
} | null>(null);

const props = defineProps<{
  students: Array<{ name: string; email: string }>;
}>();

const students = toRef(props, "students");

const filteredStudents = computed(() => {
  if (!Array.isArray(students.value) || studentSearch.value == "") return [];
  const unfilteredStudents = students.value.map((student) => ({
    name: student.name,
    email: student.email,
    display: `${student.name} | ${student.email}`,
  }));
  return unfilteredStudents.filter((student) =>
    student.display.includes(studentSearch.value)
  );
});

function choiceSelector(choice: string) {
  studentActivity.value = choice;
}

function openInfoEnterPage() {
  studentInfoScreenOpen.value = true;
}
function closeWithoutData() {
  studentSearch.value = "";
  studentActivity.value = "";
  dialog.value.close();
  studentInfoScreenOpen.value = false;
}
function submitStudentData() {
  const studentData = {
    name: selectedStudent.value?.name,
    email: selectedStudent.value?.email,
    activity: studentActivity.value,
    date: todayFormatted,
  };
  studentActivity.value = "";
  studentSearch.value = "";
  studentInfoScreenOpen.value = false;
  dialog.value.close();
}
</script>

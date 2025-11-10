<template>
  <div class="relative w-full">
    <div
      v-if="isModalOpen"
      class="fixed inset-0 bg-black/40 backdrop-blur-sm z-40"
      @click="closeModal"
    ></div>

    <dialog
      v-if="isModalOpen"
      ref="dialogRef"
      class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 rounded-xl border border-base-300 bg-base-100 p-6 w-full max-w-md shadow-xl"
      @cancel.prevent="closeModal"
      @keydown.escape="closeModal"
    >
      <div class="flex flex-col gap-6">
        <div class="flex justify-between items-center">
          <h2 class="text-2xl font-bold text-base-content">
            Manual Student Input
          </h2>
          <button
            @click="closeModal"
            class="btn btn-sm btn-ghost btn-circle"
            aria-label="Close"
          >
            ✕
          </button>
        </div>

        <form @submit.prevent="submitStudentData" class="flex flex-col gap-4">
          <div class="form-control">
            <label class="label">
              <span class="label-text font-semibold">Activity</span>
              <span class="label-text-alt text-error">*</span>
            </label>
            <div class="relative">
              <div
                class="dropdown w-full"
                :class="{ 'dropdown-open': isActivityDropdownOpen }"
              >
                <button
                  type="button"
                  tabindex="0"
                  class="btn btn-outline w-full justify-between"
                  @click="toggleActivityDropdown"
                  @blur="handleActivityDropdownBlur"
                >
                  <span :class="{ 'text-base-content/50': !selectedActivity }">
                    {{ selectedActivity || "Select Activity" }}
                  </span>
                  <svg
                    class="w-4 h-4 transition-transform"
                    :class="{ 'rotate-180': isActivityDropdownOpen }"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M19 9l-7 7-7-7"
                    />
                  </svg>
                </button>
                <ul
                  v-if="isActivityDropdownOpen"
                  tabindex="0"
                  class="dropdown-content menu bg-base-100 rounded-box border border-base-300 w-full mt-2 max-h-64 overflow-y-auto shadow-lg z-50"
                >
                  <li
                    class="sticky top-0 bg-base-100 z-10 p-2 border-b border-base-300"
                  >
                    <input
                      v-model="activitySearchQuery"
                      type="text"
                      placeholder="Search activities..."
                      class="input input-sm w-full"
                      @click.stop
                    />
                  </li>
                  <li
                    v-for="activity in filteredActivities"
                    :key="activity"
                    class="border-b border-base-200 last:border-b-0"
                  >
                    <button
                      type="button"
                      @click="selectActivity(activity)"
                      class="w-full text-left p-3 hover:bg-base-200 transition-colors"
                      :class="{
                        'bg-primary/10 text-primary font-semibold':
                          activity === selectedActivity,
                      }"
                    >
                      {{ activity }}
                    </button>
                  </li>
                  <li
                    v-if="filteredActivities.length === 0"
                    class="p-3 text-center text-sm text-base-content/50"
                  >
                    No activities found
                  </li>
                </ul>
              </div>
              <p
                v-if="isActivityDropdownOpen && !selectedActivity"
                class="text-xs text-base-content/60 mt-1"
              >
                <span v-if="activitySearchQuery">
                  Showing {{ filteredActivities.length }} of
                  {{ activityStore.activities.length }} activities
                </span>
                <span v-else>
                  {{ activityStore.activities.length }} activities available
                </span>
              </p>
            </div>
          </div>

          <div class="form-control relative">
            <label class="label">
              <span class="label-text font-semibold">Student Name</span>
              <span class="label-text-alt text-error">*</span>
            </label>
            <input
              v-model="studentName"
              type="text"
              required
              class="input input-bordered w-full"
              placeholder="Enter student name"
              @input="onStudentNameInput"
              @focus="showStudentSuggestions = true"
              @blur="handleStudentNameBlur"
            />
            <div
              v-if="
                filteredStudents.length > 0 &&
                studentName &&
                showStudentSuggestions
              "
              class="absolute top-full left-0 right-0 bg-base-100 border-2 border-base-300 rounded-xl mt-2 max-h-64 overflow-y-auto z-50 shadow-xl"
            >
              <div
                v-for="student in filteredStudents"
                :key="student.email"
                @mousedown.prevent="selectStudent(student)"
                class="p-4 hover:bg-primary/10 cursor-pointer border-b border-base-200 last:border-b-0 transition-colors"
              >
                <div class="font-semibold text-base-content">
                  {{ student.name }}
                </div>
                <div class="text-sm text-base-content/60">
                  {{ student.email }}
                </div>
              </div>
            </div>
          </div>

          <div class="form-control">
            <label class="label">
              <span class="label-text font-semibold">Student Email</span>
              <span class="label-text-alt text-error">*</span>
            </label>
            <input
              v-model="studentEmail"
              type="email"
              required
              class="input input-bordered w-full"
              placeholder="Enter student email"
            />
          </div>

          <div class="flex justify-end gap-3 mt-4">
            <button type="button" class="btn btn-ghost" @click="closeModal">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary">Submit</button>
          </div>
        </form>
      </div>
    </dialog>
    <button class="btn btn-outline btn-block" @click="openModal">
      Enter Student Information
    </button>
  </div>
</template>

<script setup lang="ts">
import fake_data from "../../public/fake_data.json";

const today = new Date();
const todayFormatted = `${
  today.getMonth() + 1
}/${today.getDate()}/${today.getFullYear()}`;

const isModalOpen = ref(false);
const dialogRef = ref<HTMLDialogElement | null>(null);

const selectedActivity = ref("");
const studentName = ref("");
const studentEmail = ref("");

const isActivityDropdownOpen = ref(false);
const activitySearchQuery = ref("");
const activityStore = useActivityStore();

const students = ref<StudentLookup[]>([]);
const showStudentSuggestions = ref(false);
let studentNameBlurTimeout: NodeJS.Timeout | null = null;

const filteredActivities = computed(() => {
  if (!activitySearchQuery.value.trim()) {
    return activityStore.activities;
  }
  return activityStore.activities.filter((activity: string) =>
    activity.toLowerCase().includes(activitySearchQuery.value.toLowerCase())
  );
});

const filteredStudents = computed(() => {
  if (!Array.isArray(students.value) || !studentName.value.trim()) {
    return [];
  }
  const searchTerm = studentName.value.toLowerCase();
  return students.value
    .filter((student) => {
      const nameMatch = student.name.toLowerCase().includes(searchTerm);
      const emailMatch = student.email.toLowerCase().includes(searchTerm);
      return nameMatch || emailMatch;
    })
    .slice(0, 10);
});

onMounted(() => {
  students.value = fake_data.map((student) => ({
    name: student.name,
    homeroom: student.homeroom,
    grad_year: student.grad_year,
    email: student.email,
    caass_id: String(student.caass_id),
    osis: student.osis,
  })) as StudentLookup[];
});

function toggleActivityDropdown() {
  isActivityDropdownOpen.value = !isActivityDropdownOpen.value;
  if (isActivityDropdownOpen.value) {
    activitySearchQuery.value = "";
  }
}

function handleActivityDropdownBlur() {
  setTimeout(() => {
    isActivityDropdownOpen.value = false;
  }, 200);
}

function selectActivity(activity: string) {
  selectedActivity.value = activity;
  isActivityDropdownOpen.value = false;
  activitySearchQuery.value = "";
}

function onStudentNameInput() {
  showStudentSuggestions.value = true;
}

function handleStudentNameBlur() {
  studentNameBlurTimeout = setTimeout(() => {
    showStudentSuggestions.value = false;
  }, 200);
}

function selectStudent(student: StudentLookup) {
  studentName.value = student.name;
  studentEmail.value = student.email;
  showStudentSuggestions.value = false;
  if (studentNameBlurTimeout) {
    clearTimeout(studentNameBlurTimeout);
  }
}

function openModal() {
  isModalOpen.value = true;
  nextTick(() => {
    if (dialogRef.value) {
      dialogRef.value.showModal();
    }
  });
}

function closeModal() {
  resetForm();
  if (dialogRef.value) {
    dialogRef.value.close();
  }
  isModalOpen.value = false;
}

function resetForm() {
  selectedActivity.value = "";
  studentName.value = "";
  studentEmail.value = "";
  activitySearchQuery.value = "";
  isActivityDropdownOpen.value = false;
  showStudentSuggestions.value = false;
}
function submitStudentData() {
  if (!selectedActivity.value) {
    return;
  }

  const studentData = {
    name: studentName.value.trim(),
    email: studentEmail.value.trim(),
    activity: selectedActivity.value,
    date: todayFormatted,
  };

  console.log("Submitting student data:", studentData);

  resetForm();
  closeModal();
}

onUnmounted(() => {
  if (studentNameBlurTimeout) {
    clearTimeout(studentNameBlurTimeout);
  }
});
</script>

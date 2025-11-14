<template>
  <attendanceModal
    v-if="showDataModal"
    :searchParams="searchParams"
    @close="showDataModal = false"
  />

  <div class="p-4 w-full">
    <button
      @click="userStore.clearUser"
      class="absolute top-3 right-3 btn btn-sm md:btn-md rounded-lg transition-transform duration-200 btn-outline"
    >
      <img src="/icons/logout.svg" class="h-4 opacity-90" alt="Search icon" />
      Logout
    </button>
    <div />
    <div class="header flex flex-col text-center gap-2 py-8">
      <h1 class="text-3xl font-bold">After-School Activity Attendence Logs</h1>
      <p class="max-w-1/2 mx-auto">
        View comprehensive attendance records for all after-school activities,
        clubs, and programs. Track student participation with detailed logs and
        historical data.
      </p>
    </div>
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
      <div class="lg:col-span-3">
        <div class="space-y-6 card card-md overflow-x-auto">
          <div class="card-body">
            <div class="flex justify-between">
              <h2 class="card-title">Student Attendance Records</h2>
              <div class="badge badge-ghost hidden md:block">
                10 activities today
              </div>
            </div>
            <table
              class="table table-zebra border-separate border-spacing-y-3 w-full"
            >
              <thead>
                <tr>
                  <th>Activity</th>
                  <th>Location</th>
                  <!-- So I dont forget make smaller width -->
                  <th>Attendance Records</th>
                  <th>Today's Attendance</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="activity in activities"
                  :key="activity"
                  class="w-full rounded-xl"
                >
                  <th class="">{{ activity }}</th>
                  <td>Room test</td>
                  <td>
                    <button
                      @click="
                        handleModal({
                          searchString: activity,
                          searchType: 'activity',
                          searchDate: selectedDate,
                        })
                      "
                      class="btn btn-sm btn-outline btn-wide"
                    >
                      Click to view
                    </button>
                  </td>
                  <td>
                    <button
                      @click="
                        handleModal({
                          searchString: activity,
                          searchType: 'activity',
                          searchDate: 'today',
                        })
                      "
                      class="btn btn-sm btn-outline btn-wide"
                    >
                      Click to view
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <div class="col-span-1 flex flex-col gap-6">
        <div class="space-y-6 card card-md mb-1">
          <div class="card-body">
            <h2 class="card-title mb-4">
              <img
                src="/icons/search.svg"
                class="h-4 opacity-50"
                alt="Search icon"
              />Search Student
            </h2>
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
            <div class="card-actions">
              <form
                class="w-full flex flex-col gap-2"
                @submit.prevent="
                  handleModal({
                    searchString: selectedStudent
                      ? selectedStudent.name
                      : studentSearch,
                    searchType: 'student',
                    searchDate: selectedDate,
                  });
                  studentSearchInputRef.blur();
                "
              >
                <label class="sr-only" for="studentSearchInputRef"
                  >Search by student name or email</label
                >
                <input
                  v-model="studentSearch"
                  v-show="!selectedStudent"
                  type="search"
                  id="studentSearchInputRef"
                  ref="studentSearchInputRef"
                  class="input w-full bg-base-200"
                  placeholder="Search student name/email"
                />
              </form>
              <button
                @click="
                  handleModal({
                    searchString: selectedStudent
                      ? selectedStudent.name
                      : studentSearch,
                    searchType: 'student',
                    searchDate: selectedDate,
                  })
                "
                class="btn btn-outline btn-block"
              >
                <img
                  src="/icons/search.svg"
                  class="h-4 opacity-50"
                  alt="Search icon"
                />Search Records
              </button>
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
            </div>
            <p class="text-error">{{ searchError }}</p>
          </div>
        </div>

        <div class="card card-md space-y-6">
          <div class="card-body">
            <h2 class="card-title">Select Date</h2>
            <div class="card-actions">
              <form
                @submit.prevent
                class="flex w-full justify-center items-center gap-2 relative border rounded-xl overflow-hidden"
              >
                <div
                  class="absolute inset-y-0 left-0 bg-primary/70 transition-transform duration-300 ease-in-out w-1/2 rounded-xl shadow-md"
                  :class="isDateSelected ? 'translate-x-full' : 'translate-x-0'"
                ></div>

                <div class="flex py-1 justify-around w-full relative z-10">
                  <button
                    type="button"
                    class="flex-1 text-xl font-bold cursor-pointer text-center"
                    @click="isDateSelected = false"
                    :class="!isDateSelected ? 'text-base-200' : ''"
                  >
                    None
                  </button>
                  <button
                    type="button"
                    class="flex-1 text-xl font-bold cursor-pointer text-center"
                    @click="isDateSelected = true"
                    :class="isDateSelected ? 'text-base-200' : ''"
                  >
                    Select
                  </button>
                </div>
              </form>
              <div v-if="isDateSelected" class="card w-full p-6 space-y-4">
                <label class="text-sm font-semibold text-base-content/70">
                  Filter by date
                </label>
                <div class="w-full flex gap-2">
                  <input
                    v-model="selectedDate"
                    type="date"
                    class="input input-bordered"
                  />
                </div>
              </div>
              <p
                v-if="!isDateSelected"
                class="text-sm text-center text-base-content/70"
              >
                Showing attendance for every date.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import fake_data from "../../public/fake_data.json";
const showDataModal = ref(false);
const studentSearch = ref("");
const searchError = ref("");
const studentSearchInputRef = ref();
const searchParams = ref({
  searchString: "",
  searchType: "",
  searchDate: "",
});
const isDateSelected = ref(false);
const selectedDate = ref("");
const students = ref<StudentLookup[]>([]);
const selectedStudent = ref<{
  name: string;
  email: string;
  display: string;
} | null>(null);
const config = useRuntimeConfig();

const activities = [
  "FTC Robotics",
  "Town Hall Meeting",
  "Science Fair",
  "Math Olympiad",
  "Art Exhibition",
  "Debate Club",
  "Photography Club",
  "Music Rehearsal",
  "Swimming Practice",
  "Football Practice",
];
const userStore = useUserStore();

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

function handleModal(params: SearchParams) {
  if (params.searchType === "student" && params.searchString === "") {
    searchError.value = "Please enter name/email of student";
    return;
  }
  searchError.value = "";
  if (!isDateSelected.value && params.searchDate !== "today") {
    params.searchDate = "";
  } else if (params.searchDate === "today") {
    params.searchDate = new Date().toLocaleDateString("en-US");
  } else {
    const [year, month, day] = params.searchDate.split("-");
    if (year && month && day) {
      params.searchDate = new Date(
        parseInt(year),
        parseInt(month) - 1,
        parseInt(day)
      ).toLocaleDateString("en-US");
    }
  }
  searchParams.value = params;

  showDataModal.value = true;
}

const fetchLookup = async () => {
  try {
    const response = await fetch(
      `${config.public.backendUrl}/students/lookup/`,
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data = await response.json();
    students.value = data.students_data;
  } catch (error) {
    console.error("Error fetching students:", error);
  }
};

/*
TEMPORARY DATA
 */
students.value = fake_data.map((student) => ({
  name: student.name,
  homeroom: student.homeroom,
  grad_year: student.grad_year,
  email: student.email,
  caass_id: String(student.caass_id),
  osis: student.osis,
})) as StudentLookup[];

onMounted(() => {
  //calls();
  //setInterval(calls, 5);
});

function calls() {
  fetchLookup();
}
</script>

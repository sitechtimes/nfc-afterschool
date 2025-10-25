<template>
  <attendanceModal
    v-if="showDataModal"
    :searchParams="searchParams"
    @close="showDataModal = false"
  />

  <div class="p-4 w-full">
    <button
      @click="userStore.clearUser"
      class="absolute top-0 left-0 w-10 btn btn-primary"
    >
      test logout
    </button>
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
        <div class="space-y-1 card card-md overflow-x-auto">
          <div class="card-body">
            <div class="flex justify-between">
              <h2 class="card-title">Avatar Attendance Records</h2>
              <div class="badge badge-ghost hidden md:block">
                10 activities today
              </div>
            </div>
            <table class="table table-zebra">
              <thead>
                <tr>
                  <th>Activity</th>
                  <th>Full Attendance Records</th>
                  <th>Today's Attendance</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="activity in activities" :key="activity">
                  <th>{{ activity }}</th>
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
        <div class="card card-md mb-1">
          <div class="card-body justify-center items-center">
            <h2 class="card-title">Manual Student Input</h2>
          </div>
          <div class="card-actions justify-center items-center">
            <EnterStudentInfo />
          </div>
        </div>
        <div class="space-y-6 card card-md mb-1">
          <div class="card-body">
            <h2 class="card-title mb-4">
              <img
                src="/icons/search.svg"
                class="h-[1em] opacity-50"
                alt="Search icon"
              />Search Student
            </h2>
            <div class="card-actions">
              <form
                class="w-full flex flex-col gap-2"
                @submit.prevent="
                  handleModal({
                    searchString: studentSearch,
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
                    searchString: studentSearch,
                    searchType: 'student',
                    searchDate: selectedDate,
                  })
                "
                class="btn btn-outline btn-block"
              >
                <img
                  src="/icons/search.svg"
                  class="h-[1em] opacity-50"
                  alt="Search icon"
                />Search Records
              </button>
              <p class="text-error">{{ searchError }}</p>
            </div>
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
</script>

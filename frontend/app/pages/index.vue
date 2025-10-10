<template>
  <attendanceModal
    v-if="showDataModal"
    :searchParams="searchParams"
    @close="showDataModal = false"
  />

  <div class="mainpage w-full">
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
                          searchDate: '',
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
                          searchDate: '',
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
      <div class="col-span-1">
        <div class="space-y-6 card card-md">
          <div class="card-body">
            <h2 class="card-title mb-4">
              <svg
                class="h-[1em] opacity-50"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
              >
                <g
                  stroke-linejoin="round"
                  stroke-linecap="round"
                  stroke-width="2.5"
                  fill="none"
                  stroke="currentColor"
                >
                  <circle cx="11" cy="11" r="8"></circle>
                  <path d="m21 21-4.3-4.3"></path>
                </g></svg
              >Search Student
            </h2>
            <div class="card-actions">
              <form
                class="w-full"
                @submit.prevent="
                  handleModal({
                    searchString: studentSearch,
                    searchType: 'student',
                    searchDate: '',
                  });
                  studentSearchInputRef.blur();
                "
              >
                <input
                  v-model="studentSearch"
                  type="search"
                  ref="studentSearchInputRef"
                  class="input w-full bg-base-200"
                  placeholder="Search student name/email/cassid"
                />
              </form>
              <button
                @click="
                  handleModal({
                    searchString: studentSearch,
                    searchType: 'student',
                    searchDate: '',
                  })
                "
                class="btn btn-outline btn-block"
              >
                <svg
                  class="h-[1em] opacity-50"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                >
                  <g
                    stroke-linejoin="round"
                    stroke-linecap="round"
                    stroke-width="2.5"
                    fill="none"
                    stroke="currentColor"
                  >
                    <circle cx="11" cy="11" r="8"></circle>
                    <path d="m21 21-4.3-4.3"></path>
                  </g></svg
                >Search Records
              </button>
              <p class="text-error">{{ searchError }}</p>
              <h2 class="text-center w-full text-3xl font-semibold">
                Select Date
              </h2>
              <form
                @submit.prevent
                class="flex w-full justify-center items-center gap-2 relative border rounded-xl overflow-hidden"
              >
                <div
                  class="absolute inset-y-0 left-0 bg-primary/70 transition-transform duration-300 ease-in-out w-1/2 rounded-xl shadow-md"
                  :class="isDateSelected ? 'translate-x-full' : 'translate-x-0'"
                ></div>

                <div class="flex py-3 px-2 justify-around w-full relative z-10">
                  <button
                    type="button"
                    class="flex-1 text-xl font-bold cursor-pointer text-center"
                    @click="isDateSelected = false"
                  >
                    No Date
                  </button>
                  <button
                    type="button"
                    class="flex-1 text-xl font-bold cursor-pointer text-center"
                    @click="isDateSelected = true"
                  >
                    Select Date
                  </button>
                </div>
              </form>
              <transition name="fade">
                <div v-if="isDateSelected" class="card w-full p-6 space-y-4">
                  <label class="text-sm font-semibold text-base-content/70">
                    Filter by date
                  </label>
                  <input
                    v-model="selectedDate"
                    type="date"
                    class="input input-bordered w-full"
                  />
                  <button
                    type="button"
                    class="btn btn-sm btn-ghost"
                    @click="selectedDate = ''"
                  >
                    Clear date
                  </button>
                </div>
              </transition>
              <div></div>
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

function handleModal(params: SearchParams) {
  if (params.searchType === "student" && params.searchString === "") {
    searchError.value = "Please enter name/email/cassid of student";
    return;
  }
  searchError.value = "";
  searchParams.value = params;
  showDataModal.value = true;
}
</script>

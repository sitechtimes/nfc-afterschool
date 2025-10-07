<template>
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
        <div class="space-y-6 card card-md">
          <div class="card-body">
            <div class="flex justify-between">
              <h2 class="card-title">Avatar Attendance Records</h2>
              <div class="badge badge-ghost hidden md:block">
                10 activities today
              </div>
            </div>
          </div>
        </div>
      </div>
      <div>
        <div></div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
const temp = ref(false);
</script>

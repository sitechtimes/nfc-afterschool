<template>
    <attendanceModal
        v-if="showDataModal"
        :search="selectedModalSearch"
        @close="showDataModal = false"
    />

    <div class="mainpage p-4 w-full">
        <button
            @click="userStore.clearUser()"
            class="absolute top-0 left-0 w-10 btn btn-primary"
        >
            test logout
        </button>
        <div class="header flex flex-col text-center gap-2 py-8">
            <h1 class="text-3xl font-bold">
                After-School Activity Attendence Logs
            </h1>
            <p class="max-w-1/2 mx-auto">
                View comprehensive attendance records for all after-school
                activities, clubs, and programs. Track student participation
                with detailed logs and historical data.
            </p>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
            <div class="lg:col-span-3">
                <div class="space-y-6 card card-md overflow-x-auto">
                    <div class="card-body">
                        <div class="flex justify-between">
                            <h2 class="card-title">
                                Avatar Attendance Records
                            </h2>
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
                                <tr
                                    v-for="activity in activities"
                                    :key="activity"
                                >
                                    <th>{{ activity }}</th>
                                    <td>
                                        <button
                                            @click="
                                                handleModal(
                                                    activity,
                                                    'activity'
                                                )
                                            "
                                            class="btn btn-sm btn-outline btn-wide"
                                        >
                                            Click to view
                                        </button>
                                    </td>
                                    <td>
                                        <button
                                            @click="
                                                handleModal(
                                                    activity,
                                                    'activity'
                                                )
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
                                    handleModal(studentSearch, 'student');
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
                                @click="handleModal(studentSearch, 'student')"
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
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useUserStore } from "~/stores/userStore";

const showDataModal = ref(false);
const selectedModalSearch = ref("");
const studentSearch = ref("");
const searchError = ref("");
const studentSearchInputRef = ref();
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

function handleModal(searchString: string, searchType: string) {
    //console.log(searchString, searchType);
    if (searchType === "student" && searchString === "") {
        searchError.value = "Please enter name/email/cassid of student";
        return;
    }
    searchError.value = "";
    //ONCE TYPESCRIPT WORKS ADD SOMETHING TO MAKE SURE U CAN SEARCH FOR SPECIFICALLY TODAY
    selectedModalSearch.value = searchString;
    showDataModal.value = true;
}
</script>

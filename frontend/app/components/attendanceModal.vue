<template>
  <dialog class="modal modal-open cursor-pointer" @click.self="$emit('close')">
    <div
      class="modal-box cursor-default max-w-5xl w-11/12 max-h-screen overflow-auto"
    >
      <table class="table">
        <thead>
          <tr>
            <th>Activity</th>
            <th>Date</th>
            <th>Student Name</th>
            <th>Student Email</th>
            <th>Student CASSID</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="instance in filteredData" :key="instance.student_cassid">
            <th>{{ instance.activity }}</th>
            <td>{{ instance.date }}</td>
            <td>{{ instance.student_name }}</td>
            <td>{{ instance.student_email }}</td>
            <td>{{ instance.student_cassid }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </dialog>
</template>

<script setup lang="ts">
import data from "../assets/fake_data.json";
const props = defineProps({ searchParams: { type: Object, required: true } });
console.log(props.searchParams);
const filteredData = computed(() => {
  if (!props.searchParams) return data;
  return data.filter(
    (item) =>
      (props.searchParams.searchType === "student"
        ? item.student_name
            ?.toLowerCase()
            .includes(props.searchParams.searchString.toLowerCase())
        : false) ||
      (props.searchParams.searchType === "student"
        ? item.student_email
            ?.toLowerCase()
            .includes(props.searchParams.searchString.toLowerCase())
        : false) ||
      // item.student_cassid
      //   ?.toString()
      //   .toLowerCase()
      //   .includes(props.search.toLowerCase()) ||
      (props.searchParams.searchType === "activity"
        ? item.activity
            ?.toLowerCase()
            .includes(props.searchParams.searchString.toLowerCase())
        : false)
  );
});
</script>

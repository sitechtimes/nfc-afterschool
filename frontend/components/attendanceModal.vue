<template>
  <dialog class="modal modal-open cursor-pointer" @click.self="$emit('close')">
    <div class="modal-box cursor-default max-w-3/4">
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

<script setup>
import data from "../assets/fake_data.json";
const props = defineProps({ search: { type: String, required: true } });

const filteredData = computed(() => {
  if (!props.search) return data;
  return data.filter(
    (item) =>
      item.studentName?.toLowerCase().includes(props.search.toLowerCase()) ||
      item.studentEmail?.toLowerCase().includes(props.search.toLowerCase()) ||
      item.studentCASSID?.toLowerCase().includes(props.search.toLowerCase()) ||
      item.activity?.toLowerCase().includes(props.search.toLowerCase())
  );
});
</script>

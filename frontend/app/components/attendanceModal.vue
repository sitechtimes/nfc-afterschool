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
            <td>{{ instance.studentName }}</td>
            <td>{{ instance.studentEmail }}</td>
            <!--fix tis-->
            <td>{{ instance.studentCaassID }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </dialog>
</template>

<script setup lang="ts">
const emit = defineEmits(["close"]);
const props = defineProps({
  searchParams: { type: Object, required: true },
  data: { type: Object, required: true }, //scaninstances
});
const filteredData = computed(() => {
  if (!props.searchParams) return props.data;
  return props.data.filter(
    (item: ScanInstance) =>
      (props.searchParams.searchDate === "" ||
        item.date === props.searchParams.searchDate) &&
      (props.searchParams.searchType !== "student" ||
        item.studentName
          ?.toLowerCase()
          .includes(props.searchParams.searchString.toLowerCase()) ||
        item.studentEmail
          ?.toLowerCase()
          .includes(props.searchParams.searchString.toLowerCase())) &&
      (props.searchParams.searchType !== "activity" ||
        item.activity
          ?.toLowerCase()
          .includes(props.searchParams.searchString.toLowerCase()))
  );
});

function onKeydown(e: KeyboardEvent) {
  if (e?.key === "Escape" || e?.code === "Escape") {
    emit("close");
  }
}

onMounted(() => window.addEventListener("keydown", onKeydown));
onBeforeUnmount(() => window.removeEventListener("keydown", onKeydown));
</script>

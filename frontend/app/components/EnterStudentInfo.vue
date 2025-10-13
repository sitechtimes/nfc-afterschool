<template>
  <div class="relative">
    <div
      v-if="IsEnterInfoScreenOpen"
      class="fixed inset-0 bg-black/40 backdrop-blur-sm z-40"
    ></div>


    <dialog
      ref="dialog"
      id="dialog"
      class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 
             z-50 bg-white rounded-lg p-6 shadow-xl w-[90%] max-w-md"

    >
      <form method="dialog" @submit.prevent="NeedDataToClose" class="flex flex-col gap-4">
        <p>
          <label class="flex flex-col text-gray-700">
            Name:
            <input
              v-model="studentName"
              type="text"
              required
              class="border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
            />
          </label>
          <label class="flex flex-col text-gray-700">
           	Student Email:
            <input
              type="text"
              v-model="studentEmail"
              required
              class="border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
            />
          </label>
        </p>
        <div class="flex justify-end gap-2">
          <input
            type="submit"
            class="bg-blue-100 hover:bg-blue-200 text-blue-700 px-4 py-2 rounded-md cursor-pointer"
            value="Submit"
          />
          <input
            type="button"
            class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md cursor-pointer"
            @click="CloseWithoutData"
            value="Close 2"
          />
        </div>
      </form>
    </dialog>
    <p class="text-center mt-6">
      <button
        class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg shadow-md"
        @click="OpenInfoEnterPage"
      >
        Enter student information
      </button>
    </p>
  </div>
</template>

<script setup>
import { ref } from "vue";


const Today = new Date();
const TodayFormatted = `${Today.getMonth() + 1}/${Today.getDate()}/${Today.getFullYear()}`;
const IsEnterInfoScreenOpen = ref(false);
const dialog = ref(null);
const studentName = ref("");
const studentEmail = ref("");

function OpenInfoEnterPage() {
  dialog.value.showModal();
  IsEnterInfoScreenOpen.value = true;
}

function CloseWithoutData() {
  dialog.value.close();
  IsEnterInfoScreenOpen.value = false;
}
/* Go over with ben which button would work better for the project | Comment so I dont forget */
function NeedDataToClose() {
  console.log("Student Name:", studentName.value);
  console.log("Student Email:", studentEmail.value);
  studentName.value = ""
  studentEmail.value = ""
  IsEnterInfoScreenOpen.value = false;
  dialog.value.close();
  /* makes blur go away but keps the form up  */
}


</script>

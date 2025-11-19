export const useUserStore = defineStore("user", () => {
  const logged = ref(
    typeof window !== "undefined" ? localStorage.getItem("token") : null
  );

  const clearUser = () => {
    logged.value = null;
    if (typeof window !== "undefined") {
      localStorage.removeItem("token");
    }
  };

  return {
    logged,
    clearUser,
  };
});

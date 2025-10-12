export const useUserStore = defineStore("user", () => {
  const user = ref<User | null>(null);

  function setUser(userData: User) {
    user.value = userData;
    localStorage.setItem("user", JSON.stringify(user.value));
  }

  function getUser() {
    const token = localStorage.getItem("user");
    if (token !== null && user.value === null) {
      setUser(token);
    } else if (token === null) {
      clearUser();
    }
  }
  function clearUser() {
    user.value = null;
    navigateTo("/login");
    localStorage.clear();
  }

  return {
    user,
    setUser,
    clearUser,
    getUser,
  };
});

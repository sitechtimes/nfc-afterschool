export const useUserStore = defineStore("user", () => {
    const user = ref<User | null>({
        username: "",
        role: "",
    });
    const isAuthenticated = ref(false);

    function setUser(userData: User) {
        user.value = userData;
        isAuthenticated.value = !!userData;
        localStorage.setItem("user", user.value.username);
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
        isAuthenticated.value = false;
        localStorage.clear();
    }

    return {
        user,
        isAuthenticated,
        setUser,
        clearUser,
        getUser,
    };
});

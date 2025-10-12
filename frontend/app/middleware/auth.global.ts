export default defineNuxtRouteMiddleware((to) => {
    if (typeof window === "undefined") return;
    const user = localStorage.getItem("user");
    if (!user && to.path !== "/login") {
        return navigateTo("/login");
    }
    if (user && to.path === "/login") {
        return navigateTo("/");
    }
});

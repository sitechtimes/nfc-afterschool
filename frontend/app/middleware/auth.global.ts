export default defineNuxtRouteMiddleware(async (to) => {
  if (typeof window === "undefined") return;

  const token = localStorage.getItem("token");

  if (to.name === "login") {
    if (token) {
      return navigateTo("/");
    }
    return;
  }

  if (!token) {
    return navigateTo("/login");
  }
});

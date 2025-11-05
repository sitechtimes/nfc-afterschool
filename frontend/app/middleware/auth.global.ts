export default defineNuxtRouteMiddleware(async (to) => {
  if (typeof window === "undefined") return;
  const config = useRuntimeConfig();

  async function checkAuth() {
    const backendUrl = config.public.backendUrl;
    if (!backendUrl || backendUrl === "undefined") {
      console.error("Backend URL not configured");
      return false;
    }

    try {
      const response = await fetch(`${backendUrl}/api/token/`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      if (!response.ok) {
        throw new Error(`Failed. Status: ${response.status}`);
      }
      console.log(response);
    } catch (error) {
      console.error("Error:", error);
      return false;
    }
    return true;
  }

  onBeforeRouteUpdate(async (to, from, next) => {
    const isAuthenticated = await checkAuth();

    if (to.meta.requiresAuth && !isAuthenticated) {
      next({ name: "login" });
    } else {
      next();
    }
  });
});

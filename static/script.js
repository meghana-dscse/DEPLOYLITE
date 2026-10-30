// Update the live indicator only after the health endpoint responds.
document.addEventListener("DOMContentLoaded", async () => {
  const indicator = document.querySelector(".updated");
  if (!indicator) return;
  try {
    const response = await fetch("/health", { cache: "no-store" });
    const health = await response.json();
    if (!response.ok || health.status !== "healthy") throw new Error("Health check failed");
    indicator.lastChild.textContent = " Healthy · checked just now";
  } catch {
    indicator.innerHTML = '<span class="status-dot" style="background:#f0a66f;box-shadow:none"></span> Health check unavailable';
  }
});

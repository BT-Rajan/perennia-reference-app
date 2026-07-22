<template>
  <main class="page-content">
    <p class="badge-eyebrow">reports.view</p>
    <h2>Reports</h2>
    <div class="card" v-if="message">
      <p>{{ message }}</p>
      <p class="dim">
        No real report data lives here - this page exists to demonstrate that
        <PermissionChip code="reports.view" granted /> gated the request on the backend.
      </p>
    </div>
    <AlertBanner v-if="errorMessage" :message="errorMessage" />
  </main>
</template>

<script setup>
import { onMounted, ref } from "vue";
import AlertBanner from "../components/AlertBanner.vue";
import PermissionChip from "../components/PermissionChip.vue";
import { apiFetch, ApiError } from "../services/api";

const message = ref("");
const errorMessage = ref("");

onMounted(async () => {
  try {
    const result = await apiFetch("/api/reports");
    message.value = result.message;
  } catch (err) {
    errorMessage.value = err instanceof ApiError ? err.message : "Something went wrong. Please try again.";
  }
});
</script>

<style scoped>
.dim {
  color: var(--color-slate-500);
  font-size: var(--text-sm);
  margin-bottom: 0;
}
</style>

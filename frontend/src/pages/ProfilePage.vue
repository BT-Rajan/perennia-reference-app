<template>
  <main class="page-content">
    <p class="badge-eyebrow">profile.view</p>
    <h2>Profile</h2>
    <div class="card" v-if="profile">
      <p><strong>Subject:</strong> <code class="mono">{{ profile.subject_id }}</code></p>
      <p><strong>Roles:</strong> {{ profile.roles.join(", ") || "none" }}</p>
      <p class="dim">
        This page is reachable because your identity carries <PermissionChip code="profile.view" granted /> -
        checked on the backend by perennia-access, not inferred from anything the frontend shows or hides.
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

const profile = ref(null);
const errorMessage = ref("");

onMounted(async () => {
  try {
    profile.value = await apiFetch("/api/profile");
  } catch (err) {
    errorMessage.value = err instanceof ApiError ? err.message : "Something went wrong. Please try again.";
  }
});
</script>

<style scoped>
.dim {
  color: var(--color-slate-500);
  font-size: var(--text-sm);
  margin-top: var(--space-5);
  margin-bottom: 0;
}
</style>

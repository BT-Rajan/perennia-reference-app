<template>
  <main class="page-content">
    <p class="badge-eyebrow">Signed in</p>
    <h2>Welcome back</h2>
    <p class="identity-line">
      Subject <code class="mono">{{ home?.subject_id }}</code>
      <span v-if="home?.roles?.length"> &middot; role: {{ home.roles.join(", ") }}</span>
    </p>

    <AlertBanner v-if="errorMessage" :message="errorMessage" />

    <div v-if="home" class="area-grid">
      <router-link
        v-for="area in home.areas"
        :key="area.key"
        :to="area.available ? area.path : ''"
        class="area-card"
        :class="{ 'is-locked': !area.available }"
        @click="area.available || $event.preventDefault()"
      >
        <h3>{{ area.label }}</h3>
        <PermissionChip :code="area.permission" :granted="area.available" />
      </router-link>
    </div>
  </main>
</template>

<script setup>
import { onMounted, ref } from "vue";
import AlertBanner from "../components/AlertBanner.vue";
import PermissionChip from "../components/PermissionChip.vue";
import { apiFetch, ApiError } from "../services/api";

const home = ref(null);
const errorMessage = ref("");

onMounted(async () => {
  try {
    home.value = await apiFetch("/api/home");
  } catch (err) {
    errorMessage.value = err instanceof ApiError ? err.message : "Something went wrong. Please try again.";
  }
});
</script>

<style scoped>
.identity-line {
  margin-bottom: var(--space-6);
}
</style>

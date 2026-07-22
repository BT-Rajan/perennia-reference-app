<template>
  <main class="page-content">
    <div class="center-column">
      <h2>Verify email</h2>
      <div class="card">
        <AlertBanner v-if="errorMessage" :message="errorMessage" />
        <AlertBanner v-if="successMessage" type="success" :message="successMessage" />
        <p v-if="!errorMessage && !successMessage">Verifying your email...</p>
        <router-link v-if="successMessage" to="/login" class="btn btn-primary btn-block">Sign in</router-link>
      </div>
    </div>
  </main>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import AlertBanner from "../components/AlertBanner.vue";
import { apiFetch, ApiError } from "../services/api";

const route = useRoute();
const errorMessage = ref("");
const successMessage = ref("");

onMounted(async () => {
  const token = route.query.token;
  if (!token) {
    errorMessage.value = "This link is missing a verification token.";
    return;
  }
  try {
    const result = await apiFetch("/api/auth/verify-email", { method: "POST", body: { token }, auth: false });
    successMessage.value = result.message;
  } catch (err) {
    errorMessage.value = err instanceof ApiError ? err.message : "Something went wrong. Please try again.";
  }
});
</script>

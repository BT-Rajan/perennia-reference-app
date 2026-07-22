<template>
  <main class="page-content">
    <div class="center-column">
      <h2>Reset password</h2>
      <div class="card">
        <AlertBanner v-if="errorMessage" :message="errorMessage" />
        <AlertBanner v-if="successMessage" type="success" :message="successMessage" />

        <form v-if="!successMessage" @submit.prevent="onSubmit" novalidate>
          <div class="field">
            <label for="new_password">New password</label>
            <input id="new_password" v-model="newPassword" type="password" autocomplete="new-password" required />
            <p class="field-hint">At least 10 characters, with an uppercase letter, a lowercase letter, and a digit.</p>
          </div>
          <button type="submit" class="btn btn-primary btn-block" :disabled="submitting">
            {{ submitting ? "Resetting..." : "Reset password" }}
          </button>
        </form>

        <p class="below-form">
          <router-link to="/login">Back to sign in</router-link>
        </p>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref } from "vue";
import { useRoute } from "vue-router";
import AlertBanner from "../components/AlertBanner.vue";
import { apiFetch, ApiError } from "../services/api";

const route = useRoute();
const token = route.query.token || "";

const newPassword = ref("");
const submitting = ref(false);
const errorMessage = ref("");
const successMessage = ref("");

async function onSubmit() {
  errorMessage.value = "";
  submitting.value = true;
  try {
    const result = await apiFetch("/api/auth/reset-password", {
      method: "POST",
      body: { token, new_password: newPassword.value },
      auth: false,
    });
    successMessage.value = result.message;
  } catch (err) {
    errorMessage.value = err instanceof ApiError ? err.message : "Something went wrong. Please try again.";
  } finally {
    submitting.value = false;
  }
}
</script>

<style scoped>
.below-form {
  margin: var(--space-5) 0 0;
  font-size: var(--text-sm);
  text-align: center;
}
</style>

<template>
  <main class="page-content">
    <div class="center-column">
      <h2>Forgot password</h2>
      <div class="card">
        <AlertBanner v-if="errorMessage" :message="errorMessage" />
        <AlertBanner v-if="successMessage" type="success" :message="successMessage" />

        <form v-if="!successMessage" @submit.prevent="onSubmit" novalidate>
          <div class="field">
            <label for="email">Email</label>
            <input id="email" v-model="email" type="email" autocomplete="email" required />
          </div>
          <button type="submit" class="btn btn-primary btn-block" :disabled="submitting">
            {{ submitting ? "Sending..." : "Send reset instructions" }}
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
import AlertBanner from "../components/AlertBanner.vue";
import { apiFetch, ApiError } from "../services/api";

const email = ref("");
const submitting = ref(false);
const errorMessage = ref("");
const successMessage = ref("");

async function onSubmit() {
  errorMessage.value = "";
  submitting.value = true;
  try {
    // The backend gives the same generic response whether or not the
    // address exists - this page shows exactly that response, unmodified.
    const result = await apiFetch("/api/auth/forgot-password", {
      method: "POST",
      body: { email: email.value },
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

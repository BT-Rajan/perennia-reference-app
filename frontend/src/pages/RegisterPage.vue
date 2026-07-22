<template>
  <main class="page-content">
    <div class="center-column">
      <h2>Create an account</h2>
      <div class="card">
        <AlertBanner v-if="errorMessage" :message="errorMessage" />
        <AlertBanner v-if="successMessage" type="success" :message="successMessage" />

        <form v-if="!successMessage" @submit.prevent="onSubmit" novalidate>
          <div class="field">
            <label for="email">Email</label>
            <input id="email" v-model="email" type="email" autocomplete="email" required />
          </div>
          <div class="field">
            <label for="password">Password</label>
            <input id="password" v-model="password" type="password" autocomplete="new-password" required />
            <p class="field-hint">At least 10 characters, with an uppercase letter, a lowercase letter, and a digit.</p>
          </div>
          <div class="field">
            <label for="role">Role (demo)</label>
            <select id="role" v-model="role">
              <option v-for="opt in roleOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
            </select>
            <p class="field-hint">
              This reference app lets you pick a role to explore. In a real application, roles are assigned by an
              administrator, not chosen at sign-up.
            </p>
          </div>
          <button type="submit" class="btn btn-primary btn-block" :disabled="submitting">
            {{ submitting ? "Creating account..." : "Create account" }}
          </button>
        </form>

        <p class="below-form">
          <router-link to="/login">Already have an account? Sign in</router-link>
        </p>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref } from "vue";
import AlertBanner from "../components/AlertBanner.vue";
import { register, ApiError } from "../state/auth";

const roleOptions = [
  { value: "employee", label: "Employee" },
  { value: "manager", label: "Manager" },
  { value: "administrator", label: "Administrator" },
];

const email = ref("");
const password = ref("");
const role = ref("employee");
const submitting = ref(false);
const errorMessage = ref("");
const successMessage = ref("");

async function onSubmit() {
  errorMessage.value = "";
  submitting.value = true;
  try {
    const result = await register(email.value, password.value, role.value);
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

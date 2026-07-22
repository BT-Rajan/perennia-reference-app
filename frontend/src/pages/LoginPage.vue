<template>
  <main class="page-content">
    <div class="center-column">
      <h2>Sign in</h2>
      <div class="card">
        <AlertBanner v-if="errorMessage" :message="errorMessage" />
        <form @submit.prevent="onSubmit" novalidate>
          <div class="field">
            <label for="email">Email</label>
            <input id="email" v-model="email" type="email" autocomplete="email" required />
          </div>
          <div class="field">
            <label for="password">Password</label>
            <input id="password" v-model="password" type="password" autocomplete="current-password" required />
          </div>
          <button type="submit" class="btn btn-primary btn-block" :disabled="submitting">
            {{ submitting ? "Signing in..." : "Sign in" }}
          </button>
        </form>
        <p class="below-form">
          <router-link to="/forgot-password">Forgot password?</router-link>
          &middot;
          <router-link to="/register">Create an account</router-link>
        </p>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import AlertBanner from "../components/AlertBanner.vue";
import { login, ApiError } from "../state/auth";

const router = useRouter();
const route = useRoute();

const email = ref("");
const password = ref("");
const submitting = ref(false);
const errorMessage = ref("");

async function onSubmit() {
  errorMessage.value = "";
  submitting.value = true;
  try {
    await login(email.value, password.value);
    router.push(route.query.next || "/home");
  } catch (err) {
    // Deliberately identical wording for "no such account" and "wrong
    // password" - perennia-auth never distinguishes the two, and neither
    // does this page.
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

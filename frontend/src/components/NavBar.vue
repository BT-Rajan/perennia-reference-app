<template>
  <nav class="app-nav">
    <div class="app-nav-inner">
      <router-link to="/" class="app-nav-brand">ABC Enterprises</router-link>
      <div class="app-nav-links">
        <template v-if="authState.ready && authState.subjectId">
          <router-link to="/home">Home</router-link>
          <router-link v-if="hasPermission('profile.view')" to="/profile">Profile</router-link>
          <router-link v-if="hasPermission('reports.view')" to="/reports">Reports</router-link>
          <router-link v-if="hasPermission('admin.access')" to="/administration">Administration</router-link>
          <button type="button" @click="onSignOut">Sign out</button>
        </template>
        <template v-else>
          <router-link to="/login">Login</router-link>
          <router-link to="/register">Register</router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from "vue-router";
import { authState, hasPermission, logout } from "../state/auth";

const router = useRouter();

async function onSignOut() {
  await logout();
  router.push("/login");
}
</script>

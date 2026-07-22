<template>
  <main class="page-content">
    <div class="center-column denied-column">
      <p class="badge-eyebrow">403</p>
      <h2>Access denied</h2>
      <div class="card">
        <p>
          You're signed in, but your account doesn't carry the permission this area requires. This is not a
          sign-in problem - your session is fine.
        </p>
        <p class="dim">If you believe this is a mistake, contact an administrator to review your role.</p>
        <router-link to="/home" class="btn btn-primary btn-block">Back to home</router-link>
      </div>
    </div>
  </main>
</template>

<script setup></script>

<style scoped>
.denied-column {
  padding-top: var(--space-7);
}

.dim {
  color: var(--color-slate-500);
  font-size: var(--text-sm);
}
</style>

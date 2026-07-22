<template>
  <main class="page-content">
    <section class="hero">
      <p class="badge-eyebrow">Perennia reference application</p>
      <h1>ABC Enterprises</h1>
      <p class="hero-sub">
        A small, real operating environment for people at ABC Enterprises - built to show exactly how
        authentication and authorization stay separate, and how every action is checked against a permission,
        not a role name.
      </p>
      <div class="hero-actions">
        <router-link to="/login" class="btn btn-primary">Sign in</router-link>
        <router-link to="/register" class="btn btn-accent">Create an account</router-link>
        <router-link to="/forgot-password" class="btn btn-ghost">Forgot password</router-link>
      </div>
    </section>

    <section class="layer-grid">
      <div class="card layer-card">
        <p class="badge-eyebrow">Layer 1</p>
        <h3>perennia-auth</h3>
        <p>Confirms who you are: registration, sign-in, sessions, and password recovery.</p>
      </div>
      <div class="card layer-card">
        <p class="badge-eyebrow">Layer 2</p>
        <h3>perennia-access</h3>
        <p>Decides what you may do, by checking your permissions - never by checking your role name.</p>
      </div>
      <div class="card layer-card">
        <p class="badge-eyebrow">Layer 3</p>
        <h3>This application</h3>
        <p>Defines the areas of ABC Enterprises and asks the two layers above for every answer.</p>
      </div>
    </section>
  </main>
</template>

<script setup></script>

<style scoped>
.hero {
  padding: var(--space-8) 0 var(--space-7);
  max-width: 640px;
}

.hero-sub {
  font-size: var(--text-lg);
  line-height: var(--leading-snug);
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
  margin-top: var(--space-6);
}

.layer-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-5);
  padding-bottom: var(--space-8);
}

.layer-card p:last-child {
  margin-bottom: 0;
}

@media (max-width: 900px) {
  .layer-grid {
    grid-template-columns: 1fr;
  }
}
</style>

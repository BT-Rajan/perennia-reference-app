<template>
  <main class="page-content">
    <p class="badge-eyebrow">search.execute</p>
    <h2>Search</h2>
    <p class="dim intro">
      Full-text search across indexed business resources, backed by <code class="mono">perennia-search</code>.
    </p>

    <AlertBanner v-if="errorMessage" :message="errorMessage" />

    <div class="card">
      <form @submit.prevent="runSearch" class="search-form">
        <div class="field search-field">
          <label for="q">Query</label>
          <input id="q" v-model="query" type="text" placeholder="e.g. acme" autocomplete="off" />
        </div>
        <div class="field resource-field">
          <label for="resource">Resource</label>
          <select id="resource" v-model="resourceFilter">
            <option value="">All resources</option>
            <option value="customer">Customer</option>
            <option value="company">Company</option>
            <option value="document">Document</option>
          </select>
        </div>
        <button type="submit" class="btn btn-primary" :disabled="searching || !query.trim()">
          {{ searching ? "Searching..." : "Search" }}
        </button>
      </form>
    </div>

    <div v-if="results" class="card results-card">
      <p class="dim">
        {{ results.total }} result{{ results.total === 1 ? "" : "s" }} for
        <strong>"{{ results.query }}"</strong>
      </p>
      <ul v-if="results.results.length" class="result-list">
        <li v-for="r in results.results" :key="`${r.resource}-${r.entity_id}`" class="result-row">
          <span class="permission-chip is-granted">{{ r.resource }}</span>
          <span class="result-title">{{ r.title }}</span>
          <span class="dim result-score">score {{ r.score.toFixed(2) }}</span>
        </li>
      </ul>
      <p v-else class="dim">
        No matches - this reference endpoint returns real shapes with no seeded index data, so an
        empty result set here means the wiring works end to end.
      </p>
    </div>

    <div class="card" v-if="hasPermission('search.manage')">
      <p class="badge-eyebrow">search.manage</p>
      <h3>Registered resources</h3>
      <button type="button" class="btn btn-ghost" @click="loadResources" :disabled="loadingResources">
        {{ loadingResources ? "Loading..." : "List resources" }}
      </button>
      <table v-if="resources" class="resource-table">
        <thead>
          <tr>
            <th>Resource</th>
            <th>Description</th>
            <th>Indexed</th>
            <th>Entities</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in resources" :key="r.resource_name">
            <td>{{ r.resource_name }}</td>
            <td>{{ r.description }}</td>
            <td>{{ r.indexed ? "Yes" : "No" }}</td>
            <td>{{ r.entity_count }}</td>
            <td>
              <button type="button" class="btn btn-ghost btn-sm" @click="rebuild(r.resource_name)">
                Rebuild index
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <AlertBanner v-if="manageMessage" :message="manageMessage" type="success" />
    </div>
  </main>
</template>

<script setup>
import { ref } from "vue";
import AlertBanner from "../components/AlertBanner.vue";
import { apiFetch, ApiError } from "../services/api";
import { hasPermission } from "../state/auth";

const query = ref("");
const resourceFilter = ref("");
const results = ref(null);
const searching = ref(false);
const errorMessage = ref("");

const resources = ref(null);
const loadingResources = ref(false);
const manageMessage = ref("");

async function runSearch() {
  if (!query.value.trim()) return;
  searching.value = true;
  errorMessage.value = "";
  try {
    const params = new URLSearchParams({ q: query.value.trim(), limit: "20" });
    if (resourceFilter.value) params.set("resource_filter", resourceFilter.value);
    results.value = await apiFetch(`/api/search/query?${params.toString()}`);
  } catch (err) {
    errorMessage.value = err instanceof ApiError ? err.message : "Something went wrong. Please try again.";
  } finally {
    searching.value = false;
  }
}

async function loadResources() {
  loadingResources.value = true;
  errorMessage.value = "";
  try {
    resources.value = await apiFetch("/api/search/resources");
  } catch (err) {
    errorMessage.value = err instanceof ApiError ? err.message : "Something went wrong. Please try again.";
  } finally {
    loadingResources.value = false;
  }
}

async function rebuild(resourceName) {
  manageMessage.value = "";
  errorMessage.value = "";
  try {
    const status = await apiFetch(`/api/search/rebuild/${resourceName}`, { method: "POST" });
    manageMessage.value = status.message;
  } catch (err) {
    errorMessage.value = err instanceof ApiError ? err.message : "Something went wrong. Please try again.";
  }
}
</script>

<style scoped>
.intro {
  margin-bottom: var(--space-5);
}

.search-form {
  display: flex;
  align-items: flex-end;
  gap: var(--space-4);
  flex-wrap: wrap;
}

.search-field {
  flex: 2;
  min-width: 220px;
  margin-bottom: 0;
}

.resource-field {
  flex: 1;
  min-width: 160px;
  margin-bottom: 0;
}

.results-card {
  margin-top: var(--space-5);
}

.result-list {
  list-style: none;
  padding: 0;
  margin: var(--space-4) 0 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.result-row {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) 0;
  border-bottom: 1px solid var(--color-slate-200);
}

.result-title {
  font-weight: var(--weight-medium);
}

.result-score {
  margin-left: auto;
}

.resource-table {
  width: 100%;
  border-collapse: collapse;
  margin: var(--space-4) 0;
  font-size: var(--text-sm);
}

.resource-table th,
.resource-table td {
  text-align: left;
  padding: var(--space-2) var(--space-3);
  border-bottom: 1px solid var(--color-slate-200);
}

.btn-sm {
  padding: 6px 12px;
  font-size: var(--text-xs);
}
</style>

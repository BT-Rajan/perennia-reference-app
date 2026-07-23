<template>
  <ResourceCrudPage ref="pageRef" :config="config">
    <template #row-actions="{ row }">
      <button
        v-if="hasPermission('quotations.approve') && row.status !== 'Approved' && !row.deleted_at"
        type="button"
        class="btn btn-accent btn-sm"
        :disabled="approvingId === row.id"
        @click="approve(row)"
      >
        {{ approvingId === row.id ? "Approving..." : "Approve" }}
      </button>
    </template>
  </ResourceCrudPage>
</template>

<script setup>
import { ref } from "vue";
import ResourceCrudPage from "../components/ResourceCrudPage.vue";
import { entityConfigs } from "../config/entities";
import { apiFetch, ApiError } from "../services/api";
import { hasPermission } from "../state/auth";

const config = entityConfigs.quotations;
const pageRef = ref(null);
const approvingId = ref(null);

// The only client-side trigger for order creation - the backend enforces
// that this is also the only *server-side* path (see
// backend/app/api/crud.py: approve_quotation).
async function approve(row) {
  approvingId.value = row.id;
  try {
    await apiFetch(`/api/quotations/${row.id}/approve`, { method: "POST" });
    pageRef.value.successMessage = "Quotation approved - order created.";
    pageRef.value.errorMessage = "";
    await pageRef.value.load();
  } catch (err) {
    pageRef.value.errorMessage = err instanceof ApiError ? err.message : "Something went wrong. Please try again.";
  } finally {
    approvingId.value = null;
  }
}
</script>

<template>
  <main class="page-content">
    <p class="badge-eyebrow">{{ config.permissionPrefix }}.read</p>
    <h2>{{ config.icon }} {{ config.label }}</h2>

    <AlertBanner v-if="errorMessage" :message="errorMessage" />
    <AlertBanner v-if="successMessage" :message="successMessage" type="success" />

    <div class="crud-toolbar">
      <button v-if="hasPermission(perm('create'))" type="button" class="btn btn-primary" @click="openCreate">
        + New {{ singular }}
      </button>
    </div>

    <div v-if="showForm" class="card card-tight crud-form-card">
      <h3>{{ editingId ? `Edit ${singular}` : `New ${singular}` }}</h3>
      <form @submit.prevent="submitForm" class="crud-form-grid">
        <div class="field" v-for="f in config.fields" :key="f.key">
          <label :for="f.key">{{ f.label }}</label>
          <select v-if="f.type === 'select'" :id="f.key" v-model="form[f.key]" :required="f.required">
            <option value="" disabled>Select...</option>
            <option v-for="opt in f.options" :key="opt" :value="opt">{{ opt }}</option>
          </select>
          <select v-else-if="f.type === 'reference'" :id="f.key" v-model="form[f.key]" :required="f.required">
            <option value="" disabled>Select...</option>
            <option v-for="opt in referenceOptions[f.reference] || []" :key="opt.id" :value="opt.id">
              {{ opt.label }}
            </option>
          </select>
          <textarea v-else-if="f.type === 'textarea'" :id="f.key" v-model="form[f.key]" rows="2"></textarea>
          <input
            v-else
            :id="f.key"
            v-model="form[f.key]"
            :type="f.type === 'number' ? 'number' : f.type === 'date' ? 'date' : 'text'"
            :step="f.step"
            :required="f.required"
          />
        </div>
        <div class="crud-form-actions">
          <button type="submit" class="btn btn-primary" :disabled="saving">{{ saving ? "Saving..." : "Save" }}</button>
          <button type="button" class="btn btn-ghost" @click="closeForm">Cancel</button>
        </div>
      </form>
    </div>

    <div class="card">
      <table class="resource-table" v-if="items.length">
        <thead>
          <tr>
            <th v-for="c in config.columns" :key="c.key">{{ c.label }}</th>
            <th v-if="hasAnyRowActions">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in items" :key="row.id" :class="{ 'is-deleted': row.deleted_at }">
            <td v-for="c in config.columns" :key="c.key">{{ displayValue(row, c) }}</td>
            <td v-if="hasAnyRowActions" class="row-actions">
              <slot name="row-actions" :row="row" />
              <button
                v-if="hasPermission(perm('update')) && !row.deleted_at"
                type="button"
                class="btn btn-ghost btn-sm"
                @click="openEdit(row)"
              >
                Edit
              </button>
              <button
                v-if="hasPermission(perm('delete')) && !row.deleted_at"
                type="button"
                class="btn btn-ghost btn-sm"
                @click="removeRow(row)"
              >
                Delete
              </button>
              <button
                v-if="hasPermission(perm('restore')) && row.deleted_at"
                type="button"
                class="btn btn-ghost btn-sm"
                @click="restoreRow(row)"
              >
                Restore
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else-if="!loading" class="dim">No records yet.</p>

      <div class="crud-pagination" v-if="total > pageSize">
        <button type="button" class="btn btn-ghost btn-sm" :disabled="page === 1" @click="changePage(page - 1)">
          Prev
        </button>
        <span class="dim">Page {{ page }} of {{ Math.ceil(total / pageSize) }}</span>
        <button
          type="button"
          class="btn btn-ghost btn-sm"
          :disabled="page * pageSize >= total"
          @click="changePage(page + 1)"
        >
          Next
        </button>
      </div>
    </div>
  </main>
</template>

<script setup>
import { computed, onMounted, reactive, ref, useSlots } from "vue";
import AlertBanner from "./AlertBanner.vue";
import { apiFetch, ApiError } from "../services/api";
import { hasPermission } from "../state/auth";
import { useCrudResource } from "../composables/useCrudResource";

const props = defineProps({
  config: { type: Object, required: true },
});

const slots = useSlots();
const { items, total, page, pageSize, loading, errorMessage, load, create, update, remove, restore } =
  useCrudResource(props.config.apiPath);

const successMessage = ref("");
const showForm = ref(false);
const editingId = ref(null);
const saving = ref(false);
const form = reactive({});
const referenceOptions = reactive({});

const singular = computed(() => props.config.label.replace(/s$/, ""));
const hasAnyRowActions = computed(
  () => ["update", "delete", "restore"].some((a) => hasPermission(perm(a))) || !!slots["row-actions"]
);

function perm(action) {
  return `${props.config.permissionPrefix}.${action}`;
}

function defaultForm() {
  const f = {};
  for (const field of props.config.fields) {
    f[field.key] = field.default !== undefined ? field.default : "";
  }
  return f;
}

function openCreate() {
  editingId.value = null;
  Object.assign(form, defaultForm());
  showForm.value = true;
}

function openEdit(row) {
  editingId.value = row.id;
  const f = defaultForm();
  for (const key of Object.keys(f)) {
    if (row[key] !== undefined && row[key] !== null) f[key] = row[key];
  }
  Object.assign(form, f);
  showForm.value = true;
}

function closeForm() {
  showForm.value = false;
  editingId.value = null;
}

async function submitForm() {
  saving.value = true;
  errorMessage.value = "";
  successMessage.value = "";
  try {
    const payload = {};
    for (const field of props.config.fields) {
      let v = form[field.key];
      if (field.type === "number" && v !== "") v = Number(v);
      if (field.type === "reference" && v !== "") v = Number(v);
      if (v !== "") payload[field.key] = v;
    }
    if (editingId.value) {
      await update(editingId.value, payload);
      successMessage.value = `${singular.value} updated.`;
    } else {
      await create(payload);
      successMessage.value = `${singular.value} created.`;
    }
    closeForm();
    await load();
  } catch (err) {
    errorMessage.value = err instanceof ApiError ? err.message : "Something went wrong. Please try again.";
  } finally {
    saving.value = false;
  }
}

async function removeRow(row) {
  errorMessage.value = "";
  successMessage.value = "";
  try {
    await remove(row.id);
    successMessage.value = `${singular.value} deleted.`;
    await load();
  } catch (err) {
    errorMessage.value = err instanceof ApiError ? err.message : "Something went wrong. Please try again.";
  }
}

async function restoreRow(row) {
  errorMessage.value = "";
  successMessage.value = "";
  try {
    await restore(row.id);
    successMessage.value = `${singular.value} restored.`;
    await load();
  } catch (err) {
    errorMessage.value = err instanceof ApiError ? err.message : "Something went wrong. Please try again.";
  }
}

function changePage(p) {
  page.value = p;
  load();
}

function displayValue(row, column) {
  const raw = row[column.key];
  if (column.type === "reference") {
    const opts = referenceOptions[column.reference] || [];
    const match = opts.find((o) => o.id === raw);
    return match ? match.label : raw;
  }
  if (raw === null || raw === undefined || raw === "") return "\u2014";
  return raw;
}

async function loadReferenceOptions() {
  const refFields = props.config.fields.filter((f) => f.type === "reference");
  for (const field of refFields) {
    if (referenceOptions[field.reference]) continue;
    try {
      const result = await apiFetch(`/api/${field.reference}?page_size=100`);
      referenceOptions[field.reference] = result.data.map((r) => ({
        id: r.id,
        label: r[field.referenceLabelKey || "name"],
      }));
    } catch {
      referenceOptions[field.reference] = [];
    }
  }
}

onMounted(async () => {
  await loadReferenceOptions();
  await load();
});

defineExpose({ load, errorMessage, successMessage });
</script>

<style scoped>
.crud-toolbar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: var(--space-4);
}

.crud-form-card {
  margin-bottom: var(--space-5);
}

.crud-form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 0 var(--space-4);
}

.crud-form-actions {
  grid-column: 1 / -1;
  display: flex;
  gap: var(--space-3);
  margin-top: var(--space-2);
}

.row-actions {
  display: flex;
  gap: var(--space-2);
  white-space: nowrap;
}

.is-deleted {
  opacity: 0.5;
}

.crud-pagination {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-top: var(--space-4);
}
</style>

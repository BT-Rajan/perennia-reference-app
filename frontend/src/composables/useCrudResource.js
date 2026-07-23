import { ref } from "vue";
import { apiFetch, ApiError } from "../services/api";

/**
 * Thin wrapper around apiFetch for one entity's REST endpoints
 * (list/create/update/delete/restore). Every CRUD entity in this app -
 * clients, products, raw_materials, suppliers, quotations - follows the
 * same route shape (see backend/app/api/crud.py), so this is the one
 * place that shape is encoded for the frontend.
 */
export function useCrudResource(apiPath) {
  const items = ref([]);
  const total = ref(0);
  const page = ref(1);
  const pageSize = 20;
  const loading = ref(false);
  const errorMessage = ref("");

  async function load() {
    loading.value = true;
    errorMessage.value = "";
    try {
      const result = await apiFetch(`${apiPath}?page=${page.value}&page_size=${pageSize}`);
      items.value = result.data;
      total.value = result.meta.pagination.total;
    } catch (err) {
      errorMessage.value = err instanceof ApiError ? err.message : "Something went wrong. Please try again.";
    } finally {
      loading.value = false;
    }
  }

  function create(data) {
    return apiFetch(apiPath, { method: "POST", body: data });
  }

  function update(id, data) {
    return apiFetch(`${apiPath}/${id}`, { method: "PUT", body: data });
  }

  function remove(id) {
    return apiFetch(`${apiPath}/${id}`, { method: "DELETE" });
  }

  function restore(id) {
    return apiFetch(`${apiPath}/${id}/restore`, { method: "POST" });
  }

  return { items, total, page, pageSize, loading, errorMessage, load, create, update, remove, restore };
}

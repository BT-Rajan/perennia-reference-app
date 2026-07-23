<template>
  <main class="page-content">
    <p class="badge-eyebrow">file.view</p>
    <h2>Files</h2>
    <p class="dim intro">
      Secure, versioned file storage backed by <code class="mono">perennia-files</code>, with optional
      AI processing on stored documents.
    </p>

    <AlertBanner v-if="errorMessage" :message="errorMessage" />
    <AlertBanner v-if="successMessage" :message="successMessage" type="success" />

    <div class="card" v-if="hasPermission('file.upload')">
      <p class="badge-eyebrow">file.upload</p>
      <h3>Upload a file</h3>
      <form @submit.prevent="upload" class="upload-form">
        <div class="field">
          <label for="upload-file">File</label>
          <input id="upload-file" type="file" @change="onFileChange" />
        </div>
        <div class="field">
          <label for="description">Description</label>
          <input id="description" v-model="uploadDescription" type="text" placeholder="Optional description" />
        </div>
        <div class="field">
          <label for="tags">Tags</label>
          <input id="tags" v-model="uploadTags" type="text" placeholder="comma,separated,tags" />
        </div>
        <button type="submit" class="btn btn-primary" :disabled="uploading || !selectedFile">
          {{ uploading ? "Uploading..." : "Upload" }}
        </button>
      </form>
    </div>

    <div class="card">
      <p class="badge-eyebrow">file.view</p>
      <h3>Look up a file</h3>
      <p class="dim">
        This reference app has no "list all files" endpoint - look a file up by ID, e.g. the
        <code class="mono">file_id</code> returned by an upload above (mock uploads return
        <code class="mono">file-001</code>).
      </p>
      <div class="lookup-row">
        <div class="field lookup-field">
          <label for="file-id">File ID</label>
          <input id="file-id" v-model="fileId" type="text" placeholder="file-001" />
        </div>
        <button type="button" class="btn btn-ghost" @click="getMetadata" :disabled="!fileId.trim()">
          Get metadata
        </button>
        <button type="button" class="btn btn-ghost" @click="listVersions" :disabled="!fileId.trim()">
          List versions
        </button>
        <button type="button" class="btn btn-ghost" @click="downloadFile" :disabled="!fileId.trim() || downloading">
          {{ downloading ? "Downloading..." : "Download" }}
        </button>
      </div>

      <div v-if="metadata" class="detail-block">
        <h4>Metadata</h4>
        <dl class="meta-list">
          <div><dt>Filename</dt><dd>{{ metadata.filename }}</dd></div>
          <div><dt>Type</dt><dd>{{ metadata.mime_type }}</dd></div>
          <div><dt>Size</dt><dd>{{ metadata.size_bytes }} bytes</dd></div>
          <div><dt>Version</dt><dd>{{ metadata.version }}</dd></div>
          <div><dt>Created</dt><dd>{{ metadata.created_at }} by {{ metadata.created_by }}</dd></div>
          <div><dt>Deleted</dt><dd>{{ metadata.is_deleted ? "Yes" : "No" }}</dd></div>
        </dl>
      </div>

      <div v-if="versions" class="detail-block">
        <h4>Versions</h4>
        <table class="resource-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Filename</th>
              <th>Size</th>
              <th>Created</th>
              <th>Current</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="v in versions" :key="v.version_number">
              <td>{{ v.version_number }}</td>
              <td>{{ v.filename }}</td>
              <td>{{ v.size_bytes }} bytes</td>
              <td>{{ v.created_at }}</td>
              <td>{{ v.is_current ? "Yes" : "" }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="hasPermission('file.manage')" class="detail-block manage-actions">
        <h4>file.manage</h4>
        <button type="button" class="btn btn-ghost btn-sm" @click="deleteFile" :disabled="!fileId.trim()">
          Delete
        </button>
        <button type="button" class="btn btn-ghost btn-sm" @click="restoreFile" :disabled="!fileId.trim()">
          Restore
        </button>
      </div>

      <div class="detail-block ai-actions">
        <h4>AI processing</h4>
        <div class="ai-row">
          <button type="button" class="btn btn-ghost btn-sm" @click="summarize" :disabled="!fileId.trim()">
            Summarize
          </button>
          <input v-model="aiQuestion" type="text" placeholder="Ask a question about the document" />
          <button type="button" class="btn btn-ghost btn-sm" @click="ask" :disabled="!fileId.trim() || !aiQuestion.trim()">
            Ask
          </button>
        </div>
        <p v-if="aiResult" class="dim ai-result">{{ aiResult }}</p>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref } from "vue";
import AlertBanner from "../components/AlertBanner.vue";
import { apiFetch, apiUpload, ApiError } from "../services/api";
import { hasPermission, getTokens } from "../state/auth";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const errorMessage = ref("");
const successMessage = ref("");

// Upload
const selectedFile = ref(null);
const uploadDescription = ref("");
const uploadTags = ref("");
const uploading = ref(false);

function onFileChange(event) {
  selectedFile.value = event.target.files[0] || null;
}

async function upload() {
  if (!selectedFile.value) return;
  uploading.value = true;
  errorMessage.value = "";
  successMessage.value = "";
  try {
    const formData = new FormData();
    formData.append("file", selectedFile.value);
    if (uploadDescription.value) formData.append("description", uploadDescription.value);
    if (uploadTags.value) formData.append("tags", uploadTags.value);
    const result = await apiUpload("/api/files/upload", formData);
    successMessage.value = result.message;
    fileId.value = result.file_id;
  } catch (err) {
    errorMessage.value = err instanceof ApiError ? err.message : "Something went wrong. Please try again.";
  } finally {
    uploading.value = false;
  }
}

// Lookup
const fileId = ref("");
const metadata = ref(null);
const versions = ref(null);
const aiQuestion = ref("");
const aiResult = ref("");
const downloading = ref(false);

async function downloadFile() {
  errorMessage.value = "";
  downloading.value = true;
  try {
    const tokens = getTokens();
    const headers = {};
    if (tokens && tokens.access_token) headers["Authorization"] = `Bearer ${tokens.access_token}`;

    const response = await fetch(`${API_BASE_URL}/api/files/download/${encodeURIComponent(fileId.value.trim())}`, {
      headers,
    });
    if (!response.ok) {
      throw new ApiError("unexpected_error", "Could not download the file.", response.status);
    }

    const disposition = response.headers.get("Content-Disposition") || "";
    const match = disposition.match(/filename="?([^";]+)"?/);
    const filename = match ? match[1] : fileId.value.trim();

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    link.click();
    URL.revokeObjectURL(url);
  } catch (err) {
    errorMessage.value = err instanceof ApiError ? err.message : "Something went wrong. Please try again.";
  } finally {
    downloading.value = false;
  }
}

async function getMetadata() {
  errorMessage.value = "";
  try {
    metadata.value = await apiFetch(`/api/files/${encodeURIComponent(fileId.value.trim())}/metadata`);
  } catch (err) {
    errorMessage.value = err instanceof ApiError ? err.message : "Something went wrong. Please try again.";
  }
}

async function listVersions() {
  errorMessage.value = "";
  try {
    versions.value = await apiFetch(`/api/files/versions/${encodeURIComponent(fileId.value.trim())}`);
  } catch (err) {
    errorMessage.value = err instanceof ApiError ? err.message : "Something went wrong. Please try again.";
  }
}

async function deleteFile() {
  errorMessage.value = "";
  successMessage.value = "";
  try {
    const result = await apiFetch(`/api/files/${encodeURIComponent(fileId.value.trim())}`, { method: "DELETE" });
    successMessage.value = result.message;
  } catch (err) {
    errorMessage.value = err instanceof ApiError ? err.message : "Something went wrong. Please try again.";
  }
}

async function restoreFile() {
  errorMessage.value = "";
  successMessage.value = "";
  try {
    const result = await apiFetch(`/api/files/${encodeURIComponent(fileId.value.trim())}/restore`, { method: "POST" });
    successMessage.value = result.message;
  } catch (err) {
    errorMessage.value = err instanceof ApiError ? err.message : "Something went wrong. Please try again.";
  }
}

async function summarize() {
  errorMessage.value = "";
  aiResult.value = "";
  try {
    const result = await apiFetch(`/api/files/${encodeURIComponent(fileId.value.trim())}/ai/summarize`, { method: "POST" });
    aiResult.value = result.result;
  } catch (err) {
    errorMessage.value = err instanceof ApiError ? err.message : "Something went wrong. Please try again.";
  }
}

async function ask() {
  errorMessage.value = "";
  aiResult.value = "";
  try {
    const params = new URLSearchParams({ question: aiQuestion.value.trim() });
    const result = await apiFetch(`/api/files/${encodeURIComponent(fileId.value.trim())}/ai/ask?${params.toString()}`, {
      method: "POST",
    });
    aiResult.value = result.result;
  } catch (err) {
    errorMessage.value = err instanceof ApiError ? err.message : "Something went wrong. Please try again.";
  }
}
</script>

<style scoped>
.intro {
  margin-bottom: var(--space-5);
}

.upload-form {
  display: flex;
  align-items: flex-end;
  gap: var(--space-4);
  flex-wrap: wrap;
}

.upload-form .field {
  margin-bottom: 0;
  min-width: 200px;
}

.card + .card {
  margin-top: var(--space-5);
}

.lookup-row {
  display: flex;
  align-items: flex-end;
  gap: var(--space-3);
  flex-wrap: wrap;
}

.lookup-field {
  margin-bottom: 0;
  min-width: 200px;
}

.detail-block {
  margin-top: var(--space-5);
  padding-top: var(--space-5);
  border-top: 1px solid var(--color-slate-200);
}

.meta-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: var(--space-3) var(--space-5);
  margin: var(--space-3) 0 0;
}

.meta-list dt {
  font-size: var(--text-xs);
  color: var(--color-slate-500);
}

.meta-list dd {
  margin: 0;
  font-weight: var(--weight-medium);
}

.resource-table {
  width: 100%;
  border-collapse: collapse;
  margin: var(--space-4) 0 0;
  font-size: var(--text-sm);
}

.resource-table th,
.resource-table td {
  text-align: left;
  padding: var(--space-2) var(--space-3);
  border-bottom: 1px solid var(--color-slate-200);
}

.manage-actions {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  flex-wrap: wrap;
}

.manage-actions h4 {
  width: 100%;
}

.ai-row {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  flex-wrap: wrap;
}

.ai-row input {
  flex: 1;
  min-width: 220px;
  font-family: var(--font-body);
  font-size: var(--text-base);
  padding: 10px 14px;
  border-radius: var(--radius-md);
  border: 1px solid var(--color-slate-200);
}

.ai-result {
  margin-top: var(--space-3);
}

.btn-sm {
  padding: 6px 12px;
  font-size: var(--text-xs);
}
</style>

<template>
  <div class="alert" :class="type === 'success' ? 'alert-success' : 'alert-error'" role="alert">
    <span class="alert-icon" aria-hidden="true">{{ type === "success" ? "✓" : "!" }}</span>
    <span>{{ message }}</span>
  </div>
</template>

<script setup>
defineProps({
  message: { type: String, required: true },
  type: { type: String, default: "error" }, // 'error' | 'success'
});
</script>

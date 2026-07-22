<template>
  <span class="permission-chip" :class="granted ? 'is-granted' : 'is-denied'">
    <span class="chip-dot" aria-hidden="true"></span>
    {{ code }}
  </span>
</template>

<script setup>
defineProps({
  code: { type: String, required: true },
  granted: { type: Boolean, default: false },
});
</script>

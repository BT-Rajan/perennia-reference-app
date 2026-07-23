<template>
  <ResourceCrudPage :config="config" />
</template>

<script setup>
import ResourceCrudPage from "../components/ResourceCrudPage.vue";
import { entityConfigs } from "../config/entities";

const config = entityConfigs.suppliers;
</script>

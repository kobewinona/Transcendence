<template>
  <h2 v-if="Boolean(title)" class="settings-section__title">{{ title }}</h2>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: undefined,
  },
});
</script>

<style scoped>
.settings-section__title {
  margin: 0;
  text-align: center;
  border-bottom: 1px solid var(--light-color);
}
</style>

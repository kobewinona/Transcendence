<template>
  <li class="section">
    <div class="section__title">
      <h2 class="section__title-text">{{ title }}</h2>
      <div class="class__title-suffix" />
    </div>
    <slot />
  </li>
</template>

<script setup>
import { defineProps } from 'vue';

const { title } = defineProps({
  title: {
    type: String,
    required: true,
  },
});
</script>

<style scoped>
.section {
  display: flex;
  flex-direction: column;
  row-gap: var(--regular-space);
}

.section__title {
  display: flex;
  flex-direction: row;
  column-gap: var(--regular-space);
  align-items: baseline;

  width: 100%;
}

.section__title-text {
  min-width: max-content;
}

.class__title-suffix {
  flex-grow: 1;
  height: 15px;
  background-color: var(--light-color-opacity-90);
}
</style>

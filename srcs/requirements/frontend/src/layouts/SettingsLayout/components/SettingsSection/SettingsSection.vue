<template>
  <div class="settings-section">
    <SectionTitle :title="title" />
    <ul class="settings-section__list">
      <li v-for="field in fields" :key="field?.key" class="settings-section__list-item">
        <SectionField :name="field.name" :label="field.label" :options="field.options" />
      </li>
    </ul>
  </div>
</template>

<script setup>
import { SectionField, SectionTitle } from './components';

const { fields } = defineProps({
  title: {
    type: String,
    default: undefined,
  },
  fields: {
    type: Array,
    required: true,
  },
});
</script>

<style scoped>
.settings-section {
  display: flex;
  flex-direction: column;
  row-gap: var(--smaller-space);
  width: 100%;
}

.settings-section__list {
  display: grid;
  grid-template-columns: 1fr 1fr;
  row-gap: var(--smaller-space);

  padding: 0;

  list-style: none;
}

.settings-section__list-item {
  display: contents;
  width: 100%;
}
</style>

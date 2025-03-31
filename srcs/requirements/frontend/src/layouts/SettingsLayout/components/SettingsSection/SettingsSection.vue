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
  display: flex;
  flex-direction: column;
  row-gap: var(--smaller-space);

  padding: 0;

  list-style: none;
}

.settings-section__list-item {
  display: flex;
  flex-direction: row;
  column-gap: var(--regular-space);
  align-items: center;
  justify-content: space-between;

  width: 100%;
}

::v-deep(.settings-section__option) {
  min-width: 100px;
}
</style>

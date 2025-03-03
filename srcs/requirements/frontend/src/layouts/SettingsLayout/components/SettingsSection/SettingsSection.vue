<template>
  <div class="settings-section">
    <SectionTitle :title="title" />
    <ul class="settings-section__list">
      <li v-for="field in fields" :key="field?.key" class="settings-section__list-item">
        <p>{{ t(field.label) }}</p>
        <CarouselSelect
          :name="field.name"
          :default-value="field?.defaultValue"
          option-class-name="settings-section__option"
          :options="field.options"
          @on-change="handleChange"
        />
      </li>
    </ul>
  </div>
</template>

<script setup>
import { CarouselSelect } from 'components';
import { useI18n } from 'vue-i18n';

import { SectionTitle } from './components';

const { t } = useI18n();

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

const emit = defineEmits(['on-change']);

const handleChange = (name, newValue) => {
  emit('on-change', name, newValue);
};
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

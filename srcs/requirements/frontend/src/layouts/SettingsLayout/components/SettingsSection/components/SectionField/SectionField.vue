<template>
  <p v-if="Boolean(label)">{{ t(label) }}</p>
  <CarouselSelect
    :name="name"
    :value="value"
    :options="options"
    @on-change="handleChange"
  />
</template>

<script setup>
import { useField } from 'vee-validate';
import { toRef } from 'vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

import { CarouselSelect } from 'components';

const { name } = defineProps({
  name: {
    type: String,
    required: true,
  },
  label: {
    type: String,
    default: '',
  },
  options: {
    type: Array,
    required: true,
  },
});

const { value, setValue } = useField(toRef(() => name));

const handleChange = (inputValue) => {
  setValue(inputValue);
};
</script>

<template>
  <form class="form" novalidate @submit.prevent="handleSubmit(onSubmit, onError)()">
    <slot />
  </form>
</template>

<script setup>
import { provide, watch } from 'vue';

import { useForm } from './composables';

const { provideKey, errors, ...formParams } = defineProps({
  provideKey: {
    type: String,
    default: undefined,
  },
  initialValues: {
    type: Object,
    default: () => {},
  },
  mode: {
    type: String,
    default: 'onChange',
  },
  errors: {
    type: Object,
    default: () => {},
  },
});

const emit = defineEmits(['on-submit', 'on-error']);

const { handleSubmit, setError, ...methods } = useForm(formParams);

if (provideKey) {
  provide(provideKey, { handleSubmit, ...methods });
}

const onSubmit = (formData) => {
  emit('on-submit', formData);
};

const onError = (errors) => {
  emit('on-error', errors);
};

watch(
  () => errors?.value,
  (newErrors = {}) => {
    if (!newErrors || typeof newErrors !== 'object') return;

    Object.keys(newErrors).forEach((field) => {
      const errorMessage = Array.isArray(newErrors[field])
        ? newErrors[field].join(' ')
        : String(newErrors[field]);

      setError(field, errorMessage);
    });
  }
);
</script>

<style scoped>
.form {
  display: contents;
}
</style>

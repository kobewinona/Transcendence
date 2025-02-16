<template>
  <form class="form" novalidate @submit.prevent="handleSubmit(onSubmit, onError)()">
    <slot />
  </form>
</template>

<script setup>
import { provide } from 'vue';

import { useForm } from './composables';

const { provideKey, ...formParams } = defineProps({
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
});

const emit = defineEmits(['on-submit', 'on-error']);

const { handleSubmit, ...methods } = useForm(formParams);

if (provideKey) {
  provide(provideKey, { handleSubmit, ...methods });
}

const onSubmit = (formData) => {
  emit('on-submit', formData);
};

const onError = (errors) => {
  emit('on-error', errors);
};
</script>

<style scoped>
.form {
  display: contents;
}
</style>

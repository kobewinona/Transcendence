<template>
  <slot v-bind="{ name, value, error, onChange: handleChange, onBlur: handleBlur }" />
</template>

<script setup>
import { computed, inject, onMounted } from 'vue';

const { provideKey, name, rules } = defineProps({
  provideKey: {
    type: String,
    required: true,
  },
  name: {
    type: String,
    required: true,
  },
  rules: {
    type: Object,
    default: null,
  },
});

const form = inject(provideKey);

if (!form) {
  throw new Error(
    '[MyController] No form context found! Ensure MyController is inside a MyForm component.'
  );
}

const value = computed(() => form.getValues(name));
const error = computed(() => form.errors[name] || '');

const handleChange = (event) => {
  const newValue = event?.target?.value ?? event;
  form.handleChange(name, newValue);
};

const handleBlur = () => {
  form.handleBlur(name);
};

onMounted(() => {
  form.setRules(name, rules);
  form.setValue(name, undefined);
});
</script>

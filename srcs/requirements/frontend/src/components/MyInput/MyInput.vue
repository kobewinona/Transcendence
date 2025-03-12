<template>
  <div class="my-input">
    <div :class="{ 'my-input__container': true, 'my-input__container_error': Boolean(error) }">
      <label
        v-if="Boolean(label)"
        :class="{
          'my-input__label': true,
          'my-input__label_place_label': !isLabelPlacePlaceholder,
        }"
        :for="name"
        >{{ label }}</label
      >
      <input
        class="my-input__input"
        :type="type"
        :name="name"
        :value="isControlled ? value : innerValue"
        @focus="handleFocus"
        @blur="handleBlur"
        @input="handleChange"
      />
    </div>
    <transition name="fade-slide">
      <span v-show="Boolean(error)" class="my-input__error">{{ error }}</span>
    </transition>
  </div>
</template>

<script setup>
import { VALID_INPUT_TYPES } from 'config/constants.js';
import { ref, watch } from 'vue';

const { value, error } = defineProps({
  name: {
    type: String,
    default: undefined,
  },
  type: {
    type: String,
    default: 'text',
    validator: (value) => VALID_INPUT_TYPES.includes(value),
  },
  label: {
    type: String,
    default: '',
  },
  value: {
    type: String,
    default: undefined,
  },
  error: {
    type: String,
    default: '',
  },
});

const emit = defineEmits(['focus', 'blur', 'change']);

const isControlled = ref(value !== undefined);

const isFocused = ref(false);
const isLabelPlacePlaceholder = ref(true);
const innerValue = ref(undefined);

const isNoValue = (checkValue) => {
  return !checkValue || checkValue === '';
};

const handleFocus = (event) => {
  isFocused.value = true;
  isLabelPlacePlaceholder.value = false;

  emit('focus', event);
};

const handleBlur = (event) => {
  isFocused.value = false;

  const { value: inputValue } = event?.target || {};

  isLabelPlacePlaceholder.value = isNoValue(inputValue);

  emit('blur', event);
};

const handleChange = (event) => {
  const { value: inputValue } = event?.target || {};

  if (!isControlled.value) {
    innerValue.value = inputValue;
  }

  emit('change', event);
};

watch(
  () => value,
  (newValue) => {
    isControlled.value = newValue !== undefined;

    if (isControlled.value && !isFocused.value) {
      isLabelPlacePlaceholder.value = isNoValue(newValue);
    }
  },
  { immediate: true }
);
</script>

<style scoped>
.my-input {
  position: relative;

  display: flex;
  flex-direction: column;
  row-gap: var(--small-space);

  width: 100%;
  height: max-content;
  margin-bottom: var(--smaller-space);
}

.my-input__container {
  position: relative;
  z-index: 2;

  display: flex;
  align-items: flex-end;

  width: 100%;
  height: 44px;
  padding: var(--small-space) var(--smaller-space);

  background-color: var(--light-color);
  border-radius: 12px;

  transition: background-color 0.2s ease-in-out;
}

.my-input__container_error {
  background-color: var(--error-color-opacity-75);
  transition: background-color 0.2s ease-in-out;
}

.my-input__label {
  pointer-events: none;

  position: absolute;
  top: calc(50% - 12px);

  height: unset;

  font-size: 1rem;
  color: var(--dark-color-opacity-50);

  transition: all 0.2s ease-in-out;
}

.my-input__label_place_label {
  top: var(--small-space);
  transform: translateY(0);

  height: 14px;

  font-size: 0.55rem;

  transition: all 0.2s ease-in-out;
}

.my-input__input {
  width: 100%;
  height: 100%;
  padding-top: 12px;

  color: var(--dark-color);

  background-color: transparent;
  border: none;
  caret-color: var(--dark-color);
}

.my-input__input:focus-visible,
.my-input__input:focus {
  outline: none;
}

.my-input__input:-webkit-autofill,
.my-input__input:-webkit-autofill:hover,
.my-input__input:-webkit-autofill:focus,
.my-input__input:-webkit-autofill:active {
  color: var(--dark-color) !important;
  background-color: transparent !important;
  transition: background-color 5000s ease-in-out 0s;

  -webkit-text-fill-color: var(--dark-color) !important;
}

.my-input__error {
  padding: 0 var(--smaller-space);
  font-size: 0.75rem;
  line-height: 0.75rem;
  color: var(--error-color);
}

::v-deep(.fade-slide-enter-active) {
  transition:
    opacity 0.3s ease,
    transform 0.3s ease;
}

::v-deep(.fade-slide-enter-from) {
  transform: translateY(-5px);
  opacity: 0;
}
</style>

<template>
  <div class="my-input">
    <div
      :class="{
        'my-input__container': true,
        'my-input__container_variant_filled': variant === 'filled',
        'my-input__container_variant_ghost': variant === 'ghost',
        'my-input__container_error': Boolean(errorMessage),
      }"
    >
      <label
        v-if="Boolean(label)"
        :class="{
          'my-input__label': true,
          'my-input__label_error': Boolean(errorMessage),
          'my-input__label_place_label': !isLabelPlacePlaceholder,
        }"
        :for="name"
        >{{ label }}</label
      >
      <input
        :class="{ 'my-input__input': true, 'my-input__input_error': Boolean(errorMessage) }"
        :type="type"
        :name="name"
        :maxlength="maxLength"
        :value="isControlled ? value : innerValue"
        v-on="handlers"
      />
    </div>
    <transition name="fade-slide">
      <span v-show="Boolean(errorMessage)" class="my-input__error">{{ errorMessage }}</span>
    </transition>
  </div>
</template>

<script setup>
import { VALID_INPUT_TYPES } from 'config/constants.js';
import { useField } from 'vee-validate';
import { computed, ref, toRef, watch } from 'vue';

import { modes } from './lib';

const props = defineProps({
  name: { type: String, required: true },
  type: {
    type: String,
    default: 'text',
    validator: (value) => VALID_INPUT_TYPES.includes(value),
  },
  maxLength: {
    type: Number,
    default: null,
  },
  mode: {
    type: String,
    default: 'lazy',
    validator: (value) => Object.keys(modes).includes(value),
  },
  variant: {
    type: String,
    default: 'filled',
    validator: (value) => value === 'filled' || value === 'ghost',
  },
  label: { type: String, default: '' },
});

// noinspection JSCheckFunctionSignatures
const { meta, value, errorMessage, handleChange, handleBlur } = useField(
  toRef(props, 'name'),
  null,
  {
    validateOnValueUpdate: false,
  }
);

const isControlled = ref(value !== undefined);
const isFocused = ref(false);
const isLabelPlacePlaceholder = ref(true);
const innerValue = ref(undefined);

const handlers = computed(() => {
  const on = {
    focus: [
      () => {
        isFocused.value = true;
        isLabelPlacePlaceholder.value = false;
      },
    ],
    blur: [
      (e) => {
        const { value: inputValue } = e?.target || {};
        isFocused.value = false;
        isLabelPlacePlaceholder.value = isNoValue(inputValue);
        handleBlur(e);
      },
    ],
    input: [(e) => handleChange(e, false)],
  };

  const triggers = modes[props.mode]({ errorMessage, meta });

  triggers.forEach((t) => {
    if (Array.isArray(on[t])) {
      on[t].push(handleChange);
    } else {
      on[t] = handleChange;
    }
  });

  return on;
});

const isNoValue = (checkValue) => {
  return !checkValue || checkValue === '';
};

watch(
  () => value.value,
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
  padding: 0 var(--smaller-space);

  background-color: var(--light-color);
  border-radius: 12px;

  transition: background-color 0.2s ease-in-out;
}

.my-input__container_variant_filled {
  background-color: var(--light-color);
}

.my-input__container_variant_ghost {
  background-color: transparent;
  border: 1px solid var(--light-color);
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

.my-input__label_error {
  color: var(--light-color-opacity-50);
}

.my-input__label_place_label {
  top: var(--small-space);
  transform: translateY(0);

  height: 14px;

  font-size: 0.55rem;

  transition: all 0.2s ease-in-out;
}

.my-input__container_variant_ghost .my-input__label {
  color: var(--light-color-opacity-70);
}

.my-input__input {
  width: 100%;
  height: 100%;
  padding-top: 16px;

  color: var(--dark-color);

  background-color: transparent;
  border: none;
  caret-color: var(--dark-color);
}

.my-input__input:focus-visible,
.my-input__input:focus {
  outline: none;
}

.my-input__container_variant_ghost .my-input__input {
  color: var(--light-color);
  caret-color: var(--light-color);
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

.my-input__input_error {
  color: var(--light-color-opacity-90);
}

.my-input__error {
  padding: 0 var(--smaller-space);
  font-size: 0.75rem;
  line-height: 0.75rem;
  color: var(--error-color);
}
</style>

<template>
  <button v-bind="attrs" :class="[className, 'button', `button_color_${color}`]" :type="type">
    <Loader v-if="loading" :size="20" />
    <slot />
  </button>
</template>

<script setup>
import { Loader } from 'shared/components';
import { useAttrs } from 'vue';

const attrs = useAttrs();

defineProps({
  className: {
    type: String,
    default: '',
  },
  type: {
    type: String,
    default: 'button',
  },
  color: {
    type: String,
    default: 'primary',
    validator: (value) => value === 'primary' || value === 'secondary',
  },
  text: {
    type: String,
    default: '',
  },
  loading: {
    type: Boolean,
    default: false,
  },
});
</script>

<!--suppress CssUnusedSymbol -->
<style scoped>
.button {
  cursor: pointer;

  display: flex;
  flex-direction: row;
  column-gap: var(--bigger-space);
  justify-content: center;

  padding: var(--smaller-space) var(--big-space);

  font-size: 1.2rem;
  font-weight: 600;

  border: none;
  border-radius: 12px;

  transition: all 0.2s ease-in-out;
}

.button_color_primary {
  background-color: var(--primary-color);
}

.button_color_secondary {
  background-color: var(--secondary-color);
}

.button_color_primary:hover:not(.button:disabled) {
  background-color: var(--primary-color-opacity-70);
  transition: all 0.2s ease-in-out;
}

.button_color_secondary:hover:not(.button:disabled) {
  background-color: var(--secondary-color-opacity-70);
  transition: all 0.2s ease-in-out;
}

.button:disabled {
  cursor: not-allowed;
  color: var(--dark-color-opacity-50);
  filter: grayscale(0.8);
  transition: all 0.4s ease-in-out;
}
</style>

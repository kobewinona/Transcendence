<template>
  <button v-bind="attrs" :class="[className, 'button']" :type="type"><slot /></button>
</template>

<script setup>
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
  text: {
    type: String,
    default: '',
  },
});
</script>

<style scoped>
.button {
  cursor: pointer;

  padding: var(--smaller-space) var(--big-space);

  font-size: 1.2rem;
  font-weight: 600;

  background-color: var(--primary-color);
  border: none;
  border-radius: 12px;

  transition: all 0.2s ease-in-out;
}

.button:hover:not(.button:disabled) {
  background-color: var(--primary-color-opacity-70);
  transition: all 0.2s ease-in-out;
}

.button:disabled {
  cursor: not-allowed;
  filter: grayscale(0.8);
  transition: all 0.4s ease-in-out;
}
</style>

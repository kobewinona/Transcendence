<template>
  <div class="message">
    <div :class="['message__icon-container', `message__icon-container_type_${type}`]">
      <component
        :is="icon[type]"
        v-show="Boolean(type)"
        v-if="isVueComponent(icon[type])"
        class="message__icon"
      />
    </div>
    <span class="message__text">{{ message }}</span>
  </div>
</template>

<script setup>
import { isVueComponent, svgComponents } from 'shared/lib/index.js';

defineProps({
  message: {
    type: String,
    required: true,
  },
  type: {
    type: String,
    default: null,
    validator: (value) => value === 'success' || value === 'error',
  },
});

const icon = {
  success: svgComponents['ApprovedIcon'],
  error: svgComponents['RejectedIcon'],
};
</script>

<!--suppress CssUnusedSymbol -->
<style scoped>
.message {
  display: flex;
  flex-direction: row;
  column-gap: var(--smaller-space);
  align-items: center;
  justify-content: center;

  padding: var(--small-space) var(--bigger-space);

  color: var(--dark-color);

  background-color: var(--light-color);
  border-radius: 12px;
}

.message__icon-container {
  width: 24px;
  height: 24px;
  padding: 2px;
  border-radius: 50%;
}

.message__icon-container_type_success {
  background-color: var(--success-color);
}

.message__icon-container_type_error {
  background-color: var(--error-color);
}

.message__icon {
  width: 100%;
  height: 100%;
  fill: var(--light-color);
  stroke: var(--light-color);
}

.message__text {
  font-size: 0.9rem;
  color: var(--dark-color-opacity-90);
}
</style>

<script setup>
defineProps({
  className: {
    type: String,
    default: '',
  },
});
</script>

<template>
  <div :class="[className, 'loading-circle']">
    <div class="circle" />
  </div>
</template>

<style scoped>
@keyframes loading-spin {
  0% {
    transform: rotate(0deg);
    border-color: var(--primary-color) transparent transparent transparent;
    border-width: 4px;
  }

  25% {
    transform: rotate(90deg);
    border-color: var(--secondary-color) transparent transparent transparent;
    border-width: 8px;
  }

  50% {
    transform: rotate(180deg);
    border-color: var(--primary-color) transparent transparent transparent;
    border-width: 4px;
  }

  75% {
    transform: rotate(270deg);
    border-color: var(--light-color-opacity-50) transparent transparent transparent;
    border-width: 6px;
  }

  100% {
    transform: rotate(360deg);
    border-color: var(--primary-color) transparent transparent transparent;
    border-width: 4px;
  }
}

.loading-circle {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 100px;
  height: 100px;
}

.circle {
  width: 100%;
  height: 100%;

  border-color: var(--primary-color) transparent transparent transparent;
  border-style: solid;
  border-width: 4px;
  border-radius: 50%;

  animation: loading-spin 2s cubic-bezier(0.4, 0, 0.2, 1) infinite;
}
</style>

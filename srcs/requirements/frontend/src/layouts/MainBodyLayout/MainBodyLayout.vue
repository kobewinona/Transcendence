<template>
  <div :class="['main-body', className]">
    <slot />
  </div>
</template>

<script setup>
const { className } = defineProps({
  className: {
    type: String,
    default: '',
  },
});
</script>

<style scoped>
.main-body {
  display: flex;
  align-items: center;

  width: 100%;
  height: 100%;
  padding: var(--big-space);

  background-color: var(--dark-color-opacity-90);
  border-top: 1px solid var(--light-color-opacity-50);
  border-bottom: 1px solid var(--light-color-opacity-50);
  border-radius: 12px;
}
</style>

<template>
  <div :class="[className, 'settings-layout']">
    <slot />
  </div>
</template>

<script setup>
defineProps({
  className: {
    type: String,
    default: '',
  },
});
</script>

<style scoped>
.settings-layout {
  overflow: auto;

  width: 70%;
  height: 100%;
  margin: 0 auto;
  padding: var(--big-space);
}
</style>

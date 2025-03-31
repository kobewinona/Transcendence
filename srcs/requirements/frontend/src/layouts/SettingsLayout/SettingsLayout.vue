<template>
  <div :class="[className, 'settings-layout']" :style="{ width }">
    <slot />
  </div>
</template>

<script setup>
defineProps({
  className: {
    type: String,
    default: '',
  },
  width: {
    type: String,
    default: '70%',
  },
});
</script>

<style scoped>
.settings-layout {
  overflow: auto;
  height: 100%;
  min-height: 0;
  margin: 0 auto;
}
</style>

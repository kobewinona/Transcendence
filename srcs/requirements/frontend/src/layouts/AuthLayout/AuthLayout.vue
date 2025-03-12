<template>
  <div :class="['auth', className]">
    <h1 class="auth__title">{{ title }}</h1>
    <slot />
  </div>
</template>

<script setup>
defineProps({
  className: {
    type: String,
    default: '',
  },
  title: {
    type: String,
    required: true,
  },
});
</script>

<style scoped>
.auth {
  display: grid;
  grid-auto-rows: max-content auto max-content;
  grid-template-columns: 100%;
  row-gap: var(--bigger-space);

  width: 70%;
  max-width: 500px;
  height: 100%;
  margin: 0 auto;
}

.auth__title {
  text-align: center;
  text-transform: uppercase;
}
</style>

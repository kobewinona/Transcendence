<template>
  <span :class="['loader-wrapper', `loader-wrapper_size_${size}`]">
    <transition name="fade-scale">
      <span v-if="isActive">
        <span class="loader" />
      </span>
    </transition>
  </span>
</template>

<script setup>
defineProps({
  isActive: {
    type: Boolean,
    required: true,
  },
  size: {
    type: String,
    default: 'small',
    validator: (value) => value === 'small' || value === 'middle',
  },
});
</script>

<!--suppress CssUnusedSymbol -->
<style scoped>
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.loader-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;

  margin-right: var(--smaller-space);

  transition:
    width 0.2s ease-in-out,
    height 0.2s ease-in-out;
}

.loader-wrapper_size_small {
  width: 1.2em;
  height: 1.2rem;
}

.loader-wrapper_size_middle {
  width: 1.8em;
  height: 1.8rem;
}

.loader-wrapper:empty {
  width: 0;
  margin-right: 0;
}

.loader {
  display: flex;

  width: 1em;
  height: 1em;

  border: 2px solid transparent;
  border-top-color: currentcolor;
  border-radius: 50%;

  animation: spin 0.6s linear infinite;
}

.fade-scale-enter-active {
  transition: opacity 0.4s ease-in-out;
}

.fade-scale-enter-from,
.fade-scale-leave-to {
  opacity: 0;
}

.fade-scale-enter-to,
.fade-scale-leave-from {
  opacity: 1;
}
</style>

<script setup>
defineProps({
  className: {
    type: String,
    default: '',
  },
});
</script>

<template>
  <div :class="['shapeshifter', className]" />
</template>

<style scoped>
@keyframes square-to-circle {
  0% {
    transform: rotate(45deg);
    border-radius: 0;
  }

  25% {
    transform: rotate(135deg);
    background: var(--dark-color-opacity-50);
    border-radius: 25% 0 0 25%;
  }

  50% {
    transform: rotate(180deg);
    background: var(--primary-color);
    border-radius: 25% 50% 0 0;
  }

  75% {
    transform: rotate(315deg);
    background: var(--light-color-opacity-50);
    border-radius: 50% 50% 50% 0;
  }

  100% {
    transform: rotate(404deg);
    background: var(--secondary-color);
    border-radius: 50%;
  }
}

.shapeshifter {
  aspect-ratio: 1 / 1;
  width: 90px;
  background-color: var(--light-color);
  animation: square-to-circle 2.5s 0.5s infinite cubic-bezier(1, 0.015, 0.295, 1.225)
    alternate-reverse;
}
</style>

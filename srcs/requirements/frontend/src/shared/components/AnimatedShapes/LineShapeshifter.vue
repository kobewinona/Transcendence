<script setup>
defineProps({
  className: {
    type: String,
    default: '',
  },
});
</script>

<template>
  <div :class="['line-shapeshifter', className]">
    <div class="line" />
  </div>
</template>

<style scoped>
@keyframes line-to-shapes {
  0% {
    transform: rotate(0deg) scaleX(1) scaleY(0.1);
    background: var(--primary-color);
  }

  25% {
    transform: rotate(45deg) scaleX(0.8) scaleY(0.8);
    background: var(--secondary-color);
  }

  50% {
    transform: rotate(0deg) scaleX(1.5) scaleY(0.1);
    background: var(--primary-color);
  }

  75% {
    transform: rotate(135deg) scaleX(1) scaleY(0.8);
    background: var(--light-color-opacity-50);
  }

  100% {
    transform: rotate(0deg) scaleX(1) scaleY(0.1);
    background: var(--primary-color);
  }
}

.line-shapeshifter {
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;

  width: 150px;
  height: 150px;
}

.line {
  width: 100%;
  height: 10%;

  background-color: var(--primary-color, #3498db);
  border-radius: 2px;

  animation: line-to-shapes 2.5s 0.5s infinite cubic-bezier(1, 0.015, 0.295, 1.225)
    alternate-reverse;
}
</style>

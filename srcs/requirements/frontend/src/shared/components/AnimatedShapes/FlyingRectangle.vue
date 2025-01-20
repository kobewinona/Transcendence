<script setup>
defineProps({
  className: {
    type: String,
    default: '',
  },
});
</script>

<template>
  <div :class="['flying-rectangle', className]">
    <div class="flying-rectangle__core" />
  </div>
</template>

<style scoped>
@keyframes fly {
  0% {
    transform: translateX(-150%);
  }

  50% {
    transform: translateX(50%);
  }

  100% {
    transform: translateX(150%);
  }
}

.flying-rectangle {
  position: relative;
  overflow: hidden;
  width: 50%;
  height: 100%;
}

.flying-rectangle__core {
  position: absolute;
  top: 60%;
  left: 0;
  transform: translateY(-50%);

  width: 50%;
  height: 20%;

  background-color: var(--secondary-color);
  border-radius: 8px;
  box-shadow: 0 4px 6px rgb(0 0 0 / 0.1);

  animation: fly 1.5s 0.5s infinite cubic-bezier(1, 0.015, 0.295, 1.225) alternate-reverse;
}
</style>

<template>
  <div
    class="static_circle"
    :style="{
      '--size-positive': `${size}px`,
      '--size-negative': `-${size}px`,
      width: `${size}px`,
      height: `${size}px`,
      backgroundColor: currentColor,
    }"
  >
    <div
      class="moving-circle"
      :style="{
        width: `${movingCircleSize}px`,
        height: `${movingCircleSize}px`,
      }"
      @animationiteration="onAnimationIteration"
    />
  </div>
</template>

<script setup>
import { computed, onUnmounted, ref } from 'vue';

const { size } = defineProps({
  className: {
    type: String,
    default: '',
  },
  size: {
    type: Number,
    default: 40,
  },
});

const movingCircleSize = computed(() => size * 1.1);

const colors = ['var(--primary-color)', 'var(--secondary-color)'];
const colorIndex = ref(0);
const currentColor = ref(colors[colorIndex.value]);

const iterationTimeoutId = ref(null);

const onAnimationIteration = () => {
  clearTimeout(iterationTimeoutId.value);

  iterationTimeoutId.value = setTimeout(() => {
    colorIndex.value = (colorIndex.value + 1) % colors.length;
    currentColor.value = colors[colorIndex.value];
  }, 750);
};

onUnmounted(() => clearTimeout(iterationTimeoutId.value));
</script>

<style scoped>
@keyframes moving {
  0% {
    transform: translate(var(--size-negative), -2px);
  }

  50% {
    transform: translate(-2px, -2px);
  }

  100% {
    transform: translate(var(--size-positive), -2px);
  }
}

.static_circle {
  --size-positive: 0;
  --size-negative: 0;

  position: relative;

  overflow: hidden;

  padding: 2px;

  border-radius: 50%;
  mix-blend-mode: hard-light;
}

.moving-circle {
  position: absolute;
  top: 0;
  left: 0;

  background-color: var(--dark-color);
  border-radius: 50%;

  animation: moving 1.5s ease-in-out infinite;
}
</style>

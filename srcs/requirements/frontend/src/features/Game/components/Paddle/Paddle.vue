<script setup>
import { computed, defineProps, onMounted, onUnmounted, ref } from 'vue';

const { side, params } = defineProps({
  side: {
    type: String,
    required: true,
    validator: (value) => ['left', 'right'].includes(value),
  },
  params: {
    type: Object,
    required: true,
    validator: (value) => {
      return (
        typeof value.width === 'number' &&
        typeof value.height === 'number' &&
        value.position &&
        typeof value.position.y === 'number' &&
        typeof value.speed === 'number' &&
        typeof value.deacceleration === 'number'
      );
    },
  },
});

const paddlePosition = ref(params?.y);
let animationFrameId = null;

const styles = computed(() => ({
  width: `${params?.width}%`,
  height: `${params?.height}%`,
  top: `${params?.y}%`,
}));

const update = () => {
  paddlePosition.value = params?.position?.y;
  animationFrameId = requestAnimationFrame(update);
};

onMounted(() => {
  animationFrameId = requestAnimationFrame(update);
});

onUnmounted(() => {
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId);
  }
});
</script>

<template>
  <div
    class="paddle"
    :class="{
      paddle_side_left: side === 'left',
      paddle_side_right: side === 'right',
    }"
    :style="styles"
  />
</template>

<style scoped>
.paddle {
  position: absolute;
  z-index: 3;
  transform: translateY(-50%);

  border-radius: 10px;

  transition:
    top 25ms linear,
    height 150ms linear;
}

.paddle_side_left {
  left: 0;
  background-color: var(--dark-color);
}

.paddle_side_right {
  right: 0;
  background-color: var(--light-color);
}
</style>

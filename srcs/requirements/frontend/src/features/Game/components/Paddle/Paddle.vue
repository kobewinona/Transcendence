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

<script setup>
import { computed } from 'vue';

import { useGameSocketInject } from '../../composables';

const { side } = defineProps({
  side: {
    type: String,
    required: true,
    validator: (value) => ['left', 'right'].includes(value),
  },
});

const gameSocket = useGameSocketInject();

const paddleWidth = computed(() =>
  side === 'left' ? gameSocket.leftPaddleWidth.value : gameSocket.rightPaddleWidth.value
);
const paddleHeight = computed(() =>
  side === 'left' ? gameSocket.leftPaddleHeight.value : gameSocket.rightPaddleHeight.value
);
const paddleY = computed(() =>
  side === 'left' ? gameSocket.leftPaddleY.value : gameSocket.rightPaddleY.value
);

const styles = computed(() => {
  return {
    width: `${paddleWidth.value}%`,
    height: `${paddleHeight.value}%`,
    top: `${paddleY.value}%`,
  };
});
</script>

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

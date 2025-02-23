<template>
  <div
    class="paddle"
    :class="{
      paddle_side_left: side === 'left',
      'paddle_side_left-color': hasMoreThanTwoPlayers && side === 'left',
      paddle_side_right: side === 'right',
      'paddle_side_right-color': hasMoreThanTwoPlayers && side === 'right',
    }"
    :style="styles"
  >
    <div
      v-show="hasMoreThanTwoPlayers"
      :class="[
        'paddle__name',
        {
          paddle__name_side_left: side === 'left',
          paddle__name_side_right: side === 'right',
        },
      ]"
    >
      {{ name }}
    </div>
  </div>
</template>

<script setup>
import { COLORS } from 'entities/Game/config/constants.js';
import { computed } from 'vue';

import { useGameSocketInject } from '../../composables';

const { name, side, paddleIndex, hasMoreThanTwoPlayers } = defineProps({
  name: {
    type: String,
    required: true,
  },
  side: {
    type: String,
    required: true,
    validator: (value) => ['left', 'right'].includes(value),
  },
  paddleIndex: {
    type: Number,
    required: true,
  },
  hasMoreThanTwoPlayers: {
    type: Boolean,
    required: true,
  },
});

const gameSocket = useGameSocketInject();

const paddleWidth = computed(() => {
  return gameSocket.paddleWidths.value[paddleIndex];
});
const paddleHeight = computed(() => {
  return gameSocket.paddleHeights.value[paddleIndex];
});
const paddleY = computed(() => {
  return gameSocket.paddlePositions.value[paddleIndex];
});

const styles = computed(() => {
  return {
    width: `${paddleWidth.value}%`,
    height: `${paddleHeight.value}%`,
    top: `${paddleY.value}%`,
    '--outline-color': `var(${COLORS[paddleIndex]})`,
    '--left-paddle-bg': `var(${hasMoreThanTwoPlayers ? '--dark-color' : '--dark-color-opacity-90'})`,
    '--right-paddle-bg': `var(${hasMoreThanTwoPlayers ? '--light-color' : '--light-color-opacity-90'})`,
  };
});
</script>

<!--suppress CssUnusedSymbol -->
<style scoped>
.paddle {
  --outline-color: '';
  --left-paddle-bg: '';
  --right-paddle-bg: '';

  position: absolute;
  z-index: 3;
  transform: translateY(-50%);

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 10px;

  transition:
    top 25ms linear,
    height 150ms linear;
}

.paddle_side_left {
  left: 0;
  background-color: var(--left-paddle-bg);
}

.paddle_side_left-color {
  border-left: 6px solid var(--outline-color);
}

.paddle_side_right {
  right: 0;
  background-color: var(--right-paddle-bg);
}

.paddle_side_right-color {
  border-right: 6px solid var(--outline-color);
}

.paddle__name {
  transform: rotate(-90deg);
  font-size: 10px;
  white-space: nowrap;
}

.paddle__name_side_left {
  color: var(--light-color);
}

.paddle__name_side_right {
  color: var(--dark-color);
}
</style>

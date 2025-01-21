<template>
  <slot />
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue';

import { useGameSocketInject } from '../../composables';

const { side, controls } = defineProps({
  side: {
    type: String,
    required: true,
    validator: (value) => ['left', 'right'].includes(value),
  },
  controls: {
    type: Object,
    required: true,
    validator: (value) => typeof value.up === 'string' && typeof value.down === 'string',
  },
});

const gameSocket = useGameSocketInject();

const direction = ref(0);

const handleKeyDown = (event) => {
  if (event.code === controls?.up) {
    direction.value = -1;
  } else if (event.code === controls?.down) {
    direction.value = 1;
  }
  sendDirection();
};

const handleKeyUp = (event) => {
  if (event.code === controls?.up || event.code === controls?.down) {
    direction.value = 0;
  }
  sendDirection();
};

const sendDirection = () => {
  gameSocket.actions.updatePaddlePosition({ side, direction: direction.value });
};

onMounted(() => {
  window.addEventListener('keydown', handleKeyDown);
  window.addEventListener('keyup', handleKeyUp);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown);
  window.removeEventListener('keyup', handleKeyUp);
});
</script>

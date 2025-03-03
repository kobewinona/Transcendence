<template>
  <slot />
</template>

<script setup>
import { useGameSocketInject } from 'entities/Game/composables';
import { onMounted, onUnmounted, ref } from 'vue';

const { name, side, controls } = defineProps({
  name: {
    type: String,
    required: true,
  },
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

const sendDirection = () => {
  gameSocket.actions.updatePaddlePosition({ name, side, direction: direction.value });
};

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

onMounted(() => {
  window.addEventListener('keydown', handleKeyDown);
  window.addEventListener('keyup', handleKeyUp);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown);
  window.removeEventListener('keyup', handleKeyUp);
});
</script>

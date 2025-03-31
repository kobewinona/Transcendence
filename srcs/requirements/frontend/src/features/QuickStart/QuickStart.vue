<template>
  <div class="quick-start" />
</template>

<script setup>
import { useGameSocketInject } from 'entities/Game/composables/index.js';
import { QUICK_START_DEFAULT_GAME_SETTINGS } from 'entities/Game/config/constants.js';
import { onMounted } from 'vue';

const gameSocket = useGameSocketInject();

onMounted(() => {
  gameSocket.actions.startGame(QUICK_START_DEFAULT_GAME_SETTINGS);
});
</script>

<style scoped>
.quick-start {
  visibility: hidden;
}
</style>

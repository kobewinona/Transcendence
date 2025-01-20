<template>
  <div class="game">
    <div class="game__void-boundary">
      <div class="game__void-boundary-shadow game__void-boundary-shadow_left" />
      <div class="game__void-boundary-shadow game__void-boundary-shadow_right" />
    </div>
    <div ref="gameContainerRef" class="game__container">
      <Ball :is-position-forced="isBallPositionForced" />
      <component
        :is="side.controlledBy === 'player' ? withPlayerControl : withAiControl"
        v-for="(side, index) in props.settings?.sides || []"
        :key="index"
        :socket="socket"
        :side="side.side"
        :controls="side.controls"
      >
        <Paddle :side="side.side" />
      </component>
    </div>
  </div>
</template>

<script setup>
import { computed, onUnmounted, ref, watch } from 'vue';

import { Ball, Paddle, withAiControl, withPlayerControl } from './components';
import { provideGameDimensions, useGameSocketInject } from './composables';
import { DEFAULT_GAME_SETTINGS } from './config/constants.js';

const gameContainerRef = ref(null);
const gameSocket = useGameSocketInject();

const props = defineProps({
  forcedBallPosition: {
    type: Object,
    default: null,
  },
  settings: {
    type: Object,
    default: () => ({ ...DEFAULT_GAME_SETTINGS }),
  },
});

provideGameDimensions(gameContainerRef, gameSocket.actions.updateGameDimensions);

let socket = null;

const isBallPositionForced = computed(() => Boolean(props.forcedBallPosition));

watch(
  () => props.settings,
  (newSettings) => {
    console.log('Game settings changed:', newSettings);
    gameSocket.actions.startGame();
  },
  { immediate: true, deep: true }
);

onUnmounted(() => {
  gameSocket.actions.closeGameSocket();
});
</script>

<style scoped>
.game {
  position: relative;

  overflow: hidden;

  box-sizing: border-box;
  width: 100%;
  height: 100%;
  padding-right: 20px;
  padding-left: 20px;

  background: linear-gradient(to right, var(--light-color) 50%, var(--dark-color) 50%);
  border-radius: 12px;
}

.game__container {
  position: relative;

  width: 100%;
  height: 100%;
  padding: 20px;

  background: linear-gradient(to right, var(--light-color) 50%, var(--dark-color) 50%);
}

.game__void-boundary {
  position: absolute;
  top: 0;
  left: 0;

  display: flex;
  justify-content: space-between;

  width: 100%;
  height: 100%;
}

.game__void-boundary-shadow {
  position: absolute;
  z-index: 2;
  width: 7%;
  height: 100%;
}

.game__void-boundary-shadow_left {
  left: 0;
  background: linear-gradient(to right, var(--light-color), transparent);
}

.game__void-boundary-shadow_right {
  right: 0;
  background: linear-gradient(to left, var(--dark-color), transparent);
}
</style>

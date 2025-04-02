<template>
  <Score />
  <div class="game">
    <Field
      :show-score="
        settings[MODE_INPUT_NAME] !== DEMO_GAME_MODE &&
        settings[MODE_INPUT_NAME] !== QUICK_START_GAME_MODE
      "
    />
    <div ref="gameContainerRef" class="game__container">
      <Ball
        v-if="winner === 0"
        :color="settings[BALL_DESIGN_INPUT_NAME][BALL_COLOR_INPUT_NAME]"
        :skin="settings[BALL_DESIGN_INPUT_NAME][BALL_SKIN_INPUT_NAME]"
        :skin-type="settings[BALL_DESIGN_INPUT_NAME][BALL_SKIN_TYPE_INPUT_NAME]"
      />
      <component
        :is="
          controller[CONTROLLED_BY_INPUT_NAME]?.key === CONTROLLED_BY_PLAYER.key
            ? withPlayerControl
            : controller[CONTROLLED_BY_INPUT_NAME]?.key === CONTROLLED_BY_AI.key && withAiControl
        "
        v-for="(controller, index) in controllers || []"
        :key="index"
        :controls="controller[CONTROLS_INPUT_NAME]"
        :index="index"
        :name="controller.name"
        :side="controller.side"
      >
        <Paddle
          v-if="controller.side === 'left' && winner !== 2"
          :has-more-than-two-players="controllers.length > 2"
          :name="controller.name"
          :paddle-index="index"
          :side="controller.side"
        />
      </component>
      <component
        :is="
          controller[CONTROLLED_BY_INPUT_NAME]?.key === CONTROLLED_BY_PLAYER.key
            ? withPlayerControl
            : controller[CONTROLLED_BY_INPUT_NAME]?.key === CONTROLLED_BY_AI.key && withAiControl
        "
        v-for="(controller, index) in controllers || []"
        :key="index"
        :controls="controller[CONTROLS_INPUT_NAME]"
        :index="index"
        :name="controller.name"
        :side="controller.side"
      >
        <Paddle
          v-if="controller.side === 'right' && winner !== 1"
          :has-more-than-two-players="controllers.length > 2"
          :name="controller.name"
          :paddle-index="index"
          :side="controller.side"
        />
      </component>
    </div>
  </div>

  <GamePauseModalProvider ref="gamePauseModalRef" />
</template>

<script setup>
import { provideGameDimensions, useGameSocketInject } from 'entities/Game/composables';
import {
  BALL_COLOR_INPUT_NAME,
  BALL_DESIGN_INPUT_NAME,
  BALL_SKIN_INPUT_NAME,
  BALL_SKIN_TYPE_INPUT_NAME,
  CONTROLLED_BY_AI,
  CONTROLLED_BY_INPUT_NAME,
  CONTROLLED_BY_PLAYER,
  CONTROLLERS_INPUT_NAME,
  CONTROLS_INPUT_NAME,
  DEMO_DEFAULT_GAME_SETTINGS,
  DEMO_GAME_MODE,
  GAME_STATUS_IDLE,
  GAME_STATUS_IN_PROGRESS,
  MODE_INPUT_NAME,
  QUICK_START_GAME_MODE,
} from 'entities/Game/config/constants.js';
import { menu } from 'store/menu.js';
import { computed, inject, onMounted, onUnmounted, ref, watch } from 'vue';

import {
  Ball,
  Field,
  GamePauseModalProvider,
  Paddle,
  Score,
  withAiControl,
  withPlayerControl,
} from './components';

const showErrorModal = inject('showErrorModal');

const gamePauseModalRef = ref(null);
const gameContainerRef = ref(null);
const gameSocket = useGameSocketInject();
provideGameDimensions(gameContainerRef, gameSocket.actions.updateGameDimensions);

const settings = computed(() => gameSocket.gameSettings.value);
const controllers = computed(() => gameSocket.gameSettings.value[CONTROLLERS_INPUT_NAME]);
const status = computed(() => gameSocket.status.value);
const winner = computed(() => gameSocket.winner.value);

const handleKeyDown = (event) => {
  if (
    event.code === 'Escape' &&
    settings.value.mode !== DEMO_GAME_MODE &&
    status.value === GAME_STATUS_IN_PROGRESS
  ) {
    // noinspection JSUnresolvedReference
    gamePauseModalRef.value?.showGamePauseModal();
  }
};

watch(
  () => gameSocket.status.value,
  (newStatus) => {
    if (newStatus === GAME_STATUS_IDLE) {
      gameSocket.actions.startGame(DEMO_DEFAULT_GAME_SETTINGS);
    }

    if (settings.value.mode === DEMO_GAME_MODE) return;

    if (newStatus === GAME_STATUS_IN_PROGRESS) {
      menu.close();
    }
  }
);

watch(
  () => gameSocket.error.value,
  (error) => showErrorModal(null, error)
);

onMounted(() => {
  window.addEventListener('keydown', handleKeyDown);
});

onUnmounted(() => {
  gameSocket.actions.closeGameSocket();
  window.removeEventListener('keydown', handleKeyDown);
});
</script>

<style scoped>
.game {
  overflow: hidden;

  box-sizing: border-box;
  width: 100%;
  height: 100%;
  padding-right: 20px;
  padding-left: 20px;

  border-radius: 12px;
}

.game__container {
  position: relative;

  width: 100%;
  height: 100%;
  padding: 20px;

  background: linear-gradient(to right, var(--light-color) 50%, var(--dark-color) 50%);
}
</style>

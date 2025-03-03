<template>
  <Score :mode="settings[MODE_INPUT_NAME]" />
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
        :skin-type="settings[BALL_DESIGN_INPUT_NAME][BALL_SKIN_TYPE_INPUT_NAME]"
        :skin="settings[BALL_DESIGN_INPUT_NAME][BALL_SKIN_INPUT_NAME]"
      />
      <component
        :is="
          controller[CONTROLLED_BY_INPUT_NAME]?.key === CONTROLLED_BY_PLAYER.key
            ? withPlayerControl
            : controller[CONTROLLED_BY_INPUT_NAME]?.key === CONTROLLED_BY_AI.key && withAiControl
        "
        v-for="(controller, index) in controllers || []"
        :key="index"
        :name="controller.name"
        :index="index"
        :side="controller.side"
        :controls="controller[CONTROLS_INPUT_NAME]"
      >
        <Paddle
          v-if="controller.side === 'left' && winner !== 2"
          :name="controller.name"
          :side="controller.side"
          :paddle-index="index"
          :has-more-than-two-players="controllers.length > 2"
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
        :name="controller.name"
        :index="index"
        :side="controller.side"
        :controls="controller[CONTROLS_INPUT_NAME]"
      >
        <Paddle
          v-if="controller.side === 'right' && winner !== 1"
          :name="controller.name"
          :side="controller.side"
          :paddle-index="index"
          :has-more-than-two-players="controllers.length > 2"
        />
      </component>
    </div>
  </div>
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
  MODE_INPUT_NAME,
  QUICK_START_GAME_MODE,
} from 'entities/Game/config/constants.js';
import { computed, onUnmounted, ref } from 'vue';

import { Ball, Field, Paddle, Score, withAiControl, withPlayerControl } from './components';

const gameContainerRef = ref(null);
const gameSocket = useGameSocketInject();

const { settings } = defineProps({
  settings: {
    type: Object,
    default: () => ({ ...DEMO_DEFAULT_GAME_SETTINGS }),
  },
});

provideGameDimensions(gameContainerRef, gameSocket.actions.updateGameDimensions);

const controllers = computed(() => settings[CONTROLLERS_INPUT_NAME]);
const winner = computed(() => gameSocket.winner.value);

onUnmounted(() => {
  gameSocket.actions.closeGameSocket();
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

<template>
  <div class="game">
    <div class="game__background-container">
      <div class="game__void-boundary">
        <div class="game__void-boundary-shadow game__void-boundary-shadow_left" />
        <div class="game__void-boundary-shadow game__void-boundary-shadow_right" />
      </div>
      <div class="game__background" :style="{ transform: backgroundTransform }" />
      <div
        class="game__background-line game__background-line_left"
        :style="{ transform: lineTransform }"
      />
      <div class="game__background-center" :style="{ transform: centerTransform }" />
      <div
        class="game__background-line game__background-line_right"
        :style="{ transform: lineTransform }"
      />
    </div>
    <div ref="gameContainerRef" class="game__container">
      <Ball
        :color="settings[BALL_DESIGN_INPUT_NAME][BALL_COLOR_INPUT_NAME]"
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
          v-if="controller.side === 'left'"
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
          v-if="controller.side === 'right'"
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
import {
  BALL_COLOR_INPUT_NAME,
  BALL_DESIGN_INPUT_NAME,
  BALL_SKIN_INPUT_NAME,
  CONTROLLED_BY_AI,
  CONTROLLED_BY_INPUT_NAME,
  CONTROLLED_BY_PLAYER,
  CONTROLLERS_INPUT_NAME,
  CONTROLS_INPUT_NAME,
  DEMO_DEFAULT_GAME_SETTINGS,
} from 'entities/Game/config/constants.js';
import { computed, onUnmounted, ref } from 'vue';

import { Ball, Paddle, withAiControl, withPlayerControl } from './components';
import { provideGameDimensions, useGameSocketInject } from './composables';

const gameContainerRef = ref(null);
const gameSocket = useGameSocketInject();

const { settings } = defineProps({
  settings: {
    type: Object,
    default: () => ({ ...DEMO_DEFAULT_GAME_SETTINGS }),
  },
});

provideGameDimensions(gameContainerRef, gameSocket.actions.updateGameDimensions);

const positionX = computed(() => gameSocket.ballPositionX.value);
const positionY = computed(() => gameSocket.ballPositionY.value);
const controllers = computed(() => settings[CONTROLLERS_INPUT_NAME]);

const backgroundTransform = computed(() => {
  const minTranslate = -150;
  const maxTranslate = 150;

  const translateX = minTranslate + (positionX.value / 100) * (maxTranslate - minTranslate);
  const translateY = minTranslate + (positionY.value / 100) * (maxTranslate - minTranslate);

  return `translate(${translateX * -1}px, ${translateY * -1}px) scale(4)`;
});

const centerTransform = computed(() => {
  const minTranslate = -100;
  const maxTranslate = 100;

  let translateX = minTranslate + (positionX.value / 100) * (maxTranslate - minTranslate);
  const translateY = minTranslate + (positionY.value / 100) * (maxTranslate - minTranslate);

  return `translate(${(translateX + 60) * -1}px, ${(translateY + 60) * -1}px)`;
});

const lineTransform = computed(() => {
  const minTranslate = -100;
  const maxTranslate = 100;

  let translateX = minTranslate + (positionX.value / 100) * (maxTranslate - minTranslate);
  const translateY = minTranslate + (positionY.value / 100) * (maxTranslate - minTranslate);

  return `translate(${translateX * -1}px, ${translateY * -1}px) scaleY(4)`;
});

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

.game__background-container {
  position: absolute;
  top: 0;
  left: 0;

  overflow: hidden;

  width: 100%;
  height: 100%;

  background: linear-gradient(to right, var(--light-color) 50%, var(--dark-color) 50%);
  border-radius: 12px;
}

.game__background-container::after {
  content: '';

  position: absolute;
  z-index: 4;
  top: 0;
  left: 0;

  width: 100%;
  height: 100%;

  box-shadow: inset 40px 40px 90px var(--dark-color-opacity-50);
}

.game__background {
  position: absolute;
  z-index: 1;
  top: 0;
  left: 0;

  width: 100%;
  height: 100%;

  background: linear-gradient(to right, var(--light-color) 50%, var(--dark-color) 50%);

  transition: all 0.1s linear;
}

.game__background-center {
  position: absolute;
  z-index: 3;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);

  width: 120px;
  height: 120px;

  /* noinspection CssNonIntegerLengthInPixels */
  border: 0.5px solid var(--light-color-opacity-50);
  border-radius: 50%;
  mix-blend-mode: difference;

  transition: all 0.1s linear;
}

.game__background-line {
  position: absolute;
  z-index: 3;
  top: 0;
  transform: translate(-50%, -50%) scale(4);

  /* noinspection CssNonIntegerLengthInPixels */
  width: 0.5px;
  height: 100%;

  background-color: var(--light-color-opacity-50);
  mix-blend-mode: difference;

  transition: all 0.1s linear;
}

.game__background-line_left {
  left: 10%;
}

.game__background-line_right {
  left: 90%;
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

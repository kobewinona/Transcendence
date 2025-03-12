<template>
  <div class="field">
    <transition name="grow" mode="out-in">
      <div
        v-if="winner !== undefined && winner !== 0"
        :class="[
          'field__winner',
          {
            field__winner_left: winner === 1,
            field__winner_right: winner === 2,
          },
        ]"
      >
        <span
          :class="[
            'field__winner-side',
            {
              'field__winner-side_left': winner === 1,
              'field__winner-side_right': winner === 2,
            },
          ]"
          >{{ winner === 1 ? t('game.left_side') : t('game.right_side') }}</span
        >
        <span class="field__winner-badge">{{ t('game.won') }}</span>
      </div>
    </transition>
    <div class="field__void-boundary">
      <div class="field__void-boundary-shadow field__void-boundary-shadow_left" />
      <div class="field__void-boundary-shadow field__void-boundary-shadow_right" />
    </div>
    <div class="field__background" :style="{ transform: fieldTransform }">
      <BackgroundScore v-if="showScore" />
    </div>
    <div class="field__line field__line_left" :style="{ transform: lineTransform }" />
    <div class="field__center" :style="{ transform: centerTransform }" />
    <div class="field__line field__line_right" :style="{ transform: lineTransform }" />
  </div>
</template>

<script setup>
import { useGameSocketInject } from 'entities/Game/composables';
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

import { BackgroundScore } from './components';

const { t } = useI18n();

const gameSocket = useGameSocketInject();

const { showScore } = defineProps({
  showScore: {
    type: Boolean,
    default: true,
  },
});

const positionX = computed(() => gameSocket.ballPositionX.value || 50);
const positionY = computed(() => gameSocket.ballPositionY.value || 50);
const winner = computed(() => gameSocket.winner.value);

const fieldTransform = computed(() => {
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
</script>

<!--suppress CssUnusedSymbol -->
<style scoped>
.field {
  position: absolute;
  top: 0;
  left: 0;

  overflow: hidden;

  width: 100%;
  height: 100%;

  background: linear-gradient(to right, var(--light-color) 50%, var(--dark-color) 50%);
  border-radius: 12px;
}

.field::after {
  content: '';

  position: absolute;
  z-index: 4;
  top: 0;
  left: 0;

  width: 100%;
  height: 100%;

  box-shadow: inset 40px 40px 90px var(--dark-color-opacity-50);
}

.field__winner {
  position: absolute;
  z-index: 2;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) scale(1);

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-around;

  width: 150px;
  height: 150px;
  padding: var(--big-space);

  border-radius: 50%;
}

.field__winner_left {
  background: linear-gradient(to bottom, var(--light-color) 50%, var(--primary-color) 50%);
}

.field__winner_right {
  background: linear-gradient(to bottom, var(--dark-color) 50%, var(--primary-color) 50%);
}

.field__winner-side {
  text-align: center;
  white-space: nowrap;
}

.field__winner-side_left {
  color: var(--dark-color);
}

.field__winner-side_right {
  color: var(--light-color);
}

.field__winner-badge {
  text-transform: uppercase;
}

.field__void-boundary {
  position: absolute;
  top: 0;
  left: 0;

  display: flex;
  justify-content: space-between;

  width: 100%;
  height: 100%;
}

.field__void-boundary-shadow {
  position: absolute;
  z-index: 2;
  width: 7%;
  height: 100%;
}

.field__void-boundary-shadow_left {
  left: 0;
  background: linear-gradient(to right, var(--light-color), transparent);
}

.field__void-boundary-shadow_right {
  right: 0;
  background: linear-gradient(to left, var(--dark-color), transparent);
}

.field__background {
  position: absolute;
  z-index: 1;
  top: 0;
  left: 0;

  width: 100%;
  height: 100%;

  background: linear-gradient(to right, var(--light-color) 50%, var(--dark-color) 50%);

  transition: all 0.3s linear;
}

.field__center {
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

.field__line {
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

.field__line_left {
  left: 10%;
}

.field__line_right {
  left: 90%;
}

.grow-enter-active,
.grow-leave-active {
  transition: transform 0.4s ease;
}

.grow-enter-from {
  transform: translate(-50%, -50%) scale(0);
}

.grow-enter-to {
  transform: translate(-50%, -50%) scale(1);
}

.grow-leave-from {
  transform: translate(-50%, -50%) scale(1);
}

.grow-leave-to {
  transform: translate(-50%, -50%) scale(0);
}
</style>

<template>
  <div class="field">
    <Winner :winner="winner" />
    <div class="field__void-boundary">
      <div class="field__void-boundary-shadow field__void-boundary-shadow_left" />
      <div class="field__void-boundary-shadow field__void-boundary-shadow_right" />
    </div>
    <div :style="{ transform: fieldTransform }" class="field__background">
      <BackgroundScore v-if="showScore" />
    </div>
    <div :style="{ transform: lineTransform }" class="field__line field__line_left" />
    <div :style="{ transform: centerTransform }" class="field__center" />
    <div :style="{ transform: lineTransform }" class="field__line field__line_right" />
  </div>
</template>

<script setup>
import { useGameSocketInject } from 'entities/Game/composables';
import { computed } from 'vue';

import { BackgroundScore, Winner } from './components';

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
  border-radius: 14px;
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
  z-index: 5;
  width: 5%;
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

  /* noinspection CssNonIntegerLengthInPixels */
  height: 120px;

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

  width: 0.5px;
  height: 100%;

  /* noinspection CssNonIntegerLengthInPixels */
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

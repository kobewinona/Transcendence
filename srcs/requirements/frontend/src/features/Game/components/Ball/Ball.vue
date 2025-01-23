<template>
  <div
    class="wrapper"
    :class="{
      wrapper_bubbling_vertical: hasBouncedOff === 2 || hasBouncedOff === 4,
      wrapper_bubbling_horizontal: hasBouncedOff === 1 || hasBouncedOff === 3,
    }"
    :style="{
      ...styles,
      '--bubbling-animation': `${hasBouncedOff === 1 || hasBouncedOff === 3 ? 'bubble-anim-horizontal' : 'bubble-anim-vertical'}`,
      '--squash-offset': squashOffset,
    }"
    @animationend="onBubbleAnimationEnd"
  >
    <div
      class="ball"
      :class="{
        'curve-splash': isCurveApplied,
        'curve-splash-max': isMaxCurveApplied,
      }"
      :style="{
        '--rotate-direction': `${rotateDirection}deg`,
        '--rotate-duration': `${rotateDuration}s`,
      }"
      @animationend="onCurveSplashAnimationEnd"
    >
      <div class="ball__container">
        <div class="ball__core spinning" :style="{ backgroundImage: `url('${ballSkin}')` }" />
      </div>
    </div>
  </div>
</template>

<script setup>
// noinspection ES6UnusedImports
import ballSkin from 'assets/ballSkins/skin2.png';
import { mapRange } from 'shared/lib';
import { computed, ref, watch } from 'vue';

import { useGameDimensionsInject, useGameSocketInject } from '../../composables';
import {
  MAX_CURVE,
  MAX_ROTATE_DURATION,
  MIN_CURVE,
  MIN_ROTATE_DURATION,
} from './config/constants.js';

const { ballWidth, ballHeight } = useGameDimensionsInject();
const gameSocket = useGameSocketInject();

const hasBouncedOff = ref(2);
const isCurveApplied = ref(false);
const isMaxCurveApplied = ref(false);

const squashOffset = ref(0.4);
const rotateDuration = ref(MAX_ROTATE_DURATION);
const rotateDirection = ref(0);

const positionX = computed(() => gameSocket.ballPositionX.value);
const positionY = computed(() => gameSocket.ballPositionY.value);
const velocityX = computed(() => gameSocket.ballVelocityX.value);
const isOutOfBounds = computed(() => gameSocket.isBallOutOfBounds.value);
const curve = computed(() => gameSocket.ballCurve.value);
const bouncedOffSurface = computed(() => gameSocket.ballBouncedOffSurface.value);

const styles = computed(() => {
  if (positionX.value === undefined || positionY.value === undefined) return {};

  const isCenter = positionY.value === 50 && positionX.value === 50;
  const transitionTime = !isOutOfBounds.value && !isCenter ? 25 : 0;

  return {
    width: `${ballWidth.value}%`,
    height: `${ballHeight.value}%`,
    top: `${positionY.value}%`,
    left: `${positionX.value}%`,
    transition: `top ${transitionTime}ms linear, left ${transitionTime}ms linear, transform 1s linear`,
  };
});

function updateBallProperties() {
  const curveVelocity = Math.abs(curve.value);
  isCurveApplied.value = curveVelocity > 1.5;
  isMaxCurveApplied.value = curveVelocity > 3.5;

  if (curve.value === 0) {
    rotateDuration.value = MAX_ROTATE_DURATION;
  }

  rotateDuration.value =
    MAX_ROTATE_DURATION -
    mapRange(curveVelocity, MIN_CURVE, MAX_CURVE, MIN_ROTATE_DURATION, MAX_ROTATE_DURATION);

  rotateDirection.value = velocityX.value > 0 ? 360 : -360;
  squashOffset.value = parseFloat(mapRange(Math.abs(velocityX.value), 0.5, 2, 0, 0.4).toFixed(2));
}

function resetRotation() {
  rotateDuration.value = MAX_ROTATE_DURATION;
  rotateDirection.value = 0;
}

watch(
  () => isOutOfBounds.value,
  () => {
    resetRotation();
  }
);

watch(
  () => bouncedOffSurface.value,
  (newValue = 0) => {
    hasBouncedOff.value = newValue;

    if (newValue === 2 || newValue === 4) {
      // hasBouncedOff.value = newValue;
      updateBallProperties();
    }
  }
);

const onBubbleAnimationEnd = () => {
  hasBouncedOff.value = 0;
};

const onCurveSplashAnimationEnd = () => {
  isCurveApplied.value = false;
  isMaxCurveApplied.value = false;
};
</script>

<!--suppress CssUnusedSymbol -->
<style scoped>
@keyframes bubble-anim-vertical {
  0% {
    transform: scale(1);
  }

  10% {
    transform: scale(0.85, 1.15);
  }

  40% {
    transform: scale(0.75, 1.1);
  }

  70% {
    transform: scale(1.1, 0.9);
  }

  80% {
    transform: scale(0.95, 1.05);
  }

  97%,
  100% {
    transform: scale(1);
  }
}

@keyframes bubble-anim-horizontal {
  0% {
    transform: scale(1);
  }

  5% {
    transform: scale(1.25, 0.65);
  }

  40% {
    transform: scale(0.85, 1.1);
  }

  70% {
    transform: scale(1.15, 0.75);
  }

  80% {
    transform: scale(0.9, 1);
  }

  97%,
  100% {
    transform: scale(1);
  }
}

@keyframes rotate {
  0% {
    transform: translate(-50%, -50%) rotate(0);
  }

  100% {
    transform: translate(-50%, -50%) rotate(var(--rotate-direction));
  }
}

@keyframes spin {
  0% {
    transform: scale(1.4);
    background-position: 0 50%;
  }

  50% {
    transform: scale(1);
  }

  100% {
    transform: scale(1.4);
    background-position: 200% 50%;
  }
}

@keyframes curve-splash-wiggle {
  0% {
    transform: scale(1) rotate(0deg) translate(0, 0);
    opacity: 1;
    border-width: 2px;
  }

  10% {
    transform: scale(1.2) rotate(5deg) translate(3px, -3px);
    opacity: 0.9;
    border-width: 4px;
  }

  20% {
    transform: scale(1.5) rotate(-5deg) translate(-3px, 3px);
    opacity: 0.8;
    border-width: 6px;
  }

  50% {
    transform: scale(2) rotate(3deg) translate(2px, -2px);
    opacity: 0.4;
    border-width: 8px;
  }

  75% {
    transform: scale(2.5) rotate(-3deg) translate(-2px, 2px);
    opacity: 0.2;
    border-width: 10px;
  }

  100% {
    transform: scale(3) rotate(0deg) translate(0, 0);
    opacity: 0;
  }
}

@keyframes curve-rotate {
  0% {
    transform: rotate(0deg) scale(1);
    opacity: 1;
  }

  60% {
    transform: rotate(360deg) scale(1.5);
    opacity: 0.8;
  }

  99% {
    transform: rotate(-360deg) scale(3);
  }

  100% {
    transform: rotate(360deg);
    opacity: 0;
  }
}

.wrapper {
  --squash-offset: 0;
  --rotate-direction: 0;
  --rotate-duration: 0;

  position: absolute;
  z-index: 1;
  top: 0;
  left: 0;

  width: 150px;
  height: 150px;
}

.wrapper_bubbling_vertical {
  animation: bubble-anim-vertical 0.4s ease-in-out;
}

.wrapper_bubbling_horizontal {
  animation: bubble-anim-horizontal 0.4s ease-in-out;
}

.ball {
  width: 100%;
  height: 100%;

  background-color: var(--primary-color);
  border-radius: 50%;

  animation: rotate 4s linear infinite;
}

.ball.curve-splash::before {
  content: '';

  position: absolute;
  z-index: 5;
  top: 0;
  left: 0;

  box-sizing: content-box;
  width: 100%;
  height: 100%;

  opacity: 0;
  background-color: var(--primary-color);
  border-radius: 50%;
  mix-blend-mode: multiply;

  animation: curve-splash-wiggle 1s linear;
}

.ball.curve-splash-max::after {
  pointer-events: none;
  content: '';

  position: absolute;
  z-index: 100;
  top: -10%;
  left: -10%;

  width: 110%;
  height: 110%;

  opacity: 0;
  border-top: 4px solid var(--secondary-color);
  border-right: 4px solid var(--secondary-color);
  border-radius: 50%;
  mix-blend-mode: hard-light;

  animation: curve-rotate 1s linear;
}

.ball__container {
  overflow: hidden;
  width: 100%;
  height: 100%;
  border-radius: 50%;
}

.ball__core {
  transform-origin: center;

  width: 100%;
  height: 100%;

  background-repeat: repeat-x;
  background-position: 0 50%;
  background-size: 200% 200%;

  animation: spin var(--rotate-duration) linear infinite;
}
</style>

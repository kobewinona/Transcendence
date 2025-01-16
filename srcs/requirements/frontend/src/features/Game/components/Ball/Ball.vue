<script setup>
import ballSkin from 'assets/ballSkins/skin2.png';
import { mapRange } from 'shared/lib';
import { computed, defineProps, onMounted, onUnmounted, ref, watch } from 'vue';

import {
  MAX_CURVE,
  MAX_ROTATE_DURATION,
  MIN_CURVE,
  MIN_ROTATE_DURATION,
} from './config/constants.js';

const {
  width,
  height,
  position,
  isPositionForced,
  velocity,
  isOutOfBounds,
  curve,
  ballBouncedOffSurface,
} = defineProps({
  width: { type: Number, default: 100 },
  height: { type: Number, default: 100 },
  position: {
    type: Object,
    required: true,
    validator: (value) => {
      return typeof value.x === 'number' && typeof value.y === 'number';
    },
  },
  isPositionForced: {
    type: Boolean,
    default: false,
  },
  velocity: {
    type: Object,
    required: true,
    validator: (value) => {
      return typeof value.x === 'number' && typeof value.y === 'number';
    },
  },
  isOutOfBounds: {
    type: Boolean,
    required: true,
  },
  curve: {
    type: Number,
    required: true,
  },
  ballBouncedOffSurface: {
    type: Number,
    required: true,
    validator: (value) => value >= 1 && value <= 4,
  },
});

const ballPosition = ref({ x: position?.x || 50, y: position?.y || 50 });
const previousXVelocitySign = ref(velocity?.x > 0 ? 1 : -1);
const hasBouncedOff = ref(0);
const isCurveApplied = ref(false);
const isMaxCurveApplied = ref(false);
let animationFrameId = null;

const squashOffset = ref(0.4);
const rotateDuration = ref(MAX_ROTATE_DURATION);
const rotateDirection = ref(0);

const styles = computed(() => {
  const isCenter = ballPosition.value.y === 50 && ballPosition.value.x === 50;
  const transitionTime = !isOutOfBounds && !isCenter ? 25 : 0;

  return {
    width: `${width}%`,
    height: `${height}%`,
    top: `${isPositionForced ? ballPosition.value.y + height : ballPosition.value.y}%`,
    left: `${isPositionForced ? ballPosition.value.x - width : ballPosition.value.x}%`,
    zIndex: isPositionForced ? 100 : 1,
    transition: `top ${isPositionForced ? 100 : transitionTime}ms linear,
      left ${isPositionForced ? 100 : transitionTime}ms linear,
      transform 1s linear`,
  };
});

watch(
  () => velocity,
  (newVelocity) => {
    const curveVelocity = Math.abs(curve);
    if (curveVelocity > 1.5) {
      isCurveApplied.value = true;
      isMaxCurveApplied.value = curveVelocity > 3.5;
    }

    if (curve === 0) {
      rotateDuration.value = MAX_ROTATE_DURATION;
    }

    const newXVelocitySign = newVelocity?.x > 0 ? 1 : -1;
    if (newXVelocitySign !== previousXVelocitySign.value) {
      rotateDuration.value =
        MAX_ROTATE_DURATION -
        mapRange(curveVelocity, MIN_CURVE, MAX_CURVE, MIN_ROTATE_DURATION, MAX_ROTATE_DURATION);
      rotateDirection.value = newVelocity?.x > 0 ? 360 : -360;
      squashOffset.value = parseFloat(
        mapRange(Math.abs(newVelocity?.x), 0.5, 2, 0, 0.4).toFixed(2)
      );
    }

    previousXVelocitySign.value = newXVelocitySign;
  },
  { immediate: true }
);

watch(
  () => ballBouncedOffSurface,
  (newValue) => {
    hasBouncedOff.value = 0;
    setTimeout(() => {
      hasBouncedOff.value = newValue;
    }, 10);
  }
);

const update = () => {
  ballPosition.value.x = position?.x;
  ballPosition.value.y = position?.y;
  animationFrameId = requestAnimationFrame(update);
};

const onBubbleAnimationEnd = () => {
  hasBouncedOff.value = 0;
};

const onCurveSplashAnimationEnd = () => {
  isCurveApplied.value = false;
  isMaxCurveApplied.value = false;
};

onMounted(() => {
  animationFrameId = requestAnimationFrame(update);
});

onUnmounted(() => {
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId);
  }
});
</script>

<template>
  <div
    class="wrapper"
    :class="{
      wrapper_bubbling_vertical: !isPositionForced && (hasBouncedOff === 2 || hasBouncedOff === 4),
      wrapper_bubbling_horizontal:
        !isPositionForced && (hasBouncedOff === 1 || hasBouncedOff === 3),
    }"
    :style="{
      ...styles,
      '--bubbling-animation': `${!isPositionForced && (hasBouncedOff === 1 || hasBouncedOff === 3) ? 'bubble-anim-horizontal' : 'bubble-anim-vertical'}`,
      '--squash-offset': squashOffset,
    }"
    @animationend="onBubbleAnimationEnd"
  >
    <div
      class="ball"
      :class="{
        'curve-splash': !isPositionForced && isCurveApplied,
        'curve-splash-max': !isPositionForced && isMaxCurveApplied,
      }"
      :style="{
        '--rotate-direction': `${isPositionForced ? 360 : rotateDirection}deg`,
        '--rotate-duration': `${isPositionForced ? MAX_ROTATE_DURATION : rotateDuration}s`,
      }"
      @animationend="onCurveSplashAnimationEnd"
    >
      <div class="ball__container">
        <div
          class="ball__core"
          :style="{ backgroundImage: `url('${ballSkin}')` }"
          :class="{ spinning: !isPositionForced && velocity !== 0 }"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
@keyframes bubble-anim-vertical {
  0% {
    transform: scale(1);
  }

  20% {
    /* noinspection CssUnresolvedCustomProperty */
    transform: scaleY(calc(0.8 + var(--squash-offset))) scaleX(calc(1.2 - var(--squash-offset)));
  }

  48% {
    /* noinspection CssUnresolvedCustomProperty */
    transform: scaleY(calc(1.25 - var(--squash-offset))) scaleX(calc(0.75 + var(--squash-offset)));
  }

  68% {
    /* noinspection CssUnresolvedCustomProperty */
    transform: scaleY(calc(0.83 + var(--squash-offset))) scaleX(calc(1.17 - var(--squash-offset)));
  }

  80% {
    /* noinspection CssUnresolvedCustomProperty */
    transform: scaleY(calc(1.17 - var(--squash-offset))) scaleX(calc(0.83 + var(--squash-offset)));
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

  20% {
    /* noinspection CssUnresolvedCustomProperty */
    transform: scaleX(calc(1.2 - var(--squash-offset))) scaleY(calc(0.8 + var(--squash-offset)));
  }

  48% {
    /* noinspection CssUnresolvedCustomProperty */
    transform: scaleX(calc(0.75 + var(--squash-offset))) scaleY(calc(1.25 - var(--squash-offset)));
  }

  68% {
    /* noinspection CssUnresolvedCustomProperty */
    transform: scaleX(calc(1.17 - var(--squash-offset))) scaleY(calc(0.83 + var(--squash-offset)));
  }

  80% {
    /* noinspection CssUnresolvedCustomProperty */
    transform: scaleX(calc(0.83 + var(--squash-offset))) scaleY(calc(1.17 - var(--squash-offset)));
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
    /* noinspection CssUnresolvedCustomProperty */
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
  position: absolute;
  z-index: 1;
  top: 0;
  left: 0;

  width: 150px;
  height: 150px;
}

.wrapper_bubbling_vertical {
  animation: bubble-anim-vertical 0.4s linear;
}

.wrapper_bubbling_horizontal {
  animation: bubble-anim-horizontal 0.4s linear;
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

  /* noinspection CssUnresolvedCustomProperty */
  animation: spin var(--rotate-duration) linear infinite;
}
</style>

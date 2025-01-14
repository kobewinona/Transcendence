<script setup>
import ballSkin from 'assets/ballSkins/skin2.png';
import { computed, defineProps, onMounted, onUnmounted, ref, watch } from 'vue';

const { width, height, position, velocity, isOutOfBounds, curve } = defineProps({
  width: { type: Number, default: 100 },
  height: { type: Number, default: 100 },
  position: {
    type: Object,
    required: true,
    validator: (value) => {
      return typeof value.x === 'number' && typeof value.y === 'number';
    },
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
});

const ballPosition = ref({ x: position?.x, y: position?.y });
const previousXVelocitySign = ref(velocity?.x > 0 ? 1 : -1);
let animationFrameId = null;
const rotateDuration = ref(1);
const rotateDirection = ref(0);

const styles = computed(() => ({
  width: `${width}%`,
  height: `${height}%`,
  top: `${ballPosition.value.y}%`,
  left: `${ballPosition.value.x}%`,
  transition: `top ${!isOutOfBounds && ballPosition.value.y !== 50 && ballPosition.value.x !== 50 ? 25 : 0}ms linear,
    left ${!isOutOfBounds && ballPosition.value.y !== 50 && ballPosition.value.x !== 50 ? 25 : 0}ms linear,
    transform 1s linear`,
}));

const mapVelocityToDegrees = (velocityValue) => {
  const minVelocity = 0.5;
  const maxVelocity = 2;
  const minDegrees = 0;
  const maxDegrees = 360;

  return (
    minDegrees +
    ((velocityValue - minVelocity) / (maxVelocity - minVelocity)) * (maxDegrees - minDegrees)
  );
};

const mapCurveToDuration = () => {
  const minCurve = 0;
  const maxCurve = 5;
  const minDuration = 0.2;
  const maxDuration = 1.2;

  return maxDuration - ((curve - minCurve) / (maxCurve - minCurve)) * (maxDuration - minDuration);
};

watch(
  () => velocity,
  (newVelocity) => {
    const newXVelocitySign = newVelocity?.x > 0 ? 1 : -1;
    if (newXVelocitySign !== previousXVelocitySign.value) {
      rotateDuration.value = mapCurveToDuration();
      rotateDirection.value = mapVelocityToDegrees(newVelocity?.y);
    }

    previousXVelocitySign.value = newXVelocitySign;
  },
  { immediate: true }
);

const update = () => {
  ballPosition.value.x = position?.x;
  ballPosition.value.y = position?.y;
  animationFrameId = requestAnimationFrame(update);
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
    class="ball"
    :style="{
      ...styles,
      '--rotate-direction': `${rotateDirection}deg`,
    }"
  >
    <div
      class="ball__core"
      :style="{
        backgroundImage: `url('${ballSkin}')`,
        '--rotate-duration': `${rotateDuration}s`,
      }"
      :class="{ spinning: velocity !== 0 }"
    />
  </div>
</template>

<style scoped>
@keyframes bubble-anim {
  0% {
    transform: scale(1);
  }

  20% {
    transform: scaleY(0.95) scaleX(1.05);
  }

  48% {
    transform: scaleY(1.1) scaleX(0.9);
  }

  68% {
    transform: scaleY(0.98) scaleX(1.02);
  }

  80% {
    transform: scaleY(1.02) scaleX(0.98);
  }

  97%,
  100% {
    transform: scale(1);
  }
}

.ball {
  position: absolute;
  z-index: 1;

  /* noinspection CssUnresolvedCustomProperty */
  transform: translate(-50%, -50%) rotate(var(--rotate-direction));

  overflow: hidden;

  width: 150px;
  height: 150px;

  background-color: var(--primary-color);
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
</style>

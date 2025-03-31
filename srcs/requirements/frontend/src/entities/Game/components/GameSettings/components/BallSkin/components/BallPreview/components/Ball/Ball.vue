<template>
  <div class="ball">
    <div
      class="ball__container"
      :class="{
        'curve-splash': isCurveApplied,
        'curve-splash-max': isMaxCurveApplied,
      }"
      :style="{ ...styles }"
    >
      <div class="ball__wrapper">
        <div
          class="ball__core spinning"
          :style="{
            backgroundColor: dynamicColor,
            backgroundImage: `url('${dynamicSkin}')`,
            '--rotate-duration': `${rotateDuration}s`,
          }"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';

const { color, skin, rotateDuration, rotateDirection } = defineProps({
  color: {
    type: String,
    default: '',
  },
  skin: {
    type: String,
    default: '',
  },
  rotateDuration: {
    type: Number,
    required: true,
  },
  rotateDirection: {
    type: Number,
    required: true,
  },
});

const dynamicColor = computed(() => color);
const dynamicSkin = computed(() => skin);

const isCurveApplied = ref(false);
const isMaxCurveApplied = ref(false);

const styles = computed(() => {
  return {
    '--rotate-direction': `${rotateDirection}deg`,
    '--rotate-direction-end': rotateDirection < 0 ? '-360deg' : '360deg',
    '--rotate-duration': `${rotateDuration}s`,
  };
});
</script>

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
    transform: rotate(0);
  }

  50% {
    transform: rotate(var(--rotate-direction));
  }

  100% {
    transform: rotate(var(--rotate-direction-end));
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

.ball {
  --squash-offset: 0;
  --rotate-direction: 0;
  --rotate-direction-end: 0;
  --rotate-duration: 0;

  width: 150px;
  height: 150px;
}

.ball_bubbling_vertical {
  animation: bubble-anim-vertical 0.4s ease-in-out;
}

.ball_bubbling_horizontal {
  animation: bubble-anim-horizontal 0.4s ease-in-out;
}

.ball__container {
  width: 100%;
  height: 100%;

  background-color: var(--primary-color);
  border-radius: 50%;

  animation: rotate 4s linear infinite;
}

.ball__container.curve-splash::before {
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

.ball__container.curve-splash-max::after {
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

.ball__wrapper {
  overflow: hidden;

  width: 100%;
  height: 100%;

  border-radius: 50%;

  transition: all 0.2s ease-in-out;
}

.ball__core {
  transform-origin: center;

  display: flex;
  align-items: center;
  justify-content: center;

  width: 100%;
  height: 100%;

  background-repeat: repeat-x;
  background-position: 0 50%;
  background-size: 200% 200%;

  transition: all 0.4s ease-in-out;
  animation: spin var(--rotate-duration) linear infinite;
}
</style>

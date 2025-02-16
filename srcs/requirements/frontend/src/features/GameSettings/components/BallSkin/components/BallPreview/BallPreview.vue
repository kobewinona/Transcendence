<template>
  <div class="ball-preview">
    <div class="ball-preview__params">
      <p class="ball-preview__params-text">
        {{
          `${t('game_settings.tabs.ball_skin.ball_preview.direction')}: ${
            rotateDirection < 0 ? '<' : '>'
          }`
        }}
      </p>
      <p class="ball-preview__params-text">
        {{ `${t('game_settings.tabs.ball_skin.ball_preview.rotation_speed')}: ${curve}` }}
      </p>
    </div>
    <div class="ball-preview__ball-container">
      <div class="ball-preview__rotation-controls">
        <button
          class="ball-preview__btn"
          type="button"
          title="Direction: right"
          @click="decrementCurve"
        >
          <component
            :is="svgComponents['CircularArrowIcon']"
            v-if="isVueComponent(svgComponents['CircularArrowIcon'])"
            class="ball-preview__btn-icon ball-preview__turn-icon_left"
          />
        </button>
        <button
          class="ball-preview__btn"
          type="button"
          title="Direction: right"
          @click="resetCurve"
        >
          <component
            :is="svgComponents['DeclineIcon']"
            v-if="isVueComponent(svgComponents['DeclineIcon'])"
            class="ball-preview__btn-icon"
          />
        </button>
        <button
          class="ball-preview__btn"
          type="button"
          title="Direction: left"
          @click="incrementCurve"
        >
          <component
            :is="svgComponents['CircularArrowIcon']"
            v-if="isVueComponent(svgComponents['CircularArrowIcon'])"
            class="ball-preview__btn-icon"
          />
        </button>
      </div>
      <div class="ball-preview__direction-controls">
        <button
          class="ball-preview__btn"
          type="button"
          title="Direction: right"
          @click="() => changeVelocity(0)"
        >
          <component
            :is="svgComponents['RightTurnIcon']"
            v-if="isVueComponent(svgComponents['RightTurnIcon'])"
            class="ball-preview__btn-icon ball-preview__turn-icon_left"
          />
        </button>
        <button
          class="ball-preview__btn"
          type="button"
          title="Direction: left"
          @click="() => changeVelocity(1)"
        >
          <component
            :is="svgComponents['RightTurnIcon']"
            v-if="isVueComponent(svgComponents['RightTurnIcon'])"
            class="ball-preview__btn-icon"
          />
        </button>
      </div>
      <Ball
        :color="color"
        :skin="skin"
        :rotate-duration="rotateDuration"
        :rotate-direction="rotateDirection"
      />
    </div>
  </div>
</template>

<script setup>
import { isVueComponent, svgComponents } from 'shared/lib';
import { computed, ref } from 'vue';
import { useI18n } from 'vue-i18n';

import { Ball } from './components';

const { t } = useI18n();

const { color, skin } = defineProps({
  color: {
    type: String,
    default: '',
  },
  skinType: {
    type: String,
    default: '',
  },
  skin: {
    type: String,
    default: '',
  },
});

const curveIncrementValue = 0.1;
const velocity = ref(0);
const curve = ref(0);
const rotateDuration = ref(1);

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

const rotateDirection = computed(() => {
  return mapVelocityToDegrees(velocity.value);
});

const changeVelocity = (newVelocity) => {
  velocity.value = newVelocity;
};

const incrementCurve = () => {
  curve.value = parseFloat((curve.value + curveIncrementValue).toFixed(2));
  if (curve.value >= 1) curve.value = 0;
  rotateDuration.value = Math.abs(1 - curve.value);
};

const resetCurve = () => {
  curve.value = 0;
  rotateDuration.value = 1;
};

const decrementCurve = () => {
  const newCurve = parseFloat((curve.value - curveIncrementValue).toFixed(2));
  curve.value = newCurve >= 0 ? newCurve : 0;
  rotateDuration.value = Math.abs(1 - curve.value);
};
</script>

<style scoped>
.ball-preview {
  display: flex;
  flex-direction: column;
  row-gap: var(--big-space);
  align-items: center;
  justify-content: center;

  width: 100%;
  height: 100%;
}

.ball-preview__params {
  display: flex;
  flex-direction: column;
  row-gap: var(--smaller-space);

  width: 100%;
  padding: var(--smaller-space);

  background-color: var(--dark-color);
  border: 1px solid var(--light-color-opacity-50);
  border-radius: 12px;
}

.ball-preview__params-text {
  margin: 0;
}

.ball-preview__ball-container {
  position: relative;

  display: flex;
  align-items: center;
  justify-content: center;

  width: 100%;
  height: 100%;
}

.ball-preview__rotation-controls {
  position: absolute;
  top: 0;
  right: 0;

  display: flex;
  flex-direction: row;
  column-gap: var(--smaller-space);
}

.ball-preview__direction-controls {
  position: absolute;
  top: 50%;
  left: 0;
  transform: translateY(-50%);

  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;

  width: 100%;
}

.ball-preview__btn {
  cursor: pointer;

  display: flex;
  align-items: center;
  justify-content: center;

  width: max-content;
  height: max-content;
  padding: var(--small-space);

  background-color: transparent;
  border: 1px solid var(--light-color);
  border-radius: 12px;
}

.ball-preview__btn-icon {
  width: 30px;
  height: 30px;

  fill: var(--light-color);
  stroke: var(--light-color);

  transition: opacity 0.2s ease-in-out;
}

.ball-preview__btn-icon_small {
  width: 15px;
  height: 15px;
}

.ball-preview__turn-icon_left {
  transform: rotate(180deg);
}

.ball-preview__btn-icon:hover {
  opacity: 0.7;
  transition: opacity 0.2s ease-in-out;
}
</style>

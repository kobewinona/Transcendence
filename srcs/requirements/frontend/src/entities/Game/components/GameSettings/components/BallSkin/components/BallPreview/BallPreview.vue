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
        <MyButton
          class-name="ball-preview__button ball-preview__button-icon_arrow-left"
          icon-class-name="ball-preview__button-icon"
          type="button"
          :title="t('game_settings.tabs.ball_skin.ball_preview.rotation_speed.decrement.aria')"
          variant="ghost"
          :icon="svgComponents['CircularArrowIcon']"
          :aria-label="t('game_settings.tabs.ball_skin.ball_preview.rotation_speed.decrement.aria')"
          @click="decrementRotationSpeed"
        />
        <MyButton
          class-name="ball-preview__button"
          icon-class-name="ball-preview__button-icon"
          type="button"
          :title="t('game_settings.tabs.ball_skin.ball_preview.rotation_speed.reset.aria')"
          variant="ghost"
          :icon="svgComponents['DeclineIcon']"
          :aria-label="t('game_settings.tabs.ball_skin.ball_preview.rotation_speed.reset.aria')"
          @click="resetRotationSpeed"
        />
        <MyButton
          class-name="ball-preview__button"
          icon-class-name="ball-preview__button-icon"
          type="button"
          :title="t('game_settings.tabs.ball_skin.ball_preview.rotation_speed.increment.aria')"
          variant="ghost"
          :icon="svgComponents['CircularArrowIcon']"
          :aria-label="t('game_settings.tabs.ball_skin.ball_preview.rotation_speed.increment.aria')"
          @click="incrementRotationSpeed"
        />
      </div>
      <div class="ball-preview__direction-controls">
        <MyButton
          class-name="ball-preview__button ball-preview__button-icon_arrow-left"
          icon-class-name="ball-preview__button-icon"
          type="button"
          :title="t('game_settings.tabs.ball_skin.ball_preview.direction.left.aria')"
          variant="ghost"
          :icon="svgComponents['RightTurnIcon']"
          :aria-label="t('game_settings.tabs.ball_skin.ball_preview.direction.left.aria')"
          @click="() => changeVelocity(0)"
        />
        <MyButton
          class-name="ball-preview__button"
          icon-class-name="ball-preview__button-icon"
          type="button"
          :title="t('game_settings.tabs.ball_skin.ball_preview.direction.right.aria')"
          variant="ghost"
          :icon="svgComponents['RightTurnIcon']"
          :aria-label="t('game_settings.tabs.ball_skin.ball_preview.direction.right.aria')"
          @click="() => changeVelocity(1)"
        />
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
import { MyButton } from 'components';
import { svgComponents } from 'shared/lib';
import { computed, ref } from 'vue';
import { useI18n } from 'vue-i18n';

import { Ball } from './components';

const { t } = useI18n();

const { color, skin } = defineProps({
  color: {
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

const incrementRotationSpeed = () => {
  curve.value = parseFloat((curve.value + curveIncrementValue).toFixed(2));
  if (curve.value >= 1) curve.value = 0;
  rotateDuration.value = Math.abs(1 - curve.value);
};

const resetRotationSpeed = () => {
  curve.value = 0;
  rotateDuration.value = 1;
};

const decrementRotationSpeed = () => {
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

::v-deep(.ball-preview__button) {
  width: 44px;
  height: 44px;
}

::v-deep(.ball-preview__button-icon) {
  width: 34px;
  height: 34px;
}

::v-deep(.ball-preview__button-icon_arrow-left) {
  rotate: -180deg;
}
</style>

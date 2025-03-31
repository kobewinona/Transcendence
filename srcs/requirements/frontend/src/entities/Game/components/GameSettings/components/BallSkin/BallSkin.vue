<template>
  <div class="ball-skin">
    <ScrollLayout>
      <div class="ball-skin__views">
        <div class="ball-skin__views-section">
          <p class="ball-skin__list-title">
            {{ t('game_settings.tabs.ball_skin.colors.title') }}
          </p>
          <ul class="ball-skin__list">
            <li
              v-for="(color, index) in BALL_COLORS"
              :key="index"
              :class="[
                'ball-skin__list-item',
                {
                  'ball-skin__list-item_active':
                    activeSkinType === BALL_REGULAR_TYPE_SKIN_KEY && index === activeColorIndex,
                },
              ]"
            >
              <MyButton
                class-name="ball-skin__button"
                type="button"
                variant="ghost"
                :disabled="activeSkinType === BALL_SPECIAL_TYPE_SKIN_KEY"
                @click="handleColorChange(index)"
              >
                <span
                  :class="[
                    'ball-skin__list-element',
                    'ball-skin__list-element_color',
                    {
                      'ball-skin__list-element_disabled':
                        activeSkinType === BALL_SPECIAL_TYPE_SKIN_KEY,
                    },
                  ]"
                  :style="{ backgroundColor: `var(${color})` }"
                />
              </MyButton>
            </li>
          </ul>
        </div>
        <SkinsList :skin-type="BALL_REGULAR_TYPE_SKIN_KEY" :active-color-index="activeColorIndex" />
        <SkinsList :skin-type="BALL_SPECIAL_TYPE_SKIN_KEY" :active-color-index="activeColorIndex" />
      </div>
    </ScrollLayout>

    <BallPreview
      :color="`var(${BALL_COLORS[activeColorIndex]})`"
      :skin="BALL_SKINS[activeSkinType][activeSkinIndex]"
    />
  </div>
</template>

<script setup>
import { MyButton } from 'components';
import {
  BALL_COLORS,
  BALL_REGULAR_TYPE_SKIN_KEY,
  BALL_SKINS,
  BALL_SPECIAL_TYPE_SKIN_KEY,
} from 'entities/BallSkin/config/constants.js';
import {
  BALL_COLOR_INPUT_NAME,
  BALL_DESIGN_INPUT_NAME,
  BALL_SKIN_INPUT_NAME,
  BALL_SKIN_TYPE_INPUT_NAME,
} from 'entities/Game/config/constants.js';
import { ScrollLayout } from 'layouts';
import { useField } from 'vee-validate';
import { computed, toRef } from 'vue';
import { useI18n } from 'vue-i18n';

import { BallPreview, SkinsList } from './components';

const { t } = useI18n();

const { value: activeColor, setValue: setColor } = useField(
  toRef(() => `${BALL_DESIGN_INPUT_NAME}.${BALL_COLOR_INPUT_NAME}`)
);
const { value: activeSkinType } = useField(
  toRef(() => `${BALL_DESIGN_INPUT_NAME}.${BALL_SKIN_TYPE_INPUT_NAME}`)
);
const { value: currentSkin } = useField(
  toRef(() => `${BALL_DESIGN_INPUT_NAME}.${BALL_SKIN_INPUT_NAME}`)
);

const activeColorIndex = computed(() =>
  BALL_COLORS.findIndex((color) => color === activeColor.value)
);
const activeSkinIndex = computed(() =>
  BALL_SKINS[activeSkinType.value]?.findIndex((skin) => skin === currentSkin.value)
);

const handleColorChange = (index) => {
  setColor(BALL_COLORS[index]);
};
</script>

<style scoped>
.ball-skin {
  display: grid;
  grid-template-columns: 1fr 1fr;
  column-gap: var(--big-space);

  width: 100%;
  height: 100%;
}

.ball-skin__views {
  scrollbar-gutter: stable;

  overflow: hidden auto;
  display: flex;
  flex-direction: column;
  row-gap: var(--big-space);

  width: 100%;
}

.ball-skin__views-section {
  display: flex;
  flex-direction: column;
  row-gap: var(--small-space);
  width: 100%;
}

.ball-skin__list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--smaller-space);

  margin: 0;
  padding: var(--smaller-space) 0;

  list-style: none;

  border-top: 1px solid var(--light-color-opacity-50);
  border-bottom: 1px solid var(--light-color-opacity-50);
}

.ball-skin__list-title {
  margin: 0;
  font-weight: 600;
}

.ball-skin__list-item {
  box-sizing: border-box;
  width: max-content;
  height: max-content;

  font-size: 0;

  border: 2px solid var(--dark-color);
  border-radius: 12px;
}

::v-deep(.ball-skin__list-item_active) {
  border: 2px solid var(--light-color);
  border-radius: 12px;
  transition: all 0.4s ease-in-out;
}

.ball-skin__list-element {
  display: block;

  width: 50px;
  height: 50px;

  background-size: contain;
  border-radius: 50%;

  transition: background-color 0.4s ease-in-out;
}

.ball-skin__list-element_color {
  width: 20px;
  height: 20px;
}

::v-deep(.ball-skin__button) {
  width: 44px;
  height: 44px;
}
</style>

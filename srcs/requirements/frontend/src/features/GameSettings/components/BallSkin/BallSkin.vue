<template>
  <div class="ball-skin">
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
            <button
              class="ball-skin__list-element-btn"
              type="button"
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
            </button>
          </li>
        </ul>
      </div>
      <div class="ball-skin__views-section">
        <p class="ball-skin__list-title">
          {{ t('game_settings.tabs.ball_skin.skins_list.regular.title') }}
        </p>
        <ul class="ball-skin__list">
          <li
            v-for="(skin, index) in BALL_SKINS[BALL_REGULAR_TYPE_SKIN_KEY]"
            :key="index"
            :class="[
              'ball-skin__list-item',
              {
                'ball-skin__list-item_active':
                  activeSkinType === BALL_REGULAR_TYPE_SKIN_KEY && index === activeSkinIndex,
              },
            ]"
          >
            <button
              class="ball-skin__list-element-btn"
              type="button"
              @click="handleSkinChange(index, BALL_REGULAR_TYPE_SKIN_KEY)"
            >
              <span
                class="ball-skin__list-element ball-skin__list-element_ball"
                :style="{
                  backgroundColor: `var(${BALL_COLORS[activeColorIndex]})`,
                  backgroundImage: `url('${skin}')`,
                }"
              />
            </button>
          </li>
        </ul>
      </div>
      <div class="ball-skin__views-section">
        <p class="ball-skin__list-title">
          {{ t('game_settings.tabs.ball_skin.skins_list.special.title') }}
        </p>
        <ul class="ball-skin__list">
          <li
            v-for="(skin, index) in BALL_SKINS[BALL_SPECIAL_TYPE_SKIN_KEY]"
            :key="index"
            :class="[
              'ball-skin__list-item',
              {
                'ball-skin__list-item_active':
                  activeSkinType === BALL_SPECIAL_TYPE_SKIN_KEY && index === activeSkinIndex,
              },
            ]"
          >
            <button
              class="ball-skin__list-element-btn"
              type="button"
              @click="handleSkinChange(index, BALL_SPECIAL_TYPE_SKIN_KEY)"
            >
              <span
                class="ball-skin__list-element ball-skin__list-element_ball"
                :style="{
                  backgroundColor: `var(${BALL_COLORS[activeColorIndex]})`,
                  backgroundImage: `url('${skin}')`,
                }"
              />
            </button>
          </li>
        </ul>
      </div>
    </div>
    <BallPreview
      :color="`var(${BALL_COLORS[activeColorIndex]})`"
      :skin-type="activeSkinType"
      :skin="BALL_SKINS[activeSkinType][activeSkinIndex]"
    />
  </div>
</template>

<script setup>
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
  NEW_GAME_SETTINGS_FORM_PROVIDE_KEY,
} from 'entities/Game/config/constants.js';
import { computed, inject } from 'vue';
import { useI18n } from 'vue-i18n';

import { BallPreview } from './components';

const { t } = useI18n();

const { getValues, setValue } = inject(NEW_GAME_SETTINGS_FORM_PROVIDE_KEY);

const colorInputName = `${BALL_DESIGN_INPUT_NAME}.${BALL_COLOR_INPUT_NAME}`;
const skinTypeInputName = `${BALL_DESIGN_INPUT_NAME}.${BALL_SKIN_TYPE_INPUT_NAME}`;
const skinInputName = `${BALL_DESIGN_INPUT_NAME}.${BALL_SKIN_INPUT_NAME}`;

const activeColorIndex = computed(() =>
  BALL_COLORS.findIndex((color) => color === getValues(colorInputName))
);
const activeSkinType = computed(() => getValues(skinTypeInputName));
const activeSkinIndex = computed(() =>
  BALL_SKINS[activeSkinType.value].findIndex((skin) => skin === getValues(skinInputName))
);

const handleColorChange = (index) => {
  setValue(colorInputName, BALL_COLORS[index]);
};

const handleSkinChange = (index, type) => {
  setValue(skinTypeInputName, type);
  setValue(skinInputName, BALL_SKINS[type][index]);
};
</script>

<!--suppress CssUnusedSymbol -->
<style scoped>
.ball-skin {
  display: flex;
  flex-direction: row;
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

.ball-skin__list-item_active {
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

.ball-skin__list-element_ball {
  width: 50px;
  height: 50px;
  background-size: contain;
}

.ball-skin__list-element_disabled {
  filter: grayscale(0.8);
}

.ball-skin__list-element-btn {
  cursor: pointer;

  overflow: hidden;

  width: 100%;
  height: 100%;
  padding: var(--small-space);

  background-color: transparent;
  border: none;
  border-radius: 50%;
}

.ball-skin__list-element-btn:disabled {
  cursor: not-allowed;
}
</style>

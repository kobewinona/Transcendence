<!--suppress JSUnresolvedReference -->
<template>
  <div class="skins-list">
    <p class="skins-list__title">
      {{ t(`game_settings.tabs.ball_skin.skins_list.${skinType}.title`) }}
    </p>
    <ul class="skin-list__list">
      <li
        v-for="(skin, index) in BALL_SKINS[skinType]"
        :key="index"
        :class="[
          'skins-list__list-item',
          {
            'skins-list__list-item_active':
              activeSkinType === skinType && index === activeSkinIndex,
          },
        ]"
      >
        <MyButton
          class-name="skins-list__button"
          type="button"
          variant="ghost"
          @click="handleSkinChange(index, skinType)"
        >
          <span
            class="skins-list__skin"
            :style="{
              backgroundColor: `var(${BALL_COLORS[activeColorIndex]})`,
              backgroundImage: `url('${skin}')`,
            }"
          />
        </MyButton>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { MyButton } from 'components/index.js';
import {
  BALL_COLORS,
  BALL_SKINS,
  BALL_SPECIAL_SKINS_COLORS,
  BALL_SPECIAL_TYPE_SKIN_KEY,
} from 'entities/BallSkin/config/constants.js';
import {
  BALL_COLOR_INPUT_NAME,
  BALL_DESIGN_INPUT_NAME,
  BALL_SKIN_INPUT_NAME,
  BALL_SKIN_TYPE_INPUT_NAME,
} from 'entities/Game/config/constants.js';
import { useField } from 'vee-validate';
import { computed, toRef } from 'vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

defineProps({
  activeColorIndex: {
    type: Number,
    required: true,
  },
  skinType: {
    type: String,
    required: true,
  },
});

const { setValue: setColor } = useField(
  toRef(() => `${BALL_DESIGN_INPUT_NAME}.${BALL_COLOR_INPUT_NAME}`)
);
const { value: activeSkinType, setValue: setSkinType } = useField(
  toRef(() => `${BALL_DESIGN_INPUT_NAME}.${BALL_SKIN_TYPE_INPUT_NAME}`)
);
const { value: activeSkin, setValue: setSkin } = useField(
  toRef(() => `${BALL_DESIGN_INPUT_NAME}.${BALL_SKIN_INPUT_NAME}`)
);

const activeSkinIndex = computed(() =>
  BALL_SKINS[activeSkinType.value]?.findIndex((skin) => skin === activeSkin.value)
);

const handleSkinChange = (index, type) => {
  setSkinType(type);
  setSkin(BALL_SKINS[activeSkinType.value][index]);

  if (type === BALL_SPECIAL_TYPE_SKIN_KEY) {
    setColor(BALL_SPECIAL_SKINS_COLORS[index]);
  }
};
</script>

<style scoped>
.skins-list {
  display: flex;
  flex-direction: column;
  row-gap: var(--small-space);
  width: 100%;
}

.skins-list__title {
  margin: 0;
  font-weight: 600;
}

.skin-list__list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--smaller-space);

  margin: 0;
  padding: var(--smaller-space) 0;

  list-style: none;

  border-top: 1px solid var(--light-color-opacity-50);
  border-bottom: 1px solid var(--light-color-opacity-50);
}

.skins-list__list-item {
  box-sizing: border-box;
  width: max-content;
  height: max-content;

  font-size: 0;

  border: 2px solid var(--dark-color);
  border-radius: 12px;
}

.skins-list__skin {
  display: block;

  width: 50px;
  height: 50px;

  background-size: contain;
  border-radius: 50%;
}

::v-deep(.skins-list__list-item_active) {
  border: 2px solid var(--light-color);
  border-radius: 12px;
  transition: all 0.4s ease-in-out;
}

::v-deep(.skins-list__button) {
  width: 64px;
  height: 64px;
}
</style>

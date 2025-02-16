<template>
  <div class="controller">
    <div
      :class="[
        'controller__container',
        {
          controller__container_side_left: side === 'left',
          controller__container_side_center: side === undefined,
          controller__container_side_right: side === 'right',
        },
      ]"
      :style="{ borderColor: `var(${COLORS[controllerIndex]})` }"
    >
      <button
        v-show="side !== 'left'"
        class="controller__switch-sides-btn controller__switch-sides-btn_left"
        type="button"
        @click="handleSideChange(-1)"
      >
        <component
          :is="svgComponents['DownloadIcon']"
          v-if="isVueComponent(svgComponents['DownloadIcon'])"
          class="controller__arrow controller__arrow_left"
        />
      </button>
      <div class="controller__master">
        <button class="controller__controlled-by" type="button" @click="handleControlledByChange">
          <transition name="fade" mode="out-in">
            <component
              :is="controlledBy?.icon"
              v-if="controlledBy?.icon && isVueComponent(controlledBy?.icon)"
              class="controller__controlled-by-icon"
            />
          </transition>
        </button>
        <button type="button" class="controller__complementary-btn">
          <component
            :is="svgComponents['AddIcon']"
            v-if="isVueComponent(svgComponents['AddIcon'])"
            class="controller__complementary-btn-icon controller__complementary-btn-icon_remove"
            @click="removeController"
          />
        </button>
        <button type="button" class="controller__complementary-btn">
          <component
            :is="svgComponents['GameDevelopmentIcon']"
            v-if="isVueComponent(svgComponents['GameDevelopmentIcon'])"
            class="controller__complementary-btn-icon"
          />
        </button>
      </div>
      <button
        v-show="side !== 'right'"
        class="controller__switch-sides-btn controller__switch-sides-btn_right"
        type="button"
        @click="handleSideChange(1)"
      >
        <span class="controller__arrow-container">
          <component
            :is="svgComponents['DownloadIcon']"
            v-if="isVueComponent(svgComponents['DownloadIcon'])"
            class="controller__arrow controller__arrow_right"
          />
        </span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { CONTROL_KEYS, SIDE_OPTIONS } from 'entities/Controller/config/constants.js';
import { COLORS, CONTROLLED_BY_AI, CONTROLLED_BY_OPTIONS } from 'entities/Game/config/constants.js';
import {
  CONTROLLED_BY_INPUT_NAME,
  CONTROLLERS_INPUT_NAME,
  CONTROLS_INPUT_NAME,
  NAME_INPUT_NAME,
  NEW_GAME_SETTINGS_FORM_PROVIDE_KEY,
  SIDE_INPUT_NAME,
} from 'entities/Game/config/constants.js';
import { isVueComponent, svgComponents } from 'shared/lib';
import { computed, inject } from 'vue';

const { setValue, getValues } = inject(NEW_GAME_SETTINGS_FORM_PROVIDE_KEY);

const { controller, controllerIndex } = defineProps({
  controller: {
    type: Object,
    required: true,
  },
  controllerIndex: {
    type: Number,
    required: true,
  },
});

const emit = defineEmits(['on-remove']);

const sideInputName = `${CONTROLLERS_INPUT_NAME}[${controllerIndex}].${SIDE_INPUT_NAME}`;
const controlledByInputName = `${CONTROLLERS_INPUT_NAME}[${controllerIndex}].${CONTROLLED_BY_INPUT_NAME}`;

const side = computed(() => controller[SIDE_INPUT_NAME]);
const controlledBy = computed(() => controller[CONTROLLED_BY_INPUT_NAME]);

const reassignControlsAndNames = () => {
  let leftSideIndex = 0;
  let rightSideIndex = 0;
  let playersIndex = 1;
  let cpusIndex = 1;

  getValues(CONTROLLERS_INPUT_NAME)?.forEach((controller, index) => {
    const currentNameInputName = `${CONTROLLERS_INPUT_NAME}[${index}].${NAME_INPUT_NAME}`;

    if (controller[CONTROLLED_BY_INPUT_NAME].key === CONTROLLED_BY_AI.key) {
      setValue(currentNameInputName, `CPU ${cpusIndex++}`);
      return;
    } else {
      setValue(currentNameInputName, `PLAYER ${playersIndex++}`);
    }

    const currentControlsInputName = `${CONTROLLERS_INPUT_NAME}[${index}].${CONTROLS_INPUT_NAME}`;

    if (controller.side === 'left') {
      setValue(currentControlsInputName, CONTROL_KEYS.left[leftSideIndex++]);
    }

    if (controller.side === 'right') {
      setValue(currentControlsInputName, CONTROL_KEYS.right[rightSideIndex++]);
    }
  });
};

const handleSideChange = (indexIncrement) => {
  const currentSideIndex =
    SIDE_OPTIONS.findIndex((sideOption) => sideOption === side.value) + indexIncrement;
  let newSideIndex = !SIDE_OPTIONS[currentSideIndex]
    ? currentSideIndex + indexIncrement
    : currentSideIndex;

  if (currentSideIndex < 0) {
    newSideIndex = SIDE_OPTIONS.length - 1;
  } else if (currentSideIndex > SIDE_OPTIONS.length - 1) {
    newSideIndex = 0;
  }

  const newSide = SIDE_OPTIONS[newSideIndex];

  setValue(sideInputName, newSide);
  reassignControlsAndNames();
};

const handleControlledByChange = () => {
  const currentIndex = CONTROLLED_BY_OPTIONS.findIndex(
    (option) => option.value.key === controlledBy.value.key
  );
  const nextIndex = (currentIndex + 1) % CONTROLLED_BY_OPTIONS.length;

  setValue(controlledByInputName, CONTROLLED_BY_OPTIONS[nextIndex].value);
  reassignControlsAndNames();
};

const removeController = () => {
  emit('on-remove', controllerIndex);
};
</script>

<!--suppress CssUnusedSymbol -->
<style scoped>
.controller {
  position: relative;
  width: 100%;
  min-height: 66px;
}

.controller__container {
  position: absolute;
  top: 0;
  transform: translateX(-50%);

  overflow: hidden;
  display: flex;
  flex-direction: row;
  align-items: center;

  height: 66px;

  background-color: var(--dark-color);
  border-bottom: 6px solid;
  border-radius: 12px;
  box-shadow: 0 -1px 0 var(--light-color);

  transition: all 0.4s ease-in-out;
}

.controller__container_side_left {
  left: 0;
}

.controller__container_side_center {
  left: 50%;
}

.controller__container_side_right {
  left: 100%;
}

.controller__master {
  display: grid;
  grid-template-columns: max-content max-content;
  height: 100%;
}

.controller__controlled-by {
  cursor: pointer;

  position: relative;

  grid-row: span 2;

  height: 100%;
  padding: 0 var(--smaller-space);

  background-color: var(--dark-color);
  border: none;
}

.controller__controlled-by-icon {
  max-width: 50px;
  max-height: 50px;

  fill: var(--light-color);
  stroke: var(--light-color);

  transition: opacity 0.2s ease-in-out;
}

.controller__controlled-by-icon:hover {
  opacity: 0.5;
  transition: opacity 0.2s ease-in-out;
}

.controller__complementary-btn {
  cursor: pointer;

  display: flex;
  align-items: center;
  justify-content: center;

  width: 40px;
  height: 100%;

  background-color: var(--dark-color);
  border: none;

  transition: opacity 0.2s ease-in-out;
}

.controller__complementary-btn-icon {
  width: 30px;
  height: 30px;

  fill: var(--light-color);
  stroke: var(--light-color);

  transition: opacity 0.2s ease-in-out;
}

.controller__complementary-btn-icon:hover {
  opacity: 0.5;
  transition: opacity 0.2s ease-in-out;
}

.controller__complementary-btn-icon_remove {
  transform: rotate(45deg);
}

.controller__switch-sides-btn {
  cursor: pointer;

  width: 30px;
  height: 100%;

  background-color: var(--dark-color);
  border: none;

  transition: all 0.2s ease-in-out;
}

.controller__switch-sides-btn_left {
  border-radius: 12px 0 0 12px;
}

.controller__switch-sides-btn_right {
  border-radius: 0 12px 12px 0;
}

.controller__arrow {
  width: 30px;
  height: 30px;

  fill: var(--light-color);
  stroke: var(--light-color);

  transition: all 0.2s ease-in-out;
}

.controller__arrow:hover {
  opacity: 0.5;
  transition: all 0.2s ease-in-out;
}

.controller__arrow_left {
  transform: rotate(90deg);
}

.controller__arrow_right {
  transform: rotate(-90deg);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.1s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

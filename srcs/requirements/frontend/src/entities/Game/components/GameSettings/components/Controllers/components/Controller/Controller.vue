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
      :style="{ borderColor: `var(${COLORS[index]})` }"
    >
      <MyButton
        v-if="side !== 'left'"
        icon-class-name="controller__side-button-icon"
        type="button"
        variant="ghost"
        :icon="svgComponents['ArrowLeftIcon']"
        @click="handleSideChange(-1)"
      />
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
        <MyButton
          class-name="controller__complementary-button"
          icon-class-name="controller__complementary-button-icon"
          type="button"
          variant="ghost"
          :icon="svgComponents['DeclineIcon']"
          :disabled="disabled"
          @click="removeController"
        />
        <MyButton
          class-name="controller__complementary-button"
          icon-class-name="controller__complementary-button-icon"
          type="button"
          variant="ghost"
          disabled
          :icon="svgComponents['GameDevelopmentIcon']"
        />
      </div>
      <MyButton
        v-if="side !== 'right'"
        icon-class-name="controller__side-button-icon"
        type="button"
        variant="ghost"
        :icon="svgComponents['ArrowRightIcon']"
        @click="handleSideChange(1)"
      />
    </div>
  </div>
</template>

<script setup>
import { MyButton } from 'components/index.js';
import { SIDE_OPTIONS } from 'entities/Controller/config/constants.js';
import { COLORS, CONTROLLED_BY_OPTIONS } from 'entities/Game/config/constants.js';
import {
  CONTROLLED_BY_INPUT_NAME,
  CONTROLLERS_INPUT_NAME,
  SIDE_INPUT_NAME,
} from 'entities/Game/config/constants.js';
import { isVueComponent, svgComponents } from 'shared/lib';
import { useField } from 'vee-validate';
import { computed, toRef } from 'vue';

const { controller, index } = defineProps({
  controller: {
    type: Object,
    required: true,
  },
  index: {
    type: Number,
    required: true,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['on-remove']);

const { setValue: setSide } = useField(
  toRef(() => `${CONTROLLERS_INPUT_NAME}[${index}].${SIDE_INPUT_NAME}`)
);
const { setValue: setControlledBy } = useField(
  toRef(() => `${CONTROLLERS_INPUT_NAME}[${index}].${CONTROLLED_BY_INPUT_NAME}`)
);

const side = computed(() => controller.value[SIDE_INPUT_NAME]);
const controlledBy = computed(() => controller.value[CONTROLLED_BY_INPUT_NAME]);

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

  setSide(newSide);
};

const handleControlledByChange = () => {
  const currentIndex = CONTROLLED_BY_OPTIONS.findIndex(
    (option) => option.value.key === controlledBy.value.key
  );
  const nextIndex = (currentIndex + 1) % CONTROLLED_BY_OPTIONS.length;
  setControlledBy(CONTROLLED_BY_OPTIONS[nextIndex].value);
};

const removeController = () => {
  emit('on-remove', index);
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

::v-deep(.controller__complementary-button) {
  width: 100%;
  height: 30px;
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

::v-deep(.controller__side-button-icon) {
  width: 24px;
  height: 24px;
}

::v-deep(.controller__complementary-button-icon) {
  width: 24px;
  height: 24px;
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

<template>
  <div class="stage-select">
    <MyButton
      :class-name="{
        'stage-select__arrow-button': true,
        'stage-select__arrow-button_hidden': currentIndex === 0,
      }"
      :icon="svgComponents['ArrowUpIcon']"
      type="button"
      variant="ghost"
      @click="scroll(-1)"
    />

    <div :style="{ '--stage-cell-size': `${STAGE_CELL_SIZE}px` }" class="stage-select__window">
      <div class="stage-select__list-shadow stage-select__list-shadow_top" />
      <ul
        :style="{
          transform: `translateY(-${currentIndex * STAGE_CELL_SIZE}px)`,
        }"
        class="stage-select__list"
      >
        <li
          v-for="(stage, i) in bracketsStageNames"
          :key="stage"
          :class="{
            'stage-select__stage': true,
            'stage-select__stage_selected': i === currentIndex,
            'stage-select__stage_faded': i !== currentIndex,
          }"
        >
          {{ stage }}
        </li>
      </ul>
      <transition name="scale-fade">
        <div
          v-if="finalBracketIndex === currentIndex"
          :key="`start-btn-${currentIndex}`"
          class="stage-select__start-button-container"
        >
          <MyButton
            v-if="
              finalBracket.left?.[TOURNAMENT_NAMES.PLAYERS_NAME] &&
              finalBracket.right?.[TOURNAMENT_NAMES.PLAYERS_NAME]
            "
            :icon="svgComponents['GameConsoleIcon']"
            class-name="stage-select__start-button"
            color="secondary"
            @click="startGame"
          />
        </div>
      </transition>
      <div class="stage-select__list-shadow stage-select__list-shadow_bottom" />
    </div>

    <MyButton
      :class-name="{
        'stage-select__arrow-button': true,
        'stage-select__arrow-button_hidden': currentIndex === finalBracketIndex,
      }"
      :icon="svgComponents['ArrowDownIcon']"
      type="button"
      variant="ghost"
      @click="scroll(1)"
    />
  </div>
</template>

<script setup>
import { MyButton } from 'components';
import { TOURNAMENT_NAMES } from 'entities/Tournaments/config/constants.js';
import { svgComponents } from 'shared/lib/index.js';
import { ref } from 'vue';

import { STAGE_CELL_SIZE } from './config/constants.js';

const { finalBracket, bracketsStageNames } = defineProps({
  bracketsStageNames: {
    type: Object,
    default: () => {},
  },
  finalBracket: {
    type: Object,
    required: true,
  },
  finalBracketIndex: {
    type: Number,
    required: true,
  },
});

const emit = defineEmits(['select-stage', 'start-game']);

const currentIndex = ref(0);

const scroll = (dir) => {
  const max = bracketsStageNames.length - 1;
  const next = currentIndex.value + dir;

  if (next >= 0 && next <= max) {
    currentIndex.value = next;
  }

  emit('select-stage', bracketsStageNames[currentIndex.value], currentIndex.value);
};

const startGame = () => {
  emit('start-game', finalBracket);
};
</script>

<!--suppress CssUnusedSymbol -->
<style scoped>
.stage-select {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  box-sizing: content-box;
  width: 100%;
  max-width: 140px;
  height: 100%;
  margin: 0 auto;

  border-right: 1px solid var(--light-color-opacity-50);
  border-left: 1px solid var(--light-color-opacity-50);
}

::v-deep(.stage-select__arrow-button) {
  width: 100%;
}

.stage-select__window {
  --stage-cell-size: 28px;

  position: relative;

  overflow: hidden;
  display: flex;
  flex-direction: column;
  row-gap: var(--smaller-space);

  width: 140px;
  height: 160px;
  margin: var(--regular-space) 0;
}

.stage-select__list-shadow {
  pointer-events: none;

  position: absolute;
  z-index: 1;

  width: 100%;
  height: var(--stage-cell-size);
}

.stage-select__list-shadow_top {
  top: 0;
  background: linear-gradient(to bottom, var(--dark-color), transparent);
}

.stage-select__list-shadow_bottom {
  bottom: 0;
  background: linear-gradient(to top, var(--dark-color), transparent);
}

.stage-select__list {
  position: relative;
  top: calc(50% - (var(--stage-cell-size) / 2));

  display: flex;
  flex-direction: column;
  align-items: center;

  list-style: none;

  transition: transform 0.3s ease;
}

.stage-select__start-button-container {
  position: absolute;
  z-index: 2;
  bottom: 0;
  width: 100%;
}

::v-deep(.stage-select__start-button) {
  width: calc(100% - var(--big-space));
  margin: var(--smaller-space) auto;
}

::v-deep(.stage-select__arrow-button_hidden) {
  visibility: hidden;
}

.stage-select__stage {
  user-select: none;

  height: var(--stage-cell-size);

  font-size: 1rem;
  line-height: var(--stage-cell-size);
  color: var(--light-color);
  text-align: center;

  transition: all 0.2s ease-in-out;
}

.stage-select__stage_selected {
  padding: 2px var(--regular-space);

  font-size: 1.4rem;
  font-weight: 900;
  color: var(--dark-color);
  letter-spacing: 4px;

  background-color: var(--light-color);
  border-radius: 10px;

  transition: all 0.2s ease-in-out;
}

.stage-select__stage_faded {
  opacity: 0.4;
}

.scale-fade-enter-active {
  transition: all 0.4s ease-in-out;
}

.scale-fade-leave-active {
  transition: all 0.2s ease-in-out;
}

.scale-fade-enter-from,
.scale-fade-leave-to {
  transform: scale(0.4);
  opacity: 0;
}

.scale-fade-enter-to,
.scale-fade-leave-from {
  transform: scale(1);
  opacity: 1;
}
</style>

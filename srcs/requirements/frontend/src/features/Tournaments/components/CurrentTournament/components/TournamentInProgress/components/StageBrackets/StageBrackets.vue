<template>
  <TransitionGroup class="stage-brackets--group" name="stage-fade" tag="div">
    <div
      v-for="(bracketPairs, bracketIndex) in bracketsStack"
      :key="bracketIndex"
      :class="{
        'stage-brackets': true,
        'stage-brackets_blurred': bracketIndex !== bracketsStack.length - 1,
      }"
    >
      <div
        v-for="(pair, pairIndex) in bracketPairs"
        :key="`${pair.left?.key || 'null'}-${pair.right?.key || 'null'}`"
        :class="{
          'stage-brackets__pair': true,
          'stage-brackets__pair_last': finalBracketIndex === bracketIndex,
          'stage-brackets__pair_placement_left': pairIndex % 2 === 0,
          'stage-brackets__pair_placement_right': pairIndex % 2 !== 0,
        }"
      >
        <div
          :class="{
            'stage-brackets__pair-cards': true,
            'stage-brackets__pair-cards_final': finalBracketIndex === bracketIndex,
          }"
        >
          <PlayerCard
            :key="pair.left?.key || `left-${pairIndex}`"
            :placement="pairIndex % 2 === 0 ? 'left' : 'right'"
            :player="pair.left"
            :score="pair.score.left"
            :winner="pair.winner"
          />
          <PlayerCard
            :key="pair.right?.key || `right-${pairIndex}`"
            :placement="
              pairIndex % 2 !== 0 || finalBracketIndex === bracketIndex ? 'right' : 'left'
            "
            :player="pair.right"
            :score="pair.score.right"
            :winner="pair.winner"
          />
        </div>
        <MyButton
          v-if="
            !pair.winner &&
            bracketIndex !== finalBracketIndex &&
            pair.left?.[TOURNAMENT_NAMES.PLAYERS_NAME] &&
            pair.right?.[TOURNAMENT_NAMES.PLAYERS_NAME]
          "
          :icon="svgComponents['GameConsoleIcon']"
          class-name="stage-brackets__pair-button"
          color="secondary"
          type="button"
          @click="startGame(pair)"
        />
      </div>
    </div>
  </TransitionGroup>
</template>

<script setup>
import { MyButton } from 'components';
import { PlayerCard } from 'entities/Tournaments/components';
import { TOURNAMENT_NAMES } from 'entities/Tournaments/config/constants.js';
import { svgComponents } from 'shared/lib/index.js';

const { finalBracketIndex, bracketsStack } = defineProps({
  bracketsStack: {
    type: Array,
    required: true,
  },
  finalBracketIndex: {
    type: Number,
    required: true,
  },
});

const emit = defineEmits(['start-game']);

const startGame = (pair) => {
  emit('start-game', pair);
};
</script>

<!--suppress CssUnusedSymbol -->
<style scoped>
.stage-brackets--group {
  display: contents;
}

.stage-brackets {
  position: absolute;
  top: 0;
  left: 0;

  overflow: auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--big-space) 180px;
  align-items: center;

  width: 100%;
  min-width: 0;
  max-width: 100%;
  height: 100%;

  background-color: var(--dark-color-opacity-70);
  border-radius: 16px;
}

.stage-brackets__pair_last {
  display: contents !important;
}

.stage-brackets_blurred {
  filter: blur(1px);
}

.stage-brackets__pair {
  display: flex;
  column-gap: var(--small-space);
  align-items: center;
  justify-content: space-between;

  min-width: 0;
}

.stage-brackets__pair_placement_left {
  flex-direction: row;
}

.stage-brackets__pair_placement_right {
  flex-direction: row-reverse;
}

.stage-brackets__pair-cards {
  display: flex;
  flex-direction: column;
  row-gap: var(--small-space);
  align-items: center;
  justify-content: space-between;

  width: 100%;
  min-width: 0;
}

.stage-brackets__pair-cards_final {
  display: contents;
}

.stage-brackets__pair-button {
  width: 54px;
  height: 94px;
  padding: 0 var(--small-space);
}

.stage-fade-enter-active,
.stage-fade-leave-active {
  transition: all 0.4s ease;
}

.stage-fade-enter-from,
.stage-fade-leave-to {
  opacity: 0;
}

.stage-fade-enter-to,
.stage-fade-leave-from {
  opacity: 1;
}
</style>

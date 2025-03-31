<template>
  <span
    ref="playerCardRef"
    :class="{
      player: true,
      player_tbd: !player?.[TOURNAMENT_NAMES.PLAYERS_NAME],
      player_winner: showWinnerAnimation && winner && winner === player.name,
      player_placement_left: placement === 'left',
      player_placement_right: placement === 'right',
    }"
  >
    <span :class="{ player__name: true, player__name_direction_reverse: placement === 'right' }">
      <span
        :class="{
          'player__name-container': true,
          'player__name-container_reverse': placement === 'right',
        }"
      >
        <span class="player__name-text">{{
          player?.[TOURNAMENT_NAMES.PLAYERS_NAME] ||
          t('tournament.tabs.current.current_tournament.tbd')
        }}</span>
        <component
          :is="svgComponents['AiIcon']"
          v-if="
            player?.[CONTROLLED_BY_INPUT_NAME] === CONTROLLED_BY_AI.key &&
            isVueComponent(svgComponents['AiIcon'])
          "
          class="player__name-icon"
        />
      </span>
      <span class="player__score">{{ score }}</span>
    </span>
  </span>
</template>

<script setup>
import { CONTROLLED_BY_AI, CONTROLLED_BY_INPUT_NAME } from 'entities/Game/config/constants.js';
import { TOURNAMENT_NAMES } from 'entities/Tournaments/config/constants.js';
import { isVueComponent, svgComponents } from 'shared/lib';
import { nextTick, onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const { winner, player } = defineProps({
  player: {
    type: Object,
    required: true,
  },
  placement: {
    type: String,
    required: true,
    validator: (value) => value === 'left' || value === 'right',
  },
  score: {
    type: Object,
    required: true,
  },
  winner: {
    type: String,
    default: null,
  },
});

const showWinnerAnimation = ref(false);

onMounted(async () => {
  await nextTick();
  if (winner && winner === player?.name) {
    setTimeout(() => {
      showWinnerAnimation.value = true;
    }, 300);
  }
});
</script>

<style scoped>
.player {
  position: relative;
  z-index: 2;

  overflow: hidden;
  display: flex;
  align-items: center;

  box-sizing: border-box;
  width: 100%;
  padding: var(--bigger-space);

  background-color: var(--dark-color);
  border-radius: 16px;
}

.player::before {
  pointer-events: none;
  content: '';

  position: absolute;
  z-index: 2;
  inset: 0;

  border: 1px solid var(--light-color-opacity-50);
  border-radius: 16px;
}

.player::after {
  content: '';

  position: absolute;
  z-index: 1;
  inset: 0;
  transform-origin: left;
  transform: scaleX(0);

  background-color: var(--success-color);

  transition: transform 0.4s ease-out;
}

.player_winner::after {
  transform: scaleX(1);
  transition: transform 0.6s ease-out;
}

.player_tbd {
  color: var(--light-color-opacity-50);
}

.player_placement_left {
  justify-content: flex-start;
}

.player_placement_right {
  justify-content: flex-end;
}

.player__name {
  user-select: none;

  position: relative;
  z-index: 2;

  display: flex;
  flex-direction: row;
  column-gap: var(--smaller-space);
  justify-content: space-between;

  width: 100%;
  min-width: 0;
}

.player__name-container {
  display: flex;
  flex-direction: row;
  column-gap: var(--smaller-space);
  align-items: center;

  min-width: 0;
}

.player__name-container_reverse {
  flex-direction: row-reverse;
}

.player__name_direction_reverse {
  flex-direction: row-reverse;
}

.player__name-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.player__name-icon {
  width: 24px;
  height: 24px;
  fill: var(--light-color);
}

.player__score {
  font-family: Silkscreen, Overpass, system-ui, Avenir, Helvetica, Arial, sans-serif;
  font-size: 1.4rem;
}
</style>

<template>
  <div class="score" :style="{ ...styles }">
    <transition name="fade" mode="in-out">
      <div
        v-if="
          isActive &&
          isScoreVisible &&
          winner === 0 &&
          mode !== DEMO_GAME_MODE &&
          mode !== QUICK_START_GAME_MODE
        "
        class="score__inner-container"
      >
        <span class="score__advantage-badge">{{ isLeftAdvantage ? t('game.advantage') : '' }}</span>
        <div class="score__container">
          <div class="score__scoreboard">
            <span class="score__score">{{ leftScore }}</span>
            <div class="score__divider" />
            <span class="score__score">{{ rightScore }}</span>
          </div>
          <span v-if="isDeuce" class="score__deuce">{{ t('game.deuce') }}</span>
        </div>
        <span class="score__advantage-badge">{{
          isRightAdvantage ? t('game.advantage') : ''
        }}</span>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { useGameSocketInject } from 'entities/Game/composables';
import {
  DEMO_GAME_MODE,
  GAME_STATUS_IN_PROGRESS,
  QUICK_START_GAME_MODE,
} from 'entities/Game/config/constants.js';
import { computed, onUnmounted, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

const { mode } = defineProps({
  mode: {
    type: String,
    required: true,
  },
});

const gameSocket = useGameSocketInject();

const positionX = computed(() => gameSocket.ballPositionX.value || 50);
const positionY = computed(() => gameSocket.ballPositionY.value || 50);

const isActive = computed(() => gameSocket.status.value === GAME_STATUS_IN_PROGRESS);

const winner = computed(() => gameSocket.winner.value);
const leftScore = computed(() => gameSocket.leftScore.value);
const rightScore = computed(() => gameSocket.rightScore.value);
const isDeuce = computed(() => gameSocket.isDeuce.value);
const isLeftAdvantage = computed(() => gameSocket.isLeftAdvantage.value);
const isRightAdvantage = computed(() => gameSocket.isRightAdvantage.value);

const isScoreVisible = ref(true);
const showTimeoutId = ref(null);

const styles = computed(() => {
  const isPositionXClose = positionX.value > 20 && positionX.value < 80;
  const isPositionYClose = positionY.value < 20;

  return {
    opacity: `${isPositionXClose && isPositionYClose ? '0.1' : 1}`,
  };
});

watch([leftScore, rightScore], () => {
  isScoreVisible.value = false;

  showTimeoutId.value = setTimeout(() => {
    isScoreVisible.value = true;
  }, 1500);
});

onUnmounted(() => {
  clearTimeout(showTimeoutId.value);
});
</script>

<!--suppress CssUnusedSymbol -->
<style scoped>
.score {
  position: absolute;
  z-index: 2;
  top: 0;
  left: 0;

  width: 100%;
  margin-top: var(--regular-space);
  padding: var(--regular-space);

  opacity: 1;
  mix-blend-mode: difference;

  transition: all 0.4s ease-in-out;
}

.score__inner-container {
  display: flex;
  align-items: flex-start;
  justify-content: space-around;
  width: 100%;
}

.score__advantage-badge {
  min-width: 150px;
  text-align: center;
}

.score__container {
  display: flex;
  flex-direction: column;
  row-gap: var(--regular-space);
}

.score__scoreboard {
  display: flex;
  flex-direction: row;
  column-gap: var(--regular-space);
}

.score__score {
  min-width: 60px;
  font-size: 2rem;
  font-weight: 600;
  text-align: center;
}

.score__divider {
  transform: translateX(-50%);

  /* noinspection CssNonIntegerLengthInPixels */
  width: 2px;
  height: 50px;
  background-color: var(--light-color);
}

.score__deuce {
  padding: 2px;

  font-size: 0.7rem;
  color: var(--dark-color);
  text-align: center;

  background-color: var(--light-color);
  border-radius: 12px;
}

.fade-enter-active {
  transition: opacity 0.6s ease-in 1s;
}

.fade-leave-active {
  transition: opacity 0.4s ease-out;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

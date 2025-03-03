<template>
  <transition name="score-fade" mode="in-out">
    <div v-if="isScoreVisible || winner !== 0" class="background-score">
      <div class="background-score__score-container">
        <div
          v-if="scoreAnimated === 'left' || winner === 1"
          class="background-score__ball background-score__ball-1"
        />
        <div
          v-if="scoreAnimated === 'left' || winner === 1"
          class="background-score__ball background-score__ball-2"
        />
        <div
          v-if="!isRightAdvantage || winner !== 0"
          :class="['background-score__score', { flip: scoreAnimated === 'left' }]"
        >
          {{ isLeftAdvantage && winner === 0 ? 'A' : leftScore }}
        </div>
      </div>
      <div class="background-score__score-container">
        <div
          v-if="scoreAnimated === 'right' || winner === 2"
          class="background-score__ball background-score__ball-1"
        />
        <div
          v-if="scoreAnimated === 'right' || winner === 2"
          class="background-score__ball background-score__ball-2"
        />
        <div
          v-if="!isLeftAdvantage || winner !== 0"
          :class="['background-score__score', { flip: scoreAnimated === 'right' }]"
        >
          {{ isRightAdvantage && winner === 0 ? 'A' : rightScore }}
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { useGameSocketInject } from 'entities/Game/composables';
import { computed, onUnmounted, ref, watch } from 'vue';

const gameSocket = useGameSocketInject();

// TODO add advantage animation
const winner = computed(() => gameSocket.winner.value);
const leftScore = computed(() => gameSocket.leftScore.value);
const isLeftAdvantage = computed(() => gameSocket.isLeftAdvantage.value);
const rightScore = computed(() => gameSocket.rightScore.value);
const isRightAdvantage = computed(() => gameSocket.isRightAdvantage.value);

const scoreAnimated = ref(undefined);
const isScoreVisible = ref(false);
const showTimeoutId = ref(null);

const showScore = (newScoreAnimated) => {
  scoreAnimated.value = newScoreAnimated;
  isScoreVisible.value = true;

  showTimeoutId.value = setTimeout(() => {
    scoreAnimated.value = undefined;
    isScoreVisible.value = false;
  }, 1500);
};

watch(leftScore, () => {
  showScore('left');
});

watch(isLeftAdvantage, (newIsLeftAdvantage) => {
  if (newIsLeftAdvantage) {
    showScore('left');
  }
});

watch(rightScore, () => {
  showScore('right');
});

watch(isRightAdvantage, (newIsRightAdvantage) => {
  if (newIsRightAdvantage) {
    showScore('right');
  }
});

onUnmounted(() => {
  clearTimeout(showTimeoutId.value);
});
</script>

<!--suppress CssUnusedSymbol -->
<style scoped>
@keyframes fade-in {
  from {
    transform: translate(-50%, -50%) scale(1.3);
    opacity: 0;
  }

  to {
    transform: translate(-50%, -50%) scale(1);
    opacity: 1;
  }
}

@keyframes fade-out {
  from {
    transform: translate(-50%, -50%) scale(1);
    opacity: 1;
  }

  to {
    transform: translate(-50%, -50%) scale(0.9);
    opacity: 0;
  }
}

@keyframes ball-1 {
  0% {
    transform: translate(-70%, -80%) scale(0.2);
    opacity: 1;
    background-color: var(--light-color);
  }

  20% {
    transform: translate(-90%, -120%) scale(1);
    opacity: 0.4;
    background-color: var(--primary-color);
  }

  40% {
    transform: translate(-60%, -10%) scale(1.4);
  }

  60% {
    transform: translate(10%, -140%) scale(1);
    opacity: 1;
  }

  80% {
    transform: translate(0, 20%) scale(0.4);
    opacity: 0.7;
  }

  100% {
    transform: translate(-70%, -80%) scale(0.2);
    opacity: 1;
    background-color: var(--light-color);
  }
}

@keyframes ball-2 {
  0% {
    transform: translate(-40%, -100%) scale(0.2);
    opacity: 1;
    background-color: var(--dark-color);
  }

  20% {
    transform: translate(30%, 10%) scale(1.4);
    opacity: 0.5;
    background-color: var(--complementary-5-color);
  }

  40% {
    transform: translate(-50%, -130%) scale(1);
    opacity: 1;
  }

  60% {
    transform: translate(-80%, -80%) scale(0.4);
    opacity: 0.7;
  }

  80% {
    transform: translate(-60%, -10%) scale(1);
    opacity: 0.5;
  }

  100% {
    transform: translate(-40%, -100%) scale(0.2);
    opacity: 1;
    background-color: var(--dark-color);
  }
}

@keyframes flip {
  0% {
    transform: rotateX(0deg);
  }

  50% {
    transform: rotateX(90deg);
    opacity: 0.4;
  }

  100% {
    transform: rotateX(0deg);
    opacity: 1;
  }
}

.flip {
  animation: flip 0.5s 0.2s ease-in-out forwards;
}

.background-score {
  position: relative;
  z-index: 4;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);

  display: flex;
  align-items: center;
  justify-content: space-around;

  width: 25%;

  font-size: 2rem;
  font-weight: 700;

  opacity: 0.8;
  mix-blend-mode: difference;
}

.background-score__score-container {
  position: relative;
}

.background-score__ball {
  position: absolute;
  z-index: 900;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);

  width: 30px;
  height: 30px;

  border-radius: 50%;
  mix-blend-mode: difference;
}

.background-score__ball-1 {
  background-color: var(--primary-color);
  animation: ball-1 2.5s linear infinite;
}

.background-score__ball-2 {
  background-color: var(--complementary-5-color);
  animation: ball-2 2.5s ease-out infinite;
}

.score-fade-enter-active,
.score-fade-leave-active {
  transition:
    opacity 0.5s ease-in-out 0.3s,
    transform 0.5s ease-in-out 0.3s;
}

.score-fade-enter-from,
.score-fade-leave-to {
  transform: translate(-50%, -50%);
  opacity: 0;
}

.score-fade-enter-to,
.score-fade-leave-from {
  transform: translate(-50%, -50%);
  opacity: 1;
}
</style>

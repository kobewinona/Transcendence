<template>
  <transition mode="out-in" name="grow">
    <div
      v-if="winner !== undefined && winner !== 0"
      :class="[
        'winner',
        {
          winner_left: winner === 1,
          winner_right: winner === 2,
        },
      ]"
    >
      <span
        :class="[
          'winner__side',
          {
            winner__side_left: winner === 1,
            winner__side_right: winner === 2,
          },
        ]"
        >{{ winner === 1 ? t('game.left_side') : t('game.right_side') }}</span
      >
      <span class="winner__badge">{{ t('game.won') }}</span>
    </div>
  </transition>
  <div v-if="winner !== undefined && winner !== 0" class="winner__button">
    <MyButton color="secondary" type="button" @click="finish">{{ t('go_back') }}</MyButton>
  </div>
</template>

<script setup>
import { MyButton } from 'components';
import { useGameSocketInject } from 'entities/Game/composables/index.js';
import { menu } from 'store/menu.js';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

const gameSocket = useGameSocketInject();

defineProps({
  winner: {
    type: Number,
    required: true,
  },
});

const finish = () => {
  gameSocket.actions.stopGame();
  menu.open();
};
</script>

<style scoped>
.winner {
  position: absolute;
  z-index: 2;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) scale(1);

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-around;

  width: 150px;
  height: 150px;
  padding: var(--big-space);

  border-radius: 50%;
}

.winner_left {
  background: linear-gradient(to bottom, var(--light-color) 50%, var(--primary-color) 50%);
}

.winner_right {
  background: linear-gradient(to bottom, var(--dark-color) 50%, var(--primary-color) 50%);
}

.winner__side {
  text-align: center;
  white-space: nowrap;
}

.winner__side_left {
  color: var(--dark-color);
}

.winner__side_right {
  color: var(--light-color);
}

.winner__badge {
  text-transform: uppercase;
}

.winner__button {
  position: absolute;
  z-index: 900;
  top: 80%;
  left: 50%;
  transform: translate(-50%);
}
</style>

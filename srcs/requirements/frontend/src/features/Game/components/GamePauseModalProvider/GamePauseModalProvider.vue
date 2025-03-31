<template>
  <MyModal :is-open="modal.isOpen" layout="full" color="dark" @close="closeGamePauseModal">
    <div class="spinning">
      <div class="game-pause-modal">
        <p class="game-pause-modal__message">{{ t('pause') }}</p>
        <div class="game-pause-modal__controls">
          <MyButton
            class-name="game-pause-modal__button"
            type="button"
            color="secondary"
            @click="handleResume"
          >
            {{ t('resume') }}
          </MyButton>
          <MyButton
            class-name="game-pause-modal__button"
            type="button"
            color="light"
            @click="handleQuit"
          >
            {{ t('quit') }}
          </MyButton>
        </div>
      </div>
    </div>
  </MyModal>
</template>

<script setup>
import { MyButton, MyModal } from 'components';
import { useGameSocketInject } from 'entities/Game/composables/index.js';
import { menu } from 'store/menu.js';
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

const gameSocket = useGameSocketInject();

const modal = ref({ isOpen: false });

const closeGamePauseModal = () => {
  modal.value.isOpen = false;
};

const showGamePauseModal = () => {
  modal.value = { isOpen: true };
  gameSocket.actions.pauseGame();
};

const handleResume = () => {
  gameSocket.actions.resumeGame();
  closeGamePauseModal();
};

const handleQuit = () => {
  closeGamePauseModal();
  gameSocket.actions.stopGame();
  menu.open();
};

defineExpose({ showGamePauseModal });
</script>

<style scoped>
@keyframes rotate {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.game-pause-modal {
  position: relative;
  z-index: 2;

  overflow: hidden;
  display: flex;
  flex-direction: column;
  row-gap: var(--smaller-space);
  align-items: center;
  justify-content: center;

  width: 100%;
}

.spinning {
  position: relative;
  z-index: 1;

  overflow: hidden;

  width: 100%;
  max-width: 400px;
  padding: var(--big-space);

  background: var(--dark-color);
  border-radius: 16px;
}

.spinning::before {
  content: '';

  position: absolute;
  z-index: 0;
  top: -5%;
  left: -5%;

  width: 110%;
  height: 110%;

  background: conic-gradient(var(--light-color), var(--dark-color), var(--light-color));
  border-radius: 20px;

  animation: rotate 4s linear infinite;
}

.spinning::after {
  content: '';

  position: absolute;
  z-index: 1;
  inset: 2px;

  background: var(--dark-color);
  border-radius: 14px;
}

.game-pause-modal__message {
  font-size: 1.8rem;
  font-weight: 700;
}

.game-pause-modal__controls {
  display: flex;
  flex-direction: row;
  column-gap: 10px;
  justify-content: center;

  width: 100%;
}

::v-deep(.game-pause-modal__button) {
  min-width: 140px;
}
</style>

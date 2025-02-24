<template>
  <main class="main">
    <section class="container">
      <transition name="transit" appear>
        <GameLoader v-show="isLoadingGame" />
      </transition>
      <Menu
        :is-open="isMenuOpen"
        @on-menu-option-select="handleMenuOptionSelect"
        @on-game-settings-change="startNewGame"
      />
      <Game :settings="gameSettings" @on-close-menu="closeMenu" />
    </section>
  </main>
</template>

<script setup>
import { GameLoader } from 'components';
import {
  CONTROLLERS_INPUT_NAME,
  GAME_STATUS_IN_PROGRESS,
  QUICK_START_DEFAULT_GAME_SETTINGS,
} from 'entities/Game/config/constants.js';
import { Game, Menu } from 'features';
import { useGameSocketInject } from 'features/Game/composables/index.js';
import { MENU_ITEMS_KEYS } from 'features/Menu/config/constants.js';
import { onMounted, onUnmounted, ref, watch } from 'vue';

const gameSocket = useGameSocketInject();

const isMenuOpen = ref(true);
const gameSettings = ref(undefined);
const isLoadingGame = ref(false);

const switchToGameTimeoutId = ref(null);
const closeMenuTimeoutId = ref(null);

const closeMenu = (delay) => {
  const close = () => {
    isMenuOpen.value = false;
  };

  if (delay && typeof delay === 'number') {
    closeMenuTimeoutId.value = setTimeout(close, delay);
  } else {
    close();
  }
};

const startNewGame = (newGameSettings) => {
  isLoadingGame.value = true;
  gameSettings.value = newGameSettings;

  if (!newGameSettings) {
    gameSocket.actions.startGame(QUICK_START_DEFAULT_GAME_SETTINGS);
  } else {
    gameSocket.actions.startGame({
      ...newGameSettings,
      [CONTROLLERS_INPUT_NAME]: [
        ...newGameSettings[CONTROLLERS_INPUT_NAME].map(({ side, name }) => ({ side, name })),
      ],
    });
  }
};

// Get rid of timeout
const handleMenuOptionSelect = (optionKey) => {
  if (optionKey === MENU_ITEMS_KEYS.QUICK_START) {
    startNewGame(QUICK_START_DEFAULT_GAME_SETTINGS);
  }
};

const handleKeyDown = (event) => {
  if (event.code === 'Escape') {
    isMenuOpen.value = !isMenuOpen.value;

    // TODO handle escape during game other than quick start
    gameSettings.value = undefined;
    gameSocket.actions.stopGame();

    // if (!gameSettings.value) return;
    //
    // if (gameSettings.value.mode === QUICK_START_GAME_MODE) {
    //   gameSettings.value = undefined;
    //   gameSocket.actions.stopGame();
    // }
  }
};

const switchToGame = (delay = 0) => {
  closeMenu();

  const doSwitch = () => {
    isLoadingGame.value = false;
  };

  if (delay && typeof delay === 'number') {
    switchToGameTimeoutId.value = setTimeout(doSwitch, delay);
  } else {
    doSwitch();
  }
};

watch(gameSocket.status, (newStatus) => {
  if (!gameSettings.value) return;

  if (newStatus === GAME_STATUS_IN_PROGRESS) {
    switchToGame(600);
  }
});

onMounted(() => {
  // startNewGame();
  window.addEventListener('keydown', handleKeyDown);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown);
  clearTimeout(switchToGameTimeoutId.value);
  clearTimeout(closeMenuTimeoutId.value);
});
</script>

<!--suppress CssUnusedSymbol -->
<style scoped>
.main {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 100%;
  height: 100%;

  background: linear-gradient(90deg, var(--dark-color) 50%, var(--light-color) 50%);
}

.container {
  position: relative;
  aspect-ratio: 4 / 3;
  height: 90%;
  border-radius: 12px;
}

.transit-enter-active,
.transit-leave-active {
  transition:
    transform 0.2s ease-in-out,
    opacity 0.2s ease-in-out;
}

.transit-enter-from {
  transform: scale(0.7);
  opacity: 0;
}

.transit-leave-to {
  transform: scale(1.4);
  opacity: 0;
}
</style>

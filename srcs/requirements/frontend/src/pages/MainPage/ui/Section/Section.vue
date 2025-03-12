<template>
  <transition name="transit" appear>
    <GameLoader v-show="isLoadingGame" :icon="MENU_ICONS[selectedMenuOptionKey]" />
  </transition>
  <Menu
    :is-open="isMenuOpen"
    @on-menu-option-select="handleMenuOptionSelect"
    @on-game-settings-change="startNewGame"
  />
  <Game :settings="gameSettings" />
</template>

<script setup>
import { GameLoader } from 'components/index.js';
import { useGameSocketInject } from 'entities/Game/composables/index.js';
import {
  CONTROLLERS_INPUT_NAME,
  GAME_STATUS_IN_PROGRESS,
  QUICK_START_DEFAULT_GAME_SETTINGS,
} from 'entities/Game/config/constants.js';
import { Game, Menu } from 'features/index.js';
import { MENU_ICONS, MENU_ITEMS_KEYS } from 'features/Menu/config/constants.js';
import { onMounted, onUnmounted, ref, watch } from 'vue';

const gameSocket = useGameSocketInject();

const isMenuOpen = ref(true);
const gameSettings = ref(undefined);
const isLoadingGame = ref(false);

const switchToGameTimeoutId = ref(null);
const closeMenuTimeoutId = ref(null);

const selectedMenuOptionKey = ref(null);

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
  let filteredGameSettings = newGameSettings;

  // Filter controllers with no selected side
  if (newGameSettings) {
    filteredGameSettings = {
      ...newGameSettings,
      [CONTROLLERS_INPUT_NAME]: newGameSettings[CONTROLLERS_INPUT_NAME].filter(
        (controller) => controller.side !== undefined
      ),
    };
  }

  gameSettings.value = filteredGameSettings;

  if (!filteredGameSettings) {
    gameSocket.actions.startGame(QUICK_START_DEFAULT_GAME_SETTINGS);
  } else {
    gameSocket.actions.startGame({
      ...filteredGameSettings,
      [CONTROLLERS_INPUT_NAME]: [
        ...filteredGameSettings[CONTROLLERS_INPUT_NAME].map(({ side, name }) => ({ side, name })),
      ],
    });
  }
};

// Get rid of timeout
const handleMenuOptionSelect = (optionKey) => {
  selectedMenuOptionKey.value = optionKey;

  if (optionKey === MENU_ITEMS_KEYS.QUICK_START) {
    startNewGame(QUICK_START_DEFAULT_GAME_SETTINGS);
  }
};

const handleKeyDown = (event) => {
  if (event.code === 'Escape') {
    isMenuOpen.value = !isMenuOpen.value;

    // TODO handle escape during game other than quick start
    selectedMenuOptionKey.value = null;
    isLoadingGame.value = false;
    gameSettings.value = undefined;
    gameSocket.actions.stopGame();
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

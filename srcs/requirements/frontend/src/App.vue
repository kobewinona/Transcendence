<template>
  <div class="no-cursor-overlay" :class="{ 'no-cursor-overlay_active': isCursorDisabled }" />
  <div class="grain-overlay" />
  <main class="main">
    <section class="container">
      <Menu
        :is-open="isMenuOpen"
        @on-close="closeMenu"
        @on-menu-option-select="handleMenuOptionSelect"
      />
      <Game :settings="gameSettings" @on-close-menu="closeMenu" />
    </section>
  </main>
</template>

<script setup>
import { Game, Menu } from 'features';
import { provideGameSocket } from 'features/Game/composables/useGameSocket.js';
import {
  QUICK_START_GAME_MODE,
  QUICK_START_GAME_SETTINGS,
} from 'features/Game/config/constants.js';
import { MENU_ITEMS_KEYS } from 'features/Menu/config/constants.js';
import { onMounted, onUnmounted, ref } from 'vue';

import { i18n } from './main.js';
import { provideLang } from './shared/composables';

provideLang(i18n);
provideGameSocket(import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws/pong/');

const isCursorDisabled = ref(false);
const isMenuOpen = ref(true);
const gameSettings = ref(undefined);

let lastMousePosition = { x: 0, y: 0 };
let isTrackingMouse = false;

const closeMenuTimeoutId = ref(null);

const disableCursor = () => {
  isCursorDisabled.value = true;
};

const enableCursor = () => {
  isCursorDisabled.value = false;
};

const enableCursorOnMouseTravel = (event) => {
  if (!lastMousePosition.x) {
    lastMousePosition.x = event.clientX;
    return;
  }

  if (!lastMousePosition.y) {
    lastMousePosition.y = event.clientY;
    return;
  }

  const distanceThreshold = 10 * 10;
  const dx = event.clientX - lastMousePosition.x;
  const dy = event.clientY - lastMousePosition.y;
  const squaredDistance = dx * dx + dy * dy;

  if (squaredDistance >= distanceThreshold) {
    enableCursor();
    window.removeEventListener('mousemove', enableCursorOnMouseTravel);
    isTrackingMouse = false;
  }
};

const startMouseTracking = (event) => {
  if (!isTrackingMouse) {
    lastMousePosition = { x: event.clientX, y: event.clientY };
    window.addEventListener('mousemove', enableCursorOnMouseTravel);
    isTrackingMouse = true;
  }
};

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

// Get rid of timeout
const handleMenuOptionSelect = (optionKey) => {
  if (optionKey === MENU_ITEMS_KEYS.QUICK_START) {
    gameSettings.value = QUICK_START_GAME_SETTINGS;
    closeMenu(500);
  }
};

const handleKeyDown = (event) => {
  startMouseTracking(event);
  disableCursor();

  if (event.code === 'Escape') {
    if (gameSettings.value.mode === QUICK_START_GAME_MODE) {
      gameSettings.value = undefined;
    }

    isMenuOpen.value = !isMenuOpen.value;
  }
};

onMounted(() => {
  window.addEventListener('keydown', handleKeyDown);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown);
  clearTimeout(closeMenuTimeoutId);
});
</script>

<style scoped>
@keyframes noise {
  0% {
    transform: translate3d(0, 9rem, 0);
  }

  10% {
    transform: translate3d(-1rem, -4rem, 0);
  }

  20% {
    transform: translate3d(-8rem, 2rem, 0);
  }

  30% {
    transform: translate3d(9rem, -9rem, 0);
  }

  40% {
    transform: translate3d(-2rem, 7rem, 0);
  }

  50% {
    transform: translate3d(-9rem, -4rem, 0);
  }

  60% {
    transform: translate3d(2rem, 6rem, 0);
  }

  70% {
    transform: translate3d(7rem, -8rem, 0);
  }

  80% {
    transform: translate3d(-9rem, 1rem, 0);
  }

  90% {
    transform: translate3d(6rem, -5rem, 0);
  }

  100% {
    transform: translate3d(-7rem, 0, 0);
  }
}

.no-cursor-overlay {
  pointer-events: none;
  cursor: none;

  position: absolute;
  z-index: 900;

  display: none;

  width: 100%;
  height: 100%;
}

.no-cursor-overlay_active {
  pointer-events: all;
}

.grain-overlay {
  pointer-events: none;

  position: fixed;
  z-index: 900;
  top: 0;
  left: 0;
  transform: translateZ(0);

  width: 100%;
  height: 100%;
}

.grain-overlay::before {
  pointer-events: none;
  content: '';

  position: fixed;
  z-index: 9999;
  top: -10rem;
  left: -10rem;

  width: calc(100% + 20rem);
  height: calc(100% + 20rem);

  opacity: 0.15;
  background-image: url('https://upload.wikimedia.org/wikipedia/commons/5/5c/Image_gaussian_noise_example.png');

  animation: noise 1s steps(2) infinite;
}

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
</style>

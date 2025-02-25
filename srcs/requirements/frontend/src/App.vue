<template>
  <ConfigProvider :theme="ANTD_THEME_CONFIG">
    <!--  <div class="no-cursor-overlay" :class="{ 'no-cursor-overlay_active': isCursorDisabled }" />-->
    <!-- <div class="grain-overlay" /> -->
    <!-- <LoginPage /> -->
    <main class="layout">
      <router-view />
  </main>
  </ConfigProvider>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { provideGameSocket } from 'features/Game/composables/useGameSocket.js';
import { MainPage } from 'pages';
import { onMounted, onUnmounted, ref } from 'vue';

import { ANTD_THEME_CONFIG } from './config/constants.js';
import { i18n } from './main.js';
import { provideLang } from './shared/composables';

const router = useRouter();

provideLang(i18n);
provideGameSocket(import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws/pong/');

const isCursorDisabled = ref(false);

let lastMousePosition = { x: 0, y: 0 };
let isTrackingMouse = false;

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

const handleKeyDown = (event) => {
  startMouseTracking(event);
  disableCursor();
};

onMounted(() => {
  window.addEventListener('keydown', handleKeyDown);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown);
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

  display: block;

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

  opacity: 0.1;
  background-image: url('https://upload.wikimedia.org/wikipedia/commons/5/5c/Image_gaussian_noise_example.png');

  animation: noise 1s steps(2) infinite;
}
</style>

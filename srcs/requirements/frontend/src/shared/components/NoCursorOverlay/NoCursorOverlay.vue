<template>
  <div class="no-cursor-overlay" :class="{ 'no-cursor-overlay_active': isCursorDisabled }" />
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue';

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
</style>

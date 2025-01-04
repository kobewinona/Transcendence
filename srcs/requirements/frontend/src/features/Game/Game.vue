<template>
  <div class="layout">
    <div ref="containerRef" class="container">
      <Ball :width="ballWidth" :height="ballHeight" />
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUpdated, onUnmounted } from 'vue';
import { Ball } from './components';
import { BALL_HEIGHT, BALL_WIDTH } from './components/Ball/config/constants.js';

const containerRef = ref(null);
const containerWidth = ref(0);
const containerHeight = ref(0);
const ballWidth = ref(0);
const ballHeight = ref(0);

const updateContainerDimensions = () => {
  // noinspection JSUnresolvedReference
  if (containerRef?.value) {
    containerWidth.value = containerRef.value.offsetWidth;
    containerHeight.value = containerRef.value.offsetHeight;
  }
};

const calculateBallSize = () => {
  if (containerWidth.value && containerHeight.value) {
    ballWidth.value = parseFloat(((BALL_WIDTH / containerWidth.value) * 100).toFixed(2));
    ballHeight.value = parseFloat(((BALL_HEIGHT / containerHeight.value) * 100).toFixed(2));
  }
};

watch([containerWidth, containerHeight], calculateBallSize, { immediate: true });

onMounted(() => {
  updateContainerDimensions();
  window.addEventListener('resize', updateContainerDimensions);
});

onUpdated(() => {
  updateContainerDimensions();
});

onUnmounted(() => {
  window.removeEventListener('resize', updateContainerDimensions);
});
</script>

<style scoped>
.layout {
  width: 100%;
  max-width: 800px;
  height: 100%;
  max-height: 400px;
  border: 2px solid white;
  border-radius: 16px;
  overflow: hidden;
  box-sizing: border-box;
}
.container {
  width: 800px;
  height: 400px;
  padding: 20px;
  position: relative;
}
</style>

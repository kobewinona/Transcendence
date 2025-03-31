<template>
  <div v-if="Boolean(icon)" class="layout">
    <div class="spinning-bg"></div>
    <div class="spinning-inner"></div>
    <div class="spinning">
      <div class="carousel">
        <component :is="icon" v-if="isVueComponent(icon)" class="quick-start-icon" />
      </div>
      <div class="shapes-container">
        <FlyingRectangle class-name="flying-rectangle" />
        <Shapeshifter class-name="shapeshifter" />
        <LineShapeshifter class-name="line-shapeshifter" />
        <RotatingCircle class-name="rotating-circle" />
      </div>
    </div>
  </div>
</template>

<script setup>
// noinspection JSFileReferences
import { AnimatedShapes } from 'shared/components';
import { isVueComponent } from 'shared/lib';

const { FlyingRectangle, Shapeshifter, LineShapeshifter, RotatingCircle } = AnimatedShapes;

const { icon } = defineProps({
  icon: {
    type: Object,
    default: null,
  },
});
</script>

<!--suppress CssUnusedSymbol -->
<style scoped>
@keyframes wing {
  0% {
    transform: rotate(0deg) translateX(0);
  }

  30% {
    transform: rotate(-15deg) translateX(15%);
  }

  70% {
    transform: rotate(15deg) translateX(-15%);
  }

  100% {
    transform: rotate(0deg) translateX(0);
  }
}

@keyframes fade-in-out {
  0%,
  100% {
    opacity: 0.7;
  }

  50% {
    opacity: 1;
  }
}

@keyframes rotate {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.layout {
  position: absolute;

  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;

  width: 100%;
  height: 100%;

  opacity: 1;
  background-color: var(--dark-color);
  border-radius: 12px;
}

.spinning-bg {
  position: absolute;
  z-index: 0;
  top: -50%;
  left: -50%;

  width: 200%;
  height: 200%;

  background-color: var(--primary-color);
  background-image: linear-gradient(var(--secondary-color), var(--secondary-color));
  background-repeat: no-repeat;
  background-position:
    0 0,
    100% 0,
    100% 100%,
    0 100%;
  background-size:
    50% 50%,
    50% 50%;

  animation: rotate 2s linear infinite;
}

.spinning-inner {
  position: absolute;
  z-index: 1;
  top: 2px;
  left: 2px;

  width: calc(100% - 4px);
  height: calc(100% - 4px);

  background: var(--dark-color);
  border-radius: 10px;
}

.spinning {
  position: absolute;
  z-index: 2;
  top: 0;
  left: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  width: 100%;
  height: 100%;
  padding: 2rem;

  font-family: sans-serif;
  font-weight: 700;

  background: transparent;
  border-radius: 10px;
}

.carousel {
  aspect-ratio: 1 / 1;
  width: 40%;
  animation: wing 4s cubic-bezier(0.4, 0, 0.2, 1) infinite;
}

.quick-start-icon {
  width: 100%;
  height: 100%;

  fill: var(--light-color);
  stroke: var(--light-color);

  animation: fade-in-out 1.5s cubic-bezier(0.4, 0, 0.2, 1) infinite;
}

.shapes-container {
  position: absolute;

  display: flex;
  align-items: center;
  justify-content: center;

  width: 100%;
  height: 100%;
}

.flying-rectangle {
  z-index: 401;
}

.shapeshifter {
  position: absolute;
  z-index: 414;
  top: 20%;
  right: 25%;
}

.line-shapeshifter {
  position: absolute;
  z-index: 401;
  top: 40%;
  left: 30%;
}

.rotating-circle {
  position: absolute;
  z-index: 400;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);

  width: 400px !important;
  height: 400px !important;
}
</style>

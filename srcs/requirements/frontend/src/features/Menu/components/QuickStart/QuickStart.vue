<template>
  <div class="layout">
    <!-- Carousel animation for the SVG -->
    <div class="carousel">
      <component
        :is="svgComponents['GameConsoleIcon']"
        v-if="isVueComponent(svgComponents['GameConsoleIcon'])"
        class="quick-start-icon"
      />
    </div>

    <!-- Geometrical shapes rotating and scaling -->
    <div class="shapes-container">
      <FlyingRectangle class-name="flying-rectangle" />
      <Shapeshifter class-name="shapeshifter" />
      <LineShapeshifter class-name="line-shapeshifter" />
      <RotatingCircle class-name="rotating-circle" />
    </div>
  </div>
</template>

<script setup>
// noinspection JSFileReferences
import { AnimatedShapes } from 'shared/components';
import { svgComponents } from 'shared/lib';
import { isVueComponent } from 'shared/lib';

const { FlyingRectangle, Shapeshifter, LineShapeshifter, RotatingCircle } = AnimatedShapes;
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
    opacity: 0.5;
  }

  50% {
    opacity: 1;
  }
}

.layout {
  position: relative;

  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;

  width: 100%;
  height: 100%;
}

.carousel {
  position: relative;
  z-index: 404;

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

<template>
  <div class="grain-overlay" />
</template>

<script setup></script>

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

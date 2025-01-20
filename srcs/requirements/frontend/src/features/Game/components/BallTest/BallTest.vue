<script setup>
import ballSkin from 'assets/ballSkins/skin1.png';
import { computed, ref } from 'vue';

const curveIncrementValue = 0.1;
const velocity = ref(0);
const curve = ref(0);
const rotateDuration = ref(1);

const mapVelocityToDegrees = (velocityValue) => {
  const minVelocity = 0.5;
  const maxVelocity = 2;
  const minDegrees = 0;
  const maxDegrees = 360;

  return (
    minDegrees +
    ((velocityValue - minVelocity) / (maxVelocity - minVelocity)) * (maxDegrees - minDegrees)
  );
};

const rotateDirection = computed(() => {
  return mapVelocityToDegrees(Math.abs(velocity.value)); // Use the absolute value for rotation
});

const changeVelocity = (newVelocity) => {
  velocity.value = newVelocity;
};

const incrementCurve = () => {
  curve.value = parseFloat((curve.value + curveIncrementValue).toFixed(2));
  rotateDuration.value = Math.abs(1 - curve.value);
};

const resetCurve = () => {
  curve.value = 0;
  rotateDuration.value = 1;
};

const decrementCurve = () => {
  const newCurve = parseFloat((curve.value - curveIncrementValue).toFixed(2));
  curve.value = newCurve >= 0 ? newCurve : 0;
  rotateDuration.value = Math.abs(1 - curve.value);
};
</script>

<template>
  <div class="container">
    <div class="params">
      <h1>Params</h1>
      <p>Velocity: {{ velocity }}</p>
      <p>Curve: {{ curve }}</p>
    </div>
    <div class="controls__containers">
      <div class="controls">
        <button @click="() => changeVelocity(-1)">velocity -</button>
        <button @click="() => changeVelocity(0)">velocity 0</button>
        <button @click="() => changeVelocity(1)">velocity +</button>
      </div>
      <div class="controls">
        <button @click="() => decrementCurve()">curve -</button>
        <button @click="() => resetCurve()">curve 0</button>
        <button @click="() => incrementCurve()">curve +</button>
      </div>
    </div>
    <div
      class="ball"
      :style="{
        '--rotate-direction': `${rotateDirection}deg`,
      }"
    >
      <div
        class="ball__core"
        :style="{
          backgroundImage: `url('${ballSkin}')`,
          '--rotate-duration': `${rotateDuration}s`,
        }"
        :class="{ spinning: velocity !== 0 }"
      />
    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  row-gap: 50px;
  align-items: center;
  justify-content: center;

  width: 100%;
  height: 100vh;
}

.params {
  padding: 20px;
  background-color: var(--dark-color);
  border-radius: 10px;
}

.controls {
  display: flex;
  flex-direction: row;
  column-gap: 20px;
}

.controls__containers {
  display: flex;
  flex-direction: column;
  row-gap: 20px;
}

.ball {
  position: relative;
  transform: rotate(var(--rotate-direction));

  overflow: hidden;

  width: 150px;
  height: 150px;

  background-color: var(--primary-color);
  border-radius: 50%;
}

.ball__core {
  transform-origin: center;

  width: 100%;
  height: 100%;

  background-repeat: repeat-x;
  background-position: 0 50%;
  background-size: 200% 200%;

  animation: spin var(--rotate-duration) linear infinite;
}

@keyframes spin {
  0% {
    transform: scale(1.4);
    background-position: 0 50%;
  }

  50% {
    transform: scale(1);
  }

  100% {
    transform: scale(1.4);
    background-position: 200% 50%;
  }
}
</style>

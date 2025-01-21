<template>
  <slot />
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue';

import { useGameSocketInject } from '../../composables';
import { PADDLE_DEFAULT_DEACCELERATION, PADDLE_DEFAULT_WIDTH } from '../Paddle/config/constants.js';
import {
  EARLY_STOP_BUFFER,
  MAX_ERROR_FACTOR,
  MOVEMENT_WINDOW,
  PREDICTION_INTERVAL,
} from './config/constants.js';

const { side } = defineProps({
  side: {
    type: String,
    required: true,
    validator: (value) => ['left', 'right'].includes(value),
  },
});

const gameSocket = useGameSocketInject();

const ballPositionX = computed(() => gameSocket.ballPositionX.value);
const ballPositionY = computed(() => gameSocket.ballPositionY.value);
const ballVelocityX = computed(() => gameSocket.ballVelocityX.value);
const ballVelocityY = computed(() => gameSocket.ballVelocityY.value);
const paddleY = computed(() =>
  side === 'left' ? gameSocket.leftPaddleY.value : gameSocket.rightPaddleY.value
);
const paddleSpeed = computed(() =>
  side === 'left' ? gameSocket.leftPaddleSpeed.value : gameSocket.rightPaddleSpeed.value
);

let aiPredictionIntervalId = null;
let aiMovementFrameId = null;
const predictedY = ref(50);
const lastDirection = ref(0);

const sendDirection = (direction) => {
  gameSocket.actions.updatePaddlePosition({ side, direction });
};

const predictBallYAtPaddle = () => {
  const paddleX = side === 'left' ? 0 : 100;
  const ballDirectionX = ballVelocityX.value > 0 ? 'right' : 'left';

  if (
    (side === 'left' && ballDirectionX !== 'left') ||
    (side === 'right' && ballDirectionX !== 'right')
  ) {
    return;
  }

  const distanceToPaddleX = Math.abs(ballPositionX.value - paddleX);
  const timeToPaddle = distanceToPaddleX / Math.abs(ballVelocityX.value);
  let predicted = ballPositionY.value + ballVelocityY.value * timeToPaddle;

  // Handle bouncing off top and bottom boundaries
  while (predicted < 0 || predicted > 100) {
    if (predicted < 0) predicted = -predicted;
    if (predicted > 100) predicted = 200 - predicted;
  }

  // Adjust prediction with paddle width
  predicted = Math.min(
    100 - PADDLE_DEFAULT_WIDTH / 2,
    Math.max(PADDLE_DEFAULT_WIDTH / 2, Math.round(predicted))
  );

  // Add prediction error
  const errorFactor = Math.min(1, distanceToPaddleX / 100);
  const error = (Math.random() * 2 - 1) * MAX_ERROR_FACTOR * errorFactor;
  predicted += error;

  predictedY.value = predicted;
};

// Return paddle closer to center
watch(
  () => ballVelocityX.value,
  () => {
    const ballDirectionX = ballVelocityX.value > 0 ? 'right' : 'left';

    if (
      (side === 'left' && ballDirectionX !== 'left') ||
      (side === 'right' && ballDirectionX !== 'right')
    ) {
      const randomY =
        paddleY.value > 50
          ? (Math.random() * (65 - 50) + 50).toFixed(2)
          : (Math.random() * (50 - 35) + 35).toFixed(2);
      predictedY.value = parseFloat(randomY);
    }
  }
);

// Move paddle to target position
watch(
  () => [predictedY.value, paddleY.value],
  ([, paddleY]) => {
    // Calculate stopping distance based on current speed
    const stoppingDistance = Math.pow(paddleSpeed.value, 2) / (2 * PADDLE_DEFAULT_DEACCELERATION);

    // Adjust bounds with stopping distance
    const lowerBound = predictedY.value - MOVEMENT_WINDOW - stoppingDistance - EARLY_STOP_BUFFER;
    const upperBound = predictedY.value + MOVEMENT_WINDOW + stoppingDistance + EARLY_STOP_BUFFER;

    // Decide movement direction
    if (paddleY < lowerBound) {
      if (lastDirection.value !== 1) {
        lastDirection.value = 1;
        sendDirection(1);
      }
    } else if (paddleY > upperBound) {
      if (lastDirection.value !== -1) {
        lastDirection.value = -1;
        sendDirection(-1);
      }
    } else if (
      paddleY >= predictedY.value - stoppingDistance &&
      paddleY <= predictedY.value + stoppingDistance &&
      lastDirection.value !== 0
    ) {
      lastDirection.value = 0;
      sendDirection(0);
    }
  }
);

const stopAI = () => {
  if (aiPredictionIntervalId) {
    clearInterval(aiPredictionIntervalId);
  }

  if (aiMovementFrameId) {
    cancelAnimationFrame(aiMovementFrameId);
  }

  sendDirection(0);
};

onMounted(() => {
  aiPredictionIntervalId = setInterval(predictBallYAtPaddle, PREDICTION_INTERVAL);
});

onUnmounted(() => {
  stopAI();
});
</script>

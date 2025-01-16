<template>
  <slot />
</template>

<script setup>
import { defineProps, onMounted, onUnmounted, watch } from 'vue';

import {
  EARLY_STOP_BUFFER,
  MAX_ERROR_FACTOR,
  MOVEMENT_WINDOW,
  PREDICTION_INTERVAL,
} from './config/constants.js';

const { socket, side, ballPosition, ballVelocity, paddleParams } = defineProps({
  socket: {
    type: WebSocket,
    required: true,
  },
  side: {
    type: String,
    required: true,
    validator: (value) => ['left', 'right'].includes(value),
  },
  ballPosition: {
    type: Object,
    required: true,
    validator: (value) => typeof value.x === 'number' && typeof value.y === 'number',
  },
  ballVelocity: {
    type: Object,
    required: true,
    validator: (value) => typeof value.x === 'number' && typeof value.y === 'number',
  },
  paddleParams: {
    type: Object,
    required: true,
    validator: (value) => {
      return (
        typeof value.width === 'number' &&
        typeof value.height === 'number' &&
        value.position &&
        typeof value.position.y === 'number' &&
        typeof value.speed === 'number' &&
        typeof value.deacceleration === 'number'
      );
    },
  },
});

let aiPredictionIntervalId = null;
let aiMovementFrameId = null;
let predictedY = paddleParams?.position?.y;
let lastDirection = 0;

// Send direction to the server
const sendDirection = (direction) => {
  if (socket.readyState === WebSocket.OPEN) {
    try {
      socket.send(
        JSON.stringify({
          type: 'paddle',
          side,
          direction,
        })
      );
    } catch (error) {
      console.error('❌ Error sending paddle direction:', error);
    }
  }
};

const predictBallYAtPaddle = () => {
  const paddleX = side === 'left' ? 0 : 100;
  const ballDirectionX = ballVelocity?.x > 0 ? 'right' : 'left';

  // Reset to center if ball is moving away
  if (
    (side === 'left' && ballDirectionX !== 'left') ||
    (side === 'right' && ballDirectionX !== 'right')
  ) {
    return;
  }

  // Calculate time until the ball reaches the paddle's x-axis
  const distanceToPaddleX = Math.abs(ballPosition?.x - paddleX);
  const timeToPaddle = distanceToPaddleX / Math.abs(ballVelocity?.x);
  let predictedY = ballPosition?.y + ballVelocity?.y * timeToPaddle;

  // Handle bouncing off top and bottom boundaries
  while (predictedY < 0 || predictedY > 100) {
    if (predictedY < 0) {
      predictedY = -predictedY;
    } else if (predictedY > 100) {
      predictedY = 200 - predictedY;
    }
  }

  // Adjust prediction with a paddle width
  predictedY = Math.min(
    100 - paddleParams?.width / 2,
    Math.max(paddleParams?.width / 2, Math.round(predictedY))
  );

  // Add prediction error based on ball distance from the paddle
  const errorFactor = Math.min(1, distanceToPaddleX / 100);
  const error = (Math.random() * 2 - 1) * MAX_ERROR_FACTOR * errorFactor;
  predictedY += error;

  return predictedY;
};

// Start AI Prediction (Once per second)
const startPrediction = () => {
  aiPredictionIntervalId = setInterval(() => {
    predictedY = predictBallYAtPaddle();
  }, PREDICTION_INTERVAL);
};

watch(
  () => ballVelocity,
  () => {
    const ballDirectionX = ballVelocity?.x > 0 ? 'right' : 'left';

    // Reset to center if ball is moving away
    if (
      (side === 'left' && ballDirectionX !== 'left') ||
      (side === 'right' && ballDirectionX !== 'right')
    ) {
      const randomY =
        paddleParams?.y > 50
          ? (Math.random() * (65 - 50) + 50).toFixed(2)
          : (Math.random() * (50 - 35) + 35).toFixed(2);
      predictedY = parseFloat(randomY);
    }
  }
);

// Adjusted watch logic
watch(
  () => paddleParams,
  (newPosition) => {
    const paddleY = newPosition.y;

    // Calculate stopping distance based on current speed
    const stoppingDistance = Math.pow(paddleParams?.speed, 2) / (2 * paddleParams?.deacceleration);

    // Adjust bounds with stopping distance
    const lowerBound = predictedY - MOVEMENT_WINDOW - stoppingDistance - EARLY_STOP_BUFFER;
    const upperBound = predictedY + MOVEMENT_WINDOW + stoppingDistance + EARLY_STOP_BUFFER;

    // Decide movement direction
    if (paddleY < lowerBound) {
      if (lastDirection !== 1) {
        lastDirection = 1;
        sendDirection(1);
      }
    } else if (paddleY > upperBound) {
      if (lastDirection !== -1) {
        lastDirection = -1;
        sendDirection(-1);
      }
    } else if (
      paddleY >= predictedY - stoppingDistance &&
      paddleY <= predictedY + stoppingDistance &&
      lastDirection !== 0
    ) {
      lastDirection = 0;
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
  startPrediction();
});

onUnmounted(() => {
  stopAI();
});
</script>

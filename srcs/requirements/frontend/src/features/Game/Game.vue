<script setup>
import { computed, defineProps, onMounted, onUnmounted, onUpdated, ref, watch } from 'vue';

import { Ball, Paddle, withAiControl, withPlayerControl } from './components';
import { BALL_HEIGHT } from './components/Ball/config/constants.js';
import { PADDLE_HEIGHT, PADDLE_WIDTH } from './components/Paddle/config/constants.js';
import { DEFAULT_GAME_SETTINGS } from './config/constants.js';

const props = defineProps({
  forcedBallPosition: {
    type: Object,
    default: null,
  },
  settings: {
    type: Object,
    default: () => ({ ...DEFAULT_GAME_SETTINGS }),
  },
});

// Dimensions
const containerRef = ref(null);
const containerWidth = ref(0);
const containerHeight = ref(0);
const ballWidth = ref(0);
const ballHeight = ref(0);
const paddleWidth = ref(0);
const paddleHeight = ref(0);

// Socket connection
const socketMessage = ref('');
let socket = null;

// Game state
const ballPosition = ref({ x: 50, y: 50 });
const ballVelocity = ref({ x: 0, y: 0 });
const isBallOutOfBounds = ref(false);
const ballCurve = ref(0);
const ballBouncedOffSurface = ref(0);
const leftPaddle = ref({
  width: 1.5,
  height: 10,
  position: { y: 50 },
  speed: 0,
  deacceleration: 0.1,
});
const rightPaddle = ref({
  width: 1.5,
  height: 10,
  position: { y: 50 },
  speed: 0,
  deacceleration: 0.1,
});

const isBallPositionForced = computed(() => Boolean(props.forcedBallPosition));

const updateContainerDimensions = () => {
  // noinspection JSUnresolvedReference
  if (containerRef?.value) {
    containerWidth.value = containerRef.value.offsetWidth;
    containerHeight.value = containerRef.value.offsetHeight;
  }
};

const calculateBallSize = () => {
  if (containerWidth.value && containerHeight.value) {
    const ballHeightPixels = (BALL_HEIGHT / 100) * containerHeight.value;
    ballHeight.value = BALL_HEIGHT;
    ballWidth.value = parseFloat(((ballHeightPixels / containerWidth.value) * 100).toFixed(2));
  }
};

const calculatePaddleSizeInPercentages = () => {
  if (containerWidth.value && containerHeight.value) {
    paddleWidth.value = parseFloat(((PADDLE_WIDTH / containerWidth.value) * 100).toFixed(2));
    paddleHeight.value = parseFloat(((PADDLE_HEIGHT / containerHeight.value) * 100).toFixed(2));
  }
};

const initializeWebSocketInPercentages = () => {
  const socketUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws/pong/';
  socket = new WebSocket(socketUrl);

  socket.onopen = () => {
    console.log('✅ WebSocket connected');

    if (isNaN(ballWidth.value) || isNaN(ballHeight.value)) {
      console.error('Invalid width or height values:', ballWidth.value, ballHeight.value);
      return;
    }

    // Check if the WebSocket is open (readyState === 1)
    if (socket.readyState === WebSocket.OPEN) {
      try {
        socket.send(
          JSON.stringify({
            type: 'init',
            ballWidth: ballWidth.value,
            ballHeight: ballHeight.value,
            paddleWidth: paddleWidth.value,
            paddleHeight: paddleHeight.value,
          })
        );
      } catch (error) {
        console.error('Error sending data:', error);
      }
    } else {
      console.error('WebSocket is not open yet');
    }
  };

  socket.onmessage = (event) => {
    // console.log('📨 Message from server:', event.data);
    const data = JSON.parse(event.data);
    const { ball, paddles } = data || {};

    socketMessage.value = data;

    if (ball) {
      const {
        position = { x: 50, y: 50 },
        velocity = { x: 0, y: 0 },
        is_out_of_bounds: isOutOfBounds = false,
        curve = 0,
        bouncedOffSurface,
      } = ball || {};
      const { forcedBallPosition } = props;
      ballPosition.value = forcedBallPosition?.x != null ? forcedBallPosition : position;
      ballVelocity.value = velocity;
      isBallOutOfBounds.value = isOutOfBounds;
      ballCurve.value = curve;
      ballBouncedOffSurface.value = bouncedOffSurface;
    }

    if (paddles) {
      const { left, right } = paddles || {};
      if (left) {
        leftPaddle.value = left;
      }
      if (right) {
        rightPaddle.value = right;
      }
    }
  };

  socket.onerror = (error) => {
    console.error('❌ WebSocket error:', error);
  };

  socket.onclose = (event) => {
    console.info('🔌 WebSocket disconnected:', event.reason);
  };
};

const closeWebSocket = () => {
  if (socket) {
    socket.close();
    console.info('🔌 WebSocket connection closed');
  }
};

watch([containerWidth, containerHeight], calculateBallSize, {
  immediate: true,
});

watch([containerWidth, containerHeight], calculatePaddleSizeInPercentages, {
  immediate: true,
});

watch(
  () => props.settings,
  (newSettings) => {
    console.log('Game settings changed:', newSettings);

    if (socket?.readyState === WebSocket.OPEN) {
      socket.send(
        JSON.stringify({
          type: 'restart',
        })
      );
    }
  },
  { immediate: true, deep: true }
);

onMounted(() => {
  updateContainerDimensions();
  initializeWebSocketInPercentages();
  window.addEventListener('resize', updateContainerDimensions);
});

onUpdated(() => {
  updateContainerDimensions();
});

onUnmounted(() => {
  closeWebSocket();
  window.removeEventListener('resize', updateContainerDimensions);
});
</script>

<template>
  <div class="game">
    <div class="game__void-boundary">
      <div class="game__void-boundary-shadow game__void-boundary-shadow_left" />
      <div class="game__void-boundary-shadow game__void-boundary-shadow_right" />
    </div>
    <div ref="containerRef" class="game__container">
      <Ball
        :width="ballWidth"
        :height="ballHeight"
        :position="ballPosition"
        :is-position-forced="isBallPositionForced"
        :velocity="ballVelocity"
        :is-out-of-bounds="isBallOutOfBounds"
        :curve="ballCurve"
        :ball-bounced-off-surface="ballBouncedOffSurface"
      />
      <component
        :is="side.controlledBy === 'player' ? withPlayerControl : withAiControl"
        v-for="(side, index) in props.settings?.sides || []"
        :key="index"
        :socket="socket"
        :side="side.side"
        :controls="side.controls"
        :ball-position="ballPosition"
        :ball-velocity="ballVelocity"
        :paddle-params="side.side === 'left' ? leftPaddle : rightPaddle"
      >
        <Paddle :side="side.side" :params="side.side === 'left' ? leftPaddle : rightPaddle" />
      </component>
    </div>
  </div>
</template>

<style scoped>
.game {
  position: relative;

  box-sizing: border-box;
  width: 100%;
  height: 100%;
  padding-right: 20px;
  padding-left: 20px;

  background: linear-gradient(to right, var(--light-color) 50%, var(--dark-color) 50%);
}

.game__container {
  position: relative;

  width: 100%;
  height: 100%;
  padding: 20px;

  background: linear-gradient(to right, var(--light-color) 50%, var(--dark-color) 50%);
}

.game__void-boundary {
  position: absolute;
  top: 0;
  left: 0;

  display: flex;
  justify-content: space-between;

  width: 100%;
  height: 100%;
}

.game__void-boundary-shadow {
  position: absolute;
  z-index: 2;
  width: 7%;
  height: 100%;
}

.game__void-boundary-shadow_left {
  left: 0;
  background: linear-gradient(to right, var(--light-color), transparent);
}

.game__void-boundary-shadow_right {
  right: 0;
  background: linear-gradient(to left, var(--dark-color), transparent);
}
</style>

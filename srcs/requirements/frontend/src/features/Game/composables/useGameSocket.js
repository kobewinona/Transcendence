import { convertObjectKeys, toSnakeCase, useWebSocket } from 'shared/lib';
import { inject, onUnmounted, provide, ref } from 'vue';

import {
  GAME_STATE_MESSAGE_TYPE,
  GAME_STATUS_IDLE,
  GAME_UPDATE_MESSAGE_TYPE,
} from '../config/constants.js';

const useGameSocket = (url) => {
  let animationFrameId;

  // Game State
  const status = ref(0);
  const countdown = ref(0);

  // Ball State
  const ballPositionX = ref(0);
  const ballPositionY = ref(0);
  const ballVelocityX = ref(0);
  const ballVelocityY = ref(0);
  const isBallOutOfBounds = ref(false);
  const ballCurve = ref(0);
  const ballBouncedOffSurface = ref(0);

  // Left Paddle State
  const leftPaddleWidth = ref(0);
  const leftPaddleHeight = ref(0);
  const leftPaddleY = ref(0);
  const leftPaddleSpeed = ref(0);

  // Right Paddle State
  const rightPaddleWidth = ref(0);
  const rightPaddleHeight = ref(0);
  const rightPaddleY = ref(0);
  const rightPaddleSpeed = ref(0);

  const actions = {};

  function handleMessage(dataView) {
    const messageType = dataView.getUint8(0);

    if (messageType === GAME_STATE_MESSAGE_TYPE) {
      status.value = dataView.getUint8(1);
      countdown.value = dataView.getUint8(2);

      if (status.value === GAME_STATUS_IDLE) {
        actions.startGame();
      }
    }

    if (messageType === GAME_UPDATE_MESSAGE_TYPE) {
      // Ball State
      ballPositionX.value = dataView.getFloat32(1, true);
      ballPositionY.value = dataView.getFloat32(5, true);
      ballVelocityX.value = dataView.getFloat32(9, true);
      ballVelocityY.value = dataView.getFloat32(13, true);
      isBallOutOfBounds.value = dataView.getUint8(17) === 1;
      ballCurve.value = dataView.getFloat32(18, true);
      ballBouncedOffSurface.value = dataView.getUint8(22);

      // Left Paddle State
      leftPaddleWidth.value = dataView.getFloat32(23, true);
      leftPaddleHeight.value = dataView.getFloat32(27, true);
      leftPaddleY.value = dataView.getFloat32(31, true);
      leftPaddleSpeed.value = dataView.getFloat32(35, true);

      // Right Paddle State
      rightPaddleWidth.value = dataView.getFloat32(39, true);
      rightPaddleHeight.value = dataView.getFloat32(43, true);
      rightPaddleY.value = dataView.getFloat32(47, true);
      rightPaddleSpeed.value = dataView.getFloat32(51, true);
    }
  }

  const {
    socket,
    sendMessage,
    close: closeGameSocket,
  } = useWebSocket(url, {
    onMessage: handleMessage,
    binaryType: 'arraybuffer',
  });

  function startGame() {
    sendMessage({ action: 'start' });
  }

  function stopGame() {
    sendMessage({ action: 'stop' });
  }

  function pauseGame() {
    sendMessage({ action: 'pause' });
  }

  function resetGame() {
    sendMessage({ action: 'reset' });
  }

  function updatePaddlePosition(data) {
    sendMessage({
      action: 'update_paddle',
      ...convertObjectKeys(data, toSnakeCase),
    });
  }

  function updateGameDimensions(data) {
    sendMessage({
      action: 'update_dimensions',
      ...convertObjectKeys(data, toSnakeCase),
    });
  }

  Object.assign(actions, {
    closeGameSocket,
    handleMessage,
    startGame,
    stopGame,
    pauseGame,
    resetGame,
    updatePaddlePosition,
    updateGameDimensions,
  });

  onUnmounted(() => {
    cancelAnimationFrame(animationFrameId);
  });

  return {
    socket,
    status,
    ballPositionX,
    ballPositionY,
    ballVelocityX,
    ballVelocityY,
    isBallOutOfBounds,
    ballCurve,
    ballBouncedOffSurface,
    leftPaddleWidth,
    leftPaddleHeight,
    leftPaddleY,
    leftPaddleSpeed,
    rightPaddleWidth,
    rightPaddleHeight,
    rightPaddleY,
    rightPaddleSpeed,
    actions,
  };
};

export const provideGameSocket = (url) => {
  const gameState = useGameSocket(url);
  provide('gameState', gameState);
};

export const useGameSocketInject = () => {
  const context = inject('gameState');
  if (!context) {
    throw new Error('useGameStateInject must be used within provideGameState');
  }
  return context;
};

export default useGameSocket;

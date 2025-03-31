import {
  CONTROLLERS_INPUT_NAME,
  DEMO_DEFAULT_GAME_SETTINGS,
  NAME_INPUT_NAME,
  SIDE_INPUT_NAME,
} from 'entities/Game/config/constants.js';
import { isPlainObject } from 'lodash';
import { useWebSocket } from 'shared/composables';
import { convertObjectKeys, toSnakeCase } from 'shared/lib';
import { inject, onUnmounted, provide, ref } from 'vue';

const useGameSocket = (url) => {
  let animationFrameId;

  // Game State
  const status = ref(0);
  const leftScore = ref(0);
  const rightScore = ref(0);
  const isDeuce = ref(false);
  const isLeftAdvantage = ref(false);
  const isRightAdvantage = ref(false);
  const winner = ref(undefined);

  // Ball State
  const ballPositionX = ref(0);
  const ballPositionY = ref(0);
  const ballVelocityX = ref(0);
  const ballVelocityY = ref(0);
  const isBallOutOfBounds = ref(false);
  const ballCurve = ref(0);
  const ballBouncedOffSurface = ref(0);

  const paddleNames = ref([]);
  const paddleWidths = ref([]);
  const paddleHeights = ref([]);
  const paddlePositions = ref([]);
  const paddleSpeeds = ref([]);

  const gameSettings = ref(DEMO_DEFAULT_GAME_SETTINGS);

  const error = ref('');

  const actions = {};

  function handleMessage(data) {
    if (isPlainObject(data)) {
      const bindings = {
        error,
        status,
        leftScore,
        rightScore,
        isDeuce,
        isLeftAdvantage,
        isRightAdvantage,
        winner,
      };

      for (const [key, ref] of Object.entries(bindings)) {
        if (data?.[key] !== undefined) {
          ref.value = data[key];
        }
      }
    }

    if (data instanceof DataView) {
      let offset = 0;

      const minBallStateSize = 4 * 4 + 1 + 4 + 1;
      if (data.byteLength < minBallStateSize) {
        console.error(
          '❌ Invalid GAME_UPDATE_MESSAGE_TYPE: Payload too short for ball state',
          data.byteLength
        );
        return;
      }

      // Ball State
      ballPositionX.value = data.getFloat32(offset, true);
      offset += 4;
      ballPositionY.value = data.getFloat32(offset, true);
      offset += 4;
      ballVelocityX.value = data.getFloat32(offset, true);
      offset += 4;
      ballVelocityY.value = data.getFloat32(offset, true);
      offset += 4;
      isBallOutOfBounds.value = data.getUint8(offset) === 1;
      offset += 1;
      ballCurve.value = data.getFloat32(offset, true);
      offset += 4;
      ballBouncedOffSurface.value = data.getUint8(offset);
      offset += 1;

      const paddleDataSize = 4 * 4;
      const expectedSize = minBallStateSize + paddleNames.value.length * paddleDataSize;

      if (data.byteLength < expectedSize) {
        console.error(
          `❌ Incomplete paddle data: Expected ${expectedSize}, got ${data.byteLength}`
        );
        return;
      }

      // Paddle States
      for (let i = 0; i < paddleNames.value.length; i++) {
        paddleWidths.value[i] = data.getFloat32(offset, true);
        offset += 4;
        paddleHeights.value[i] = data.getFloat32(offset, true);
        offset += 4;
        paddlePositions.value[i] = data.getFloat32(offset, true);
        offset += 4;
        paddleSpeeds.value[i] = data.getFloat32(offset, true);
        offset += 4;
      }
    }
  }

  const {
    socket,
    sendMessage,
    close: closeGameSocket,
    ...rest
  } = useWebSocket(url, {
    onMessage: handleMessage,
    binaryType: 'arraybuffer',
  });

  function startGame(settings) {
    if (!settings) return;

    gameSettings.value = settings;
    paddleNames.value = settings[CONTROLLERS_INPUT_NAME]?.map(({ name }) => name);

    const message = {
      action: 'start',
      data: {
        ...settings,
        [CONTROLLERS_INPUT_NAME]: settings[CONTROLLERS_INPUT_NAME].map(
          ({ [SIDE_INPUT_NAME]: side, [NAME_INPUT_NAME]: name }) => ({ side, name })
        ),
      },
    };

    sendMessage(message);
  }

  function stopGame() {
    sendMessage({ action: 'stop' });
  }

  function pauseGame() {
    sendMessage({ action: 'pause' });
  }

  function resumeGame() {
    sendMessage({ action: 'resume' });
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
    resumeGame,
    updatePaddlePosition,
    updateGameDimensions,
  });

  onUnmounted(() => {
    cancelAnimationFrame(animationFrameId);
  });

  return {
    socket,
    status,
    leftScore,
    rightScore,
    isDeuce,
    isLeftAdvantage,
    isRightAdvantage,
    winner,
    ballPositionX,
    ballPositionY,
    ballVelocityX,
    ballVelocityY,
    isBallOutOfBounds,
    ballCurve,
    ballBouncedOffSurface,
    paddleNames,
    paddleWidths,
    paddleHeights,
    paddlePositions,
    paddleSpeeds,
    actions,
    gameSettings,
    error,
    ...rest,
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

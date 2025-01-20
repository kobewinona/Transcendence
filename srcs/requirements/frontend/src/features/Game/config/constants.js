export const GAME_STATE_MESSAGE_TYPE = 1;
export const GAME_UPDATE_MESSAGE_TYPE = 2;

export const GAME_STATUS_IDLE = 1;
export const GAME_STATUS_INIT = 2;
export const GAME_STATUS_COUNTDOWN = 3;
export const GAME_STATUS_IN_PROGRESS = 4;
export const GAME_STATUS_ENDED = 5;

export const QUICK_START_GAME_MODE = 'quick_start';
export const DEMO_GAME_MODE = 'demo';

export const CONTROLLED_BY_PLAYER = 'player';
export const CONTROLLED_BY_AI = 'AI';

export const DEFAULT_GAME_SETTINGS = {
  mode: DEMO_GAME_MODE,
  sides: [
    {
      side: 'left',
      controlledBy: CONTROLLED_BY_AI,
      controls: null,
    },
    {
      side: 'right',
      controlledBy: CONTROLLED_BY_AI,
      controls: null,
    },
  ],
};

export const QUICK_START_GAME_SETTINGS = {
  mode: QUICK_START_GAME_MODE,
  sides: [
    {
      side: 'left',
      controlledBy: CONTROLLED_BY_PLAYER,
      controls: { up: 'KeyW', down: 'KeyS' },
    },
    {
      side: 'right',
      controlledBy: CONTROLLED_BY_AI,
      controls: null,
    },
  ],
};

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

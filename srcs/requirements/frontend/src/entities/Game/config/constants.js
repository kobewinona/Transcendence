import ballSkin1 from 'assets/ballSkins/regular/skin1.png';
import { BALL_REGULAR_TYPE_SKIN_KEY } from 'entities/BallSkin/config/constants.js';
import { CONTROL_KEYS } from 'entities/Controller/config/constants.js';
import { svgComponents } from 'shared/lib';

export const MAX_PLAYERS_AMOUNT = 6;

export const GAME_STATE_MESSAGE_TYPE = 1;
export const GAME_UPDATE_MESSAGE_TYPE = 2;

export const GAME_STATUS_IDLE = 1;
export const GAME_STATUS_INIT = 2;
export const GAME_STATUS_COUNTDOWN = 3;
export const GAME_STATUS_IN_PROGRESS = 4;
export const GAME_STATUS_ENDED = 5;

export const DEMO_GAME_MODE = 'demo';
export const QUICK_START_GAME_MODE = 'quick_start';
export const NEW_GAME_GAME_MODE = 'new_game';

export const MODE_INPUT_NAME = 'mode';

export const CONTROLLERS_INPUT_NAME = 'controllers';
export const SIDE_INPUT_NAME = 'side';
export const NAME_INPUT_NAME = 'name';
export const CONTROLLED_BY_INPUT_NAME = 'controlledBy';
export const CONTROLS_INPUT_NAME = 'controls';

export const BALL_DESIGN_INPUT_NAME = 'design';
export const BALL_COLOR_INPUT_NAME = 'color';
export const BALL_SKIN_TYPE_INPUT_NAME = 'skin_type';
export const BALL_SKIN_INPUT_NAME = 'skin';

export const NEW_GAME_SETTINGS_FORM_PROVIDE_KEY = 'new_game_settings_form';

export const COLORS = [
  '--primary-color-opacity-50',
  '--secondary-color-opacity-50',
  '--complementary-1-color-opacity-50',
  '--complementary-2-color-opacity-50',
  '--complementary-3-color-opacity-50',
  '--complementary-4-color-opacity-50',
];

export const CONTROLLED_BY_PLAYER = {
  key: 'player',
  name: 'Player',
  icon: svgComponents['GameConsoleIcon'],
};

export const CONTROLLED_BY_AI = {
  key: 'ai',
  name: 'AI',
  icon: svgComponents['AiIcon'],
};

export const CONTROLLED_BY_OPTIONS = [
  { value: CONTROLLED_BY_PLAYER, label: 'Controlled by Player' },
  { value: CONTROLLED_BY_AI, label: 'Controlled by AI' },
];

export const NEW_CONTROLLER_SETTINGS = (index, side) => ({
  [SIDE_INPUT_NAME]: side,
  [NAME_INPUT_NAME]: `PLAYER ${index}`,
  [CONTROLLED_BY_INPUT_NAME]: CONTROLLED_BY_PLAYER,
  [CONTROLS_INPUT_NAME]: undefined,
});

export const DEFAULT_DESIGN_SETTINGS = {
  [BALL_DESIGN_INPUT_NAME]: {
    [BALL_COLOR_INPUT_NAME]: '--primary-color',
    [BALL_SKIN_TYPE_INPUT_NAME]: BALL_REGULAR_TYPE_SKIN_KEY,
    [BALL_SKIN_INPUT_NAME]: ballSkin1,
  },
};

export const DEMO_DEFAULT_GAME_SETTINGS = {
  [MODE_INPUT_NAME]: DEMO_GAME_MODE,
  [CONTROLLERS_INPUT_NAME]: [
    {
      [SIDE_INPUT_NAME]: 'left',
      [NAME_INPUT_NAME]: 'CPU 1',
      [CONTROLLED_BY_INPUT_NAME]: CONTROLLED_BY_AI,
      [CONTROLS_INPUT_NAME]: null,
    },
    {
      [SIDE_INPUT_NAME]: 'right',
      [NAME_INPUT_NAME]: 'CPU 2',
      [CONTROLLED_BY_INPUT_NAME]: CONTROLLED_BY_AI,
      [CONTROLS_INPUT_NAME]: null,
    },
  ],
  ...DEFAULT_DESIGN_SETTINGS,
};

export const QUICK_START_DEFAULT_GAME_SETTINGS = {
  [MODE_INPUT_NAME]: QUICK_START_GAME_MODE,
  [CONTROLLERS_INPUT_NAME]: [
    {
      [SIDE_INPUT_NAME]: 'left',
      [NAME_INPUT_NAME]: 'PLAYER 1',
      [CONTROLLED_BY_INPUT_NAME]: CONTROLLED_BY_PLAYER,
      [CONTROLS_INPUT_NAME]: CONTROL_KEYS['left'][0],
    },
    {
      [SIDE_INPUT_NAME]: 'right',
      [NAME_INPUT_NAME]: 'CPU 1',
      [CONTROLLED_BY_INPUT_NAME]: CONTROLLED_BY_AI,
      [CONTROLS_INPUT_NAME]: null,
    },
  ],
  ...DEFAULT_DESIGN_SETTINGS,
};

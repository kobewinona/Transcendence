import ballSkin1 from 'assets/ballSkins/regular/skin1.png';
import { BALL_REGULAR_TYPE_SKIN_KEY } from 'entities/BallSkin/config/constants.js';
import { CONTROL_KEYS } from 'entities/Controller/config/constants.js';
import { svgComponents } from 'shared/lib';

export const MAX_PLAYERS_AMOUNT = 6;

// TODO if the score settings works correctly
export const END_SCORE_OPTIONS = [
  { value: 6, label: '6' },
  { value: 11, label: '11' },
  { value: 21, label: '21' },
];

export const DEUCE_SYSTEM_OPTIONS = [
  { value: 1, label: 'off' },
  { value: 2, label: 'on' },
];

export const SPEED_OPTIONS = [
  { value: 1, label: 'slow' },
  { value: 2, label: 'default' },
  { value: 3, label: 'fast' },
];

export const VELOCITY_OPTIONS = [
  { value: 1, label: 'low' },
  { value: 2, label: 'default' },
  { value: 3, label: 'high' },
];

export const DEFAULT_END_SCORE = END_SCORE_OPTIONS[1];
export const DEFAULT_IS_DEUCE_ON = DEUCE_SYSTEM_OPTIONS[1];
export const DEFAULT_BALL_SPEED = SPEED_OPTIONS[1];
export const DEFAULT_MAX_BALL_CURVE = VELOCITY_OPTIONS[1];

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

export const GAME_INPUT_NAME = 'game';
export const END_GAME_SCORE_INPUT_NAME = 'end_score';
export const IS_DEUCE_ON_INPUT_NAME = 'is_deuce_on';

export const GAMEPLAY_INPUT_NAME = 'gameplay';
export const BALL_SPEED_INPUT_NAME = 'ball_speed';
export const MAX_BALL_CURVE_INPUT_NAME = 'max_ball_curve';
export const PADDLE_SPEED_INPUT_NAME = 'paddle_speed';

export const BALL_DESIGN_INPUT_NAME = 'design';
export const BALL_COLOR_INPUT_NAME = 'color';
export const BALL_SKIN_TYPE_INPUT_NAME = 'skin_type';
export const BALL_SKIN_INPUT_NAME = 'skin';

export const NEW_GAME_SETTINGS_FORM_PROVIDE_KEY = 'new_game_settings_form';

export const COLORS = [
  '--primary-color',
  '--secondary-color',
  '--complementary-1-color',
  '--complementary-2-color',
  '--complementary-3-color',
  '--complementary-4-color',
];

// Controllers
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

// Default settings
export const DEFAULT_GAME_SETTINGS = {
  [END_GAME_SCORE_INPUT_NAME]: DEFAULT_END_SCORE,
  [IS_DEUCE_ON_INPUT_NAME]: DEFAULT_IS_DEUCE_ON,
};

export const DEFAULT_GAMEPLAY_SETTINGS = {
  [BALL_SPEED_INPUT_NAME]: DEFAULT_BALL_SPEED,
  [MAX_BALL_CURVE_INPUT_NAME]: DEFAULT_MAX_BALL_CURVE,
};

export const DEFAULT_DESIGN_SETTINGS = {
  [BALL_COLOR_INPUT_NAME]: '--primary-color',
  [BALL_SKIN_TYPE_INPUT_NAME]: BALL_REGULAR_TYPE_SKIN_KEY,
  [BALL_SKIN_INPUT_NAME]: ballSkin1,
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
  [GAME_INPUT_NAME]: null,
  [GAMEPLAY_INPUT_NAME]: null,
  [BALL_DESIGN_INPUT_NAME]: DEFAULT_DESIGN_SETTINGS,
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
  [GAME_INPUT_NAME]: null,
  [GAMEPLAY_INPUT_NAME]: null,
  [BALL_DESIGN_INPUT_NAME]: DEFAULT_DESIGN_SETTINGS,
};

export const NEW_GAME_DEFAULT_GAME_SETTINGS = {
  [MODE_INPUT_NAME]: NEW_GAME_GAME_MODE,
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
  [GAME_INPUT_NAME]: DEFAULT_GAME_SETTINGS,
  [GAMEPLAY_INPUT_NAME]: DEFAULT_GAMEPLAY_SETTINGS,
  [BALL_DESIGN_INPUT_NAME]: DEFAULT_DESIGN_SETTINGS,
};

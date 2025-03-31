import {
  BALL_SPEED_INPUT_NAME,
  DEUCE_SYSTEM_OPTIONS,
  END_GAME_SCORE_INPUT_NAME,
  END_SCORE_OPTIONS,
  GAME_INPUT_NAME,
  GAMEPLAY_INPUT_NAME,
  IS_DEUCE_ON_INPUT_NAME,
  MAX_BALL_CURVE_INPUT_NAME,
  SPEED_OPTIONS,
  VELOCITY_OPTIONS,
} from 'entities/Game/config/constants.js';

export const GAME_SETTINGS_FIELDS = [
  {
    key: 'end_score',
    name: `${GAME_INPUT_NAME}.${END_GAME_SCORE_INPUT_NAME}`,
    label: 'game_settings.tabs.game.fields.score.label',
    options: END_SCORE_OPTIONS,
  },
  {
    key: 'deuce',
    name: `${GAME_INPUT_NAME}.${IS_DEUCE_ON_INPUT_NAME}`,
    label: 'game_settings.tabs.game.fields.deuce.label',
    options: DEUCE_SYSTEM_OPTIONS,
  },
];

export const GAMEPLAY_SETTINGS_FIELDS = [
  {
    key: 'ball_speed',
    name: `${GAMEPLAY_INPUT_NAME}.${BALL_SPEED_INPUT_NAME}`,
    label: 'game_settings.tabs.gameplay.fields.ball_speed.label',
    options: SPEED_OPTIONS,
  },
  {
    key: 'max_ball_curve',
    name: `${GAMEPLAY_INPUT_NAME}.${MAX_BALL_CURVE_INPUT_NAME}`,
    label: 'game_settings.tabs.gameplay.fields.max_ball_curve.label',
    options: VELOCITY_OPTIONS,
  },
];

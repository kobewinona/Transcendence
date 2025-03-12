import {
  BALL_SPEED_INPUT_NAME,
  DEUCE_SYSTEM_OPTIONS,
  END_GAME_SCORE_INPUT_NAME,
  END_SCORE_OPTIONS,
  IS_DEUCE_ON_INPUT_NAME,
  MAX_BALL_CURVE_INPUT_NAME,
  SPEED_OPTIONS,
  VELOCITY_OPTIONS,
} from 'entities/Game/config/constants.js';

export const GAME_SETTINGS_FIELDS = [
  {
    key: 'end_score',
    name: END_GAME_SCORE_INPUT_NAME,
    label: 'game_settings.tabs.game.fields.score.label',
    defaultValue: 11,
    options: END_SCORE_OPTIONS,
  },
  {
    key: 'deuce',
    name: IS_DEUCE_ON_INPUT_NAME,
    label: 'game_settings.tabs.game.fields.deuce.label',
    defaultValue: 2,
    options: DEUCE_SYSTEM_OPTIONS,
  },
];

export const GAMEPLAY_SETTINGS_FIELDS = [
  {
    key: 'ball_speed',
    name: BALL_SPEED_INPUT_NAME,
    label: 'game_settings.tabs.gameplay.fields.ball_speed.label',
    defaultValue: 2,
    options: SPEED_OPTIONS,
  },
  {
    key: 'max_ball_curve',
    name: MAX_BALL_CURVE_INPUT_NAME,
    label: 'game_settings.tabs.gameplay.fields.max_ball_curve.label',
    defaultValue: 2,
    options: VELOCITY_OPTIONS,
  },
];

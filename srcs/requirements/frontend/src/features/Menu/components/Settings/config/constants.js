import { DEUCE_SYSTEM_OPTIONS, END_SCORE_OPTIONS } from 'entities/Game/config/constants.js';

export const SETTINGS_FIELDS = [
  {
    key: 'language',
    label: 'menu.settings.system.language',
    options: END_SCORE_OPTIONS,
  },
  {
    key: 'end_score',
    label: 'game_settings.tabs.game.fields.deuce.label',
    options: DEUCE_SYSTEM_OPTIONS,
  },
];

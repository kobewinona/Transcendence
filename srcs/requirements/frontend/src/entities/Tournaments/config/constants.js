import {
  CONTROLLED_BY_PLAYER,
  DEFAULT_GAME_SETTINGS,
  DEFAULT_GAMEPLAY_SETTINGS,
  GAME_INPUT_NAME,
  GAMEPLAY_INPUT_NAME,
} from 'entities/Game/config/constants.js';
import { nanoid } from 'nanoid';

export const CURRENT_TAB_NAME = 'current';
export const HISTORY_TAB_NAME = 'history';

export const IN_PROGRESS_STATUS_NAME = 'in_progress';
export const ABANDONED_STATUS_NAME = 'abandoned';
export const FINISHED_STATUS_NAME = 'finished';

export const TOURNAMENT_TABS = [
  { value: 'current', label: 'tournament.tabs.current.title' },
  { value: 'history', label: 'tournament.tabs.history.title' },
];

export const TOURNAMENT_NAMES = {
  NAME: 'name',
  PLAYERS: 'players',
  PLAYERS_NAME: 'name',
  PLAYERS_CONTROLLED_BY: 'controlled_by',
  CONTROLS: 'controls',
  GAME: 'game',
  GAMEPLAY: 'gameplay',
};

export const NEW_PLAYER_DEFAULT_VALUES = {
  key: nanoid(),
  [TOURNAMENT_NAMES.PLAYERS_NAME]: '',
  [TOURNAMENT_NAMES.PLAYERS_CONTROLLED_BY]: CONTROLLED_BY_PLAYER.key,
};

export const NEW_TOURNAMENT_DEFAULT_VALUES = {
  [TOURNAMENT_NAMES.NAME]: '',
  [TOURNAMENT_NAMES.PLAYERS]: [
    {
      key: nanoid(),
      [TOURNAMENT_NAMES.PLAYERS_NAME]: '',
      [TOURNAMENT_NAMES.PLAYERS_CONTROLLED_BY]: CONTROLLED_BY_PLAYER.key,
    },
    {
      key: nanoid(),
      [TOURNAMENT_NAMES.PLAYERS_NAME]: '',
      [TOURNAMENT_NAMES.PLAYERS_CONTROLLED_BY]: CONTROLLED_BY_PLAYER.key,
    },
  ],
  [GAME_INPUT_NAME]: DEFAULT_GAME_SETTINGS,
  [GAMEPLAY_INPUT_NAME]: DEFAULT_GAMEPLAY_SETTINGS,
};

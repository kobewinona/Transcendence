// noinspection JSFileReferences
import { NewGame, Profile, Settings, Tournaments } from 'features/Menu/components';
import { svgComponents } from 'shared/lib';

export const QUICK_START_OPTION_KEY = 'quick_start';
export const NEW_GAME_OPTION_KEY = 'new_game';
export const TOURNAMENT_OPTION_KEY = 'tournament';
export const PROFILE_OPTION_KEY = 'profile';
export const SETTINGS_OPTION_KEY = 'settings';

export const MENU_ITEMS_KEYS = {
  QUICK_START_OPTION_KEY,
  NEW_GAME_OPTION_KEY,
  TOURNAMENT_OPTION_KEY,
  PROFILE_OPTION_KEY,
  SETTINGS_OPTION_KEY,
};

export const MENU_OPTION_KEYS_REQUIRING_LOADING = [TOURNAMENT_OPTION_KEY, PROFILE_OPTION_KEY];

export const MENU_ICONS = {
  [QUICK_START_OPTION_KEY]: svgComponents['LaunchIcon'],
  [NEW_GAME_OPTION_KEY]: svgComponents['GameConsoleIcon'],
  [TOURNAMENT_OPTION_KEY]: svgComponents['TournamentIcon'],
  [PROFILE_OPTION_KEY]: svgComponents['DeveloperIcon'],
  [SETTINGS_OPTION_KEY]: svgComponents['GameDevelopmentIcon'],
};

export const MODES_WITH_SOCKET_REQUIRED = [
  QUICK_START_OPTION_KEY,
  NEW_GAME_OPTION_KEY,
  TOURNAMENT_OPTION_KEY,
];

export const MENU_ITEMS = (t) => [
  {
    height: '70%',
    items: [
      {
        key: QUICK_START_OPTION_KEY,
        title: t('menu.items.item.quick_start.title'),
        description: t('menu.items.item.quick_start.description'),
        content: null,
        icon: MENU_ICONS[QUICK_START_OPTION_KEY],
        iconSlideTo: 'bottom',
        disabled: false,
      },
      {
        key: NEW_GAME_OPTION_KEY,
        title: t('menu.items.item.new_game.title'),
        description: t('menu.items.item.new_game.description'),
        content: NewGame,
        icon: MENU_ICONS[NEW_GAME_OPTION_KEY],
        iconSlideTo: 'bottom',
        disabled: false,
      },
      {
        key: TOURNAMENT_OPTION_KEY,
        title: t('menu.items.item.tournament.title'),
        description: t('menu.items.item.tournament.description'),
        content: Tournaments,
        icon: MENU_ICONS[TOURNAMENT_OPTION_KEY],
        iconSlideTo: 'bottom',
        disabled: false,
      },
    ],
  },
  {
    height: '30%',
    items: [
      {
        key: PROFILE_OPTION_KEY,
        title: t('menu.items.item.profile.title'),
        description: t('menu.items.item.profile.description'),
        content: Profile,
        icon: MENU_ICONS[PROFILE_OPTION_KEY],
        iconSlideTo: 'right',
        disabled: false,
      },
      {
        key: SETTINGS_OPTION_KEY,
        title: t('menu.items.item.settings.title'),
        description: t('menu.items.item.settings.description'),
        content: Settings,
        icon: MENU_ICONS[SETTINGS_OPTION_KEY],
        iconSlideTo: 'right',
        disabled: false,
      },
    ],
  },
];

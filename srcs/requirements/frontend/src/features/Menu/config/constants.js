// noinspection JSFileReferences
import { svgComponents } from 'shared/lib';

import { NewGame, Settings } from '../components';

const QUICK_START = 'quick_start';
const NEW_GAME = 'new_game';
const PLAY_ONLINE = 'play_online';
const PROFILE = 'profile';
const SETTINGS = 'settings';

export const MENU_ITEMS_KEYS = {
  QUICK_START,
  NEW_GAME,
  PLAY_ONLINE,
  PROFILE,
  SETTINGS,
};

export const MENU_ICONS = {
  [QUICK_START]: svgComponents['LaunchIcon'],
  [NEW_GAME]: svgComponents['GameConsoleIcon'],
  [PLAY_ONLINE]: svgComponents['GamepadIcon'],
  [PROFILE]: svgComponents['DeveloperIcon'],
  [SETTINGS]: svgComponents['GameDevelopmentIcon'],
};

export const MODES_WITH_SOCKET_REQUIRED = [QUICK_START, NEW_GAME, PLAY_ONLINE];

export const MENU_ITEMS = (t) => [
  {
    height: '70%',
    items: [
      {
        key: QUICK_START,
        title: t('menu.items.item.quick_start.title'),
        description: t('menu.items.item.quick_start.description'),
        content: null,
        icon: MENU_ICONS[QUICK_START],
        iconSlideTo: 'bottom',
        disabled: false,
      },
      {
        key: NEW_GAME,
        title: t('menu.items.item.new_game.title'),
        description: t('menu.items.item.new_game.description'),
        content: NewGame,
        icon: MENU_ICONS[NEW_GAME],
        iconSlideTo: 'bottom',
        disabled: false,
      },
      {
        key: PLAY_ONLINE,
        title: t('menu.items.item.online.title'),
        description: t('menu.items.item.online.description'),
        icon: MENU_ICONS[PLAY_ONLINE],
        iconSlideTo: 'bottom',
        disabled: true,
      },
    ],
  },
  {
    height: '30%',
    items: [
      {
        key: PROFILE,
        title: t('menu.items.item.profile.title'),
        description: t('menu.items.item.profile.description'),
        icon: MENU_ICONS[PLAY_ONLINE][PROFILE],
        iconSlideTo: 'right',
        disabled: true,
      },
      {
        key: SETTINGS,
        title: t('menu.items.item.settings.title'),
        description: t('menu.items.item.settings.description'),
        content: Settings,
        icon: MENU_ICONS[SETTINGS],
        iconSlideTo: 'right',
        disabled: false,
      },
    ],
  },
];

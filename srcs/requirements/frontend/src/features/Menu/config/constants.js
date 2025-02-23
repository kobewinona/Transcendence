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
        icon: svgComponents['GameIcon'],
        iconSlideTo: 'bottom',
        disabled: false,
      },
      {
        key: NEW_GAME,
        title: t('menu.items.item.new_game.title'),
        description: t('menu.items.item.new_game.description'),
        content: NewGame,
        icon: svgComponents['GameConsoleIcon'],
        iconSlideTo: 'bottom',
        disabled: false,
      },
      {
        key: PLAY_ONLINE,
        title: t('menu.items.item.online.title'),
        description: t('menu.items.item.online.description'),
        icon: svgComponents['GamepadIcon'],
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
        icon: svgComponents['DeveloperIcon'],
        iconSlideTo: 'right',
        disabled: true,
      },
      {
        key: SETTINGS,
        title: t('menu.items.item.settings.title'),
        description: t('menu.items.item.settings.description'),
        content: Settings,
        icon: svgComponents['GameDevelopmentIcon'],
        iconSlideTo: 'right',
        disabled: false,
      },
    ],
  },
];

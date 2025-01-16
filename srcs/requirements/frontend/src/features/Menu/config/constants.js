// noinspection JSFileReferences
import { svgComponents } from 'assets/svgComponents.js';

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

export const MENU_ITEMS = [
  {
    height: '70%',
    items: [
      {
        key: QUICK_START,
        title: 'Quick Start',
        description: 'Start a quick game against AI',
        icon: svgComponents['GameIcon'],
        iconSlideTo: 'bottom',
        disabled: false,
      },
      {
        key: NEW_GAME,
        title: 'New Game',
        description: 'Set up and start a new game',
        icon: svgComponents['GameConsoleIcon'],
        iconSlideTo: 'bottom',
        disabled: true,
      },
      {
        key: PLAY_ONLINE,
        title: 'Play Online',
        description: 'Join other players around the World',
        icon: svgComponents['GamepadIcon'],
        iconSlideTo: 'bottom',
        disabled: true,
      },
    ],
  },
  {
    title: '',
    height: '30%',
    items: [
      {
        key: PROFILE,
        title: 'Profile',
        description: 'See and configure your profile settings',
        icon: svgComponents['DeveloperIcon'],
        iconSlideTo: 'right',
        disabled: true,
      },
      {
        key: SETTINGS,
        title: 'Settings',
        description: 'See and configure game settings',
        icon: svgComponents['GameDevelopmentIcon'],
        iconSlideTo: 'right',
        disabled: true,
      },
    ],
  },
];

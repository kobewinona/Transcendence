// noinspection JSFileReferences
import svgComponents from 'assets/svgComponents.js';

import { QuickStart } from '../components';

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
        content: QuickStart,
        icon: svgComponents['GameIcon'],
        iconSlideTo: 'bottom',
        disabled: false,
      },
      {
        key: NEW_GAME,
        title: 'New Game',
        description: 'Set up and start a new game',
        content: 'some content here',
        icon: svgComponents['GameConsoleIcon'],
        iconSlideTo: 'bottom',
        disabled: false,
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
    height: '30%',
    items: [
      {
        key: PROFILE,
        title: 'Profile',
        description: 'See and configure your profile settings',
        icon: svgComponents['DeveloperIcon'],
        iconSlideTo: 'right',
        disabled: false,
      },
      {
        key: SETTINGS,
        title: 'Settings',
        description: 'See and configure game settings',
        content: 'settings here...',
        icon: svgComponents['GameDevelopmentIcon'],
        iconSlideTo: 'right',
        disabled: false,
      },
    ],
  },
];

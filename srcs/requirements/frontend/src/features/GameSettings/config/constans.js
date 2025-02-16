import { BallSkin, Controllers } from '../components';

export const DEFAULT_GAME_SETTINGS_TABS = [
  { value: 'sides', label: 'game_settings.tabs.sides.title' },
  { value: 'gameplay', label: 'game_settings.tabs.gameplay.title' },
  { value: 'ball_skin', label: 'game_settings.tabs.ball_skin.title' },
];

export const GAME_SETTINGS_TABS_COMPONENTS = [
  {
    key: 'sides',
    title: 'game_settings.tabs.sides.title',
    component: Controllers,
  },
  {
    key: 'ball_skin',
    title: 'game_settings.tabs.ball_skin.title',
    component: BallSkin,
  },
];

import { BallSkin, Controllers, Game } from '../components';

export const DEFAULT_GAME_SETTINGS_TABS = [
  { value: 'sides', label: 'game_settings.tabs.sides.title' },
  { value: 'game', label: 'game_settings.tabs.game.title' },
  { value: 'ball_skin', label: 'game_settings.tabs.ball_skin.title' },
];

export const GAME_SETTINGS_TABS_COMPONENTS = [
  {
    key: 'sides',
    component: Controllers,
  },
  {
    key: 'game',
    component: Game,
  },
  {
    key: 'ball_skin',
    component: BallSkin,
  },
];

import { MenuLoader } from 'components';
import { NewGame, Profile, QuickStart, Settings, Tournaments } from 'features';
import { Congratulations } from 'features/Tournaments/components/CurrentTournament/components';
import { svgComponents } from 'shared/lib';

export const MENU_LAYER_KEYS = {
  MAIN: 'key',
  QUICK_GAME: 'quick_game',
  NEW_GAME: 'new_game',
  TOURNAMENT: 'tournament',
  TOURNAMENT_CONGRATS: 'tournament_congrats',
  PROFILE: 'profile',
  SETTINGS: 'settings',
  LOADING: 'loading',
};

export const MENU_ICONS = {
  [MENU_LAYER_KEYS.QUICK_GAME]: svgComponents['LaunchIcon'],
  [MENU_LAYER_KEYS.NEW_GAME]: svgComponents['GameConsoleIcon'],
  [MENU_LAYER_KEYS.TOURNAMENT]: svgComponents['TournamentIcon'],
  [MENU_LAYER_KEYS.PROFILE]: svgComponents['DeveloperIcon'],
  [MENU_LAYER_KEYS.SETTINGS]: svgComponents['GameDevelopmentIcon'],
};

export const LOADING_LAYER = (layerKey) => ({
  key: MENU_LAYER_KEYS.LOADING,
  title: null,
  description: null,
  content: MenuLoader,
  icon: MENU_ICONS[layerKey],
});

export const QUICK_GAME_LAYER = () => ({
  key: MENU_LAYER_KEYS.QUICK_GAME,
  title: 'menu.items.item.quick_start.title',
  description: 'menu.items.item.quick_start.description',
  content: QuickStart,
  icon: MENU_ICONS[MENU_LAYER_KEYS.QUICK_GAME],
  iconSlideTo: 'bottom',
  ghost: true,
  loadingRequired: true,
  minPlayers: 1,
  maxPlayers: 1,
});

export const NEW_GAME_LAYER = () => ({
  key: MENU_LAYER_KEYS.NEW_GAME,
  title: 'menu.items.item.new_game.title',
  description: 'menu.items.item.new_game.description',
  content: NewGame,
  icon: MENU_ICONS[MENU_LAYER_KEYS.NEW_GAME],
  iconSlideTo: 'bottom',
  minPlayers: 1,
  maxPlayers: 6,
});

export const TOURNAMENT_LAYER = () => ({
  key: MENU_LAYER_KEYS.TOURNAMENT,
  title: 'menu.items.item.tournament.title',
  description: 'menu.items.item.tournament.description',
  content: Tournaments,
  icon: MENU_ICONS[MENU_LAYER_KEYS.TOURNAMENT],
  iconSlideTo: 'bottom',
  loadingRequired: true,
  minPlayers: 2,
  maxPlayers: null,
});

export const TOURNAMENT_CONGRATULATIONS_LAYER = (props = {}) => ({
  key: `${MENU_LAYER_KEYS.TOURNAMENT_CONGRATS}_${props?.tournament?.id}`,
  title: null,
  description: null,
  content: Congratulations,
  props,
  icon: MENU_ICONS[MENU_LAYER_KEYS.TOURNAMENT],
});

export const PROFILE_LAYER = () => ({
  key: MENU_LAYER_KEYS.PROFILE,
  title: 'menu.items.item.profile.title',
  description: 'menu.items.item.profile.description',
  content: Profile,
  icon: MENU_ICONS[MENU_LAYER_KEYS.PROFILE],
  iconSlideTo: 'right',
  loadingRequired: true,
});

export const SETTINGS_LAYER = () => ({
  key: MENU_LAYER_KEYS.SETTINGS,
  title: 'menu.items.item.settings.title',
  description: 'menu.items.item.settings.description',
  content: Settings,
  icon: MENU_ICONS[MENU_LAYER_KEYS.SETTINGS],
  iconSlideTo: 'right',
});

export const MENU_LAYERS = (props = {}) => ({
  [MENU_LAYER_KEYS.LOADING]: LOADING_LAYER(props),
  [MENU_LAYER_KEYS.QUICK_GAME]: QUICK_GAME_LAYER(props),
  [MENU_LAYER_KEYS.NEW_GAME]: NEW_GAME_LAYER(props),
  [MENU_LAYER_KEYS.TOURNAMENT]: TOURNAMENT_LAYER(props),
  [MENU_LAYER_KEYS.TOURNAMENT_CONGRATS]: TOURNAMENT_CONGRATULATIONS_LAYER(props),
  [MENU_LAYER_KEYS.PROFILE]: PROFILE_LAYER(props),
  [MENU_LAYER_KEYS.SETTINGS]: SETTINGS_LAYER(props),
});

export const MENU_ITEMS = () => [
  { height: '70%', items: [QUICK_GAME_LAYER(), NEW_GAME_LAYER(), TOURNAMENT_LAYER()] },
  { height: '30%', items: [PROFILE_LAYER(), SETTINGS_LAYER()] },
];

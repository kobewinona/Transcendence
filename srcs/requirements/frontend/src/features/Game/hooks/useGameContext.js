import { useContext } from 'react';

import GameContext from '../context/GameContext';

export const useGameContext = () => useContext(GameContext);

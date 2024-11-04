import React, { useMemo, useState } from 'react';

import GameContext from '../../context/GameContext';

function TableContextProvider({ children }) {
  const [playerScore, setPlayerScore] = useState(0);
  const [opponentScore, setOpponentScore] = useState(0);

  const incrementPlayerScore = () => {
    setPlayerScore((prevState) => prevState + 1);
  };

  const incrementOpponentScore = () => {
    setOpponentScore((prevState) => prevState + 1);
  };

  const value = useMemo(
    () => ({
      playerScore,
      opponentScore,
      incrementPlayerScore,
      incrementOpponentScore,
    }),
    [playerScore, opponentScore, incrementPlayerScore, incrementOpponentScore],
  );

  return <GameContext.Provider value={value}>{children}</GameContext.Provider>;
}

export default TableContextProvider;

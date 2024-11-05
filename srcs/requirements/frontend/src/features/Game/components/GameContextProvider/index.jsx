import React, { useMemo, useState } from 'react';

import GameContext from '../../context/GameContext';

function TableContextProvider({ children }) {
  const [playerScore, setPlayerScore] = useState(0);
  const [opponentScore, setOpponentScore] = useState(0);

  const [leftPaddlePosition, setLeftPaddlePosition] = useState(50);
  const [rightPaddlePosition, setRightPaddlePosition] = useState(50);

  const incrementPlayerScore = () => {
    setPlayerScore((prevState) => prevState + 1);
  };

  const incrementOpponentScore = () => {
    setOpponentScore((prevState) => prevState + 1);
  };

  const updatePaddlePosition = ({ lowerBoundary, upperBoundary, currentSpeed, side }) => {
    if (side === 'left') {
      setLeftPaddlePosition((prevPosition) =>
        Math.min(lowerBoundary, Math.max(upperBoundary, prevPosition + currentSpeed)),
      );
    }

    if (side === 'right') {
      setRightPaddlePosition((prevPosition) =>
        Math.min(lowerBoundary, Math.max(upperBoundary, prevPosition + currentSpeed)),
      );
    }
  };

  const resetPaddlesPosition = () => {
    setLeftPaddlePosition(50);
    setRightPaddlePosition(50);
  };

  const value = useMemo(
    () => ({
      playerScore,
      opponentScore,
      leftPaddlePosition,
      rightPaddlePosition,
      incrementPlayerScore,
      incrementOpponentScore,
      updatePaddlePosition,
      resetPaddlesPosition,
    }),
    [
      playerScore,
      opponentScore,
      leftPaddlePosition,
      rightPaddlePosition,
      incrementPlayerScore,
      incrementOpponentScore,
      updatePaddlePosition,
      resetPaddlesPosition,
    ],
  );

  return <GameContext.Provider value={value}>{children}</GameContext.Provider>;
}

export default TableContextProvider;

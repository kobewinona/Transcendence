import classNames from 'classnames/bind';
import { useGameContext } from 'features/Game/hooks/useGameContext';
import React from 'react';

import { ScoreCard } from './components';
import styles from './styles.module.css';

const cx = classNames.bind(styles);

function ScoreBoard() {
  const { playerScore, opponentScore } = useGameContext();
  const formatScore = (value) => String(value).padStart(2, '0');

  return (
    <div className={cx('scoreboard')}>
      <div className={cx('scoreboard__cards')}>
        <ScoreCard digit={formatScore(playerScore)[0]} />
        <ScoreCard digit={formatScore(playerScore)[1]} />
      </div>
      <span className={cx('colon')}> : </span>
      <div className={cx('scoreboard__cards')}>
        <ScoreCard digit={formatScore(opponentScore)[0]} />
        <ScoreCard digit={formatScore(opponentScore)[1]} />
      </div>
    </div>
  );
}

export default ScoreBoard;

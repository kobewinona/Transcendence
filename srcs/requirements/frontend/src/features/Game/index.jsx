import classNames from 'classnames/bind';
import ScoreBoard from 'features/Game/components/ScoreBoard';
import React from 'react';

import { AdminControls, GameContextProvider } from './components';
import styles from './styles.module.css';

const cx = classNames.bind(styles);

function Game() {
  return (
    <GameContextProvider>
      <section className={cx('layout')}>
        <AdminControls />
        <div className={cx('game-container')}>
          <ScoreBoard />
        </div>
      </section>
    </GameContextProvider>
  );
}

export default Game;

import classNames from 'classnames/bind';
import ScoreBoard from 'features/Game/components/ScoreBoard';
import React, { useEffect, useRef, useState } from 'react';

import { AdminControls, Ball, GameContextProvider, Paddle } from './components';
import styles from './styles.module.css';

const cx = classNames.bind(styles);

function Game() {
  const containerRef = useRef(null);
  const leftPaddleRef = useRef(null);
  const rightPaddleRef = useRef(null);

  const [gameStarted, setGameStarted] = useState(false);

  // Start the game after a timeout of 1000ms or on space press
  useEffect(() => {
    // Timeout to start the game after 1000ms
    const timeoutId = setTimeout(() => {
      setGameStarted(true);
    }, 1000);

    // Event listener for spacebar press
    const handleKeyDown = (event) => {
      if (event.code === 'Space') {
        setGameStarted(true);
        clearTimeout(timeoutId); // Clear timeout if space is pressed
      }
    };

    window.addEventListener('keydown', handleKeyDown);

    // Cleanup event listener and timeout
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      clearTimeout(timeoutId);
    };
  }, []);

  return (
    <GameContextProvider>
      <section className={cx('layout')}>
        <AdminControls />
        <div ref={containerRef} className={cx('game-container')}>
          <ScoreBoard />
          {gameStarted && (
            <>
              <Paddle ref={leftPaddleRef} containerRef={containerRef} side="left" />
              <Paddle ref={rightPaddleRef} containerRef={containerRef} side="right" />
              <Ball containerRef={containerRef} leftPaddleRef={leftPaddleRef} rightPaddleRef={rightPaddleRef} />
            </>
          )}
        </div>
      </section>
    </GameContextProvider>
  );
}

export default Game;

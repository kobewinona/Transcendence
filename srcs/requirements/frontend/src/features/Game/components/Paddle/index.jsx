import classNames from 'classnames/bind';
import { useGameContext } from 'features/Game/hooks/useGameContext';
import React, { forwardRef, useEffect, useRef } from 'react';

import { ACCELERATION_FACTOR, DEACCELERATION_FACTOR, MAX_SPEED, PADDLE_HEIGHT } from '../../config/constants';
import styles from './styles.module.css';

const cx = classNames.bind(styles);

const Paddle = forwardRef(({ containerRef, side }, ref) => {
  const { leftPaddlePosition, rightPaddlePosition, updatePaddlePosition } = useGameContext();
  const speed = useRef(0);
  const direction = useRef(0);
  const upperBoundary = useRef(0);
  const lowerBoundary = useRef(100);

  useEffect(() => {
    if (containerRef.current) {
      const containerHeight = containerRef.current.clientHeight;
      upperBoundary.current = (PADDLE_HEIGHT / 2 / containerHeight) * 100 + 0.2;
      lowerBoundary.current = 100 - upperBoundary.current - 0.2;
    }
  }, [containerRef]);

  useEffect(() => {
    // Event listeners for key presses
    const handleKeyDown = (event) => {
      if ((side === 'left' && event.code === 'KeyW') || (side === 'right' && event.code === 'ArrowUp')) {
        direction.current = -1;
      } else if ((side === 'left' && event.code === 'KeyS') || (side === 'right' && event.code === 'ArrowDown')) {
        direction.current = 1;
      }
    };

    const handleKeyUp = (event) => {
      if (
        (side === 'left' && (event.code === 'KeyW' || event.code === 'KeyS')) ||
        (side === 'right' && (event.code === 'ArrowUp' || event.code === 'ArrowDown'))
      ) {
        direction.current = 0; // Stop moving
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    // Clean up event listeners on component unmount
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, [side]);

  useEffect(() => {
    const move = () => {
      if (direction.current !== 0) {
        speed.current = Math.min(Math.abs(speed.current) + ACCELERATION_FACTOR, MAX_SPEED) * direction.current;
      } else if (speed.current > 0) {
        speed.current = Math.max(speed.current - DEACCELERATION_FACTOR, 0);
      } else if (speed.current < 0) {
        speed.current = Math.min(speed.current + DEACCELERATION_FACTOR, 0);
      }

      // Update position based on calculated boundaries
      updatePaddlePosition({
        lowerBoundary: lowerBoundary.current,
        upperBoundary: upperBoundary.current,
        currentSpeed: speed.current,
        side,
      });

      requestAnimationFrame(move);
    };

    const animationId = requestAnimationFrame(move);

    return () => cancelAnimationFrame(animationId);
  }, []);

  return (
    <div
      ref={ref}
      className={cx('racket', `racket_${side}`)}
      style={{ top: `${side === 'left' ? leftPaddlePosition : rightPaddlePosition}%` }}
    />
  );
});

Paddle.displayName = 'Paddle';
export default Paddle;

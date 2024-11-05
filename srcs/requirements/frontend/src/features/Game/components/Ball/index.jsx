import classNames from 'classnames/bind';
import { useGameContext } from 'features/Game/hooks/useGameContext';
import React, { useEffect, useRef, useState } from 'react';

import {
  ANGLE_FACTOR,
  BALL_DIAMETER,
  MAX_BALL_SPEED,
  MAX_VELOCITY,
  MIN_BALL_SPEED,
  RESET_DELAY,
} from '../../config/constants';
import styles from './styles.module.css';

const cx = classNames.bind(styles);

function Ball({ containerRef, leftPaddleRef, rightPaddleRef }) {
  const { incrementPlayerScore, incrementOpponentScore, resetPaddlesPosition } = useGameContext();
  const [containerWidth, setContainerWidth] = useState(0);
  const [containerHeight, setContainerHeight] = useState(0);
  const [position, setPosition] = useState({ x: 50, y: 50 });
  const [currentSpeed, setCurrentSpeed] = useState(MIN_BALL_SPEED);
  const ballDiameterPercent = (BALL_DIAMETER / containerWidth) * 100 * 2;
  const velocity = useRef({
    x: Math.random() < 0.5 ? -0.1 : 0.1,
    y: 0,
  });
  const resetTimeoutRef = useRef(null);

  const reset = (speedAtReset) => {
    velocity.current = { x: 0, y: 0 };

    if (speedAtReset > MIN_BALL_SPEED) {
      setCurrentSpeed((prevState) => {
        const newSpeed = prevState / 1.5;
        if (newSpeed > MIN_BALL_SPEED) {
          return newSpeed;
        }
        return prevState;
      });
    }

    if (resetTimeoutRef.current) clearTimeout(resetTimeoutRef.current);

    resetTimeoutRef.current = setTimeout(() => {
      velocity.current = {
        x: Math.random() < 0.5 ? -0.1 : 0.1,
        y: 0,
      };
      setPosition({ x: 50, y: 50 });
      resetPaddlesPosition();
    }, RESET_DELAY);
  };

  const updateSpeed = () => {
    setCurrentSpeed((prevState) => Math.min(prevState + 0.4, MAX_BALL_SPEED));
  };

  const adjustDirectionOnPaddleHit = (paddleTopPercent, paddleBottomPercent, newY) => {
    const impactPoint = (newY - paddleTopPercent) / (paddleBottomPercent - paddleTopPercent) - 0.5;
    velocity.current.y = Math.max(-MAX_VELOCITY, Math.min(MAX_VELOCITY, ANGLE_FACTOR * impactPoint));
  };

  // Set container width on mount
  useEffect(() => {
    if (containerRef?.current) {
      const containerRect = containerRef.current.getBoundingClientRect();
      setContainerWidth(containerRect.width);
      setContainerHeight(containerRect.height);
    }
  }, [containerRef]);

  useEffect(() => {
    let animationFrameId;

    const updatePosition = () => {
      // Get paddle positions in percentage terms
      const leftPaddle = leftPaddleRef?.current?.getBoundingClientRect();
      const rightPaddle = rightPaddleRef?.current?.getBoundingClientRect();
      const container = containerRef?.current?.getBoundingClientRect();

      if (leftPaddle && rightPaddle && container) {
        // Convert paddles' top and bottom positions to percentages
        const leftPaddleTopPercent = ((leftPaddle.top - container.top) / container.height) * 100;
        const leftPaddleBottomPercent = ((leftPaddle.bottom - container.top) / container.height) * 100;
        const rightPaddleTopPercent = ((rightPaddle.top - container.top) / container.height) * 100;
        const rightPaddleBottomPercent = ((rightPaddle.bottom - container.top) / container.height) * 100;
        const rightPaddleLeftPercent = ((rightPaddle.left - container.left) / container.width) * 100;
        const leftPaddleRightPercent = ((leftPaddle.right - container.left) / container.width) * 100;

        setPosition((prevPosition) => {
          let newX = prevPosition.x + velocity.current.x * currentSpeed;
          const newY = prevPosition.y + velocity.current.y * currentSpeed;

          // Boundary percentages for the container
          const topBoundary = 0;
          const rightBoundary = 100 - (BALL_DIAMETER / containerWidth) * 100 + ballDiameterPercent;
          const bottomBoundary = 100 - (BALL_DIAMETER / containerHeight) * 100;
          const leftBoundary = 0 - ballDiameterPercent;

          // Collision with top and bottom boundaries
          if (newY <= topBoundary || newY >= bottomBoundary) {
            velocity.current.y *= -1;
          } else if (newX <= leftBoundary || newX >= rightBoundary) {
            velocity.current.x *= -1;
          }

          if (newX <= leftBoundary || newX >= rightBoundary) {
            if (newX <= leftBoundary) incrementOpponentScore();
            if (newX >= rightBoundary) incrementPlayerScore();
            reset(currentSpeed);
            return { x: 50, y: 50 };
          }

          // Collision with left paddle
          if (
            velocity.current.x < 0 &&
            newX <= leftPaddleRightPercent &&
            newY + (BALL_DIAMETER / containerHeight) * 100 >= leftPaddleTopPercent &&
            newY <= leftPaddleBottomPercent
          ) {
            newX = leftPaddleRightPercent;
            velocity.current.x *= -1;
            adjustDirectionOnPaddleHit(leftPaddleTopPercent, leftPaddleBottomPercent, newY);
            updateSpeed();
          }

          // Collision with right paddle
          if (
            velocity.current.x > 0 &&
            newX + (BALL_DIAMETER / containerWidth) * 100 >= rightPaddleLeftPercent &&
            newY + (BALL_DIAMETER / containerHeight) * 100 >= rightPaddleTopPercent &&
            newY <= rightPaddleBottomPercent
          ) {
            newX = rightPaddleLeftPercent - (BALL_DIAMETER / containerWidth) * 100;
            velocity.current.x *= -1;
            adjustDirectionOnPaddleHit(rightPaddleTopPercent, rightPaddleBottomPercent, newY);
            updateSpeed();
          }

          return { x: newX, y: newY };
        });

        animationFrameId = requestAnimationFrame(updatePosition);
      }
    };

    animationFrameId = requestAnimationFrame(updatePosition);

    return () => cancelAnimationFrame(animationFrameId);
  }, [containerWidth, containerHeight, leftPaddleRef, rightPaddleRef, currentSpeed]);

  // Clean up timeout on component unmount
  useEffect(() => {
    return () => {
      if (resetTimeoutRef.current) clearTimeout(resetTimeoutRef.current);
    };
  }, []);

  return (
    <div
      className={cx('ball')}
      style={{
        width: `${BALL_DIAMETER}px`,
        height: `${BALL_DIAMETER}px`,
        left: `${position.x}%`,
        top: `${position.y}%`,
      }}
    />
  );
}

export default Ball;

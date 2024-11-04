import classNames from 'classnames/bind';
import React, { useEffect, useState } from 'react';

import styles from './styles.module.css';

const cx = classNames.bind(styles);

function ScoreCard({ digit }) {
  const [displayedScore, setDisplayedScore] = useState(digit);
  const [animationClass, setAnimationClass] = useState('');
  let flipInTimer = null;
  let flipOutTimer = null;

  useEffect(() => {
    if (digit !== displayedScore) {
      setAnimationClass('flip-out');
      flipOutTimer = setTimeout(() => {
        setDisplayedScore(digit);
        setAnimationClass('flip-in');

        flipInTimer = setTimeout(() => {
          setAnimationClass('');
        }, 300);
      }, 300);
    }
  }, [digit, displayedScore]);

  useEffect(() => {
    return () => {
      clearTimeout(flipInTimer);
      clearTimeout(flipOutTimer);
    };
  }, []);

  return <span className={cx('score', animationClass)}>{displayedScore}</span>;
}

export default ScoreCard;

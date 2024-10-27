import classNames from 'classnames/bind';
import { Button } from 'components/shared';
import Menu from 'features/Menu';
import React, { useState } from 'react';

import styles from './styles.module.css';

const cx = classNames.bind(styles);

function TitleScreen() {
  const [isMenuHovered, setIsMenuHovered] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleMouseEnter = () => {
    setIsMenuHovered(true);
  };

  const handleMouseLeave = () => {
    setIsMenuHovered(false);
  };

  const openMenu = () => {
    setIsMenuOpen(true);
  };

  return (
    <div className={cx('layout')}>
      <div className={cx('ball', { ball_up: isMenuOpen })} />
      <div
        className={cx('ball-overlay', { 'ball-overlay_half-down': isMenuHovered, 'ball-overlay_down': isMenuOpen })}
      />
      <div
        className={cx('controls-container')}
        role="presentation"
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
      >
        <Button className={cx('start-button', { hidden: isMenuOpen })} text="Start" onClick={openMenu} />
        <div className={cx('menu-container')}>
          <Menu isMenuOpen={isMenuOpen} />
        </div>
      </div>
    </div>
  );
}

export default TitleScreen;

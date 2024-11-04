import classNames from 'classnames/bind';
import { Button } from 'components/shared';
import React from 'react';
import { Link } from 'react-router-dom';

import styles from './styles.module.css';

const cx = classNames.bind(styles);

function Menu({ isMenuOpen }) {
  return (
    <ul className={`${cx('menu', { hidden: !isMenuOpen })} grow`}>
      <li>
        <Button text="Profile" />
      </li>
      <li>
        <Link className={cx('link')} to="pong-offline">
          Play Offline
        </Link>
      </li>
      <li>
        <Button text="Play Online" />
      </li>
      <li>
        <Button text="Settings" />
      </li>
    </ul>
  );
}

export default Menu;

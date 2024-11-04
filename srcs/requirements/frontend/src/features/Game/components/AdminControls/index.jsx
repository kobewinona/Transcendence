import classNames from 'classnames/bind';
import { useGameContext } from 'features/Game/hooks/useGameContext';
import React from 'react';

import styles from './styles.module.css';

const cx = classNames.bind(styles);

function AdminControls() {
  const { incrementPlayerScore, incrementOpponentScore } = useGameContext();

  return (
    <div className={cx('admin-controls')}>
      <p>
        {`increment player score `}
        <button onClick={incrementPlayerScore}>⌃</button>
      </p>
      <p>
        {`increment opponent score `}
        <button onClick={incrementOpponentScore}>⌃</button>
      </p>
    </div>
  );
}

export default AdminControls;

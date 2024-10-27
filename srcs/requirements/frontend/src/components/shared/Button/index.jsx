import classNames from 'classnames/bind';
import React from 'react';

import styles from './styles.module.css';

const cx = classNames.bind(styles);

function Button({ className, type, text, onClick = () => {} }) {
  return (
    <button className={cx(className, 'button')} type={type} onClick={onClick}>
      {text || ''}
    </button>
  );
}

export default Button;

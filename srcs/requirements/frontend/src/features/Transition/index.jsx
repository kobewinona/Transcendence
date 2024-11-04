import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';

function Transition({ children }) {
  const location = useLocation();
  const [displayChildren, setDisplayChildren] = useState(children);
  const [fadeClass, setFadeClass] = useState('fade-in');

  useEffect(() => {
    setFadeClass('shrink');
    const timer = setTimeout(() => {
      setDisplayChildren(children);
      setFadeClass('grow');
    }, 300);

    return () => clearTimeout(timer);
  }, [children, location]);

  return <div className={fadeClass}>{displayChildren}</div>;
}

export default Transition;

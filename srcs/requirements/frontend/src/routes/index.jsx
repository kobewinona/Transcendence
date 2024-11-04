import { Game, TitleScreen, Transition } from 'features';
import React from 'react';
import { Route, Routes, useLocation } from 'react-router-dom';

function AppRoutes() {
  const location = useLocation();

  // handle not logged-in user routes (sign up, sign in) here

  return (
    <Transition>
      <Routes location={location}>
        <Route path="/" element={<TitleScreen />} />
        <Route path="/pong-offline" element={<Game />} />
      </Routes>
    </Transition>
  );
}

export default AppRoutes;

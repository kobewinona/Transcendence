import { menu } from './menu.js';

export const auth = {
  isAuthorized: Boolean(localStorage.getItem('access_token')),
  login(token) {
    localStorage.setItem('access_token', token);
    this.isAuthorized = true;
  },
  logout() {
    menu.reset();
    localStorage.removeItem('access_token');
    this.isAuthorized = false;
  },
};

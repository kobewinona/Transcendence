export const auth = {
  isAuthorized: Boolean(localStorage.getItem('access_token')),
  login(token) {
    localStorage.setItem('access_token', token);
    this.isAuthorized = true;
  },
  logout() {
    localStorage.removeItem('access_token');
    this.isAuthorized = false;
  },
};

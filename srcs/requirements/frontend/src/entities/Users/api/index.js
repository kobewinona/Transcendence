import api from 'api';

export default {
  getUserInfo() {
    return api.get('users/me');
  },
};

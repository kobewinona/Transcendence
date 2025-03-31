import api from 'api';

export default {
  getUserInfo({ params }) {
    return api.get('users/me', { params });
  },
};

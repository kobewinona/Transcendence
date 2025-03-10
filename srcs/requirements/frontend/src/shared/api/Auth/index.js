import api from 'api';

export default {
  signUp({ data }) {
    return api.post('signup/', data);
  },
  getOtp({ data }) {
    return api.post('otp/', data);
  },
  signIn({ data }) {
    return api.post('signin/', data);
  },
  refreshTokens() {
    return api.post('refresh_tokens/', {}, { withCredentials: true });
  },
  signOut() {
    return api.post('signout/', {}, { withCredentials: true });
  },
};

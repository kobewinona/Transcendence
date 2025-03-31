import api from 'api';

export default {
  getTournaments({ params }) {
    return api.get('tournaments/', { params });
  },
  createTournament({ data }) {
    return api.post('tournaments/', data);
  },
  updateTournament({ data }) {
    return api.patch('tournaments/', data);
  },
};

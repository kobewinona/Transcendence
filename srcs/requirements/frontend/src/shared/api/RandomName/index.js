import axios from 'axios';

export default {
  getRandomUser() {
    return axios.get('https://api.api-ninjas.com/v1/randomuser', {
      headers: {
        'X-Api-Key': import.meta.env.VITE_RANDOM_NAME_API_KEY,
      },
    });
  },
};

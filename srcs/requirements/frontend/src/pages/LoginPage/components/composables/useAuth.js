import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
const route = useRoute();

export function useAuth() {
  const router = useRouter()
  const loading = ref(false)
  const errors = ref([])


  const handleRegularLogin = async (name, password, rememberMe) => {
    loading.value = true
    errors.value = []

    try {
      const response = await axios.post('/api/login/', {
        name,
        password,
        remember_me: rememberMe
      })

      if (response.data?.access) {
        // Store token in localStorage
        localStorage.setItem('token', response.data.access)
        localStorage.setItem('isAuthenticated', 'true')
        
        axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`
        
        router.push('/game')
      } else {
        errors.value.push('Authentication failed. Please try again.')
      }
    } catch (error) {
      handleError(error)
    } finally {
      loading.value = false
    }
  }

  const handleOAuthLogin = () => {
      console.log("OAuth login button clicked!"); 
      const clientId = 'u-s4t2ud-c691b276ef7aa2660fa1d1be08026efd0282c75fdb314fb7307fdcfd7f61d6ce'; //should take from backend
      const redirectUri = 'https://localhost/game';
      const authUrl = `https://api.intra.42.fr/oauth/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=code&scope=public`;
      console.log(authUrl);
      window.location.href = authUrl;
    // Once the the request approved, the OAuth provider will redirect usr back to specified 
    // redirect_uri along with an authorization code.
  }

  const handleOAuthCallback = async () => {
    const code = route.query.code;
  if (!code) {
    console.error("No OAuth code found in URL!");
    return;
  }

  console.log("OAuth code received:", code); // Debugging
  const backendURL = `/api/oauth/oauth_42/?code=${code}`;
  console.log("Sending request to backend:", backendURL); // Debugging

    try {
      // when the user approves application
      // oAuth will provide code

      //The function makes an httpget request to backend endpoint
      // including the received code as a query parameter.
      //and exchanging the Code for an Access Token:
      const response = await axios.get(`api/oauth/oauth_42/?code=${code}`)

      
      if (response.data?.access) {//if contains 
        //should get rid of the localstorage
        localStorage.setItem('token', response.data.access)
        localStorage.setItem('isAuthenticated', 'true')
        
        // configuring Axios to include the access token in the Authorization
        //  header for all future HTTP requests
        axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`
        
        router.push('/game')
      } else {
        errors.value.push('OAuth authentication failed. Please try again.')
      }
    } catch (error) {
      handleError(error)
    }
  }

  const logout = async () => {
    try {
      await axios.post('/api/logout/')
      // Clear localStorage
      localStorage.removeItem('token')
      localStorage.removeItem('isAuthenticated')
      // Clear axios header
      delete axios.defaults.headers.common['Authorization']
      router.push('/login')
    } catch (error) {
      handleError(error)
    }
  }

  const handleError = (error) => {
    if (error.response?.data?.error) {
      errors.value.push(error.response.data.error)
    } else if (error.response?.data?.message) {
      errors.value.push(error.response.data.message)
    } else if (!navigator.onLine) {
      errors.value.push('Please check your internet connection.')
    } else {
      errors.value.push('An unexpected error occurred. Please try again.')
    }
  }

  // checking for the token in localStorage in case of refresh
  const initializeAuth = () => {
    const token = localStorage.getItem('token')
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    }
  }

  // Call if composable created
  initializeAuth()

  return {
    loading,
    errors,
    handleRegularLogin,
    handleOAuthLogin,
    handleOAuthCallback,
    logout
  }
}
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export function useAuth() {
  const router = useRouter()
  const loading = ref(false)
  const errors = ref([])

  const handleRegularLogin = async (email, password, rememberMe) => {
    loading.value = true
    errors.value = []

    try {
      const response = await axios.post('/api/login/', {
        email,
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
    const OAUTH_CONFIG = {
      clientId: import.meta.env.CLIENT_ID || `u-s4t2ud-c691b276ef7aa2660fa1d1be08026efd0282c75fdb314fb7307fdcfd7f61d6ce`,
      redirectUri: encodeURIComponent(import.meta.env.REDIRECT_URI || 'http://localhost/game'),
      apiUrl: 'https://api.intra.42.fr/oauth/authorize'
    }

    const queryParams = new URLSearchParams({
      client_id: OAUTH_CONFIG.clientId,
      redirect_uri: OAUTH_CONFIG.redirectUri,
      response_type: 'code',
      scope: 'public'
    })

    window.location.href = `${OAUTH_CONFIG.apiUrl}?${queryParams.toString()}`
  }

  const handleOAuthCallback = async (code) => {
    try {
      const response = await axios.get(`/oauth/callback?code=${code}`)
      
      if (response.data?.access) {
        // Store token in localStorage
        localStorage.setItem('token', response.data.access)
        localStorage.setItem('isAuthenticated', 'true')
        
        // Set axios default header
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

  // Initialize axios if token exists
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
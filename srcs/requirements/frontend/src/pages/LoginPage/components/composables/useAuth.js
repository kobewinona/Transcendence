import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
const route = useRoute();

export function useAuth() {
  const router = useRouter()
  const loading = ref(false)
  const errors = ref([])

  const sendOTP = async (username, password) =>{
    loading.value = true
    errors.value = []
    try {
      const otpData = { username, password };
      const tokenResponse = await axios.post('/api/token/', otpData, {
        username,
        password,
      })
      if (tokenResponse.status >= 200 && tokenResponse.status < 300){
        const tokenData = tokenResponse.data;
      const responseOTP = await axios.post('api/get-otp/', otpData,
      {
          headers: {
            'Authorization' : `Bearer ${tokenData.access}`,
          },
          withCredentials: true,// Include cookies if needed
      });
        if (responseOTP.status >= 200 && responseOTP.status < 300) {
          console.log('OTP Response:', responseOTP.data);
        } else {
          console.error('Failed to send OTP:', responseOTP.statusText);
        }
        return true;
      } else {
        console.error('Failed to get token:', tokenResponse.statusText);
        return false;
      }
    } catch (error) {
      if (error.response) {
        console.error('Error Response:', error.response.data);
      } else if (error.request) {
        console.error('No response received:', error.request);
      } else {
        console.error('Error:', error.message);
      }
    }
  }

  const checkOTP = async(username, password, otp) => {
      try{
        const respone =  await axios.post('/api/token/', {
            username,
            password,
            otp
        })
        if (respone.status >= 200 && respone.status < 300 ){
            const otpData = { username, otp };
            const tokenData = tokenResponse.data;

            const responseOtp = await axios.post('/api/verify-otp/', otpData, 
              {
                headers: {
                  'Authorization' : `Bearer ${tokenData.access}`,
                },
                withCredentials: true,// Include cookies if needed
            });
            if (responseOtp.status >= 200 && responseOtp.status < 300 ) {
              const errorText = await responseOtp.text();
              setError("wrong otp. try again");
              console.log(errorText)
            } else {
              setError('')
              setToken(tokenData)
              console.log('JWT is set');
              router.push('/game')
            }
          } else {
          setError("wrong credentials (checking otp)");
        }
      }
      catch (error) {
        console.error('wrong credentials (checking otp):', error);
      }
  }

  const handleOAuthLogin = () => {
      console.log("OAuth login button clicked!"); 
      const clientId = 'u-s4t2ud-c691b276ef7aa2660fa1d1be08026efd0282c75fdb314fb7307fdcfd7f61d6ce'; //should take from backend
      const redirectUri = 'http://localhost:8000/oauth/redirect/';
      const authUrl = `https://api.intra.42.fr/oauth/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=code&scope=public`;
      console.log(authUrl);
      window.location.href = authUrl;
    // Once the the request approved, the OAuth provider will redirect usr back to specified 
    // redirect_uri along with an authorization code.
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
    // tokenData,
    sendOTP,
    checkOTP,
    handleOAuthLogin,
    logout
  }
}

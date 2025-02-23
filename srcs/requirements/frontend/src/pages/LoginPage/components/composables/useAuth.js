import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { setToken, unsetToken, getToken, getTokenPayload } from '@/components/tokenUtils';
const route = useRoute();

export function useAuth() {
  const router = useRouter()
  const loading = ref(false)
  const errors = ref([])

  const sendOTP = async (username, password) =>{
    loading.value = true
    errors.value = []
    if (!username || !password) {
      errors.value.push('Both username and password fields must be filled.');
      loading.value = false;
      return false;
    }
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
          errors.value.push('Failed to send OTP');
        }
        return true;
      } else {
        console.error('Failed to get token:', tokenResponse.statusText);
        errors.value.push('Failed to get token');
        return false;
      }
    } catch (error) {
      handleError(error)
    }
  }
  const handleError = (error) => {
    if (error.response) {
      // Handle specific status codes
      if (error.response.status === 401) {
        // Unauthorized access
        errors.value.push('No such user or invalid credentials.')
        loading.value = false;
        return false;
      } else if (error.response.data?.error) {
        errors.value.push(error.response.data.error)
        loading.value = false;
      } else if (error.response.data?.message) {
        errors.value.push(error.response.data.message)
        loading.value = false;
      } else {
        errors.value.push('An unexpected error occurred. Please try again.')
        loading.value = false;
      }
    } else if (error.request) {
      // No response received
      errors.value.push('No response received from the server.')
      loading.value = false;
      return false;
    } else {
      // Other errors
      errors.value.push('An unexpected error occurred. Please try again.')
      loading.value = false;
      return false;
    }
  }
  const checkOTP = async(username, password, otp) => {
    console.log('check OTP');
      try{
          const tokenResponse =  await axios.post('/api/token/', {
            username,
            password,
            otp
        })
        console.log('before cheing status', tokenResponse.status);
        if (tokenResponse.status >= 200 && tokenResponse.status < 300 ){

            const otpData = { username, otp };
            console.log(otpData);
            const tokenData = tokenResponse.data;
            console.log('JWT is set');
            const responseOtp = await axios.post('/api/verify-otp/', otpData, 
              {
                headers: {
                  'Authorization' : `Bearer ${tokenData.access}`,
                },
                withCredentials: true,// Include cookies if needed
            });
            if (responseOtp.status < 200 && responseOtp.status > 300 ) {
              const errorText = await responseOtp.text(); //wait for code error with promise
              console.log(errorText)
            } else {
              setToken(tokenData) // in components 
              console.log('JWT is set');
              router.push('/game')
            }
          } else {
            errors.value.push('Invalid OTP. Please try again.');
        }
      }
      catch (error) {
        console.error('wrong credentials (checking otp):', error);
        errors.value.push('Invalid OTP. Please try again.');
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
      unsetToken();
      router.push('/login');
    } catch (error) {
      handleError(error);
    }
  };

  return {
    loading,
    errors,
    sendOTP,
    checkOTP,
    handleOAuthLogin,
    logout
  }
}

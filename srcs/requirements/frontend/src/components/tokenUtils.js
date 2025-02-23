// import 
import Cookies from 'js-cookie';
import VueCookies from 'vue-cookies';
export const setToken = async (token) => {
	VueCookies.set('access_token', token.access)
	VueCookies.set('refresh_token', token.refresh)
};

export const unsetToken = async () => {

	VueCookies.remove('access_token')
	VueCookies.remove('refresh_token')
}

export const getToken = async () => {
	return VueCookies.get('access_token');
}

export const getTokenPayload = () => {
    const token = VueCookies.get('access_token');
    if (!token) return null;

    try {
        const [, payloadBase64] = token.split('.');
        const payloadJson = atob(payloadBase64);
        const payload = JSON.parse(payloadJson);
        return payload;
    } catch (error) {
        console.error('Error decoding token:', error);
        return null;
    }
};
export const isAuthenticated = () => {
    const payload = getTokenPayload();
    if (!payload) return false;
    const currentTime = Math.floor(Date.now() / 1000);
    return payload.exp > currentTime; // Check if the token is not expired
  };



//   import Cookies from 'js-cookie';
//   // Set tokens
// export const setToken = (token) => {
//     Cookies.set('access_token', token.access);
//     Cookies.set('refresh_token', token.refresh);
//   };
  
//   // Remove tokens
//   export const unsetToken = () => {
//     Cookies.remove('access_token');
//     Cookies.remove('refresh_token');
//   };
  
//   // Get access token
//   export const getToken = () => {
//     return Cookies.get('access_token');
// //   };
// export const getTokenPayload = () => {
//     const token = Cookies.get('access_token'); // Direct cookie access
//     if (!token) return null;
  
//     try {
//       // Split JWT into parts (header.payload.signature)
//       const [, payloadBase64] = token.split('.');
      
//       // Handle URL-safe base64 encoding (common in JWTs)
//       const decodedPayload = payloadBase64
//         .replace(/-/g, '+')
//         .replace(/_/g, '/');
      
//       // Decode and parse
//       const payloadJson = atob(decodedPayload);
//       return JSON.parse(payloadJson);
//     } catch (error) {
//       console.error('Error decoding token:', error);
//       return null;
//     }
//   };

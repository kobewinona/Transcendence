import './style.css'
import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import router from './router'
import VueCookies from 'vue-cookies';

//  set a base URL for axios:
// axios.defaults.baseURL = 'http://127.0.0.1:80'
const app = createApp(App)
app.use(VueCookies);
app.use(router)

// Make axios available globally (optional)
app.config.globalProperties.$axios = axios
app.config.globalProperties.$cookies.config('7d'); // Default expiration

app.mount('#app')
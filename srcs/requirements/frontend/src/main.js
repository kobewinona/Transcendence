import './style.css'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
// import { useAuthStore } from './store/auth'
import App from './App.vue'
import axios from 'axios' // http requests 
import router from './router'

// axios.defaults.baseURL = 'http://127.0.0.1:80' // automatically prepend URL to the request path.

const app = createApp(App)
app.use(createPinia())
app.use(router, axios)


// const authStore = useAuthStore()
// authStore.setCsrfToken()

app.mount('#app') // for DOM

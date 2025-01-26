import './style.css'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
// import { useAuthStore } from './store/auth'
import App from './App.vue'
import axios from 'axios'
import router from './router'

axios.defaults.baseURL = 'http://127.0.0.1:8000'

const app = createApp(App)
app.use(createPinia())
app.use(router, axios)


// const authStore = useAuthStore()
// authStore.setCsrfToken()

app.mount('#app')

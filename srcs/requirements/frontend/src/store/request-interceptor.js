import axios from 'axios'
import { useAuth } from './auth'

const axiosInstance = axios.create({
    baseURL: 'http://localhost:8000' // Your Django backend URL
})

axiosInstance.interceptors.request.use(async (config) => {
    const { state, refreshToken } = useAuth()
    
    if (state.user.access) {
        config.headers.Authorization = `Bearer ${state.user.access}`
    }
    return config
})

axiosInstance.interceptors.response.use(
    response => response,
    async (error) => {
        const originalRequest = error.config
        const { state, refreshToken } = useAuth()
        
        if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true
            try {
                const newAccess = await refreshToken()
                originalRequest.headers.Authorization = `Bearer ${newAccess}`
                return axiosInstance(originalRequest)
            } catch (refreshError) {
                return Promise.reject(refreshError)
            }
        }
        return Promise.reject(error)
    }
)

export default axiosInstance
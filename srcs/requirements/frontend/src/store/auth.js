import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import router from '@/router';

export const useAuthStore = defineStore('auth', () => {
  const authToken = ref(localStorage.getItem('authToken') || null);

  const isAuthenticated = computed(() => !!authToken.value);

  function login(token, remember = false) {
    authToken.value = token;
    const storage = remember ? localStorage : sessionStorage;
    storage.setItem('authToken', token);
  }

  function logout() {
    authToken.value = null;
    localStorage.removeItem('authToken');
    sessionStorage.removeItem('authToken');
    router.push('/');
  }

  return { authToken, isAuthenticated, login, logout };
});
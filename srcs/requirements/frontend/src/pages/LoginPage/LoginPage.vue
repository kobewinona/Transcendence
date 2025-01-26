<template>
  <div class="login">
    <img src="@/pages/LoginPage/components/img/login-bg.png" alt="background" class="login__bg" />

    <form class="login__form" @submit.prevent="handleSubmit">
      <h1 class="login__title">Login</h1>

      <div class="login__inputs">
        <div class="login__box">
          <input 
            type="email" 
            v-model="email" 
            placeholder="Email ID" 
            required 
            class="login__input" 
          />
          <i class="ri-mail-fill"></i>
        </div>

        <div class="login__box">
          <input 
            type="password" 
            v-model="password" 
            placeholder="Password" 
            required 
            class="login__input" 
          />
          <i class="ri-lock-2-fill"></i>
        </div>
      </div>

      <div v-if="errors.length" class="bg-red-300 text-white rounded-lg p-6 mb-4">
        <p v-for="(error, index) in errors" :key="index">{{ error }}</p>
      </div>

      <div class="login__check">
        <div class="login__check-box">
          <input 
            type="checkbox" 
            id="remember-me" 
            v-model="rememberMe" 
            class="login__check-input" 
          />
          <label for="remember-me" class="login__check-label">Remember me</label>
        </div>
        <router-link to="/forgot-password" class="login__forgot">Forgot Password?</router-link>
      </div>

      <button 
        type="submit" 
        class="login__button"
        :disabled="loading"
      >
        {{ loading ? 'Logging in...' : 'Login' }}
      </button>

      <div class="login__register">
        Don't have an account? <router-link to="/register">Register</router-link>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { useToastStore } from '@/store/toast';

const router = useRouter();
const toastStore = useToastStore();

const email = ref('');
const password = ref('');
const rememberMe = ref(false);
const errors = ref([]);
const loading = ref(false);

const validateForm = () => {
  errors.value = [];
  
  if (!email.value.trim()) {
    errors.value.push('Email is required');
  }
  
  if (!password.value) {
    errors.value.push('Password is required');
  }

  return errors.value.length === 0;
};

const handleSubmit = async () => {
  if (!validateForm()) return;

  loading.value = true;
  
  try {
    const response = await axios.post('/api/login/', {
      email: email.value,
      password: password.value
    });

    if (response.data.success) {
      // Store token based on remember me choice
      const storage = rememberMe.value ? localStorage : sessionStorage;
      storage.setItem('authToken', response.data.token);

      toastStore.showToast(3000, 'Login successful!', 'bg-emerald-500');
      router.push('/game');
    }
  } catch (error) {
    if (error.response) {
      errors.value = [error.response.data.message || 'Invalid credentials'];
    } else {
      errors.value = ['Network error. Please try again.'];
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* Import base styles from CSS file */
@import "@/pages/LoginPage/components/css/styles.css";

.login__forgot {
  color: #007bff;
  text-decoration: none;
}

.login__forgot:hover {
  text-decoration: underline;
}

.bg-red-300 {
  margin: 1rem 0;
}
</style>
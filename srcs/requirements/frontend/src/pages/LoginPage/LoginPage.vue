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

const router = useRouter();

const email = ref('');
const password = ref('');
const errors = ref([]);
const loading = ref(false);

// This is the login logic that calls the backend API to validate user credentials.
const handleSubmit = async () => {
  loading.value = true;
  errors.value = []; // Clear previous errors

  try {
    const response = await axios.post('/api/login/', {
      email: email.value,
      password: password.value,

      // rememberMe: rememberMe.value,
    });
    // Check for a successful response. 
    if (response.data && response.data.access) {
      console.log("Access token received:", response.data);
      //store in local 
      localStorage.setItem('token', response.data.access);
      //store ststus
      localStorage.setItem('isAuthenticated', 'true');
      const token = localStorage.getItem('token');
      if (token)
        axios.defaults.headers.common['Authorization'] = "Bearer " + token;
      router.push('/game');
      } else {
        errors.value.push('User is not authenticated.');
    }
  } catch (error) {
    // Handle errors returned from the server or network issues.
    if (error.response && error.response.data) {
      // The backend might return an object with error details.
      // Adjust this as necessary for your backend.
      errors.value.push(error.response.data.error || 'An error occurred during login.');
    } else {
      errors.value.push('Network error or server is not available.');
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
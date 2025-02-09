<template>
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

    <div class="login__buttons">
      <button 
        type="submit" 
        class="login__button"
        :disabled="loading"
      >
        {{ loading ? 'Logging in...' : 'Login' }}
      </button>

      <button 
        type="button" 
        class="login__oauth-button"
        @click="handleOAuthLogin"
        :disabled="loading"
      >
        Login with 42
      </button>
    </div>

    <div class="login__register">
      Don't have an account? <router-link to="/register">Register</router-link>
    </div>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { useAuth } from '@/pages/LoginPage/components/composables/useAuth'

const email = ref('')
const password = ref('')
const rememberMe = ref(false)

const { loading, errors, handleRegularLogin, handleOAuthLogin } = useAuth()

const handleSubmit = () => {
  handleRegularLogin(email.value, password.value, rememberMe.value)
}
</script>


<style scoped>
@import "@/pages/LoginPage/components/css/styles.css";

.login__forgot {
  color: #007bff;
  text-decoration: none;
}

.login__oauth-button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 1s;
  margin-top: 20px;
  margin-bottom: 0.8rem;
  margin-top: 0.2rem;
  
}

.login__oauth-button:hover {
  background-color: #b3005a;
  transition: background-color 1s;
}
</style>
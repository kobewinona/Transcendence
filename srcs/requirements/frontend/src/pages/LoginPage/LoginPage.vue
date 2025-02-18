<template>
    <div class="login"></div>
      <img src="@/pages/LoginPage/components/img/login-bg.png" alt="background" class="login__bg" />
      <!-- collect user input and prevent the page from reloading v-on:submit-->

      <form class="login__form" @submit.prevent="handleSubmit">
        <h1 class="login__title">Login</h1>

      <div class="login__inputs">
        <div class="login__box">
          <input type="name"  v-model="name" placeholder="name ID" required class="login__input" />
          <i class="ri-mail-fill"></i>
        </div>

        <div class="login__box">
          <input type="password"  v-model="password" placeholder="Password" required class="login__input" />
          <i class="ri-lock-2-fill"></i>
        </div>
      </div>

      <div v-if="errors.length" class="bg-red-300 text-white rounded-lg p-6 mb-4">
        <p v-for="(error, index) in errors" :key="index">{{ error }}</p>
      </div>

      <div class="login__check">
        <div class="login__check-box">
          <input type="checkbox" id="remember-me" v-model="rememberMe" class="login__check-input" />
          <label for="remember-me" class="login__check-label">Remember me</label>
        </div>
        <router-link to="/forgot-password" class="login__forgot">Forgot Password?</router-link>
      </div>

      <div class="login__buttons" id="login__buttons">
        <button type="submit" class="login__button":disabled="loading">
          {{ loading   ? 'Logging in...' : 'Login' }}
        </button>

        <button type="button" class="login__otp-button" @click="sendOTP" :disabled="loading || isOTPSent" >
          Send OTP
        </button>

        <button type="button" class="login__oauth-button" @click="handleOAuthLogin" :disabled="loading" >
          Login with 42
        </button>

        <div v-if="isOTPSent" class="login__otp-input-container">
          <input
            type="text"
            v-model="otp"
            placeholder="Enter OTP"
            class="login__otp-input"
          />
          <button
            type="button"
            class="login__verify-otp-button"
            @click="verifyOTP"
            :disabled="loading"
          >
            Verify OTP
          </button>
        </div>
        <!-- <div v-if="!isOTPSent">
          <button 
            type="button" 
            class="login__otp-button"
            @click="RegularLoginSendOTP"
            :disabled="loading"
          >
            Send OTP
          </button> -->
        <!-- </div> -->
        
        <!-- <div v-else class="login__otp-input-container">
          <input 
            type="text" 
            v-model="otp" 
            placeholder="Enter OTP" 
            class="login__otp-input" 
          />
          <button 
            type="button" 
            class="login__verify-otp-button"
            @click="checkOTP"
            :disabled="loading"
          >
            Verify OTP
          </button>
        </div> -->
      </div>

      <div class="login__register">
        Don't have an account? <router-link to="/register">Register</router-link>
      </div>
  </form>
</template>

<!-- <script src="./components/composables/useAuth.js"></script> -->

<script setup>
  const btn = document.getElementById('login__buttons');

  import { ref } from 'vue'

  import { useAuth } from '@/pages/LoginPage/components/composables/useAuth'

  // const name = ref('')
  // const password = ref('')
  const rememberMe = ref(false)

  const email = ref('');
const password = ref('');
const otp = ref('');
const isOTPSent = ref(false);
  const { loading, errors, RegularLoginSendOTP,checkOTP, handleOAuthLogin } = useAuth()

  const handleSubmit = () => {
    console.log("going to login")
    RegularLoginSendOTP(email.value, password.value, rememberMe.value)
    checkOTP(email.value, password.value, otp.value)
    console.log("submitted")
  }
</script>

<style scoped>
  @import "@/pages/LoginPage/components/css/styles.css";
  .login__otp-input-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

.login__otp-input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 150px;
}

.login__verify-otp-button {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.login__verify-otp-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
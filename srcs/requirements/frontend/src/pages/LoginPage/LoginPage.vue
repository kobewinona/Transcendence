<template>
    <div class="login"></div>
      <img src="@/pages/LoginPage/components/img/login-bg.png" alt="background" class="login__bg" />
      <!-- collect user input and prevent the page from reloading v-on:submit-->

      <form class="login__form" @submit.prevent="handleSubmit">
        <h1 class="login__title">Login</h1>

      <div class="login__inputs">
        <div class="login__box">
          <input type="username"  v-model="username" placeholder="username" required class="login__input" />
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
          {{ loading   ? 'Sending...' : 'Send Otp' }}
        </button>


        <button type="button" class="login__oauth-button" @click="handleOAuthLogin" :disabled="loading" >
          Login with 42
        </button>

        <div v-if="isOTPSent" class="login__otp-input-container">
          <input type="text" v-model="otp" placeholder="Enter OTP" class="login__otp-input" />
          <button type="button" class="login__verify-otp-button" @click="verifyOTP" :disabled="loading">
            Verify OTP
          </button>
        </div>
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
  import { useAuth, useOTP} from '@/pages/LoginPage/components/composables/useAuth'

  const username = ref('');
  const password = ref('');
  const otp = ref('');
  // const rememberMe = ref(false)
  const isOTPSent = ref(false);

  const { loading, errors,sendOTP, checkOTP,handleOAuthLogin } = useAuth()

//send otp
  const handleSubmit = async() => {
    try {
      console.log("validatig member...");
      console.log("sending OTP");
      await sendOTP(username.value, password.value);
      isOTPSent.value = True;
    }
    catch (error) {
      console.error("failed ot send otp");
      errors.value.push('Failed to send OTP. Please try again.');
    }
  };

  //validate
  const verifyOTP = async() =>{
    try{
      console.log("verifying OTP");
      const isVerified = await checkOTP(username.value, password.value, otp.value);
      if (isVerified){
        console.log("boooomba");
        router.push('/game');
      } else{
        errors.value.push('Invalid OTP. Please try again.');
      }
    } catch (error){
      console.error('OTP verification failed')
      errors.value.push('rukopop')
    }
  };
</script>

<style scoped>
  @import "@/pages/LoginPage/components/css/styles.css";
</style>
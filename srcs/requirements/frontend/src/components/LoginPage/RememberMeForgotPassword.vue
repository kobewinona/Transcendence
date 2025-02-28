<template>
    <div class="login__check">
      <div class="login__check-box">
        <input 
          id="remember-me" 
          v-model="rememberMe" 
          type="checkbox" 
          class="login__check-input" 
        />
        <label for="remember-me" class="login__check-label">Remember me</label>
      </div>
      <router-link to="/forgot-password" class="login__forgot">
        Forgot Password?
      </router-link>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const rememberMe = ref(false);
  
  defineExpose({
    rememberMe,
  });
  </script>
  <style scoped>
  @import "@/pages/LoginPage/components/css/styles.css";
  </style>
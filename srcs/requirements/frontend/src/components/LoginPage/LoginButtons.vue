<template>
    <div class="login__buttons">
      <button 
        type="submit" 
        class="login__button" 
        :disabled="loading" 
        @click="handleSubmit"
      >
        {{ loading ? 'Sending...' : 'Send OTP' }}
      </button>
      <slot name="otp-buttons"></slot>
      <button 
        type="button" 
        class="login__oauth-button" 
        :disabled="loading" 
        @click="handleOAuthLogin"
      >
        Login with 42
      </button>
    </div>
  </template>
  
  <script setup>
  defineProps({
    loading: {
      type: Boolean,
      default: false,
    },
  });
  
  defineEmits(['submit', 'oauth-login']);
  </script>
  <style scoped>
  @import "@/pages/LoginPage/components/css/styles.css";
  </style>
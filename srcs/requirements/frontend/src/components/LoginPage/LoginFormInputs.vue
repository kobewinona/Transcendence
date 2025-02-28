<template>
    <div class="login__inputs">
      <div class="login__box">
        <input 
          v-model="username" 
          type="text" 
          placeholder="Username" 
          required 
          class="login__input" 
        />
        <i class="ri-mail-fill"></i>
      </div>
      <div class="login__box">
        <input 
          v-model="password" 
          type="password" 
          placeholder="Password" 
          required 
          class="login__input" 
        />
        <i class="ri-lock-2-fill"></i>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const username = ref('');
  const password = ref('');
  
  defineExpose({
    username,
    password,
  });
  </script>
  <style scoped>
  @import "@/pages/LoginPage/components/css/styles.css";
  </style>
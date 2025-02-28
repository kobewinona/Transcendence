<template>
    <button type="submit" class="register__button">
      {{ label }}
    </button>
  </template>
  
  <script setup>
  defineProps({
    label: {
      type: String,
      required: true
    }
  });
  </script>
  
  <style scoped>
  @import "@/pages/RegisterPage/components/css/register-styles.css";
  </style>
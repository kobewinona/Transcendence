<template>
    <div 
      v-if="errors.length" 
      class="bg-red-300 text-white rounded-lg p-6 mb-4"
    >
      <p v-for="(error, index) in errors" :key="index">{{ error }}</p>
    </div>
  </template>
  
  <script setup>
  defineProps({
    errors: {
      type: Array,
      default: () => []
    }
  });
  </script>
  
  <style scoped>
  @import "@/pages/RegisterPage/components/css/register-styles.css";
  </style>
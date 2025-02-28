<template>
    <div class="register__box">
      <input 
        :type="type" 
        :placeholder="placeholder" 
        :value="modelValue" 
        required 
        class="register__input" 
        @input="$emit('update:modelValue', $event.target.value)"
      />
      <i :class="iconClass"></i>
    </div>
  </template>
  
  <script setup>
  defineProps({
    type: {
      type: String,
      default: 'text'
    },
    placeholder: {
      type: String,
      required: true
    },
    modelValue: {
      type: String,
      required: true
    },
    iconClass: {
      type: String,
      required: true
    }
  });
  defineEmits(['update:modelValue']);
  </script>
  
  <style scoped>
  @import "@/pages/RegisterPage/components/css/register-styles.css";
  </style>
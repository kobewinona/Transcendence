<template>
    <div class="otp">
      <input
        v-for="(digitInput, index) in otpLength"
        :key="index"
        v-model="otpArray[index]"
        type="text"
        maxlength="1"
        class="input"
        @keydown="handleEnter(index, $event)"
        @input="handleInput(index, $event)"
        @paste="handlePaste(index, $event)"
      />
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const otpLength = ref(6);
  const otpArray = ref(Array(otpLength.value).fill(''));
  
  defineExpose({
    otpArray,
  });
  
  const handleInput = (index, event) => {
    const value = event.target.value;
    if (value.length > 1) {
      otpArray.value[index] = value[0];
    } else {
      otpArray.value[index] = value;
    }
    if (value && index < otpLength.value - 1) {
      document.querySelectorAll('.input')[index + 1].focus();
    }
  };
  
  const handlePaste = (index, event) => {
    event.preventDefault();
    const pastedData = event.clipboardData.getData('text').trim();
    for (let i = 0; i < pastedData.length && i < otpLength.value; i++) {
      otpArray.value[index + i] = pastedData[i];
    }
    const lastPopulatedIndex = Math.min(index + pastedData.length, otpLength.value - 1);
    document.querySelectorAll('.input')[lastPopulatedIndex].focus();
  };
  
  const handleEnter = (index, event) => {
    if (event.key === 'Backspace' && !otpArray.value[index] && index > 0) {
      otpArray.value[index - 1] = '';
      document.querySelectorAll('.input')[index - 1].focus();
    }
  };
  </script>
  <style scoped>
  @import "@/pages/LoginPage/components/css/styles.css";
  </style>
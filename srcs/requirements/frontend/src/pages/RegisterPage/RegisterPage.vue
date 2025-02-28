<template>
  <div class="register">
    <!-- Background Image -->
    <img 
      src="@/pages/RegisterPage/components/img/register-bg.png" 
      alt="background" 
      class="register__bg" 
    />
    <!-- Registration Form -->
    <form class="register__form" @submit.prevent="handleSubmit">
      <h1 class="register__title">Register</h1>

      <!-- Input Fields -->
      <div class="register__inputs">
        <InputField 
          v-model="form.username" 
          placeholder="Full username" 
          icon-class="ri-user-fill" 
        />
        <InputField 
          v-model="form.email" 
          type="email" 
          placeholder="Email ID" 
          icon-class="ri-mail-fill" 
        />
        <InputField 
          v-model="form.password1" 
          :type="showPassword ? 'text' : 'password'" 
          placeholder="Password" 
          icon-class="ri-eye-fill password-toggle" 
          @click="togglePasswordVisibility"
        />
        <InputField 
          v-model="form.password2" 
          :type="showPassword ? 'text' : 'password'" 
          placeholder="Confirm Password" 
          icon-class="ri-eye-fill password-toggle" 
          @click="togglePasswordVisibility"
        />
      </div>
      <ErrorMessages :errors="errors" />
      <SubmitButton label="Create Account" />
      <LoginLink />
    </form>
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import ErrorMessages from '@/components/RegisterPage/ErrorMessages.vue';
import InputField from '@/components/RegisterPage/InputField.vue';
import LoginLink from '@/components/RegisterPage/LoginLink.vue';
import SubmitButton from '@/components/RegisterPage/SubmitButton.vue';

const router = useRouter();
const form = ref({
  username: '',
  email: '',
  password1: '',
  password2: ''
});
const errors = ref([]);
const showPassword = ref(false);

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

const handleSubmit = async () => {
  errors.value = [];

  if (form.value.password1 !== form.value.password2) {
    errors.value.push("Passwords do not match!");
    return;
  }

  const registrationData = {
    username: form.value.username,
    email: form.value.email,
    password: form.value.password1
  };

  try {
    const response = await axios.post('/api/signup/', registrationData);
    console.log('Server response:', response.data);
    router.push('/');
  } catch (error) {
    if (error.response?.data) {
      const backendErrors = error.response.data;
      for (const key in backendErrors) {
        backendErrors[key].forEach(err => {
          errors.value.push(`${key}: ${err}`);
        });
      }
    } else {
      errors.value.push("Registration failed. Please try again.");
    }
  }
};
</script>

<style scoped>
@import "@/pages/RegisterPage/components/css/register-styles.css";
</style>
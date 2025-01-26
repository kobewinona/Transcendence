<template>
  <div class="register">
    <img src="@/pages/RegisterPage/components/img/register-bg.png" alt="background" class="register__bg" />
    <form class="register__form" @submit.prevent="handleSubmit">
      <h1 class="register__title">Register</h1>

      <div class="register__inputs">
        <div class="register__box">
          <input 
            type="text" 
            v-model="form.name" 
            placeholder="Full Name" 
            required 
            class="register__input" 
          />
          <i class="ri-user-fill"></i>
        </div>

        <div class="register__box">
          <input 
            type="email" 
            v-model="form.email" 
            placeholder="Email ID" 
            required 
            class="register__input" 
          />
          <i class="ri-mail-fill"></i>
        </div>

        <div class="register__box">
          <input 
            :type="showPassword ? 'text' : 'password'"
            v-model="form.password1" 
            placeholder="Password" 
            required 
            class="register__input"
          />
          <i 
            class="ri-eye-fill password-toggle"
            @click="togglePasswordVisibility"
          ></i>
        </div>

        <div class="register__box">
          <input 
            :type="showPassword ? 'text' : 'password'"
            v-model="form.password2" 
            placeholder="Confirm Password" 
            required 
            class="register__input"
          />
          <i class="ri-lock-2-fill"></i>
        </div>
      </div>
      
      <div v-if="errors.length" class="bg-red-300 text-white rounded-lg p-6 mb-4">
        <p v-for="(error, index) in errors" :key="index">{{ error }}</p>
      </div>

      <button type="submit" class="register__button">Create Account</button>

      <div class="register__login">
        Already have an account? <router-link to="/">Login</router-link>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { useToastStore } from '@/store/toast';

const router = useRouter();
const toastStore = useToastStore();

const form = ref({
  name: '',
  email: '',
  password1: '',
  password2: ''
});

const errors = ref([]);
const showPassword = ref(false);

const validateForm = () => {
  errors.value = [];
  
  if (!form.value.name.trim()) {
    errors.value.push('Name is required');
  }
  
  if (!form.value.email.trim()) {
    errors.value.push('Email is required');
  } else if (!/^\S+@\S+\.\S+$/.test(form.value.email)) {
    errors.value.push('Invalid email format');
  }
  
  if (!form.value.password1) {
    errors.value.push('Password is required');
  } else if (form.value.password1.length < 8) {
    errors.value.push('Password must be at least 8 characters');
  }
  
  if (form.value.password1 !== form.value.password2) {
    errors.value.push('Passwords do not match');
  }

  return errors.value.length === 0;
};

const handleSubmit = async () => {
  if (!validateForm()) return;

  try {
    const response = await axios.post('/api/signup/', form.value);
    
    if (response.data.message === 'success') {
      toastStore.showToast(5000, 'Registration successful! Please login.', 'bg-emerald-500');
      router.push('/');
    }
  } catch (error) {
    if (error.response) {
      // Handle Django validation errors
      const errorData = error.response.data;
      errors.value = Object.values(errorData).flat();
    } else {
      errors.value = ['Network error. Please try again.'];
    }
  }
};

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};
</script>

<style scoped>
/* Import base styles from CSS file */
@import "@/pages/RegisterPage/components/css/register-styles.css";

.password-toggle {
  cursor: pointer;
  transition: opacity 0.3s;
}

.password-toggle:hover {
  opacity: 0.8;
}
</style>
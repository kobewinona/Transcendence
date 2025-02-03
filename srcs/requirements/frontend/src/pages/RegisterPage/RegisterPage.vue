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
          <i 
            class="ri-eye-fill password-toggle"
            @click="togglePasswordVisibility"
          ></i>
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

const router = useRouter();

const form = ref({
  name: '',
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
  
  // Frontend validation
  if (form.value.password1 !== form.value.password2) {
    errors.value.push("Passwords do not match!");
    return;
  }

  // Prepare data for backend
  const registrationData = {
    name: form.value.name,
    email: form.value.email,
    password: form.value.password1
  };

  try {
    // Send POST request to Django backend
    const response = await axios.post(
      '/api/signup/',registrationData
    );
    // Handle successful registration
    router.push('/'); // Redirect to login page
  } catch (error) {
    // Handle errors
    if (error.response?.data) {
      // Convert Django error object to array
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

.password-toggle {
  cursor: pointer;
  transition: opacity 0.3s;
}

.password-toggle:hover {
  opacity: 0.8;
}
</style>







<!-- src/pages/RegisterPage/RegisterPage.vue -->
<template>
    <div class="register">
      <img src="@/pages/RegisterPage/components/img/register-bg.png" alt="background" class="register__bg" />
  
      <form class="register__form" @submit.prevent="handleSubmit">
        <h1 class="register__title">Register</h1>
  
        <div class="register__inputs">
          <div class="register__box">
            <input 
              type="text" 
              v-model="form.fullName" 
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
              type="password" 
              v-model="form.password" 
              placeholder="Password" 
              required 
              class="register__input"
              :type="showPassword ? 'text' : 'password'" 
            />
            <i 
              class="ri-eye-fill password-toggle"
              @click="togglePasswordVisibility"
            ></i>
          </div>
  
          <div class="register__box">
            <input 
              type="password" 
              v-model="form.confirmPassword" 
              placeholder="Confirm Password" 
              required 
              class="register__input"
              :type="showPassword ? 'text' : 'password'" 
            />
            <i class="ri-lock-2-fill"></i>
          </div>
        </div>
  
        <button type="submit" class="register__button">Create Account</button>
  
        <div class="register__login">
          Already have an account? <router-link to="/login">Login</router-link>
        </div>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    name: "RegisterPage",
    data() {
      return {
        showPassword: false,
        form: {
          fullName: '',
          email: '',
          password: '',
          confirmPassword: ''
        }
      };
    },
    // methods: {
    //   togglePasswordVisibility() {
    //     this.showPassword = !this.showPassword;
    //   },
    //   handleSubmit() {
    //     if (this.form.password !== this.form.confirmPassword) {
    //       alert("Passwords don't match!");
    //       return;
    //     }
    //     // Add registration logic here
    //     console.log('Registration data:', this.form);
    //   }
    // }
    
  };
  </script>
  
  <style scoped>
  /* Import base styles from CSS file */
  @import "@/pages/RegisterPage/components/css/register-styles.css";
  </style>
<template>
  <div class="login">
    <img src="@/pages/LoginPage/components/img/login-bg.png" alt="background" class="login__bg" />

    <form class="login__form">
      <h1 class="login__title">Login</h1>

      <div class="login__inputs">
        <div class="login__box">
          <input type="email" placeholder="Email ID" required class="login__input" />
          <i class="ri-mail-fill"></i>
        </div>

        <div class="login__box">
          <input type="password" placeholder="Password" required class="login__input" />
          <i class="ri-lock-2-fill"></i>
        </div>
      </div>

      <!-- Updated Check & Forgot Section -->
      <div class="login__check">
        <div class="login__check-box">
          <input type="checkbox" id="remember-me" class="login__check-input" />
          <label for="remember-me" class="login__check-label">Remember me</label>
        </div>
        <a href="#" class="login__forgot">Forgot Password?</a>
      </div>

      <!-- Login Button -->
      <button type="submit" class="login__button">Login</button>

      <!-- Register Link -->
      <div class="login__register">
        Don't have an account? <a href="#">Register</a>
        <!-- Don't have an account?  <router-link to="/register">Register</router-lin  -->
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: "LoginPage",
};
</script>

<style scoped>
/* Import styles from the CSS file */
@import "@/pages/LoginPage/components/css/styles.css";
</style>

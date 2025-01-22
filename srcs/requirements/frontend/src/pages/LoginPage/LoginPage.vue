<!-- <template>
  <div class="login">
    <img src="@/pages/LoginPage/components/img/login-bg.png" alt="image" class="login__bg" />

    <form action="" class="login__form">
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

      <div class="login__check">
        <div class="login__check-box">
          <input type="checkbox" class="login__check-input" id="user-check" />
          <label for="user-check" class="login__check-label">Remember me</label>
        </div>

        <button type="submit" class="login__button">Login</button>

        <div class="login__register">
          Don't have an account? <a href="#">Register</a>
        </div>
        <div class="login__forgot-wrapper">
          <a href="#" class="login__forgot">Forgot Password?</a>
        </div>
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

.login__forgot-wrapper {
  margin-top: 10px;
}
</style> -->

<!-- <template>
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

      <div class="login__check-box">
        <input type="checkbox" id="remember-me" class="login__check-input" />
        <label for="remember-me" class="login__check-label">Remember me</label>
      </div>
       <div class="login__forgot-wrapper">
          <a href="#" class="login__forgot">Forgot Password?</a>
        </div>
      <button type="submit" class="login__button">Login</button>

      <div class="login__register">
        Don't have an account? <a href="#">Register</a>
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
</style> -->

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

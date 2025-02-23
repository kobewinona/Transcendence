<template>
    <div class="login"></div>
      <img src="@/pages/LoginPage/components/img/login-bg.png" alt="background" class="login__bg" />
      <!-- collect user input and prevent the page from reloading v-on:submit-->

      <form class="login__form" @submit.prevent="handleSubmit">
        <h1 class="login__title">Login</h1>
      <div class="login__inputs">
        <div class="login__box">
          <input type="username"  v-model="username" placeholder="username" required class="login__input" />
          <i class="ri-mail-fill"></i>
        </div>

        <div class="login__box">
          <input type="password"  v-model="password" placeholder="Password" required class="login__input" />
          <i class="ri-lock-2-fill"></i>
        </div>
      </div>

      <div v-if="errors.length" class="bg-red-300 text-white rounded-lg p-6 mb-4">
        <p v-for="(error, index) in errors" :key="index">{{ error }}</p>
      </div>

      <div class="login__check">
        <div class="login__check-box">
          <input type="checkbox" id="remember-me" v-model="rememberMe" class="login__check-input" />
          <label for="remember-me" class="login__check-label">Remember me</label>
        </div>
        <router-link to="/forgot-password" class="login__forgot">Forgot Password?</router-link>
      </div>

      <div class="login__buttons" id="login__buttons">
        <button type="submit" class="login__button" @click="handleSubmit" :disabled="loading">
          {{ loading   ? 'Sending...' : 'Send Otp' }}
        </button>
          <div class="otp">
            <input
              v-for="(digitInput, index) in otpLength"
              :key="index"
              v-model="otpArray[index]"
              @keydown="handleEnter(index, $event)"
              @input="handleInput(index, $event)"
              @paste="handlePaste(index, $event)"
              type="text"
              step="1"
              maxlength="1"
              class="input"
            />
          </div>
        </div>
      <button v-if="isOTPSent" type="button" class="login__verify-otp-button" @click="verifyOTP" :disabled="loading" >
          Verify OTP
        </button>
    <button type="button" class="login__oauth-button" @click="handleOAuthLogin" :disabled="loading" >
      Login with 42
    </button>

      <div class="login__register">
        Don't have an account? <router-link to="/register">Register</router-link>
      </div>
  </form>
</template>

<!-- <script src="./components/composables/useAuth.js"></script> -->

<script setup>
  
  import { ref } from 'vue'
  // import OtpInput from '.@/pages/LoginPage/components/composables/otp.vue'
  import { useAuth} from '@/pages/LoginPage/components/composables/useAuth'

  const username = ref('');
  const password = ref('');
  const otp = ref('');
  const rememberMe = ref(false)
  const isOTPSent = ref(false);
  const otpLength = ref(6); // Number of OTP digits
  const otpArray = ref(Array(otpLength.value).fill('')); // Array to hold OTP digits
  const isUserValidated = ref(false);

  const { loading, errors,sendOTP, checkOTP,handleOAuthLogin } = useAuth()

//send otp
  const handleSubmit = async() => {
    try {
      console.log("validatig member...");
      console.log("sending OTP");
      loading.value = true;
      const otpSentSuccessfully = await sendOTP(username.value, password.value);
      if (otpSentSuccessfully) {
      // Set isOTPSent to true only if sendOTP succeeds
        isOTPSent.value = true;
        console.log(isOTPSent.value, "isOTPSent");
    } else {
      // Handle the case where sendOTP fails but doesn't throw an error
        errors.value.push('Failed to send OTP. Please try again.');
       }
      console.log(isOTPSent.value, "isOTPSent");
    }
    catch (error) {
      console.error("failed ot send otp");
      errors.value.push('Failed to send OTP. Please try again.');
    }
    loading.value = false;
    console.log("Loading state after OTP send:", loading.value);
  };

  //validate
  const verifyOTP = async() =>{
    try{
      console.log("verifying OTP");
      const otp = otpArray.value.join(''); // make single string
      console.log("Entered OTP:", otp);
      const isVerified = await checkOTP(username.value, password.value, otp);
      if (isVerified){
        console.log("boooomba");
        router.push('/game');
      } else{
        errors.value.push('Invalid OTP. Please try again.');
      }
    } catch (error){
      console.error('OTP verification failed')
      errors.value.push('rukopop')
    }
  };

    //OTP input fields
  const handleInput = (index, event) => {
    const value = event.target.value;

    //only one character is entered
    if (value.length > 1) {
      otpArray.value[index] = value[0];
    } else {
      otpArray.value[index] = value;
    }

    //next input field
    if (value && index < otpLength.value - 1) {
      document.querySelectorAll('.input')[index + 1].focus();
    }
  };
  const handlePaste = (index, event) => {
    event.preventDefault();
    const pastedData = event.clipboardData.getData('text').trim();

    // Populate the OTP fields with the pasted data
    for (let i = 0; i < pastedData.length && i < otpLength.value; i++) {
      otpArray.value[index + i] = pastedData[i];
    }

    // Focus on the last populated field
    const lastPopulatedIndex = Math.min(index + pastedData.length, otpLength.value - 1);
    document.querySelectorAll('.input')[lastPopulatedIndex].focus();
  };
  const handleEnter = (index, event) => {
    if (event.key === 'Backspace' && !otpArray.value[index] && index > 0) {
      // Move focus to the previous field if Backspace is pressed on an empty field
      otpArray.value[index - 1] = '';
      document.querySelectorAll('.input')[index - 1].focus();
    }
  };
</script>

<style scoped>
  @import "@/pages/LoginPage/components/css/styles.css";
  .otp {
  display: flex;
  gap: 1rem;
  margin: 1rem auto;
  width: 80%;
  justify-content: center;
}

.input {
  outline: none;
  width: 2rem;
  display: flex;
  justify-content: center;
  padding: 0px;
  margin-right: 1rem;
  color: inherit;
  border: 1px solid #222222;
  border-radius: 8px;
  padding: 0.85rem;
  padding-right: 0;
  font-family: inherit;
  font-size: 1.5rem;
  font-weight: 700;
  line-height: 20px;
  appearance: none;
  letter-spacing: normal;
}
.input:focus {
  border: 2px solid #222222;
}

</style>
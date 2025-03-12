<template>
  <MainBodyLayout>
    <AuthLayout :title="t('auth.signin.title')">
      <div class="otp">
        <p class="otp__description">{{ t('auth.otp.description') }}</p>
        <div class="otp__container">
          <input
            v-for="(_, index) in otp"
            :key="index"
            ref="otpRefs"
            v-model="otp[index]"
            class="otp__input"
            type="text"
            maxlength="1"
            @input="handleInput(index, $event)"
            @keydown.backspace="handleBackspace(index)"
            @paste="handlePaste"
          />
        </div>
        <div :class="{ otp__loader: true, otp__loader_visible: isLoading }">
          <Loader :size="40" />
        </div>
      </div>

      <span class="otp__link">
        <router-link to="/signin">{{ t('auth.return-to-signin.text') }}</router-link>
      </span>
    </AuthLayout>
  </MainBodyLayout>
</template>

<script setup>
import { USERNAME_STORAGE_KEY } from 'config/constants.js';
import { AuthLayout, MainBodyLayout } from 'layouts';
import api from 'shared/api/Auth';
import { Loader } from 'shared/components';
import { useMutation } from 'shared/composables';
import { auth } from 'store/auth.js';
import { computed, inject, nextTick, onMounted, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';

const { t } = useI18n();
const router = useRouter();
const showErrorModal = inject('showErrorModal');
const notify = inject('notify');

const otp = ref(['', '', '', '', '', '']);
const otpRefs = ref([]);

const isOtpComplete = computed(() => otp.value.every((digit) => digit !== ''));

const { mutate: signIn, isLoading } = useMutation(api.signIn, {
  onSuccess: (res) => {
    const { access_token: token } = res?.data || {};
    auth.login(token);
    sessionStorage.removeItem(USERNAME_STORAGE_KEY);
    notify(t('success', 'success'));
    router.push('/');
  },
  onError: (error) => {
    const errorMessage =
      error?.response?.data?.message || error?.response?.statusText || t('unknown_error');
    showErrorModal(error.status, errorMessage);
  },
});

const handleInput = (index, event) => {
  const value = event.target.value;
  if (!/^\d?$/.test(value)) {
    otp.value[index] = '';
    return;
  }

  if (value && index < otp.value.length - 1) {
    nextTick(() => otpRefs.value[index + 1]?.focus());
  }
};

const handleBackspace = (index) => {
  if (!otp.value[index] && index > 0) {
    nextTick(() => otpRefs.value[index - 1]?.focus());
  }
};

const handlePaste = (event) => {
  event.preventDefault();

  const pasteData = event.clipboardData.getData('text').replace(/\D/g, '');
  const otpArray = pasteData.slice(0, otp.value.length + 1).split('');

  otpArray.forEach((char, index) => {
    otp.value[index] = char;
  });

  nextTick(() => {
    const nextEmptyIndex = otp.value.findIndex((char) => char === '');
    if (nextEmptyIndex !== -1) {
      otpRefs.value[nextEmptyIndex]?.focus();
    }
  });
};

watch(
  () => isOtpComplete.value,
  () => {
    const username = sessionStorage.getItem('username');
    signIn({ data: { username, otp: otp.value.join('') } });
  }
);

onMounted(() => {
  nextTick(() => {
    otpRefs.value[0]?.focus();
  });
});
</script>

<style scoped>
.otp {
  display: flex;
  flex-direction: column;
  row-gap: var(--bigger-space);
  align-items: center;
  justify-content: center;

  width: 100%;
  height: 100%;
}

.otp__description {
  text-align: center;
}

.otp__container {
  display: flex;
  flex-direction: row;
  column-gap: var(--smaller-space);
  align-items: center;
  justify-content: center;

  width: 100%;
}

.otp__input {
  width: 70px;
  height: 90px;

  font-size: 2.2rem;
  font-weight: 800;
  color: var(--dark-color);
  text-align: center;

  background-color: var(--light-color);
  border: none;
  border-radius: 12px;
}

.otp__input:focus-visible,
.otp__input:focus {
  outline: 4px solid var(--secondary-color);
}

.otp__loader {
  visibility: hidden;
}

.otp__loader_visible {
  visibility: visible;
}

.otp__link {
  text-align: center;
}
</style>

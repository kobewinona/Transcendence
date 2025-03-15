<template>
  <MainBodyLayout>
    <AuthLayout :title="t('auth.signin.title')" class-name="auth-layout">
      <MyForm
        :errors="serverErrors"
        :provide-key="SIGNIN_FORM_PROVIDE_KEY"
        mode="onBlur"
        @on-submit="handleSubmit"
      >
        <div class="signin-form__fields">
          <AuthFormFields
            :fields="{
              [EMAIL_INPUT_NAME]: true,
              [PASSWORD_INPUT_NAME]: true,
            }"
            :provide-key="SIGNIN_FORM_PROVIDE_KEY"
          />
        </div>
        <div class="signin-form__controls">
          <MyButton
            class-name="signin-form__button"
            color="secondary"
            type="submit"
            :loading="isLoading"
            >{{ t('auth.signin.submit_button.text') }}
          </MyButton>
          <a class="signin-form__intra-link" href="http://localhost:8001/api/signin_intra/">
            <img class="signin-form__intra-logo" :src="logo42" alt="Intra 42 logo" />
            {{ t('auth.signin_intra.submit_button.text') }}
          </a>
          <span class="signin-form__redirect">
            {{ t('auth.signin.link_to_signup.text') }}
            <router-link to="/signup">{{ t('auth.signup.title') }}</router-link>
          </span>
        </div>
      </MyForm>
    </AuthLayout>
  </MainBodyLayout>
</template>

<script setup>
import logo42 from 'assets/logo42.png';
import { MyButton, MyForm } from 'components';
import {
  EMAIL_INPUT_NAME,
  PASSWORD_INPUT_NAME,
  SIGNIN_FORM_PROVIDE_KEY,
} from 'config/AuthForm/constants.js';
import { EMAIL_STORAGE_KEY } from 'config/constants.js';
import { AuthFormFields } from 'features';
import { AuthLayout, MainBodyLayout } from 'layouts';
import api from 'shared/api/Auth';
import { useMutation } from 'shared/composables';
import { inject, reactive } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';

const { t } = useI18n();
const router = useRouter();
const showErrorModal = inject('showErrorModal');

const serverErrors = reactive({});

const { mutate: getOtp, isLoading } = useMutation(api.getOtp, {
  onSuccess: () => {
    router.push('/otp');
  },
  onError: (error) => {
    if (error.status === 400) {
      serverErrors.value = error.response?.data || {};
    } else {
      const errorMessage =
        error?.response?.data?.message || error?.response?.statusText || t('unknown_error');
      showErrorModal(error.status, errorMessage);
    }

    sessionStorage.removeItem(EMAIL_STORAGE_KEY);
  },
});

const handleSubmit = (formData) => {
  sessionStorage.setItem(EMAIL_STORAGE_KEY, formData[EMAIL_INPUT_NAME]);
  getOtp({ data: formData });
};
</script>

<style scoped>
::v-deep(.auth-layout) {
  height: 80%;
}

.signin-form__fields {
  display: flex;
  flex-direction: column;
  row-gap: var(--smaller-space);

  width: 100%;
  height: 100%;
}

.signin-form__controls {
  display: flex;
  flex-direction: column;
  row-gap: var(--small-space);
  width: 100%;
}

::v-deep(.signin-form__button) {
  width: 100%;
}

.signin-form__redirect {
  font-size: 0.85rem;
  color: var(--light-color-opacity-90);
  text-align: center;
}

.signin-form__intra-link {
  display: flex;
  flex-direction: row;
  column-gap: var(--small-space);
  align-items: center;
  justify-content: center;

  height: 44px;
  padding: var(--smaller-space);

  color: var(--dark-color);

  background-color: var(--light-color);
  border-radius: 12px;
}

.signin-form__intra-link:hover {
  filter: brightness(85%);
  transition: filter 0.2s ease-in-out;
}

.signin-form__intra-logo {
  width: 20px;
  height: 20px;
}
</style>

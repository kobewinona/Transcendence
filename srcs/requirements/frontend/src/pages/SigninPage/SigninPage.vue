<template>
  <MainBodyLayout>
    <AuthLayout class-name="auth-layout" :title="t('auth.signin.title')">
      <MyForm
        :provide-key="SIGNIN_FORM_PROVIDE_KEY"
        mode="onBlur"
        :errors="serverErrors"
        @on-submit="handleSubmit"
      >
        <div class="signin-form__fields">
          <AuthFormFields
            :provide-key="SIGNIN_FORM_PROVIDE_KEY"
            :fields="{
              [USERNAME_INPUT_NAME]: true,
              [PASSWORD_INPUT_NAME]: true,
            }"
          />
        </div>
        <div class="signin-form__controls">
          <MyButton class-name="signin-form__button" type="submit" :loading="isLoading">{{
            t('auth.signin.submit-button.text')
          }}</MyButton>
          <span class="signin-form__redirect">
            {{ t('auth.signin.link-to-signup.text') }}
            <router-link to="/signup">{{ t('auth.signup.title') }}</router-link>
          </span>
        </div>
      </MyForm>
    </AuthLayout>
  </MainBodyLayout>
</template>

<script setup>
import { MyButton, MyForm } from 'components';
import {
  PASSWORD_INPUT_NAME,
  SIGNIN_FORM_PROVIDE_KEY,
  USERNAME_INPUT_NAME,
} from 'config/AuthForm/constants.js';
import { USERNAME_STORAGE_KEY } from 'config/constants.js';
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

    sessionStorage.removeItem(USERNAME_STORAGE_KEY);
  },
});

const handleSubmit = (formData) => {
  sessionStorage.setItem(USERNAME_STORAGE_KEY, formData[USERNAME_INPUT_NAME]);
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
</style>

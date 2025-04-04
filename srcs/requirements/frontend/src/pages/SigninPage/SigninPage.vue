<template>
  <MainBodyLayout>
    <AuthLayout :title="t('auth.signin.title')" class-name="auth-layout">
      <form class="signin-form__form" novalidate @submit="onSubmit">
        <div class="signin-form__fields">
          <MyInput
            :label="t('auth.email.label')"
            :name="AUTH_NAMES.EMAIL"
            mode="eager"
            type="email"
          />
          <MyInput
            :label="t('auth.password.label')"
            :name="AUTH_NAMES.PASSWORD"
            mode="eager"
            type="password"
          />
        </div>
        <div class="signin-form__controls">
          <MyButton
            :loading="isFetchingOtp"
            class-name="signin-form__button"
            color="secondary"
            type="submit"
            >{{ t('auth.signin.submit_button.text') }}
          </MyButton>
          <MyButton
            :icon="logo42"
            :loading="isLoadingIntraAuthPage"
            color="light"
            type="button"
            @click="handleIntraSignClick"
          >
            {{ t('auth.signin_intra.submit_button.text') }}
          </MyButton>
          <span class="signin-form__redirect">
            {{ t('auth.signin.link_to_signup.text') }}
            <router-link to="/signup">{{ t('auth.signup.title') }}</router-link>
          </span>
        </div>
      </form>
    </AuthLayout>
  </MainBodyLayout>
</template>

<script setup>
import logo42 from 'assets/logo42.png';
import { MyButton, MyInput } from 'components';
import { AUTH_NAMES } from 'config/AuthForm/constants.js';
import { EMAIL_STORAGE_KEY } from 'config/constants.js';
import { AuthLayout, MainBodyLayout } from 'layouts';
import api from 'shared/api/Auth';
import { useMutation } from 'shared/composables';
import { tryParseAnyError } from 'shared/lib';
import { signinSchema } from 'shared/validation';
import { useForm } from 'vee-validate';
import { inject, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';

const { t } = useI18n();
const router = useRouter();
const showErrorModal = inject('showErrorModal');

const isLoadingIntraAuthPage = ref(false);

const { handleSubmit } = useForm({
  validationSchema: signinSchema(t, { strictPassword: false }),
});

const { mutate: getOtp, isLoading: isFetchingOtp } = useMutation({
  fetchFn: api.getOtp,
  options: {
    onSuccess: () => router.push('/otp'),
    onError: (error) => {
      showErrorModal(error.status, tryParseAnyError(error));
      sessionStorage.removeItem(EMAIL_STORAGE_KEY);
    },
  },
});

const onSubmit = handleSubmit((formData) => {
  sessionStorage.setItem(EMAIL_STORAGE_KEY, formData[AUTH_NAMES.EMAIL]);
  getOtp({ data: formData });
});

const handleIntraSignClick = () => {
  isLoadingIntraAuthPage.value = true;
  window.location.href = `${import.meta.env.VITE_API_URL}/api/signin_intra/`;
};
</script>

<style scoped>
::v-deep(.auth-layout) {
  height: 80%;
}

.signin-form__form {
  display: contents;
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

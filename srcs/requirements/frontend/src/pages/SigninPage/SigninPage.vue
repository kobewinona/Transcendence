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
          <a :href="intraOAuthUrl" class="signin-form__intra-link" @click="handleIntraSignClick">
            <Loader :is-active="isLoadingIntraAuthPage" />
            <img :src="logoPath" alt="Intra 42 logo" class="signin-form__intra-logo" />
            {{ t('auth.signin_intra.submit_button.text') }}
          </a>
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
import { AUTHORIZE_ENDPOINT, EMAIL_STORAGE_KEY } from 'config/constants.js';
import { AuthLayout, MainBodyLayout } from 'layouts';
import { isPlainObject } from 'lodash';
import api from 'shared/api/Auth';
import { Loader } from 'shared/components';
import { useMutation } from 'shared/composables';
import { parseValidationErrors, tryParseAnyError } from 'shared/lib';
import { signinSchema } from 'shared/validation';
import { useForm } from 'vee-validate';
import { computed, inject, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';

const { t } = useI18n();
const router = useRouter();
const showErrorModal = inject('showErrorModal');

const isLoadingIntraAuthPage = ref(false);

const intraOAuthUrl = computed(() => {
  const CLIENT_ID = import.meta.env.VITE_CLIENT_ID;
  const REDIRECT_URI = import.meta.env.VITE_REDIRECT_URI;

  const params = new URLSearchParams({
    client_id: CLIENT_ID,
    redirect_uri: REDIRECT_URI,
    response_type: 'code',
  });

  return `${AUTHORIZE_ENDPOINT}?${params.toString()}`;
});
const logoPath = computed(() => (import.meta.env.DEV ? logo42 : '/logo42.png'));

const { setErrors, handleSubmit } = useForm({
  validationSchema: signinSchema(t, { strictPassword: false }),
});

const { mutate: getOtp, isLoading: isFetchingOtp } = useMutation({
  fetchFn: api.getOtp,
  options: {
    onSuccess: () => router.push('/otp'),
    onError: (error) => {
      if (error.status === 400) {
        const serverValidationErrors = parseValidationErrors(error.response?.data) || {};

        if (serverValidationErrors && isPlainObject(serverValidationErrors)) {
          // noinspection JSCheckFunctionSignatures
          setErrors(serverValidationErrors);
        } else {
          showErrorModal(error.status, tryParseAnyError(error));
        }
      } else {
        showErrorModal(error.status, tryParseAnyError(error));
      }

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

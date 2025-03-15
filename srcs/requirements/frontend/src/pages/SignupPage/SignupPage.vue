<template>
  <MainBodyLayout>
    <AuthLayout :title="t('auth.signup.title')" class-name="auth-layout">
      <MyForm
        :errors="serverErrors"
        :provide-key="SIGNUP_FORM_PROVIDE_KEY"
        mode="onBlur"
        @on-submit="handleSubmit"
      >
        <div class="signup-form__fields">
          <AuthFormFields :provide-key="SIGNUP_FORM_PROVIDE_KEY" />
        </div>
        <div class="signup-form__controls">
          <MyButton
            :loading="isLoading"
            class-name="signup-form__button"
            color="secondary"
            type="submit"
            >{{ t('auth.signup.submit_button.text') }}
          </MyButton>
          <span class="signup-form__redirect">
            {{ t('auth.signup.link_to_signin.text') }}
            <router-link to="/signin">{{ t('auth.signin.title') }}</router-link>
          </span>
        </div>
      </MyForm>
    </AuthLayout>
  </MainBodyLayout>
</template>

<script setup>
import { MyButton, MyForm } from 'components';
import { SIGNUP_FORM_PROVIDE_KEY } from 'config/AuthForm/constants.js';
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
const notify = inject('notify');

const serverErrors = reactive({});

const { mutate: signUp, isLoading } = useMutation(api.signUp, {
  onSuccess: () => {
    notify(t('success'), 'success');
    router.push('/signin');
  },
  onError: (error) => {
    if (error.status === 400) {
      serverErrors.value = error.response?.data || {};
    } else {
      const errorMessage =
        error?.response?.data?.message || error?.response?.statusText || t('unknown_error');
      showErrorModal(error.status, errorMessage);
    }
  },
});

const handleSubmit = (formData) => {
  signUp({ data: formData });
};
</script>

<style scoped>
::v-deep(.auth-layout) {
  height: 80%;
}

.signup-form__fields {
  display: flex;
  flex-direction: column;
  row-gap: var(--smaller-space);

  width: 100%;
  height: 100%;
}

.signup-form__controls {
  display: flex;
  flex-direction: column;
  row-gap: var(--small-space);
  width: 100%;
}

::v-deep(.signup-form__button) {
  width: 100%;
}

.signup-form__redirect {
  font-size: 0.85rem;
  color: var(--light-color-opacity-90);
  text-align: center;
}
</style>

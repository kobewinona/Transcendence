<template>
  <MainBodyLayout>
    <AuthLayout :title="t('auth.signup.title')" class-name="auth-layout">
      <form class="signup-form__form" novalidate @submit="onSubmit">
        <div class="signup-form__fields">
          <MyInput
            :name="AUTH_NAMES.USERNAME"
            type="text"
            :label="t('auth.username.label')"
            mode="eager"
          />
          <MyInput
            :name="AUTH_NAMES.EMAIL"
            type="email"
            :label="t('auth.email.label')"
            mode="eager"
          />
          <MyInput
            :name="AUTH_NAMES.PASSWORD"
            type="password"
            :label="t('auth.password.label')"
            mode="eager"
          />
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
      </form>
    </AuthLayout>
  </MainBodyLayout>
</template>

<script setup>
import { MyButton, MyInput } from 'components';
import { AUTH_NAMES } from 'config/AuthForm/constants.js';
import { EMAIL_STORAGE_KEY } from 'config/constants.js';
import { AuthLayout, MainBodyLayout } from 'layouts';
import { isPlainObject } from 'lodash';
import api from 'shared/api/Auth';
import { useMutation } from 'shared/composables';
import { parseValidationErrors, tryParseAnyError } from 'shared/lib';
import { signupSchema } from 'shared/validation';
import { useForm } from 'vee-validate';
import { inject } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';

const { t } = useI18n();
const router = useRouter();

const showErrorModal = inject('showErrorModal');
const notify = inject('notify');

const { handleSubmit, setErrors } = useForm({ validationSchema: signupSchema(t) });

const { mutate: signUp, isLoading } = useMutation({
  fetchFn: api.signUp,
  options: {
    onSuccess: () => {
      notify(t('success'), 'success');
      router.push('/signin');
    },
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
  signUp({ data: formData });
});
</script>

<style scoped>
::v-deep(.auth-layout) {
  height: 80%;
}

.signup-form__form {
  display: contents;
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

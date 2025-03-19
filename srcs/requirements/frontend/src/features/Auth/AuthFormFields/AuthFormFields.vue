<template>
  <MyController
    v-if="Boolean(fields[USERNAME_INPUT_NAME])"
    :name="USERNAME_INPUT_NAME"
    :provide-key="provideKey"
    :rules="{
      required: t('validation.required', { field_name: t('auth.username.label') }),
      minLength: {
        value: 2,
        message: t('validation.min_length', { min_length: USERNAME_MIN_LENGTH }),
      },
    }"
  >
    <template #default="{ name, value, error, onChange, onBlur }">
      <MyInput
        :error="error"
        :label="t('auth.username.label')"
        :name="name"
        :value="value"
        @blur="onBlur"
        @input="onChange"
      />
    </template>
  </MyController>
  <MyController
    v-if="Boolean(fields[EMAIL_INPUT_NAME])"
    :name="EMAIL_INPUT_NAME"
    :provide-key="provideKey"
    :rules="{
      required: t('validation.required', { field_name: t('auth.email.label') }),
      pattern: { value: EMAIL_REG, message: t('validation.incorrect') },
    }"
  >
    <template #default="{ name, value, error, onChange, onBlur }">
      <MyInput
        :error="error"
        :label="t('auth.email.label')"
        :name="name"
        :value="value"
        @blur="onBlur"
        @input="onChange"
      />
    </template>
  </MyController>
  <MyController
    v-if="Boolean(fields[PASSWORD_INPUT_NAME])"
    :name="PASSWORD_INPUT_NAME"
    :provide-key="provideKey"
    :rules="{
      required: t('validation.required', { field_name: t('auth.password.label') }),
    }"
  >
    <template #default="{ name, value, error, onChange, onBlur }">
      <MyInput
        :error="error"
        :label="t('auth.password.label')"
        :name="name"
        :value="value"
        type="password"
        @blur="onBlur"
        @input="onChange"
      />
    </template>
  </MyController>
</template>

<script setup>
import { MyController, MyInput } from 'components';
import {
  EMAIL_INPUT_NAME,
  PASSWORD_INPUT_NAME,
  USERNAME_INPUT_NAME,
  USERNAME_MIN_LENGTH,
} from 'config/AuthForm/constants.js';
import { useI18n } from 'vue-i18n';

import { EMAIL_REG } from '../../../config/constants.js';

const { t } = useI18n();

defineProps({
  provideKey: {
    type: String,
    required: true,
  },
  fields: {
    type: Object,
    default: () => ({
      [USERNAME_INPUT_NAME]: true,
      [EMAIL_INPUT_NAME]: true,
      [PASSWORD_INPUT_NAME]: true,
    }),
    validator: (value = {}) => {
      return (
        typeof value === 'object' &&
        value !== null &&
        !Array.isArray(value) &&
        Object.values(value).every((v) => v === true)
      );
    },
  },
});
</script>

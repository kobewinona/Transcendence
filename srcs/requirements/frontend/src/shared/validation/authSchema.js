import * as yup from 'yup';

export function createRules(t, { strictPassword = true } = {}) {
  const basePasswordRule = yup
    .string()
    .required(t('validation.required', { field_name: t('auth.password.label') }));

  const strongPasswordRule = basePasswordRule
    .min(6, t('validation.min_length', { field_name: t('auth.password.label'), min_length: 6 }))
    .matches(/[^A-Za-z0-9]/, t('validation.must_include_special_characters'));

  return {
    email: yup
      .string()
      .required(t('validation.required', { field_name: t('auth.email.label') }))
      .email(t('generic.validation.email_invalid')),

    password: strictPassword ? strongPasswordRule : basePasswordRule,

    username: yup
      .string()
      .required(t('validation.required', { field_name: t('auth.username.label') }))
      .min(2, t('validation.min_length', { field_name: t('auth.username.label'), min_length: 2 })),
  };
}

export function signinSchema(t, options = {}) {
  const { email, password } = createRules(t, options);
  return yup.object({ email, password });
}

export function signupSchema(t, options = {}) {
  const { email, password, username } = createRules(t, options);
  return yup.object({ username, email, password });
}

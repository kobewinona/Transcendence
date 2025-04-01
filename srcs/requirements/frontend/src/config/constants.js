export const API_HOST = import.meta.env.VITE_API_URL;
export const WS_HOST = import.meta.env.VITE_WS_URL;

export const MS_PER_SEC = 1000;

export const EMAIL_STORAGE_KEY = 'email';
export const ACCESS_TOKEN_STORAGE_KEY = 'access_token';

export const LANG_OPTIONS = (t) => [
  { value: 'en-US', label: t('english') },
  { value: 'fr-FR', label: t('french') },
  { value: 'th-TH', label: t('thai') },
  { value: 'ru-RU', label: t('russian') },
];

export const VALID_INPUT_TYPES = [
  'text',
  'email',
  'password',
  'number',
  'tel',
  'url',
  'search',
  'date',
  'datetime-local',
  'month',
  'week',
  'time',
  'color',
  'file',
  'checkbox',
  'radio',
  'range',
  'hidden',
  'button',
  'submit',
  'reset',
];

export const EMAIL_REG =
  /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

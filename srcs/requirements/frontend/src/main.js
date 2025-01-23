import '@dzangolab/vue-country-flag-icon/dist/CountryFlag.css';
import './vendor/normalize.css';
import './vendor/fonts/lexend_exa/lexend_exa.css';
import './styles.css';
import './assets/styles/global.css';

import CountryFlag from '@dzangolab/vue-country-flag-icon';
import { createApp } from 'vue';
import { createI18n } from 'vue-i18n';

import App from './App.vue';
import en from './locales/en.json';
import ru from './locales/ru.json';
import th from './locales/th.json';
import { svgComponents } from './shared/lib';

export const i18n = createI18n({
  locale: localStorage.getItem('lang'),
  fallbackLocale: 'en',
  legacy: false,
  messages: {
    en,
    ru,
    th,
  },
});

const app = createApp(App);

Object.entries(svgComponents).forEach(([name, component]) => {
  // noinspection JSCheckFunctionSignatures
  app.component(name, component);
});

app.component('CountryFlag', CountryFlag);

app.use(i18n);
app.mount('#app');

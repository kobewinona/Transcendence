import '@dzangolab/vue-country-flag-icon/dist/CountryFlag.css';
import './vendor/normalize.css';
import './vendor/fonts/overpass/overpass.css';
import './vendor/fonts/silkscreen/silkscreen.css';
import './assets/styles/global.css';
import './styles.css';

import CountryFlag from '@dzangolab/vue-country-flag-icon';
import { all } from '@vee-validate/rules';
import { defineRule } from 'vee-validate';
import { createApp } from 'vue';
import { createI18n } from 'vue-i18n';

import App from './App.vue';
import en from './locales/en.json';
import fr from './locales/fr.json';
import ru from './locales/ru.json';
import th from './locales/th.json';
import router from './router';
import { svgComponents } from './shared/lib';

Object.entries(all).forEach(([name, rule]) => {
  defineRule(name, rule);
});

export const i18n = createI18n({
  locale: localStorage.getItem('lang'),
  fallbackLocale: 'en-US',
  legacy: false,
  escapeParameterHtml: false,
  interpolation: { escapeValue: false, defaultVariables: {} },
  messages: {
    en,
    fr,
    th,
    ru,
  },
});

const app = createApp(App);

Object.entries(svgComponents).forEach(([name, component]) => {
  // noinspection JSCheckFunctionSignatures
  app.component(name, component);
});

app.component('CountryFlag', CountryFlag);

app.use(i18n);
app.use(router);
app.mount('#app');

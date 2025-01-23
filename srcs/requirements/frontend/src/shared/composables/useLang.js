import { inject, provide } from 'vue';

const useLang = (i18n) => {
  const changeLang = (newLang) => {
    i18n.global.locale.value = newLang;
    localStorage.setItem('lang', newLang);
  };

  return {
    i18n,
    changeLang,
  };
};

export const provideLang = (i18nInstance) => {
  provide('lang', useLang(i18nInstance));
};

export const useLangInject = () => {
  const context = inject('lang');
  if (!context) {
    throw new Error('useLang must be used within provideLang');
  }
  return context;
};

export default useLang;

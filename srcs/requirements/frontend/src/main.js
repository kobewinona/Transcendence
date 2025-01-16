import './style.css';
import './assets/styles/global.css';

import { svgComponents } from 'assets/svgComponents.js';
import { createApp } from 'vue';

import App from './App.vue';

const app = createApp(App);

Object.entries(svgComponents).forEach(([name, component]) => {
  // noinspection JSCheckFunctionSignatures
  app.component(name, component);
});

// Mount the app
app.mount('#app');

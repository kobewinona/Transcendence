import { MainPage, OtpPage, SigninPage, SignupPage } from 'pages';
import { auth } from 'store/auth.js';
import { createRouter, createWebHistory } from 'vue-router';

import { EMAIL_STORAGE_KEY } from './config/constants.js';

const routes = [
  {
    path: '/',
    component: MainPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/signup',
    component: SignupPage,
    meta: { guestOnly: true },
  },
  {
    path: '/otp',
    component: OtpPage,
    meta: { guestOnly: true },
  },
  {
    path: '/signin',
    component: SigninPage,
    meta: { guestOnly: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const email = sessionStorage.getItem(EMAIL_STORAGE_KEY);
  const accessToken = to.query.access_token;

  if (accessToken) {
    auth.login(accessToken);
    return next('/');
  }

  if (to.meta.requiresAuth && !auth.isAuthorized) {
    return next('/signin');
  } else if (to.path === '/otp' && !email) {
    next('/signin');
  }

  if (to.meta.guestOnly && auth.isAuthorized) {
    return next('/', { replace: true });
  }

  next(); // Allow navigation
});

export default router;

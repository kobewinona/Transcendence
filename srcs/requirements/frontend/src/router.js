import { MainPage, OtpPage, SigninPage, SignupPage } from 'pages';
import { auth } from 'store/auth';
import { createRouter, createWebHistory } from 'vue-router';

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
  const username = sessionStorage.getItem('username');

  if (to.meta.requiresAuth && !auth.isAuthorized) {
    return next('/signin');
  } else if (to.path === '/otp' && !username) {
    next('/signin');
  }

  if (to.meta.guestOnly && auth.isAuthorized) {
    return next('/', { replace: true });
  }

  next(); // Allow navigation
});

export default router;

import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '@/pages/LoginPage/LoginPage.vue';
import Game from '@/features/Game/Game.vue';
import RegisterPage from '@/pages/RegisterPage/RegisterPage.vue';
import MainPage from '@/pages/MainPage/MainPage.vue';
import NotFound from '@/pages/NotFound.vue';
import { getToken, isAuthenticated } from '@/components/tokenUtils';
import axios from 'axios';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Login',
      component: LoginPage,
      meta: { requiresAuth: false }
    },
    {
      path: '/register',
      name: 'Register',
      component: RegisterPage,
      meta: { requiresAuth: false }
    },
    {
      path: '/mainpage',
      name: 'MainPage',
      component: MainPage,
      meta: { requiresAuth: true }
    },
    {
      path: '/game',
      name: 'Game',
      component: Game,
      meta: { requiresAuth: true }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: NotFound
    }
  ]
});

router.beforeEach(async (to, from, next) => {
  // if the route requires authentication
  if (to.meta.requiresAuth) {
    try {
      //cookies
      const token = await getToken();
      if (!token || !isAuthenticated()) {
        return next({ name: 'Login' });
      }
      return next();
    } catch (error) {
      console.error('Error during authentication check:', error);
      return next({ name: 'Login' });
    }
  }
  return next();
});

export default router;
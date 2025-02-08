import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '@/pages/LoginPage/LoginPage.vue';
import Game from '@/features/Game/Game.vue';
import RegisterPage from '@/pages/RegisterPage/RegisterPage.vue';
import NotFound from '@/pages/NotFound.vue';
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
  if (to.meta.requiresAuth) {
    try {
      const response = await axios.get('/api/auth-status/');
      if (!response.data.isAuthenticated) {
        next('/');
        console.log('laize bastard');
      } else {
        next();
      }
    } catch (error) {
      console.error('Error checking authentication status:', error);
      next('/');
    }
  } else {
    next();
  }
});

export default router;
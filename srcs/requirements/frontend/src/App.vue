<script setup>
import { ref, computed, watchEffect } from 'vue';
import LoginPage from './pages/LoginPage/LoginPage.vue';
import Game from './features/Game/Game.vue';
import NotFound from './pages/NotFound.vue';

// Reactive authentication state
const isAuthenticated = ref(localStorage.getItem('authToken') !== null);

// Define routes
const routes = {
  '/': LoginPage,
  '/game': Game,
};

// Reactive current path
const currentPath = ref(window.location.hash || '#/');

// Route guard logic
const checkAuth = (path) => {
  if (path === '#/game' && !isAuthenticated.value) {
    window.location.hash = '#/';
    return false;
  }
  return true;
};

// Update the path when the hash changes
window.addEventListener('hashchange', () => {
  if (checkAuth(window.location.hash)) {
    currentPath.value = window.location.hash;
  }
});

// Determine the current component based on the path
const currentView = computed(() => {
  const path = currentPath.value.slice(1); // Remove `#`
  return routes[path] || NotFound;
});

// Handle login/logout state changes
const updateAuthStatus = (loggedIn) => {
  isAuthenticated.value = loggedIn;
  if (!loggedIn) {
    localStorage.removeItem('authToken');
    window.location.hash = '#/';
  }
};

</script>

<template>
  <nav>
    <a href="#/">Login</a> |
    <a href="#/game" v-if="isAuthenticated">Game</a>
    <a v-else style="color: #666; cursor: not-allowed">Game</a>
    <template v-if="isAuthenticated">
      | <button @click="updateAuthStatus(false)">Logout</button>
    </template>
  </nav>
  <main class="layout">
    <!-- Pass auth methods to login component -->
    <component 
      :is="currentView" 
      @login-success="updateAuthStatus(true)"
    />
  </main>
</template>

<style scoped>
.layout {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 100%;
  height: 100%;
}
nav {
  margin-bottom: 20px;
}

a {
  text-decoration: none;
  color: #007bff;
}

a:hover {
  text-decoration: underline;
}
</style>
<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const isAuthenticated = ref(!!localStorage.getItem('access_token'));

// You can use this function to update authentication state
const updateAuthState = () => {
  isAuthenticated.value = !!localStorage.getItem('access_token');
};
</script>

<template>
  <nav>
    <router-link to="/">Login</router-link> |
    <router-link to="/register">Register</router-link> |
    <router-link 
      v-if="isAuthenticated"
      to="/game"
    >
      Game
    </router-link>
    <a 
      v-else 
      class="disabled-link"
    >
      Game
    </a>
  </nav>
  
  <main class="layout">
    <router-view v-slot="{ Component }">
      <component :is="Component" />
    </router-view>
  </main>
</template>

<style scoped>
.layout {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 20px;
}

nav {
  margin-bottom: 2rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

a {
  text-decoration: none;
  color: #007bff;
  margin: 0 0.5rem;
  transition: color 0.3s ease;
}

a:hover {
  color: #0056b3;
  text-decoration: underline;
}

.disabled-link {
  color: #6c757d;
  cursor: not-allowed;
  margin: 0 0.5rem;
}
</style>











<!-- <script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
// import { useAuthStore } from '@/store/auth';
import axios from 'axios';

const router = useRouter();
// const authStore = useAuthStore();

// Reactive authentication state
const isAuthenticated = computed(() => authStore.isAuthenticated);

// Handle logout
const handleLogout = async () => {
  try {
    const response = await axios.post('/api/logout/', {});
    if (response.data && response.data.message === 'logged out') {
      // Clear local storage access token
      localStorage.removeItem('access_token');
      // Redirect to login page
      router.push('/');
    } else {
      console.error('Logout failed');
    }
  } catch (error) {
    console.error('Error during logout:', error);
  }
};
</script>

<template>
  <nav>
    <router-link to="/">Login</router-link> |
    <router-link to="/register">Register</router-link> |
    <router-link 
      v-if="isAuthenticated"
      to="/game"
    >
      Game
    </router-link>
    <a 
      v-else 
      class="disabled-link"
    >
      Game
    </a>
    
    <template v-if="isAuthenticated">
      | <button @click="handleLogout">Logout</button>
    </template>
  </nav>
  
  <main class="layout">
    <router-view v-slot="{ Component }">
      <component :is="Component" />
    </router-view>
  </main>
</template>

<style scoped>
.layout {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 20px;
}

nav {
  margin-bottom: 2rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

a {
  text-decoration: none;
  color: #007bff;
  margin: 0 0.5rem;
  transition: color 0.3s ease;
}

a:hover {
  color: #0056b3;
  text-decoration: underline;
}

.disabled-link {
  color: #6c757d;
  cursor: not-allowed;
  margin: 0 0.5rem;
}

button {
  background: #dc3545;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s ease;
}

button:hover {
  background: #bb2d3b;
}
</style> -->
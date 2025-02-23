<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { setToken, unsetToken, getToken, getTokenPayload } from '@/components/tokenUtils';

const router = useRouter();
const checkToken = async () => {
        const token = await getToken()
        const payload = await getTokenPayload()
        if (!token || !payload)
            router.push('/signup')
	}
</script>

<template>
  <nav>
    <router-link to="/">Login</router-link> |
    <router-link to="/register">Register</router-link> |
    <router-link v-if="isAuthenticated" to="/game">
      Game
    </router-link>
    <a v-else class="disabled-link">
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

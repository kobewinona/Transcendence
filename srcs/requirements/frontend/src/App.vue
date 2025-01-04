<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import HelloWorld from './components/HelloWorld.vue'

// Reactive state for WebSocket data
const socketMessage = ref('')
let socket = null

// Function to initialize WebSocket connection
const initializeWebSocket = () => {
  console.log('window.location.protocol', window?.location?.protocol);
  const socketUrl = window.location.protocol === 'https:'
    ? 'wss://localhost/ws/pong/'
    : 'ws://localhost/ws/pong/';
  console.log('socketUrl', socketUrl);

  socket = new WebSocket(socketUrl);

  socket.onopen = () => {
    console.log('✅ WebSocket connected');
    socket.send(JSON.stringify({
      position: { x: 50, y: 50 },
      velocity: { x: 0, y: 0 }
    }));
  };

  socket.onmessage = (event) => {
    console.log('📨 Message from server:', event.data);
    socketMessage.value = event.data;
  };

  socket.onerror = (error) => {
    console.error('❌ WebSocket error:', error);
  };

  socket.onclose = (event) => {
    console.log('🔌 WebSocket disconnected:', event.reason);
  };
};

// Cleanup WebSocket connection
const closeWebSocket = () => {
  if (socket) {
    socket.close()
    console.log('🔌 WebSocket connection closed')
  }
}

// Lifecycle hooks
onMounted(() => {
  initializeWebSocket()
})

onUnmounted(() => {
  closeWebSocket()
})
</script>

<template>
  <div>
    <a href="https://vite.dev" target="_blank">
      <img src="/vite.svg" class="logo" alt="Vite logo" />
    </a>
    <a href="https://vuejs.org/" target="_blank">
      <img src="./assets/vue.svg" class="logo vue" alt="Vue logo" />
    </a>
  </div>
  <HelloWorld msg="Vite + Vue" />
  <div>
    <h2>WebSocket Message:</h2>
    <pre>{{ socketMessage }}</pre>
  </div>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>

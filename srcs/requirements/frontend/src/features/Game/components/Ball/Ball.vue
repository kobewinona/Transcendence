<template>
  <div
    class="ball"
    :style="{
        width: `${width}%`,
        height: `${height}%`,
        top: `${ballPosition.y}%`,
        left: `${ballPosition.x}%`
      }"
  />
  <span class="ball__state">{{ socketMessage }}</span>
</template>

<script setup>
import { ref, onMounted, onUnmounted, defineProps } from 'vue';

const { width, height } = defineProps({
  width: Number,
  height: Number
});

const socketMessage = ref('')
const ballPosition = ref({ x: 50, y: 50 });
let socket = null

const initializeWebSocket = () => {
  const socketUrl = window.location.protocol === 'https:'
    ? 'wss://localhost/ws/pong/'
    : 'ws://localhost/ws/pong/';
  socket = new WebSocket(socketUrl);
  console.log('socket', socket);

  socket.onopen = () => {
    console.log('✅ WebSocket connected');
    console.log(`ballWidth: ${width}, ballHeight: ${height}`);

    if (isNaN(width) || isNaN(height)) {
      console.error('Invalid width or height values:', width, height);
      return;
    }

    // Check if the WebSocket is open (readyState === 1)
    if (socket.readyState === WebSocket.OPEN) {
      try {
        socket.send(JSON.stringify({
          position: { x: 50, y: 50 },
          velocity: { x: 0, y: 0 },
          width,
          height,
        }));
      } catch (error) {
        console.log('Error sending data:', error);
      }
    } else {
      console.error('WebSocket is not open yet');
    }
  };

  socket.onmessage = (event) => {
    console.log('📨 Message from server:', event.data);
    const data = JSON.parse(event.data);
    socketMessage.value = data;
    ballPosition.value = data.position;
  };

  socket.onerror = (error) => {
    console.error('❌ WebSocket error:', error);
  };

  socket.onclose = (event) => {
    console.info('🔌 WebSocket disconnected:', event.reason);
  };
};

const closeWebSocket = () => {
  if (socket) {
    socket.close()
    console.info('🔌 WebSocket connection closed');
  }
}

onMounted(() => {
  initializeWebSocket();
})

onUnmounted(() => {
  closeWebSocket();
})
</script>

<style scoped>
.ball {
  position: absolute;
  border-radius: 50%;
  background-color: white;
  transform: translate(-50%, -50%);
  transition: top 0.1s ease, left 0.1s ease;
}
.ball__state {
  font-family: 'Monospaced', sans-serif;
  font-size: 0.8rem;
  font-weight: 400;
  opacity: 0.2;
}
</style>

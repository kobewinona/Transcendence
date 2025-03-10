<template>
  <Teleport to="body">
    <div class="notifications-container">
      <transition-group name="fade-slide">
        <MyMessage
          v-for="(alert, index) in alerts"
          :key="index"
          :message="alert.message"
          :type="alert.type"
        />
      </transition-group>
    </div>
  </Teleport>
</template>

<script setup>
import { MyMessage } from 'shared/components';
import { ref } from 'vue';

const alerts = ref([]);

const notify = (message, type = 'success', duration = 2000) => {
  const alert = { message, type };

  alerts.value.push(alert);

  setTimeout(() => {
    alerts.value.shift();
  }, duration);
};

defineExpose({ notify });
</script>

<!--suppress CssUnusedSymbol -->
<style scoped>
.notifications-container {
  position: fixed;
  z-index: 1000;
  top: 5%;
  left: 50%;
  transform: translateX(-50%);

  display: flex;
  flex-direction: column;
  gap: 10px;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition:
    transform 0.5s ease,
    opacity 0.5s ease;
}

.fade-slide-enter-from {
  transform: translateY(-30px);
  opacity: 0;
}

.fade-slide-leave-to {
  transform: translateY(30px);
  opacity: 0;
}
</style>

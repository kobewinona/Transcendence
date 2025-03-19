<template>
  <Teleport to="body">
    <transition name="fade" mode="in-out">
      <div v-if="isOpen" class="modal-backdrop" @click.self="close">
        <div class="modal-content">
          <slot></slot>
        </div>
      </div>
    </transition>
  </Teleport>
</template>

<script setup>
defineProps({
  isOpen: Boolean,
});

const emit = defineEmits(['close']);

const close = () => {
  emit('close');
};
</script>

<!--suppress CssUnusedSymbol -->
<style scoped>
.modal-backdrop {
  position: fixed;
  z-index: 1000;
  inset: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  background: rgb(0 0 0 / 0.5);
}

.modal-content {
  position: relative;

  min-width: 300px;
  max-width: 40%;
  padding: 20px;

  color: var(--dark-color);

  background-color: var(--light-color);
  border-radius: 8px;
  box-shadow: 0 4px 6px rgb(0 0 0 / 0.1);
}

.modal-close {
  cursor: pointer;

  position: absolute;
  top: 10px;
  right: 15px;

  font-size: 24px;

  background: none;
  border: none;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

<template>
  <Teleport to="body">
    <transition name="fade" mode="in-out">
      <div v-if="isOpen" class="modal" @click.self="close">
        <div
          :class="[
            'modal-content',
            `modal-content_color_${color}`,
            `modal-content_layout_${layout}`,
          ]"
        >
          <slot></slot>
        </div>
      </div>
    </transition>
  </Teleport>
</template>

<script setup>
defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
  layout: {
    type: String,
    default: 'default',
    validator: (value) => value === 'default' || value === 'full',
  },
  color: {
    type: String,
    default: 'light',
    validator: (value) => value === 'light' || value === 'dark',
  },
});

const emit = defineEmits(['close']);

const close = () => {
  emit('close');
};
</script>

<!--suppress CssUnusedSymbol -->
<style scoped>
.modal {
  position: fixed;
  z-index: 1000;
  inset: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  background: var(--dark-color-opacity-50);
}

.modal-content {
  position: relative;

  min-width: 300px;
  max-width: 40%;

  border-radius: 16px;
  box-shadow: 0 4px 6px rgb(0 0 0 / 0.1);
}

.modal-content_layout_default {
  padding: var(--big-space);
}

.modal-content_layout_full {
  padding: 0;
}

.modal-content_color_light {
  color: var(--dark-color);
  background-color: var(--light-color);
}

.modal-content_color_dark {
  color: var(--light-color);
  background-color: var(--dark-color);
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

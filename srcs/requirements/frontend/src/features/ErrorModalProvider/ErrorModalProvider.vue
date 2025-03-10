<template>
  <Teleport to="body">
    <MyModal :is-open="modal.isOpen" @close="closeModal">
      <div class="error-modal">
        <component
          :is="svgComponents['RejectedIcon']"
          v-if="isVueComponent(svgComponents['RejectedIcon'])"
          class="error-modal__icon"
        />
        <p class="error-modal__title">{{ modal.title }}</p>
        <div class="error-modal__divider" />
        <p class="error-modal__message">{{ modal.message }}</p>
      </div>
    </MyModal>
  </Teleport>
</template>

<script setup>
import { MyModal } from 'components';
import { isVueComponent, svgComponents } from 'shared/lib';
import { defineExpose, ref } from 'vue';

const modal = ref({
  isOpen: false,
  title: '',
  message: '',
});

const showErrorModal = (title, message) => {
  modal.value = {
    isOpen: true,
    title,
    message,
  };
};

const closeModal = () => {
  modal.value.isOpen = false;
};

defineExpose({ showErrorModal });
</script>

<style scoped>
.error-modal {
  display: flex;
  flex-direction: column;
  row-gap: var(--smaller-space);
  align-items: center;
  justify-content: center;

  width: 100%;
}

.error-modal__divider {
  width: 100%;
  height: 1px;
  background-color: var(--dark-color-opacity-50);
}

.error-modal__title {
  font-size: 1.8rem;
  font-weight: 700;
}

.error-modal__message {
  text-align: center;
}

.error-modal__icon {
  width: 40px;
  height: 40px;
  fill: var(--error-color);
  stroke: var(--error-color);
}
</style>

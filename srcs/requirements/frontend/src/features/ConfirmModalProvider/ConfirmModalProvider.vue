<template>
  <MyModal :is-open="modal.isOpen" @close="closeModal">
    <div class="confirm-modal">
      <p class="confirm-modal__message">{{ modal.message }}</p>
      <p class="confirm-modal__comment">{{ modal.comment }}</p>
      <div class="confirm-modal__controls">
        <MyButton
          class-name="confirm-modal__button"
          type="button"
          color="secondary"
          @click="handleConfirm"
        >
          {{ modal.confirmText }}
        </MyButton>
        <MyButton
          class-name="confirm-modal__button"
          type="button"
          variant="bordered"
          color="dark"
          @click="handleCancel"
        >
          {{ t('cancel') }}
        </MyButton>
      </div>
    </div>
  </MyModal>
</template>

<script setup>
import { MyButton, MyModal } from 'components';
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

const modal = ref({
  isOpen: false,
  message: '',
  comment: '',
  confirmText: '',
  onConfirm: () => {},
  onCancel: () => {},
});

const showConfirmModal = ({
  message,
  confirmText,
  comment = '',
  onConfirm = () => {},
  onCancel = () => {},
}) => {
  modal.value = {
    isOpen: true,
    message,
    confirmText,
    comment,
    onConfirm,
    onCancel,
  };
};

const closeModal = () => {
  modal.value.isOpen = false;
};

const handleConfirm = () => {
  closeModal();
  modal.value.onConfirm();
};

const handleCancel = () => {
  closeModal();
  modal.value.onCancel();
};

defineExpose({ showConfirmModal });
</script>

<style scoped>
.confirm-modal {
  display: flex;
  flex-direction: column;
  row-gap: var(--smaller-space);
  align-items: center;
  justify-content: center;

  width: 100%;
  max-width: 400px;
}

.confirm-modal__divider {
  width: 100%;
  height: 1px;
  background-color: var(--dark-color-opacity-50);
}

.confirm-modal__message {
  font-size: 1.8rem;
  font-weight: 700;
}

.confirm-modal__comment {
  font-size: 1rem;
  color: var(--dark-color-opacity-50);
  text-align: center;
}

.confirm-modal__controls {
  display: flex;
  flex-direction: row;
  column-gap: 10px;
  justify-content: center;

  width: 100%;
}

::v-deep(.confirm-modal__button) {
  min-width: 140px;
}
</style>

<template>
  <MyForm
    :provide-key="NEW_GAME_SETTINGS_FORM_PROVIDE_KEY"
    :initial-values="{
      ...QUICK_START_DEFAULT_GAME_SETTINGS,
      NEW_GAME_GAME_MODE,
    }"
    mode="onBlur"
    @on-submit="handleSubmit"
    @on-error="handleErrors"
  >
    <GameSettings :is-open="isOpen" />
  </MyForm>
</template>

<script setup>
import { MyForm } from 'components';
import {
  NEW_GAME_GAME_MODE,
  NEW_GAME_SETTINGS_FORM_PROVIDE_KEY,
  QUICK_START_DEFAULT_GAME_SETTINGS,
} from 'entities/Game/config/constants.js';
import { GameSettings } from 'features';

defineProps({
  isOpen: {
    type: Boolean,
    required: true,
  },
});

const emit = defineEmits(['on-close', 'on-game-settings-change']);

// const open = computed(() => props.isOpen);

const handleSubmit = (formData = {}) => {
  emit('on-game-settings-change', formData);
  emit('on-close');
};

const handleErrors = (errors) => {
  console.log('errors', errors);
};
</script>

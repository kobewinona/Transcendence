<template>
  <MyForm
    :provide-key="NEW_GAME_SETTINGS_FORM_PROVIDE_KEY"
    :initial-values="NEW_GAME_DEFAULT_GAME_SETTINGS"
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
  BALL_SPEED_INPUT_NAME,
  END_GAME_SCORE_INPUT_NAME,
  GAME_INPUT_NAME,
  GAMEPLAY_INPUT_NAME,
  IS_DEUCE_ON_INPUT_NAME,
  MAX_BALL_CURVE_INPUT_NAME,
  NEW_GAME_DEFAULT_GAME_SETTINGS,
  NEW_GAME_SETTINGS_FORM_PROVIDE_KEY,
  PADDLE_SPEED_INPUT_NAME,
} from 'entities/Game/config/constants.js';
import { GameSettings } from 'features';

defineProps({
  isOpen: {
    type: Boolean,
    required: true,
  },
});

const emit = defineEmits(['on-close', 'on-game-settings-change']);

const handleSubmit = (formData = {}) => {
  const sanitizedFormData = {
    ...formData,
    [GAME_INPUT_NAME]: {
      [END_GAME_SCORE_INPUT_NAME]: formData[GAME_INPUT_NAME][END_GAME_SCORE_INPUT_NAME]?.value,
      [IS_DEUCE_ON_INPUT_NAME]: formData[GAME_INPUT_NAME][IS_DEUCE_ON_INPUT_NAME]?.value,
    },
    [GAMEPLAY_INPUT_NAME]: {
      [BALL_SPEED_INPUT_NAME]: formData[GAMEPLAY_INPUT_NAME][BALL_SPEED_INPUT_NAME]?.value,
      [MAX_BALL_CURVE_INPUT_NAME]: formData[GAMEPLAY_INPUT_NAME][MAX_BALL_CURVE_INPUT_NAME]?.value,
      [PADDLE_SPEED_INPUT_NAME]: formData[GAMEPLAY_INPUT_NAME][PADDLE_SPEED_INPUT_NAME]?.value,
    },
  };
  emit('on-game-settings-change', sanitizedFormData);
  emit('on-close');
};

const handleErrors = (errors) => {
  console.log('errors', errors);
};
</script>

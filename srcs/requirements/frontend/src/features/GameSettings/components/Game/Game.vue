<template>
  <SettingsLayout class-name="game-settings">
    <SettingsSection
      :title="t('game_settings.tabs.game.title')"
      :fields="GAME_SETTINGS_FIELDS"
      @on-change="handleGameChange"
    />
    <SettingsSection
      :title="t('game_settings.tabs.gameplay.title')"
      :fields="GAMEPLAY_SETTINGS_FIELDS"
      @on-change="handleGameplayChange"
    />
  </SettingsLayout>
</template>

<script setup>
import { GAME_INPUT_NAME, GAMEPLAY_INPUT_NAME } from 'entities/Game/config/constants.js';
import { SettingsLayout } from 'layouts';
import { SettingsSection } from 'layouts/SettingsLayout/components';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

import { NEW_GAME_SETTINGS_FORM_PROVIDE_KEY } from 'entities/Game/config/constants.js';
import { inject } from 'vue';

import { GAME_SETTINGS_FIELDS, GAMEPLAY_SETTINGS_FIELDS } from './config/constants.js';
const { setValue } = inject(NEW_GAME_SETTINGS_FORM_PROVIDE_KEY);

const handleGameChange = (name, newValue) => {
  setValue(`${GAME_INPUT_NAME}.${name}`, newValue);
};

const handleGameplayChange = (name, newValue) => {
  setValue(`${GAMEPLAY_INPUT_NAME}.${name}`, newValue);
};
</script>

<style scoped>
::v-deep(.game-settings) {
  display: flex;
  flex-direction: column;
  row-gap: var(--bigger-space);
  width: 70%;
}
</style>

<template>
  <SettingsLayout :width="width">
    <ScrollLayout>
      <div class="game-settings">
        <SettingsSection
          :title="t('game_settings.tabs.game.title')"
          :fields="GAME_SETTINGS_FIELDS"
        />
        <SettingsSection
          :title="t('game_settings.tabs.gameplay.title')"
          :fields="GAMEPLAY_SETTINGS_FIELDS"
        />
      </div>
    </ScrollLayout>
  </SettingsLayout>
</template>

<script setup>
import { ScrollLayout, SettingsLayout } from 'layouts';
import { SettingsSection } from 'layouts/SettingsLayout/components';
import { useI18n } from 'vue-i18n';

import { GAME_SETTINGS_FIELDS, GAMEPLAY_SETTINGS_FIELDS } from './config/constants.js';

const { t } = useI18n();

defineProps({
  width: {
    type: String,
    default: '70%',
  },
});
</script>

<style scoped>
.game-settings {
  display: flex;
  flex-direction: column;
  row-gap: var(--bigger-space);

  width: 100%;
  height: 100%;
}
</style>

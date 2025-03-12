<template>
  <ul class="settings">
    <SettingsLayout class-name="settings__section">
      <SectionTitle :title="t('menu.settings.system')" />
      <div class="settings__item">
        <p class="settings__item-label">{{ t('menu.settings.system.language') }}</p>
        <CarouselSelect
          :value="i18n.global.locale.value"
          :options="options"
          @on-change="handleLangChange"
        >
          <template #renderOption="{ option }">
            <div class="settings__item-lang-option">
              <CountryFlag class="settings__item-lang-flag" :iso="iso" mode="rounded" />
              <span class="settings__item-lang-option-text">{{ option?.label }}</span>
            </div>
          </template>
        </CarouselSelect>
      </div>
    </SettingsLayout>
  </ul>
</template>

<script setup>
import { CarouselSelect } from 'components';
import { LANG_OPTIONS } from 'config';
import { SettingsLayout } from 'layouts';
import { SectionTitle } from 'layouts/SettingsLayout/components/SettingsSection/components';
import { useLangInject } from 'shared/composables';
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
const { i18n, changeLang } = useLangInject();

const iso = computed(() => {
  const currentLocale = i18n.global.locale.value || 'gb';
  const currentLocalePrefix = currentLocale.split('-')[0];

  if (currentLocalePrefix === 'en') {
    return 'GB';
  } else {
    return currentLocalePrefix.toUpperCase();
  }
});

const handleLangChange = (newLang) => {
  changeLang(newLang);
};

const options = computed(() => LANG_OPTIONS(t));
</script>

<!--suppress CssUnusedSymbol -->
<style scoped>
.settings {
  display: flex;
  flex-direction: column;
  row-gap: var(--big-space);

  width: 100%;
  height: 100%;
  padding: 0;

  list-style: none;
}

::v-deep(.settings__section) {
  display: flex;
  flex-direction: column;
  row-gap: var(--smaller-space);
  padding: 0;
}

.settings__item {
  display: flex;
  flex-direction: row;
  column-gap: var(--big-space);
  justify-content: space-between;

  width: 100%;
}

.settings__item-label {
  margin: 0;
}

.settings__item-lang-option {
  display: flex;
  flex-direction: row;
  column-gap: var(--small-space);
  align-items: center;
  justify-content: center;

  min-width: 100px;
}

.settings__item-lang-flag {
  max-height: 15px;
}

.settings__item-lang-option-text {
  text-align: center;
}

.select {
  display: flex;
  flex-direction: row;
  column-gap: var(--small-space);
  align-items: center;
}

.arrow {
  width: 30px;
  height: 30px;
  fill: var(--light-color);
  stroke: var(--light-color);
}

.arrow_left {
  transform: rotate(90deg);
}

.arrow_right {
  transform: rotate(-90deg);
}
</style>

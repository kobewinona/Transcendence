<!--suppress JSFileReferences -->
<template>
  <div class="game-settings">
    <div class="game-settings__controls">
      <NavTabs :tabs="DEFAULT_GAME_SETTINGS_TABS" @on-change="handleTabChange" />
      <MyButton
        class-name="game-settings__start-btn"
        type="submit"
        :disabled="!hasControllersOnBothSides"
        >{{ t('game_settings.start') }}</MyButton
      >
    </div>

    <!-- Active Tab Content -->
    <transition name="fade" mode="out-in">
      <component
        :is="activeComponent"
        v-if="activeComponent && isVueComponent(activeComponent)"
        class="game-settings__content"
        v-bind="dynamicProps"
      />
    </transition>
  </div>
</template>

<script setup>
// noinspection JSUnresolvedReference
import { MyButton, NavTabs } from 'components';
import {
  CONTROLLERS_INPUT_NAME,
  NEW_GAME_SETTINGS_FORM_PROVIDE_KEY,
} from 'entities/Game/config/constants.js';
import { isVueComponent } from 'shared/lib';
import { computed, inject, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';

import { DEFAULT_GAME_SETTINGS_TABS, GAME_SETTINGS_TABS_COMPONENTS } from './config/constans.js';

const { t } = useI18n();

const { isOpen } = defineProps({
  isOpen: {
    type: Boolean,
    required: true,
  },
});

const { getValues, reset } = inject(NEW_GAME_SETTINGS_FORM_PROVIDE_KEY);

const controllers = computed(() => getValues(CONTROLLERS_INPUT_NAME));

const hasControllersOnBothSides = ref(true);
const activeTab = ref(DEFAULT_GAME_SETTINGS_TABS[0]);

const activeComponent = computed(() => {
  const tabComponent = GAME_SETTINGS_TABS_COMPONENTS.find(
    (component) => component.key === activeTab.value.value
  );
  return tabComponent ? tabComponent.component : null;
});

const dynamicProps = computed(() => {
  return {};
});

const handleTabChange = (newTab) => {
  activeTab.value = newTab;
};

watch(
  () => controllers,
  (newControllers) => {
    const hasLeft = newControllers.value.some((controller) => controller.side === 'left');
    const hasRight = newControllers.value.some((controller) => controller.side === 'right');
    hasControllersOnBothSides.value = hasLeft && hasRight;
  },
  { deep: true }
);

watch(
  () => isOpen,
  () => {
    if (!isOpen) {
      reset();
    }
  }
);
</script>

<!--suppress CssUnusedSymbol -->
<style scoped>
.game-settings {
  overflow: hidden;
  display: flex;
  flex-direction: column;
  row-gap: var(--regular-space);

  height: 100%;
}

.game-settings__controls {
  display: flex;
  flex-direction: row;
  column-gap: var(--big-space);
  justify-content: space-between;

  height: 50px;
}

.game-settings__start-btn {
  min-width: 120px;
}

.game-settings__content {
  scrollbar-gutter: stable;
  overflow: hidden auto;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

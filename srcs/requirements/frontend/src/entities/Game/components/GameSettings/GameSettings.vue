<!--suppress JSFileReferences -->
<template>
  <div class="game-settings">
    <div class="game-settings__controls">
      <NavTabs :tabs="tabs" @on-change="handleTabChange" />
      <slot />
    </div>

    <!-- Active Tab Content -->
    <transition name="fade" mode="out-in">
      <div v-if="activeComponent && isVueComponent(activeComponent)" class="game-settings__content">
        <component :is="activeComponent" />
      </div>
    </transition>
  </div>
</template>

<script setup>
// noinspection JSUnresolvedReference
import { NavTabs } from 'components';
import { isVueComponent } from 'shared/lib';
import { computed, ref } from 'vue';

import { DEFAULT_GAME_SETTINGS_TABS, GAME_SETTINGS_TABS_COMPONENTS } from './config/constans.js';

defineProps({
  tabs: {
    type: Array,
    default: DEFAULT_GAME_SETTINGS_TABS,
  },
});

const activeTab = ref(DEFAULT_GAME_SETTINGS_TABS[0]);

const activeComponent = computed(() => {
  const tabComponent = GAME_SETTINGS_TABS_COMPONENTS.find(
    (component) => component.key === activeTab.value.value
  );
  return tabComponent ? tabComponent.component : null;
});

const handleTabChange = (newTab) => {
  activeTab.value = newTab;
};
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
  overflow: auto;
  height: 100%;
  min-height: 0;
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

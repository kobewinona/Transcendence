<template>
  <div class="tournaments">
    <NavTabs :tabs="TOURNAMENT_TABS" @on-change="handleTabChange" />
    <transition name="fade" mode="out-in">
      <component
        :is="activeTabComponent"
        v-if="activeTabComponent && isVueComponent(activeTabComponent)"
        class="tournaments__content"
        :tournaments="tournaments"
        @refetch-tournaments="handleRefetch"
      />
    </transition>
  </div>
</template>

<script setup>
// noinspection JSUnresolvedReference
import { NavTabs } from 'components';
import tournamentsApi from 'entities/Tournaments/api';
import {
  CURRENT_TAB_NAME,
  HISTORY_TAB_NAME,
  TOURNAMENT_TABS,
} from 'entities/Tournaments/config/constants.js';
import { useQuery } from 'shared/composables';
import { isVueComponent, tryParseAnyError } from 'shared/lib';
import { menu } from 'store/menu';
import { computed, inject, ref, watch } from 'vue';

import { CurrentTournament, History } from './components';

const showErrorModal = inject('showErrorModal');

const activeTab = ref(TOURNAMENT_TABS[0]);

const { data: tournaments = [], refetch } = useQuery({
  fetchFn: tournamentsApi.getTournaments,
  options: {
    select: (res) => res?.data || [],
    onError: (error) => {
      menu.reset();
      showErrorModal(error.status, tryParseAnyError(error));
    },
    onSettled: () => menu.release(),
  },
});

const activeTabComponent = computed(() => {
  if (activeTab.value.value === CURRENT_TAB_NAME) {
    return CurrentTournament;
  }

  if (activeTab.value.value === HISTORY_TAB_NAME) {
    return History;
  }

  return null;
});

const handleTabChange = (newTab) => {
  activeTab.value = newTab;
};

const handleRefetch = () => {
  menu.hold();
  refetch();
};

watch(
  () => tournaments,
  (newTournaments) => {
    console.log('newTournaments', newTournaments);
  },
  { deep: true }
);
</script>

<!--suppress CssUnusedSymbol -->
<style scoped>
.tournaments {
  display: grid;
  grid-template-rows: max-content auto;
  row-gap: var(--regular-space);

  width: 100%;
  height: 100%;
  min-height: 0;
}

.tournaments__content {
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

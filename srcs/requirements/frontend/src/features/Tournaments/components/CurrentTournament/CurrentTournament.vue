<template>
  <div>
    <TournamentInProgress
      v-if="!isEmpty(tournamentInProgress)"
      :tournament="tournamentInProgress"
      @refetch-tournaments="emit('refetch-tournaments')"
    />
    <NewTournament v-else @refetch-tournaments="emit('refetch-tournaments')" />
  </div>
</template>

<script setup>
import {
  FINISHED_STATUS_NAME,
  IN_PROGRESS_STATUS_NAME,
} from 'entities/Tournaments/config/constants.js';
import { isEmpty } from 'lodash';
import { menu } from 'store/menu.js';
import { computed, ref, toRaw, watch } from 'vue';
import { MENU_LAYER_KEYS } from 'widgets/Menu/config/constants.js';

import { NewTournament, TournamentInProgress } from './components';

const { tournaments } = defineProps({
  tournaments: {
    type: Array,
    default: () => [],
  },
});

const emit = defineEmits(['refetch-tournaments']);

const unnotifiedTournaments = ref([]);

const tournamentInProgress = computed(() =>
  tournaments?.find(({ status }) => status === IN_PROGRESS_STATUS_NAME)
);

watch(
  () => tournaments,
  (currentTournaments = []) => {
    // Step 1: Remove notified ones
    unnotifiedTournaments.value = unnotifiedTournaments.value.filter((existing) => {
      const updatedTournament = currentTournaments?.find((t) => t.id === existing.id);
      return updatedTournament && !updatedTournament?.notified;
    });

    // Step 2: Add new unnotified ones
    const existingIds = new Set(unnotifiedTournaments.value.map((t) => t.id));

    currentTournaments?.forEach((tournament) => {
      const isUnnotified =
        tournament.status === FINISHED_STATUS_NAME && tournament.winner && !tournament?.notified;

      if (isUnnotified && !existingIds.has(tournament.id)) {
        unnotifiedTournaments.value.push(tournament);
      }
    });
  },
  { immediate: true, deep: true }
);

const showCongratulations = () => {
  unnotifiedTournaments.value.forEach((tournament) =>
    menu.goTo(MENU_LAYER_KEYS.TOURNAMENT_CONGRATS, {
      tournament: toRaw(tournament),
      localAction: async () => {
        await emit('refetch-tournaments');
      },
    })
  );
};

watch(
  () => [unnotifiedTournaments.value, menu.isLoading],
  ([unnotified, isMenuLoading]) => {
    if (unnotified.length && !isMenuLoading) {
      showCongratulations();
    }
  },
  { immediate: true }
);
</script>

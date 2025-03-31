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
import { IN_PROGRESS_STATUS_NAME } from 'entities/Tournaments/config/constants.js';
import { isEmpty } from 'lodash';
import { computed } from 'vue';

import { NewTournament, TournamentInProgress } from './components';

const { tournaments } = defineProps({
  tournaments: {
    type: Array,
    default: () => [],
  },
});

const emit = defineEmits(['refetch-tournaments']);

const tournamentInProgress = computed(() => tournaments?.find(({ status }) => status === IN_PROGRESS_STATUS_NAME));
</script>

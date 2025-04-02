<template>
  <ScrollLayout>
    <div v-if="Boolean(!tournaments?.length)" class="history__placeholder">
      <p>{{ t('tournament.tabs.history.no_tournaments_message') }}</p>
    </div>
    <table v-else class="history">
      <thead>
        <tr>
          <th>{{ t('tournament.tabs.history.table.header.created_at') }}</th>
          <th>{{ t('tournament.tabs.history.table.header.name') }}</th>
          <th>{{ t('tournament.tabs.history.table.header.status') }}</th>
          <th>{{ t('tournament.tabs.history.table.header.winner') }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="tournament in tournamentsList" :key="tournament.id">
          <td>
            {{ dayjs(tournament.created_at).format('DD.MM.YYYY') }}
          </td>
          <td>{{ tournament.name }}</td>
          <td :class="['history__status-cell', `history__status-cell_${tournament.status}`]">
            {{ t(`tournament.tabs.history.table.header.status.${tournament.status}`) }}
          </td>
          <td class="history__winner">
            <component
              :is="svgComponents['TrophyIcon']"
              v-if="isVueComponent(svgComponents['TrophyIcon'])"
              class="history__winner-icon"
            />
            <span>{{ tournament.winner || '-' }}</span>
          </td>
        </tr>
      </tbody>
    </table>
  </ScrollLayout>
</template>

<script setup>
import dayjs from 'dayjs';
import { ScrollLayout } from 'layouts';
import { isVueComponent, svgComponents } from 'shared/lib/index.js';
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

const { tournaments } = defineProps({
  tournaments: {
    type: Array,
    required: true,
  },
});

const tournamentsList = computed(() => tournaments || []);
</script>

<!--suppress CssUnusedSymbol -->
<style scoped>
.history {
  position: relative;

  overflow: hidden;
  display: grid;
  grid-template-columns: max-content 1fr max-content 1fr;
  grid-template-rows: auto;
  gap: var(--smaller-space) var(--bigger-space);

  width: 100%;
  height: max-content;
}

.history thead,
.history tbody,
.history tr {
  display: contents;
}

.history tr {
  text-align: justify;
}

.history tr > th {
  font-size: 1.2rem;
  border-bottom: 1px solid var(--light-color-opacity-50);
}

.history__placeholder {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 100%;
  height: 100%;

  font-size: 1.25rem;
}

.history__status-cell {
  color: var(--light-color);
}

.history__status-cell_in_progress {
  color: var(--secondary-color);
}

.history__status-cell_abandoned {
  color: var(--error-color);
}

.history__status-cell_finished {
  color: var(--success-color);
}

.history__winner {
  display: flex;
  flex-direction: row;
  column-gap: var(--regular-space);
}

.history__winner-icon {
  width: 24px;
  height: 24px;
  fill: var(--light-color);
}
</style>

<template>
  <div class="congratulations">
    <div class="congratulations__inner-container">
      <h2>{{ t('tournament.tabs.current.current_tournament.congratulations.title') }}</h2>
      <div class="congratulations__winner-container">
        <span class="congratulations__winner-name">{{ tournament.winner }}</span>
        <span class="congratulations__winner-message">{{
          t('tournament.tabs.current.current_tournament.tournament_winner', {
            tournament_name: tournament.name,
          })
        }}</span>
        <component
          :is="svgComponents['TrophyIcon']"
          v-if="isVueComponent(svgComponents['TrophyIcon'])"
          class="congratulations__trophy-icon"
        />
      </div>
      <div class="congratulations__final-match">
        <PlayerCard
          :player="finalMatch.left"
          :score="finalMatch.score.left"
          :winner="tournament.winner"
          placement="left"
        />
        <PlayerCard
          :player="finalMatch.right"
          :score="finalMatch.score.right"
          :winner="tournament.winner"
          placement="right"
        />
      </div>
    </div>
    <MyButton type="button" color="light" :loading="isLoading" @click="close">{{
      t('close')
    }}</MyButton>
  </div>
</template>

<script setup>
import { MyButton } from 'components';
import tournamentApi from 'entities/Tournaments/api';
import { PlayerCard } from 'entities/Tournaments/components';
import { useMutation } from 'shared/composables';
import { isVueComponent, svgComponents } from 'shared/lib/index.js';
import { menu } from 'store/menu.js';
import { inject } from 'vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

const notify = inject('notify');

const { props } = defineProps({
  props: {
    type: Object,
    required: true,
  },
});
const { tournament = {}, localAction = () => {} } = props || {};

const finalMatches = tournament?.brackets['Final'] || [];
const finalMatch = finalMatches[0];

const { mutate: onUpdateTournament, isLoading } = useMutation({
  fetchFn: tournamentApi.updateTournament,
  options: {
    onError: () => notify(t('error'), 'error'),
    onSettled: () => localAction(),
  },
});

const close = () => {
  onUpdateTournament({ id: tournament.id, data: { notified: true } });
  menu.goBack();
};
</script>

<style scoped>
@keyframes winner-glow {
  0% {
    text-shadow: 0 0 4px var(--secondary-color);
  }

  100% {
    text-shadow: 0 0 12px #fff8dc;
  }
}

@keyframes trophy-pop {
  0% {
    transform: scale(0.8) rotate(-10deg);
    opacity: 0;
  }

  100% {
    transform: scale(1) rotate(0deg);
    opacity: 1;
  }
}

@keyframes trophy-glow {
  0% {
    filter: drop-shadow(0 0 4px var(--light-color-opacity-50));
  }

  100% {
    filter: drop-shadow(0 0 12px #ffd700);
  }
}

.congratulations {
  display: grid;
  grid-template-rows: auto max-content;
  row-gap: var(--big-space);

  width: 100%;
  max-width: 500px;
  height: 100%;
  margin: 0 auto;
  padding: var(--big-space);

  background-color: var(--dark-color);
  border: 2px solid var(--light-color);
  border-radius: 16px;
}

.congratulations__inner-container {
  display: flex;
  flex-direction: column;
  row-gap: var(--regular-space);
  align-items: center;
  justify-content: center;

  width: 100%;
}

.congratulations__winner-container {
  display: flex;
  flex-direction: column;
  row-gap: var(--small-space);
  align-items: center;

  width: 100%;
}

.congratulations__winner-name {
  font-size: 2.4rem;
  font-weight: 900;
  color: var(--secondary-color);
  text-shadow: 0 2px 4px rgb(0 0 0 / 0.2);

  background: linear-gradient(90deg, var(--secondary-color), var(--primary-color));
  background-clip: text;

  animation: winner-glow 1.8s ease-in-out infinite alternate;

  -webkit-text-fill-color: transparent;
}

.congratulations__winner-message {
  font-size: 1.2rem;
}

.congratulations__final-match {
  display: flex;
  flex-direction: row;
  column-gap: var(--big-space);
  justify-content: center;

  width: 100%;
}

.congratulations__trophy-icon {
  transform-origin: center;

  max-width: 120px;
  max-height: 120px;

  filter: drop-shadow(0 0 4px rgb(255 255 255 / 0.4));

  fill: var(--light-color);

  animation:
    trophy-pop 0.6s ease-out,
    trophy-glow 2s ease-in-out infinite alternate;
}
</style>

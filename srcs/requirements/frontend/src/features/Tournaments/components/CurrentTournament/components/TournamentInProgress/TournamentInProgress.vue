<template>
  <div class="tournament-in-progress">
    <div class="tournament-in-progress__header">
      <h2>{{ tournament.name }}</h2>
      <MyButton :loading="isLoading" type="button" @click="handleAbandonTournament">
        {{ t('tournament.tabs.current.current_tournament.abandon_button.text') }}
      </MyButton>
    </div>
    <div class="tournament-in-progress__body">
      <ScrollLayout>
        <StageBrackets
          :brackets-stack="bracketsStack"
          :final-bracket-index="sortedBracketsStageNames.length - 1"
          @start-game="startGame"
        />
      </ScrollLayout>
      <StageSelect
        :brackets-stage-names="sortedBracketsStageNames"
        :final-bracket="brackets['Final'][0]"
        :final-bracket-index="sortedBracketsStageNames.length - 1"
        @select-stage="handleSelectStage"
        @start-game="startGame"
      />
    </div>
  </div>
</template>

<script setup>
import { MyButton } from 'components';
import { CONTROL_KEYS } from 'entities/Controller/config/constants.js';
import { useGameSocketInject } from 'entities/Game/composables';
import {
  BALL_DESIGN_INPUT_NAME,
  CONTROLLED_BY_AI,
  CONTROLLED_BY_INPUT_NAME,
  CONTROLLERS_INPUT_NAME,
  CONTROLS_INPUT_NAME,
  DEFAULT_DESIGN_SETTINGS,
  GAME_INPUT_NAME,
  GAMEPLAY_INPUT_NAME,
  MODE_INPUT_NAME,
  NAME_INPUT_NAME,
  SIDE_INPUT_NAME,
  TOURNAMENT_GAME_MODE,
  TOURNAMENT_ID,
} from 'entities/Game/config/constants.js';
import tournamentApi from 'entities/Tournaments/api';
import { ABANDONED_STATUS_NAME, TOURNAMENT_NAMES } from 'entities/Tournaments/config/constants.js';
import { ScrollLayout } from 'layouts';
import { useMutation } from 'shared/composables';
import { tryParseAnyError } from 'shared/lib';
import { menu } from 'store/menu.js';
import { inject, reactive, toRaw } from 'vue';
import { useI18n } from 'vue-i18n';

import { StageBrackets, StageSelect } from './components';

const { t } = useI18n();
const showErrorModal = inject('showErrorModal');
const showConfirmModal = inject('showConfirmModal');
const notify = inject('notify');

const gameSocket = useGameSocketInject();

const { tournament } = defineProps({
  tournament: {
    type: Object,
    required: true,
  },
});

const brackets = tournament.brackets || {};
const sortedBracketsStageNames = Object.keys(brackets || {}).sort((a, b) => {
  if (a === 'Final') return 1;
  if (b === 'Final') return -1;

  const getFractionValue = (str) => {
    const [num, denom] = str.split('/').map(Number);
    return num / denom;
  };

  return getFractionValue(a) - getFractionValue(b);
});

const bracketsStack = reactive([toRaw(brackets[sortedBracketsStageNames[0]])]);

const emit = defineEmits(['refetch-tournaments']);

const { mutate: onUpdateTournament, isLoading } = useMutation({
  fetchFn: tournamentApi.updateTournament,
  options: {
    onSuccess: async () => {
      emit('refetch-tournaments');
      notify(t('success', 'success'));
    },
    onError: (error) => {
      showErrorModal(error.status, tryParseAnyError(error));
    },
  },
});

const handleAbandonTournament = () => {
  showConfirmModal({
    message: t('tournament.tabs.current.current_tournament.abandon_message.text'),
    confirmText: t('tournament.tabs.current.current_tournament.abandon_button.text'),
    onConfirm: () =>
      onUpdateTournament({ id: tournament.id, data: { status: ABANDONED_STATUS_NAME } }),
  });
};

const handleSelectStage = (selectedStage, selectedStageIndex) => {
  const selectedBracket = brackets[selectedStage];

  if (selectedStageIndex > bracketsStack.length - 1) {
    bracketsStack.push(selectedBracket);
  } else {
    bracketsStack.pop();
  }
};

const startGame = (pair) => {
  menu.hold();

  const settings = {
    [MODE_INPUT_NAME]: TOURNAMENT_GAME_MODE,
    [TOURNAMENT_ID]: tournament.id,
    [CONTROLLERS_INPUT_NAME]: [
      {
        [SIDE_INPUT_NAME]: 'left',
        [NAME_INPUT_NAME]: pair.left?.[TOURNAMENT_NAMES.PLAYERS_NAME],
        [CONTROLLED_BY_INPUT_NAME]: {
          key: pair.left?.[TOURNAMENT_NAMES.PLAYERS_CONTROLLED_BY],
        },
        [CONTROLS_INPUT_NAME]:
          pair.left?.[TOURNAMENT_NAMES.PLAYERS_CONTROLLED_BY] === CONTROLLED_BY_AI.key
            ? null
            : CONTROL_KEYS['left'][0],
      },
      {
        [SIDE_INPUT_NAME]: 'right',
        [NAME_INPUT_NAME]: pair.right?.[TOURNAMENT_NAMES.PLAYERS_NAME],
        [CONTROLLED_BY_INPUT_NAME]: {
          key: pair.right?.[TOURNAMENT_NAMES.PLAYERS_CONTROLLED_BY],
        },
        [CONTROLS_INPUT_NAME]:
          pair.right?.[TOURNAMENT_NAMES.PLAYERS_CONTROLLED_BY] === CONTROLLED_BY_AI.key
            ? null
            : CONTROL_KEYS['right'][0],
      },
    ],
    [GAME_INPUT_NAME]: tournament[TOURNAMENT_NAMES.GAME],
    [GAMEPLAY_INPUT_NAME]: tournament[TOURNAMENT_NAMES.GAMEPLAY],
    [BALL_DESIGN_INPUT_NAME]: DEFAULT_DESIGN_SETTINGS,
  };

  gameSocket.actions.startGame(settings);
};
</script>

<style scoped>
.tournament-in-progress {
  position: relative;

  display: grid;
  grid-auto-rows: max-content auto;
  row-gap: 14px;

  width: 100%;
  height: 100%;
  min-height: 0;
}

.tournament-in-progress__header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;
}

.tournament-in-progress__body {
  position: relative;
  overflow: hidden;
  width: 100%;
  height: 100%;
}
</style>

<template>
  <form class="new-tournament" novalidate @submit="onSubmit">
    <div class="new-tournament__form">
      <!--      Tournament General Settings Section-->
      <div class="new-tournament__settings">
        <h2 class="new-tournament__title">
          {{ t('tournament.tabs.current.new_tournament_form.tournament.title') }}
        </h2>

        <MyInput
          :label="t('tournament.tabs.current.new_tournament_form.tournament_name.label')"
          :name="TOURNAMENT_NAMES.NAME"
          mode="eager"
          variant="ghost"
        />

        <Game width="100%" />
      </div>

      <!--      Tournament Players List Section-->
      <div class="new-tournament__players">
        <div class="new-tournament__title-container">
          <div class="new-tournament__title-inner-container">
            <h2>
              {{ t('tournament.tabs.current.new_tournament_form.players.title') }}
            </h2>
            <span
              v-if="Boolean(players && players.length > 0)"
              class="new-tournament__players-counter"
              >{{ players.length }}</span
            >
          </div>
          <MyButton
            :icon="svgComponents['AddUserIcon']"
            color="light"
            size="middle"
            type="button"
            @click="addPlayer"
            >{{
              t('tournament.tabs.current.new_tournament_form.players.add_player_button.text')
            }}</MyButton
          >
        </div>
        <ScrollLayout>
          <transition-group class="new-tournament__players-list" name="fade-list" tag="ul">
            <li
              v-for="(player, index) in players"
              :key="player?.key"
              class="new-tournament__player"
            >
              <MyButton
                :disabled="players.length <= 2"
                :icon="svgComponents['RemoveUserIcon']"
                aria-label="Remove player."
                class-name="new-tournament__remove-player-button"
                color="light"
                tabindex="-1"
                type="button"
                @click="() => removePlayer(index)"
              />
              <MyInput
                :label="t('tournament.tabs.current.new_tournament_form.players.player_name.label')"
                :max-length="14"
                :name="`${TOURNAMENT_NAMES.PLAYERS}.${index}.${TOURNAMENT_NAMES.PLAYERS_NAME}`"
                mode="eager"
                variant="ghost"
              />
            </li>
          </transition-group>
        </ScrollLayout>
      </div>
    </div>
    <div class="new-tournament__controls">
      <MyButton :loading="isCreatingTournament" color="secondary" type="submit">{{
        t('tournament.tabs.current.new_tournament_form.submit_button.text')
      }}</MyButton>
    </div>
  </form>
</template>

<script setup>
import { MyButton, MyInput } from 'components';
import { Game } from 'entities/Game/components/GameSettings/components';
import tournamentApi from 'entities/Tournaments/api';
import {
  NEW_PLAYER_DEFAULT_VALUES,
  NEW_TOURNAMENT_DEFAULT_VALUES,
  TOURNAMENT_NAMES,
} from 'entities/Tournaments/config/constants.js';
import { ScrollLayout } from 'layouts';
import { isPlainObject } from 'lodash';
import { useMutation } from 'shared/composables';
import { parseValidationErrors, svgComponents, tryParseAnyError } from 'shared/lib';
import { tournamentSchema } from 'shared/validation';
import { useFieldArray, useForm } from 'vee-validate';
import { inject, watch } from 'vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
const showErrorModal = inject('showErrorModal');
const showConfirmModal = inject('showConfirmModal');
const notify = inject('notify');
import { menu } from 'store/menu.js';

const emit = defineEmits(['refetch-tournaments']);

const { values, handleSubmit, setErrors, validateField } = useForm({
  initialValues: NEW_TOURNAMENT_DEFAULT_VALUES,
  validationSchema: tournamentSchema(t),
});
const { fields: players, push, remove } = useFieldArray(TOURNAMENT_NAMES.PLAYERS);

const { mutate: onCreateTournament, isLoading: isCreatingTournament } = useMutation({
  fetchFn: tournamentApi.createTournament,
  options: {
    onSuccess: async () => {
      emit('refetch-tournaments');
      notify(t('success', 'success'));
    },
    onError: (error) => {
      if (error.status === 400) {
        const serverValidationErrors = parseValidationErrors(error.response?.data) || {};

        if (serverValidationErrors && isPlainObject(serverValidationErrors)) {
          // noinspection JSCheckFunctionSignatures
          setErrors(serverValidationErrors);
        } else {
          showErrorModal(error.status, tryParseAnyError(error));
        }
      } else {
        showErrorModal(error.status, tryParseAnyError(error));
      }
    },
    onSettled: () => menu.release(),
  },
});

const addPlayer = () => {
  push(NEW_PLAYER_DEFAULT_VALUES);
};

const removePlayer = (index) => {
  remove(index);
};

const invalidatePlayers = (formData) => {
  onCreateTournament({ data: formData });
};

function calculatePlayersShortage(playerCount) {
  let nextPowerOfTwo = 2;
  while (nextPowerOfTwo < playerCount) {
    nextPowerOfTwo *= 2;
  }

  return nextPowerOfTwo - playerCount;
}

const onSubmit = handleSubmit((formData) => {
  const playersShortage = calculatePlayersShortage(formData[TOURNAMENT_NAMES.PLAYERS].length);

  if (playersShortage > 0) {
    showConfirmModal({
      message: t('tournament.tabs.current.new_tournament_form.players.not_enough.title'),
      confirmText: t('ok'),
      comment: t('tournament.tabs.current.new_tournament_form.players.not_enough.comment', {
        players_shortage: playersShortage,
      }),
      onConfirm: () => invalidatePlayers(formData),
    });
  } else {
    onCreateTournament({ data: formData });
  }
});

// Re-validate player names
watch(
  () => values.players,
  (players) => {
    if (!Array.isArray(players)) return;

    const nameCounts = players.reduce((acc, player) => {
      const trimmed = player?.name?.trim().toLowerCase();

      if (!trimmed) return acc;
      acc[trimmed] = (acc[trimmed] || 0) + 1;

      return acc;
    }, {});

    const hasDuplicates = Object.values(nameCounts).some((count) => count > 1);

    if (!hasDuplicates) {
      players.forEach((player, index) => {
        const isEmpty = !player.name?.trim();

        if (!isEmpty) {
          // noinspection JSCheckFunctionSignatures
          validateField(`players.${index}.name`);
        }
      });
    }
  }
);
</script>

<!--suppress CssUnusedSymbol -->
<style scoped>
.new-tournament {
  display: flex;
  flex-direction: column;
  row-gap: var(--regular-space);

  width: 100%;
  height: 100%;
  min-height: 0;
}

.new-tournament__form {
  display: grid;
  grid-template-columns: 1fr 1fr;
  column-gap: var(--big-space);

  width: 100%;
  height: 100%;
  min-height: 0;
}

.new-tournament__title {
  text-align: center;
  border-bottom: 1px solid var(--light-color);
}

.new-tournament__settings {
  overflow: hidden;
  display: flex;
  flex-direction: column;
  row-gap: var(--smaller-space);

  width: 100%;
  max-width: 500px;
  height: 100%;
  margin: 0 auto;
}

.new-tournament__players {
  overflow: hidden;
  display: flex;
  flex-direction: column;
  row-gap: var(--smaller-space);

  width: 100%;
  max-width: 400px;
  margin: 0 auto;

  border-radius: 12px;
}

.new-tournament__title-container {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;

  border-bottom: 1px solid var(--light-color);
}

.new-tournament__title-inner-container {
  display: flex;
  flex-direction: row;
  column-gap: var(--small-space);
  align-items: baseline;
}

.new-tournament__players-counter {
  color: var(--light-color-opacity-50);
}

.new-tournament__players-list {
  display: flex;
  flex-direction: column-reverse;
  justify-content: flex-end;

  height: 100%;
  margin: 0;
  padding: 0;

  list-style: none;
}

.new-tournament__player {
  display: flex;
  flex-direction: row;
  column-gap: var(--smaller-space);
  width: 100%;
}

.new-tournament__remove-player-button {
  min-width: 44px;
  padding: var(--small-space);
}

.new-tournament__controls {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.fade-list-move,
.fade-list-enter-active,
.fade-list-leave-active {
  transition: all 0.4s ease;
}

.fade-list-enter-from {
  transform: scale(0.8);
  opacity: 0;
}

.fade-list-enter-to {
  transform: scale(1);
  opacity: 1;
}

.fade-list-leave-active {
  position: absolute;
  z-index: 1;
  width: 100%;
}

.fade-list-leave-from {
  transform: scale(1);
  opacity: 1;
}

.fade-list-leave-to {
  transform: scale(0.8);
  opacity: 0;
}
</style>

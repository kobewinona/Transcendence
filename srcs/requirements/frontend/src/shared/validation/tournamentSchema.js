import { isEqual } from 'lodash';
import * as yup from 'yup';

function createRules(t) {
  return {
    name: yup
      .string()
      .required(
        t('validation.required', {
          field_name: t('tournament.tabs.current.new_tournament_form.tournament_name.label'),
        })
      )
      .min(
        2,
        t('validation.min_length', {
          field_name: t('tournament.tabs.current.new_tournament_form.tournament_name.label'),
          min_length: 2,
        })
      ),

    players: yup.array().of(
      yup.object({
        name: yup
          .string()
          .required(
            t('validation.required', {
              field_name: t(
                'tournament.tabs.current.new_tournament_form.players.player_name.label'
              ),
            })
          )
          .min(
            2,
            t('validation.min_length', {
              field_name: t(
                'tournament.tabs.current.new_tournament_form.players.player_name.label'
              ),
              min_length: 2,
            })
          )
          .test('is-unique', t('validation.tournament.not_unique_player_name'), function (value) {
            const { options, parent, path, createError } = this;
            const players = options?.context?.players || [];

            if (!value || !players.length) return true;

            const currentIndex = players.findIndex((p) => isEqual(p, parent));
            const currentName = value.trim().toLowerCase();

            const duplicateIndex = players.findIndex(
              (p, idx) => idx !== currentIndex && p.name?.trim().toLowerCase() === currentName
            );

            if (duplicateIndex !== -1) {
              return createError({ path, message: this.message });
            }

            return true;
          }),
        controlled_by: yup.string().required(),
      })
    ),
  };
}

function tournamentSchema(t, options = {}) {
  const { name, players } = createRules(t, options);
  return yup.object({ name, players });
}

export default tournamentSchema;

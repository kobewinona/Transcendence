<template>
  <form class="new-game" novalidate @submit="onSubmit">
    <GameSettings :provider-key="NEW_GAME_FORM_PROVIDER_KEY">
      <MyButton
        color="secondary"
        type="submit"
        :icon="svgComponents['GameConsoleIcon']"
        :disabled="!hasControllersOnBothSides"
      >
        {{ t('game_settings.start') }}
      </MyButton>
    </GameSettings>
  </form>
</template>

<script setup>
import { MyButton } from 'components';
import { invalidateControllers } from 'entities/Controller/lib';
import { GameSettings } from 'entities/Game/components';
import { useGameSocketInject } from 'entities/Game/composables';
import {
  CONTROLLERS_INPUT_NAME,
  NEW_GAME_DEFAULT_GAME_SETTINGS,
  NEW_GAME_FORM_PROVIDER_KEY,
} from 'entities/Game/config/constants.js';
import { svgComponents } from 'shared/lib/index.js';
import { menu } from 'store/menu.js';
import { useForm } from 'vee-validate';
import { provide, ref, toRaw, watch } from 'vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

const gameSocket = useGameSocketInject();

const methods = useForm({
  initialValues: NEW_GAME_DEFAULT_GAME_SETTINGS,
  keepValuesOnUnmount: true,
});
const { values, handleSubmit } = methods;

provide(NEW_GAME_FORM_PROVIDER_KEY, methods);

const hasControllersOnBothSides = ref(true);

const onSubmit = handleSubmit((formData) => {
  menu.hold();
  const controllers = formData[CONTROLLERS_INPUT_NAME];

  gameSocket.actions.startGame({
    ...formData,
    [CONTROLLERS_INPUT_NAME]: invalidateControllers(controllers),
  });
});

watch(
  () => values,
  (newValues) => {
    console.info('FORM VALUES', toRaw(newValues));

    const controllers = toRaw(newValues)[CONTROLLERS_INPUT_NAME];

    let leftControllers = 0;
    let rightControllers = 0;

    controllers.forEach(({ side }) => {
      if (side === 'left') leftControllers++;
      else if (side === 'right') rightControllers++;
    });

    hasControllersOnBothSides.value = Boolean(leftControllers > 0 && rightControllers > 0);
  },
  { deep: true }
);
</script>

<style scoped>
.new-game {
  display: contents;
}
</style>

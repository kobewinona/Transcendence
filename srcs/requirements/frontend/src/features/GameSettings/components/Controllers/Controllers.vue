<template>
  <div class="controllers">
    <div class="controllers__side controllers__side_left">
      <transition name="fade" mode="out-in">
        <span
          v-if="!controllers.some((controller) => controller.side === 'left')"
          class="controllers__side-alert"
        >
          {{ t('game_settings.tabs.sides.controllers.not_enough_controllers_message') }}
        </span>
      </transition>
    </div>
    <div class="controllers__side controllers__side_right">
      <transition name="fade" mode="out-in">
        <span
          v-if="!controllers.some((controller) => controller.side === 'right')"
          class="controllers__side-alert"
        >
          {{ t('game_settings.tabs.sides.controllers.not_enough_controllers_message') }}
        </span>
      </transition>
    </div>
    <div class="controllers__container">
      <Controller
        v-for="(controller, index) in controllers"
        :key="index"
        :controller="controller"
        :controller-index="index"
        @on-remove="removeController"
      />
      <button
        v-if="controllers.length < MAX_PLAYERS_AMOUNT"
        class="controllers__add-btn"
        aria-label="Add Controller"
        type="button"
        @click="addController"
      >
        <component
          :is="svgComponents['AddIcon']"
          v-if="isVueComponent(svgComponents['AddIcon'])"
          class="controllers__add-btn-icon"
        />
      </button>
    </div>
  </div>
</template>

<script setup>
import { MAX_PLAYERS_AMOUNT, NEW_CONTROLLER_SETTINGS } from 'entities/Game/config/constants.js';
import {
  CONTROLLERS_INPUT_NAME,
  NEW_GAME_SETTINGS_FORM_PROVIDE_KEY,
} from 'entities/Game/config/constants.js';
import { isVueComponent, svgComponents } from 'shared/lib';
import { computed, inject, reactive } from 'vue';
import { useI18n } from 'vue-i18n';

import { Controller } from './components';

const { t } = useI18n();

const { getValues } = inject(NEW_GAME_SETTINGS_FORM_PROVIDE_KEY);

const controllers = computed(() => getValues(CONTROLLERS_INPUT_NAME));

const addController = () => {
  controllers.value.push(reactive({ ...NEW_CONTROLLER_SETTINGS(controllers.value.length) }));
};

const removeController = (controllerIndex) => {
  const controllersArray = getValues(CONTROLLERS_INPUT_NAME);

  // Ensure controllersArray is reactive
  if (Array.isArray(controllersArray)) {
    controllersArray.splice(controllerIndex, 1);
  }
};
</script>

<!--suppress CssUnusedSymbol -->
<style scoped>
.controllers {
  position: relative;

  display: flex;

  width: 100%;
  height: 100%;

  border: 1px solid var(--light-color-opacity-50);
  border-radius: 12px;
}

.controllers__side {
  position: absolute;
  top: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  width: 50%;
  height: 100%;
}

.controllers__side_left {
  left: 0;
  color: var(--dark-color);
  background-color: var(--light-color);
  border-radius: 12px 0 0 12px;
}

.controllers__side_right {
  right: 0;
  color: var(--light-color);
  background-color: var(--dark-color);
  border-radius: 0 12px 12px 0;
}

.controllers__side-alert {
  width: 60%;
  text-align: center;
}

.controllers__container {
  position: relative;

  display: flex;
  flex-direction: column;
  row-gap: var(--small-space);
  align-items: center;
  justify-content: flex-start;

  width: 50%;
  height: 100%;
  margin: 0 auto;
  padding: var(--regular-space) 0;
}

.controllers__add-btn {
  cursor: pointer;

  width: 40px;
  height: 40px;

  background-color: var(--dark-color);
  border: none;
  border-radius: 50%;
}

.controllers__add-btn-icon {
  width: 40px;
  height: 40px;

  fill: var(--light-color);
  stroke: var(--light-color);

  transition: opacity 0.2s ease-in-out;
}

.controllers__add-btn-icon:hover {
  opacity: 0.7;
  transition: opacity 0.2s ease-in-out;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

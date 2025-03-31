<template>
  <div class="controllers">
    <div class="controllers__side controllers__side_left">
      <transition mode="out-in" name="fade">
        <span
          v-if="!controllers.some((controller) => controller.value.side === 'left')"
          class="controllers__side-alert"
        >
          {{ t('game_settings.tabs.sides.controllers.not_enough_controllers_message') }}
        </span>
      </transition>
    </div>
    <div class="controllers__side controllers__side_right">
      <transition mode="out-in" name="fade">
        <span
          v-if="!controllers.some((controller) => controller.value.side === 'right')"
          class="controllers__side-alert"
        >
          {{ t('game_settings.tabs.sides.controllers.not_enough_controllers_message') }}
        </span>
      </transition>
    </div>
    <div class="controllers__container">
      <TransitionGroup class="controllers-list" name="controller-bubble" tag="div">
        <Controller
          v-for="(controller, index) in controllers"
          :key="index"
          :controller="controller"
          :disabled="controllers.length <= 2"
          :index="index"
          @on-remove="removeController"
        />
      </TransitionGroup>
      <button
        v-if="controllers.length < MAX_PLAYERS_AMOUNT"
        aria-label="Add Controller"
        class="controllers__add-btn"
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
import {
  CONTROLLERS_INPUT_NAME,
  MAX_PLAYERS_AMOUNT,
  NEW_CONTROLLER_SETTINGS,
} from 'entities/Game/config/constants.js';
import { isVueComponent, svgComponents } from 'shared/lib';
import { useFieldArray } from 'vee-validate';
import { useI18n } from 'vue-i18n';

import { Controller } from './components';

const { t } = useI18n();

const { fields: controllers, insert, remove } = useFieldArray(CONTROLLERS_INPUT_NAME);

const addController = () => {
  insert(controllers.value.length, { ...NEW_CONTROLLER_SETTINGS(controllers.value.length) });
};

const removeController = (controllerIndex) => {
  if (controllers.value.length > 2) {
    remove(controllerIndex);
  }
};
</script>

<!--suppress CssUnusedSymbol -->
<style scoped>
.controllers {
  position: relative;

  display: flex;

  width: 100%;
  min-height: 100%;

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

.controllers-list {
  display: contents;
}

.controller-bubble-enter-active {
  transition: all 0.25s ease;
}

.controller-bubble-enter-from {
  transform: scale(0.8);
  opacity: 0;
}

.controller-bubble-enter-to {
  transform: scale(1);
  opacity: 1;
}
</style>

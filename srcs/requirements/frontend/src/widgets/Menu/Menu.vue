<template>
  <div class="menu-layout">
    <transition name="menu-transition" @enter="pulsate" @leave="pulsate">
      <ul v-show="menu.isOpen" class="menu u-list-reset">
        <li class="menu__pulse" />
        <li
          v-for="(row, rowIndex) in MENU_ITEMS()"
          :key="rowIndex"
          :style="{ height: row?.height || '50%' }"
        >
          <ul class="menu__row-list u-list-reset">
            <li
              v-for="item in row.items"
              :key="item.key"
              :class="{ menu__item_opened: menu.layerKey === item.key }"
              class="menu__item"
            >
              <button class="menu__item-button" @click="() => selectMenuItem(item.key)">
                <span class="menu__item-header">
                  <span class="menu__item-title">{{ t(item.title) }}</span>
                  <PlayersBadge
                    v-if="item.minPlayers"
                    :max-players="item.maxPlayers"
                    :min-players="item.minPlayers"
                  />
                </span>
                <span
                  :class="{ 'menu__item-description_short': item.iconSlideTo === 'right' }"
                  class="menu__item-description"
                >
                  {{ t(item.description) }}
                </span>
                <component
                  :is="item.icon"
                  v-if="item.icon"
                  :class="{
                    'menu__item-icon_slide-bottom': item.iconSlideTo === 'bottom',
                    'menu__item-icon_slide-right': item.iconSlideTo === 'right',
                  }"
                  class="menu__item-icon"
                />
              </button>
            </li>
          </ul>
        </li>
      </ul>
    </transition>

    <transition-group
      name="layer-transition"
      tag="div"
      @enter="handleLayerEnter"
      @after-enter="handleLayerAfterEnter"
      @after-leave="handleLayerAfterLeave"
    >
      <div
        v-for="(layer, index) in menu.layers"
        v-show="menu.isOpen && Boolean(layer.content)"
        :key="layer.key"
        :data-layer="JSON.stringify(layer)"
        :style="{
          zIndex: 91 + index,
          transitionDelay: `${layer.key === MENU_LAYER_KEYS.LOADING ? 0 : 0.2 + index * 0.2}s`,
        }"
        :class="{ menu__layer: true, 'menu__layer_no-title': !layer.title }"
      >
        <div v-if="layer.title" class="menu__later-header">
          <h2>{{ t(layer.title) }}</h2>
          <MyButton
            :icon="svgComponents['DeclineIcon']"
            aria-label="Close Menu."
            icon-class-name="menu__layer-close-btn-icon"
            type="button"
            variant="ghost"
            @click="() => menu.goBack()"
          />
        </div>
        <component
          :is="layer.content"
          v-if="layer.key === MENU_LAYER_KEYS.LOADING || shownLayers.has(layer.key)"
          :icon="layer.icon"
          :props="layer.props"
        />
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { MyButton, PlayersBadge } from 'components';
import { svgComponents } from 'shared/lib';
import { menu } from 'store/menu';
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';

import { MENU_ITEMS, MENU_LAYER_KEYS } from './config/constants.js';

const { t } = useI18n();

const emit = defineEmits(['on-menu-select']);

const shownLayers = ref(new Set());

function handleLayerEnter(el) {
  const layer = JSON.parse(el.dataset.layer);
  if (layer.loadingRequired === true) menu.hold();
}

function handleLayerAfterEnter(el) {
  const layer = JSON.parse(el.dataset.layer);
  if (layer.key) shownLayers.value.add(layer.key);
}

function handleLayerAfterLeave(el) {
  const layer = JSON.parse(el.dataset.layer);
  if (layer.key) shownLayers.value.delete(layer.key);
}

const selectMenuItem = (selectedItemKey) => {
  menu.goTo(selectedItemKey);
  emit('on-menu-select', selectedItemKey);
};

const pulsate = (el) => {
  const childEl = el.children[0];
  childEl.classList.add('pulsate');
  setTimeout(() => childEl.classList.remove('pulsate'), 400);
};
</script>

<!--suppress CssUnusedSymbol -->
<style scoped>
@keyframes pulsate {
  0% {
    transform: scaleY(1) scale(1);
    opacity: 0;
  }

  30% {
    opacity: 1;
  }

  100% {
    transform: scaleY(1.05) scaleX(1.2);
    opacity: 0;
  }
}

.menu-layout {
  position: absolute;
  z-index: 90;
  top: 0;
  left: 0;

  width: 100%;
  height: 100%;
}

.u-list-reset {
  list-style: none;
}

.menu {
  position: absolute;
  z-index: 90;
  top: 0;
  left: 0;

  display: flex;
  flex-direction: column;
  row-gap: var(--smaller-space);

  width: 100%;
  height: 100%;
  padding: 2px;

  border-radius: 12px;
}

.menu__pulse {
  position: absolute;
  top: 0;
  left: 0;

  width: 100%;
  height: 100%;

  opacity: 0;
  background-color: var(--dark-color-opacity-70);
  border-radius: 14px;
}

.pulsate {
  animation: pulsate 0.2s ease-in-out;
}

.menu__row-list {
  display: flex;
  flex-direction: row;
  column-gap: var(--smaller-space);
  height: 100%;
}

.menu__item {
  user-select: none;

  position: relative;

  display: flex;
  flex: 1;
  flex-direction: column;
  row-gap: var(--smaller-space);

  height: 100%;

  background-color: var(--dark-color-opacity-90);
  border-radius: 12px;

  transition: all 0.4s ease-in-out;
}

.menu__item:hover:not(.menu__item_opened) {
  flex: 2;
  background-color: var(--dark-color);
}

.menu__item_opened {
  flex: 0;
  width: 0;
  margin-left: calc(0px - var(--smaller-space));
}

.menu__item-button {
  cursor: pointer;

  position: relative;

  overflow: hidden;
  display: flex;
  flex-direction: column;
  row-gap: var(--small-space);

  height: 100%;
  padding: var(--regular-space);

  background-color: var(--light-color-opacity-10);
  border: none;
  border-radius: 12px;

  transition:
    transform 0.1s ease-in-out,
    box-shadow 0.1s ease-in-out;
}

.menu__item-button:disabled {
  cursor: not-allowed;
}

.menu__item-header {
  display: flex;
  flex-direction: row;
  column-gap: var(--regular-space);
  justify-content: space-between;

  width: 100%;
}

.menu__item-title {
  margin: 0;
  font-size: 2em;
  font-weight: 900;
}

.menu__item-description {
  height: 0;

  font-size: 1.4rem;
  font-weight: 300;
  text-align: left;

  opacity: 0;

  transition: opacity 0s ease-in-out;
}

.menu__item-description_short {
  max-width: 60%;
}

.menu__item:hover .menu__item-description {
  opacity: 1;
  transition: opacity 0.4s ease-in-out 0.3s;
}

.menu__item-icon {
  position: absolute;
  top: 60%;
  left: 50%;
  transform: translate(-50%, -50%);

  aspect-ratio: 1 / 1;
  max-width: 40%;
  max-height: 40%;
  margin: 0 auto;

  fill: var(--light-color);
  stroke: var(--light-color);

  transition: all 0.2s ease-in-out;
}

.menu__item:hover .menu__item-icon_slide-bottom {
  top: 70%;
}

.menu__item:hover .menu__item-icon_slide-right {
  left: 80%;
}

.menu__layer {
  position: absolute;
  inset: 0;

  display: grid;
  grid-template-rows: max-content auto;
  row-gap: var(--big-space);

  width: 100%;
  height: 100%;
  padding: var(--big-space);

  background-color: var(--dark-color-opacity-95);
  border-radius: 12px;
}

.menu__layer_no-title {
  grid-template-rows: auto;
}

.menu__later-header {
  display: flex;
  flex-direction: row;
  column-gap: var(--regular-space);
  justify-content: space-between;

  width: 100%;
}

::v-deep(.menu__layer-close-btn-icon) {
  width: 44px;
  height: 44px;
}

.menu-transition-enter-active,
.menu-transition-leave-active,
.layer-transition-enter-active,
.layer-transition-leave-active {
  transform-origin: center;
  transition:
    transform 0.4s cubic-bezier(0.22, 1, 0.36, 1),
    opacity 0.4s ease;
}

.menu-transition-enter-from,
.layer-transition-enter-from {
  transform: scale(1.15) translateY(20px);
  opacity: 0;
}

.menu-transition-enter-to,
.layer-transition-enter-to {
  transform: scale(1) translateY(0);
  opacity: 1;
}

.menu-transition-leave-from,
.layer-transition-leave-from {
  transform: scale(1) translateY(0);
  opacity: 1;
}

.menu-transition-leave-to,
.layer-transition-leave-to {
  transform: scale(1.15) translateY(20px);
  opacity: 0;
}
</style>

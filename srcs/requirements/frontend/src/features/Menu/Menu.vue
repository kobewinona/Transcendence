<template>
  <div
    v-show="!isMenuHidden"
    class="menu"
    :class="{ menu_open: isOpen }"
    :style="{
      '--menu-container-width': `${menuContainerWidth}px`,
      '--menu-container-height': `${menuContainerHeight}px`,
    }"
    @transitionend="onTransitionEnd"
  >
    <ul ref="menuContainerRef" class="menu__container">
      <li
        v-for="(row, rowIndex) in MENU_ITEMS"
        :key="rowIndex"
        class="menu__row"
        :style="{ height: row.height || '50%' }"
      >
        <ul class="menu__list">
          <li
            v-for="(item, itemIndex) in row.items"
            :key="itemIndex"
            :ref="(el) => (menuItemRefs[rowIndex][itemIndex] = el)"
            class="menu__item"
            :class="{
              menu__item_row_first: rowIndex === 0,
              menu__item_row_middle: rowIndex > 0 && rowIndex < MENU_ITEMS.length - 1,
              menu__item_row_last: rowIndex === MENU_ITEMS.length - 1,
              menu__item_active: activeRowIndex === rowIndex && activeItemIndex === itemIndex,
              menu__item_opened: menuItemOpenedKey === item.key,
            }"
            @mouseenter="handleMouseEnter"
            @mouseleave="handleMouseLeave"
          >
            <div class="menu__item-content">
              <span class="menu__item-title">{{ item.title }}</span>
              <template v-if="item.content">
                <component :is="item.content" v-if="isVueComponent(item.content)" />
                <span v-else>{{ item.content }}</span>
              </template>
            </div>
            <div class="menu__item-container">
              <button
                class="menu__item-button"
                :class="{ 'menu__item-button_clicked': menuItemClickedKey === item.key }"
                :disabled="item.disabled"
                @click="() => handleMenuOptionSelect(item.key)"
                @animationend="onMenuAnimationEnd"
              >
                <span class="menu__item-title">{{ item.title }}</span>
                <span
                  class="menu__item-description"
                  :class="{ 'menu__item-description_short': item.iconSlideTo === 'right' }"
                >
                  {{ item.description }}
                </span>
                <component
                  :is="item.icon"
                  v-if="item.icon"
                  class="menu__item-icon"
                  :class="{
                    'menu__item-icon_slide-bottom': item.iconSlideTo === 'bottom',
                    'menu__item-icon_slide-right': item.iconSlideTo === 'right',
                  }"
                />
              </button>
            </div>
          </li>
        </ul>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { isVueComponent } from 'shared/lib';
import { onMounted, onUnmounted, onUpdated, ref, watch } from 'vue';

import { MENU_ITEMS } from './config/constants.js';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: true,
  },
});

const emit = defineEmits([
  'on-disable-cursor',
  'on-enable-cursor',
  'on-force-ball-position',
  'on-menu-option-select',
]);

const menuContainerRef = ref(null);
const menuItemRefs = ref(Array.from({ length: MENU_ITEMS.length }, () => []));

const menuContainerWidth = ref(0);
const menuContainerHeight = ref(0);

const isDestroyed = ref(false);
const isMenuHidden = ref(false);
const menuItemClickedKey = ref(null);
const menuItemOpenedKey = ref(null);
const forcedBallPositionUpdateTimeoutId = ref(null);
const menuItemDimensionsUpdateTimoutId = ref(null);
const isMouseInsideMenu = ref(false);

const activeRowIndex = ref(null);
const activeItemIndex = ref(null);
const navigationMethod = ref('');

const updateMenuContainerDimensions = () => {
  // noinspection JSUnresolvedReference
  if (menuContainerRef?.value) {
    menuContainerWidth.value = menuContainerRef.value.offsetWidth;
    menuContainerHeight.value = menuContainerRef.value.offsetHeight;
  }
};

const updateMenuItemDimensions = () => {
  menuItemRefs.value.forEach((row) => {
    row.forEach((item) => {
      if (item) {
        // noinspection JSUnresolvedReference
        const containerBox = menuContainerRef.value.getBoundingClientRect();
        const boundingBox = item?.getBoundingClientRect();
        const top = ((boundingBox.top - containerBox.top) / containerBox.height) * 100;
        const left = ((boundingBox.left - containerBox.left) / containerBox.width) * 100;
        const width = item?.offsetWidth;
        const height = item?.offsetHeight;

        item?.style.setProperty('--menu-item-top', `${top}%`);
        item?.style.setProperty('--menu-item-left', `${left}%`);
        item?.style.setProperty('--menu-item-width', `${width}px`);
        item?.style.setProperty('--menu-item-height', `${height}px`);
      }
    });
  });
};

const closeMenuItem = () => {
  menuItemClickedKey.value = null;
  menuItemOpenedKey.value = null;
  setTimeout(() => (isDestroyed.value = true), 500);
};

const updateForcedBallPosition = (activeElement) => {
  if (!activeElement || Boolean(menuItemOpenedKey)) {
    emit('on-force-ball-position', null);
    return;
  }

  if (navigationMethod.value === 'mouse' && !isMouseInsideMenu.value) return;

  const container = activeElement.offsetParent;
  const containerRect = container.getBoundingClientRect();
  const boundingBox = activeElement.getBoundingClientRect();
  const top =
    ((boundingBox.top - containerRect.top + window.scrollY + 15) / containerRect.height) * 100;
  const left =
    ((boundingBox.left + boundingBox.width - containerRect.left + window.scrollX) /
      containerRect.width) *
    100;

  emit('on-force-ball-position', { x: left, y: top });
};

const handleMouseEnter = (event) => {
  if (navigationMethod.value !== 'mouse') {
    navigationMethod.value = 'mouse';
    activeRowIndex.value = null;
    activeItemIndex.value = null;
  }

  clearTimeout(forcedBallPositionUpdateTimeoutId.value);
  isMouseInsideMenu.value = true;
  forcedBallPositionUpdateTimeoutId.value = setTimeout(() => {
    updateForcedBallPosition(event.target);
  }, 350);
  menuItemDimensionsUpdateTimoutId.value = setTimeout(updateMenuItemDimensions, 450);
};

const handleMouseLeave = () => {
  emit('on-force-ball-position', null);
  isMouseInsideMenu.value = false;
};

const handleMenuOptionSelect = (optionKey) => {
  emit('on-menu-option-select', optionKey);
  menuItemClickedKey.value = optionKey;
  menuItemOpenedKey.value = optionKey;
  updateForcedBallPosition();
  setTimeout(() => (isDestroyed.value = true), 500);
};

const onMenuAnimationEnd = () => {
  menuItemClickedKey.value = null;
};

const onTransitionEnd = (event) => {
  if (event.target.classList.contains('menu')) {
    if (!props.isOpen) {
      isMenuHidden.value = true;
    }
  }
};

// Handle keyboard navigation
const handleKeydown = (event) => {
  if (isMenuHidden.value || !props.isOpen) return;

  if (navigationMethod.value !== 'keyboard') {
    navigationMethod.value = 'keyboard';
    activeRowIndex.value = 0;
    activeItemIndex.value = 0;
    const activeElement = menuItemRefs.value[activeRowIndex.value]?.[activeItemIndex.value];
    forcedBallPositionUpdateTimeoutId.value = setTimeout(
      () => updateForcedBallPosition(activeElement),
      350
    );
    menuItemDimensionsUpdateTimoutId.value = setTimeout(updateMenuItemDimensions, 450);
    return;
  }

  const rowCount = MENU_ITEMS.length;
  const itemCount = MENU_ITEMS[activeRowIndex.value]?.items.length || 0;

  clearTimeout(forcedBallPositionUpdateTimeoutId.value);

  switch (event.key) {
    case 'ArrowDown':
      activeRowIndex.value = (activeRowIndex.value + 1) % rowCount;
      activeItemIndex.value = 0;
      break;

    case 'ArrowUp':
      activeRowIndex.value = (activeRowIndex.value - 1 + rowCount) % rowCount;
      activeItemIndex.value = 0;
      break;

    case 'ArrowRight':
      activeItemIndex.value = (activeItemIndex.value + 1) % itemCount;
      break;

    case 'ArrowLeft':
      activeItemIndex.value = (activeItemIndex.value - 1 + itemCount) % itemCount;
      break;

    case 'Enter': {
      const activeItem = MENU_ITEMS[activeRowIndex.value]?.items[activeItemIndex.value];
      if (activeItem && !activeItem.disabled) {
        handleMenuOptionSelect(activeItem.key);
      }
      return;
    }

    default:
      break;
  }

  const activeElement = menuItemRefs.value[activeRowIndex.value]?.[activeItemIndex.value];
  forcedBallPositionUpdateTimeoutId.value = setTimeout(
    () => updateForcedBallPosition(activeElement),
    350
  );
};

// Save menu item id
watch(
  () => props.isOpen,
  (newValue) => {
    if (newValue) {
      updateMenuContainerDimensions();
      updateMenuItemDimensions();
      isMenuHidden.value = false;
    }

    if (!newValue) {
      setTimeout(closeMenuItem, 500);
    }
  }
);

onMounted(() => {
  updateMenuContainerDimensions();
  updateMenuItemDimensions();
  window.addEventListener('keydown', handleKeydown);
});

onUpdated(() => {
  updateMenuContainerDimensions();
  updateMenuItemDimensions();
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown);
  clearTimeout(forcedBallPositionUpdateTimeoutId.value);
  clearTimeout(menuItemDimensionsUpdateTimoutId.value);
});
</script>

<style scoped>
@keyframes button-blink {
  0% {
    transform: scale(1);
    background-color: var(--dark-color-opacity-50);
  }

  50% {
    transform: scale(0.98);
    background-color: var(--light-color-opacity-50);
  }

  100% {
    transform: scale(1);
    background-color: var(--dark-color-opacity-50);
  }
}

@keyframes button-blink-subtle {
  0% {
    transform: scale(1);
    opacity: 1;
  }

  50% {
    transform: scale(0.98);
    opacity: 0.7;
  }

  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.menu {
  --menu-container-width: unset;
  --menu-container-height: unset;
  --menu-item-top: unset;
  --menu-item-left: unset;
  --menu-item-width: unset;
  --menu-item-height: unset;

  position: absolute;
  z-index: 90;
  top: 0;
  left: 0;
  transform: scale(1.5);

  width: 100%;
  height: 100%;

  opacity: 0;
  background-color: var(--light-color-opacity-50);
  border-radius: 12px;

  transition: all 0.4s ease-in-out 0.4s;
}

.menu_open {
  transform: scale(1);
  opacity: 1;
  transition: all 0.2s ease-in-out;
}

.menu__container {
  display: flex;
  flex-direction: column;
  row-gap: var(--smaller-space);

  width: 100%;
  height: 100%;

  list-style: none;

  background-color: var(--dark-color-opacity-50);
  border-radius: 12px;
}

.menu__list {
  display: flex;
  flex-direction: row;
  column-gap: var(--smaller-space);

  height: 100%;

  list-style: none;
}

.menu__item {
  user-select: none;

  top: var(--menu-item-top);
  left: var(--menu-item-left);

  display: flex;
  flex: 1;
  flex-direction: column;
  row-gap: var(--smaller-space);

  height: 100%;

  transition: all 0.4s ease-in-out;
}

.menu__item:hover:not(.menu__item_opened),
.menu__item_active:not(.menu__item_opened) {
  cursor: pointer;
  flex: 2;
}

.menu__item_opened {
  flex: 0;
  width: 0;
  margin-left: calc(0px - var(--smaller-space));
}

.menu__item-content {
  position: absolute;
  z-index: -1;
  top: var(--menu-item-top);
  left: var(--menu-item-left);

  display: flex;
  flex-direction: column;
  row-gap: var(--regular-space);

  width: var(--menu-item-width);
  height: var(--menu-item-height);

  opacity: 0;

  transition: all 0.4s ease-in-out;
}

.menu__item_opened .menu__item-content {
  position: absolute;
  z-index: 900;
  top: 0;
  left: 0;

  width: var(--menu-container-width);
  height: var(--menu-container-height);
  padding: calc(var(--regular-space) + var(--smaller-space));

  opacity: 1;
  background-color: var(--dark-color-opacity-95);
  border-radius: 12px;

  transition: all 0.4s ease-in-out;
}

.menu__item-container {
  position: relative;

  width: 100%;
  height: 100%;
  padding: var(--regular-space);

  background-color: var(--dark-color-opacity-50);
  border-radius: 12px;

  transition: all 0.4s ease-in-out;
}

.menu__item:hover:not(.menu__item_opened) .menu__item-container,
.menu__item_active:not(.menu__item_opened) .menu__item-container {
  background-color: var(--dark-color-opacity-90);
}

.menu__item_opened .menu__item-container {
  display: none;
}

.menu__item_row_first .menu__item-container {
  border-radius: 0 0 12px 12px;
}

.menu__item_row_first:first-child .menu__item-container {
  border-radius: 12px 0;
}

.menu__item_row_first:last-child .menu__item-container {
  border-radius: 0 12px;
}

.menu__item_row_middle {
  border-radius: 12px;
}

.menu__item_row_middle:first-child .menu__item-container {
  border-radius: 0 12px 12px 0;
}

.menu__item_row_middle:last-child .menu__item-container {
  border-radius: 12px 0 0 12px;
}

.menu__item_row_last .menu__item-container {
  border-radius: 12px 12px 0 0;
}

.menu__item_row_last:first-child .menu__item-container {
  border-radius: 0 12px 0 0;
}

.menu__item_row_last:last-child .menu__item-container {
  border-radius: 12px 0;
}

.menu__item:hover .menu__item-container,
.menu__item_active .menu__item-container {
  background-color: var(--light-color-opacity-50);
  transition: all 0.4s ease-in-out;
}

.menu__item-button {
  all: unset;

  overflow: hidden;
  display: flex;
  flex-direction: column;
  row-gap: var(--small-space);

  width: calc(100% - 2 * 10px);
  height: calc(100% - 2 * 10px);
  padding: var(--smaller-space);

  background-color: transparent;
  border-radius: 12px;

  transition:
    transform 0.1s ease-in-out,
    box-shadow 0.1s ease-in-out;
}

.menu__item_active .menu__item-button {
  animation: button-blink-subtle 0.5s ease-in-out infinite;
}

.menu__item-button:disabled {
  cursor: not-allowed;
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

  opacity: 0;

  transition: opacity 0s ease-in-out;
}

.menu__item-description_short {
  max-width: 60%;
}

.menu__item:hover .menu__item-description,
.menu__item_active .menu__item-description {
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

.menu__item:hover .menu__item-icon_slide-bottom,
.menu__item_active .menu__item-icon_slide-bottom {
  top: 70%;
}

.menu__item:hover .menu__item-icon_slide-right,
.menu__item_active .menu__item-icon_slide-right {
  left: 80%;
}
</style>

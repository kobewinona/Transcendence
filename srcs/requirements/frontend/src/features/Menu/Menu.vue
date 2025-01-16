<script setup>
import { defineProps, onMounted, onUnmounted, ref, watch } from 'vue';

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
  'on-on-menu-option-select',
]);

const menuItemRefs = ref(Array.from({ length: MENU_ITEMS.length }, () => []));

const isMenuHidden = ref(false);
const menuItemClickedKey = ref(null);
const forcedBallPositionUpdateTimeoutId = ref(null);
const isMouseInsideMenu = ref(false);

const activeRowIndex = ref(null);
const activeItemIndex = ref(null);
const navigationMethod = ref('');

const updateForcedBallPosition = (activeElement) => {
  if (navigationMethod.value === 'mouse' && !isMouseInsideMenu.value) return;

  const container = activeElement.offsetParent;
  const containerRect = container.getBoundingClientRect();
  const boundingBox = activeElement.getBoundingClientRect();
  const top = ((boundingBox.top - containerRect.top + window.scrollY) / containerRect.height) * 100;
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
  forcedBallPositionUpdateTimeoutId.value = setTimeout(
    () => updateForcedBallPosition(event.target),
    300
  );
};

const handleMouseLeave = () => {
  emit('on-force-ball-position', null);
  isMouseInsideMenu.value = false;
};

const handleMenuOptionSelect = (optionKey) => {
  emit('on-on-menu-option-select', optionKey);
  menuItemClickedKey.value = optionKey;
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
      300
    );
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
    300
  );
};

watch(
  () => props.isOpen,
  (newValue) => {
    if (newValue) {
      isMenuHidden.value = false;
    }
  }
);

onMounted(() => {
  window.addEventListener('keydown', handleKeydown);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown);
  clearTimeout(forcedBallPositionUpdateTimeoutId.value);
});
</script>

<template>
  <div
    v-show="!isMenuHidden"
    class="menu"
    :class="{ menu_open: isOpen }"
    @transitionend="onTransitionEnd"
  >
    <div
      class="disabling-overlay"
      :class="{ 'disabling-overlay_active': navigationMethod === 'keyboard' }"
    />
    <ul class="menu-container">
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
            :ref="
              (el) => {
                menuItemRefs[rowIndex][itemIndex] = el;
              }
            "
            class="menu__item"
            :class="{ active: activeRowIndex === rowIndex && activeItemIndex === itemIndex }"
            @mouseenter="handleMouseEnter"
            @mouseleave="handleMouseLeave"
          >
            <button
              class="menu__item-button"
              :class="{
                'menu__item-button_clicked': menuItemClickedKey === item.key,
                active: activeRowIndex === rowIndex && activeItemIndex === itemIndex,
              }"
              :disabled="item.disabled"
              @click="() => handleMenuOptionSelect(item.key)"
              @animationend="onMenuAnimationEnd"
            >
              <span class="menu__item-title">{{ item.title }}</span>
              <span
                class="menu__item-description"
                :class="{
                  'menu__item-description_short': item.iconSlideTo === 'right',
                  active: activeRowIndex === rowIndex && activeItemIndex === itemIndex,
                }"
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
                  active: activeRowIndex === rowIndex && activeItemIndex === itemIndex,
                }"
              />
            </button>
          </li>
        </ul>
      </li>
    </ul>
  </div>
</template>

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
  position: absolute;
  z-index: 90;
  top: 0;
  left: 0;
  transform: scale(1.5);

  width: 100%;
  height: 100%;

  opacity: 0;
  background-color: var(--light-color-opacity-50);

  transition: all 0.4s ease-in-out 0.4s;
}

.menu_open {
  transform: scale(1);
  opacity: 1;
  transition: all 0.2s ease-in-out;
}

.menu-container {
  display: flex;
  flex-direction: column;
  row-gap: var(--smaller-space);

  width: 100%;
  height: 100%;

  background-color: var(--dark-color-opacity-50);
}

.menu__list {
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
  padding: var(--regular-space);

  background-color: var(--dark-color-opacity-50);

  transition: all 0.4s ease-in-out;
}

.menu__item:hover,
.menu__item.active {
  cursor: pointer;
  flex: 2;
  background-color: var(--light-color-opacity-50);
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

.menu__item-button_clicked {
  animation: button-blink 0.2s ease-in-out forwards;
}

.menu__item-button.active {
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
.menu__item-description.active {
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
.menu__item-icon_slide-bottom.active {
  top: 70%;
}

.menu__item:hover .menu__item-icon_slide-right,
.menu__item-icon_slide-right.active {
  left: 80%;
}
</style>

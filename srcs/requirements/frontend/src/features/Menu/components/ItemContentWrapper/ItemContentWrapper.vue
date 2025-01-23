<template>
  <div :class="[className, 'item-content', { 'item-content_opened': isOpen }]">
    <h1 class="item-content__title">{{ title }}</h1>
    <button class="item-content__close-btn" type="button" @click="onClose">
      <component
        :is="svgComponents['DeclineIcon']"
        v-if="isVueComponent(svgComponents['DeclineIcon'])"
        class="item-content__close-btn-icon"
      >
        svgComponents['DeclineIcon']
      </component>
    </button>
    <slot />
  </div>
</template>

<!--suppress JSFileReferences -->
<script setup>
import { svgComponents } from 'shared/lib';
import { isVueComponent } from 'shared/lib';
import { defineProps } from 'vue';

const { className, title, isOpen, onClose } = defineProps({
  className: {
    type: String,
    default: '',
  },
  title: {
    type: String,
    required: true,
  },
  isOpen: {
    type: Boolean,
    default: false,
  },
  onClose: {
    type: Function,
    default: () => {},
  },
});
</script>

<style scoped>
.item-content {
  position: absolute;
  z-index: -1;
  top: var(--menu-item-top);
  left: var(--menu-item-left);

  display: flex;
  flex-direction: column;
  row-gap: var(--big-space);

  width: var(--menu-item-width);
  height: var(--menu-item-height);

  opacity: 0;

  transition: all 0.4s ease-in-out;
}

/* noinspection CssUnusedSymbol */
.item-content_opened {
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

.item-content__close-btn {
  cursor: pointer;

  position: absolute;
  top: calc(var(--regular-space) + var(--smaller-space));
  right: calc(var(--regular-space) + var(--smaller-space));

  background-color: transparent;
  border: none;

  transition: opacity 0.2s ease-in-out;
}

.item-content__close-btn:hover {
  opacity: 0.5;
  transition: opacity 0.2s ease-in-out;
}

.item-content__close-btn-icon {
  max-width: 50px;
  max-height: 50px;
  fill: var(--light-color);
  stroke: var(--light-color);
}
</style>

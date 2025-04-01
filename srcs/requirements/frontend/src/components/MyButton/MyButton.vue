<template>
  <button
    :class="[
      className,
      'button',
      `button_color_${color}`,
      `button_size_${size}`,
      `button_variant_${variant}`,
      { button_clicked: animate },
    ]"
    :disabled="disabled"
    :tabindex="tabindex"
    :type="type"
    v-bind="attrs"
    @animationend="animate = false"
    @click="handleClick"
  >
    <component
      :is="icon"
      v-if="isVueComponent(icon) && !loading"
      key="button__icon"
      :class="['button__icon', { button__icon_alone: !hasDefaultSlot }, iconClassName]"
    />
    <img
      v-else-if="typeof icon === 'string' && !loading"
      :class="['button__img', { button__img_alone: !hasDefaultSlot }, iconClassName]"
      :src="icon"
      alt=""
    />
    <Loader :is-active="loading" />
    <span v-if="hasDefaultSlot" class="button__text">
      <slot />
    </span>
  </button>
</template>

<script setup>
import { Loader } from 'shared/components';
import { isVueComponent } from 'shared/lib';
import { ref, useAttrs, useSlots } from 'vue';

const slots = useSlots();
const attrs = useAttrs();

const { icon, disabled } = defineProps({
  className: {
    type: String,
    default: '',
  },
  iconClassName: {
    type: String,
    default: '',
  },
  tabindex: {
    type: Number,
    default: 1,
  },
  type: {
    type: String,
    default: 'button',
  },
  color: {
    type: String,
    default: 'primary',
    validator: (value) => value === 'primary' || value === 'secondary' || value === 'light',
  },
  size: {
    type: String,
    default: 'large',
    validator: (value) => value === 'large' || value === 'middle' || value === 'small',
  },
  variant: {
    type: String,
    default: 'default',
    validator: (value) => value === 'bordered' || value === 'default' || value === 'ghost',
  },
  text: {
    type: String,
    default: '',
  },
  icon: {
    type: Object || String,
    default: null,
  },
  loading: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
});

const hasDefaultSlot = !!slots.default;

const emit = defineEmits(['click']);

const animate = ref(false);

const handleClick = () => {
  animate.value = true;
  emit('click');
};
</script>

<!--suppress CssUnusedSymbol -->
<style scoped>
@keyframes press-fade {
  0% {
    transform: scale(0.9);
    opacity: 1;
  }

  100% {
    transform: scale(1.1);
    opacity: 0;
  }
}

.button {
  height: 44px;

  color: var(--light-color);

  font-size: 1.2rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;

  position: relative;

  flex-direction: row;
  justify-content: center;
  align-items: center;

  border: none;
  border-radius: 12px;

  transition: all 0.2s ease-in-out;
}

.button_color_primary {
  background-color: var(--primary-color);
}

.button_color_secondary {
  background-color: var(--secondary-color);
}

.button_color_light {
  color: var(--dark-color);
  background-color: var(--light-color);
}

.button_color_dark {
  color: var(--light-color);
  background-color: var(--dark-color);
}

.button_variant_bordered {
  border: 1px solid var(--light-color);
}

.button_color_dark.button_variant_bordered {
  color: var(--dark-color);
  background-color: var(--light-color);
  border: 1px solid var(--dark-color);
}

.button_color_light.button_variant_bordered {
  color: var(--light-color);
  background-color: var(--dark-color);
  border: 1px solid var(--light-color);
}

.button_variant_default {
  padding: var(--smaller-space) var(--big-space);
}

.button_variant_ghost {
  background-color: transparent;
  padding: 0 !important;
}

.button_size_large {
  height: 44px;
  padding: var(--small-space) var(--big-space);
}

.button_size_middle {
  height: 32px;
  font-size: 1rem;
  padding: var(--small-space) var(--smaller-space);
}

.button_size_small {
  height: 28px;
  font-size: 0.85rem;
  padding: var(--small-space) var(--small-space);
}

.button:hover:not(.button:disabled) {
  transition: filter 0.2s ease-in-out;
  filter: brightness(0.8);
}

.button_clicked::after {
  content: '';
  background: var(--light-color-opacity-50);

  position: absolute;
  border-radius: inherit;

  animation: press-fade 300ms ease;
  pointer-events: none;

  inset: 0;
}

.button:disabled {
  cursor: not-allowed;
  transition: filter 0.2s ease-in-out;
  filter: saturate(0.4);
}

button:disabled .icon {
  opacity: 0.4;
  transition: opacity;
}

.button__icon {
  width: 100%;
  height: 100%;
  margin-right: var(--smaller-space);
  fill: var(--light-color);
}

.button__icon_alone {
  margin-right: 0;
}

.button__img {
  aspect-ratio: 1 / 1;
  height: 100%;
  margin-right: var(--smaller-space);
}

.button__img_alone {
  margin-right: 0;
}

.button_color_light .icon {
  fill: var(--dark-color);
}

.button__text {
  white-space: nowrap;
  display: flex;
  flex-direction: row;
  column-gap: var(--smaller-space);

  align-items: center;
}
</style>

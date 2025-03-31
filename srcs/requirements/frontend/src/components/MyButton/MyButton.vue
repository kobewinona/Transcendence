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
    :tabindex="tabindex"
    :type="type"
    v-bind="attrs"
    :disabled="disabled"
    @click="handleClick"
    @animationend="animate = false"
  >
    <component
      :is="icon"
      v-if="isVueComponent(icon) && !loading"
      key="icon"
      :class="['icon', { icon_alone: !hasDefaultSlot }, iconClassName]"
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
    type: Object,
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
  cursor: pointer;

  position: relative;

  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;

  height: 44px;

  font-size: 1.2rem;
  font-weight: 600;
  color: var(--light-color);

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
  padding: 0 !important;
  background-color: transparent;
}

.button_size_large {
  height: 44px;
  padding: var(--small-space) var(--big-space);
}

.button_size_middle {
  height: 32px;
  padding: var(--small-space) var(--smaller-space);
  font-size: 1rem;
}

.button_size_small {
  height: 28px;
  padding: var(--small-space) var(--small-space);
  font-size: 0.85rem;
}

.button:hover:not(.button:disabled) {
  filter: brightness(0.8);
  transition: filter 0.2s ease-in-out;
}

.button_clicked::after {
  pointer-events: none;
  content: '';

  position: absolute;
  inset: 0;

  background: var(--light-color-opacity-50);
  border-radius: inherit;

  animation: press-fade 300ms ease;
}

.button:disabled {
  cursor: not-allowed;
  filter: saturate(0.4);
  transition: filter 0.2s ease-in-out;
}

button:disabled .icon {
  opacity: 0.4;
  transition: opacity;
}

.icon {
  width: 100%;
  height: 100%;
  margin-right: var(--smaller-space);
  fill: var(--light-color);
}

.icon_alone {
  margin-right: 0;
}

.button_color_light .icon {
  fill: var(--dark-color);
}

.button__text {
  white-space: nowrap;
}
</style>

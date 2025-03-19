<template>
  <button
    :class="[className, 'button', `button_color_${color}`]"
    :type="type"
    v-bind="attrs"
    @click="handleClick"
  >
    <TransitionGroup class="icon-wrapper" name="fade-scale" tag="span">
      <component :is="icon" v-if="isVueComponent(icon) && !loading" key="icon" class="icon" />
      <Loader v-if="loading" key="loader" :size="20" />
    </TransitionGroup>
    <span
      :class="{
        'button-text': true,
        'button-text_shifted': loading || (icon && isVueComponent(icon)),
      }"
    >
      <slot />
    </span>
  </button>
</template>

<script setup>
import { Loader } from 'shared/components';
import { isVueComponent } from 'shared/lib';
import { useAttrs } from 'vue';

const attrs = useAttrs();

const { icon } = defineProps({
  className: {
    type: String,
    default: '',
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
});

const emit = defineEmits(['click']);

const handleClick = () => {
  emit('click');
};
</script>

<!--suppress CssUnusedSymbol -->
<style scoped>
.button {
  cursor: pointer;

  display: flex;
  flex-direction: row;
  column-gap: var(--regular-space);
  align-items: center;
  justify-content: center;

  height: 44px;
  padding: var(--smaller-space) var(--big-space);

  font-size: 1.2rem;
  font-weight: 600;

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

.button:hover:not(.button:disabled) {
  filter: brightness(85%);
  transition: filter 0.2s ease-in-out;
}

.button:disabled {
  cursor: not-allowed;
  color: var(--dark-color-opacity-50);
  filter: grayscale(0.8);
  transition: all 0.4s ease-in-out;
}

.icon-wrapper {
  width: 20px;
  height: 20px;
}

.icon {
  width: 20px;
  height: 20px;
}

.button-text {
  transform: translateX(-20px);
  transition: all 0.1s ease-in-out;
}

.button-text_shifted {
  transform: translateX(0);
  transition: all 0.1s ease-in-out;
}

.fade-scale-enter-active,
.fade-scale-leave-active {
  transition:
    opacity 0.1s ease,
    transform 0.1s ease;
}

.fade-scale-enter-from,
.fade-scale-leave-to {
  transform: scale(0);
  opacity: 0;
}
</style>

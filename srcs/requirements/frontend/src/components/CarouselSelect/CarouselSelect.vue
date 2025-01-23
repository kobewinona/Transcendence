<template>
  <div class="carousel-select" :style="{ '--swipe-translate': swipeTranslateOffset }">
    <button class="carousel-select__button" @click="prevOption">
      <component
        :is="svgComponents['DownloadIcon']"
        v-if="isVueComponent(svgComponents['DownloadIcon'])"
        class="carousel-select__arrow carousel-select__arrow_left"
      />
    </button>
    <transition name="bubble-anim" mode="out-in">
      <div :key="activeValue" :class="['carousel-select__item', optionClassName]">
        <template v-if="slots.renderOption">
          <slot name="renderOption" :option="activeOption" />
        </template>
        <span v-else>
          {{ activeOption?.label }}
        </span>
      </div>
    </transition>
    <button class="carousel-select__button" @click="nextOption">
      <component
        :is="svgComponents['DownloadIcon']"
        v-if="isVueComponent(svgComponents['DownloadIcon'])"
        class="carousel-select__arrow carousel-select__arrow_right"
      />
    </button>
  </div>
</template>

<script setup>
// noinspection JSFileReferences
import { svgComponents } from 'shared/lib';
import { isVueComponent } from 'shared/lib';
import { computed, defineEmits, defineProps, ref, useSlots, watch } from 'vue';

const slots = useSlots();

const { optionClassName, value, options } = defineProps({
  optionClassName: {
    type: String,
    default: '',
  },
  value: {
    type: String || Number,
    default: undefined,
  },
  options: {
    type: Array,
    default: () => [],
  },
});

const emit = defineEmits(['update:value', 'on-change', 'render-option']);

const activeValue = ref(value);
const swipeTranslateOffset = ref('60%');
const activeOption = computed(() => options.find((option) => option.value === activeValue.value));

const prevOption = () => {
  swipeTranslateOffset.value = '-60%';
  const currentIndex = options.findIndex((option) => option.value === activeValue.value);
  const newIndex = (currentIndex - 1 + options.length) % options.length;
  updateValue(options[newIndex].value);
};

const nextOption = () => {
  swipeTranslateOffset.value = '60%';
  const currentIndex = options.findIndex((option) => option.value === activeValue.value);
  const newIndex = (currentIndex + 1) % options.length;
  updateValue(options[newIndex].value);
};

const updateValue = (newValue) => {
  activeValue.value = newValue;
  emit('update:value', newValue);
  emit(
    'on-change',
    options.find((option) => option.value === newValue)
  );
};

watch(
  () => value,
  (newValue) => {
    activeValue.value = newValue;
  }
);
</script>

<!--suppress CssUnusedSymbol -->
<style scoped>
.carousel-select {
  --swipe-translate: ;

  display: flex;
  flex-direction: row;
  column-gap: var(--regular-space);
  align-items: center;
}

.carousel-select__button {
  cursor: pointer;
  background-color: transparent;
  border: none;
  transition: opacity 0.2s ease-in-out;
}

.carousel-select__button:hover {
  opacity: 0.5;
  transition: opacity 0.2s ease-in-out;
}

.carousel-select__item {
  overflow: hidden;
  width: 100%;
}

.carousel-select__arrow {
  width: 30px;
  height: 30px;
  fill: var(--light-color);
  stroke: var(--light-color);
}

.carousel-select__arrow_left {
  transform: rotate(90deg);
}

.carousel-select__arrow_right {
  transform: rotate(-90deg);
}

.bubble-anim-enter-active,
.bubble-anim-leave-active {
  transition:
    transform 0.1s ease,
    opacity 0.1s ease;
}

.bubble-anim-enter-from {
  transform: scale(0.8) translateX(calc(var(--swipe-translate) * -1));
  opacity: 0;
}

.bubble-anim-leave-to {
  transform: scale(0.8) translateX(var(--swipe-translate));
  opacity: 0;
}

.bubble-anim-enter-to,
.bubble-anim-leave-from {
  transform: scale(1);
  opacity: 1;
}
</style>

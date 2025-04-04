<template>
  <div class="carousel-select" :style="{ '--swipe-translate': swipeTranslateOffset }">
    <MyButton
      type="button"
      variant="ghost"
      :icon="svgComponents['ArrowLeftIcon']"
      aria-label="Previous Option."
      @click="prevOption"
    />
    <transition name="bubble-anim" mode="out-in">
      <div :key="activeValue" :class="['carousel-select__item', optionClassName]">
        <template v-if="slots.renderOption">
          <slot name="renderOption" :option="activeOption" />
        </template>
        <span v-else class="carousel-select__item-text">
          {{ t(activeOption?.label || '') }}
        </span>
      </div>
    </transition>
    <MyButton
      type="button"
      variant="ghost"
      :icon="svgComponents['ArrowRightIcon']"
      aria-label="Next Option."
      @click="nextOption"
    />
  </div>
</template>

<script setup>
// noinspection JSFileReferences
import { MyButton } from 'components';
import { svgComponents } from 'shared/lib';
import { computed, ref, useSlots, watch } from 'vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

const slots = useSlots();

const { optionClassName, defaultValue, value, options } = defineProps({
  optionClassName: {
    type: String,
    default: '',
  },
  name: {
    type: String,
    default: undefined,
  },
  defaultValue: {
    type: [String, Number],
    default: undefined,
  },
  value: {
    type: [String, Number],
    default: undefined,
  },
  options: {
    type: Array,
    default: () => [],
  },
});

const emit = defineEmits(['update:value', 'on-change', 'render-option']);

const activeValue = ref(value || defaultValue || options[0]?.value);
const swipeTranslateOffset = ref('60%');
const activeOption = computed(() => options.find((option) => option.value === activeValue.value));

const updateValue = (newValue) => {
  activeValue.value = newValue.value;
  emit('update:value', newValue);
  emit('on-change', newValue);
};

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

  font-size: 0;

  background-color: transparent;
  border: none;

  transition: opacity 0.2s ease-in-out;
}

.carousel-select__button:hover {
  opacity: 0.7;
  transition: opacity 0.2s ease-in-out;
}

.carousel-select__item {
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;

  width: 100%;
}

.carousel-select__item-text {
  text-align: center;
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

::v-deep(.carousel-select__btn-icon) {
  width: 34px !important;
  height: 34px !important;
}

::v-deep(.carousel-select__btn-icon_next) {
  rotate: -90deg;
}

::v-deep(.carousel-select__btn-icon_prev) {
  rotate: 90deg;
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

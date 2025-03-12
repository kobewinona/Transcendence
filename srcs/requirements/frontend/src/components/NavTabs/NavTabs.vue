<template>
  <div class="nav-tabs">
    <div class="nav-tabs__active-tab-marker" :style="markerStyle" />
    <ul class="nav-tabs__tabs">
      <li v-for="(tab, index) in tabs" :key="tab.value" class="nav-tabs__tabs-item">
        <button
          :ref="(el) => (tabRefs[index] = el)"
          :class="['nav-tabs__tab', { 'nav-tabs__tab_active': activeTab.value === tab.value }]"
          type="button"
          @click="handleChange(tab)"
        >
          {{ t(tab.label) }}
        </button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { isEqual } from 'lodash';
import { onUnmounted, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

const { tabs } = defineProps({
  tabs: {
    type: Array,
    required: true,
  },
});

const emit = defineEmits(['on-change']);

const tabRefs = ref([]);
const activeTab = ref(tabs[0]);
const markerStyle = ref({});
const timeoutId = ref(null);

watch(
  () => activeTab.value,
  () => {
    timeoutId.value = setTimeout(() => {
      const activeIndex = tabs.findIndex((tab) => isEqual(tab, activeTab.value));
      const activeElement = tabRefs.value[activeIndex];

      if (!activeElement) return;

      const rect = activeElement.getBoundingClientRect();

      markerStyle.value = {
        width: `${rect.width}px`,
        transform: `translate(${activeElement.offsetLeft}px, ${activeElement.offsetTop}px)`,
      };
    }, 100);
  },
  { immediate: true }
);

const handleChange = (newTab) => {
  activeTab.value = newTab;
  emit('on-change', newTab);
};

onUnmounted(() => clearTimeout(timeoutId.value));
</script>

<!--suppress CssUnusedSymbol -->
<style scoped>
.nav-tabs {
  position: relative;
}

.nav-tabs__tabs {
  display: flex;
  flex-direction: row;

  width: 100%;
  height: 100%;
  padding: 0;

  list-style: none;
}

.nav-tabs__tabs-item {
  height: 100%;
}

.nav-tabs__active-tab-marker {
  position: absolute;
  z-index: 300;

  height: 44px;

  background-color: var(--light-color);
  border-radius: 12px;

  transition: all 0.2s ease-in-out;
}

.nav-tabs__tab {
  cursor: pointer;

  position: relative;
  z-index: 400;

  height: 100%;
  padding: var(--smaller-space) var(--big-space);

  font-size: 1.2rem;
  font-weight: 500;

  background-color: transparent;
  border: none;

  transition: all 0.2s ease-in-out;
}

.nav-tabs__tab:hover:not(.nav-tabs__tab_active) {
  opacity: 0.7;
  transition: all 0.2s ease-in-out;
}

.nav-tabs__tab_active {
  color: var(--dark-color);
}
</style>

<template>
  <div class="scroll-layout">
    <div
      :class="['scroll-layout__shadow', 'scroll-layout__shadow_top']"
      :style="{ opacity: topShadowOpacity }"
    />
    <div ref="contentContainer" class="scroll-layout__content" @scroll.passive="handleScroll">
      <div ref="content" class="scroll-layout__content-ref">
        <slot ref="content" />
      </div>
    </div>
    <div
      :class="['scroll-layout__shadow', 'scroll-layout__shadow_bottom']"
      :style="{ opacity: bottomShadowOpacity }"
    />
  </div>
</template>

<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref } from 'vue';

const contentContainer = ref(null);
const content = ref(null);
const topShadowOpacity = ref(0);
const bottomShadowOpacity = ref(0);

const maxDistance = 50;
let resizeObserver;

const handleScroll = () => {
  // noinspection JSUnresolvedReference
  const el = contentContainer.value;
  if (!el) return;

  const scrollTop = el.scrollTop;
  const scrollHeight = el.scrollHeight;
  const clientHeight = el.clientHeight;
  const scrollBottom = scrollHeight - scrollTop - clientHeight;

  topShadowOpacity.value = Math.min(1, scrollTop / maxDistance);
  bottomShadowOpacity.value = Math.min(1, scrollBottom / maxDistance);
};

onMounted(() => {
  nextTick(() => {
    handleScroll();

    resizeObserver = new ResizeObserver(() => {
      handleScroll();
    });

    // noinspection JSUnresolvedReference
    if (content.value) {
      resizeObserver.observe(content.value);
    }
  });
});

onBeforeUnmount(() => {
  resizeObserver?.disconnect();
});
</script>

<style scoped>
.scroll-layout {
  position: relative;

  overflow: hidden;

  height: 100%;
  min-height: 0;

  border-radius: 12px;
}

.scroll-layout__content {
  scrollbar-gutter: stable;

  overflow: hidden auto;

  width: 100%;
  height: 100%;
  min-height: 0;
}

.scroll-layout__content-ref {
  height: 100%;
}

.scroll-layout__shadow {
  pointer-events: none;

  position: absolute;
  z-index: 100;
  right: 0;
  left: 0;

  height: 44px;

  transition: opacity 0.2s ease;
}

.scroll-layout__shadow_top {
  top: 0;
  background: linear-gradient(to bottom, var(--dark-color), transparent);
}

.scroll-layout__shadow_bottom {
  bottom: 0;
  background: linear-gradient(to top, var(--dark-color), transparent);
}
</style>

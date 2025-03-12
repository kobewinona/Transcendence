<template>
  <NoCursorOverlay />
  <GrainOverlay />

  <MainLayout>
    <router-view />
  </MainLayout>

  <ErrorModalProvider ref="errorModalRef" />
  <NotificationProvider ref="notificationRef" />
</template>

<script setup>
import { NotificationProvider } from 'components';
import { ErrorModalProvider } from 'features';
import { MainLayout } from 'layouts';
import { GrainOverlay, NoCursorOverlay } from 'shared/components';
import { provideLang } from 'shared/composables';
import { onMounted, provide, ref } from 'vue';

import { i18n } from './main.js';

const errorModalRef = ref(null);
const notificationRef = ref(null);

// provide('showErrorModal', errorModalRef.value?.showErrorModal);

provide('notify', (message, type) => {
  notificationRef.value?.notify(message, type);
});

provideLang(i18n);

onMounted(() => {
  provide('showErrorModal', errorModalRef.value?.showErrorModal);
});
</script>

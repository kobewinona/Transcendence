<template>
  <NoCursorOverlay />
  <GrainOverlay />

  <MainLayout>
    <router-view />
  </MainLayout>

  <ErrorModalProvider ref="errorModalRef" />
  <ConfirmModalProvider ref="confirmModalRef" />
  <NotificationProvider ref="notificationRef" />
</template>

<script setup>
import { NotificationProvider } from 'components';
import { ConfirmModalProvider, ErrorModalProvider } from 'features';
import { MainLayout } from 'layouts';
import { GrainOverlay, NoCursorOverlay } from 'shared/components';
import { provideLang } from 'shared/composables';
import { onMounted, provide, ref } from 'vue';

import { i18n } from './main.js';

const errorModalRef = ref(null);
const confirmModalRef = ref(null);
const notificationRef = ref(null);

provide('notify', (message, type) => {
  // noinspection JSUnresolvedReference
  notificationRef.value?.notify(message, type);
});

provideLang(i18n);

onMounted(() => {
  // noinspection JSUnresolvedReference
  provide('showErrorModal', errorModalRef.value?.showErrorModal);
  // noinspection JSUnresolvedReference
  provide('showConfirmModal', confirmModalRef.value?.showConfirmModal);
});
</script>

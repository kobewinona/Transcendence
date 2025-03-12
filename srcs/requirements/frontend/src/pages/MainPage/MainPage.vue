<template>
  <Section />
</template>

<script setup>
import { provideGameSocket } from 'entities/Game/composables';

import { Section } from './ui';

provideGameSocket(import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws/pong/');
</script>

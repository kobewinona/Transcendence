<template>
  <Section />
</template>

<script setup>
import { WS_HOST } from 'config/constants.js';
import { provideGameSocket } from 'entities/Game/composables';

import { Section } from './ui';

provideGameSocket(`${WS_HOST}/ws/pong/`);
</script>

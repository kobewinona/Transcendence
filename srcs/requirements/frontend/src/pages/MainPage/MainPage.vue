<template>
  <Game />
  <Menu />
</template>

<script setup>
import { WS_HOST } from 'config/constants.js';
import { provideGameSocket } from 'entities/Game/composables';
import { Game } from 'features';
import { Menu } from 'widgets';

provideGameSocket(`${WS_HOST}/ws/pong/`);
</script>

<script setup>
import { Game } from 'features';
// import BallTest from 'features/Game/components/BallTest/BallTest.vue';
</script>

<template>
  <main class="layout">
    <Game />
    <!--    <BallTest />-->
  </main>
</template>

<style scoped>
.layout {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 100%;
  height: 100%;

  background: linear-gradient(to right, var(--dark-color) 50%, var(--light-color) 50%);
}
</style>

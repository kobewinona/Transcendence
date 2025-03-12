<template>
  <main class="main">
    <section class="main__container">
      <slot />
    </section>
  </main>
</template>

<script setup></script>

<style scoped>
.main {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 100%;
  height: 100%;

  background: linear-gradient(90deg, var(--dark-color) 50%, var(--light-color) 50%);
}

.main__container {
  position: relative;
  aspect-ratio: 4 / 3;
  height: 90%;
  border-radius: 12px;
}
</style>

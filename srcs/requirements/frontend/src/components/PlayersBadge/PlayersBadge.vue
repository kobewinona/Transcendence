<template>
  <span class="players-badge">
    <component
      :is="svgComponents['OnePlayerIcon']"
      v-if="maxPlayers === 1"
      class="players-badge__icon"
    />
    <component
      :is="svgComponents['ManyPlayersIcon']"
      v-else-if="maxPlayers > 4"
      class="players-badge__icon"
    />
    <component
      :is="svgComponents['MorePlayersIcon']"
      v-else-if="maxPlayers === null"
      class="players-badge__icon"
    />
    <span class="players-badge__text">{{ textString }}</span>
  </span>
</template>

<script setup>
import { svgComponents } from 'shared/lib/index.js';

const { minPlayers, maxPlayers } = defineProps({
  minPlayers: {
    type: Number,
    required: true,
  },
  maxPlayers: {
    type: Number || null,
    required: true,
  },
});

let textString = minPlayers;
if (maxPlayers > 4) {
  textString = `${minPlayers}-${maxPlayers}`;
} else if (maxPlayers === null) {
  textString = `> ${minPlayers}`;
}
</script>

<style scoped>
.players-badge {
  display: flex;
  flex-direction: row;
  column-gap: var(--small-space);
  align-items: center;

  height: max-content;
}

.players-badge__icon {
  width: 20px;
  height: 20px;
  fill: var(--light-color);
}

.players-badge__text {
  font-size: 0.85rem;
  white-space: nowrap;
}
</style>

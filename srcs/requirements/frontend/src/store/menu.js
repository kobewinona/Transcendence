import { reactive } from 'vue';
import { LOADING_LAYER, MENU_LAYER_KEYS, MENU_LAYERS } from 'widgets/Menu/config/constants.js';

let loadingTimer = null;
let loadingStartTime = null;
let closePending = false;

export const menu = reactive({
  stack: [],

  isLoading: false,
  isOpen: true,
  layerKey: null,

  open() {
    this.isOpen = true;
  },

  close() {
    if (this.isLoading) {
      closePending = true;
      this.release();
    } else {
      this.isOpen = false;
    }
  },

  goTo(layerKey, props = {}) {
    this.stack.push(MENU_LAYERS(props)[layerKey]);
  },

  goBack() {
    this.stack.pop();
    this.cleanupGhostLayers();
  },

  hold() {
    if (this.stack.length < 1) return;

    if (loadingTimer) {
      clearTimeout(loadingTimer);
    }

    if (this.currentLayer.key === MENU_LAYER_KEYS.LOADING) return;

    this.stack.push(LOADING_LAYER(this.currentLayer.key));
    this.isLoading = true;
    loadingStartTime = Date.now();
  },

  release() {
    if (loadingTimer) {
      clearTimeout(loadingTimer);
    }

    if (this.currentLayer.key !== MENU_LAYER_KEYS.LOADING) return;

    const elapsed = Date.now() - loadingStartTime;
    const remaining = Math.max(400 - elapsed, 0);

    loadingTimer = setTimeout(() => {
      this.stack.pop();
      this.isLoading = false;
      this.cleanupGhostLayers();

      if (closePending) {
        this.isOpen = false;
        closePending = false;
      }
    }, remaining);
  },

  reset() {
    this.stack = [];
    this.isLoading = false;
  },

  cleanupGhostLayers() {
    while (this.stack.length > 0) {
      const top = this.stack[this.stack.length - 1];
      if (top?.ghost) {
        this.stack.pop();
      } else {
        break;
      }
    }
  },

  get layers() {
    return this.stack;
  },

  get currentLayer() {
    const len = this.stack.length;
    if (len === 0) return {};

    const last = this.stack[len - 1];
    if (last === MENU_LAYER_KEYS.LOADING && len > 1) {
      return this.stack[len - 2];
    }

    return last;
  },
});

import vue from '@vitejs/plugin-vue';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true,
        changeOrigin: true,
      },
    },
  },
  resolve: {
    alias: {
      '@': '/src',
      pages: '/src/pages',
      features: '/src/features',
      entities: '/src/entities',
      components: '/src/components',
      assets: '/src/assets',
    },
  },
});

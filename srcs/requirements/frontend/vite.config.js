import vue from '@vitejs/plugin-vue';
import { defineConfig } from 'vite';
import svgLoader from 'vite-svg-loader';

export default defineConfig({
  base: '/',
  publicDir: 'public',
  plugins: [vue(), svgLoader()],
  server: {
    mimeTypes: {
      ttf: 'font/ttf',
      woff: 'font/woff',
      woff2: 'font/woff2',
    },
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
      api: '/src/api',
      pages: '/src/pages',
      features: '/src/features',
      entities: '/src/entities',
      components: '/src/components',
      shared: '/src/shared',
      layouts: '/src/layouts',
      assets: '/src/assets',
      config: '/src/config',
      store: '/src/store',
    },
  },
});

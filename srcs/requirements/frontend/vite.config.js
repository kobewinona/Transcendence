/* eslint-disable no-undef */
import vue from '@vitejs/plugin-vue';
import * as path from 'path';
import { defineConfig } from 'vite';
import svgLoader from 'vite-svg-loader';

// noinspection JSUnusedGlobalSymbols,JSCheckFunctionSignatures
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
      '/v1/randomuser': {
        target: 'https://api.api-ninjas.com',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/v1\/randomuser/, '/v1/randomuser'),
      },
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
      api: path.resolve(__dirname, 'src/api'),
      pages: path.resolve(__dirname, 'src/pages'),
      widgets: path.resolve(__dirname, 'src/widgets'),
      features: path.resolve(__dirname, 'src/features'),
      entities: path.resolve(__dirname, 'src/entities'),
      components: path.resolve(__dirname, 'src/components'),
      shared: path.resolve(__dirname, 'src/shared'),
      layouts: path.resolve(__dirname, 'src/layouts'),
      assets: path.resolve(__dirname, 'src/assets'),
      config: path.resolve(__dirname, 'src/config'),
      store: path.resolve(__dirname, 'src/store'),
    },
  },
});

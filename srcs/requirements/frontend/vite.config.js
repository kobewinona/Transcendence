import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': '/src',
      'pages': '/src/pages',
      'features': '/src/features',
      'entities': '/src/entities',
      'components': '/src/components',
    }
  }
})

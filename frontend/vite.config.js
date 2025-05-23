import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueJsx(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/auth': {
        target: 'http://localhost:81',
        changeOrigin: true,
        rewrite: path => path.replace(/^\/auth/, '/auth')
      },
      '/user': {
        target: 'http://localhost:81',
        changeOrigin: true
      },
      '/device': {
        target: 'http://localhost:81',
        changeOrigin: true
      }
    }
  }
})

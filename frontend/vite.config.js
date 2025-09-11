import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      manifest: false, // a saját site.webmanifest fájlod lesz használva
      includeAssets: [
        'favicon.ico',
        'apple-touch-icon.png',
        'android-chrome-192x192.png',
        'android-chrome-512x512.png'
      ],
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg}']
      }
    })
  ],
  server: {
    host: true // <- ezt meghagyjuk
  }
})

import autoprefixer from 'autoprefixer'
import { defineConfig } from 'vite'
import { resolve } from 'path' 

export default defineConfig ({

  server: {
    origin: 'http://localhost:5173',
  },

  build: {
    outDir: "static/dist",
    assetsDir: "assets",
    emptyOutDir: true,
    target: "es2015",
    
    rollupOptions: { 
      input: {
        main: "./src/js/main.js",
        styles: "./src/styles/main.scss"
      },
      output: {
        entryFileNames: '[name].js',
      }
    }
  },

  css: {
    postcss: {
      plugins: [autoprefixer()]
    }
  },

  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
      '@styles': resolve(__dirname, 'src/styles'),
      '@fonts': resolve(__dirname, 'static/fonts'),
      '@images': resolve(__dirname, 'static/images'),
    }
  }
})
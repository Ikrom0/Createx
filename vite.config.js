import autoprefixer from 'autoprefixer'
import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({

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
      },
      output: {
        entryFileNames: '[name].js',
        assetFileNames: (assetInfo) => {
          if (assetInfo.name === 'main.css') {
            return 'assets/main.css';
          }

          return 'assets/[name]-[hash][extname]';
        },
      },
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
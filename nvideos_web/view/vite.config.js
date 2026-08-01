import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [
    tailwindcss(),
    react()
  ],
  build: {
    outDir: '.',
    emptyOutDir: false,
    rollupOptions: {
      input: {
        //Base
        'base/main': './base/css/main.css',
        'base/avatar_entry': './home/entries/avatar_entry.jsx'
      },
      output: {
        entryFileNames: (chunkInfo)=>{
          const [module, name] = chunkInfo.name.split('/');
          return `${module}/static/${name}.js`;
        },
        assetFileNames: (chunkInfo)=>{
          const [module, name] = chunkInfo.name.split('/');
          return `${module}/static/${name}.[ext]`;
        }
      }
    }
  }
})
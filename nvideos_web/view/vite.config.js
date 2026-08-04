import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import obfuscator from 'rollup-plugin-obfuscator';

export default defineConfig({
    plugins: [
        tailwindcss(),
        react()
    ],
    build: {
        sourcemap: process.env.NODE_ENV !== "production",
        outDir: '.',
        emptyOutDir: false,
            rollupOptions: {
            plugins: [
                process.env.NODE_ENV === "production" ? obfuscator({
                    include: [
                        //Home
                        './home/entries/user_registration/user_register_form_validation.js',
                        './home/entries/user_registration/user_avatar_upload_media_server.js'
                    ],
                    compact: true,
                    controlFlowFlattening: true,
                }) : null
            ],
            input: {
                //Base
                'base/main': './base/css/main.css',
                
                //Home
                'home/avatar_entry': './home/entries/avatar_entry.jsx',
                'home/user_register_form_validation/ufrv': './home/entries/user_registration/user_register_form_validation.js',
                'home/user_avatar_upload_media_server/uavms': './home/entries/user_registration/user_avatar_upload_media_server.js'
            },
            output: {
                entryFileNames: (chunkInfo) => {
                    const chunkName = chunkInfo.name.split('/');
                    if (chunkName.length == 3) {
                        const [module, name, subName] = chunkInfo.name.split('/');
                        return `${module}/static/dist/${subName}.js`;
                    }
                    const [module, name] = chunkInfo.name.split('/');
                    return `${module}/static/dist/${name}.js`;
                },
                assetFileNames: (chunkInfo) => {
                    const [module, name] = chunkInfo.name.split('/');
                    return `${module}/static/dist/${name}`;
                }
            }
        }
    }
})